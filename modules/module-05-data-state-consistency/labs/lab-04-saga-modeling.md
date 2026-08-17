# Lab 04 — Saga Modeling (Business Process)

## Outcome

You will model a business process as a saga and define compensations.

## Scenario: Place Order

High-level steps:

1. Create Order (orders)
2. Reserve Inventory (inventory)
3. Authorize Payment (payments)
4. Confirm Order (orders)

## Tasks

### 1) Choose saga style

Pick one:

- **Choreography**: services react to events; no central coordinator
- **Orchestration**: one coordinator drives steps and decisions

Write down why you chose it for this scenario.

### 2) Define happy-path events/messages

List the events for each step and which service publishes/consumes them.

### 3) Define failure cases + compensations

At minimum define:

- inventory reservation fails → cancel order
- payment authorization fails → release inventory + cancel order
- order confirmation fails after payment authorized → refund/void payment + release inventory

### 4) Define timeouts and retry limits

For each step:

- timeout budget
- retry policy (max attempts, backoff)
- “poison” handling (DLQ, manual intervention)

## Checkpoint

- You have a full saga diagram in text form and can explain compensations.


