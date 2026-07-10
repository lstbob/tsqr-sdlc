---
title: "[Tech] Cross-aggregate transaction refactoring (Part of #30)"
type: Tech
repo: tsqr-tool-lib
parent: https://github.com/lstbob/tsqr-tool-lib/issues/30
issue: https://github.com/lstbob/tsqr-tool-lib/issues/33
sprint: 1
status: Backlog
priority: P1
size: L
estimate: 5
---

Refactor RegisterToolCommandHandler, LoanToolCommandHandler, and ReserveToolCommandHandler to act on a single aggregate per transaction. Remove duplicated ReservationDate/ReservationMemberId from InventoryItem.
