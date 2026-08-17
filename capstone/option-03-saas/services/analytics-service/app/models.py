import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.database import Base


class UsageEventModel(Base):
    __tablename__ = "usage_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, nullable=False, index=True)
    metric = Column(String, nullable=False)
    units = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
