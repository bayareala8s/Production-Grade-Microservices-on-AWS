# Exercise 03 — Define Service Contracts (OpenAPI + Event Schema)

## Outcome

Students practice writing contracts that allow independent development between teams.

## Instructions (30–45 min)

For each of your 3 services, define:

### A) One synchronous API (OpenAPI-level)

Write an endpoint with:

- method + path
- request body schema
- success response schema
- error response schema
- versioning plan (e.g., `/api/v1`)

### B) One asynchronous event (schema-level)

Define:

- event name (e.g., `order.created`)
- payload schema (fields + types)
- idempotency key strategy (e.g., `event_id`)
- consumer expectations (what must be true)

## Deliverables

- One page per service with the API + event contract.


