# Architecture Doc Template

## 1) Overview

One paragraph: what does the system do and for whom?

## 2) Diagrams

- system context diagram
- service diagram (services + data stores + event bus)

## 3) Services

| Service | Owner | Responsibilities | Data owned | Dependencies |
|---|---|---|---|---|
| orders | Team A | ... | Orders table | payments, inventory |

## 4) Contracts

- APIs (OpenAPI links/exports)
- Events (schemas + versioning rules)

## 5) Critical flows

Describe at least one end-to-end flow:

- step-by-step sequence
- failure handling (timeouts/retries/compensations)

## 6) Security

- authn/authz approach
- IAM roles/permissions summary
- secrets strategy
- network layout summary

## 7) Observability & SLOs

- dashboards
- SLIs/SLOs
- alert strategy

## 8) Deployment

- CI pipeline
- deploy strategy (rolling/blue-green)
- rollback plan


