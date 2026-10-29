#!/usr/bin/env python3
"""Shared helpers for the tsqr sprint scheduler.

The project is a user-owned GitHub Project (lstbob/projects/4).  All access
goes through the `gh` CLI, so the caller must be authenticated with the
`project` scope (or have GH_TOKEN set to a PAT with that scope).
"""
from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

OWNER = os.environ.get("SPRINT_OWNER", "lstbob")
PROJECT_NUMBER = int(os.environ.get("SPRINT_PROJECT", "4"))
FIELD_NAME = os.environ.get("SPRINT_FIELD", "bob-sprint")
CAPACITY = int(os.environ.get("SPRINT_CAPACITY", "5"))
ALERT_DAYS = int(os.environ.get("SPRINT_ALERT_DAYS", "2"))
REPO_ROOT = Path(__file__).resolve().parent.parent
BACKUP_DIR = REPO_ROOT / "sprints"

STATE_QUERY = """
query($owner: String!, $number: Int!, $cursor: String) {
  user(login: $owner) {
    projectV2(number: $number) {
      id
      title
      field(name: "%s") {
        ... on ProjectV2IterationField {
          id
          name
          configuration {
            iterations { id title startDate duration }
            completedIterations { id title startDate duration }
          }
        }
      }
      items(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          content {
            ... on Issue {
              number
              title
              state
              url
              repository { nameWithOwner }
              subIssues(first: 1) { totalCount }
            }
          }
          fieldValues(first: 30) {
            nodes {
              ... on ProjectV2ItemFieldIterationValue {
                iterationId
                title
                field { ... on ProjectV2FieldCommon { name } }
              }
              ... on ProjectV2ItemFieldNumberValue {
                number
                field { ... on ProjectV2FieldCommon { name } }
              }
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field { ... on ProjectV2FieldCommon { name } }
              }
            }
          }
        }
      }
    }
  }
}
""" % FIELD_NAME

SET_ITERATION = """
mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $iterationId: String!) {
  updateProjectV2ItemFieldValue(input: {
    projectId: $projectId
    itemId: $itemId
    fieldId: $fieldId
    value: { iterationId: $iterationId }
  }) {
    projectV2Item { id }
  }
}
"""

CLEAR_ITERATION = """
mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!) {
  clearProjectV2ItemFieldValue(input: {
    projectId: $projectId
    itemId: $itemId
    fieldId: $fieldId
  }) {
    projectV2Item { id }
  }
}
"""


def gh(query: str, **variables: Any) -> dict:
    """Run a GraphQL query through gh and return the `data` payload."""
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if value is None:
            cmd += ["-F", f"{key}=null"]
        elif isinstance(value, bool):
            cmd += ["-F", f"{key}={'true' if value else 'false'}"]
        elif isinstance(value, int):
            cmd += ["-F", f"{key}={value}"]
        else:
            cmd += ["-f", f"{key}={value}"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip())
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"Unexpected gh output: {proc.stdout[:500]}")
    if payload.get("errors"):
        raise RuntimeError(json.dumps(payload["errors"], indent=2))
    return payload["data"]


def normalize(node: dict) -> dict:
    content = node.get("content") or {}
    repo = (content.get("repository") or {}).get("nameWithOwner", "")
    number = content.get("number")
    key = f"{repo.split('/')[-1]}#{number}" if repo and number is not None else node["id"]

    estimate = None
    status = None
    priority = None
    iteration = None
    for value in (node.get("fieldValues") or {}).get("nodes", []):
        field = value.get("field") or {}
        name = field.get("name")
        if name == "Estimate(SP)" and value.get("number") is not None:
            estimate = int(value["number"])
        elif name == "Status":
            status = value.get("name")
        elif name == "Priority":
            priority = value.get("name")
        elif name == FIELD_NAME:
            iteration = {
                "id": value.get("iterationId"),
                "title": value.get("title"),
            }

    return {
        "id": node["id"],
        "key": key,
        "repo": repo,
        "number": number,
        "url": content.get("url"),
        "title": content.get("title", ""),
        "state": content.get("state"),
        "estimate": estimate,
        "status": status,
        "priority": priority,
        "iteration": iteration,
        "is_epic": (content.get("subIssues") or {}).get("totalCount", 0) > 0,
    }


def load_state() -> dict:
    nodes: list[dict] = []
    project: dict | None = None
    field: dict | None = None
    cursor = None
    while True:
        data = gh(STATE_QUERY, owner=OWNER, number=PROJECT_NUMBER, cursor=cursor)
        project = data["user"]["projectV2"]
        if field is None:
            field = project.get("field")
        page = project["items"]
        nodes.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]

    if not field:
        raise RuntimeError(f"Iteration field {FIELD_NAME!r} not found on project #{PROJECT_NUMBER}")

    active = sorted(field["configuration"]["iterations"], key=lambda x: x["startDate"])
    completed = sorted(
        field["configuration"]["completedIterations"], key=lambda x: x["startDate"]
    )
    items = [normalize(n) for n in nodes]
    return {
        "project": {"id": project["id"], "title": project["title"]},
        "field": {"id": field["id"], "name": field["name"]},
        "active": active,
        "completed": completed,
        "items": items,
        "by_key": {i["key"]: i for i in items},
        "by_id": {i["id"]: i for i in items},
    }


def sprint_number(title: str | None) -> int | None:
    if not title:
        return None
    try:
        return int(title.split()[-1])
    except (ValueError, IndexError):
        return None


def sprint_title(number: int) -> str:
    return f"Sprint {number}"


def end_date(iteration: dict) -> dt.date:
    return dt.date.fromisoformat(iteration["startDate"]) + dt.timedelta(
        days=int(iteration["duration"]) - 1
    )


def items_in(state: dict, title: str) -> list[dict]:
    return [i for i in state["items"] if (i["iteration"] or {}).get("title") == title]


def sprint_load(state: dict, title: str) -> int:
    return sum((i["estimate"] or 0) for i in items_in(state, title))


def active_by_number(state: dict) -> dict[int, dict]:
    return {sprint_number(i["title"]): i for i in state["active"]}


def iteration_by_title(state: dict, title: str) -> dict | None:
    for iteration in state["active"] + state["completed"]:
        if iteration["title"] == title:
            return iteration
    return None


def capacity_bar(load: int, capacity: int = CAPACITY) -> str:
    if load > capacity:
        return f"[!{load}/{capacity}]"
    return "[" + "=" * load + "-" * (capacity - load) + "]"


def print_status(state: dict, capacity: int = CAPACITY) -> None:
    print(f"Project: {state['project']['title']}  (capacity {capacity} SP/sprint)\n")
    for iteration in state["active"]:
        title = iteration["title"]
        load = sprint_load(state, title)
        items = items_in(state, title)
        flag = "  OVER" if load > capacity else ""
        print(
            f"{title:9} {iteration['startDate']}..{end_date(iteration)}  "
            f"{load:2}/{capacity} SP {capacity_bar(load, capacity)}{flag}"
        )
        for item in sorted(items, key=lambda x: (x["priority"] or "P9", x["key"])):
            est = "?" if item["estimate"] is None else str(item["estimate"])
            print(f"    {est:>2} SP  {item['priority'] or '-':3}  {item['key']:24} {item['title'][:60]}")
        if not items:
            print("    (empty)")

    scheduled = [i for i in state["items"] if i["iteration"]]
    backlog = [i for i in state["items"] if not i["iteration"]]
    print(
        f"\nScheduled: {len(scheduled)} items, {sum((i['estimate'] or 0) for i in scheduled)} SP"
    )
    print(
        f"Backlog:   {len(backlog)} items, {sum((i['estimate'] or 0) for i in backlog)} SP"
    )


def audit(state: dict, capacity: int = CAPACITY) -> list[tuple[str, str]]:
    problems: list[tuple[str, str]] = []

    for item in state["items"]:
        if item["is_epic"] and item["iteration"]:
            problems.append(
                ("error", f"Epic {item['key']} has {item['iteration']['title']}; epics must be unscheduled")
            )
        if item["iteration"] and (item["estimate"] or 0) > capacity:
            problems.append(
                (
                    "error",
                    f"{item['key']} is {item['estimate']} SP (> {capacity}) in {item['iteration']['title']}",
                )
            )
        if item["iteration"] and item["estimate"] is None:
            problems.append(
                ("warn", f"{item['key']} has no estimate (treated as 0 SP) in {item['iteration']['title']}")
            )
        if item["iteration"] and item["status"] == "Done":
            problems.append(
                ("warn", f"{item['key']} is Done but still in {item['iteration']['title']}")
            )

    completed_titles = {i["title"] for i in state["completed"]}
    for item in state["items"]:
        if item["iteration"] and item["iteration"]["title"] in completed_titles:
            problems.append(
                ("warn", f"{item['key']} is in completed {item['iteration']['title']}")
            )

    for iteration in state["active"]:
        load = sprint_load(state, iteration["title"])
        if load > capacity:
            problems.append(
                ("error", f"{iteration['title']} is {load} SP (> {capacity})")
            )

    return problems


def apply_iteration(state: dict, item_id: str, iteration_id: str) -> None:
    gh(
        SET_ITERATION,
        projectId=state["project"]["id"],
        itemId=item_id,
        fieldId=state["field"]["id"],
        iterationId=iteration_id,
    )


def clear_iteration(state: dict, item_id: str) -> None:
    gh(
        CLEAR_ITERATION,
        projectId=state["project"]["id"],
        itemId=item_id,
        fieldId=state["field"]["id"],
    )


def _backup_iterations(state: dict) -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    path = BACKUP_DIR / f"iterations-backup-{stamp}.json"
    payload = {
        "exportedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "project": state["project"],
        "field": state["field"],
        "active": state["active"],
        "completed": state["completed"],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return path


def extend_iterations(count: int, apply: bool = False) -> list[dict]:
    """Append `count` iterations, preserving existing IDs (schema 2026-10-01)."""
    if count < 1:
        return []

    state = load_state()
    if not state["active"]:
        raise RuntimeError("No active iterations to extend")

    last = state["active"][-1]
    next_number = max(sprint_number(i["title"]) or 0 for i in state["active"]) + 1
    start = end_date(last) + dt.timedelta(days=1)
    new: list[dict] = []
    for offset in range(count):
        new.append(
            {
                "title": sprint_title(next_number + offset),
                "startDate": start.isoformat(),
                "duration": int(last["duration"]),
            }
        )
        start += dt.timedelta(days=int(last["duration"]))

    if not apply:
        for iteration in new:
            print(f"  + {iteration['title']}  {iteration['startDate']}  ({iteration['duration']} days)")
        return new

    backup = _backup_iterations(state)
    print(f"  backup: {backup}")

    all_iterations = state["completed"] + state["active"] + new
    all_iterations.sort(key=lambda x: x["startDate"])
    first_start = all_iterations[0]["startDate"]
    duration = int(state["active"][0]["duration"])

    def literal(iteration: dict) -> str:
        parts = []
        if iteration.get("id"):
            parts.append(f"id: {json.dumps(iteration['id'])}")
        parts += [
            f"title: {json.dumps(iteration['title'])}",
            f"startDate: {json.dumps(iteration['startDate'])}",
            f"duration: {int(iteration['duration'])}",
        ]
        return "{" + ", ".join(parts) + "}"

    iterations_literal = ", ".join(literal(i) for i in all_iterations)
    query = f"""
mutation {{
  updateProjectV2Field(input: {{
    fieldId: {json.dumps(state['field']['id'])}
    iterationConfiguration: {{
      startDate: {json.dumps(first_start)}
      duration: {duration}
      iterations: [{iterations_literal}]
    }}
  }}) {{
    projectV2Field {{
      ... on ProjectV2IterationField {{
        id
        configuration {{
          iterations {{ id title startDate duration }}
          completedIterations {{ id title startDate duration }}
        }}
      }}
    }}
  }}
}}
"""
    gh(query)

    after = load_state()
    after_active = {i["id"] for i in after["active"]}
    after_completed = {i["id"] for i in after["completed"]}
    old_active = {i["id"] for i in state["active"]}
    old_completed = {i["id"] for i in state["completed"]}

    if not old_active.issubset(after_active):
        print(
            "  WARNING: existing iteration IDs changed; item assignments may need repair.",
            file=sys.stderr,
        )
    if not old_completed.issubset(after_completed):
        print(
            "  WARNING: completed iteration IDs changed. Restore from the backup if needed.",
            file=sys.stderr,
        )
    print(f"  added {len(new)} iteration(s); active={len(after['active'])}, completed={len(after['completed'])}")
    return new


def ensure_sprints(state: dict, target: int, apply: bool = False) -> dict:
    """Make sure an iteration numbered `target` exists."""
    active = active_by_number(state)
    if not active:
        raise RuntimeError("No active iterations")
    highest = max(active)
    if target <= highest:
        return state
    extend_iterations(target - highest, apply=apply)
    return load_state() if apply else state
