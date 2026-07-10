---
title: "[Tech] Domain model cleanup"
type: Tech
repo: tsqr-tool-lib
issue: https://github.com/lstbob/tsqr-tool-lib/issues/31
created: 2026-07-10
---

## Problem

Three small but impactful issues in the domain layer.

### Debug method leaked into production
`Entity.cs:56-59` (the domain base class inherited by every aggregate) contains a misspelled test method:
```csharp
public Task<int> TestAsnc()
{
    return Task.FromResult(3);
}
```
Every entity in the system inherits this method — it pollutes the domain API and serves no purpose.

### Wrong aggregate root markers
`Manufacturer` is embedded within the `Tool` aggregate (referenced by `Tool.Manufacturer`) but has its own repository `IRepository<Manufacturer, ManufacturerId>`. It has no independent lifecycle outside of being referenced by a `Tool`. Should be a value object or child entity within the `Tool` aggregate.

### Contradictory state transitions
`Member.Reinstate()` in `Member.cs:213-219` allows `Banned → Active` directly:
```csharp
if (Status != MemberStatus.Suspended && Status != MemberStatus.Banned)
    return new DomainError(...);
Status = MemberStatus.Active;
```
Banned should be a terminal state — reinstating banned members contradicts the original domain analysis.

## Suggested Approach
1. Remove `TestAsnc()` from `Entity.cs`
2. Convert `Manufacturer` to a value object or child entity of `Tool`; remove its repository
3. Add `Banned` to the guard clause in `Member.Reinstate()` to reject reinstatement from banned status

## Affected Files
- `Entity.cs:56-59`
- `Manufacturer.cs`, `IRepository<Manufacturer, ManufacturerId>` registration
- `Member.cs:213-219`
