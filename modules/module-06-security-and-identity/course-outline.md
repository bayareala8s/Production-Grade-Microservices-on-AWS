# Module 6 — Course Outline (Instructor)

## Recommended duration

3–6 hours

## Learning objectives

- apply least-privilege IAM design for microservices
- understand identity at the edge (JWT/OAuth) and inside the mesh (service roles)
- manage secrets safely (storage, rotation, runtime injection)
- isolate services with VPC/subnets/security groups and minimize blast radius

## Lesson plan (suggested)

### Part A — Threat model for microservices (30–45 min)

- what you must assume in production (internet noise, compromised creds, misconfig)
- the “four layers”: edge, service runtime, data plane, control plane
- define: auth vs authz vs accounting (AAA)

### Part B — IAM in practice (60–90 min)

- IAM roles per service; task roles vs execution roles (ECS)
- least-privilege: start narrow; add only what’s required
- policy structure: actions, resources, conditions
- lab tie-in: `labs/lab-01-iam-least-privilege.md`

### Part C — Secrets management (45–75 min)

- why env vars alone are not “secure”
- Secrets Manager vs SSM Parameter Store
- rotation basics and operational ownership
- lab tie-in: `labs/lab-02-secrets-manager.md`

### Part D — API identity (JWT/OAuth) (45–75 min)

- JWT anatomy; signing vs encryption
- issuer/audience/expiry; key rotation with JWKS
- practical validation at API boundary
- lab tie-in: `labs/lab-03-jwt-auth.md`

### Part E — Network isolation (45–75 min)

- public vs private subnets
- security groups and egress control
- “internal-only” services and admin endpoints
- lab tie-in: `labs/lab-04-network-isolation.md`

## Instructor checkpoints

- students can explain the difference between task role and execution role
- students can produce a least-privilege policy for a concrete service dependency
- students can describe JWT validation steps and common failure modes
- students can draw a minimal VPC layout with controlled ingress/egress


