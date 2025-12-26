# Lab 05 — Outbox Pattern & Projections (Conceptual)

## Outcome

You will understand two production patterns:

- the **outbox pattern** to reliably publish events after DB commits
- **projections/read models** for query performance and decoupling

## Part A — Outbox pattern (why it exists)

### Problem

If you:

- write to your DB, then
- publish an event

…you can fail in between and end up with “DB says yes, event never published”.

### Pattern (high level)

- within the same DB transaction:
  - write business state
  - write an outbox row (event payload)
- a separate publisher process reads outbox rows and publishes them
- after successful publish, mark outbox row as sent

## Part B — Read models / projections

### When to use

- consumers need fast reads
- joining across services is not allowed (no shared DB)

### Pattern (high level)

- consumer subscribes to events
- consumer maintains its own query-optimized table (“projection”)

## Checkpoint

- Students can explain why outbox exists and how projections avoid cross-service joins.


