#!/usr/bin/env python3
"""Portable file-backed helper for the idea-to-execution skill.

This script manages a simple `.agent/kanban/` board with tasks in board.json,
runs in runs/<task_id>.jsonl, and events in events.jsonl. It is intentionally
small and dependency-free so it can be copied into coding-agent projects.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_AGENTS = {
    "orchestrator": {},
    "requirements_analyst": {},
    "product_strategist": {},
    "ux_designer": {},
    "technical_architect": {},
    "decision_maker": {},
    "specifier": {},
    "implementer": {},
    "spec_reviewer": {},
    "quality_reviewer": {},
    "supervisor": {},
}

TERMINAL_STATUSES = {"done", "blocked", "archived"}
PRIORITY_RANK = {"p0": 0, "p1": 1, "p2": 2, "p3": 3}
VALID_STATUSES = {
    "triage",
    "todo",
    "ready",
    "running",
    "review",
    "quality_review",
    "blocked",
    "done",
    "archived",
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def board_root(path: str) -> Path:
    return Path(path).resolve()


def board_path(root: Path) -> Path:
    return root / "board.json"


def events_path(root: Path) -> Path:
    return root / "events.jsonl"


def decisions_path(root: Path) -> Path:
    return root / "decisions.jsonl"


def trace_path(root: Path) -> Path:
    return root / "trace.jsonl"


def final_report_path(root: Path) -> Path:
    return root / "final_report.md"


def requirements_audit_path(root: Path) -> Path:
    return root / "requirements_audit.md"


def product_spec_path(root: Path) -> Path:
    return root / "product_spec.md"


def ux_spec_path(root: Path) -> Path:
    return root / "ux_spec.md"


def architecture_spec_path(root: Path) -> Path:
    return root / "architecture_spec.md"


def runs_dir(root: Path) -> Path:
    return root / "runs"


def tasks_dir(root: Path) -> Path:
    return root / "tasks"


def load_board(root: Path) -> Dict[str, Any]:
    path = board_path(root)
    if not path.exists():
        raise SystemExit(f"board not found: {path}; run init first")
    return json.loads(path.read_text())


def save_board(root: Path, board: Dict[str, Any]) -> None:
    board["updated_at"] = now()
    board_path(root).write_text(json.dumps(board, indent=2, sort_keys=True) + "\n")


def append_jsonl(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, sort_keys=True) + "\n")


def append_trace(root: Path, kind: str, task_id: Optional[str], run_id: Optional[str], actor: str, summary: str, metadata: Optional[Dict[str, Any]] = None) -> None:
    append_jsonl(
        trace_path(root),
        {
            "timestamp": now(),
            "kind": kind,
            "task_id": task_id,
            "run_id": run_id,
            "actor": actor,
            "summary": summary,
            "metadata": metadata or {},
        },
    )


def append_event(root: Path, event: str, task_id: Optional[str], actor: str, summary: str, run_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> None:
    record = {
        "timestamp": now(),
        "event": event,
        "task_id": task_id,
        "run_id": run_id,
        "actor": actor,
        "summary": summary,
        "metadata": metadata or {},
    }
    append_jsonl(events_path(root), record)
    append_trace(root, "event", task_id, run_id, actor, f"{event}: {summary}", record)


def next_task_id(board: Dict[str, Any]) -> str:
    nums = []
    for task in board.get("tasks", []):
        tid = str(task.get("id", ""))
        if tid.startswith("T-") and tid[2:].isdigit():
            nums.append(int(tid[2:]))
    return f"T-{(max(nums) + 1) if nums else 1:03d}"


def next_run_id(root: Path, task_id: str) -> str:
    path = runs_dir(root) / f"{task_id}.jsonl"
    count = 0
    if path.exists():
        count = sum(1 for line in path.read_text().splitlines() if line.strip())
    return f"R-{task_id[2:]}-{count + 1:03d}"


def next_decision_id(root: Path) -> str:
    path = decisions_path(root)
    count = 0
    if path.exists():
        count = sum(1 for line in path.read_text().splitlines() if line.strip())
    return f"D-{count + 1:03d}"


def find_task(board: Dict[str, Any], task_id: str) -> Dict[str, Any]:
    for task in board.get("tasks", []):
        if task.get("id") == task_id:
            return task
    raise SystemExit(f"task not found: {task_id}")


def parse_list(values: Optional[List[str]]) -> List[str]:
    if not values:
        return []
    result: List[str] = []
    for value in values:
        for item in value.split(","):
            stripped = item.strip()
            if stripped:
                result.append(stripped)
    return result


def init(args: argparse.Namespace) -> None:
    root = board_root(args.board)
    root.mkdir(parents=True, exist_ok=True)
    runs_dir(root).mkdir(exist_ok=True)
    tasks_dir(root).mkdir(exist_ok=True)
    events_path(root).touch(exist_ok=True)
    decisions_path(root).touch(exist_ok=True)
    trace_path(root).touch(exist_ok=True)
    requirements_audit_path(root).touch(exist_ok=True)
    product_spec_path(root).touch(exist_ok=True)
    ux_spec_path(root).touch(exist_ok=True)
    architecture_spec_path(root).touch(exist_ok=True)
    if board_path(root).exists() and not args.force:
        print(f"board already exists: {board_path(root)}")
        return
    ts = now()
    board = {
        "version": 5,
        "name": args.name,
        "idea": args.idea or args.goal or "",
        "goal": args.goal or "",
        "autonomy_level": "autonomous_best_effort",
        "created_at": ts,
        "updated_at": ts,
        "agents": DEFAULT_AGENTS,
        "spec_artifacts": {
            "requirements_audit": "requirements_audit.md",
            "product_spec": "product_spec.md",
            "ux_spec": "ux_spec.md",
            "architecture_spec": "architecture_spec.md",
            "requirements_gate_status": "required",
        },
        "logging_policy": {
            "require_step_logs": True,
            "mirror_to_trace_jsonl": True,
            "secret_logging": "forbidden",
        },
        "dispatch_policy": {
            "execution_mode": "sequential",
            "autonomy_level": "autonomous_best_effort",
            "requirements_gate_required": True,
            "review_required_for_done": True,
            "self_approval_allowed": False,
            "auto_continue": True,
            "ask_user_by_default": False,
            "stop_conditions": [
                "all_feasible_tasks_terminal",
                "hard_external_blocker_after_auto_resolution",
                "unsafe_operation",
                "missing_required_permission_or_credentials",
            ],
        },
        "success_criteria": [],
        "assumptions": [],
        "tasks": [],
    }
    save_board(root, board)
    append_event(root, "board_initialized", None, "supervisor", f"board initialized: {args.name}")
    if args.idea or args.goal:
        decision = {
            "timestamp": now(),
            "decision_id": next_decision_id(root),
            "actor": "orchestrator",
            "scope": "board",
            "question": "initial goal interpretation",
            "selected": args.goal or args.idea or "",
            "rejected_options": [],
            "rationale": "initialized autonomous board from the user's supplied idea or goal",
            "assumptions": parse_list(args.assumption),
            "risk": [],
            "reversibility": "high",
            "affected_tasks": [],
        }
        append_jsonl(decisions_path(root), decision)
        append_trace(root, "decision", None, None, "orchestrator", decision["question"], decision)
        append_event(root, "decision_logged", None, "orchestrator", decision["question"], None, {"decision_id": decision["decision_id"]})
    print(f"initialized board at {root}")


def add_task(args: argparse.Namespace) -> None:
    root = board_root(args.board)
    board = load_board(root)
    if args.status not in VALID_STATUSES:
        raise SystemExit(f"invalid status: {args.status}")
    task_id = next_task_id(board)
    ts = now()
    task = {
        "id": task_id,
        "title": args.title,
        "body": args.body or "",
        "status": args.status,
        "priority": args.priority,
        "assignee": args.assignee,
        "current_agent": None,
        "tenant": args.tenant,
        "parent_ids": parse_list(args.parent),
        "child_ids": [],
        "dependencies": parse_list(args.dependency),
        "objective": args.objective or args.title,
        "assumptions": parse_list(args.assumption),
        "acceptance_criteria": parse_list(args.criteria),
        "expected_outputs": parse_list(args.output),
        "spec_references": parse_list(args.spec_ref),
        "verification_method": parse_list(args.verify),
        "review_policy": {
            "spec_review_required": not args.no_spec_review,
            "quality_review_required": not args.no_quality_review,
            "self_approval_allowed": False,
        },
        "created_at": ts,
        "updated_at": ts,
    }
    board["tasks"].append(task)
    # Populate child links for any parents already present.
    for parent_id in task["parent_ids"]:
        try:
            parent = find_task(board, parent_id)
            if task_id not in parent.setdefault("child_ids", []):
                parent["child_ids"].append(task_id)
        except SystemExit:
            pass
    save_board(root, board)
    append_event(root, "created", task_id, "orchestrator", f"created task: {args.title}")
    print(json.dumps(task, indent=2, sort_keys=True))


def list_tasks(args: argparse.Namespace) -> None:
    board = load_board(board_root(args.board))
    tasks = board.get("tasks", [])
    if args.status:
        tasks = [task for task in tasks if task.get("status") == args.status]
    for task in tasks:
        print(f"{task['id']} [{task['priority']}] {task['status']} -> {task['assignee']}: {task['title']}")


def parents_done(board: Dict[str, Any], task: Dict[str, Any]) -> bool:
    for parent_id in task.get("parent_ids", []):
        parent = find_task(board, parent_id)
        if parent.get("status") != "done":
            return False
    return True


def promote(args: argparse.Namespace) -> None:
    root = board_root(args.board)
    board = load_board(root)
    promoted = []
    for task in board.get("tasks", []):
        if task.get("status") == "todo" and parents_done(board, task):
            task["status"] = "ready"
            task["updated_at"] = now()
            promoted.append(task["id"])
            append_event(root, "promoted", task["id"], "dispatcher", "dependencies satisfied; task promoted to ready")
    save_board(root, board)
    print(json.dumps({"promoted": promoted}, indent=2))


def next_ready(args: argparse.Namespace) -> None:
    root = board_root(args.board)
    board = load_board(root)
    ready = [task for task in board.get("tasks", []) if task.get("status") == "ready" and parents_done(board, task)]
    ready.sort(key=lambda task: (PRIORITY_RANK.get(task.get("priority", "p3"), 99), task.get("created_at", "")))
    if not ready:
        print("no ready task")
        return
    task = ready[0]
    if args.claim:
        run_id = claim_task(root, board, task["id"], args.actor or task.get("assignee") or "implementer")
        task = find_task(board, task["id"])
        task["active_run_id"] = run_id
        save_board(root, board)
    print(json.dumps(task, indent=2, sort_keys=True))


def claim_task(root: Path, board: Dict[str, Any], task_id: str, actor: str) -> str:
    task = find_task(board, task_id)
    if task.get("status") != "ready":
        raise SystemExit(f"task {task_id} is not ready; current status: {task.get('status')}")
    run_id = next_run_id(root, task_id)
    ts = now()
    task["status"] = "running"
    task["current_agent"] = actor
    task["active_run_id"] = run_id
    task["updated_at"] = ts
    run = {
        "run_id": run_id,
        "task_id": task_id,
        "agent": actor,
        "started_at": ts,
        "ended_at": None,
        "outcome": "active",
        "summary": "",
        "changed_files": [],
        "commands": [],
        "verification": [],
        "step_log": [
            {
                "timestamp": ts,
                "actor": actor,
                "phase": "inspect",
                "action": "claimed task and loaded task context",
                "target": task_id,
                "rationale": "start an auditable execution attempt",
                "observation": "task status changed from ready to running",
                "files_changed": [],
                "commands": [],
                "result": "info",
                "next_step": "execute assigned task",
            }
        ],
        "decisions": [],
        "required_fixes": [],
        "blocked_reason": None,
        "unblock_condition": None,
        "residual_risk": [],
        "next_agent": None,
    }
    append_jsonl(runs_dir(root) / f"{task_id}.jsonl", run)
    append_event(root, "claimed", task_id, actor, "task claimed", run_id)
    return run_id


def claim(args: argparse.Namespace) -> None:
    root = board_root(args.board)
    board = load_board(root)
    run_id = claim_task(root, board, args.task, args.actor)
    save_board(root, board)
    print(json.dumps({"task_id": args.task, "run_id": run_id, "actor": args.actor}, indent=2))


def read_runs(root: Path, task_id: str) -> List[Dict[str, Any]]:
    path = runs_dir(root) / f"{task_id}.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def write_runs(root: Path, task_id: str, runs: List[Dict[str, Any]]) -> None:
    path = runs_dir(root) / f"{task_id}.jsonl"
    path.write_text("".join(json.dumps(run, sort_keys=True) + "\n" for run in runs))


def update_latest_run(root: Path, task_id: str, patch: Dict[str, Any]) -> Dict[str, Any]:
    runs = read_runs(root, task_id)
    if not runs:
        raise SystemExit(f"no runs for task: {task_id}")
    runs[-1].update(patch)
    write_runs(root, task_id, runs)
    return runs[-1]


def append_run_step(root: Path, task_id: str, step: Dict[str, Any]) -> Dict[str, Any]:
    runs = read_runs(root, task_id)
    if not runs:
        raise SystemExit(f"no runs for task: {task_id}")
    run = runs[-1]
    run.setdefault("step_log", []).append(step)
    # Keep aggregate fields useful for quick reporting.
    for key in ("files_changed", "commands"):
        for item in step.get(key, []) or []:
            if item and item not in run.setdefault(key, []):
                run[key].append(item)
    write_runs(root, task_id, runs)
    append_trace(root, "step", task_id, run.get("run_id"), step.get("actor", "unknown"), step.get("action", "step logged"), step)
    return run


def step_log(args: argparse.Namespace) -> None:
    root = board_root(args.board)
    board = load_board(root)
    task = find_task(board, args.task)
    step = {
        "timestamp": now(),
        "actor": args.actor,
        "phase": args.phase,
        "action": args.action,
        "target": args.target or args.task,
        "rationale": args.rationale or "maintain auditable task execution trace",
        "observation": args.observation,
        "files_changed": parse_list(args.file),
        "commands": parse_list(args.command),
        "result": args.result,
        "next_step": args.next_step or "continue dispatch loop",
    }
    run = append_run_step(root, args.task, step)
    task["updated_at"] = now()
    save_board(root, board)
    append_event(root, "step_logged", args.task, args.actor, args.action, run.get("run_id"), {"phase": args.phase, "result": args.result})
    print(json.dumps({"run_id": run.get("run_id"), "step": step}, indent=2, sort_keys=True))


def submit(args: argparse.Namespace) -> None:
    root = board_root(args.board)
    board = load_board(root)
    task = find_task(board, args.task)
    if task.get("status") != "running":
        raise SystemExit(f"task {args.task} must be running to submit; current status: {task.get('status')}")
    append_run_step(root, args.task, {
        "timestamp": now(),
        "actor": args.actor,
        "phase": "handoff",
        "action": "submitted task for spec review",
        "target": args.task,
        "rationale": "implementation attempt is ready for review gate",
        "observation": args.summary,
        "files_changed": parse_list(args.file),
        "commands": parse_list(args.command),
        "result": "success",
        "next_step": "spec review",
    })
    run = update_latest_run(
        root,
        args.task,
        {
            "ended_at": now(),
            "outcome": "submitted_for_review",
            "summary": args.summary,
            "changed_files": parse_list(args.file),
            "commands": parse_list(args.command),
            "verification": parse_list(args.verification),
            "decisions": parse_list(args.decision),
            "residual_risk": parse_list(args.risk),
            "next_agent": "spec_reviewer",
        },
    )
    task["status"] = "review"
    task["current_agent"] = "spec_reviewer"
    task.pop("active_run_id", None)
    task["updated_at"] = now()
    save_board(root, board)
    append_event(root, "submitted_for_review", args.task, args.actor, args.summary, run["run_id"])
    print(json.dumps(run, indent=2, sort_keys=True))


def block(args: argparse.Namespace) -> None:
    root = board_root(args.board)
    board = load_board(root)
    task = find_task(board, args.task)
    if task.get("status") not in {"running", "ready", "review", "quality_review"}:
        raise SystemExit(f"cannot block task from status: {task.get('status')}")
    run_id = task.get("active_run_id")
    if run_id:
        append_run_step(root, args.task, {
            "timestamp": now(),
            "actor": args.actor,
            "phase": "block",
            "action": "blocked task",
            "target": args.task,
            "rationale": "execution cannot continue without unblock condition",
            "observation": args.reason,
            "files_changed": [],
            "commands": [],
            "result": "blocked",
            "next_step": args.unblock_condition,
        })
        update_latest_run(
            root,
            args.task,
            {
                "ended_at": now(),
                "outcome": "blocked",
                "summary": args.reason,
                "blocked_reason": args.reason,
                "unblock_condition": args.unblock_condition,
                "next_agent": "supervisor",
            },
        )
    task["status"] = "blocked"
    task["current_agent"] = "supervisor"
    task.pop("active_run_id", None)
    task["blocked_reason"] = args.reason
    task["unblock_condition"] = args.unblock_condition
    task["updated_at"] = now()
    save_board(root, board)
    append_event(root, "blocked", args.task, args.actor, args.reason, run_id, {"unblock_condition": args.unblock_condition})
    print(json.dumps(task, indent=2, sort_keys=True))


def unblock(args: argparse.Namespace) -> None:
    root = board_root(args.board)
    board = load_board(root)
    task = find_task(board, args.task)
    if task.get("status") != "blocked":
        raise SystemExit(f"task {args.task} is not blocked")
    task["status"] = "ready"
    task["current_agent"] = task.get("assignee", "implementer")
    task.pop("blocked_reason", None)
    task.pop("unblock_condition", None)
    task["updated_at"] = now()
    save_board(root, board)
    append_event(root, "unblocked", args.task, args.actor, args.reason or "task unblocked")
    print(json.dumps(task, indent=2, sort_keys=True))


def review(args: argparse.Namespace, quality: bool) -> None:
    root = board_root(args.board)
    board = load_board(root)
    task = find_task(board, args.task)
    expected = "quality_review" if quality else "review"
    if task.get("status") != expected:
        raise SystemExit(f"task {args.task} must be in {expected}; current status: {task.get('status')}")
    agent = "quality_reviewer" if quality else "spec_reviewer"
    run_id = next_run_id(root, args.task)
    event_prefix = "quality" if quality else "spec"
    ts = now()
    outcome = "approved" if args.approve else "rejected"
    run = {
        "run_id": run_id,
        "task_id": args.task,
        "agent": agent,
        "started_at": ts,
        "ended_at": ts,
        "outcome": outcome,
        "summary": args.summary,
        "changed_files": [],
        "commands": [],
        "verification": parse_list(args.evidence),
        "step_log": [
            {
                "timestamp": ts,
                "actor": agent,
                "phase": "review",
                "action": "reviewed task evidence",
                "target": args.task,
                "rationale": "apply review gate before completion",
                "observation": args.summary,
                "files_changed": [],
                "commands": [],
                "result": "success" if args.approve else "failure",
                "next_step": "supervisor final trace consolidation" if args.approve and quality else ("quality review" if args.approve else "return to implementer"),
            }
        ],
        "decisions": [],
        "required_fixes": parse_list(args.fix),
        "blocked_reason": None,
        "unblock_condition": None,
        "residual_risk": parse_list(args.risk),
        "next_agent": None,
    }
    if args.approve:
        if quality:
            task["status"] = "done"
            task["current_agent"] = "supervisor"
            event = "completed"
            run["next_agent"] = "supervisor"
        else:
            task["status"] = "quality_review"
            task["current_agent"] = "quality_reviewer"
            event = "spec_approved"
            run["next_agent"] = "quality_reviewer"
    else:
        task["status"] = "ready"
        task["current_agent"] = "implementer"
        event = f"{event_prefix}_rejected"
        run["next_agent"] = "implementer"
    append_jsonl(runs_dir(root) / f"{args.task}.jsonl", run)
    task["updated_at"] = now()
    save_board(root, board)
    append_event(root, event, args.task, agent, args.summary, run_id, {"required_fixes": run["required_fixes"]})
    print(json.dumps({"task": task, "run": run}, indent=2, sort_keys=True))


def decide(args: argparse.Namespace) -> None:
    root = board_root(args.board)
    board = load_board(root)
    affected = parse_list(args.task)
    decision = {
        "timestamp": now(),
        "decision_id": next_decision_id(root),
        "actor": args.actor,
        "scope": args.scope,
        "question": args.question,
        "selected": args.selected,
        "rejected_options": parse_list(args.rejected),
        "rationale": args.rationale,
        "assumptions": parse_list(args.assumption),
        "risk": parse_list(args.risk),
        "reversibility": args.reversibility,
        "affected_tasks": affected,
    }
    append_jsonl(decisions_path(root), decision)
    append_trace(root, "decision", affected[0] if affected else None, None, args.actor, args.question, decision)
    for task_id in affected:
        try:
            task = find_task(board, task_id)
            task.setdefault("decision_ids", []).append(decision["decision_id"])
            task["updated_at"] = now()
        except SystemExit:
            pass
    save_board(root, board)
    append_event(root, "decision_logged", affected[0] if affected else None, args.actor, args.question, None, {"decision_id": decision["decision_id"]})
    print(json.dumps(decision, indent=2, sort_keys=True))


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]




def text_has_all(path: Path, required: List[str]) -> List[str]:
    if not path.exists():
        return [f"missing file: {path.name}"]
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    missing = []
    for item in required:
        if item.lower() not in text:
            missing.append(item)
    return missing


def validate_spec_quality(root: Path) -> List[str]:
    errors: List[str] = []
    spec_checks = [
        (requirements_audit_path(root), [
            "raw user idea", "restated intent", "detected", "corrected requirement", "assumption", "confidence"
        ]),
        (product_spec_path(root), [
            "target", "problem", "mvp", "non-goal", "core loop", "success", "assumption", "risk"
        ]),
        (ux_spec_path(root), [
            "journey", "screen", "state", "empty", "error", "success", "interaction"
        ]),
        (architecture_spec_path(root), [
            "stack", "data model", "persistence", "state", "test", "run"
        ]),
    ]
    for path, required in spec_checks:
        missing = text_has_all(path, required)
        if missing:
            errors.append(f"requirements gate: {path.name} missing required concepts: {', '.join(missing)}")
    return errors

def report(args: argparse.Namespace) -> None:
    root = board_root(args.board)
    board = load_board(root)
    events = read_jsonl(events_path(root))
    decisions = read_jsonl(decisions_path(root))
    trace = read_jsonl(trace_path(root))
    counts: Dict[str, int] = {status: 0 for status in sorted(VALID_STATUSES)}
    lines: List[str] = []
    for task in board.get("tasks", []):
        counts[task.get("status", "unknown")] = counts.get(task.get("status", "unknown"), 0) + 1
    lines.append("# Final Report")
    lines.append("")
    lines.append("## Final result")
    lines.append("")
    lines.append(args.result or board.get("goal") or board.get("idea") or "Autonomous kanban execution completed.")
    lines.append("")
    lines.append("## Completion summary")
    lines.append("")
    for status_name in sorted(counts):
        if counts[status_name]:
            lines.append(f"- {status_name}: {counts[status_name]}")
    lines.append("")
    lines.append("## Tasks")
    lines.append("")
    total_runs = 0
    total_steps = 0
    for task in board.get("tasks", []):
        runs = read_runs(root, task.get("id"))
        step_count = sum(len(run.get("step_log", [])) for run in runs)
        total_runs += len(runs)
        total_steps += step_count
        lines.append(f"- {task.get('id')} [{task.get('status')}] {task.get('title')} - runs: {len(runs)}, steps: {step_count}")
    lines.append("")
    lines.append("## Trace completeness")
    lines.append("")
    lines.append(f"- tasks: {len(board.get('tasks', []))}")
    lines.append(f"- runs: {total_runs}")
    lines.append(f"- run steps: {total_steps}")
    lines.append(f"- events: {len(events)}")
    lines.append(f"- decisions: {len(decisions)}")
    lines.append(f"- trace entries: {len(trace)}")
    lines.append("")
    lines.append("## Key decisions")
    lines.append("")
    for dec in decisions[-20:]:
        lines.append(f"- {dec.get('decision_id')}: {dec.get('selected')} - {dec.get('rationale')}")
    lines.append("")
    lines.append("## Recent events")
    lines.append("")
    for event in events[-30:]:
        lines.append(f"- {event.get('timestamp')} {event.get('event')} {event.get('task_id') or ''}: {event.get('summary')}")
    lines.append("")
    lines.append("## Trace files")
    lines.append("")
    lines.append("- board.json")
    lines.append("- requirements_audit.md")
    lines.append("- product_spec.md")
    lines.append("- ux_spec.md")
    lines.append("- architecture_spec.md")
    lines.append("- events.jsonl")
    lines.append("- decisions.jsonl")
    lines.append("- trace.jsonl")
    lines.append("- runs/")
    final_report_path(root).write_text("\n".join(lines) + "\n")
    append_trace(root, "report", None, None, "supervisor", "final report generated", {"path": str(final_report_path(root)), "tasks": len(board.get("tasks", [])), "runs": total_runs, "steps": total_steps})
    print(str(final_report_path(root)))


def status(args: argparse.Namespace) -> None:
    root = board_root(args.board)
    board = load_board(root)
    counts: Dict[str, int] = {status: 0 for status in sorted(VALID_STATUSES)}
    for task in board.get("tasks", []):
        counts[task.get("status", "unknown")] = counts.get(task.get("status", "unknown"), 0) + 1
    non_terminal = [task for task in board.get("tasks", []) if task.get("status") not in TERMINAL_STATUSES]
    print(json.dumps({"counts": counts, "non_terminal": [task["id"] for task in non_terminal]}, indent=2, sort_keys=True))


def validate(args: argparse.Namespace) -> None:
    root = board_root(args.board)
    board = load_board(root)
    errors: List[str] = []
    seen = set()
    if board.get("dispatch_policy", {}).get("requirements_gate_required") and board.get("tasks"):
        if not requirements_audit_path(root).read_text().strip():
            errors.append("requirements gate: requirements_audit.md is empty")
        if not product_spec_path(root).read_text().strip():
            errors.append("requirements gate: product_spec.md is empty")
        if not ux_spec_path(root).read_text().strip():
            errors.append("requirements gate: ux_spec.md is empty")
        if not architecture_spec_path(root).read_text().strip():
            errors.append("requirements gate: architecture_spec.md is empty")
        if not errors:
            errors.extend(validate_spec_quality(root))
    for task in board.get("tasks", []):
        tid = task.get("id")
        if not tid:
            errors.append("task missing id")
            continue
        if tid in seen:
            errors.append(f"duplicate task id: {tid}")
        seen.add(tid)
        if task.get("status") not in VALID_STATUSES:
            errors.append(f"{tid}: invalid status {task.get('status')}")
        is_executable = task.get("assignee") in {"implementer", "specifier", "spec_reviewer", "quality_reviewer"} or task.get("status") in {"todo", "ready", "running", "review", "quality_review", "done"}
        if is_executable:
            if not task.get("acceptance_criteria"):
                errors.append(f"{tid}: executable task missing acceptance criteria")
            if not task.get("expected_outputs"):
                errors.append(f"{tid}: executable task missing expected outputs")
            if not task.get("verification_method"):
                errors.append(f"{tid}: executable task missing verification method")
            if board.get("dispatch_policy", {}).get("requirements_gate_required") and not task.get("spec_references"):
                errors.append(f"{tid}: executable task missing spec references")
            policy = task.get("review_policy", {})
            if policy.get("self_approval_allowed"):
                errors.append(f"{tid}: self approval is not allowed")
            if policy.get("spec_review_required") is False:
                errors.append(f"{tid}: spec review cannot be disabled for autonomous quality mode")
            if policy.get("quality_review_required") is False:
                errors.append(f"{tid}: quality review cannot be disabled for autonomous quality mode")
        runs = read_runs(root, tid)
        if task.get("status") in {"running", "review", "quality_review", "blocked", "done"} and not runs:
            errors.append(f"{tid}: status {task.get('status')} with no runs")
        for run in runs:
            if "step_log" not in run:
                errors.append(f"{tid}/{run.get('run_id')}: missing step_log")
            elif run.get("outcome") != "active" and not run.get("step_log"):
                errors.append(f"{tid}/{run.get('run_id')}: closed run has empty step_log")
            if run.get("outcome") != "active" and not run.get("summary"):
                errors.append(f"{tid}/{run.get('run_id')}: closed run missing summary")
        if task.get("status") == "done":
            if not task.get("acceptance_criteria"):
                errors.append(f"{tid}: done without acceptance criteria")
            if not task.get("expected_outputs"):
                errors.append(f"{tid}: done without expected outputs")
            if not task.get("verification_method"):
                errors.append(f"{tid}: done without verification method")
            if not runs:
                errors.append(f"{tid}: done with no runs")
            outcomes = [run.get("outcome") for run in runs]
            if "approved" not in outcomes:
                errors.append(f"{tid}: done without approval run")
            if not any(run.get("agent") == "implementer" and run.get("outcome") == "submitted_for_review" for run in runs):
                errors.append(f"{tid}: done without implementer submission run")
            if not any(run.get("agent") == "spec_reviewer" and run.get("outcome") == "approved" for run in runs):
                errors.append(f"{tid}: done without spec reviewer approval")
            if not any(run.get("agent") == "quality_reviewer" and run.get("outcome") == "approved" for run in runs):
                errors.append(f"{tid}: done without quality reviewer approval")
        for parent_id in task.get("parent_ids", []):
            if parent_id not in seen and not any(t.get("id") == parent_id for t in board.get("tasks", [])):
                errors.append(f"{tid}: missing parent {parent_id}")
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, indent=2))
        raise SystemExit(1)
    print(json.dumps({"valid": True, "task_count": len(board.get("tasks", []))}, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Portable idea-to-execution helper")
    parser.add_argument("--board", default=".agent/kanban", help="board directory")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init")
    p.add_argument("--name", default="default")
    p.add_argument("--idea", default="")
    p.add_argument("--goal", default="")
    p.add_argument("--assumption", action="append")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=init)

    p = sub.add_parser("add-task")
    p.add_argument("--title", required=True)
    p.add_argument("--body", default="")
    p.add_argument("--objective", default="")
    p.add_argument("--status", default="triage")
    p.add_argument("--priority", default="p1")
    p.add_argument("--assignee", default="implementer")
    p.add_argument("--tenant", default=None)
    p.add_argument("--parent", action="append")
    p.add_argument("--dependency", action="append")
    p.add_argument("--assumption", action="append")
    p.add_argument("--criteria", action="append")
    p.add_argument("--output", action="append")
    p.add_argument("--spec-ref", action="append", default=[], help="reference to product/ux/architecture spec section")
    p.add_argument("--verify", action="append", default=[], help="verification method for the task")
    p.add_argument("--no-spec-review", action="store_true")
    p.add_argument("--no-quality-review", action="store_true")
    p.set_defaults(func=add_task)

    p = sub.add_parser("list")
    p.add_argument("--status", default=None)
    p.set_defaults(func=list_tasks)

    p = sub.add_parser("promote")
    p.set_defaults(func=promote)

    p = sub.add_parser("next")
    p.add_argument("--claim", action="store_true")
    p.add_argument("--actor", default=None)
    p.set_defaults(func=next_ready)

    p = sub.add_parser("claim")
    p.add_argument("--task", required=True)
    p.add_argument("--actor", default="implementer")
    p.set_defaults(func=claim)

    p = sub.add_parser("step-log")
    p.add_argument("--task", required=True)
    p.add_argument("--actor", default="implementer")
    p.add_argument("--phase", default="info", choices=["inspect", "plan", "edit", "command", "verify", "review", "decision", "block", "handoff", "report", "info"])
    p.add_argument("--action", required=True)
    p.add_argument("--target", default="")
    p.add_argument("--rationale", default="")
    p.add_argument("--observation", default="")
    p.add_argument("--file", action="append")
    p.add_argument("--command", action="append")
    p.add_argument("--result", default="info", choices=["success", "failure", "partial", "blocked", "info"])
    p.add_argument("--next-step", default="")
    p.set_defaults(func=step_log)

    p = sub.add_parser("submit")
    p.add_argument("--task", required=True)
    p.add_argument("--actor", default="implementer")
    p.add_argument("--summary", required=True)
    p.add_argument("--file", action="append")
    p.add_argument("--command", action="append")
    p.add_argument("--verification", action="append")
    p.add_argument("--decision", action="append")
    p.add_argument("--risk", action="append")
    p.set_defaults(func=submit)

    p = sub.add_parser("block")
    p.add_argument("--task", required=True)
    p.add_argument("--actor", default="implementer")
    p.add_argument("--reason", required=True)
    p.add_argument("--unblock-condition", required=True)
    p.set_defaults(func=block)

    p = sub.add_parser("unblock")
    p.add_argument("--task", required=True)
    p.add_argument("--actor", default="supervisor")
    p.add_argument("--reason", default="")
    p.set_defaults(func=unblock)

    p = sub.add_parser("spec-review")
    p.add_argument("--task", required=True)
    p.add_argument("--approve", action="store_true")
    p.add_argument("--summary", required=True)
    p.add_argument("--evidence", action="append")
    p.add_argument("--fix", action="append")
    p.add_argument("--risk", action="append")
    p.set_defaults(func=lambda args: review(args, quality=False))

    p = sub.add_parser("quality-review")
    p.add_argument("--task", required=True)
    p.add_argument("--approve", action="store_true")
    p.add_argument("--summary", required=True)
    p.add_argument("--evidence", action="append")
    p.add_argument("--fix", action="append")
    p.add_argument("--risk", action="append")
    p.set_defaults(func=lambda args: review(args, quality=True))


    p = sub.add_parser("decide")
    p.add_argument("--actor", default="decision_maker")
    p.add_argument("--scope", default="board")
    p.add_argument("--question", required=True)
    p.add_argument("--selected", required=True)
    p.add_argument("--rationale", required=True)
    p.add_argument("--rejected", action="append")
    p.add_argument("--assumption", action="append")
    p.add_argument("--risk", action="append")
    p.add_argument("--reversibility", default="high", choices=["high", "medium", "low"])
    p.add_argument("--task", action="append")
    p.set_defaults(func=decide)

    p = sub.add_parser("report")
    p.add_argument("--result", default="")
    p.set_defaults(func=report)

    p = sub.add_parser("status")
    p.set_defaults(func=status)

    p = sub.add_parser("validate")
    p.set_defaults(func=validate)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
