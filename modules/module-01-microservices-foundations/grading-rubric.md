# Module 1 — Grading Rubric (Suggested)

## Total: 100 points

### Service boundaries & ownership (35)

- 15: clear bounded contexts (not “one service per table”)
- 10: explicit ownership per service (team/on-call responsibility)
- 10: responsibilities are cohesive and loosely coupled

### Data ownership & integration (25)

- 15: database-per-service is respected (no shared DB)
- 10: integration patterns chosen appropriately (sync vs async)

### Failure mode thinking (25)

- 10: identifies cascading failure risks and mitigations
- 10: addresses retries/timeouts and partial failures
- 5: addresses duplicate messages / idempotency conceptually

### Communication & clarity (15)

- 10: diagram + explanation are clear and consistent
- 5: tradeoffs are acknowledged (what got worse / better)


