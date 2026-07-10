# tsqr-sdlc

SDLC artifacts for the **TSQR (TownsSquare)** platform — backlog, sprints, issue definitions, ADRs, and process documentation across all microservices.

- **[Project Board](https://github.com/users/lstbob/projects/4)**
- **[19 Sprint Backlog](https://github.com/users/lstbob/projects/4/views/1)**

---

## Repository Structure

```
tsqr-sdlc/
├── README.md
├── issues/                    # Canonical issue definitions by repo
│   ├── tsqr-tool-lib/
│   ├── tsqr-communities/
│   ├── tsqr-soup-kitchen/
│   ├── tsqr-identity/
│   ├── tsqr-autheo/
│   └── tsqr-support/
├── sprints/                   # Sprint plans (this file)
├── rfcs/                      # (future)
├── adrs/                      # (future)
└── templates/                 # (future)
```

---

## Sprint Plan (19 Sprints × 5 SP max per 2-week sprint)

**Capacity:** 1 developer, max 5 story points per sprint.

### Sprint 1 (Jul 10–23)
| Item | SP | Repo |
|------|----|------|
| Cross-aggregate transaction refactoring | 5 | tool-lib [#33](https://github.com/lstbob/tsqr-tool-lib/issues/33) |

### Sprint 2 (Jul 24–Aug 6)
| Item | SP | Repo |
|------|----|------|
| Domain event wiring + ReservationQueueService | 5 | tool-lib [#34](https://github.com/lstbob/tsqr-tool-lib/issues/34) |

### Sprint 3 (Aug 7–20)
| Item | SP | Repo |
|------|----|------|
| Policy aggregate + FineService integration | 3 | tool-lib [#35](https://github.com/lstbob/tsqr-tool-lib/issues/35) |
| Domain model cleanup | 2 | tool-lib [#31](https://github.com/lstbob/tsqr-tool-lib/issues/31) |

### Sprint 4 (Aug 21–Sep 3)
| Item | SP | Repo |
|------|----|------|
| Clean persistence abstractions + folder structure | 5 | tool-lib [#36](https://github.com/lstbob/tsqr-tool-lib/issues/36) |

### Sprint 5 (Sep 4–17)
| Item | SP | Repo |
|------|----|------|
| Optimistic concurrency control | 5 | tool-lib [#37](https://github.com/lstbob/tsqr-tool-lib/issues/37) |

### Sprint 6 (Sep 18–Oct 1)
| Item | SP | Repo |
|------|----|------|
| Affected row count checks | 3 | tool-lib [#38](https://github.com/lstbob/tsqr-tool-lib/issues/38) |
| Domain model improvements (slug + agg roots) | 2 | communities [#2](https://github.com/lstbob/tsqr-communities/issues/2) |

### Sprint 7 (Oct 2–15)
| Item | SP | Repo |
|------|----|------|
| QuickRegister txn fix + pagination | 5 | communities [#4](https://github.com/lstbob/tsqr-communities/issues/4) |

### Sprint 8 (Oct 16–29)
| Item | SP | Repo |
|------|----|------|
| UoW injection into GeographyQueries/DashboardQueries | 3 | communities [#5](https://github.com/lstbob/tsqr-communities/issues/5) |
| Schema hardening | 2 | soup-kitchen [#3](https://github.com/lstbob/tsqr-soup-kitchen/issues/3) |

### Sprint 9 (Oct 30–Nov 12)
| Item | SP | Repo |
|------|----|------|
| Schema hardening (indexes, CHECK, SELECT *) | 5 | communities [#3](https://github.com/lstbob/tsqr-communities/issues/3) |

### Sprint 10 (Nov 13–26)
| Item | SP | Repo |
|------|----|------|
| Constructor validation + factory methods | 5 | soup-kitchen [#4](https://github.com/lstbob/tsqr-soup-kitchen/issues/4) |

### Sprint 11 (Nov 27–Dec 10)
| Item | SP | Repo |
|------|----|------|
| Convert Meal/Guest/Volunteer/Donation to child entities | 3 | soup-kitchen [#5](https://github.com/lstbob/tsqr-soup-kitchen/issues/5) |
| Schema hardening | 2 | autheo [#2](https://github.com/lstbob/tsqr-autheo/issues/2) |

### Sprint 12 (Dec 11–24)
| Item | SP | Repo |
|------|----|------|
| Query layer refactor (dynamic WHERE, pagination, UoW) | 5 | soup-kitchen [#2](https://github.com/lstbob/tsqr-soup-kitchen/issues/2) |

### Sprint 13 (Dec 25–Jan 7)
| Item | SP | Repo |
|------|----|------|
| UserProfile encapsulation + behavior | 5 | identity [#3](https://github.com/lstbob/tsqr-identity/issues/3) |

### Sprint 14 (Jan 8–21)
| Item | SP | Repo |
|------|----|------|
| Role domain model + handler updates | 3 | identity [#4](https://github.com/lstbob/tsqr-identity/issues/4) |

### Sprint 15 (Jan 22–Feb 4)
| Item | SP | Repo |
|------|----|------|
| Schema consolidation (dead AspNetUsers, VARCHAR→UUID) | 5 | identity [#2](https://github.com/lstbob/tsqr-identity/issues/2) |

### Sprint 16 (Feb 5–18)
| Item | SP | Repo |
|------|----|------|
| Error handling (Result<T>) + async fix | 5 | autheo [#1](https://github.com/lstbob/tsqr-autheo/issues/1) |

### Sprint 17 (Feb 19–Mar 4)
| Item | SP | Repo |
|------|----|------|
| Ticket aggregate + state machine | 5 | support [#3](https://github.com/lstbob/tsqr-support/issues/3) |

### Sprint 18 (Mar 5–18)
| Item | SP | Repo |
|------|----|------|
| Incident aggregate + event wiring | 3 | support [#4](https://github.com/lstbob/tsqr-support/issues/4) |

### Sprint 19 (Mar 19–Apr 1)
| Item | SP | Repo |
|------|----|------|
| Schema + query hardening | 5 | support [#2](https://github.com/lstbob/tsqr-support/issues/2) |

**Total: 95 SP across 19 sprints**

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

All 30 board items have been set with:

| Field | Values Used |
|-------|-------------|
| **Sprint** (bob-sprint) | Sprint 1–19 (iteration field) |
| **Priority** | P1 (high), P2 (medium) |
| **Size** | XS, S, M, L, XL |
| **Estimate(SP)** | 1, 2, 3, 5, 8, 13 (Fibonacci) |
| **Status** | Backlog / Done |
| **Sub-issues progress** | Auto-computed by GitHub |
