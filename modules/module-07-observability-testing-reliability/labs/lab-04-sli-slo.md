# Lab 04 — SLIs/SLOs (Customer-Facing Reliability)

## Outcome

You will define one SLI and one SLO for a service.

## Steps

### 1) Choose an SLI

Examples:

- availability for `GET /api/v1/products`
- latency for `POST /api/v1/orders`

### 2) Define the measurement window

Examples:

- rolling 28 days
- calendar month

### 3) Set an SLO target

Example:

- 99.9% of requests succeed (non-5xx) over 28 days

### 4) Define alerts vs SLOs

Write down:

- alert threshold (fast detection)
- SLO threshold (long-term target)

## Checkpoint

- Students can explain “error budget” in plain language.


