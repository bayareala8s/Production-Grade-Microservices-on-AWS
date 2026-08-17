# Module 1 — Instructor Guide

## Teaching goals

- Prevent “microservices cargo culting”
- Teach **ownership + operability** as first-class requirements
- Build strong design narratives students can use in interviews

## Prompts that work well

- “What is the single biggest reason to NOT choose microservices for this product?”
- “What does the on-call person need at 2am to debug this?”
- “Which team owns the data? Who gets paged when it breaks?”

## Common pitfalls

- Designing around frameworks instead of domains
- Sharing a single database “because it’s easier”
- Over-splitting services too early (too many deployables)
- Ignoring failure modes (“it’ll be fine in prod”)

## Coaching tips

- Ask students to define **service-level SLOs** even if they can’t implement yet.
- Force explicit contracts: OpenAPI for sync APIs, event schema for async.
- Require a “dependency map” with at least one failure scenario.


