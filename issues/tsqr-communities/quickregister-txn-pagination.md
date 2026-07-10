---
title: "[Tech] QuickRegister transaction fix and pagination (Part of #1)"
type: Tech
repo: tsqr-communities
parent: https://github.com/lstbob/tsqr-communities/issues/1
issue: https://github.com/lstbob/tsqr-communities/issues/4
sprint: 7
status: Backlog
priority: P1
size: L
estimate: 5
---

Wrap QuickRegisterCommunityCommand's 4 SaveChangesAsync calls in a single transaction. Add LIMIT/OFFSET pagination to ToolRepository.GetAllAsync and all GeographyQueries list methods.
