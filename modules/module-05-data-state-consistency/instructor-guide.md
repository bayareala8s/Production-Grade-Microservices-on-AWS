# Module 5 — Instructor Guide

## Teaching goals

Help students internalize that data in microservices is:

- **owned** by a service (and its team)
- **propagated** to other services via contracts (APIs/events)
- subject to **partial failure** and **duplicates**

## Suggested pacing (3–6 hours)

- 45–60 min: Data ownership + integration choices
- 45–60 min: Consistency models + read models
- 60–90 min: Idempotency patterns (API + event handlers)
- 45–75 min: Saga intro + business process modeling workshop
- 15 min: Presentations / review

## Key talking points (high signal)

- “Shared database” is shared **deployment + incident domain**.
- You don’t “choose eventual consistency”; you accept reality and engineer for it.
- At-least-once delivery ⇒ **duplicates are normal**.
- Sagas are about **business invariants** and **compensation**, not tech hype.

## Common pitfalls (and coaching)

- **Pitfall**: Students design “global transaction manager”.
  - **Coach**: Ask what team owns it, how it scales, what happens during outages.
- **Pitfall**: Students treat events as “async RPC”.
  - **Coach**: Emphasize event meaning (“something happened”), not “do this”.
- **Pitfall**: Missing versioning in event schemas.
  - **Coach**: Require event name + `schema_version` (or explicit versioned type).

## Lab facilitation tips

- Keep labs lightweight on AWS setup; focus on **thinking and patterns**.
- Use the included example payloads as “contract artifacts” students can review.

## What to preview for next modules

- Module 6: IAM roles, secrets, network isolation for service ownership
- Module 7: tracing and debugging async flows (EventBridge/SQS) with correlation IDs


