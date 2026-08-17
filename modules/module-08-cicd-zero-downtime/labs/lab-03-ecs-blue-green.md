# Lab 03 — ECS Blue/Green Deployment (Conceptual + Template)

## Outcome

You will understand blue/green deploy flow and configure a template.

## Steps

### 1) Understand routing

Blue/green requires:

- two target groups (blue and green)
- a way to shift traffic (ALB listener rules)
- health checks to validate the new version

### 2) Define promotion gates

Write down what must be true before switching traffic:

- smoke tests pass
- error rate below threshold
- latency within budget

### 3) Review starter artifacts

See:

- `starter/codedeploy/appspec.yml` (reference)
- `starter/ecs/bluegreen-notes.md`

## Checkpoint

- Students can describe the blue/green lifecycle and where rollback happens.


