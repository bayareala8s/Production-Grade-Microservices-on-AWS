from pydantic import BaseModel, Field


class Money(BaseModel):
    amount: float = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3, description="ISO-4217 currency code")


class ProductCreateV2(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    price: Money


class ProductV2(BaseModel):
    id: str
    name: str
    price: Money


