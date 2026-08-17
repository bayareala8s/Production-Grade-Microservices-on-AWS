import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, String, Text

from app.database import Base


class ScanModel(Base):
    __tablename__ = "scans"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    aws_account_id = Column(String, nullable=False)
    mode = Column(String, nullable=False, default="mock")
    status = Column(String, nullable=False, default="COMPLETED")
    resource_count = Column(Float, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class ResourceModel(Base):
    __tablename__ = "resources"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    scan_id = Column(String, nullable=False, index=True)
    resource_type = Column(String, nullable=False)  # NAT | ALB | ECS_SERVICE | EIP
    resource_id = Column(String, nullable=False)
    region = Column(String, nullable=False, default="us-east-1")
    name = Column(String, nullable=True)
    signals = Column(Text, nullable=False, default="{}")  # JSON signals for analyzer
    created_at = Column(DateTime, default=datetime.utcnow)
