# Module 3 — Course Outline (Instructor)

## Recommended duration

3–5 hours (depending on AWS account setup speed)

## Learning objectives

- understand container fundamentals (images, layers, runtime)
- apply Docker best practices (small images, least privilege, env config)
- choose compute: ECS Fargate vs EKS vs Lambda
- deploy to ECS Fargate and perform a basic scale test

## Lesson plan (suggested)

### Part A — Docker production fundamentals (45–60 min)

- Dockerfile best practices: caching, small base images, deterministic builds
- runtime config: env vars, secrets, non-root (conceptual)
- health endpoints: why ECS needs them

### Part B — Compute decision matrix (45–60 min)

- ECS Fargate: lowest ops overhead for containers
- EKS: flexibility + Kubernetes ecosystem, higher platform cost
- Lambda: event-driven, fast iteration, different constraints (cold start, limits)

### Part C — ECS Fargate deployment walkthrough (90–150 min)

- cluster/service/task definition concepts
- networking basics (VPC, subnets, security groups)
- ALB integration (if time) or direct public IP for simplest lab

### Part D — Scaling & cost intuition (30–45 min)

- horizontal scaling vs vertical
- CPU/memory sizing basics
- autoscaling signals (CPU, request count, latency via ALB)


