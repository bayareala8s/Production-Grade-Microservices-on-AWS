from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class AccountCreate(BaseModel):
    customer_id: str
    currency: str = "USD"
    initial_balance: Decimal = Field(default=Decimal("0.00"), ge=0)


class AccountResponse(BaseModel):
    id: str
    customer_id: str
    currency: str
    balance: Decimal
    created_at: datetime

    class Config:
        from_attributes = True


class TransferCreate(BaseModel):
    from_account_id: str
    to_account_id: str
    amount: Decimal = Field(gt=0)


class TransferResponse(BaseModel):
    id: str
    from_account_id: str
    to_account_id: str
    amount: Decimal
    currency: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
