import logging
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("banking-notification")

app = FastAPI(title="Banking Notification Service", version="1.0.0")
EVENT_LOG: list[dict[str, Any]] = []

WELCOME_HTML = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Capstone Option 2 — Banking</title>
<style>body{font-family:system-ui;background:#0f172a;color:#e2e8f0;padding:2rem}
a{color:#7dd3fc}code{background:#1e293b;padding:.2em .4em;border-radius:4px}</style>
</head><body>
<h1>Option 2 — Banking Platform</h1>
<p>Customer · Payment · Fraud · Notification</p>
<ul>
<li><a href="/events">GET /events</a> — PaymentPlaced / FraudAlert log</li>
<li>Customer API: <code>:8011</code> · Payment: <code>:8012</code> · Fraud: <code>:8013</code></li>
</ul>
</body></html>
"""


class CloudEvent(BaseModel):
    source: str
    detail_type: str = Field(alias="detail-type")
    detail: dict[str, Any]

    class Config:
        populate_by_name = True


@app.get("/", response_class=HTMLResponse)
def welcome():
    return WELCOME_HTML


@app.get("/health")
def health():
    return {"status": "ok", "service": "notification-service", "events_received": len(EVENT_LOG)}


@app.post("/events")
def receive_event(event: CloudEvent):
    record = {
        "source": event.source,
        "detail_type": event.detail_type,
        "detail": event.detail,
    }
    EVENT_LOG.append(record)
    logger.info("Event: %s — %s", event.detail_type, event.detail)
    return {"status": "processed", "detail_type": event.detail_type}


@app.get("/events")
def list_events():
    return {"events": EVENT_LOG[-50:]}
