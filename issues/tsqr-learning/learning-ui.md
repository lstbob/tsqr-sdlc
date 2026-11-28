---
title: "[Story] Learning pages in tsqr-ui"
type: Story
repo: tsqr-ui
issue: ""
created: 2026-11-28
---

## Problem

The user interface (UI) has no pages for decks, cards, practice or statistics. Learners cannot use the Learning service in the app.

## Suggested Approach
1. Add pages under `/learning`: a deck list, a deck detail page with its cards, and a form to create a card.
2. Add a practice page. It shows the card cue, takes a typed answer, reveals the answer and records the review with a confidence rating.
3. Add a statistics page that shows the figures from `GET /stats`.
4. Call the endpoints through the gateway prefix `/api/learning`.
5. Run `npm run build` and `npm run lint` before the pull request.

## Affected Files
- `app/learning/` (pages)
- `components/` (practice and card components)
- `lib/` (API client for `/api/learning`)

Estimate: 5 SP
