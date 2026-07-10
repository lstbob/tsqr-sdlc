---
title: "[Tech] Schema hardening"
type: Tech
repo: tsqr-communities
issue: https://github.com/lstbob/tsqr-communities/issues/3
created: 2026-07-10
---

## Problem

Cross-cutting database safety improvements for tsqr-communities.

### Schema design gaps
- `SELECT *` in every GetById mapping — fragile when columns change, wasteful fetching unused columns
- No `CHECK` constraints on INTEGER-encoded enum columns (Status, Type, Category stored as plain INTEGER — value `99` accepted silently)
- No indexes on critical query paths (only implicit PK index on `Id`)

### No optimistic concurrency control
No row version column (`xmin` or explicit `RowVersion`). No UPDATE/DELETE uses `WHERE` to verify row hasn't changed since read. Lost updates possible.

### Ignored affected row counts
`db.Execute()` return value ignored — zero-row updates silently succeed.

### Hard deletes without audit trail
All DELETEs are hard. No `DeletedAt`/`DeletedBy` columns. No recovery or audit trail possible. Deleting a member breaks FK references from their past loans, inventory, and maintenance records.

## Suggested Approach
1. Replace SELECT * with explicit column lists; add CHECK constraints; add indexes on FK columns and frequently queried columns
2. Add row version checks (`xmin` or explicit `RowVersion` column)
3. Check `db.Execute()` return value; throw on zero rows
4. Add `DeletedAt TIMESTAMP NULL` and `DeletedBy VARCHAR(200)` columns; replace DELETE with soft-delete UPDATE

## Affected Files
- All mapping files (e.g., `CommunityMapping.cs`, `CountryMapping.cs`)
- All SQL init scripts
- All repository `Update`/`Delete` methods
