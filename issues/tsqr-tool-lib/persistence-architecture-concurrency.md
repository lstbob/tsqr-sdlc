---
title: "[Tech] Persistence architecture and concurrency safety"
type: Tech
repo: tsqr-tool-lib
issue: https://github.com/lstbob/tsqr-tool-lib/issues/32
created: 2026-07-10
---

## Problem

Four related issues in the persistence infrastructure.

### No pure abstraction for persistence
`IRepository<TAggregateRoot, TId>` is technology-agnostic, but `SqlRepository<TEntity, TId>` uses `dynamic` to extract `.Value` from ID value objects (assumes int), and `ISqlEntityMapping<TEntity>` assumes SQL. Switching to a document store would require rewriting the entire persistence stack.

### No INoSqlRepository contract
There is no `IDocumentRepository<T>` or `INoSqlRepository<TAggregateRoot>` for non-relational stores. Every new repository must conform to the same SQL-tainted interface.

### No folder structure for persistence backends
All persistence code lives under `Infrastructure/Dapper/`. Adding MongoDB would have no established pattern.

### Ignored affected row counts
`SqlRepository.Update()` and `Delete()` ignore the return value of `db.Execute()`. If an UPDATE or DELETE affects zero rows, the application has no way to detect it. `DapperUnitOfWork.SaveChangesAsync()` will still succeed.

## Suggested Approach
1. Define a clean `IDocumentRepository<T>` or `IDbRepository<T, TId>` family of interfaces in the domain layer
2. Add `Infrastructure/Persistence/Dapper/` and `Infrastructure/Persistence/DocumentDb/` folder convention
3. Make `Update`/`Delete` return or check affected rows; throw `ConcurrencyException` when zero rows affected
4. Add optimistic concurrency control (PostgreSQL `xmin` or explicit `RowVersion`)

## Affected Files
- `SqlRepository.cs`, `ISqlEntityMapping.cs`, `IRepository.cs`
- `Infrastructure/Dapper/` folder structure
- All repository implementations that call `db.Execute()`
