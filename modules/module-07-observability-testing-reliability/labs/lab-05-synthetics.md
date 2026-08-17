# Lab 05 — Synthetic Checks & Canary Testing

## Outcome

You will define a synthetic check and a canary plan.

## Steps

### 1) Define a synthetic check

Pick a critical flow:

- `GET /health/ready`
- `GET /api/v1/products`

Define:

- frequency (every 1–5 minutes)
- expected latency
- expected response shape

### 2) Define a canary

Write down:

- what percentage of traffic is canary (1–10%)
- what metric gates promotion (error rate, latency)
- rollback trigger conditions

### 3) Connect to alarms

List alarms that should trigger rollback or paging.

## Checkpoint

- Students can distinguish smoke vs canary vs synthetic monitoring.


