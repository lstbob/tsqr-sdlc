---
title: "[Tech] Clean persistence abstractions and folder structure (Part of #32)"
type: Tech
repo: tsqr-tool-lib
parent: https://github.com/lstbob/tsqr-tool-lib/issues/32
issue: https://github.com/lstbob/tsqr-tool-lib/issues/36
sprint: 4
status: Backlog
priority: P1
size: L
estimate: 5
---

Define IDocumentRepository<T> for non-relational stores. Restructure Infrastructure/Dapper/ into Infrastructure/Persistence/Dapper/. Remove dynamic dispatch from SqlRepository.
