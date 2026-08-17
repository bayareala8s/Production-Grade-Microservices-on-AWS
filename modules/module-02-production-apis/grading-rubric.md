# Module 2 — Grading Rubric (Suggested)

## Total: 100 points

### API contract quality (30)

- 10: Consistent JSON response shapes for success paths
- 10: OpenAPI spec is generated and reflects the implementation
- 10: Breaking changes are handled via versioning (no silent v1 breaks)

### Validation & error handling (30)

- 10: Request validation rules are defined (types + constraints)
- 10: Validation errors return the standard error contract
- 10: Non-validation errors (404/500) return the standard error contract

### Operability basics (20)

- 10: Health endpoints exist (`/health/live`, `/health/ready`)
- 10: Request correlation is implemented (`X-Request-Id`)

### Testing (20)

- 10: Contract tests for v1 and v2 endpoints
- 10: Error contract tests for invalid input and not-found cases


