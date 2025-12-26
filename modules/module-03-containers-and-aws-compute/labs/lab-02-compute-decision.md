# Lab 02 — Compute Decision Exercise (ECS vs EKS vs Lambda)

## Outcome

Students can justify compute choices using constraints.

## Scenarios

Pick one:

### Scenario A — Public API microservice

- steady traffic with occasional peaks
- needs VPC access to a database
- team wants minimal platform overhead

### Scenario B — Data processing pipeline

- large batch jobs, scheduled
- heavy CPU/memory
- teams already use Kubernetes

### Scenario C — Event-driven image resizing

- triggered by object uploads
- bursts + idle periods
- simple runtime

## Deliverable

For your chosen scenario, write:

- your compute choice (ECS Fargate / EKS / Lambda)
- top 3 reasons
- top 2 risks/tradeoffs


