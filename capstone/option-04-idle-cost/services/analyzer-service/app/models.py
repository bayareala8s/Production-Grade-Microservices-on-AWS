import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, DateTime, Numeric, String, Text

from app.database import Base


class FindingModel(Base):
    __tablename__ = "findings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    scan_id = Column(String, nullable=False, index=True)
    resource_type = Column(String, nullable=False)
    resource_id = Column(String, nullable=False)
    idle_score = Column(Numeric(4, 2), nullable=False)
    estimated_monthly_usd = Column(Numeric(10, 2), nullable=False)
    reason = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
