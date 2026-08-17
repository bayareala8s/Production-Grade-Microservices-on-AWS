# AWS Cost Control — Start / Stop / Destroy

## Scripts

| Script | What it does | Idle cost |
|--------|----------------|-----------|
| `./scripts/labs-start.sh --all` | Local Docker + AWS (recommended) | **~$1.50–3/day** while running |
| `./scripts/labs-stop.sh` | Stop local Docker + AWS minimize mode | **~$0–2/month** |
| `./scripts/labs-status.sh` | Show local/AWS state and cost mode | — |
| `./scripts/labs-stop.sh --destroy` | Delete all AWS resources | **$0** |
| `./scripts/aws-start.sh` | AWS only (NAT + ALB + ECS) | **~$1.50–3/day** |
| `./scripts/aws-stop.sh` | AWS minimize-cost stop | **~$0–2/month** |
| `./scripts/aws-destroy.sh` | Full AWS teardown | **$0** |

## Typical teaching week

```bash
# Monday — start class environment (local + AWS)
./scripts/labs-start.sh --all

# Check what's running
./scripts/labs-status.sh

# Friday — stop to avoid weekend charges
./scripts/labs-stop.sh

# End of course — zero AWS bill
./scripts/labs-stop.sh --destroy
```

## Faster AWS restart (same day, images already in ECR)

```bash
./scripts/labs-start.sh --aws-only --skip-build
```

## What aws-stop removes (cost drivers)

- NAT Gateway (~$0.045/hr)
- Application Load Balancer (~$0.0225/hr)
- ECS Fargate tasks (vCPU/memory per hour)

## What remains (low cost)

- VPC, subnets (free)
- ECR image storage (cents)
- DynamoDB on-demand with no traffic (cents)
- EventBridge bus (free tier)

## Full teardown

```bash
./scripts/aws-destroy.sh
# type: destroy
```

## Redeploy after code changes (platform running)

```bash
./scripts/aws-deploy.sh
```
