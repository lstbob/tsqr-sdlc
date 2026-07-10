---
title: "[Tech] Query layer: inject ISqlUnitOfWork instead of connectionString (Part of #1)"
type: Tech
repo: tsqr-communities
parent: https://github.com/lstbob/tsqr-communities/issues/1
issue: https://github.com/lstbob/tsqr-communities/issues/5
sprint: 8
status: Backlog
priority: P1
size: M
estimate: 3
---

Replace string connectionString dependency with ISqlUnitOfWork in GeographyQueries and DashboardQueries. Remove independent NpgsqlConnection creation. Update DI registration.
