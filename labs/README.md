# Hands-On Labs

Complete student lab workbooks — one per module (Weeks 1–9).

| Week | Lab | Hours |
|------|-----|-------|
| 1 | [module-01/](module-01/README.md) | 4h |
| 2 | [module-02/](module-02/README.md) | 4h |
| 3 | [module-03/](module-03/README.md) | 4h |
| 4 | [module-04/](module-04/README.md) | 4h |
| 5 | [module-05/](module-05/README.md) | 4h |
| 6 | [module-06/](module-06/README.md) | 4h |
| 7 | [module-07/](module-07/README.md) | 4h |
| 8 | [module-08/](module-08/README.md) | 4h |
| 9 | [module-09/](module-09/README.md) | 4h |

Week 10: [capstone/README.md](../capstone/README.md)

**Start / stop labs (minimize cost when not teaching):**

```bash
./scripts/labs-start.sh --all     # local Docker + AWS (~15–20 min first AWS start)
./scripts/labs-stop.sh            # stop local + AWS (NAT/ALB/Fargate off → ~$0–2/mo idle)
./scripts/labs-status.sh          # show what's running and estimated cost
./scripts/labs-stop.sh --destroy  # delete all AWS resources ($0/month)
```

**Run the platform locally before Lab 3:**

```bash
./scripts/labs-start.sh --local
# or: docker compose up --build
```

**Verify labs:**

```bash
./scripts/verify-all-labs.sh    # all labs; AWS 04–08 when platform active
./scripts/verify-aws-labs.sh    # AWS labs 04–08 (requires ./scripts/labs-start.sh --aws)
```
