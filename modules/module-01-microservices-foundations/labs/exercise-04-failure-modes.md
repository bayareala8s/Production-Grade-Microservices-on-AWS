# Exercise 04 — Failure Modes (Design-Only “Game Day”)

## Outcome

Students learn to anticipate real production failures and propose mitigations.

## Instructions (30–45 min)

1. Draw a dependency map of your 3 services.
2. Pick **one** of the scenarios below.
3. Describe what breaks, what users see, and what mitigations exist.

## Scenarios

### Scenario A — Dependency timeout

Service A calls Service B. Service B becomes slow and starts timing out.

Questions:

- What happens to Service A threads/worker pool?
- What happens if you retry? What if every request retries?
- What timeouts and backoffs would you set?

### Scenario B — Duplicate events

Service C receives the same “order created” event twice.

Questions:

- What data gets corrupted?
- How do you make handlers idempotent?

### Scenario C — Partial outage

One service is down. Users still need partial functionality.

Questions:

- Which features can degrade gracefully?
- What does the UI/API return?

## Deliverable

One page “incident narrative” including:

- symptoms
- blast radius
- mitigation and long-term fixes


