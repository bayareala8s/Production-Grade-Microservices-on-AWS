from pydantic import BaseModel, Field


class ProductCreateV1(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    price_usd: float = Field(gt=0)


class ProductV1(BaseModel):
    id: str
    name: str
    price_usd: float


