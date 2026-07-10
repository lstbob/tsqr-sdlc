---
title: "[Tech] Domain event wiring and ReservationQueueService (Part of #30)"
type: Tech
repo: tsqr-tool-lib
parent: https://github.com/lstbob/tsqr-tool-lib/issues/30
issue: https://github.com/lstbob/tsqr-tool-lib/issues/34
sprint: 2
status: Backlog
priority: P1
size: L
estimate: 5
---

Raise PickupReminderEvent, ReturnReminderEvent, ToolReservedEvent from aggregate methods. Implement 4 empty event handlers. Call ReservationQueueService.ShiftQueueAfterCancellation().
