---
title: "[Tech] Domain model creation"
type: Tech
repo: tsqr-support
issue: https://github.com/lstbob/tsqr-support/issues/1
created: 2026-07-10
---

## Problem

The Support context has no domain model whatsoever.

### No domain aggregates
- `ITicketsRepository` takes primitive parameters: `CreateTicketAsync(string subject, int category, string description, ...)`
- `ISupportQueries` returns flat DTO records (`TicketListItemRow`, `TicketDetailRow`, etc.)
- The closest thing to a domain model is `Enums.cs` (5 enums with label extensions)
- No `Entity` base class, no `IAggregateRoot` marker, no value objects, no domain events

There is no `Ticket` aggregate, no `Incident` aggregate. Business rules like "a resolved ticket cannot be reopened" or "an incident must transition from Investigating to Ongoing to Resolved" are not enforced anywhere.

## Suggested Approach
1. Define a `Ticket` aggregate with: Id, Subject, Description, Category, Priority, Status (with valid state machine transitions), SubmitterEmail, CreatedAt, UpdatedAt, and domain events for state changes
2. Define an `Incident` aggregate with investigation lifecycle and state machine
3. Add named factory methods with validation and `private set` encapsulation
4. Add `IRepository<Ticket, TicketId>` and migrate `ITicketsRepository` to use the aggregate
5. Add domain events for ticket created, resolved, reopened, etc.

## Affected Files
- All files in `TSQR.Support.Domain/`
- `ITicketsRepository.cs`, `ISupportQueries.cs`
- All application handlers that work with raw primitives
