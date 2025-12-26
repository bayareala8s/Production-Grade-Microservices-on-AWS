# Module 6 — Grading Rubric (Suggested)

## Total: 100 points

### IAM least privilege (35)

- 15: Clear separation of execution role vs task role (or equivalent)
- 10: Policy is least-privilege (actions/resources/conditions are scoped)
- 10: Explains why permissions exist (dependency mapping)

### Secrets management (25)

- 10: Secrets are not hardcoded; runtime retrieval/injection is defined
- 10: Rotation story exists (even if simulated): what changes, who owns it
- 5: Access to secrets is scoped to the service role

### API identity (25)

- 10: JWT validation includes signature + `iss` + `aud` + `exp`
- 10: Auth failure responses are standardized and do not leak sensitive info
- 5: Documents how keys rotate / JWKS changes are handled

### Network isolation (15)

- 10: Minimal VPC layout (public/private) with justified entry points
- 5: Security group rules are explicit (ingress + egress)


