# Execution Trace Contract

This protocol requires a complete, append-only execution trace. The user should be able to reconstruct what happened from the artifact records without relying on chat memory.

## Trace layers

Maintain five trace layers whenever the environment supports persistence:

1. **Task record**: durable current state, owner, objective, acceptance criteria, dependencies, assumptions, and expected outputs.
2. **Run record**: one execution or review attempt by one role. Never overwrite prior attempts.
3. **Step log**: ordered observable steps inside a run. Each meaningful action, command, file edit, inspection, review finding, blocker, and verification attempt must appear here.
4. **Event log**: append-only state transitions and telemetry such as created, promoted, claimed, heartbeat, submitted_for_review, rejected, completed, blocked, unblocked, archived, or decision_logged.
5. **Decision log**: assumptions, tradeoffs, selected path, rejected alternatives, rationale, and affected tasks.

Also maintain a chronological `trace.jsonl` stream when files are available. It mirrors important task, run, event, step, and decision records into one ordered ledger for auditing.

## Mandatory step log schema

Each run step must capture observable process, not hidden chain-of-thought:

```json
{
  "timestamp": "2026-05-13T10:00:00Z",
  "task_id": "T-001",
  "run_id": "R-001-001",
  "actor": "implementer",
  "phase": "inspect|plan|edit|command|verify|review|decision|block|handoff|report",
  "action": "what was done",
  "target": "file, command, task, or subsystem touched",
  "rationale": "brief reason for the action",
  "observation": "what happened or what was found",
  "files_changed": [],
  "commands": [],
  "result": "success|failure|partial|blocked|info",
  "next_step": "what should happen next"
}
```

## Logging rules

- Log before and after material work. At minimum log inspect, plan, each meaningful edit group, each command, each verification attempt, each review outcome, each blocker, and each handoff.
- For long work, add heartbeat or progress steps after meaningful milestones.
- A task cannot be marked `done` unless every successful implementer run and every review run has a summary plus at least one step log.
- A failed or rejected attempt must remain visible. Do not delete, compress away, or rewrite failed runs.
- When a retry occurs, the first step of the new run must reference prior failure or reviewer feedback.
- If no file changed, record that explicitly in the run and step log.
- If verification is impossible, record the exact limitation and the substitute evidence used.
- Do not log secrets, access tokens, private keys, or raw credentials. Record only that such information was required or unavailable.
- Do not include hidden chain-of-thought. Log concise rationale, assumptions, evidence, observations, and decisions.

## Trace completeness gate

Before final reporting, validate:

- every non-triage task has at least one event,
- every running/review/quality_review/done/blocked task has at least one run,
- every run has `started_at`, `ended_at` unless active, `agent`, `outcome`, `summary` or active placeholder, and `step_log`,
- every completed task has implementation, spec review, quality review, evidence, and events,
- every blocked task has blocker reason, unblock condition, and a step explaining attempted resolution,
- every material assumption or tradeoff has a decision record,
- `final_report.md` summarizes task, run, step, event, and decision counts.
