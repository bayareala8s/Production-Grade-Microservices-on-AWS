import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, UniqueConstraint

from app.database import Base


class TenantModel(Base):
    __tablename__ = "tenants"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class MemberModel(Base):
    __tablename__ = "members"
    __table_args__ = (UniqueConstraint("tenant_id", "email", name="uq_tenant_email"),)

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False)
    role = Column(String, nullable=False, default="member")
    status = Column(String, nullable=False, default="INVITED")
    created_at = Column(DateTime, default=datetime.utcnow)
