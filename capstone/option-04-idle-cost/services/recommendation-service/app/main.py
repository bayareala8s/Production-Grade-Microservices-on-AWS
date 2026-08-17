import os
from typing import Any

import httpx
from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import RecommendationModel

app = FastAPI(title="Recommendation Service", version="1.0.0")
Base.metadata.create_all(bind=engine)

NOTIFY_EVENT_URL = os.getenv("NOTIFY_EVENT_URL", "http://localhost:8035/events")

ACTION_MAP = {
    "NAT": "stop_nat_or_platform",
    "ALB": "destroy_alb_when_stopped",
    "ECS_SERVICE": "scale_desired_count_to_zero",
    "EIP": "release_eip",
}


class CloudEvent(BaseModel):
    source: str
    detail_type: str = Field(alias="detail-type")
    detail: dict[str, Any]

    class Config:
        populate_by_name = True


def severity_for(score: float) -> str:
    if score >= 0.9:
        return "HIGH"
    if score >= 0.7:
        return "MEDIUM"
    return "LOW"


def publish_finding(rec: dict[str, Any]) -> None:
    payload = {
        "source": "capstone.finops.recommendation",
        "detail-type": "IdleCostFinding",
        "detail": rec,
    }
    try:
        with httpx.Client(timeout=10.0) as client:
            client.post(NOTIFY_EVENT_URL, json=payload)
    except Exception:
        pass


@app.get("/health")
def health():
    return {"status": "ok", "service": "recommendation-service"}


@app.post("/events")
def receive_scored(event: CloudEvent, db: Session = Depends(get_db)):
    if event.detail_type != "IdleCostScored":
        return {"status": "ignored"}
    scan_id = event.detail["scan_id"]
    created = []
    for f in sorted(
        event.detail.get("findings", []),
        key=lambda x: x.get("estimated_monthly_usd", 0),
        reverse=True,
    ):
        action = ACTION_MAP.get(f["resource_type"], "review_manually")
        rec = RecommendationModel(
            scan_id=scan_id,
            resource_type=f["resource_type"],
            resource_id=f["resource_id"],
            action=action,
            severity=severity_for(float(f.get("idle_score", 0))),
            estimated_monthly_usd=f["estimated_monthly_usd"],
            rationale=f.get("reason", ""),
        )
        db.add(rec)
        db.flush()
        item = {
            "id": rec.id,
            "scan_id": scan_id,
            "resource_type": rec.resource_type,
            "resource_id": rec.resource_id,
            "action": rec.action,
            "severity": rec.severity,
            "estimated_monthly_usd": float(rec.estimated_monthly_usd),
            "rationale": rec.rationale,
            "auto_destroy": False,
        }
        created.append(item)
        publish_finding(item)
    db.commit()
    return {"status": "recommended", "count": len(created), "recommendations": created}


@app.get("/recommendations")
def list_recommendations(db: Session = Depends(get_db)):
    rows = db.query(RecommendationModel).order_by(RecommendationModel.created_at.desc()).limit(50).all()
    return {
        "recommendations": [
            {
                "id": r.id,
                "scan_id": r.scan_id,
                "resource_type": r.resource_type,
                "resource_id": r.resource_id,
                "action": r.action,
                "severity": r.severity,
                "estimated_monthly_usd": float(r.estimated_monthly_usd),
                "rationale": r.rationale,
                "auto_destroy": False,
            }
            for r in rows
        ]
    }
