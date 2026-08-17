from datetime import datetime

from pydantic import BaseModel, Field


class TenantCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)


class TenantResponse(BaseModel):
    id: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


class InviteRequest(BaseModel):
    email: str
    role: str = "member"


class MemberResponse(BaseModel):
    id: str
    tenant_id: str
    email: str
    role: str
    status: str

    class Config:
        from_attributes = True
