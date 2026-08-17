# Module 7 — Instructor Guide

## Teaching goals

Students should learn to:

- pick signals that matter (not “graph everything”)
- debug distributed failures with correlation
- operationalize reliability with SLIs/SLOs and alerts

## Common pitfalls

- **Pitfall**: Dashboards show system health but not user impact.
  - **Coach**: start with “what does the customer experience?” then map metrics.
- **Pitfall**: Logging PII or secrets.
  - **Coach**: require a redaction rule and “never log tokens”.
- **Pitfall**: Alert fatigue.
  - **Coach**: alerts should be tied to SLOs and actionable.

## Facilitation tips

- Ask students to narrate an incident: “user reports checkout failure” → how do you debug?
- Keep SLOs simple at first (availability/latency for one endpoint).


