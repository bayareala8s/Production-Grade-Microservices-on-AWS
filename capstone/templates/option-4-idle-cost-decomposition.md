# Option 4 — AWS Idle Cost Advisor · Service Decomposition

**Capstone track:** FinOps / cloud cost governance  
**Use with:** [service-decomposition.md](../../labs/module-01/templates/service-decomposition.md) (Lab 1 style)

---

## Problem statement

AWS accounts accrue idle cost when teaching or lab environments leave NAT Gateways, ALBs, and Fargate tasks running. Build a microservices platform that **discovers** underused resources, **estimates** waste, and **recommends** start/stop actions — without auto-deleting production infrastructure.

---

## Bounded contexts

### 1. Account / Auth

| | |
|--|--|
| **Owns** | Users, orgs, linked AWS account IDs, JWT |
| **API** | `POST /users`, `POST /auth/login`, `POST /accounts/link` |
| **Events** | (optional) `AccountLinked` |

### 2. Inventory

| | |
|--|--|
| **Owns** | Resource snapshots (type, id, region, tags, last_seen) |
| **API** | `POST /scans`, `GET /resources` |
| **Events** | `InventoryScanCompleted` |
| **Data** | DynamoDB or SQLite per environment |

**In-scope resource types (minimum):** ECS services (desired count), ALB, NAT Gateway, Elastic IP.

### 3. Cost Analyzer

| | |
|--|--|
| **Owns** | Idle scores, estimated monthly waste USD |
| **API** | `POST /analyze`, `GET /findings/{scan_id}` |
| **Events** | Consumes `InventoryScanCompleted`; publishes `IdleCostScored` |
| **Inputs** | Inventory snapshot + optional Cost Explorer (or static rate card for labs) |

**Example heuristics**

| Signal | Suggested finding |
|--------|-------------------|
| NAT Gateway + near-zero CloudWatch bytes | Idle NAT (~$0.045/hr) |
| ALB + 0 healthy targets for N hours | Idle ALB |
| ECS desiredCount ≥ 1, CPU ~0 for N days | Candidate scale-to-zero |
| Unattached EIP | Idle EIP |

### 4. Recommendation

| | |
|--|--|
| **Owns** | Ranked recommendations, severity, suggested action |
| **API** | `GET /recommendations`, `GET /recommendations/{id}` |
| **Events** | Publishes `IdleCostFinding` |
| **Actions** | `stop_platform`, `destroy_alb`, `release_eip` — **recommend only** |

### 5. Notification

| | |
|--|--|
| **Owns** | Alert delivery log |
| **API** | `POST /events`, `GET /events` |
| **Consumes** | `IdleCostFinding` |
| **Demo** | Log / webhook / email mock (same pattern as course notification-service) |

---

## Sync vs async

```text
Auth ──sync──► Inventory (start scan)
Inventory ──event──► Cost Analyzer
Cost Analyzer ──event──► Recommendation
Recommendation ──event──► Notification
```

Keep HTTP for request/response APIs; use events for scan → score → recommend → notify.

---

## Security constraints (required)

- Task role: **read-only** on target account (`ec2:Describe*`, `ecs:Describe*`, `elasticloadbalancing:Describe*`, `ce:GetCostAndUsage` optional)
- No long-lived AWS keys in containers — use IAM roles / assume-role
- Never auto-destroy resources in the graded demo
- Secrets (JWT) not committed to Git

---

## AWS deployment (same bar as other options)

- ≥ 3 services on ECS Fargate behind ALB
- Terraform (extend course modules)
- CloudWatch logs + one dashboard or alarm
- CI/CD to ECR/ECS
- Cost analysis of **your** platform (use `templates/cost-analysis-template.md`) — ironic and useful

---

## Demo script (15–20 min)

1. Architecture: contexts + idle-cost event flow  
2. Trigger scan → show inventory resources  
3. Show findings with estimated \$/month idle  
4. Show recommendation list (stop NAT/ALB/ECS)  
5. Optional: relate to course `./scripts/labs-stop.sh`  
6. CI/CD + CloudWatch + security model Q&A  

---

## Rubric notes (instructor)

| Criterion | Option 4 emphasis |
|-----------|-------------------|
| Architecture | Clear FinOps boundaries; no god “scanner” service |
| Implementation | Live or mocked scan path; events between analyzer and notify |
| Security | Read-only IAM demonstrated |
| Observability | Scan duration, findings count metrics/logs |
| Demo | Credible idle \$ estimate with stated assumptions |
