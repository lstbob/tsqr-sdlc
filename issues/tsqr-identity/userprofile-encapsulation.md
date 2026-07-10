---
title: "[Tech] UserProfile encapsulation and domain behavior (Part of #1)"
type: Tech
repo: tsqr-identity
parent: https://github.com/lstbob/tsqr-identity/issues/1
issue: https://github.com/lstbob/tsqr-identity/issues/3
sprint: 13
status: Backlog
priority: P1
size: L
estimate: 5
---

Add IAggregateRoot to UserProfile, make setters private set. Add factory method with validation. Add SetLockoutEnd(), UpdateProfile() with guard clauses. Add Entity base class. Update handlers.
