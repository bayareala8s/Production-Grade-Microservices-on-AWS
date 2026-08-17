# Module 7 — Course Outline (Instructor)

## Recommended duration

3–6 hours

## Learning objectives

- understand the difference between logs, metrics, and traces
- implement correlation for debugging distributed systems
- define SLIs/SLOs that reflect customer experience
- apply production testing: smoke tests, canaries, synthetic checks

## Lesson plan (suggested)

### Part A — Observability fundamentals (30–45 min)

- what each signal is best at (logs/metrics/traces)
- “unknown unknowns” and why dashboards alone don’t solve incidents
- correlation IDs across services (request ID, trace ID)

### Part B — Structured logging (45–60 min)

- JSON logs, stable fields, redaction
- logging for incident response (who/what/when/where)
- lab tie-in: `labs/lab-01-structured-logging.md`

### Part C — Metrics + dashboards (45–75 min)

- golden signals (latency, traffic, errors, saturation)
- service-level vs dependency-level metrics
- lab tie-in: `labs/lab-02-metrics-dashboards.md`

### Part D — Tracing (45–75 min)

- spans, context propagation
- tracing async workflows (events/queues)
- lab tie-in: `labs/lab-03-tracing.md`

### Part E — SLIs/SLOs + reliability tests (45–90 min)

- choosing SLIs/SLOs
- canaries, smoke tests, synthetic monitoring
- lab tie-in: `labs/lab-04-sli-slo.md` and `labs/lab-05-synthetics.md`

## Instructor checkpoints

- students can propose a dashboard that maps to user experience
- students can define one SLO and explain alerting thresholds
- students can describe a debugging flow using logs + traces


