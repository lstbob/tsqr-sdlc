---
title: "[Tech] Transaction boundary and query layer refactor"
type: Tech
repo: tsqr-communities
issue: https://github.com/lstbob/tsqr-communities/issues/1
created: 2026-07-10
---

## Problem

Three related issues in transaction and connection discipline.

### QuickRegister broken transaction boundary
`QuickRegisterCommunityCommand.cs` calls `SaveChangesAsync()` after each entity creation:
```csharp
await countryRepo.UnitOfWork.SaveChangesAsync(ct);
await cityRepo.UnitOfWork.SaveChangesAsync(ct);
await neighbourhoodRepo.UnitOfWork.SaveChangesAsync(ct);
await communityRepo.UnitOfWork.SaveChangesAsync(ct);
```
The first call commits the transaction. If community creation fails after country/city are saved, those records are orphaned.

### GeographyQueries and DashboardQueries bypass UoW
`GeographyQueries(connectionString)` creates independent `NpgsqlConnection` per call instead of using the scoped `ISqlUnitOfWork` from DI. These bypass the ambient transaction, breaking read-your-writes consistency.

### No pagination on any list query
`ToolRepository.GetAllAsync()`, `GeographyQueries`, and all list queries return unbounded result sets. Tool Library's `GetAllAsync` has an N+1 pattern via JOIN + per-row scarcity loading.

## Suggested Approach
1. Wrap QuickRegister in a single transaction with one commit at the end
2. Inject `ISqlUnitOfWork` into GeographyQueries and DashboardQueries instead of `connectionString`
3. Add `LIMIT/OFFSET` pagination to all list queries, starting with ToolRepository.GetAllAsync

## Affected Files
- `QuickRegisterCommunityCommand.cs`
- `GeographyQueries.cs`, `DashboardQueries.cs`
- `ToolRepository.cs:7`, `GeographyQueries.cs` list methods
