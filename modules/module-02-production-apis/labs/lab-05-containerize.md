# Lab 05 — Containerize Like Production (Baseline)

## Outcome

You will:

- build and run the service via Docker
- understand what needs to be configured for later ECS deployment

## Steps

### 1) Build image

```bash
cd modules/module-02-production-apis/starter/catalog-service
docker build -t catalog-service:local .
```

### 2) Run container

```bash
docker run --rm -p 8000:8000 \
  -e LOG_LEVEL=INFO \
  catalog-service:local
```

### 3) Smoke test

```bash
curl -s http://localhost:8000/health/ready
curl -s http://localhost:8000/api/v1/products
```

## Checkpoint

- Service runs reliably inside a container.


