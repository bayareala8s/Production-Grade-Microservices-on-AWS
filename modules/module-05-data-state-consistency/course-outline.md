# Module 5 — Course Outline (Instructor)

## Recommended duration

3–6 hours

## Learning objectives

- understand why distributed transactions don’t scale organizationally
- apply database-per-service with event-driven integration
- implement idempotency patterns to handle duplicates
- introduce saga patterns (choreography vs orchestration)

## Lesson plan

### Part A — Data ownership in microservices (40–60 min)

- “database per service” and why shared DB causes coupling
- integration via APIs vs events
- lab tie-in: `labs/lab-01-data-ownership-boundaries.md`

### Part B — Consistency models (40–60 min)

- strong consistency vs eventual consistency
- read models / materialized views (conceptual)
- outbox pattern (conceptual)
- lab tie-in: `labs/lab-05-outbox-and-projections.md`

### Part C — Idempotency (45–75 min)

- duplicates happen (at-least-once delivery)
- idempotency keys for APIs
- idempotent event handlers
- lab tie-in: `labs/lab-03-idempotency-api-and-events.md`

### Part D — Sagas intro (45–75 min)

- choreography (events) vs orchestration (coordinator)
- compensating actions
- why sagas are about business processes, not technology
- lab tie-in: `labs/lab-04-saga-modeling.md`

### Part E — Event contracts & versioning (30–45 min)

- events as long-lived contracts
- schema evolution rules (additive vs breaking)
- examples as artifacts (see `starter/event-contracts/`)
- lab tie-in: `labs/lab-02-event-contracts-and-versioning.md`

## Instructor checkpoints

- students can explain why shared DB is a coupling risk (with concrete failure examples)
- students can define an event schema and versioning rules
- students can propose an idempotency strategy for both APIs and event handlers
- students can model a simple order saga with compensations and timeouts


