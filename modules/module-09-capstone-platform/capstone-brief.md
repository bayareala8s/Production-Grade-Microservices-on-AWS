# Capstone Brief — Production Microservices Platform

## What you must deliver

### Architecture deliverables

- system context diagram + container diagram (or equivalent)
- service ownership + data ownership table
- API contracts (OpenAPI) and/or event contracts (schemas + versions)

### Implementation deliverables

- at least **3 services**
- at least **one integration path**:
  - synchronous (API calls), and/or
  - asynchronous (events via EventBridge/SQS)
- database-per-service (can be DynamoDB/RDS/SQLite for local demo)

### Operations deliverables

- dashboards (logs/metrics/traces where available)
- health endpoints
- runbook for “service is down” and “latency spike”
- CI pipeline + safe deployment strategy

## Non-negotiable requirements

- every service has a clear owner and on-call expectation (simulated)
- APIs are versioned or changes are explicitly backward compatible
- error responses are standardized
- a failure mode is demonstrated and mitigated (timeout/retry, circuit breaker, DLQ, etc.)

## Demo requirements (10–15 min)

- architecture overview
- walk a critical user flow end-to-end
- show a dashboard and trace/log correlation
- trigger one failure and show mitigation/rollback


