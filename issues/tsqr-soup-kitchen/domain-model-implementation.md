---
title: "[Tech] Domain model implementation"
type: Tech
repo: tsqr-soup-kitchen
issue: https://github.com/lstbob/tsqr-soup-kitchen/issues/1
created: 2026-07-10
---

## Problem

The Soup Kitchen domain layer provides zero protection against invalid state.

### Public constructors with zero validation
Every aggregate uses public constructors with no guards:
```csharp
public Event(string name, string description, DateTime eventDate, string location,
    int? maxGuests, int communityId) : base(new EventId(0))
{
    Name = name;            // can be null/empty
    Description = description; // can be null/empty
    EventDate = eventDate;  // can be DateTime.MinValue or in the past
    Location = location;    // can be null/empty
    Status = EventStatus.Planned;
    MaxGuests = maxGuests;  // can be 0 or negative
}
```
Same pattern in `Guest`, `Meal`, `Volunteer`, `Donation`.

### Wrong aggregate root markers
`Meal`, `Guest`, `Volunteer`, `Donation` are independent aggregates referencing an `Event` by `EventId`. A Meal has no existence without an Event — they should be child entities of `Event`. Current design allows creating meals for non-existent events.

## Suggested Approach
1. Make constructors internal, add named factory methods with validation (e.g., `Event.Create(name, ...)` returning `Result<Event>`)
2. Add guard clauses for null/empty strings, past dates, negative values, zero max guests
3. Convert Meal/Guest/Volunteer/Donation to child entities within the `Event` aggregate; remove their individual repositories; access them through `Event`

## Affected Files
- `Event.cs`, `Guest.cs`, `Meal.cs`, `Volunteer.cs`, `Donation.cs` (constructors)
- Individual repository interfaces and implementations for Meal/Guest/Volunteer/Donation
