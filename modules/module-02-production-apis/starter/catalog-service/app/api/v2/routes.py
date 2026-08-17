import uuid
from typing import Dict, List

from fastapi import APIRouter, HTTPException, status

from app.api.v2.schemas import Money, ProductCreateV2, ProductV2


router = APIRouter(prefix="/api/v2", tags=["catalog-v2"])

# NOTE: intentionally separate in-memory store to keep v1/v2 shapes decoupled for the lab.
_PRODUCTS: Dict[str, ProductV2] = {}


@router.get("/products", response_model=List[ProductV2])
def list_products() -> List[ProductV2]:
    return list(_PRODUCTS.values())


@router.post("/products", response_model=ProductV2, status_code=status.HTTP_201_CREATED)
def create_product(body: ProductCreateV2) -> ProductV2:
    pid = str(uuid.uuid4())
    p = ProductV2(id=pid, name=body.name, price=body.price)
    _PRODUCTS[pid] = p
    return p


@router.get("/products/{product_id}", response_model=ProductV2)
def get_product(product_id: str) -> ProductV2:
    p = _PRODUCTS.get(product_id)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return p


@router.post("/products/{product_id}/discount", response_model=ProductV2)
def apply_discount(product_id: str, percent: float = 10.0) -> ProductV2:
    """
    Example of a v2-only endpoint that changes behavior without impacting v1 consumers.
    """
    if percent <= 0 or percent >= 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid discount percent")
    p = _PRODUCTS.get(product_id)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    discounted = p.price.amount * (1 - (percent / 100.0))
    p.price = Money(amount=discounted, currency=p.price.currency)
    _PRODUCTS[product_id] = p
    return p


