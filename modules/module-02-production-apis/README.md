# Module 2 – Building Production APIs

## Goal

Ship **enterprise-quality APIs** with:

- consistent request/response contracts
- input validation
- standardized error responses
- API versioning and backward compatibility
- OpenAPI generation and contract-first workflows
- testability and container packaging (foundation for later ECS/EKS modules)

## What you will build

A FastAPI microservice starter (`catalog-service`) that includes:

- `/api/v1` and `/api/v2` versioned endpoints
- request ID correlation (`X-Request-Id`)
- health endpoints (`/health/live`, `/health/ready`)
- error contract returned for validation errors, 404s, and 500s
- OpenAPI export script
- unit tests and Dockerfile

## Prerequisites

- Python 3.11+
- Docker (for container build/run)

## Quickstart (starter service)

```bash
cd modules/module-02-production-apis/starter/catalog-service
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest
uvicorn app.main:app --reload --port 8000
```

Then open:

- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`


