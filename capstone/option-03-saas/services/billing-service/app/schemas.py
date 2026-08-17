from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field


class PlanResponse(BaseModel):
    id: str
    name: str
    monthly_price: Decimal
    included_units: int
    overage_price: Decimal

    class Config:
        from_attributes = True


class SubscribeRequest(BaseModel):
    tenant_id: str
    plan_name: str = "starter"


class SubscriptionResponse(BaseModel):
    id: str
    tenant_id: str
    plan_id: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class InvoiceResponse(BaseModel):
    id: str
    tenant_id: str
    amount: Decimal
    description: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class CloudEvent(BaseModel):
    source: str
    detail_type: str = Field(alias="detail-type")
    detail: dict[str, Any]

    class Config:
        populate_by_name = True
