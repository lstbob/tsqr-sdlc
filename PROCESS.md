# TSQR Development Process

## Team
- **1 developer** (solo)
- 2-week sprints
- Max **5 story points** capacity per sprint

---

## 1. Issue Types

Prefixes used in issue titles:

| Prefix | When to Use | Example |
|--------|-------------|---------|
| `[Story]` | New feature or user-facing capability | `[Story] Add tool reservation calendar view` |
| `[Tech]` | Technical improvement, refactoring, architectural change | `[Tech] Add optimistic concurrency control` |
| `[Bug]` | Defect — incorrect behavior, crash, data loss | `[Bug] Loan end date allows past dates` |
| `[Hotfix]` | Urgent production fix (bypasses sprint) | `[Hotfix] Auth token validation rejects valid tokens` |
| `[Infra]` | CI/CD, Docker, database, tooling setup | `[Infra] Set up PostgreSQL backup job` |
| `[Epic]` | Large cross-cutting initiative spanning multiple sprints | `[Epic] Migrate identity to proper DDD` |

---

## 2. Statuses & Transitions

All issues flow through these statuses:

```
Backlog → In progress → In review → Ready For QA → In QA → Done
```

| Status | Meaning |
|--------|---------|
| **Backlog** | Refined, estimated, ready to pull into a sprint |
| **In progress** | Actively being worked on this sprint |
| **In review** | Code written, awaiting self-review or PR review |
| **Ready For QA** | Code merged, needs verification on staging |
| **In QA** | Being tested |
| **Done** | Merged, tested, deployed to production |

### Rules
- Only move an issue to **In progress** during sprint planning or when capacity frees up mid-sprint
- An issue cannot skip **In review** → move there once you open a PR
- **Done** means the code is merged, the feature works, and no follow-up is needed from this sprint
- If work isn't finished by sprint end, move it back to **Backlog** (don't carry over)

---

## 3. Estimation (Story Points)

Use the **Fibonacci sequence**: 1, 2, 3, 5, 8, 13, 21

### What each value means (for a solo dev)

| SP | What fits | Examples |
|----|-----------|----------|
| **1** | Trivial — one file, one change, < 2 hours | Fix a typo, rename a method, add a CHECK constraint |
| **2** | Small — a few files, understood path, < 4 hours | Add a new query method, remove dead code, formulaic SQL changes for one repo |
| **3** | Medium — moderate refactoring, one aggregate | Add validation to an entity, convert a child entity, implement event handler |
| **5** | Large — multi-file, multiple concerns within one bounded context | Schema hardening for a full service, full aggregate encapsulation, query layer refactor |
| **8** | Very large — affects multiple aggregates, significant domain modeling | Build a domain model from scratch (Ticket aggregate, UserProfile encapsulation) |
| **13** | Extra large — cross-cutting, multiple bounded contexts | Persistence abstraction redesign, aggregate boundary refactoring across handlers |
| **21** | Epic — too big for one sprint, must be split | (Avoid — break into 13s and 8s) |

### Splitting Rule
Any issue > **5 SP** must be split into sub-issues where each part is ≤ 5 SP.

Sub-issues use the naming pattern: `{label} — {description of part} (Part of #{parent})`

Example:
- Parent: `[Tech] Aggregate boundary, events, and domain service wiring` (13 SP)
- Sub 1: `1a — Refactor cross-aggregate transactions (Part of #30)` (5 SP)
- Sub 2: `1b — Wire domain events and ReservationQueueService (Part of #30)` (5 SP)
- Sub 3: `1c — Integrate Policy aggregate and FineService (Part of #30)` (3 SP)

### Sprint Capacity Rule
A sprint's total story points must not exceed **5**. To pack efficiently:
- Combine a **3 SP** item with a **2 SP** item to fill a sprint
- A **5 SP** item fills a sprint alone
- Smaller items (1–3 SP) can go solo with slack time

---

## 4. Priority

| Priority | Meaning |
|----------|---------|
| **P0** | Blocking — nothing else moves until this is done (reserved for hotfixes/production outages) |
| **P1** | High — must be completed for the current milestone or architectural integrity |
| **P2** | Medium — important but can be deferred to a later sprint |

### Current backlog priority distribution
- **P1:** All architecture, domain model, and query layer issues (11 items)
- **P2:** Schema hardening, cleanup, and formulaic SQL changes (4 items)
- **P0:** (none yet)

---

## 5. Size (Relative Complexity)

| Size | Meaning | Typical SP Range |
|------|---------|-----------------|
| **XS** | One-file change, no refactoring | 1 |
| **S** | Small scope, well-understood | 2 |
| **M** | Moderate, touches 2–3 files | 3 |
| **L** | Significant, multiple files and concerns | 5 |
| **XL** | Cross-cutting, multiple bounded contexts | 8+ |

---

## 6. Sprint Process

### Before sprint start
1. Populate sprint from **Backlog** (highest priority P1 items first)
2. Ensure sprint total ≤ **5 SP**
3. Assign the sprint iteration field to each issue

### During sprint
1. Move issue to **In progress** when you start working
2. Create PR, move to **In review**
3. Merge, move to **Ready For QA**
4. Test, move to **In QA**
5. Verify, move to **Done**

### At sprint end
1. Any issue not **Done** goes back to **Backlog**
2. Review velocity (did you finish all 5 SP?)
3. Plan next sprint's 5 SP

---

## 7. Sub-Issues & Parent Tracking

- **Parent issues** carry the overarching title and total SP estimate
- **Sub-issues** carry the sprint assignment and per-part SP
- The **Sub-issues progress** field on the project board auto-computes completion % from sub-issues
- Sub-issues reference their parent with `Part of #{number}` in the body
- A parent issue's Status should reflect the aggregate of its sub-issues

### When to create sub-issues
- Any issue > **5 SP** (mandatory split)
- Any issue that spans > 2 files and has clearly separable work items

---

## 8. Quality Gates

Before moving **In review → Ready For QA**:
- [ ] Code compiles without warnings
- [ ] Existing tests pass
- [ ] No `TODO`, `FIXME`, or debug code left in
- [ ] Follows Clean Architecture dependency direction
- [ ] No new public constructors without validation

Before moving **In QA → Done**:
- [ ] Feature works on staging
- [ ] No regressions in related functionality
- [ ] Database migrations (if any) are reversible
