# 6-Week Cohort Schedule — Production-Grade Microservices on AWS

## Assumptions (edit as needed)

- **2 live sessions/week**, 2.5–3 hours each
- **1 optional office hour/week**, 60 minutes
- Students work in teams of 2–4 for capstone (recommended)

## Course flow (at a glance)

- Weeks 1–4: Modules 1–6 + capstone design/vertical slice
- Week 5: Module 7–8 + production hardening
- Week 6: Capstone completion + demos + postmortems

---

## Week 1 — Foundations + Production APIs (Modules 1–2)

### Session 1 (Module 1)

- Concepts: monolith vs microservices tradeoffs, bounded contexts, ownership, failure modes
- In-class: review `modules/module-01-microservices-foundations/course-outline.md`
- Lab/exercises:
  - `modules/module-01-microservices-foundations/labs/exercise-01-readiness.md`
  - `modules/module-01-microservices-foundations/labs/exercise-02-decomposition.md`

### Session 2 (Module 2)

- Concepts: contract thinking, validation, standardized errors, OpenAPI as artifact
- In-class starter run: `modules/module-02-production-apis/starter/catalog-service/`
- Labs:
  - `modules/module-02-production-apis/labs/lab-01-contracts-openapi.md`
  - `modules/module-02-production-apis/labs/lab-02-validation-error-contracts.md`

### Homework (end of Week 1)

- Finish:
  - Module 1 exercises 1–2
  - Module 2 labs 1–2
- Deliverables:
  - 1-page decomposition + ownership table
  - exported OpenAPI spec (`openapi.generated.json`) for the starter service

---

## Week 2 — Versioning + Containers/Compute Choices (Modules 2–3)

### Session 3 (Module 2 continuation)

- Concepts: versioning strategies, backward compatibility, contract tests
- Labs:
  - `modules/module-02-production-apis/labs/lab-03-versioning-backward-compat.md`
  - `modules/module-02-production-apis/labs/lab-04-testing.md`

### Session 4 (Module 3)

- Concepts: Docker best practices, ECS Fargate vs EKS vs Lambda decision matrix
- Labs:
  - `modules/module-03-containers-and-aws-compute/labs/lab-01-docker-production.md`
  - `modules/module-03-containers-and-aws-compute/labs/lab-02-compute-decision.md`

### Homework (end of Week 2)

- Finish:
  - `modules/module-02-production-apis/labs/lab-05-containerize.md`
  - Module 3 Lab 01 (Docker) deliverable image build/run instructions
- Capstone kickoff (start now):
  - Choose capstone option in `modules/module-09-capstone-platform/README.md`
  - Create service boundaries + ownership table (draft)
  - Start `modules/module-09-capstone-platform/templates/architecture-doc-template.md`

---

## Week 3 — ECS Deploy + Networking/Reliability (Modules 3–4)

### Session 5 (Module 3 continuation)

- Concepts: ECS basics (task defs, services), deployment mechanics, scaling intuition
- Labs:
  - `modules/module-03-containers-and-aws-compute/labs/lab-03-ecs-fargate-deploy.md`
  - `modules/module-03-containers-and-aws-compute/labs/lab-04-scaling.md`

### Session 6 (Module 4)

- Concepts: entry points (API Gateway vs ALB), internal calls, timeouts/retries/backoff, failure simulation
- Labs:
  - `modules/module-04-networking-and-traffic-management/labs/lab-01-entrypoints.md`
  - `modules/module-04-networking-and-traffic-management/labs/lab-03-failure-simulation.md`

### Homework (end of Week 3)

- Capstone Milestone 1 (Design) due:
  - `modules/module-09-capstone-platform/capstone-brief.md` (Architecture deliverables section)
  - 1 ADR using `modules/module-09-capstone-platform/templates/adr-template.md`
- Implementation:
  - deploy at least one service to ECS (or document deployment plan if AWS access limited)

---

## Week 4 — Data Consistency + Security (Modules 5–6)

### Session 7 (Module 5)

- Concepts: database-per-service, event contracts, idempotency, saga intro
- Labs:
  - `modules/module-05-data-state-consistency/labs/lab-01-data-ownership-boundaries.md`
  - `modules/module-05-data-state-consistency/labs/lab-03-idempotency-api-and-events.md`
  - (reference artifacts) `modules/module-05-data-state-consistency/starter/event-contracts/`

### Session 8 (Module 6)

- Concepts: IAM least privilege, secrets, JWT validation, network isolation
- Labs:
  - `modules/module-06-security-and-identity/labs/lab-01-iam-least-privilege.md`
  - `modules/module-06-security-and-identity/labs/lab-02-secrets-manager.md`

### Homework (end of Week 4)

- Capstone Milestone 2 (Vertical slice) due:
  - one end-to-end flow across services (even if simple)
  - event contract(s) or API contract(s) written and versioned
  - idempotency strategy documented (Module 5 rubric)
- Security:
  - least-privilege policy draft for one service dependency

---

## Week 5 — Observability + CI/CD (Modules 7–8)

### Session 9 (Module 7)

- Concepts: logs/metrics/traces, correlation, SLIs/SLOs, synthetic checks
- Labs:
  - `modules/module-07-observability-testing-reliability/labs/lab-01-structured-logging.md`
  - `modules/module-07-observability-testing-reliability/labs/lab-04-sli-slo.md`
  - Starter: `modules/module-07-observability-testing-reliability/starter/cloudwatch/dashboard-template.json`

### Session 10 (Module 8)

- Concepts: CI → CD, artifact promotion, release gates, rollback
- Labs:
  - `modules/module-08-cicd-zero-downtime/labs/lab-01-ci-pipeline.md`
  - `modules/module-08-cicd-zero-downtime/labs/lab-04-rollback-gates.md`
  - Starters: `modules/module-08-cicd-zero-downtime/starter/`

### Homework (end of Week 5)

- Capstone Milestone 3 (Production hardening) due:
  - SLO defined + dashboard plan (Module 7 rubric)
  - CI pipeline exists for at least one service (Module 8)
  - rollback plan documented
  - runbook draft using `modules/module-09-capstone-platform/templates/runbook-template.md`

---

## Week 6 — Capstone Finalization + Demo Day (Module 9)

### Session 11 (Capstone build + rehearsal)

- In-class:
  - review demo checklist `modules/module-09-capstone-platform/templates/demo-checklist.md`
  - failure-mode rehearsal: break something safely and show mitigation
- Target: “feature freeze” by end of session

### Session 12 (Demo day + postmortems)

- Demos (10–15 minutes each)
- Lightweight postmortem:
  - `modules/module-09-capstone-platform/templates/incident-postmortem-template.md`
- Wrap-up:
  - what to improve next (security hardening, cost, resilience, data correctness)

### Final deliverables (end of Week 6)

- Completed architecture doc
- At least 3 services with clear ownership boundaries
- Contracts (OpenAPI and/or event schemas) stored as artifacts
- CI pipeline + deployment plan + rollback plan
- Dashboard + SLO + runbooks


