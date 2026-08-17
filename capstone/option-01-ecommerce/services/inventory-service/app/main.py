import os
from contextlib import asynccontextmanager

import httpx
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine, get_db
from app.models import InventoryModel
from app.schemas import (
    InventoryResponse,
    ReserveRequest,
    ReserveResponse,
    UpsertInventory,
)

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:8002")


def seed_from_catalog(db: Session) -> None:
    """Seed inventory rows from product-service when empty (retry for compose startup)."""
    if db.query(InventoryModel).count() > 0:
        return
    products = []
    for _ in range(10):
        try:
            with httpx.Client(timeout=3.0) as client:
                response = client.get(f"{PRODUCT_SERVICE_URL}/products")
                if response.status_code == 200:
                    products = response.json()
                    if products:
                        break
        except Exception:
            pass
        import time

        time.sleep(1)
    if not products:
        return
    for p in products:
        db.add(
            InventoryModel(
                product_id=p["id"],
                available=int(p.get("stock", 0)),
                reserved=0,
            )
        )
    db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_from_catalog(db)
    finally:
        db.close()
    yield


app = FastAPI(title="Inventory Service", version="1.0.0", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok", "service": "inventory-service"}


@app.get("/inventory", response_model=list[InventoryResponse])
def list_inventory(db: Session = Depends(get_db)):
    return db.query(InventoryModel).all()


@app.get("/inventory/{product_id}", response_model=InventoryResponse)
def get_inventory(product_id: str, db: Session = Depends(get_db)):
    row = db.query(InventoryModel).filter(InventoryModel.product_id == product_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Inventory not found for product")
    return row


@app.put("/inventory/{product_id}", response_model=InventoryResponse)
def upsert_inventory(product_id: str, payload: UpsertInventory, db: Session = Depends(get_db)):
    if payload.product_id != product_id:
        raise HTTPException(status_code=400, detail="product_id mismatch")
    row = db.query(InventoryModel).filter(InventoryModel.product_id == product_id).first()
    if row:
        row.available = payload.available
    else:
        row = InventoryModel(product_id=product_id, available=payload.available, reserved=0)
        db.add(row)
    db.commit()
    db.refresh(row)
    return row


@app.post(
    "/inventory/{product_id}/reserve",
    response_model=ReserveResponse,
    status_code=status.HTTP_200_OK,
)
def reserve_stock(product_id: str, payload: ReserveRequest, db: Session = Depends(get_db)):
    row = db.query(InventoryModel).filter(InventoryModel.product_id == product_id).first()
    if not row:
        raise HTTPException(status_code=404, detail=f"No inventory for product {product_id}")
    if row.available < payload.quantity:
        raise HTTPException(
            status_code=409,
            detail=f"Insufficient stock: available={row.available}, requested={payload.quantity}",
        )
    row.available -= payload.quantity
    row.reserved += payload.quantity
    db.commit()
    db.refresh(row)
    return ReserveResponse(
        product_id=product_id,
        quantity=payload.quantity,
        available=row.available,
        reserved=row.reserved,
        status="RESERVED",
    )


@app.post(
    "/inventory/{product_id}/release",
    response_model=ReserveResponse,
)
def release_stock(product_id: str, payload: ReserveRequest, db: Session = Depends(get_db)):
    row = db.query(InventoryModel).filter(InventoryModel.product_id == product_id).first()
    if not row:
        raise HTTPException(status_code=404, detail=f"No inventory for product {product_id}")
    release_qty = min(payload.quantity, row.reserved)
    row.reserved -= release_qty
    row.available += release_qty
    db.commit()
    db.refresh(row)
    return ReserveResponse(
        product_id=product_id,
        quantity=release_qty,
        available=row.available,
        reserved=row.reserved,
        status="RELEASED",
    )
