import logging
from typing import Any

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("finops-notification")

app = FastAPI(title="FinOps Notification Service", version="1.0.0")
EVENT_LOG: list[dict[str, Any]] = []

WELCOME = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Option 4 — Idle Cost Advisor</title>
<style>body{font-family:system-ui;background:#0f172a;color:#e2e8f0;padding:2rem}
a{color:#7dd3fc}code{background:#1e293b;padding:.15em .4em;border-radius:4px}</style></head>
<body>
<h1>Option 4 — AWS Idle Cost Advisor</h1>
<p>FinOps: discover idle NAT/ALB/ECS/EIP · estimate $/mo · recommend stop (never auto-destroy)</p>
<ul>
<li><a href="/events">GET /events</a> — IdleCostFinding digests</li>
<li>Account <code>:8031</code> · Inventory <code>:8032</code> · Analyzer <code>:8033</code> · Recommend <code>:8034</code></li>
<li>Local tip: <code>./scripts/labs-stop.sh</code> on the course platform</li>
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
    return WELCOME


@app.get("/health")
def health():
    return {"status": "ok", "service": "notification-service", "events_received": len(EVENT_LOG)}


@app.post("/events")
def receive(event: CloudEvent):
    record = {"source": event.source, "detail_type": event.detail_type, "detail": event.detail}
    EVENT_LOG.append(record)
    logger.info("Event %s — %s", event.detail_type, event.detail)
    return {"status": "processed", "detail_type": event.detail_type}


@app.get("/events")
def list_events():
    return {"events": EVENT_LOG[-50:]}
