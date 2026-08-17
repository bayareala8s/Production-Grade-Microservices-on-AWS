import os
from decimal import Decimal

import httpx
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import AccountModel, LedgerEntryModel, TransferModel
from app.schemas import AccountCreate, AccountResponse, TransferCreate, TransferResponse

app = FastAPI(title="Payment Service", version="1.0.0")
Base.metadata.create_all(bind=engine)

CUSTOMER_SERVICE_URL = os.getenv("CUSTOMER_SERVICE_URL", "http://localhost:8011")
EVENT_HTTP_ENDPOINT = os.getenv(
    "EVENT_HTTP_ENDPOINT", "http://localhost:8014/events"
)
FRAUD_HIGH_AMOUNT = Decimal(os.getenv("FRAUD_HIGH_AMOUNT", "10000"))


def require_approved_customer(customer_id: str) -> None:
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}")
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Customer service unavailable: {exc}",
        ) from exc
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Customer not found")
    response.raise_for_status()
    if response.json().get("kyc_status") != "APPROVED":
        raise HTTPException(status_code=403, detail="Customer KYC not approved")


def publish_payment_event(transfer: TransferModel, from_customer_id: str) -> None:
    payload = {
        "source": "capstone.banking.payments",
        "detail-type": "PaymentPlaced",
        "detail": {
            "transfer_id": transfer.id,
            "from_account_id": transfer.from_account_id,
            "to_account_id": transfer.to_account_id,
            "amount": str(transfer.amount),
            "currency": transfer.currency,
            "customer_id": from_customer_id,
            "high_value": transfer.amount >= FRAUD_HIGH_AMOUNT,
        },
    }
    try:
        with httpx.Client(timeout=10.0) as client:
            client.post(EVENT_HTTP_ENDPOINT, json=payload).raise_for_status()
    except Exception:
        # Event fan-out failure should not roll back committed ledger (teaching note)
        pass


@app.get("/health")
def health():
    return {"status": "ok", "service": "payment-service"}


@app.post("/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(payload: AccountCreate, db: Session = Depends(get_db)):
    require_approved_customer(payload.customer_id)
    account = AccountModel(
        customer_id=payload.customer_id,
        currency=payload.currency,
        balance=payload.initial_balance,
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@app.get("/accounts/{account_id}", response_model=AccountResponse)
def get_account(account_id: str, db: Session = Depends(get_db)):
    account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@app.post("/transfers", response_model=TransferResponse, status_code=status.HTTP_201_CREATED)
def create_transfer(payload: TransferCreate, db: Session = Depends(get_db)):
    if payload.from_account_id == payload.to_account_id:
        raise HTTPException(status_code=400, detail="Cannot transfer to same account")

    from_acct = db.query(AccountModel).filter(AccountModel.id == payload.from_account_id).first()
    to_acct = db.query(AccountModel).filter(AccountModel.id == payload.to_account_id).first()
    if not from_acct or not to_acct:
        raise HTTPException(status_code=404, detail="Account not found")
    if from_acct.currency != to_acct.currency:
        raise HTTPException(status_code=400, detail="Currency mismatch")
    if from_acct.balance < payload.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # Double-entry ledger within one service (bounded context)
    from_acct.balance = Decimal(from_acct.balance) - payload.amount
    to_acct.balance = Decimal(to_acct.balance) + payload.amount
    transfer = TransferModel(
        from_account_id=from_acct.id,
        to_account_id=to_acct.id,
        amount=payload.amount,
        currency=from_acct.currency,
        status="COMPLETED",
    )
    db.add(transfer)
    db.flush()
    db.add(
        LedgerEntryModel(
            transfer_id=transfer.id,
            account_id=from_acct.id,
            entry_type="DEBIT",
            amount=payload.amount,
        )
    )
    db.add(
        LedgerEntryModel(
            transfer_id=transfer.id,
            account_id=to_acct.id,
            entry_type="CREDIT",
            amount=payload.amount,
        )
    )
    db.commit()
    db.refresh(transfer)

    publish_payment_event(transfer, from_acct.customer_id)
    return transfer


@app.get("/transfers/{transfer_id}", response_model=TransferResponse)
def get_transfer(transfer_id: str, db: Session = Depends(get_db)):
    transfer = db.query(TransferModel).filter(TransferModel.id == transfer_id).first()
    if not transfer:
        raise HTTPException(status_code=404, detail="Transfer not found")
    return transfer


@app.get("/transfers/{transfer_id}/ledger")
def get_ledger(transfer_id: str, db: Session = Depends(get_db)):
    entries = (
        db.query(LedgerEntryModel)
        .filter(LedgerEntryModel.transfer_id == transfer_id)
        .all()
    )
    return {
        "transfer_id": transfer_id,
        "entries": [
            {
                "id": e.id,
                "account_id": e.account_id,
                "entry_type": e.entry_type,
                "amount": str(e.amount),
            }
            for e in entries
        ],
    }
