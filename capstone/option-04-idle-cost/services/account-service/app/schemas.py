from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(min_length=8)
    org_id: str = "default-org"


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    org_id: str


class LinkAccountRequest(BaseModel):
    aws_account_id: str = Field(min_length=12, max_length=12)
    role_arn: str | None = None


class LinkedAccountResponse(BaseModel):
    id: str
    org_id: str
    aws_account_id: str
    role_arn: str | None
    mode: str

    class Config:
        from_attributes = True
