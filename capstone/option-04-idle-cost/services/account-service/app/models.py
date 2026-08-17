import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String

from app.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    org_id = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class LinkedAccountModel(Base):
    __tablename__ = "linked_accounts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    org_id = Column(String, nullable=False, index=True)
    aws_account_id = Column(String, nullable=False)
    role_arn = Column(String, nullable=True)
    mode = Column(String, nullable=False, default="read_only")
    created_at = Column(DateTime, default=datetime.utcnow)
