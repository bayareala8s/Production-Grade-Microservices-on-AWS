# Typical Microservices on AWS (Reference)

## High-level components

- **Edge/entry**: CloudFront + WAF (optional) → API Gateway and/or ALB
- **Compute**: ECS Fargate (or EKS / Lambda depending on workloads)
- **Async**: EventBridge for domain events; SQS for work queues (optional)
- **Data**: database-per-service (DynamoDB/RDS/Aurora/etc.)
- **Identity**: JWT/OAuth at the edge; IAM task roles inside AWS
- **Observability**: CloudWatch logs/metrics + X-Ray/OTel tracing
- **CI/CD**: pipelines per service; blue/green or rolling deployments

## Recommended production defaults (teach these)

- versioned API contracts and standardized errors
- timeouts + retries with backoff + jitter (avoid retry storms)
- correlation IDs end-to-end
- least-privilege task roles (no shared “mega role”)
- dashboards aligned to SLIs/SLOs (not just CPU graphs)

## Common variants

- **API Gateway** for auth/throttling + request validation at the edge
- **ALB** for path routing to services; often paired with ECS
- **Service-to-service**: direct HTTP inside VPC, or async events for decoupling


