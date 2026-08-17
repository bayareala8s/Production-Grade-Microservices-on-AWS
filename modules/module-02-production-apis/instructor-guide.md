# Module 2 — Instructor Guide

## Suggested pacing (2.5–4 hours)

- 15 min: Why contracts break production systems; consumer-driven thinking
- 30–45 min: OpenAPI exploration + export artifact (Lab 01)
- 45–60 min: Validation + error contracts (Lab 02)
- 30–45 min: Versioning strategy discussion + v2 extension (Lab 03)
- 30–45 min: Contract testing (Lab 04)
- 20–30 min: Containerize baseline + “what changes for ECS?” (Lab 05)

## Key talking points

- API versioning is an **organizational contract** as much as a technical one.
- Standard errors reduce MTTR: tooling can reliably parse failures.
- Health endpoints are for **automation**, not humans.
- Tests should enforce **shape**, not only values.

## Common student pitfalls (and how to coach)

- Changing v1 response when adding fields: show additive changes vs breaking changes.
- Returning framework-default errors: emphasize stability for consumers.
- Mixing business logic into routes: keep routes thin; introduce service layer in later modules.

## “Production next steps” preview

- Module 3: build image scanning, runtime sizing, deploy to ECS Fargate
- Module 6: auth + secrets manager, IAM task roles
- Module 7: structured logs, metrics, tracing (CloudWatch + X-Ray)


