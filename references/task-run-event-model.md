# Task, Run, Event, and Decision Model

## Task

A task is a durable work item and current state.

Required fields:

```json
{
  "id": "T-001",
  "title": "short imperative title",
  "status": "ready",
  "priority": "p0|p1|p2|p3",
  "assignee": "implementer",
  "current_agent": "implementer",
  "parent_ids": [],
  "child_ids": [],
  "dependencies": [],
  "objective": "what must become true",
  "acceptance_criteria": [],
  "expected_outputs": [],
  "spec_references": [],
  "verification_method": [],
  "assumptions": [],
  "review_policy": {
    "spec_review_required": true,
    "quality_review_required": true,
    "self_approval_allowed": false
  }
}
```

## Run

A run is one attempt by one role.

```json
{
  "run_id": "R-001-001",
  "task_id": "T-001",
  "agent": "implementer",
  "started_at": "iso-8601",
  "ended_at": "iso-8601 or null",
  "outcome": "active|submitted_for_review|approved|rejected|blocked|failed|canceled",
  "summary": "what happened",
  "changed_files": [],
  "commands": [],
  "verification": [],
  "decisions": [],
  "required_fixes": [],
  "blocked_reason": null,
  "unblock_condition": null,
  "residual_risk": [],
  "next_agent": "spec_reviewer"
}
```

## Event

A step log records ordered observable work inside a run. An event is immutable audit history.

```json
{
  "timestamp": "iso-8601",
  "event": "created|promoted|claimed|submitted_for_review|spec_approved|quality_approved|completed|blocked|unblocked|archived|decision_logged|heartbeat",
  "task_id": "T-001 or null",
  "run_id": "R-001-001 or null",
  "actor": "agent role",
  "summary": "brief event summary",
  "metadata": {}
}
```

## Decision

A decision is a durable reasoning artifact for an assumption, tradeoff, unblock, architecture choice, or stop condition.

```json
{
  "timestamp": "iso-8601",
  "decision_id": "D-001",
  "actor": "decision_maker",
  "scope": "board|T-001|R-001-001",
  "question": "what had to be decided",
  "selected": "chosen option",
  "rejected_options": [],
  "rationale": "why this option was selected",
  "assumptions": [],
  "risk": [],
  "reversibility": "high|medium|low",
  "affected_tasks": []
}
```

## Separation rule

Do not merge these records. Spec artifacts define what should be built. Tasks show current state, runs show attempts, step logs show execution process, events show history, decisions show reasoning, and trace.jsonl shows the chronological ledger. The final report must summarize all of them.

## Spec artifact fields

When a task implements user-facing or software behavior, include `spec_references` pointing to sections in `requirements_audit.md`, `product_spec.md`, `ux_spec.md`, or `architecture_spec.md`. A reviewer must reject implementation tasks with no spec references unless they are pure housekeeping tasks such as repository inspection or final reporting.
