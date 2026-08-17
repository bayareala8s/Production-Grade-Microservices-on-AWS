# Module 5 — Grading Rubric (Suggested)

## Total: 100 points

### Data ownership & boundaries (25)

- 10: Clear database-per-service boundaries (no shared tables)
- 10: Integration path defined (API vs events) with justification
- 5: Defined ownership (who owns what data and how changes propagate)

### Event-driven consistency design (25)

- 10: Event schema is explicit (names, versions, required fields)
- 10: Consumer behavior defined (projection/read model update, retries, DLQ strategy)
- 5: Handles out-of-order / duplicate deliveries in design

### Idempotency (25)

- 10: Idempotency key strategy for write APIs (storage + TTL + conflict behavior)
- 10: Idempotent event processing approach (dedupe store + stable business keys)
- 5: Clear “exactly once is a myth” explanation + handling approach

### Saga / business process modeling (25)

- 10: Choreography vs orchestration tradeoffs articulated
- 10: Compensating actions defined for failure cases
- 5: Failure-mode thinking: partial failure, timeouts, retries, poison messages


