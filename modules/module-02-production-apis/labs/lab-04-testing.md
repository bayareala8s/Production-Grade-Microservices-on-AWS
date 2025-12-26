# Lab 04 — Testing Production APIs

## Outcome

You will:

- add tests that enforce **contracts**
- validate error responses, not just “happy path” behavior

## Steps

### 1) Run tests

```bash
cd modules/module-02-production-apis/starter/catalog-service
pytest -q
```

### 2) Add a contract test

Add a test that asserts:

- `GET /api/v1/products` returns a list of objects each with `id`, `name`, `price_usd`
- headers include `X-Request-Id`

### 3) Add an error contract test

Add a test that asserts invalid body returns:

- `status_code == 422`
- `error.code == "validation_error"`
- `request_id` is present

## Checkpoint

- Tests fail when the API contract changes unintentionally.


