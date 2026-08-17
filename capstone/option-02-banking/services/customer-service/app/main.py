from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import CustomerModel
from app.schemas import CustomerCreate, CustomerResponse, KycUpdate

app = FastAPI(title="Customer Service", version="1.0.0")
Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok", "service": "customer-service"}


@app.post("/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    existing = db.query(CustomerModel).filter(CustomerModel.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    customer = CustomerModel(
        email=payload.email,
        full_name=payload.full_name,
        kyc_status="PENDING",
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.patch("/customers/{customer_id}/kyc", response_model=CustomerResponse)
def update_kyc(customer_id: str, payload: KycUpdate, db: Session = Depends(get_db)):
    customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer.kyc_status = payload.kyc_status
    db.commit()
    db.refresh(customer)
    return customer
