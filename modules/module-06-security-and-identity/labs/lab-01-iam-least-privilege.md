# Lab 01 — IAM Least Privilege for Microservices

## Outcome

You will produce a least-privilege IAM task role policy for a service and explain it.

## Scenario

Your `orders-service` on ECS needs to:

- write to DynamoDB table `Orders`
- publish events to EventBridge bus `orders-bus`
- read one secret `orders/db_password` from Secrets Manager

## Steps

### 1) Map dependencies

Write down:

- required AWS services
- required actions (read/write/list/publish)
- resource ARNs (table ARN, secret ARN, event bus ARN)

### 2) Start from deny-by-default

Write a policy that only includes the required actions and resources.

Use the template in:

- `starter/iam/orders-service-task-role-policy.json`

### 3) Add conditions (optional, advanced)

Add conditions where possible:

- limit by `aws:SourceVpce` (private endpoints)
- limit by encryption context or tags

## Checkpoint

- Policy contains no wildcard resources unless justified.


