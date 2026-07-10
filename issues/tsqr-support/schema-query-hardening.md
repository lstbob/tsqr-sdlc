---
title: "[Tech] Schema and query hardening"
type: Tech
repo: tsqr-support
issue: https://github.com/lstbob/tsqr-support/issues/2
created: 2026-07-10
---

## Problem

Cross-cutting database and query safety improvements for tsqr-support.

### Schema design gaps
- SELECT * in mappings
- No CHECK constraints on INTEGER-encoded enum columns (Category, Status, State)
- No indexes on FK/lookup columns

### No pagination on list queries
Only `SupportQueries.ListTicketsAsync` has a `LIMIT 50` — but all other list queries are unbounded. Support tickets can grow without bound over time.

### No optimistic concurrency control
No row version column. Lost updates possible.

### Ignored affected row counts
db.Execute() return value ignored on all writes.

### Hard deletes without audit trail
No DeletedAt/DeletedBy columns.

## Suggested Approach
1. Replace SELECT * with explicit column lists; add CHECK constraints; add indexes
2. Add LIMIT/OFFSET to all list queries (parameterized with page/pageSize defaults)
3. Add row version checks (`xmin` or explicit `RowVersion` column)
4. Check db.Execute() return value; throw on zero rows
5. Add DeletedAt/DeletedBy columns; replace DELETE with soft-delete UPDATE

## Affected Files
- All mapping files
- All SQL init scripts
- All repository Update/Delete methods
- SupportQueries.cs list query methods
