import json

from fastapi import Depends, FastAPI, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.discover import discover, publish_scan_completed
from app.models import ResourceModel, ScanModel

app = FastAPI(title="Inventory Service", version="1.0.0")
Base.metadata.create_all(bind=engine)


class ScanRequest(BaseModel):
    aws_account_id: str = Field(default="123456789012", min_length=12, max_length=12)


class ScanResponse(BaseModel):
    id: str
    aws_account_id: str
    mode: str
    status: str
    resource_count: int


@app.get("/health")
def health():
    return {"status": "ok", "service": "inventory-service"}


@app.post("/scans", response_model=ScanResponse, status_code=status.HTTP_201_CREATED)
def start_scan(payload: ScanRequest, db: Session = Depends(get_db)):
    mode, resources = discover()
    scan = ScanModel(
        aws_account_id=payload.aws_account_id,
        mode=mode,
        status="COMPLETED",
        resource_count=len(resources),
    )
    db.add(scan)
    db.flush()
    for r in resources:
        db.add(
            ResourceModel(
                scan_id=scan.id,
                resource_type=r["resource_type"],
                resource_id=r["resource_id"],
                region=r.get("region", "us-east-1"),
                name=r.get("name"),
                signals=json.dumps(r.get("signals", {})),
            )
        )
    db.commit()
    db.refresh(scan)
    publish_scan_completed(scan.id, payload.aws_account_id, resources)
    return ScanResponse(
        id=scan.id,
        aws_account_id=scan.aws_account_id,
        mode=scan.mode,
        status=scan.status,
        resource_count=int(scan.resource_count),
    )


@app.get("/scans/{scan_id}/resources")
def list_resources(scan_id: str, db: Session = Depends(get_db)):
    rows = db.query(ResourceModel).filter(ResourceModel.scan_id == scan_id).all()
    return {
        "scan_id": scan_id,
        "resources": [
            {
                "resource_type": r.resource_type,
                "resource_id": r.resource_id,
                "region": r.region,
                "name": r.name,
                "signals": json.loads(r.signals),
            }
            for r in rows
        ],
    }


@app.get("/resources")
def list_latest_resources(db: Session = Depends(get_db)):
    latest = db.query(ScanModel).order_by(ScanModel.created_at.desc()).first()
    if not latest:
        return {"scan_id": None, "resources": []}
    return list_resources(latest.id, db)
