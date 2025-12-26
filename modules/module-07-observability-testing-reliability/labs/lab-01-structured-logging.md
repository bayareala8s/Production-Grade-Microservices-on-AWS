# Lab 01 — Structured Logging (Production Style)

## Outcome

You will define a logging schema and ensure logs are usable during incidents.

## Steps

### 1) Define a minimal JSON log schema

Required fields:

- `ts`
- `level`
- `service`
- `msg`
- `request_id` (and/or `trace_id`)
- `path` and `method` (for API logs)

### 2) Define a redaction policy

List what must never be logged:

- credentials, secrets, tokens
- payment details
- PII beyond a safe identifier

### 3) Add error logging conventions

Define:

- how you log exceptions
- how you tag errors with request/trace IDs
- what information goes into logs vs metrics vs traces

## Checkpoint

- Given a request ID, a student can locate all related logs.


