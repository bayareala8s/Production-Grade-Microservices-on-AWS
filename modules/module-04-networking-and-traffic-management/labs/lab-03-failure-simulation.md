# Lab 03 — Failure Simulation: Timeouts and Retry Storms (Local)

## Outcome

Students observe how small latency increases can cascade into outages.

## Setup

Use `catalog-service` (Module 2) running locally.

## Steps

### 1) Add artificial latency

Modify one endpoint handler (example: `GET /api/v1/products`) to sleep 500–1500ms.

### 2) Write a simple load script (conceptual)

Have a client send many requests concurrently.

Observe:

- response times
- error rates
- CPU usage

### 3) Add retries (badly) and observe amplification

Retry immediately on timeouts with high concurrency.

Discuss:

- why retries can make overload worse

### 4) Fix the retry policy

Add:

- max attempts (e.g., 2)
- exponential backoff + jitter
- stop retrying non-idempotent operations

## Deliverable

A short write-up:

- what failed
- what mitigation reduced blast radius
- what you’d configure at client vs gateway vs service


