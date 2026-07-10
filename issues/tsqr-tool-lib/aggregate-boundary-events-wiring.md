---
title: "[Tech] Aggregate boundary, events, and domain service wiring"
type: Tech
repo: tsqr-tool-lib
issue: https://github.com/lstbob/tsqr-tool-lib/issues/30
created: 2026-07-10
---

## Problem

Several command handlers in Tool Library violate aggregate boundary rules and domain wiring is incomplete.

### Cross-aggregate transactions (3 handlers)
- **RegisterToolCommandHandler** — creates both `Tool` and `InventoryItem` in one transaction
- **LoanToolCommandHandler** — mutates `Loan` + `InventoryItem` in one transaction
- **ReserveToolCommandHandler** — mutates `Reservation` + `InventoryItem` in one transaction

Proper DDD: one transaction per aggregate. Side effects should happen through domain event handlers. Additionally, `InventoryItem.cs:46-47` has `ReservationDate`/`ReservationMemberId` — duplicated reservation state that creates a dual-write risk.

### Domain events defined but never raised
- `PickupReminderEvent`, `ReturnReminderEvent`, `ToolReservedEvent` — defined as record types, never called
- 4 handlers are empty stubs: `ToolMarkedForRepairNotificationHandler`, `NextInLineNotificationHandler`, `PickupReminderHandler`, `ReturnReminderHandler`

### ReservationQueueService unwired
`ReservationQueueService.ShiftQueueAfterCancellation()` exists in domain but never called. When a reservation is cancelled, `QueuePosition` values are not renumbered.

### Policy aggregate and FineService ignored
- `Loan.EndLoan()` hardcodes `$1/day` instead of calling `FineService` or reading `Policy.LateFeePerDay`
- `Policy.MaxLoanDurationDays` not checked by `LoanToolCommandHandler`
- `Policy.MaxRenewalCount` unused — no `Loan.Renew()` method exists
- `Policy.MaxLoanReservationDays` not checked by `ReserveToolCommandHandler`

## Suggested Approach
1. Refactor RegisterTool/LoanTool/ReserveTool handlers to act on one aggregate, emit domain events for side effects
2. Wire domain event raises in the aggregate behavioral methods
3. Implement the 4 empty event handlers
4. Call `ReservationQueueService.ShiftQueueAfterCancellation()` from `ReservationCancelledEventHandler`
5. Load and enforce `Policy` in the relevant command handlers; use `FineService` instead of hardcoded `$1/day`

## Affected Files
- `Loan.cs:121-125`, `RegisterToolCommandHandler.cs`, `LoanToolCommandHandler.cs`, `ReserveToolCommandHandler.cs`
- `ReservationQueueService.cs`, multiple event handler stubs, `Policy.cs`, `FineService.cs`
