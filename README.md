# Production-Grade Microservices on AWS

This repository contains **enterprise-style course modules** for building, deploying, securing, and operating microservices on AWS.

## Modules

- `modules/module-01-microservices-foundations/`: when microservices make sense, boundaries, failure modes
- `modules/module-02-production-apis/`: robust versioned APIs (validation, error contracts, OpenAPI, tests)
- `modules/module-03-containers-and-aws-compute/`: Docker, ECS/EKS/Lambda tradeoffs, ECS Fargate baseline
- `modules/module-04-networking-and-traffic-management/`: entrypoints, internal calls, retries/timeouts, failure simulation
- `modules/module-05-data-state-consistency/`: database-per-service, events, idempotency, sagas, outbox/projections
- `modules/module-06-security-and-identity/`: IAM least privilege, secrets, JWT/OAuth concepts, network isolation
- `modules/module-07-observability-testing-reliability/`: logs/metrics/traces, SLIs/SLOs, canaries/synthetics
- `modules/module-08-cicd-zero-downtime/`: CI/CD pipelines, blue/green, release gates, rollback
- `modules/module-09-capstone-platform/`: capstone project brief + deliverables + grading templates

## How to use this repo

Each module contains:

- `README.md`: goals, outcomes, prerequisites
- `labs/`: step-by-step lab guides
- `starter/`: ready-to-run starter projects used in the labs

## Instructor pack

See `course/` for cross-module materials (syllabus, checklists, reference architectures).


