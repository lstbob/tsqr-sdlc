---
title: "[Story] Learning: Leitner review and interleaved practice queue"
type: Story
repo: tsqr-learning
issue: ""
created: 2026-11-28
---

## Problem

Learners cannot review a card. The service has no Leitner rules, no review record and no practice queue.

## Suggested Approach
1. Add the `LeitnerBox` value object for boxes 1 to 5. The next review is due 1, 2, 4, 8 or 16 days later.
2. Add `POST /cards/{id}/reviews`. Require a non-empty typed answer. Return a `DomainError` when the card is not due.
3. A correct answer moves the card up one box, to a maximum of 5. A wrong answer moves it to box 1 and adds one lapse.
4. Insert one Review row for each review. Store the confidence (Low, Medium or High), the result and the box before and after.
5. Add `POST /cards/{id}/reveal`. Return the expected answer only after a typed attempt.
6. Add `GET /practice/queue`. Return the due cards from all decks, mixed. Never return the expected answer.

## Affected Files
- `src/TSQR.Learning.Domain` (`LeitnerBox`, `Confidence`, `Card` review method, `Review`, `CardReviewedDomainEvent`)
- `src/TSQR.Learning.Application` (review, reveal and practice queue handlers)
- `src/TSQR.Learning.Infrastructure` (review insert and due-card query)
- `src/TSQR.Learning.WebApi` (endpoints)
- `tests/` (Leitner rule tests and queue tests)

Estimate: 5 SP
