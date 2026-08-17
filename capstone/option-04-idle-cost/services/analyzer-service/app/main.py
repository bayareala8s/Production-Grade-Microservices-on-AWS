import os
from decimal import Decimal
from typing import Any

import httpx
from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import FindingModel
from app.scoring import score_resource

app = FastAPI(title="Analyzer Service", version="1.0.0")
Base.metadata.create_all(bind=engine)

RECOMMENDATION_EVENT_URL = os.getenv(
    "RECOMMENDATION_EVENT_URL", "http://localhost:8034/events"
)


class CloudEvent(BaseModel):
    source: str
    detail_type: str = Field(alias="detail-type")
    detail: dict[str, Any]

    class Config:
        populate_by_name = True


def publish_scored(scan_id: str, findings: list[dict[str, Any]]) -> None:
    payload = {
        "source": "capstone.finops.analyzer",
        "detail-type": "IdleCostScored",
        "detail": {"scan_id": scan_id, "findings": findings},
    }
    try:
        with httpx.Client(timeout=10.0) as client:
            client.post(RECOMMENDATION_EVENT_URL, json=payload).raise_for_status()
    except Exception:
        pass


@app.get("/health")
def health():
    return {"status": "ok", "service": "analyzer-service"}


@app.post("/events")
def receive_scan(event: CloudEvent, db: Session = Depends(get_db)):
    if event.detail_type != "InventoryScanCompleted":
        return {"status": "ignored"}
    scan_id = event.detail["scan_id"]
    findings_out = []
    for resource in event.detail.get("resources", []):
        scored = score_resource(resource)
        if not scored:
            continue
        row = FindingModel(
            scan_id=scan_id,
            resource_type=scored["resource_type"],
            resource_id=scored["resource_id"],
            idle_score=scored["idle_score"],
            estimated_monthly_usd=scored["estimated_monthly_usd"],
            reason=scored["reason"],
        )
        db.add(row)
        findings_out.append(
            {
                "resource_type": scored["resource_type"],
                "resource_id": scored["resource_id"],
                "idle_score": float(scored["idle_score"]),
                "estimated_monthly_usd": float(scored["estimated_monthly_usd"]),
                "reason": scored["reason"],
            }
        )
    db.commit()
    publish_scored(scan_id, findings_out)
    total = sum(Decimal(str(f["estimated_monthly_usd"])) for f in findings_out)
    return {
        "status": "scored",
        "scan_id": scan_id,
        "finding_count": len(findings_out),
        "estimated_monthly_usd_total": str(total.quantize(Decimal("0.01"))),
    }


@app.get("/findings/{scan_id}")
def get_findings(scan_id: str, db: Session = Depends(get_db)):
    rows = db.query(FindingModel).filter(FindingModel.scan_id == scan_id).all()
    return {
        "scan_id": scan_id,
        "findings": [
            {
                "resource_type": r.resource_type,
                "resource_id": r.resource_id,
                "idle_score": float(r.idle_score),
                "estimated_monthly_usd": float(r.estimated_monthly_usd),
                "reason": r.reason,
            }
            for r in rows
        ],
        "estimated_monthly_usd_total": float(
            sum((r.estimated_monthly_usd for r in rows), Decimal("0"))
        ),
    }
