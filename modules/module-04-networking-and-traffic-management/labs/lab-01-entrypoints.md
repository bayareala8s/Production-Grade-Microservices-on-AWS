# Lab 01 — Entry Points: API Gateway vs ALB

## Outcome

Students select the right entrypoint pattern and justify it.

## Prompts

For each scenario, choose **one** primary entrypoint:

- API Gateway
- ALB

### Scenario A — Public API with auth and throttling

- needs JWT/OAuth integration later
- needs rate limiting and WAF

### Scenario B — Internal-only service mesh of APIs

- only called by other services
- simpler L7 routing required

### Scenario C — Large file uploads

- needs streaming / large payload handling

## Deliverable

One page:

- choice per scenario
- why it fits
- what the tradeoff is


