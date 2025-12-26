# Lab 01 — Docker Best Practices (Production Baseline)

## Outcome

Students can build a container image that is production-friendly and repeatable.

## Use this service

`modules/module-02-production-apis/starter/catalog-service`

## Tasks

1. Confirm `Dockerfile` builds and runs locally.
2. Explain the difference between:
   - image build time vs container runtime
   - environment variables vs secrets
3. Add (optional) improvements:
   - pin dependency versions (already done in `requirements.txt`)
   - expose config through env vars only

## Checkpoint

- `docker build` succeeds
- `docker run -p 8000:8000 ...` serves `/health/ready`


