# Module 4 — Instructor Guide

## Prep checklist

- students deployed at least one service to ECS from Module 3 OR can run locally
- decide whether you’ll teach “Console-first” or IaC-first; this module supports both

## Coaching notes

- keep the failure simulation simple: add latency, then observe cascading effects
- highlight that retries “hide” failures briefly but can amplify load

## Common pitfalls

- retrying on non-idempotent requests without idempotency keys
- setting timeouts too high (threads get stuck) or too low (false errors)
- misunderstanding “where to configure” (client vs gateway vs load balancer)


