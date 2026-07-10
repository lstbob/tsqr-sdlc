---
title: "[Tech] Domain model improvements"
type: Tech
repo: tsqr-communities
issue: https://github.com/lstbob/tsqr-communities/issues/2
created: 2026-07-10
---

## Problem

Two domain-level issues.

### Naive slug generation
`Community.cs:41-42` generates slugs with:
```csharp
name.ToLowerInvariant().Replace(' ', '-').Replace("--", "-");
```
Fails on: special characters, consecutive hyphens beyond two, leading/trailing hyphens, non-ASCII characters, and no uniqueness enforcement — two communities can have the same slug, breaking URL routing.

### Wrong aggregate root markers
`Country`, `City`, `Neighbourhood` are tagged as `IAggregateRoot` but are reference/lookup data — created once, rarely mutated. Making each an independent aggregate root forces `QuickRegisterCommunityCommand` to commit after each creation. Should be value objects or a single `Location` aggregate.

## Suggested Approach
1. Replace slug generation with a robust utility (e.g., `System.Text.RegularExpressions` to strip non-alphanumeric chars, collapse hyphens, trim edges; add DB unique constraint)
2. Convert `Country`/`City`/`Neighbourhood` to value objects or child entities under a `Location` aggregate; remove their individual repositories

## Affected Files
- `Community.cs:41-42`
- `Country.cs`, `City.cs`, `Neighbourhood.cs` and their `IRepository` interfaces
