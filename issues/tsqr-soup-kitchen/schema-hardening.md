---
title: "[Tech] Schema hardening"
type: Tech
repo: tsqr-soup-kitchen
issue: https://github.com/lstbob/tsqr-soup-kitchen/issues/3
created: 2026-07-10
---

## Problem

Cross-cutting database safety improvements for tsqr-soup-kitchen.

### Schema design gaps
- SELECT * in every GetById mapping
- No CHECK constraints on INTEGER-encoded enum columns (Status, Category stored as plain INTEGER)
- No indexes on FK columns (EventId in Guests/Meals/Volunteers/Donations)

### No optimistic concurrency control
No row version column. Lost updates possible — two concurrent writes can silently overwrite each other.

### Ignored affected row counts
db.Execute() return value ignored on all writes.

### Hard deletes without audit trail
No DeletedAt/DeletedBy columns. Deleting an Event cascades FK issues to dependent rows.

## Suggested Approach
1. Replace SELECT * with explicit column lists; add CHECK constraints; add FK indexes
2. Add row version checks (`xmin` or explicit `RowVersion` column)
3. Check db.Execute() return value; throw on zero rows
4. Add DeletedAt/DeletedBy columns; replace DELETE with soft-delete UPDATE

## Affected Files
- All mapping files (EventMapping.cs, GuestMapping.cs, MealMapping.cs, VolunteerMapping.cs, DonationMapping.cs)
- All SQL init scripts
- All repository Update/Delete methods
