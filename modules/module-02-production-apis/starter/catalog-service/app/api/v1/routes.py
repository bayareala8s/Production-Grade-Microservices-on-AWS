import uuid
from typing import Dict, List

from fastapi import APIRouter, HTTPException, status

from app.api.v1.schemas import ProductCreateV1, ProductV1


router = APIRouter(prefix="/api/v1", tags=["catalog-v1"])

# NOTE: in later modules this becomes DynamoDB/RDS per-service.
_PRODUCTS: Dict[str, ProductV1] = {}


@router.get("/products", response_model=List[ProductV1])
def list_products() -> List[ProductV1]:
    return list(_PRODUCTS.values())


@router.post("/products", response_model=ProductV1, status_code=status.HTTP_201_CREATED)
def create_product(body: ProductCreateV1) -> ProductV1:
    pid = str(uuid.uuid4())
    p = ProductV1(id=pid, name=body.name, price_usd=body.price_usd)
    _PRODUCTS[pid] = p
    return p


@router.get("/products/{product_id}", response_model=ProductV1)
def get_product(product_id: str) -> ProductV1:
    p = _PRODUCTS.get(product_id)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return p


