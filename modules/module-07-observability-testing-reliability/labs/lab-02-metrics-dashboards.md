# Lab 02 — Metrics & Dashboards (Golden Signals)

## Outcome

You will propose a dashboard that reflects customer experience.

## Steps

### 1) Pick one critical API

Example:

- `POST /api/v1/orders`

### 2) Define golden signal metrics

- latency (p50/p95/p99)
- traffic (RPS)
- errors (4xx/5xx)
- saturation (CPU/memory, queue depth)

### 3) Define alert conditions

Write down thresholds tied to impact:

- “p95 latency > 800ms for 5 minutes”
- “5xx error rate > 1% for 10 minutes”

### 4) Use the starter dashboard template (optional)

See:

- `starter/cloudwatch/dashboard-template.json`

## Checkpoint

- Dashboard includes at least 6 widgets that map to user impact.


