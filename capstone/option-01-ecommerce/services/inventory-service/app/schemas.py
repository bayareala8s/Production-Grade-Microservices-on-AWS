from pydantic import BaseModel, Field


class InventoryResponse(BaseModel):
    product_id: str
    available: int
    reserved: int

    class Config:
        from_attributes = True


class UpsertInventory(BaseModel):
    product_id: str
    available: int = Field(ge=0)


class ReserveRequest(BaseModel):
    quantity: int = Field(ge=1)
    order_id: str | None = None


class ReserveResponse(BaseModel):
    product_id: str
    quantity: int
    available: int
    reserved: int
    status: str
