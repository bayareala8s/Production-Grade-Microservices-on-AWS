# Module 4 — Course Outline (Instructor)

## Recommended duration

3–5 hours

## Learning objectives

- understand external vs internal service exposure
- learn traffic management primitives: gateway, load balancer, service discovery
- model and mitigate failures using timeouts/retries/backoff

## Lesson plan (suggested)

### Part A — Entry points (45–60 min)

- API Gateway: auth, throttling, request validation, API keys, WAF integration
- ALB: L7 load balancing for services, sticky sessions, path-based routing
- common patterns:
  - API Gateway → ALB → ECS
  - CloudFront → API Gateway → services

### Part B — Internal traffic and discovery (30–45 min)

- public vs private subnets
- security groups as “firewall rules”
- service discovery concepts (Cloud Map) and alternatives

### Part C — Reliability basics (60–90 min)

- timeout budgets
- retry policies (limited retries, exponential backoff, jitter)
- circuit breaker concept and bulkheads
- “avoid retry storms” workshop

### Part D — Lab wrap-up (15 min)

- students present their failure simulation and mitigation choices


