---
title: "[Infra] Wire tsqr-learning into gateway, autheo and deploy"
type: Infra
repo: tsqr-deploy
issue: ""
created: 2026-11-28
---

## Problem

The Learning service cannot be reached through the gateway. Autheo does not issue a token for its audience, and the stack has no database or container for it.

## Suggested Approach
1. In `tsqr-gateway`, add the route `/api/learning/{**catch-all}` to the cluster `learning`.
2. In `tsqr-autheo`, add the audience `tsqr-learning`.
3. In `tsqr-deploy`, add the Docker Compose service `learning` on local port 5100.
4. In `tsqr-deploy`, add the database `tsqr_learning` and the schema script `infra/30-learning.sql`. Make the script idempotent and additive.
5. Add the script to the upgrade list in `tsqr-deploy/README.md`.
6. Open one pull request per repo, with the same branch name in each repo, and link them.

## Affected Files
- `tsqr-gateway`: route and cluster configuration
- `tsqr-autheo`: audience configuration
- `tsqr-deploy/docker-compose` file (service `learning`)
- `tsqr-deploy/infra/30-learning.sql` (new)
- `tsqr-deploy/README.md` (upgrade list)

Estimate: 3 SP
