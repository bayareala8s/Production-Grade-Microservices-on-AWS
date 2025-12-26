# JWT Validation Checklist (Reference)

Use this as a “minimum required checks” list for production-style JWT validation.

## Required checks

- **Signature**: verify using the correct key (supports rotation)
- **Issuer (`iss`)**: exact match against expected issuer
- **Audience (`aud`)**: expected service/client audience
- **Expiry (`exp`)**: reject expired tokens; allow small clock skew
- **Not before (`nbf`)** (if present): reject tokens not yet valid

## Authorization mapping

- decide whether you use `scope` (OAuth) or `roles` claims
- enforce least privilege per endpoint (don’t just “check token exists”)

## Operational notes

- cache JWKS keys with TTL and refresh on unknown key ID (`kid`)
- don’t log full tokens; log request IDs and claim subsets (e.g., `sub`)


