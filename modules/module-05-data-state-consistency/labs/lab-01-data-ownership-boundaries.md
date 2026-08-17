# Lab 01 — Data Ownership & Boundaries

## Outcome

You will produce a short design doc that clearly answers:

- which service **owns** each piece of data
- which service is the **source of truth**
- how other services get the data they need (API vs events)

## Scenario

You have three services:

- `orders`: owns orders
- `payments`: owns payment intents/transactions
- `inventory`: owns stock counts

## Tasks

### 1) Define the ownership table

Create a table with:

- **data entity** (Order, PaymentIntent, StockItem, Reservation)
- **owning service**
- **consumers**
- **integration method** (sync API, async event, or both)

### 2) Identify shared-db anti-patterns

List at least 3 ways a shared database causes coupling:

- deployment coupling
- schema change blast radius
- incident/lock contention

### 3) Choose integration paths

For each integration, decide:

- API read (query-time) vs event replication (projection)
- what happens during outages (stale reads, degraded mode, etc.)

## Checkpoint

- You can explain “who owns what data” without ambiguity.


