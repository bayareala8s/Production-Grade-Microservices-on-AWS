# Lab 01 — API Contracts & OpenAPI (Contract-First Mindset)

## Outcome

You will:

- understand **what a stable API contract** means in production
- generate and export an **OpenAPI spec** from a running service
- validate that your service contract stays consistent across changes

## Why this matters in enterprise systems

In production, APIs are consumed by:

- other microservices
- frontend teams
- external partners

Contract instability is one of the fastest ways to create incidents.

## Steps

### 1) Run the starter service

```bash
cd modules/module-02-production-apis/starter/catalog-service
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload --port 8000
```

### 2) Inspect interactive docs

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 3) Export the OpenAPI spec

In a separate terminal:

```bash
python scripts/export_openapi.py --base-url http://localhost:8000 --out openapi.generated.json
```

### 4) Treat the spec as an artifact

In production teams, you typically:

- store the OpenAPI file in the repo (or publish it)
- run a CI step to diff contract changes
- review breaking changes before merge

## Checkpoint

- You can access `GET /openapi.json`
- You generated `openapi.generated.json`


