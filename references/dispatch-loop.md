# Dispatch Loop

## Initialization

When starting a new board:

1. Create `.agent/kanban/` if the environment supports files.
2. Create `board.json` from `assets/BOARD.template.json`.
3. Create `events.jsonl` and `decisions.jsonl` if missing.
4. Register default agents from `assets/AGENT_PROFILES.template.yaml`.
5. Convert the user's idea into a goal, assumptions, success criteria, and initial scope.
6. Run the requirements audit: restate the idea, detect issues, correct the requirement, and log assumptions.
7. Run the requirements gate: requirements audit, product spec, UX spec, and architecture spec.
8. Log initial assumptions and high-impact requirement/product/UX/architecture choices as decision records.
9. Create implementation tasks only after the corrected requirement and specs exist.

## Autonomous polling algorithm

Default single-threaded dispatch:

1. Load board.
2. Validate statuses and dependencies.
3. Verify requirements audit and spec artifacts exist for user-facing or software work; if missing or weak, route to requirements_analyst, product_strategist, ux_designer, and technical_architect before implementation.
4. Promote `todo` tasks whose parents are all `done`.
5. Route ambiguous or blocked tasks to `decision_maker` before asking the user.
6. Decision-maker chooses defaults, creates substitute tasks, reduces scope, or unblocks.
7. Select the highest-priority `ready` task.
8. Claim it by moving it to `running` and creating a run.
9. Dispatch the assigned role.
10. Close the run as one of: `submitted_for_review`, `blocked`, `failed`, `canceled`.
11. Route to review, retry, auto-unblock, or archive flow.
12. Continue until a stop condition is reached.
13. Emit the final result and trace.

## Priority

Recommended priority order:

```text
p0 > p1 > p2 > p3
```

Within the same priority, prefer tasks that unblock the most downstream work, then tasks that protect the core user journey, then tasks with the strongest evidence of user value, then oldest created time.

## Claiming

Claiming a task must:

- change status from `ready` to `running`,
- set `current_agent`,
- create a run record,
- append a `claimed` event,
- include timestamp and actor.

## Heartbeats

For long-running work, append heartbeat events and step logs. In a manual single-agent setting, heartbeat can be a short note after meaningful milestones. Heartbeats help future readers distinguish slow work from stalled work.

## Completion routing

- Implementer success moves `running -> review`.
- Spec review approval moves `review -> quality_review`. Spec review must compare against product, UX, and architecture specs when relevant.
- Spec review rejection moves `review -> ready` with required fixes.
- Quality review approval moves `quality_review -> done` if done gate passes.
- Quality review rejection moves `quality_review -> ready` with required fixes.
- Ambiguous blocked work moves to `decision_maker`, then usually back to `ready`.
- Hard external blockers stay `blocked` with reason, attempted auto-resolution, and substitute work if any.

## Retry behavior

A retry must read:

- latest task body,
- prior run outcomes,
- required fixes,
- blocker notes,
- parent handoffs,
- reviewer comments,
- decision records.

The retry summary must explicitly state what changed relative to the failed or blocked attempt.

## Stop conditions

Stop the loop and report status only when:

- all feasible tasks are `done`, `blocked`, or `archived`,
- only hard external blockers remain after auto-resolution attempts,
- permissions or credentials are missing and no bounded substitute exists,
- an unsafe or irreversible destructive action would be required,
- the platform cannot continue without external input.

Do not stop for normal product, architecture, naming, format, prioritization, implementation, or review decisions. Use the decision-maker role and continue.

## Reporting final state

When stopping after execution, report:

- final result,
- completed tasks,
- blocked tasks and attempted auto-resolution,
- archived tasks and reasons,
- key decisions and assumptions,
- last run summaries,
- changed files and commands,
- verification evidence,
- residual risks.

## Trace discipline

Every dispatch cycle must leave enough record for a future reader to replay the process:

- `claimed` event when a run starts.
- at least one step log before any run closes.
- step log for each command, file edit group, verification attempt, review finding, blocked condition, and handoff.
- event for every status transition.
- decision record for each assumption, tradeoff, prioritization, unblock, or stop decision.
- trace ledger entry for each event, decision, and step when file persistence is available.

If the agent notices it performed a material action without logging, it must immediately append a corrective step log describing the action, evidence, and timestamp of the correction.

## Requirements-depth guardrail

If the output quality is poor or task decomposition feels shallow, the usual cause is a missing or weak requirements gate. Before implementing, inspect whether the board contains a real product spec, UX spec, architecture spec, and spec-backed task graph. If not, stop implementation, create missing specs, log decisions, and regenerate tasks.

For a user idea such as a habit app, learning app, dashboard, workflow tool, or any user-facing project, default to at least these task families: domain model, seed/demo data, primary user flow, persistence, UI states, verification, and usage docs.
