# Lab 02 — Build & Push to ECR

## Outcome

You will define an image tagging and publishing strategy.

## Steps

### 1) Choose tag strategy

Recommended:

- `service:sha-<git_sha>`
- `service:main` (mutable convenience tag)

### 2) Authenticate to ECR

Use AWS auth in CI via:

- OIDC federation (preferred), or
- long-lived credentials (not recommended)

### 3) Push image

Confirm:

- image exists in ECR
- tag points to correct digest

## Checkpoint

- Students can explain why “rebuild for prod” is risky and how promotion works.


