---
title: "[Tech] Optimistic concurrency control (Part of #32)"
type: Tech
repo: tsqr-tool-lib
parent: https://github.com/lstbob/tsqr-tool-lib/issues/32
issue: https://github.com/lstbob/tsqr-tool-lib/issues/37
sprint: 5
status: Backlog
priority: P1
size: L
estimate: 5
---

Add xmin (PostgreSQL) or explicit RowVersion to all tables. Update UPDATE/DELETE statements with WHERE xmin = @ExpectedVersion. Propagate concurrency failures.
