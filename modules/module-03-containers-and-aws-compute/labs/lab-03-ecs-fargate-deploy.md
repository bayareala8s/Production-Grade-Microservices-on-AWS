# Lab 03 — Deploy to ECS Fargate (Catalog Service)

## Outcome

Students can deploy a containerized microservice to ECS Fargate and access it.

## Pre-reqs

- AWS account
- AWS CLI configured (or use AWS Console)
- An ECR repository

## Artifact to deploy

Use the Module 2 service:

`modules/module-02-production-apis/starter/catalog-service`

## Steps (high-level)

### 1) Build and tag the image

```bash
cd modules/module-02-production-apis/starter/catalog-service
docker build -t catalog-service:local .
```

### 2) Push to ECR (conceptual)

- create ECR repo `catalog-service`
- authenticate docker to ECR
- tag and push the image

### 3) Create IAM roles

- task execution role: allows pulling image + writing logs
- task role: least-privilege permissions for your app (empty for now)

Reference policy template:

`modules/module-03-containers-and-aws-compute/starter/ecs-fargate/iam-task-execution-role-policy.json`

### 4) Register task definition

Use:

`modules/module-03-containers-and-aws-compute/starter/ecs-fargate/task-definition.json`

Replace:

- `REPLACE_WITH_ECR_IMAGE_URI`
- role ARNs
- region

### 5) Create an ECS service

Simplest path (teaching):

- Fargate service with **public IP**
- security group allows inbound TCP 8000 from your IP

### 6) Smoke test

Verify:

- `/health/ready`
- `/api/v1/products`

## Checkpoint

- A running ECS service responds to health checks and API calls.


