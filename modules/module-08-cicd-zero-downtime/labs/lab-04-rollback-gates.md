# Lab 04 — Rollback Gates (Alarms + Smoke Tests)

## Outcome

You will define rollback triggers and post-deploy validation.

## Steps

### 1) Define post-deploy smoke tests

Examples:

- `GET /health/ready`
- a basic business flow (create + read)

### 2) Define alarms as rollback triggers

Define alarms for:

- target 5xx > threshold
- p95 latency > threshold

### 3) Runbook: what happens on rollback

Write down:

- who is paged
- where to find logs/traces
- what data might need cleanup (if any)

## Checkpoint

- Students can explain what triggers rollback and what the operator does next.


