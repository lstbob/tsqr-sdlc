# Sprint Workflow — Updating Issues & Sprints

Runbook for the **tsqr** GitHub Project (#4). Use this when you need to add, defer, move, rebalance, or extend sprint work.

- **Board:** <https://github.com/users/lstbob/projects/4>
- **Current Sprint view:** <https://github.com/users/lstbob/projects/4/views/1>
- **Next Sprint view:** <https://github.com/users/lstbob/projects/4/views/2>
- **Sprint plan snapshot:** [README.md](../README.md)
- **Process rules:** [PROCESS.md](../PROCESS.md)

> Examples use the board state as of **2026-10-30**. Run `./scripts/sprint status` for the current state before copying commands.

---

## Quick start

```bash
cd /home/lbobc/dev/tsqr-sdlc

./scripts/sprint status          # inspect current loads
./scripts/sprint audit           # check for rule violations

./scripts/sprint defer <repo>#<num>            # dry run
./scripts/sprint defer <repo>#<num> --apply    # write

./scripts/sprint status          # verify
./scripts/sprint audit
```

Replace `<repo>#<num>` with a real reference such as `tsqr-tool-lib#31` or a full issue URL.

Every write command is a **dry run** until you add `--apply`. Always read the dry-run output before applying it.

---

## 1. Rules the scripts enforce

| Rule | Why |
|---|---|
| Max **5 SP** per sprint | Solo developer, 2-week sprint |
| Parent epics stay unscheduled | Epics are tracked by Sub-issues progress; only sub-issues get sprint assignments |
| Items **>5 SP** are refused | Split them first, per `PROCESS.md` |
| `defer` cascades forward | Later scheduled items shift +1 sprint so capacity is preserved |
| `add` does not cascade | It only places one backlog item into a sprint with room |
| Every write is a dry run by default | Review the cascade before changing the board |

**Current sprint** means the iteration containing today's date. If no iteration contains today, the CLI uses the next future iteration (or the last active sprint if none are in the future).

---

## 2. Setup

Run all commands from the repository root:

```bash
cd /home/lbobc/dev/tsqr-sdlc
```

Check GitHub CLI authentication:

```bash
gh auth status
```

The CLI needs the `project` scope. If it is missing:

```bash
gh auth refresh -s project
```

Python 3.10+ is required (the scripts use modern type hints).

Optional environment variables:

| Variable | Default | Purpose |
|---|---|---|
| `SPRINT_OWNER` | `lstbob` | Project owner |
| `SPRINT_PROJECT` | `4` | Project number |
| `SPRINT_FIELD` | `bob-sprint` | Iteration field name |
| `SPRINT_CAPACITY` | `5` | Story points per sprint |
| `SPRINT_ALERT_DAYS` | `2` | Days before sprint end to alert |

---

## 3. Inspect before changing anything

```bash
./scripts/sprint status
./scripts/sprint status --json
./scripts/sprint audit
```

`status` shows each active iteration, its dates, load/capacity bar, and items sorted by priority. The bottom shows scheduled and backlog totals.

`audit` checks for:

- parent epics assigned to a sprint (error)
- items larger than the capacity (error)
- sprints over capacity (error)
- items without an estimate (warning)
- `Done` items still assigned to a sprint (warning)
- items assigned to completed sprints (warning)

A clean audit looks like:

```text
Audit clean: every sprint is within capacity and no epics are scheduled.
```

For machine-readable output:

```bash
./scripts/sprint status --json
```

Raw project data:

```bash
gh project item-list 4 --owner lstbob --limit 100 --format json
```

---

## 4. Command map

| Command | What it does | Cascades? |
|---|---|---|
| `add` | Backlog → sprint | No |
| `defer` | Current sprint → next sprint | Yes: every later item shifts +1 |
| `move --to N` | Scheduled item → sprint N | Yes if N is later; no if N is earlier |
| `rebalance --from N` | Repack scheduled items from N onward | Reassigns within the scheduled set |
| `extend --count N` | Add future iterations | No item changes |
| `status` / `audit` | Read-only inspection | — |

---

## 5. Add a backlog item to a sprint

Use `add` when the item has **no sprint assignment**.

```bash
./scripts/sprint add <repo>#<num> --to <sprint>          # dry run
./scripts/sprint add <repo>#<num> --to <sprint> --apply  # write
```

If `--to` is omitted, the item goes to the current sprint.

### Real example

Sprint 9 currently has **3/5 SP**, so a 2 SP item fits exactly:

```bash
./scripts/sprint add tsqr-tool-lib#31 --to 9
./scripts/sprint add tsqr-tool-lib#31 --to 9 --apply
```

The dry run shows the item and the resulting sprint load. The `--apply` line actually fills Sprint 9 to 5/5.

### `add` refuses when

- the item is a parent epic
- the item is already scheduled (use `move` instead)
- the item is larger than 5 SP (split it first)
- the target sprint is not active (choose an active sprint, or run `extend` first if it is beyond the horizon)
- the destination would exceed 5 SP

`add` does **not** cascade. If the destination is full, either choose another sprint or free capacity with `defer`/`move`.

---

## 6. Defer — push an item forward

Use `defer` when you cannot finish an item this sprint. It moves the item to the next sprint and shifts **every later scheduled item forward one sprint**.

```bash
./scripts/sprint defer <repo>#<num>                 # dry run, next sprint
./scripts/sprint defer <repo>#<num> --apply         # write
./scripts/sprint defer <repo>#<num> --to <sprint>   # specific later sprint
```

### Real example

`tsqr-communities#5` is currently in Sprint 9. Previewing a defer:

```bash
./scripts/sprint defer tsqr-communities#5
```

The preview shows:

- `tsqr-communities#5`: Sprint 9 → 10
- `tsqr-identity#5`: Sprint 10 → 11
- `tsqr-autheo#3`: Sprint 11 → 12
- … every later scheduled item shifts one sprint
- `tsqr-communities#4`: Sprint 19 → 20

Sprint 20 already exists, so no new iteration is needed. If the cascade goes past the last active sprint, the script adds iterations first and writes an iteration-config backup to `sprints/`.

Apply only after checking the preview:

```bash
./scripts/sprint defer tsqr-communities#5 --apply
```

### `defer` refuses when

- the item is a parent epic
- the item is closed or `Done`
- the item has no sprint (use `add` instead)
- the item is larger than 5 SP (split it first)

After applying, run `./scripts/sprint status` and `./scripts/sprint audit`.

---

## 7. Move — place an item in a specific sprint

Use `move` for an item that **already has a sprint**.

```bash
./scripts/sprint move <repo>#<num> --to <sprint>          # dry run
./scripts/sprint move <repo>#<num> --to <sprint> --apply  # write
```

### Moving later

Moving to a later sprint uses the same cascade as `defer`: every item at or after the target shifts +1.

Example: `tsqr-tool-lib#43` is in Sprint 15. Moving it to Sprint 16 shifts Sprint 16–19 forward to 17–20:

```bash
./scripts/sprint move tsqr-tool-lib#43 --to 16
```

### Moving earlier

Moving to an earlier sprint does **not** cascade. The destination must already have room.

Example: if Sprint 9 has 2 SP free, a 2 SP item from a later sprint can be pulled forward:

```bash
./scripts/sprint move <repo>#<num> --to 9
```

If the destination would exceed 5 SP, the command refuses.

### `move` refuses when

- the item is a parent epic
- the item is closed or `Done`
- the item has no sprint (use `add` instead)
- the item is larger than 5 SP (split it first)
- the target sprint does not exist (run `extend` first)
- moving earlier would exceed the destination capacity

If the target is beyond the current horizon, `move` adds iterations automatically (with a config backup).

---

## 8. Rebalance — repack scheduled work

Use `rebalance` after estimates change, after a sprint ends, or when sprint loads are uneven. It repacks all scheduled items from a starting sprint onward, priority-first (`P0` → `P1` → `P2`).

```bash
./scripts/sprint rebalance --from <sprint>          # dry run
./scripts/sprint rebalance --from <sprint> --apply  # write
```

Example:

```bash
./scripts/sprint rebalance --from 9
```

What it does:

- considers items already scheduled from Sprint 9 onward
- skips parent epics
- leaves items larger than 5 SP untouched and lists them
- sorts by original sprint, then priority, then issue key
- greedily packs items into 5 SP sprints
- adds future sprints if the repack needs more room

`rebalance` does **not** pull items from the backlog. Use `add` for that.

---

## 9. Extend — add future sprints

Use `extend` when you want more future iterations before assigning work.

```bash
./scripts/sprint extend --count 1          # dry run
./scripts/sprint extend --count 1 --apply  # write
```

What it does:

- appends iterations after the last active one
- keeps the same duration and contiguous dates
- writes `sprints/iterations-backup-<timestamp>.json` before changing the field
- preserves existing iteration IDs
- warns if any existing IDs changed

`defer`, `move`, and `rebalance` also add iterations automatically when their target is past the horizon, so a separate `extend` is only needed when you want to pre-create headroom.

---

## 10. Sprint-end alerts

The alert workflow runs daily at **07:00 UTC**. When a sprint ends within the alert window and still has open items, it creates or updates an issue in `lstbob/tsqr-sdlc`, assigned to `@lstbob`. GitHub's assignment notification sends the email.

### Local dry run

```bash
python3 scripts/sprint-alert --dry-run
```

### Manual workflow run

```bash
gh workflow run sprint-alert.yml -f alert_days=5
gh run list --workflow sprint-alert.yml --limit 5
gh run view <run-id> --log
```

### Setup

The workflow needs a repository secret named `PROJECT_TOKEN` containing a PAT with `project` and `repo` scopes:

```bash
gh secret set PROJECT_TOKEN -R lstbob/tsqr-sdlc
```

If the secret is missing or expired, the workflow fails at the `Check PROJECT_TOKEN` step. Close the generated alert issue manually after you have handled the sprint.

---

## 11. Common recipes

### A P0 hotfix arrives and the sprint is full

1. Defer a lower-priority item to free capacity:
   ```bash
   ./scripts/sprint defer <lower-priority-item> --apply
   ```
2. Add the hotfix to the current sprint if it is ≤5 SP:
   ```bash
   ./scripts/sprint add <hotfix> --to <current-sprint> --apply
   ```
3. If the hotfix is >5 SP, split it first.

### You want to pull work forward

Use `move` to the current sprint. The destination must have room, and no cascade occurs:

```bash
./scripts/sprint move <repo>#<num> --to <current-sprint>
```

If there is no room, defer something first or wait for the next sprint.

### A sprint ends with unfinished work

Defer the unfinished item; later sprints shift automatically:

```bash
./scripts/sprint defer <repo>#<num> --apply
```

Then rebalance if the shift left uneven loads:

```bash
./scripts/sprint rebalance --from <next-sprint> --apply
```

### An item is too big for one sprint

1. Split it into sub-issues where each part is ≤5 SP (see `PROCESS.md`).
2. Keep the parent epic unscheduled.
3. Add each sub-issue to a sprint:
   ```bash
   ./scripts/sprint add <sub-issue> --to <sprint> --apply
   ```

### Sprint loads are uneven

```bash
./scripts/sprint rebalance --from <sprint> --apply
```

### You need more horizon

```bash
./scripts/sprint extend --count 2 --apply
```

### The current sprint has spare capacity

Add a small backlog item that fits:

```bash
./scripts/sprint add tsqr-tool-lib#31 --to 9
```

---

## 12. After applying changes: update README and push

The scripts update GitHub, **not** the README. The README sprint tables are a human-readable snapshot and must be updated after any write.

Checklist:

1. Verify the board:
   ```bash
   ./scripts/sprint status
   ./scripts/sprint audit
   ```
2. Update the sprint tables in `README.md`:
   - add/remove items in the affected sprint sections
   - update each item's SP
   - update the scheduled total
   - update the backlog count and SP
3. If you added or removed iterations, update the horizon text in `README.md`.
4. Commit and push:
   ```bash
   git add README.md docs/SPRINT-WORKFLOW.md
   git commit -m "Update sprint plan after defer/move"
   git push
   ```

Before a large cascade, it helps to capture the current state:

```bash
./scripts/sprint status --json > /tmp/sprint-before.json
```

The board is the source of truth; the README should match it after every change.

---

## 13. Troubleshooting

### `gh` authentication errors

```bash
gh auth status
gh auth refresh -s project
```

### `Sprint N is not active`

Run `./scripts/sprint status` and choose an active sprint. If you need a new future sprint:

```bash
./scripts/sprint extend --count 1 --apply
```

### `... is a parent epic; epics must stay unscheduled`

Schedule the sub-issues instead. The parent stays unscheduled for Sub-issues progress tracking.

### `... is X SP, over the 5 SP capacity; split it first`

Split the issue into sub-issues of ≤5 SP each, then add the sub-issues.

### `... has no sprint; use add --to <sprint>`

Use `add` for backlog items. `move` and `defer` only work on items that already have a sprint.

### `Sprint N has X SP; adding Y SP would exceed 5`

Free capacity first:

```bash
./scripts/sprint defer <lower-priority-item> --apply
```

Then retry the `add` or `move`.

### `WARNING: ... has no estimate; treating it as 0 SP`

Set the **Estimate(SP)** field on the project item. `audit` will continue to warn until it is set.

### Audit reports a `Done` item still in a sprint

Clear the sprint field for that item in the GitHub UI. The CLI does not expose a `clear` command; `clearProjectV2ItemFieldValue` can also be used via GraphQL.

### The Priority field lost an option

Symptoms: items show **“choose an option”**, priority changes revert, or a P0/P1/P2 group disappears.

Check the current options:

```bash
gh project field-list 4 --owner lstbob --format json
```

For this project, the original option IDs are:

| Option | ID | Color |
|---|---|---|
| P0 | `79628723` | RED |
| P1 | `0a877460` | ORANGE |
| P2 | `da944a9c` | YELLOW |

> **Note:** These IDs are specific to this project. If the field was recreated, query the current options first and preserve the IDs that still exist.

Restore a deleted option while preserving the others:

```bash
gh api graphql -f query='
mutation {
  updateProjectV2Field(input: {
    fieldId: "PVTSSF_lAHODNbEK84A7AFTzgvbcM0"
    singleSelectOptions: [
      {id: "79628723", name: "P0", color: RED, description: ""},
      {id: "0a877460", name: "P1", color: ORANGE, description: ""},
      {id: "da944a9c", name: "P2", color: YELLOW, description: ""}
    ]
  }) {
    projectV2Field {
      ... on ProjectV2SingleSelectField {
        id
        name
        options { id name color }
      }
    }
  }
}'
```

> **Important:** pass the `id` for every existing option. Omitting an ID can regenerate it and break the items that reference it.

Then reassign any items that lost their value from `sprints/backup-2026-10-29.json`:

```bash
gh project item-edit \
  --project-id PVT_kwHODNbEK84A7AFT \
  --id <project-item-id> \
  --field-id PVTSSF_lAHODNbEK84A7AFTzgvbcM0 \
  --single-select-option-id 79628723
```

Find the project item ID with `gh project item-list 4 --owner lstbob --limit 100 --format json` or the GraphQL `items` query.

Use `0a877460` for P1 and `da944a9c` for P2. Verify with:

```bash
./scripts/sprint status
```

### A view is not grouped by Priority

View grouping is stored per view and is **not** controlled by the sprint filter. The API cannot change it (`UpdateProjectV2ViewInput` only exposes `visibleFieldIds`).

In the GitHub UI:

1. Open the view (for example, **Current Sprint**).
2. Open the view menu.
3. Set **Group by** to **Priority**.

The **Next Sprint** view already groups by Priority. The **Current Sprint** view does not by default.

### The alert workflow fails

- Check that `PROJECT_TOKEN` exists and has not expired:
  ```bash
  gh secret list -R lstbob/tsqr-sdlc
  ```
- The PAT needs `project` and `repo` scopes.
- Inspect the run:
  ```bash
  gh run list --workflow sprint-alert.yml --limit 5
  gh run view <run-id> --log
  ```

---

## 14. Reference

### Project and fields

| Item | ID |
|---|---|
| Project | `PVT_kwHODNbEK84A7AFT` |
| Sprint field (`bob-sprint`) | `PVTIF_lAHODNbEK84A7AFTzg29qs4` |
| Priority field | `PVTSSF_lAHODNbEK84A7AFTzgvbcM0` |
| Priority P0 option | `79628723` |
| Priority P1 option | `0a877460` |
| Priority P2 option | `da944a9c` |

### Backups

| File | Contents |
|---|---|
| `sprints/backup-2026-10-29.json` | Pre-reschedule item snapshot, including priorities and sprint assignments |
| `sprints/iterations-backup-*.json` | Iteration configuration written before `extend` changes |

### Scripts

| Script | Purpose |
|---|---|
| `scripts/sprint` | Add, defer, move, rebalance, extend, status, audit |
| `scripts/sprintlib.py` | Shared GraphQL, state, capacity, and iteration helpers |
| `scripts/sprint-alert` | Create/update sprint-end alert issues |
| `.github/workflows/sprint-alert.yml` | Daily/manual sprint-end alert workflow |

### Links

- [Project board](https://github.com/users/lstbob/projects/4)
- [Current Sprint view](https://github.com/users/lstbob/projects/4/views/1)
- [Next Sprint view](https://github.com/users/lstbob/projects/4/views/2)
- [README sprint plan](../README.md)
- [PROCESS.md](../PROCESS.md)
