# Module 3 — Instructor Guide

## Prep checklist

- students have AWS accounts with permissions to create ECS, IAM roles, and VPC components (or a pre-provisioned sandbox)
- AWS CLI configured (or use the AWS Console for labs)
- Docker installed and able to build local images

## Coaching notes

- keep the first ECS deployment simple (public IP) before introducing ALB
- emphasize immutable artifacts: build once, deploy the same image everywhere
- explain that “ECS Fargate” is a runtime choice, not an architecture by itself

## Common pitfalls

- missing task execution role (cannot pull images / write logs)
- security group rules block inbound traffic
- confusion between task definition vs service vs cluster


