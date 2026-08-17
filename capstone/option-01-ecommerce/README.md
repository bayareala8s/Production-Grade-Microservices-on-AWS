# Option 1 — E-Commerce Capstone

Extends the course platform with a dedicated **Inventory** service (database-per-service for stock).

| Service | Port | Role |
|---------|------|------|
| user-service | 8001 | Accounts, JWT (course) |
| product-service | 8002 | Catalog / pricing (course) |
| order-service | 8003 | Checkout; reserves inventory when configured |
| notification-service | 8004 | `OrderPlaced` events + welcome page |
| **inventory-service** | **8005** | Stock levels, reserve / release |

## Quick start

```bash
cd capstone/option-01-ecommerce
docker compose up -d --build
./scripts/demo.sh
./scripts/verify.sh
```

## Architecture

```text
Customer → ALB / localhost
  ├── /users, /auth     → user
  ├── /products         → product
  ├── /orders           → order ──sync──► product (price)
  │                         └──sync──► inventory (reserve)
  ├── /inventory*       → inventory
  └── /events           → notification ◄── OrderPlaced (async)
```

## Deliverables checklist

- [x] Inventory microservice (own DB)
- [x] Order → reserve stock before commit
- [x] Local compose + demo + verify
- [x] OpenAPI for inventory (`contracts/`)
- [ ] AWS ECS path (extend Terraform later)
- [ ] Cost analysis write-up

## Next

When verify is green, continue with [Option 2 — Banking](../option-02-banking/).
