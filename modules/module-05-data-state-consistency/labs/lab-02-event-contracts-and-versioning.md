# Lab 02 — Event Contracts & Versioning

## Outcome

You will define **event contracts** that are stable enough for production:

- explicit names
- explicit schema versions
- required/optional fields
- examples (payloads)

## Steps

### 1) Define event names (domain meaning)

Use “something happened” names, not commands:

- `OrderCreated`
- `OrderCancelled`
- `PaymentAuthorized`
- `PaymentFailed`
- `InventoryReserved`
- `InventoryReservationFailed`

### 2) Define a minimal schema

Each event should contain:

- `event_type` (or use the bus’s native type field)
- `schema_version`
- `event_id` (UUID)
- `occurred_at` (ISO timestamp)
- a **business key** (e.g., `order_id`)
- the relevant payload fields for consumers

### 3) Create a versioning rule

Write down rules students must follow:

- additive fields are OK (new optional fields)
- breaking changes require a new `schema_version` (or new event type name)
- consumers must ignore unknown fields

## Checkpoint

- You produced at least 4 event definitions with examples.


