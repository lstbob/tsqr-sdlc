---
title: "[Story] Learning service: decks and cards"
type: Story
repo: tsqr-learning
issue: ""
created: 2026-11-28
---

## Problem

The Learning service cannot store decks or cards. A learner cannot create a deck or add a card to it.

## Suggested Approach
1. Add the `Deck` and `Card` aggregates. Each has a validating `Create(...)` that returns `Result<T>`, and a `Rehydrate(...)` for loading.
2. Add `GET /decks`, `GET /decks/{id}`, `POST /decks`, `GET /decks/{id}/cards` and `POST /cards`.
3. Filter every read and write by the `community_id` claim and the `sub` claim.
4. Keep the table definitions aligned with `tsqr-deploy/infra/30-learning.sql`, which is covered in `platform-wiring.md`.
5. Use explicit column lists and parameterised SQL.

## Affected Files
- `src/TSQR.Learning.Domain` (`Deck`, `Card`, value objects, domain events)
- `src/TSQR.Learning.Application` (deck and card commands and queries)
- `src/TSQR.Learning.Infrastructure` (Dapper mappings and repositories)
- `src/TSQR.Learning.WebApi` (endpoints)
- `tests/` (unit tests for the aggregates and handlers)

Estimate: 5 SP
