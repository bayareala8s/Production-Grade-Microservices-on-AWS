# Module 6 — Instructor Guide

## Teaching goals

Students should leave with a security mindset that is:

- practical (works with AWS primitives)
- least-privilege oriented
- production-operable (rotation, debugging, ownership)

## Suggested pacing (example: 4 hours)

- 30 min: threat model + shared responsibility refresher
- 75 min: IAM deep dive + lab
- 45 min: secrets + lab
- 45 min: JWT auth + lab
- 45 min: network isolation + lab

## Key talking points

- Microservices security is “who can do what” at scale. IAM is the backbone.
- **AuthN** decides “who”; **AuthZ** decides “can they do it”.
- Secrets must be treated like runtime dependencies with owners and rotation.
- Networks reduce blast radius but do not replace IAM.

## Common pitfalls (and coaching)

- **Pitfall**: Use `*` in policy actions/resources.
  - **Coach**: require a dependency list first, then translate into a minimal policy.
- **Pitfall**: Validate JWT signature but ignore `aud`/`iss`/`exp`.
  - **Coach**: treat these as mandatory checks; show real incident examples.
- **Pitfall**: Put everything in a public subnet “for simplicity”.
  - **Coach**: show a minimal 2-subnet architecture and what must remain public.

## Suggested discussion prompts

- What should be allowed from the internet vs only internal?
- Which team owns secret rotation? What breaks when rotation happens?


