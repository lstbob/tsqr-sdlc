---
title: "[Story] Learning: calibration stats"
type: Story
repo: tsqr-learning
issue: ""
created: 2026-11-28
---

## Problem

Learners cannot see how their confidence matches their results. The service has no statistics endpoint.

## Suggested Approach
1. Add `GET /stats`. Return the number of decks, the number of cards, the cards due now, the number of reviews and the accuracy (the share of right answers) for each confidence level.
2. Read the figures with one SQL query. Use explicit column lists and parameters.
3. Filter the query by the `community_id` claim and the `sub` claim.
4. Return a DTO. Do not load aggregates for this read.

## Affected Files
- `src/TSQR.Learning.Application` (stats query and DTO)
- `src/TSQR.Learning.Infrastructure` (SQL query)
- `src/TSQR.Learning.WebApi` (endpoint)
- `tests/` (query tests)

Estimate: 2 SP
