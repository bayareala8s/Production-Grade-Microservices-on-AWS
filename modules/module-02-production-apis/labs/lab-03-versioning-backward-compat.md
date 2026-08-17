# Lab 03 — API Versioning & Backward Compatibility

## Outcome

You will:

- understand practical API versioning approaches
- run both v1 and v2 endpoints side-by-side
- make a change in v2 without breaking v1 consumers

## Steps

### 1) Compare v1 vs v2 responses

```bash
curl -s http://localhost:8000/api/v1/products | jq
curl -s http://localhost:8000/api/v2/products | jq
```

### 2) Add a field only to v2

In `app/api/v2/schemas.py`, add a field (example: `tags: list[str] = []`).

Update only the v2 route implementation to return the new field.

### 3) Confirm v1 is unchanged

Re-run the two curl commands. v1 should not change shape.

## Checkpoint

- Both `/api/v1/...` and `/api/v2/...` are supported concurrently.


