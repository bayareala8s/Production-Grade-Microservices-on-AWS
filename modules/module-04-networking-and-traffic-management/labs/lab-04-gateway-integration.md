# Lab 04 — API Gateway → ECS Integration (Optional / Conceptual)

## Outcome

Students understand how API Gateway can front ECS services.

## Pattern options

- API Gateway (HTTP API) → VPC Link → ALB → ECS
- API Gateway → Lambda → internal service (not recommended for high throughput unless needed)

## Steps (conceptual)

1. Deploy ECS service behind an ALB (from Module 3 extension).
2. Create an API Gateway HTTP API.
3. Create an integration to the ALB via VPC Link.
4. Add routes like `GET /api/v1/products`.

## Checkpoint

- API Gateway endpoint returns responses from the ECS service.


