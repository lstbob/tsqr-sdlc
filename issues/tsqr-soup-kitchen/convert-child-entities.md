---
title: "[Tech] Convert Meal/Guest/Volunteer/Donation to child entities (Part of #1)"
type: Tech
repo: tsqr-soup-kitchen
parent: https://github.com/lstbob/tsqr-soup-kitchen/issues/1
issue: https://github.com/lstbob/tsqr-soup-kitchen/issues/5
sprint: 11
status: Backlog
priority: P1
size: M
estimate: 3
---

Move Meal/Guest/Volunteer/Donation under Event aggregate. Remove their individual IRepository interfaces. Access child entities through Event only. Update application handlers.
