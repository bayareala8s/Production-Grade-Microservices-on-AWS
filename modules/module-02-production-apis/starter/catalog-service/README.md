# Catalog Service (Starter)

Production-grade API starter used in Module 2.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload --port 8000
```

## Run tests

```bash
pytest -q
```

## Export OpenAPI

```bash
python scripts/export_openapi.py --base-url http://localhost:8000 --out openapi.generated.json
```

## Docker

```bash
docker build -t catalog-service:local .
docker run --rm -p 8000:8000 catalog-service:local
```


