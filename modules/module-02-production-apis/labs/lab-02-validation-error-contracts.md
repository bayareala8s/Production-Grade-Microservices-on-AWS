# Lab 02 — Validation & Standard Error Contracts

## Outcome

You will:

- implement and test a **standard error response**
- ensure validation errors are returned consistently (not framework defaults)

## Error contract used in this module

All errors return JSON shaped like:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "details": [
      { "loc": ["body", "price_usd"], "msg": "Field required", "type": "missing" }
    ]
  },
  "request_id": "..."
}
```

## Steps

### 1) Trigger a validation error

Run the service, then:

```bash
curl -s -X POST http://localhost:8000/api/v1/products \
  -H 'Content-Type: application/json' \
  -d '{"name": "Keyboard"}' | jq
```

### 2) Confirm request correlation

```bash
curl -i http://localhost:8000/health/live | sed -n '1,20p'
```

You should see an `X-Request-Id` header returned.

### 3) Add a new validation rule

In `app/api/v1/schemas.py`, add a constraint (example: `name` min length).

### 4) Update tests

Update or add a test in `tests/` that asserts:

- status code is correct
- `error.code` and `request_id` are present

## Checkpoint

- All validation errors conform to the module error contract.


