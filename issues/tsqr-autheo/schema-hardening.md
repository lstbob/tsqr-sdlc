---
title: "[Tech] Schema hardening"
type: Tech
repo: tsqr-autheo
issue: https://github.com/lstbob/tsqr-autheo/issues/2
created: 2026-07-10
---

## Problem

Cross-cutting database safety improvements for tsqr-autheo.

### Schema design gaps
- SELECT * in GetById mappings (if applicable)
- No CHECK constraints on INTEGER-encoded enum columns
- No indexes beyond PK on frequently queried columns

### No optimistic concurrency control
No row version column. Lost updates possible.

### Ignored affected row counts
db.Execute() return value ignored.

### Hard deletes without audit trail
No DeletedAt/DeletedBy columns.

## Suggested Approach
1. Replace SELECT * with explicit column lists; add CHECK constraints; add indexes
2. Add row version checks (`xmin` or explicit `RowVersion` column)
3. Check db.Execute() return value; throw on zero rows
4. Add DeletedAt/DeletedBy columns; replace DELETE with soft-delete UPDATE

## Affected Files
- All mapping files
- All SQL init scripts
- All repository Update/Delete methods
