# Observability Reference (Logs, Metrics, Traces)

## Logs

- structured JSON logs
- correlation fields: `request_id`, `trace_id`, `service`
- redact secrets/PII

## Metrics

Teach the “golden signals”:

- latency
- traffic
- errors
- saturation

## Traces

- propagate trace context on inbound/outbound calls
- use spans for dependency calls (HTTP, DB, queues, event publish)

## Recommended debugging workflow (teach this)

1. Start with user-impact dashboard (errors/latency)
2. Find a representative request ID / trace ID
3. Use trace to locate slow/failing dependency
4. Use logs for high-cardinality context and details


