# Option 3 — SaaS Capstone

**Status:** Local MVP implemented

| Service | Port | Responsibility |
|---------|------|----------------|
| auth-service | 8025 | Register/login; JWT includes `tenant_id` + `role` |
| billing-service | 8022 | Plans, subscriptions, invoices; consumes `UsageRecorded` |
| user-mgmt-service | 8023 | Tenants, invites, members (tenant-scoped) |
| analytics-service | 8024 | Usage metering → `UsageRecorded` event |

## Event flow

```text
POST /usage (tenant-scoped)
  → Analytics stores event
  → UsageRecorded → Billing
  → Overage invoice if units > plan included_units
```

## Focus

- **Tenant isolation** on invites, usage, and JWT claims
- Cross-tenant usage with wrong token → **403**

## Quick start

```bash
cd capstone/option-03-saas
docker compose up -d --build
./scripts/demo.sh
./scripts/verify.sh
```

## Deliverables checklist

- [x] Four microservices + compose
- [x] JWT tenant claims + isolation demo
- [x] Usage → billing overage invoices
- [x] demo.sh + verify.sh
- [x] OpenAPI for billing
- [ ] AWS ECS deploy
- [ ] Cost analysis write-up

## Next

[Option 4 — Idle Cost Advisor](../option-04-idle-cost/)
