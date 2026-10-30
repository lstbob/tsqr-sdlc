# tsqr-sdlc

SDLC artifacts for the **TSQR (TownsSquare)** platform — backlog, sprints, issue definitions, ADRs, and process documentation across all microservices.

- **[Project Board](https://github.com/users/lstbob/projects/4)**
- **[Sprint Backlog](https://github.com/users/lstbob/projects/4/views/1)**

---

## Repository Structure

```
tsqr-sdlc/
├── README.md
├── PROCESS.md
├── issues/                    # Canonical issue definitions by repo
│   ├── tsqr-tool-lib/
│   ├── tsqr-communities/
│   ├── tsqr-soup-kitchen/
│   ├── tsqr-identity/
│   ├── tsqr-autheo/
│   └── tsqr-support/
├── scripts/                   # Sprint scheduler CLI and alert script
├── sprints/                   # Snapshots and iteration backups
├── rfcs/                      # (future)
├── adrs/                      # (future)
└── templates/                 # (future)
```

---

## Sprint Backlog (rolling 10-sprint horizon × 5 SP max per 2-week sprint)

**Capacity:** 1 developer, max 5 story points per sprint.

> **Note:** Items listed here are the actionable sub-issues and standalone issues assigned to each sprint. Parent grouping issues (e.g., #30, #32) are not assigned to sprints — they remain on the board only for Sub-issues Progress tracking.

The board was re-anchored on **2026-10-29**. Sprint 9 (Oct 30–Nov 12) is skipped because it starts before 2 November. The first active sprint is **Sprint 10 (Nov 13–26)**.

### Sprint 10 (Nov 13–26)
| Item | SP | Repo |
|------|----|------|
| Email-change feature end-to-end | 5 | identity [#5](https://github.com/lstbob/tsqr-identity/issues/5) |

### Sprint 11 (Nov 27–Dec 10)
| Item | SP | Repo |
|------|----|------|
| `/register` self-Admin exploit + password reset | 5 | autheo [#3](https://github.com/lstbob/tsqr-autheo/issues/3) |

### Sprint 12 (Dec 11–24)
| Item | SP | Repo |
|------|----|------|
| Refresh token concurrency + revoke guard | 5 | autheo [#4](https://github.com/lstbob/tsqr-autheo/issues/4) |

### Sprint 13 (Dec 25–Jan 7)
| Item | SP | Repo |
|------|----|------|
| Authorization: write controllers + query scoping | 3 | communities [#6](https://github.com/lstbob/tsqr-communities/issues/6) |
| Reconcile `infra/02-tool-library.sql` | 2 | deploy [#2](https://github.com/lstbob/tsqr-deploy/issues/2) |

### Sprint 14 (Jan 8–21)
| Item | SP | Repo |
|------|----|------|
| Ticket submission auth + multi-tenancy | 5 | support [#5](https://github.com/lstbob/tsqr-support/issues/5) |

### Sprint 15 (Jan 22–Feb 4)
| Item | SP | Repo |
|------|----|------|
| ReservationQueueService direction bug | 5 | tool-lib [#43](https://github.com/lstbob/tsqr-tool-lib/issues/43) |

### Sprint 16 (Feb 5–18)
| Item | SP | Repo |
|------|----|------|
| Test infrastructure across microservices | 5 | tool-lib [#40](https://github.com/lstbob/tsqr-tool-lib/issues/40) |

### Sprint 17 (Feb 19–Mar 4)
| Item | SP | Repo |
|------|----|------|
| Clean persistence abstractions + folder structure | 5 | tool-lib [#36](https://github.com/lstbob/tsqr-tool-lib/issues/36) |

### Sprint 18 (Mar 5–18)
| Item | SP | Repo |
|------|----|------|
| Optimistic concurrency control | 5 | tool-lib [#37](https://github.com/lstbob/tsqr-tool-lib/issues/37) |

### Sprint 19 (Mar 19–Apr 1)
| Item | SP | Repo |
|------|----|------|
| QuickRegister txn fix + pagination | 5 | communities [#4](https://github.com/lstbob/tsqr-communities/issues/4) |

**Scheduled: 50 SP across 10 sprints.** Sprint 20 is kept empty as headroom; `defer` uses it and adds more iterations when needed. Everything else is in the Backlog (no iteration assignment).

### Backlog (unscheduled)

The remaining **210 SP** is intentionally unscheduled. It is pulled into the horizon as sprints complete, using `scripts/sprint` (see below).

**Oversized items (>5 SP) — must be split before scheduling:**

| Item | SP | Repo |
|------|----|------|
| Shared kernel: DDD base classes | 13 | common [#2](https://github.com/lstbob/tsqr-common/issues/2) |
| Multi-tenancy enforcement | 8 | soup-kitchen [#6](https://github.com/lstbob/tsqr-soup-kitchen/issues/6) |
| State-transition guards + UNIQUE constraints | 8 | communities [#7](https://github.com/lstbob/tsqr-communities/issues/7) |
| Cross-aggregate invariants | 8 | soup-kitchen [#7](https://github.com/lstbob/tsqr-soup-kitchen/issues/7) |
| State-machine guards | 8 | soup-kitchen [#8](https://github.com/lstbob/tsqr-soup-kitchen/issues/8) |
| Entity base + IAggregateRoot | 8 | identity [#6](https://github.com/lstbob/tsqr-identity/issues/6) |
| Rate limiting + RS256 JWT | 8 | autheo [#5](https://github.com/lstbob/tsqr-autheo/issues/5) |
| Ticket state machine + Incident aggregate | 8 | support [#6](https://github.com/lstbob/tsqr-support/issues/6) |
| DB migration runner (DbUp/FluentMigrator) | 8 | deploy [#3](https://github.com/lstbob/tsqr-deploy/issues/3) |

Per `PROCESS.md`, any issue >5 SP must be split into sub-issues where each part is ≤5 SP.

---

## Rescheduling

The `scripts/sprint` CLI enforces the 5 SP capacity and cascades changes. It is a dry-run by default; add `--apply` to write.

```bash
./scripts/sprint status                 # per-sprint load and capacity
./scripts/sprint audit                  # epics, oversized items, missing estimates
./scripts/sprint defer tsqr-tool-lib#43 # preview moving to the next sprint
./scripts/sprint defer tsqr-tool-lib#43 --apply
./scripts/sprint add tsqr-communities#5 --to 9   # add an unscheduled item
./scripts/sprint add tsqr-communities#5 --to 9 --apply
./scripts/sprint move tsqr-tool-lib#43 --to 16 --apply
./scripts/sprint rebalance --from 10 --apply
./scripts/sprint extend --count 1 --apply
```

**`defer` behaviour:** moves the item to the next sprint, shifts every item in later sprints forward one iteration, and refuses to place an item larger than the capacity. If the last sprint overflows, it adds a new iteration first (with a config backup).

**`add` behaviour:** puts an unscheduled backlog item into a sprint, refusing if the item or the destination exceeds capacity.

**Authentication:** the CLI uses `gh` and needs the `project` scope. In GitHub Actions, set `GH_TOKEN` to a PAT with `project` + `repo` scopes.

---

## Sprint-end alerts

`.github/workflows/sprint-alert.yml` runs daily at 07:00 UTC. When an iteration ends within 2 days and still has open items, it creates an issue in this repo assigned to `@lstbob` with a checklist. GitHub sends the assignment email — no custom mail server.

If an alert issue for that sprint is already open, the workflow updates it instead of creating a duplicate.

**Setup (one-time):**

1. Create a classic PAT with `project` and `repo` scopes.
2. Store it as a repository secret:

   ```bash
   gh secret set PROJECT_TOKEN -R lstbob/tsqr-sdlc
   ```

3. (Optional) adjust `SPRINT_ALERT_DAYS` in the workflow.

---

## Parent Issues & Sub-issues

| Parent | Parts | Total SP |
|--------|-------|----------|
| [#30](https://github.com/lstbob/tsqr-tool-lib/issues/30) Aggregate boundary & events | [#33](https://github.com/lstbob/tsqr-tool-lib/issues/33) Cross-aggregate txns (5), [#34](https://github.com/lstbob/tsqr-tool-lib/issues/34) Event wiring (5), [#35](https://github.com/lstbob/tsqr-tool-lib/issues/35) Policy/FineService (3) | 13 |
| [#32](https://github.com/lstbob/tsqr-tool-lib/issues/32) Persistence architecture | [#36](https://github.com/lstbob/tsqr-tool-lib/issues/36) Clean abstractions (5), [#37](https://github.com/lstbob/tsqr-tool-lib/issues/37) Concurrency (5), [#38](https://github.com/lstbob/tsqr-tool-lib/issues/38) Row counts (3) | 13 |
| [#1](https://github.com/lstbob/tsqr-communities/issues/1) Transaction & query refactor | [#4](https://github.com/lstbob/tsqr-communities/issues/4) QuickRegister txn + pagination (5), [#5](https://github.com/lstbob/tsqr-communities/issues/5) UoW injection (3) | 8 |
| [#1](https://github.com/lstbob/tsqr-soup-kitchen/issues/1) Domain model impl. | [#4](https://github.com/lstbob/tsqr-soup-kitchen/issues/4) Constructor validation (5), [#5](https://github.com/lstbob/tsqr-soup-kitchen/issues/5) Child entities (3) | 8 |
| [#1](https://github.com/lstbob/tsqr-identity/issues/1) Domain model creation | [#3](https://github.com/lstbob/tsqr-identity/issues/3) UserProfile (5), [#4](https://github.com/lstbob/tsqr-identity/issues/4) Role model (3) | 8 |
| [#1](https://github.com/lstbob/tsqr-support/issues/1) Domain model creation | [#3](https://github.com/lstbob/tsqr-support/issues/3) Ticket aggregate (5), [#4](https://github.com/lstbob/tsqr-support/issues/4) Incident aggregate (3) | 8 |

---

## Field Values

All 61 board items use:

| Field | Values Used |
|-------|-------------|
| **Sprint** (bob-sprint) | Sprint 10–19 for scheduled work; empty for the Backlog |
| **Priority** | P0 (critical), P1 (high), P2 (medium) |
| **Size** | XS, S, M, L, XL |
| **Estimate(SP)** | 1, 2, 3, 5, 8, 13 (Fibonacci) |
| **Status** | Backlog / In progress / In review / Ready For QA / In QA / Done |
| **Sub-issues progress** | Auto-computed by GitHub |
