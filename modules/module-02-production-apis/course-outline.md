# Module 2 — Course Outline (Instructor)

## Recommended duration

3–5 hours

## Learning objectives

- design stable API contracts (request/response, errors, validation)
- implement API versioning strategies and avoid breaking changes
- generate and treat OpenAPI specs as artifacts
- test APIs with contract and error-contract tests

## Lesson plan (suggested)

### Part A — Contracts in production (30–45 min)

- consumers are teams and systems; breaking changes cause incidents
- contract-first vs code-first tradeoffs
- lab tie-in: `labs/lab-01-contracts-openapi.md`

### Part B — Validation and error contracts (45–75 min)

- input validation as a reliability feature
- standardized error responses across the platform
- lab tie-in: `labs/lab-02-validation-error-contracts.md`

### Part C — Versioning and backward compatibility (45–75 min)

- path versioning vs header versioning
- additive vs breaking changes
- lab tie-in: `labs/lab-03-versioning-backward-compat.md`

### Part D — Testing for contracts (45–75 min)

- contract tests (shape) vs behavioral tests (logic)
- testing error contracts
- lab tie-in: `labs/lab-04-testing.md`

### Part E — Container baseline (20–30 min)

- Docker packaging as the bridge to ECS (Module 3)
- lab tie-in: `labs/lab-05-containerize.md`

## Instructor checkpoints

- students can describe a stable error contract and why it matters
- students can add a v2 change without breaking v1 clients
- students can generate OpenAPI and treat it as a review artifact


