# ECS Blue/Green Notes (Reference)

## What blue/green gives you

- validate the new version without fully switching traffic
- fast rollback by switching the listener back

## What you need

- ALB listener + two target groups
- health checks configured correctly (path, port, thresholds)
- deployment controller (CodeDeploy-style) or custom routing automation

## Promotion gates (recommended)

- smoke tests pass against green target group
- no elevated 5xx
- latency within budget


