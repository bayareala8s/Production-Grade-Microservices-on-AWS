# Lab 03 — JWT Auth at the API Boundary

## Outcome

You will implement JWT validation logic and document the required checks.

## What “good” looks like

JWT validation includes:

- verify signature (using rotating keys)
- verify `iss` (issuer)
- verify `aud` (audience)
- verify `exp` (expiry) and optionally `nbf`
- map claims to authorization (roles/scopes)

## Steps

### 1) Define token contract

Create a short spec:

- `iss`: `https://auth.example.com/`
- `aud`: `catalog-service`
- claims used: `sub`, `scope` or `roles`

### 2) Add auth middleware/dependency

Use the reference pseudocode in:

- `starter/auth/jwt-validation-checklist.md`

### 3) Add protected endpoints

Pick one endpoint in your service and require auth.

### 4) Test failure modes

Write down expected responses for:

- missing token
- expired token
- wrong audience
- invalid signature

## Checkpoint

- Auth failures return consistent errors and do not leak internal details.


