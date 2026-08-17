# Exercise 02 — Decompose a Monolith into 3 Services

## Scenario (provided)

You have a monolithic “Store” backend that handles:

- product catalog
- orders
- payments
- inventory updates
- user accounts

## Instructions (30–45 min)

Decompose the monolith into **exactly 3 services**.

For each service define:

- name and responsibility
- owned data (tables/collections) — assume **no shared database**
- primary APIs (sync) and/or events (async)
- dependencies on other services
- what team owns it

## Guardrails

- avoid “god services” (one service owns everything)
- avoid “anemic services” (one service per table)
- keep boundaries aligned to the domain (bounded contexts)

## Deliverables

1. Context diagram showing the 3 services and integrations
2. One paragraph justification of tradeoffs



