# Option 4 — AWS Idle Cost Advisor (FinOps)

**Status:** Local MVP implemented

| Service | Port | Responsibility |
|---------|------|----------------|
| account-service | 8031 | Users, JWT, link AWS account (`read_only`) |
| inventory-service | 8032 | Discover NAT/ALB/ECS/EIP (`SCAN_MODE=mock` or `aws`) |
| analyzer-service | 8033 | Idle score + monthly \$ estimate (rate card) |
| recommendation-service | 8034 | Ranked actions — **never auto-destroy** |
| notification-service | 8035 | `IdleCostFinding` digests + welcome page |

## Event flow

```text
POST /scans
  → InventoryScanCompleted → Analyzer
  → IdleCostScored → Recommendation
  → IdleCostFinding → Notification
```

## Quick start

```bash
cd capstone/option-04-idle-cost
docker compose up -d --build
./scripts/demo.sh
./scripts/verify.sh
```

Welcome: http://localhost:8035/

### Optional live AWS scan (read-only)

```bash
SCAN_MODE=aws AWS_REGION=us-east-1 docker compose up -d --build inventory-service
```

Requires AWS credentials with describe permissions only.

## Constraints

- Recommend-only (`auto_destroy: false`)
- Mock fixtures by default (works with course platform stopped)
- Ties to course cost control: `./scripts/labs-stop.sh`

## Deliverables checklist

- [x] Five microservices + compose
- [x] Mock scan + scoring + recommendations
- [x] IdleCostFinding events
- [x] demo.sh + verify.sh
- [x] OpenAPI for inventory
- [ ] AWS ECS deploy of this platform
- [ ] Cost analysis write-up

## Decomposition

See [../templates/option-4-idle-cost-decomposition.md](../templates/option-4-idle-cost-decomposition.md).
