# Quality & improvement roadmap

This document tracks production-readiness improvements for the course platform.

## Completed

| Area | Change |
|------|--------|
| **CI** | Matrix build for all 4 services; tests fail the workflow on error |
| **CD** | Matrix deploy to all 4 ECR repos / ECS services |
| **Terraform** | ECS task SG ingress via separate rules (fixes stop/start drift) |
| **Terraform** | Removed deprecated `failure_threshold` on service discovery |
| **Order service** | Clear 404/502/503 errors when product-service is unavailable |
| **Tests** | User: 409 duplicate email, 401 bad password |
| **Tests** | Order: insufficient stock, product not found |
| **Tests** | Notification: isolated `EVENT_LOG` per test |
| **Verify** | `verify-all-labs.sh` runs AWS labs 04–08 when platform active |
| **Ops** | `labs-start/stop/status` lifecycle scripts with cost modes |
| **Capstone** | Option 4 — AWS Idle Cost Advisor (FinOps) + decomposition template |

## Recommended next (by impact)

### High — teaching reliability

1. **EventBridge on AWS** — Wire `EVENT_PUBLISH_MODE=eventbridge` in ECS and add API Destination or Lambda → notification-service (Lab 5 Part C reference implementation).
2. **DynamoDB orders adapter** — Implement `app/dynamodb_repo.py` in order-service (Lab 6 reference).
3. **Transactional outbox** — Persist events before publish; retry on failure (Module 5 lecture alignment).

### Medium — security & observability

4. **JWT-protected POST /products** — Optional extension in product-service with shared auth dependency.
5. **Secrets Manager** — Replace `JWT_SECRET` env default in ECS task definitions.
6. **CloudWatch dashboard Terraform** — Codify Lab 8 dashboard + alarms.

### Lower — polish

7. **Consolidate `shared/events.py`** — Single module copied into order-service image.
8. **Pydantic v2 `ConfigDict`** — Remove deprecation warnings in models.
9. **Capstone verify script** — Optional `labs/module-10/verify.sh` for demo checklist.

## Quality gates (run before each cohort)

```bash
./scripts/run-all-tests.sh      # unit tests (all services)
./scripts/labs-start.sh --all   # when teaching AWS
./scripts/verify-all-labs.sh    # full lab verification
./scripts/labs-stop.sh          # minimize cost after class
```

## Cost discipline

| State | Command | Typical idle cost |
|-------|---------|-------------------|
| Teaching | `labs-start --all` | ~$1.50–3/day |
| Paused | `labs-stop` | ~$0–2/month |
| Teardown | `labs-stop --destroy` | $0 |
