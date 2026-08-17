# Module 4 — Grading Rubric (Suggested)

## Total: 100 points

### Architecture choices (35)

- 15: appropriate entrypoint choice (API Gateway vs ALB) with justification
- 10: correct internal/external exposure model
- 10: identifies dependency paths and blast radius

### Reliability behavior (45)

- 15: timeouts are configured and justified
- 15: retries are safe and bounded (backoff + max attempts)
- 15: failure scenario is simulated and mitigated

### Clarity (20)

- 10: diagram + explanation is coherent
- 10: can explain idempotency vs retries


