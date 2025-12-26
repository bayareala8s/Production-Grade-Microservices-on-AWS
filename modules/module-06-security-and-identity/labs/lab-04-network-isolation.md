# Lab 04 — Network Isolation (VPC, Subnets, Security Groups)

## Outcome

You will design a minimal network layout that reduces blast radius.

## Scenario

- `api-gateway` or `alb` is public entry
- `catalog-service` should be reachable only from the entry point
- `payments-service` should be internal-only

## Tasks

### 1) Draw the minimal layout

Include:

- public subnets (ingress only)
- private subnets (services + databases)
- NAT or egress strategy (if needed)

### 2) Define security group rules

Write the rules explicitly:

- inbound allowed sources + ports
- outbound allowed destinations + ports (avoid “all egress” unless justified)

### 3) Identify admin-only endpoints

Define which endpoints should never be public:

- `/admin/*`
- `/internal/*`

## Checkpoint

- Services in private subnets are not directly reachable from the internet.


