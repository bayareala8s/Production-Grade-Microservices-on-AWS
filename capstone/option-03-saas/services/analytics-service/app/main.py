import os

import httpx
from fastapi import Depends, FastAPI, Header, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import UsageEventModel
from app.schemas import UsageEventResponse, UsageRecordRequest

app = FastAPI(title="Analytics Service", version="1.0.0")
Base.metadata.create_all(bind=engine)

BILLING_EVENT_URL = os.getenv("BILLING_EVENT_URL", "http://localhost:8022/events")
JWT_SECRET = os.getenv("JWT_SECRET", "saas-dev-secret-change-me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


def tenant_from_token(authorization: str | None = Header(default=None)) -> str | None:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    try:
        return jwt.decode(
            authorization.split(" ", 1)[1], JWT_SECRET, algorithms=[JWT_ALGORITHM]
        ).get("tenant_id")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def publish_usage(tenant_id: str, units: int, metric: str) -> None:
    payload = {
        "source": "capstone.saas.analytics",
        "detail-type": "UsageRecorded",
        "detail": {"tenant_id": tenant_id, "units": units, "metric": metric},
    }
    try:
        with httpx.Client(timeout=10.0) as client:
            client.post(BILLING_EVENT_URL, json=payload).raise_for_status()
    except Exception:
        pass


@app.get("/health")
def health():
    return {"status": "ok", "service": "analytics-service"}


@app.get("/", response_class=None)
def welcome():
    return {
        "title": "Option 3 — SaaS Platform",
        "services": {
            "auth": 8025,
            "billing": 8022,
            "user_mgmt": 8023,
            "analytics": 8024,
        },
    }


@app.post("/usage", response_model=UsageEventResponse, status_code=status.HTTP_201_CREATED)
def record_usage(
    payload: UsageRecordRequest,
    db: Session = Depends(get_db),
    token_tenant: str | None = Depends(tenant_from_token),
):
    if token_tenant and token_tenant != payload.tenant_id:
        raise HTTPException(status_code=403, detail="Cross-tenant usage forbidden")
    event = UsageEventModel(
        tenant_id=payload.tenant_id,
        metric=payload.metric,
        units=payload.units,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    publish_usage(payload.tenant_id, payload.units, payload.metric)
    return event


@app.get("/tenants/{tenant_id}/usage", response_model=list[UsageEventResponse])
def list_usage(
    tenant_id: str,
    db: Session = Depends(get_db),
    token_tenant: str | None = Depends(tenant_from_token),
):
    if token_tenant and token_tenant != tenant_id:
        raise HTTPException(status_code=403, detail="Cross-tenant access forbidden")
    return (
        db.query(UsageEventModel)
        .filter(UsageEventModel.tenant_id == tenant_id)
        .order_by(UsageEventModel.created_at.desc())
        .all()
    )
