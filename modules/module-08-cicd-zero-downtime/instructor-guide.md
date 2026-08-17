# Module 8 — Instructor Guide

## Teaching goals

Students should learn to make shipping safe by default:

- automated checks over manual heroics
- predictable rollout strategies
- fast rollback paths

## Common pitfalls

- **Pitfall**: “CI passes” but deployments still break due to config drift.
  - **Coach**: introduce environment config as code; validate at deploy time.
- **Pitfall**: No artifact promotion (rebuilding for prod).
  - **Coach**: emphasize provenance and repeatability.
- **Pitfall**: No post-deploy checks.
  - **Coach**: require smoke tests and alarms as gates.

## Suggested prompts

- What metric would you gate deploy on?
- What does “rollback” mean for stateful changes?


