# tsqr-sdlc

SDLC artifacts for the **TSQR (TownsSquare)** platform.

This repository serves as the canonical source of truth for issue definitions, ADRs, RFCs, and process documentation across all TSQR microservices.

## Repository Structure

```
tsqr-sdlc/
├── README.md
├── issues/                       # Canonical issue definitions
│   ├── tsqr-tool-lib/
│   ├── tsqr-communities/
│   ├── tsqr-soup-kitchen/
│   ├── tsqr-identity/
│   ├── tsqr-autheo/
│   └── tsqr-support/
├── rfcs/                         # (future) RFCs for major changes
├── adrs/                         # (future) Architecture Decision Records
└── templates/                    # (future) Issue and PR templates
```

## Projects

- **[TSQR Project Board](https://github.com/users/lstbob/projects/4)** — tracks all active backlog items

## Current Backlog (15 [Tech] Issues)

### tsqr-tool-lib
| # | Title | Issue |
|---|-------|-------|
| 1 | Aggregate boundary, events, and domain service wiring | [#30](https://github.com/lstbob/tsqr-tool-lib/issues/30) |
| 2 | Domain model cleanup | [#31](https://github.com/lstbob/tsqr-tool-lib/issues/31) |
| 3 | Persistence architecture and concurrency safety | [#32](https://github.com/lstbob/tsqr-tool-lib/issues/32) |

### tsqr-communities
| # | Title | Issue |
|---|-------|-------|
| 4 | Transaction boundary and query layer refactor | [#1](https://github.com/lstbob/tsqr-communities/issues/1) |
| 5 | Domain model improvements | [#2](https://github.com/lstbob/tsqr-communities/issues/2) |
| 6 | Schema hardening | [#3](https://github.com/lstbob/tsqr-communities/issues/3) |

### tsqr-soup-kitchen
| # | Title | Issue |
|---|-------|-------|
| 7 | Domain model implementation | [#1](https://github.com/lstbob/tsqr-soup-kitchen/issues/1) |
| 8 | Query layer refactor | [#2](https://github.com/lstbob/tsqr-soup-kitchen/issues/2) |
| 9 | Schema hardening | [#3](https://github.com/lstbob/tsqr-soup-kitchen/issues/3) |

### tsqr-identity
| # | Title | Issue |
|---|-------|-------|
| 10 | Domain model creation | [#1](https://github.com/lstbob/tsqr-identity/issues/1) |
| 11 | Schema consolidation and hardening | [#2](https://github.com/lstbob/tsqr-identity/issues/2) |

### tsqr-autheo
| # | Title | Issue |
|---|-------|-------|
| 12 | Error handling and async patterns | [#1](https://github.com/lstbob/tsqr-autheo/issues/1) |
| 13 | Schema hardening | [#2](https://github.com/lstbob/tsqr-autheo/issues/2) |

### tsqr-support
| # | Title | Issue |
|---|-------|-------|
| 14 | Domain model creation | [#1](https://github.com/lstbob/tsqr-support/issues/1) |
| 15 | Schema and query hardening | [#2](https://github.com/lstbob/tsqr-support/issues/2) |
