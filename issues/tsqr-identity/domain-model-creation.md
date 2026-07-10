---
title: "[Tech] Domain model creation"
type: Tech
repo: tsqr-identity
issue: https://github.com/lstbob/tsqr-identity/issues/1
created: 2026-07-10
---

## Problem

The Identity domain layer is effectively a DTO namespace with zero encapsulation.

### Completely anemic domain
`UserProfile` is a plain data class with public get/set properties:
```csharp
public sealed class UserProfile
{
    public string Id { get; set; } = string.Empty;   // anyone can change the ID
    public string? FirstName { get; set; }            // can be set to anything
    public string? LastName { get; set; }
    public string? AvatarUrl { get; set; }
    public string? Bio { get; set; }
    public DateTime CreatedAt { get; set; }           // mutable — can be rewritten
    public DateTime UpdatedAt { get; set; }
    public DateTime? LockoutEnd { get; set; }
}
```
No encapsulation, no domain behavior, no invariants. `Role` has the same pattern.

The domain layer (`TSQR.Identity.Domain`) contains:
- No `IAggregateRoot` marker on any entity
- No `Entity` base class
- No domain events
- No value objects
- No `Result<T>` validation

It is functionally a DTO namespace.

## Suggested Approach
1. Add `IAggregateRoot` to `UserProfile`, make all property setters `private set`
2. Add named factory methods with validation (e.g., `UserProfile.Create(firstName, lastName)` returning `Result<UserProfile>`)
3. Add domain behavior methods (`SetLockoutEnd()`, `UpdateProfile()`) with guard clauses
4. Add `Entity` base class, domain events collection, value objects where appropriate
5. Update application handlers to call domain methods instead of setting properties directly

## Affected Files
- `UserProfile.cs`, `Role.cs` in `TSQR.Identity.Domain`
- All application handlers that set UserProfile properties directly
- `ProfileRepository.cs`, `UserAdminRepository.cs`
