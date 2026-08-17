from datetime import datetime

from pydantic import BaseModel, Field


class CustomerCreate(BaseModel):
    email: str = Field(min_length=5, max_length=200)
    full_name: str = Field(min_length=2, max_length=120)


class CustomerResponse(BaseModel):
    id: str
    email: str
    full_name: str
    kyc_status: str
    created_at: datetime

    class Config:
        from_attributes = True


class KycUpdate(BaseModel):
    kyc_status: str = Field(pattern="^(PENDING|APPROVED|REJECTED)$")
