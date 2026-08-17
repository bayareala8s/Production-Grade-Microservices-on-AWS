import os
from decimal import Decimal
from typing import Any

import httpx
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Fraud Service", version="1.0.0")

EVENT_LOG: list[dict[str, Any]] = []
SCORES: list[dict[str, Any]] = []
NOTIFY_URL = os.getenv("NOTIFY_EVENT_URL", "http://localhost:8014/events")
HIGH_RISK_THRESHOLD = float(os.getenv("HIGH_RISK_THRESHOLD", "0.7"))


class CloudEvent(BaseModel):
    source: str
    detail_type: str = Field(alias="detail-type")
    detail: dict[str, Any]

    class Config:
        populate_by_name = True


def score_payment(detail: dict[str, Any]) -> dict[str, Any]:
    amount = Decimal(str(detail.get("amount", "0")))
    high_value = bool(detail.get("high_value")) or amount >= Decimal("10000")
    # Simple teaching heuristic — not a real ML model
    risk = 0.9 if high_value else 0.1
    if amount >= Decimal("5000") and amount < Decimal("10000"):
        risk = 0.55
    return {
        "transfer_id": detail.get("transfer_id"),
        "customer_id": detail.get("customer_id"),
        "amount": str(amount),
        "risk_score": risk,
        "decision": "REVIEW" if risk >= HIGH_RISK_THRESHOLD else "ALLOW",
    }


def forward_alert(score: dict[str, Any], payment_detail: dict[str, Any]) -> None:
    # Always notify of the transfer; add FraudAlert when high risk
    events = [
        {
            "source": "capstone.banking.payments",
            "detail-type": "PaymentPlaced",
            "detail": payment_detail,
        }
    ]
    if score["decision"] == "REVIEW":
        events.append(
            {
                "source": "capstone.banking.fraud",
                "detail-type": "FraudAlert",
                "detail": score,
            }
        )
    try:
        with httpx.Client(timeout=5.0) as client:
            for payload in events:
                client.post(NOTIFY_URL, json=payload)
    except Exception:
        pass


@app.get("/health")
def health():
    return {"status": "ok", "service": "fraud-service", "scores": len(SCORES)}


@app.post("/events")
def receive_event(event: CloudEvent):
    record = {
        "source": event.source,
        "detail_type": event.detail_type,
        "detail": event.detail,
    }
    EVENT_LOG.append(record)
    if event.detail_type == "PaymentPlaced":
        score = score_payment(event.detail)
        SCORES.append(score)
        forward_alert(score, event.detail)
        return {"status": "scored", "score": score}
    return {"status": "ignored", "detail_type": event.detail_type}


@app.get("/scores")
def list_scores():
    return {"scores": SCORES[-50:]}
