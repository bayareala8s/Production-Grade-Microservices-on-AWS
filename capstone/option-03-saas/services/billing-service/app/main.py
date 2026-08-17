from contextlib import asynccontextmanager
from decimal import Decimal

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine, get_db
from app.models import InvoiceModel, PlanModel, SubscriptionModel
from app.schemas import (
    CloudEvent,
    InvoiceResponse,
    PlanResponse,
    SubscribeRequest,
    SubscriptionResponse,
)


def seed_plans(db: Session) -> None:
    if db.query(PlanModel).count() > 0:
        return
    db.add_all(
        [
            PlanModel(
                name="starter",
                monthly_price=Decimal("29.00"),
                included_units=1000,
                overage_price=Decimal("0.02"),
            ),
            PlanModel(
                name="growth",
                monthly_price=Decimal("99.00"),
                included_units=10000,
                overage_price=Decimal("0.01"),
            ),
        ]
    )
    db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_plans(db)
    finally:
        db.close()
    yield


app = FastAPI(title="Billing Service", version="1.0.0", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok", "service": "billing-service"}


@app.get("/plans", response_model=list[PlanResponse])
def list_plans(db: Session = Depends(get_db)):
    return db.query(PlanModel).all()


@app.post(
    "/subscriptions",
    response_model=SubscriptionResponse,
    status_code=status.HTTP_201_CREATED,
)
def subscribe(payload: SubscribeRequest, db: Session = Depends(get_db)):
    plan = db.query(PlanModel).filter(PlanModel.name == payload.plan_name).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    existing = (
        db.query(SubscriptionModel)
        .filter(
            SubscriptionModel.tenant_id == payload.tenant_id,
            SubscriptionModel.status == "ACTIVE",
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="Active subscription exists")
    sub = SubscriptionModel(tenant_id=payload.tenant_id, plan_id=plan.id, status="ACTIVE")
    db.add(sub)
    # Base monthly invoice
    db.add(
        InvoiceModel(
            tenant_id=payload.tenant_id,
            amount=plan.monthly_price,
            description=f"Subscription {plan.name} monthly",
            status="OPEN",
        )
    )
    db.commit()
    db.refresh(sub)
    return sub


@app.get("/tenants/{tenant_id}/invoices", response_model=list[InvoiceResponse])
def list_invoices(tenant_id: str, db: Session = Depends(get_db)):
    return (
        db.query(InvoiceModel)
        .filter(InvoiceModel.tenant_id == tenant_id)
        .order_by(InvoiceModel.created_at.desc())
        .all()
    )


@app.post("/events")
def receive_usage_event(event: CloudEvent, db: Session = Depends(get_db)):
    if event.detail_type != "UsageRecorded":
        return {"status": "ignored"}
    detail = event.detail
    tenant_id = detail.get("tenant_id")
    units = int(detail.get("units", 0))
    if not tenant_id or units <= 0:
        raise HTTPException(status_code=400, detail="Invalid usage detail")

    sub = (
        db.query(SubscriptionModel)
        .filter(SubscriptionModel.tenant_id == tenant_id, SubscriptionModel.status == "ACTIVE")
        .first()
    )
    if not sub:
        raise HTTPException(status_code=404, detail="No active subscription for tenant")
    plan = db.query(PlanModel).filter(PlanModel.id == sub.plan_id).first()
    overage = max(0, units - plan.included_units)
    amount = (Decimal(overage) * Decimal(plan.overage_price)).quantize(Decimal("0.01"))
    if amount <= 0:
        return {"status": "no_overage", "units": units}

    invoice = InvoiceModel(
        tenant_id=tenant_id,
        amount=amount,
        description=f"Usage overage {overage} units",
        status="OPEN",
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return {"status": "invoiced", "invoice_id": invoice.id, "amount": str(invoice.amount)}
