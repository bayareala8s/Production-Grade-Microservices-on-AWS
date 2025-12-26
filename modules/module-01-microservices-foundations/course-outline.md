# Module 1 — Course Outline (Instructor)

## Recommended duration

2–3 hours

## Learning objectives

- understand tradeoffs: microservices are not “better”, they are different
- define bounded contexts and service ownership boundaries
- reason about data ownership and integration patterns
- anticipate production failure modes and design mitigations

## Lesson plan (suggested)

### Part A — Why microservices (and why not) (30–40 min)

- monolith strengths: simplicity, transactions, lower ops overhead
- microservices strengths: independent deploy, scaling, team autonomy
- hidden costs: distributed systems, consistency, testing, ops complexity
- “microservices readiness checklist” (see `labs/exercise-01-readiness.md`)

### Part B — Bounded contexts & ownership (35–50 min)

- domain-driven design (lightweight): bounded contexts
- service ownership: one team owns code + runtime + data + on-call
- “conway’s law” mapping: org structure ↔ architecture
- design exercise: decomposition of a monolith into 3 services

### Part C — Integration patterns & failure modes (40–60 min)

- synchronous calls (REST/gRPC) vs async events (SNS/SQS/EventBridge)
- fallacies of distributed computing (latency, partial failure, etc.)
- production failure modes:
  - timeout amplification / retry storms
  - cascading failure / dependency meltdown
  - data inconsistency / duplicate events
  - schema drift / breaking contract changes

### Part D — Wrap-up & deliverables (10–15 min)

- present designs
- highlight what will be implemented in Modules 2–5

## Instructor checkpoints

- students can define service boundaries + owned data
- students can identify at least 3 failure modes in their design
- students can choose sync vs async and justify the choice


