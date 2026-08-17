from datetime import datetime

from pydantic import BaseModel, Field


class UsageRecordRequest(BaseModel):
    tenant_id: str
    metric: str = "api_calls"
    units: int = Field(ge=1)


class UsageEventResponse(BaseModel):
    id: str
    tenant_id: str
    metric: str
    units: int
    created_at: datetime

    class Config:
        from_attributes = True
