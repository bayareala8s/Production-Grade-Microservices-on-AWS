# Option 2 — Banking Capstone

**Status:** Local MVP implemented

| Service | Port | Responsibility |
|---------|------|----------------|
| customer-service | 8011 | Profiles + KYC (PENDING/APPROVED/REJECTED) |
| payment-service | 8012 | Accounts, transfers, double-entry ledger (`Decimal`) |
| fraud-service | 8013 | Scores `PaymentPlaced`; emits `FraudAlert` when high risk |
| notification-service | 8014 | Event log + welcome page |

## Event flow

```text
Transfer → PaymentPlaced → Fraud (score)
                         ↓
              Notification (PaymentPlaced always)
                         ↓
              FraudAlert (when amount ≥ $10,000 / REVIEW)
```

## Quick start

```bash
cd capstone/option-02-banking
docker compose up -d --build
./scripts/demo.sh
./scripts/verify.sh
```

## Constraints (teaching)

- Money as `Decimal` (no float)
- Double-entry ledger inside payment bounded context
- PCI for real cards is **out of scope**
- KYC must be APPROVED before opening accounts

## Deliverables checklist

- [x] Four microservices + compose
- [x] Decimal ledger + PaymentPlaced / FraudAlert
- [x] demo.sh + verify.sh
- [x] OpenAPI for payment
- [ ] AWS ECS deploy
- [ ] Cost analysis write-up

## Next

[Option 3 — SaaS](../option-03-saas/)
