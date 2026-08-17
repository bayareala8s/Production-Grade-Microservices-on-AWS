import os

import httpx
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.events import publish_event
from app.models import OrderItemModel, OrderModel
from app.schemas import OrderCreate, OrderItemResponse, OrderResponse

app = FastAPI(title="Order Service", version="1.0.0")
Base.metadata.create_all(bind=engine)

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:8002")
INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL", "")


def fetch_product(product_id: str) -> dict:
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Product service unavailable: {exc}",
        ) from exc

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    if response.status_code >= 500:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Product service returned an error",
        )
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Product service returned an error",
        ) from exc
    return response.json()


def reserve_inventory(product_id: str, quantity: int, order_id: str | None = None) -> None:
    """When INVENTORY_SERVICE_URL is set (capstone Option 1), reserve stock there."""
    if not INVENTORY_SERVICE_URL:
        return
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                f"{INVENTORY_SERVICE_URL}/inventory/{product_id}/reserve",
                json={"quantity": quantity, "order_id": order_id},
            )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Inventory service unavailable: {exc}",
        ) from exc
    if response.status_code == 409:
        raise HTTPException(status_code=400, detail=response.json().get("detail", "Insufficient stock"))
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"No inventory for product {product_id}")
    if response.status_code >= 500:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Inventory service returned an error",
        )
    response.raise_for_status()


@app.get("/health")
def health():
    return {"status": "ok", "service": "order-service"}


@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    order_items = []
    total = 0.0

    for item in payload.items:
        product = fetch_product(item.product_id)
        if INVENTORY_SERVICE_URL:
            reserve_inventory(item.product_id, item.quantity)
        elif product["stock"] < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product['name']}",
            )
        line_total = product["price"] * item.quantity
        total += line_total
        order_items.append(
            OrderItemModel(
                product_id=product["id"],
                product_name=product["name"],
                quantity=item.quantity,
                unit_price=product["price"],
            )
        )

    order = OrderModel(user_id=payload.user_id, total=total, status="PLACED", items=order_items)
    db.add(order)
    db.commit()
    db.refresh(order)

    publish_event(
        source="course.orders",
        detail_type="OrderPlaced",
        detail={
            "order_id": order.id,
            "user_id": order.user_id,
            "total": order.total,
            "items": [
                {
                    "product_id": i.product_id,
                    "product_name": i.product_name,
                    "quantity": i.quantity,
                }
                for i in order.items
            ],
        },
    )

    return _to_response(order)


@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return _to_response(order)


def _to_response(order: OrderModel) -> OrderResponse:
    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        status=order.status,
        total=order.total,
        created_at=order.created_at,
        items=[
            OrderItemResponse(
                product_id=i.product_id,
                product_name=i.product_name,
                quantity=i.quantity,
                unit_price=i.unit_price,
            )
            for i in order.items
        ],
    )
