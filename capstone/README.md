# Module 10 — Enterprise Capstone Project

**Weeks 10+**

Students design, build, deploy, secure, observe, and operate a complete microservices platform.

**Build tracks one by one:** [IMPLEMENTATION.md](IMPLEMENTATION.md)

## Option 1 — E-Commerce Platform

| Service | Responsibility |
|---------|----------------|
| User Service | Accounts, profiles |
| Product Service | Catalog, pricing |
| Inventory Service | Stock levels |
| Order Service | Checkout, orders |
| Notification Service | Email/SMS events |

## Option 2 — Banking Platform

| Service | Responsibility |
|---------|----------------|
| Customer Service | KYC, profiles |
| Payment Service | Transactions |
| Fraud Service | Risk scoring |
| Notification Service | Alerts |

## Option 3 — SaaS Platform

| Service | Responsibility |
|---------|----------------|
| Authentication | Login, tokens |
| Billing | Subscriptions, invoices |
| User Management | Tenants, roles |
| Analytics | Usage metrics |

## Option 4 — AWS Idle Cost Advisor (FinOps)

Discover underused cloud resources, estimate idle spend, and recommend start/stop actions.

| Service | Responsibility |
|---------|----------------|
| Account / Auth | Orgs, JWT, link AWS account (assume-role) |
| Inventory | Discover ECS, ALB, NAT, EIP, and related resources |
| Cost Analyzer | Idle heuristics + Cost Explorer estimates |
| Recommendation | Rank findings; suggest stop/destroy actions |
| Notification | Digest alerts (`IdleCostFinding` events) |

**Template:** [templates/option-4-idle-cost-decomposition.md](templates/option-4-idle-cost-decomposition.md)

**Scope guidance**

- **In:** Read-only IAM; 1–2 accounts; resources students already know (ECS, ALB, NAT); recommend-only (no auto-delete)
- **Out:** Multi-cloud; production auto-remediation; full CUR/Athena billing pipelines
- **Demo:** Mock findings + one live read-only scan; show monthly idle \$ estimate

**Why this track:** Builds on course cost control (`labs-start` / `labs-stop`) and maps cleanly to FinOps / platform engineering roles.

---

## Required Capstone Deliverables

1. Architecture diagrams (context, container, deployment)
2. Source code repositories (one mono-repo or multi-repo—document choice)
3. CI/CD pipelines with automated tests
4. Observability dashboards and tracing
5. Security review (threat model or checklist)
6. Cost analysis (monthly estimate with assumptions)
7. Final demo (15–20 minutes)

## Evaluation

See [rubrics.md](rubrics.md).

## Suggested Timeline

| Week | Focus |
|------|-------|
| 10.1 | Architecture sign-off |
| 10.2 | Core services + APIs |
| 10.3 | Events, data, security |
| 10.4 | CI/CD, observability, demo prep |
