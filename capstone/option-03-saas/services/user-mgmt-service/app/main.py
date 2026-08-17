from fastapi import Depends, FastAPI, Header, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import os

from app.database import Base, engine, get_db
from app.models import MemberModel, TenantModel
from app.schemas import InviteRequest, MemberResponse, TenantCreate, TenantResponse

app = FastAPI(title="User Management Service", version="1.0.0")
Base.metadata.create_all(bind=engine)

JWT_SECRET = os.getenv("JWT_SECRET", "saas-dev-secret-change-me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


def optional_tenant_from_token(authorization: str | None = Header(default=None)) -> str | None:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.split(" ", 1)[1]
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM]).get("tenant_id")
    except JWTError:
        return None


@app.get("/health")
def health():
    return {"status": "ok", "service": "user-mgmt-service"}


@app.post("/tenants", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
def create_tenant(payload: TenantCreate, db: Session = Depends(get_db)):
    tenant = TenantModel(name=payload.name)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant


@app.get("/tenants/{tenant_id}", response_model=TenantResponse)
def get_tenant(tenant_id: str, db: Session = Depends(get_db)):
    tenant = db.query(TenantModel).filter(TenantModel.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


@app.post(
    "/tenants/{tenant_id}/invites",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def invite_member(
    tenant_id: str,
    payload: InviteRequest,
    db: Session = Depends(get_db),
    token_tenant: str | None = Depends(optional_tenant_from_token),
):
    if token_tenant and token_tenant != tenant_id:
        raise HTTPException(status_code=403, detail="Cross-tenant invite forbidden")
    if not db.query(TenantModel).filter(TenantModel.id == tenant_id).first():
        raise HTTPException(status_code=404, detail="Tenant not found")
    existing = (
        db.query(MemberModel)
        .filter(MemberModel.tenant_id == tenant_id, MemberModel.email == payload.email)
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="Member already invited")
    member = MemberModel(tenant_id=tenant_id, email=payload.email, role=payload.role, status="INVITED")
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


@app.get("/tenants/{tenant_id}/members", response_model=list[MemberResponse])
def list_members(
    tenant_id: str,
    db: Session = Depends(get_db),
    token_tenant: str | None = Depends(optional_tenant_from_token),
):
    if token_tenant and token_tenant != tenant_id:
        raise HTTPException(status_code=403, detail="Cross-tenant access forbidden")
    return db.query(MemberModel).filter(MemberModel.tenant_id == tenant_id).all()
