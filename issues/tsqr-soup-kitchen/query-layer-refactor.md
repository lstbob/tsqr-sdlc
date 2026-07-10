---
title: "[Tech] Query layer refactor"
type: Tech
repo: tsqr-soup-kitchen
issue: https://github.com/lstbob/tsqr-soup-kitchen/issues/2
created: 2026-07-10
---

## Problem

The Soup Kitchen WebApi query handlers have security and performance issues.

### String concatenation for dynamic WHERE clauses
Present in `GetMealsQuery.cs`, `GetVolunteersQuery.cs`, `GetEventsQuery.cs`, `GetGuestsQuery.cs`, `GetDonationsQuery.cs`:
```csharp
var conditions = new List<string>();
if (request.EventId.HasValue) conditions.Add("m.EventId = @EventId");
var where = conditions.Count > 0 ? "WHERE " + string.Join(" AND ", conditions) : "";
var sql = $"SELECT ... FROM Meals m {where} ORDER BY ...";
```
While values are parameterized, the WHERE string itself is concatenated. A missing space or future contributor adding user input to the string part creates a SQL injection vector. Fragile: a missing space before WHERE or between conditions produces invalid SQL.

### No pagination
All list queries return unbounded result sets. No `LIMIT/OFFSET` on any query except `SupportQueries.ListTicketsAsync`.

### Queries bypass scoped UoW
All 6 WebApi query handlers create independent `NpgsqlConnection` per call instead of using the scoped `ISqlUnitOfWork` from DI. Each connection involves TCP handshake + SSL + auth. Dashboard pages calling multiple queries waste 5+ TCP connections per request.

## Suggested Approach
1. Extract filter building into a shared helper returning a tuple `(where, parameters)` used for both COUNT and data queries; use `DynamicParameters`
2. Add `LIMIT @PageSize OFFSET @Offset` to all list queries
3. Inject `ISqlUnitOfWork` into all query handlers instead of `connectionString`

## Affected Files
- `GetMealsQuery.cs`, `GetVolunteersQuery.cs`, `GetEventsQuery.cs`, `GetGuestsQuery.cs`, `GetDonationsQuery.cs`
- `DashboardQueries.cs`, `Program.cs` (DI registration)
