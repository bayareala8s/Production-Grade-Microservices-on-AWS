# Capstone Implementation Roadmap

Build all four tracks **one by one**. Do not start the next option until the current option’s local demo + verify pass.

| Order | Track | Folder | Status |
|-------|--------|--------|--------|
| 1 | E-Commerce | [option-01-ecommerce/](option-01-ecommerce/) | **Done (local)** — Inventory + demo/verify green |
| 2 | Banking | [option-02-banking/](option-02-banking/) | **Done (local)** — KYC, Decimal ledger, fraud alerts |
| 3 | SaaS | [option-03-saas/](option-03-saas/) | **Done (local)** — tenant JWT, usage→billing |
| 4 | Idle Cost Advisor | [option-04-idle-cost/](option-04-idle-cost/) | **Done (local)** — mock scan → IdleCostFinding, recommend-only |

## Shared rules (every option)

- ≥ 3 services, OpenAPI contracts, at least one async event
- Local: Docker Compose demo script
- AWS: reuse course Terraform patterns when ready (after local green)
- Stop AWS with `./scripts/labs-stop.sh` when not demoing

## How we work

```bash
# Option currently in progress
cd capstone/option-01-ecommerce
docker compose up -d --build
./scripts/demo.sh
./scripts/verify.sh
```

When Option 1 is done, mark it **Done** here and open Option 2.
