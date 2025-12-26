# Lab 02 — Internal Service-to-Service Calls (Concept + Implementation Option)

## Outcome

Students understand internal calls and how private networking affects design.

## Concept checklist

Answer:

- Which services are public? Which are internal only?
- What network boundary enforces that? (security group, private subnet)
- How do services discover each other? (DNS, Cloud Map, config)

## Optional implementation (local)

Run two services locally:

- `catalog-service` (Module 2)
- a simple “client” script that calls it with timeouts and retries

Deliverable:

- document the chosen timeout and retry policy and why


