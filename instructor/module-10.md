# Instructor Notes — Module 10 (Capstone)

## Demo day logistics

- Strict timekeeper
- Backup recording if live demo fails (video acceptable)
- Rubric scoring sheet per presenter

## Architecture review checkpoint (Week 10 Day 1)

Approve or send back for revision before heavy coding.

## Enterprise cohort

Offer banking/SaaS/FinOps rubric adjustments (fraud service, tenant isolation, read-only idle-cost IAM).

## Option 4 — Idle Cost Advisor

- Reject single-script submissions; require ≥ 3 ECS services + events.
- Require **read-only** IAM and recommend-only actions (no auto-destroy in demo).
- Decomposition template: `capstone/templates/option-4-idle-cost-decomposition.md`.
- Strong demos tie findings back to course `./scripts/labs-stop.sh`.
