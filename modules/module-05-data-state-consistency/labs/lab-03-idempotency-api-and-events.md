# Lab 03 — Idempotency (APIs + Event Handlers)

## Outcome

You will design idempotency for:

- a **write API** (client retries)
- an **event handler** (at-least-once delivery)

## Part A — API idempotency keys

### Scenario

`POST /payments/authorize` can be retried by clients due to timeouts.

### Tasks

- Choose an idempotency header: `Idempotency-Key`
- Define storage strategy:
  - key: `(tenant_id, idempotency_key, endpoint)`
  - value: `status`, `response_body_hash`, `created_at`, TTL
- Define conflict behavior:
  - same key + different payload ⇒ `409 Conflict` with a clear error code

## Part B — Event handler idempotency

### Scenario

`payments` receives `OrderCreated` and creates a payment intent.

### Tasks

- Define dedupe key:
  - either `event_id` (delivery-level) or `order_id` (business-level) depending on behavior
- Define storage:
  - “processed events” table with TTL
- Define ordering behavior:
  - how you handle `OrderCancelled` arriving before `OrderCreated`

## Checkpoint

- You can explain why “exactly once” is not the default and how you handle duplicates.


