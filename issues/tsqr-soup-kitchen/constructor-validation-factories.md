---
title: "[Tech] Constructor validation and factory methods for aggregates (Part of #1)"
type: Tech
repo: tsqr-soup-kitchen
parent: https://github.com/lstbob/tsqr-soup-kitchen/issues/1
issue: https://github.com/lstbob/tsqr-soup-kitchen/issues/4
sprint: 10
status: Backlog
priority: P1
size: L
estimate: 5
---

Make Event/Guest/Meal/Volunteer/Donation constructors internal. Add static factory methods with guard clauses (null/empty strings, past dates, negative values). Add private set encapsulation.
