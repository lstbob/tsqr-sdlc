# tsqr-sdlc

SDLC artifacts for the **TSQR (TownsSquare)** platform — backlog, sprints, issue definitions, ADRs, and process documentation across all microservices.

- **[Project Board](https://github.com/users/lstbob/projects/4)**
- **[Current Sprint](https://github.com/users/lstbob/projects/4/views/1)**
- **[Next Sprint](https://github.com/users/lstbob/projects/4/views/2)**
- **[Sprint Workflow Runbook](docs/SPRINT-WORKFLOW.md)**

---

## Repository Structure

```
tsqr-sdlc/
├── README.md
├── PROCESS.md
├── docs/                      # Sprint workflow runbook and how-to docs
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

## Sprint Backlog (Sprints 11–16, capacity 40 SP per 2-week sprint)

**Capacity:** 1 developer, **40 SP** per sprint, and no single issue larger than **5 SP**. The measured speed in Sprints 9 and 10 was about 110 SP per sprint, so 40 SP leaves room for review, QA and unplanned fixes.

> **Note:** Parent epics stay without a sprint. Only their sub-issues and standalone issues get a sprint. Done issues keep their sprint, so the board records what each sprint delivered.

**Delivery record:** Sprint 10 (Nov 13–26) closed 41 board items: 113 SP of leaf work, without parent issues. The 2026-10-29 plan put 60 issues into sprints; 40 of them (199 SP) closed before their planned sprint started.

**Current state (2026-11-27):** the audit v3.5 work (`tsqr-domain/thegoodandthebad-v3.5.md`) is scheduled in Sprints 11–16 in priority order: P0 security and data integrity first, then the tool-lib circulation loop, then P1 and P2. autheo#20 (per-service audiences) and tool-lib#75 (C-3) are Done in Sprint 11.

**Identity contract:** [`sub` is the canonical cross-service identity](https://github.com/lstbob/tsqr-autheo/blob/main/docs/JWT-CONTRACT.md); the `mbr` claim is retired. Each service validates its own audience (`tsqr-<service>`); the gateway exchanges the user token for a service token.

### Sprint 11 (Nov 27–Dec 10) — 34/40 SP
| Item | SP | Priority | Repo |
|------|----|----------|------|
| [Bug] Guard repair and lost transitions and release the item when the queue is empty ✅ | 5 | P1 | tool-lib [#75](https://github.com/lstbob/tsqr-tool-lib/issues/75) |
| [Tech] Per-service JWT audience / token exchange ✅ | 5 | — | autheo [#20](https://github.com/lstbob/tsqr-autheo/issues/20) |
| [Bug] Refuse to sign tokens with HS256 outside Development | 1 | P0 | autheo [#23](https://github.com/lstbob/tsqr-autheo/issues/23) |
| [Bug] Remove the HS256 fallback from shared JWT validation | 2 | P0 | common [#12](https://github.com/lstbob/tsqr-common/issues/12) |
| [Bug] Stop the static role map from widening explicit token permissions | 2 | P0 | common [#13](https://github.com/lstbob/tsqr-common/issues/13) |
| [Bug] Remove the commit retry that commits an empty transaction | 1 | P0 | communities [#32](https://github.com/lstbob/tsqr-communities/issues/32) |
| [Bug] Stop logging reset and confirmation tokens in Production | 2 | P0 | deploy [#29](https://github.com/lstbob/tsqr-deploy/issues/29) |
| [Bug] Deny by default at the gateway: FallbackPolicy, rate limiter and route-contract test | 5 | P0 | gateway [#12](https://github.com/lstbob/tsqr-gateway/issues/12) |
| [Bug] Delete and rotate the committed identity Jwt:Key | 1 | P0 | identity [#18](https://github.com/lstbob/tsqr-identity/issues/18) |
| [Bug] Close ticket and incident data exposure and the community-1 fallback | 5 | P0 | support [#19](https://github.com/lstbob/tsqr-support/issues/19) |
| [Bug] End the active loan and calculate the fine on return | 5 | P0 | tool-lib [#73](https://github.com/lstbob/tsqr-tool-lib/issues/73) |

### Sprint 12 (Dec 11–Dec 24) — 34/40 SP
| Item | SP | Priority | Repo |
|------|----|----------|------|
| [Tech] Add a CommunityId value object and ITenantContext with 403 on a missing claim | 3 | P0 | common [#15](https://github.com/lstbob/tsqr-common/issues/15) |
| [Bug] Complete the reservation on loan and enforce the queue order | 5 | P0 | tool-lib [#74](https://github.com/lstbob/tsqr-tool-lib/issues/74) |
| [Story] Raise the credential policy: PBKDF2 600 000, 12-character minimum, account lockout, revoke on reset | 5 | P1 | autheo [#24](https://github.com/lstbob/tsqr-autheo/issues/24) |
| [Bug] Trust forwarded headers only from the gateway network so the rate limiter is per client | 3 | P1 | common [#14](https://github.com/lstbob/tsqr-common/issues/14) |
| [Bug] Restrict community updates to the coordinators of that community | 2 | P1 | communities [#29](https://github.com/lstbob/tsqr-communities/issues/29) |
| [Infra] Use one least-privilege PostgreSQL role per service | 3 | P1 | deploy [#30](https://github.com/lstbob/tsqr-deploy/issues/30) |
| [Infra] Run every container as non-root with a hardened compose profile | 5 | P1 | deploy [#31](https://github.com/lstbob/tsqr-deploy/issues/31) |
| [Bug] Validate avatar ids and file content | 2 | P1 | identity [#19](https://github.com/lstbob/tsqr-identity/issues/19) |
| [Bug] Add soup-kitchen permissions for writes and guest reads | 3 | P1 | soup-kitchen [#33](https://github.com/lstbob/tsqr-soup-kitchen/issues/33) |
| [Bug] Take actor ids from the token and guard renew and return | 3 | P1 | tool-lib [#67](https://github.com/lstbob/tsqr-tool-lib/issues/67) |

### Sprint 13 (Dec 25–Jan 7) — 32/40 SP
| Item | SP | Priority | Repo |
|------|----|----------|------|
| [Tech] Issue token permissions from identity role grants of the active community | 5 | P1 | autheo [#26](https://github.com/lstbob/tsqr-autheo/issues/26) |
| [Infra] Bind published ports to localhost and split the compose network | 2 | P1 | deploy [#32](https://github.com/lstbob/tsqr-deploy/issues/32) |
| [Infra] Pin images and actions, and add Dependabot, CodeQL and image scanning | 5 | P1 | deploy [#34](https://github.com/lstbob/tsqr-deploy/issues/34) |
| [Infra] Fail CI on vulnerable packages and new warnings | 2 | P1 | deploy [#35](https://github.com/lstbob/tsqr-deploy/issues/35) |
| [Infra] Add a database backup job and a tested restore runbook | 3 | P1 | deploy [#37](https://github.com/lstbob/tsqr-deploy/issues/37) |
| [Infra] Mount secrets as files and use one environment policy | 3 | P1 | deploy [#40](https://github.com/lstbob/tsqr-deploy/issues/40) |
| [Tech] ADR: one IAM authority and community-scoped role grants | 2 | P1 | domain [#7](https://github.com/lstbob/tsqr-domain/issues/7) |
| [Tech] Scope tool-lib reads and writes by tenant through ITenantContext | 5 | P1 | tool-lib [#68](https://github.com/lstbob/tsqr-tool-lib/issues/68) |
| [Story] Model fine payment and waiver as a fine ledger | 5 | P1 | tool-lib [#71](https://github.com/lstbob/tsqr-tool-lib/issues/71) |

### Sprint 14 (Jan 8–Jan 21) — 35/40 SP
| Item | SP | Priority | Repo |
|------|----|----------|------|
| [Tech] Harden Result<T> and add one Result-to-HTTP mapper | 3 | P1 | common [#18](https://github.com/lstbob/tsqr-common/issues/18) |
| [Tech] Publish TSQR.Common.Persistence: async Dapper unit of work and xmin repository | 5 | P1 | common [#19](https://github.com/lstbob/tsqr-common/issues/19) |
| [Tech] 3a — Choose the migration runner and baseline the 28 init scripts | 5 | P1 | deploy [#41](https://github.com/lstbob/tsqr-deploy/issues/41) |
| [Tech] 3b — Run migrations at stack start and apply them twice in CI | 3 | P1 | deploy [#42](https://github.com/lstbob/tsqr-deploy/issues/42) |
| [Tech] 6a — Adopt the shared kernel Entity and IAggregateRoot | 3 | P1 | identity [#21](https://github.com/lstbob/tsqr-identity/issues/21) |
| [Tech] 6b — Add identity value objects and return Result from PendingEmailChange | 5 | P1 | identity [#22](https://github.com/lstbob/tsqr-identity/issues/22) |
| [Story] Expire reservations and send reminders from a scheduled process manager | 5 | P1 | tool-lib [#72](https://github.com/lstbob/tsqr-tool-lib/issues/72) |
| [Story] Add a loan read model and return the loan id on create | 3 | P1 | tool-lib [#76](https://github.com/lstbob/tsqr-tool-lib/issues/76) |
| [Bug] Let regular members borrow with a tools.borrow permission | 3 | P1 | tool-lib [#77](https://github.com/lstbob/tsqr-tool-lib/issues/77) |

### Sprint 15 (Jan 22–Feb 4) — 33/40 SP
| Item | SP | Priority | Repo |
|------|----|----------|------|
| [Tech] 6a — Add ticket comments | 3 | P1 | support [#20](https://github.com/lstbob/tsqr-support/issues/20) |
| [Tech] 6b — Add ticket attachments with size and type limits | 3 | P1 | support [#21](https://github.com/lstbob/tsqr-support/issues/21) |
| [Tech] 6c — Add ResolvedBy, ClosedBy and LastModified audit fields to tickets | 2 | P1 | support [#22](https://github.com/lstbob/tsqr-support/issues/22) |
| [Tech] Replace the shared internal API key with per-caller service credentials | 3 | P2 | autheo [#25](https://github.com/lstbob/tsqr-autheo/issues/25) |
| [Tech] Make Communities the owner of community membership | 5 | P2 | communities [#30](https://github.com/lstbob/tsqr-communities/issues/30) |
| [Tech] Write a personal-data inventory with retention and erasure rules | 3 | P2 | domain [#6](https://github.com/lstbob/tsqr-domain/issues/6) |
| [Tech] Send security response headers at the edge | 2 | P2 | gateway [#13](https://github.com/lstbob/tsqr-gateway/issues/13) |
| [Tech] Split Donation and volunteer shifts out of the Event aggregate | 5 | P2 | soup-kitchen [#34](https://github.com/lstbob/tsqr-soup-kitchen/issues/34) |
| [Tech] Reduce Member to borrower facts with one membership state machine | 5 | P2 | tool-lib [#69](https://github.com/lstbob/tsqr-tool-lib/issues/69) |
| [Tech] Remove the dead tool-lib model: Location, Country, unused services and NoSQL contracts | 2 | P2 | tool-lib [#70](https://github.com/lstbob/tsqr-tool-lib/issues/70) |

### Sprint 16 (Feb 5–Feb 18) — 33/40 SP
| Item | SP | Priority | Repo |
|------|----|----------|------|
| [Tech] Give integration events stable names and versions | 3 | P2 | common [#16](https://github.com/lstbob/tsqr-common/issues/16) |
| [Tech] Split liveness and readiness health checks | 2 | P2 | common [#17](https://github.com/lstbob/tsqr-common/issues/17) |
| [Tech] Provide one internal API key authentication handler | 2 | P2 | common [#20](https://github.com/lstbob/tsqr-common/issues/20) |
| [Tech] Tighten shared-kernel encapsulation and allow record value objects | 3 | P2 | common [#21](https://github.com/lstbob/tsqr-common/issues/21) |
| [Tech] Return Result instead of exceptions in the communities domain | 2 | P2 | communities [#31](https://github.com/lstbob/tsqr-communities/issues/31) |
| [Infra] Add a TLS-terminating edge proxy with HSTS | 3 | P2 | deploy [#33](https://github.com/lstbob/tsqr-deploy/issues/33) |
| [Infra] Add .dockerignore everywhere and build tsqr-common once per pipeline | 2 | P2 | deploy [#36](https://github.com/lstbob/tsqr-deploy/issues/36) |
| [Infra] Persist identity avatars on a named volume | 1 | P2 | deploy [#38](https://github.com/lstbob/tsqr-deploy/issues/38) |
| [Infra] Add an OpenTelemetry collector and a trace backend profile | 3 | P2 | deploy [#39](https://github.com/lstbob/tsqr-deploy/issues/39) |
| [Tech] Use typed resilient HTTP clients in the BFF and validate service URLs at startup | 3 | P2 | gateway [#14](https://github.com/lstbob/tsqr-gateway/issues/14) |
| [Tech] Move avatar and profile logic from ProfileController into commands | 3 | P2 | identity [#20](https://github.com/lstbob/tsqr-identity/issues/20) |
| [Tech] Inject TimeProvider and pass the time into aggregate methods | 3 | P2 | tool-lib [#78](https://github.com/lstbob/tsqr-tool-lib/issues/78) |
| [Tech] Add Directory.Build.props and an architecture test, and fix the 34 CS8618 warnings | 3 | P2 | tool-lib [#79](https://github.com/lstbob/tsqr-tool-lib/issues/79) |

**Scheduled: 201 SP** in Sprints 11–16. Sprints 17–20 are empty headroom; `defer` uses them and adds more iterations when needed.

### Backlog (unscheduled)

Only parent epics and one placeholder stay in the Backlog. Epics are tracked by **Sub-issues progress**:

| Epic | Repo |
|------|------|
| [Tech] Adopt DB migration runner (DbUp/FluentMigrator); no `IF NOT EXISTS`/no version table today | deploy [#3](https://github.com/lstbob/tsqr-deploy/issues/3) |
| Fixing AI slop | domain [#1](https://github.com/lstbob/tsqr-domain/issues/1) |
| [Epic] Audit v3.5: security hardening | domain [#2](https://github.com/lstbob/tsqr-domain/issues/2) |
| [Epic] Audit v3.5: domain model (DDD) corrections | domain [#3](https://github.com/lstbob/tsqr-domain/issues/3) |
| [Epic] Audit v3.5: infrastructure, deployment and database | domain [#4](https://github.com/lstbob/tsqr-domain/issues/4) |
| [Epic] Audit v3.5: C# and design-pattern improvements | domain [#5](https://github.com/lstbob/tsqr-domain/issues/5) |
| [Tech] Introduce Entity base + IAggregateRoot + value objects (fixes audit §8 foundation) | identity [#6](https://github.com/lstbob/tsqr-identity/issues/6) |
| [Tech] Ticket state machine + Incident aggregate + Comments/Attachments + pagination | support [#6](https://github.com/lstbob/tsqr-support/issues/6) |
| [Epic] Close the tool-lib circulation loop (Part of lstbob/tsqr-domain#3) | tool-lib [#66](https://github.com/lstbob/tsqr-tool-lib/issues/66) |

`tsqr-domain#1` is an unestimated placeholder that needs triage.

---

## Rescheduling & sprint workflow

The `scripts/sprint` CLI enforces the 40 SP capacity and the 5 SP item limit, and cascades changes. It is a dry-run by default; add `--apply` to write.

> **Full runbook:** see **[docs/SPRINT-WORKFLOW.md](docs/SPRINT-WORKFLOW.md)** for step-by-step add/defer/move/rebalance instructions, recipes, and troubleshooting.

```bash
./scripts/sprint status                  # per-sprint load and capacity
./scripts/sprint audit                   # epics, oversized items, missing estimates
./scripts/sprint add <repo>#<num> --to 9 # add a backlog item (dry run)
./scripts/sprint defer <repo>#<num>      # defer to next sprint + cascade (dry run)
./scripts/sprint move <repo>#<num> --to 12
./scripts/sprint rebalance --from 9
./scripts/sprint extend --count 1
```

**`defer` behaviour:** moves the item to the next sprint, shifts every item in later sprints forward one iteration, and refuses to place an item larger than the capacity. If the last sprint overflows, it adds a new iteration first (with a config backup).

**`add` behaviour:** puts an unscheduled backlog item into a sprint, refusing if the item or the destination exceeds capacity.

**Authentication:** the CLI uses `gh` and needs the `project` scope. In GitHub Actions, set `GH_TOKEN` to a PAT with `project` + `repo` scopes.

---

## Testing

Each service owns its test project under `tests/` and uses the same stack:
xUnit 2.9.3, `Microsoft.NET.Test.Sdk` 17.14.1, `xunit.runner.visualstudio`
3.1.4, and `coverlet.collector` 6.0.4. Domain invariants, persistence adapters,
and command handlers are covered with hand-written fakes (no mocking library).

Run every discovered suite from the workspace:

```bash
./scripts/test-all                                  # all affected repos
./scripts/test-all --repo tsqr-support              # one repo
./scripts/test-all --repo tsqr-support --repo tsqr-gateway
./scripts/test-all --filter "FullyQualifiedName~Handler"
```

The runner discovers `tests/**/*.csproj`, so a new test project is picked up
automatically. It exits non-zero if any suite fails. Repositories checked out
on an older branch without the test project are reported as `SKIP`.

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

3. (Optional) adjust the default alert window in `.github/workflows/sprint-alert.yml`, or pass `alert_days` when running the workflow manually.

---

## Parent Issues & Sub-issues

No open parent issues remain. The tool-library, identity, soup-kitchen, and support grouping issues were closed after their sub-issues shipped. Remaining work is tracked as standalone follow-ups.

---

## Field Values

All board items use:

| Field | Values Used |
|-------|-------------|
| **Sprint** (bob-sprint) | Sprint 9–19 (currently empty); empty for the Backlog |
| **Priority** | P0 (critical), P1 (high), P2 (medium) |
| **Size** | XS, S, M, L, XL |
| **Estimate(SP)** | 1, 2, 3, 5, 8, 13 (Fibonacci) |
| **Status** | Backlog / In progress / In review / Ready For QA / In QA / Done |
| **Sub-issues progress** | Auto-computed by GitHub |
