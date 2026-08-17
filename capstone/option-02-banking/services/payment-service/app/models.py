import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, DateTime, Numeric, String

from app.database import Base


class AccountModel(Base):
    __tablename__ = "accounts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String, nullable=False, index=True)
    currency = Column(String, nullable=False, default="USD")
    balance = Column(Numeric(18, 2), nullable=False, default=Decimal("0.00"))
    created_at = Column(DateTime, default=datetime.utcnow)


class TransferModel(Base):
    __tablename__ = "transfers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    from_account_id = Column(String, nullable=False)
    to_account_id = Column(String, nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    currency = Column(String, nullable=False, default="USD")
    status = Column(String, nullable=False, default="COMPLETED")
    created_at = Column(DateTime, default=datetime.utcnow)


class LedgerEntryModel(Base):
    """Double-entry: each transfer creates debit + credit lines."""

    __tablename__ = "ledger_entries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    transfer_id = Column(String, nullable=False, index=True)
    account_id = Column(String, nullable=False, index=True)
    entry_type = Column(String, nullable=False)  # DEBIT or CREDIT
    amount = Column(Numeric(18, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
