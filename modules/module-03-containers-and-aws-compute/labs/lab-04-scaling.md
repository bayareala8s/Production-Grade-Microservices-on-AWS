# Lab 04 — Scaling Basics (ECS Service)

## Outcome

Students learn how ECS scaling works and how to validate it.

## Steps

### 1) Scale desired count

Change desired tasks from 1 → 2 (or 3).

### 2) Validate

- ECS shows multiple tasks `RUNNING`
- service still responds to `/health/ready`
- verify logs for each task in CloudWatch

### 3) Discuss autoscaling signals (conceptual)

Common choices:

- CPU utilization
- memory utilization
- ALB request count per target
- custom metrics (latency, queue depth)

## Checkpoint

- student can explain desired count vs autoscaling and show multiple tasks running.


