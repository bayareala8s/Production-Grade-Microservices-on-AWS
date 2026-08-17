from sqlalchemy import Column, Integer, String

from app.database import Base


class InventoryModel(Base):
    __tablename__ = "inventory"

    product_id = Column(String, primary_key=True)
    available = Column(Integer, nullable=False, default=0)
    reserved = Column(Integer, nullable=False, default=0)
