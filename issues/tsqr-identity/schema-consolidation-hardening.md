---
title: "[Tech] Schema consolidation and hardening"
type: Tech
repo: tsqr-identity
issue: https://github.com/lstbob/tsqr-identity/issues/2
created: 2026-07-10
---

## Problem

Three related schema-level issues.

### Identity schema duplication and type mismatch
tsqr-identity has two mutually exclusive database schemas:
- `init.sql` and `001_InitialSchema.sql` define `AspNetUsers`, `AspNetRoles` etc. — dead code, never queried by any repository
- `05-identity.sql` (from tsqr-deploy) defines `user_profiles`, `roles` — what code actually uses

Type mismatch: `user_profiles.Id` is `VARCHAR(128)` while `tsqr-autheo`'s `Users.Id` is `UUID`. Both hold the same GUID. Prevents FK references, direct JOINs, and database-level type safety.

### Schema design gaps
- SELECT * in every GetById mapping
- No CHECK constraints on INTEGER-encoded enum columns
- Minimal indexing (only `IX_user_roles_RoleId` and `IX_pending_email_changes_UserId`/`TokenHash`)

### Hard deletes without audit trail
All DELETEs are hard. No recovery possible.

## Suggested Approach
1. Remove dead `init.sql` and `001_InitialSchema.sql` files
2. Change `user_profiles.Id` from `VARCHAR(128)` to `UUID`
3. Add CHECK constraints, explicit column lists, and indexes on FK/lookup columns
4. Add `DeletedAt`/`DeletedBy` columns; replace DELETE with soft-delete UPDATE

## Affected Files
- `src/.../Api/docker/init.sql`
- `src/.../Infrastructure/Migrations/001_InitialSchema.sql`
- `../../tsqr-deploy/infra/05-identity.sql`
- All mapping files, all repository Update/Delete methods
