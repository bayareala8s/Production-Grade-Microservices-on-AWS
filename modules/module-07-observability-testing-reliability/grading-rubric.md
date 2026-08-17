# Module 7 — Grading Rubric (Suggested)

## Total: 100 points

### Logs (25)

- 10: Structured logs with stable fields (level, service, request_id/trace_id)
- 10: Redaction rules (no secrets/PII) and consistent error logging
- 5: Logs are usable for incident debugging (actionable messages)

### Metrics & dashboards (30)

- 10: Golden signals are covered (latency/traffic/errors/saturation)
- 10: Dashboard maps to user experience (endpoint-level, not only infra)
- 10: Alarms are meaningful and not overly noisy

### Tracing (25)

- 10: Context propagation is understood and documented
- 10: A trace can be followed across at least 2 components
- 5: Explains how to trace async/event-driven flows

### SLIs/SLOs + testing (20)

- 10: Defines at least one SLO with measurement window and target
- 10: Includes smoke/canary/synthetic check plan


