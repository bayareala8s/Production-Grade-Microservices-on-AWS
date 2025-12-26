# Lab 03 — Distributed Tracing (Request → Dependencies)

## Outcome

You will define how a request is traced across services.

## Steps

### 1) Define propagation rules

Pick a propagation method:

- `traceparent` (W3C)
- `X-Amzn-Trace-Id` (X-Ray)

### 2) Define what gets a span

At minimum:

- inbound HTTP request
- outbound call to dependency (HTTP/db/event publish)

### 3) Define trace search workflow

Write down how you answer:

- “why is latency spiking?”
- “which dependency is failing?”

## Checkpoint

- Students can explain how they would trace a request end-to-end.


