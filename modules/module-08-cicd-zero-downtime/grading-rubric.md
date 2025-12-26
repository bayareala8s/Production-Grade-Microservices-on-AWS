# Module 8 — Grading Rubric (Suggested)

## Total: 100 points

### CI pipeline quality (35)

- 10: Automated tests are part of CI
- 10: Packaging/build step produces a reproducible artifact (image)
- 10: Security checks exist (dependency scan/image scan conceptually)
- 5: Pipeline is documented and understandable

### Deployment strategy (35)

- 15: Deployment approach fits risk profile (rolling vs blue/green)
- 10: Health checks are configured and validated
- 10: Promotion gates exist (smoke tests, alarms)

### Rollback strategy (30)

- 15: Rollback is automated or one-command and well defined
- 10: Clear rollback triggers (alarm thresholds)
- 5: Handles schema/config changes safely (or documents limitations)


