from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import LinkedAccountModel, UserModel
from app.schemas import (
    LinkAccountRequest,
    LinkedAccountResponse,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)
from app.security import create_token, hash_password, verify_password

app = FastAPI(title="Account Service", version="1.0.0")
Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok", "service": "account-service"}


@app.post("/users", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(UserModel).filter(UserModel.email == payload.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    user = UserModel(
        email=payload.email,
        password_hash=hash_password(payload.password),
        org_id=payload.org_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "email": user.email, "org_id": user.org_id}


@app.post("/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(access_token=create_token(user.id, user.org_id), org_id=user.org_id)


@app.post(
    "/accounts/link",
    response_model=LinkedAccountResponse,
    status_code=status.HTTP_201_CREATED,
)
def link_account(payload: LinkAccountRequest, db: Session = Depends(get_db), org_id: str = "default-org"):
    # Teaching MVP: org_id query/default — production would use JWT
    linked = LinkedAccountModel(
        org_id=org_id,
        aws_account_id=payload.aws_account_id,
        role_arn=payload.role_arn,
        mode="read_only",
    )
    db.add(linked)
    db.commit()
    db.refresh(linked)
    return linked


@app.get("/accounts", response_model=list[LinkedAccountResponse])
def list_accounts(org_id: str = "default-org", db: Session = Depends(get_db)):
    return db.query(LinkedAccountModel).filter(LinkedAccountModel.org_id == org_id).all()
