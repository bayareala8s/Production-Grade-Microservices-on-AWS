# Lab 02 — Secrets Manager (Runtime Secrets)

## Outcome

You will define a secure way to store and access secrets without hardcoding.

## Steps

### 1) Define secret naming and ownership

Pick a convention:

- `/prod/orders/db_password`
- `/staging/orders/db_password`

Write down:

- who owns rotation
- who is allowed to read it (which service role)

### 2) Store the secret

In an AWS account, create a secret (console or CLI).

### 3) Wire runtime access

Decide one:

- ECS secrets injection (recommended)
- fetch at runtime from SDK (requires careful caching/error handling)

### 4) Audit access

Show how you would confirm:

- which role accessed the secret
- when it was accessed

## Checkpoint

- Secrets are not in code, images, or plain-text config committed to git.


