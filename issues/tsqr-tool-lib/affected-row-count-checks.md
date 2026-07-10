---
title: "[Tech] Affected row count checks from writes (Part of #32)"
type: Tech
repo: tsqr-tool-lib
parent: https://github.com/lstbob/tsqr-tool-lib/issues/32
issue: https://github.com/lstbob/tsqr-tool-lib/issues/38
sprint: 6
status: Backlog
priority: P2
size: M
estimate: 3
---

Check db.Execute() return value in SqlRepository.Update() and Delete(). Throw ConcurrencyException when zero rows affected. Apply across all bounded contexts.
