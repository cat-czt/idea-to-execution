---
name: idea-to-execution
description: use this skill when coordinating complex multi-step or multi-agent work through an autonomous durable kanban dispatch protocol. use it when a user gives only an idea and expects the model to infer product requirements, ux flows, architecture, task decomposition, implementation, review, trace logs, and final results without routine human decisions. use it when tasks must be decomposed from strong specs, assigned to default agent roles, persisted across context resets, executed through worker runs, reviewed through product/spec/quality gates, and repeatedly polled until all feasible work is done, blocked by hard external constraints, or archived. suitable for claude code, codex, opencode, hermes-like systems, or single-agent role simulation.
---

# Idea to Execution

## Purpose

Use this skill to turn a user's rough idea into an autonomous, durable agent execution workflow. The user should be able to provide only an idea and receive a usable result plus a complete execution trace. Treat the board as the source of truth, not the chat transcript. Every task must have state, owner role, run history, step logs, decisions, events, and evidence before it can be accepted.

Default behavior is **autonomous product-and-engineering execution**: the model audits and corrects the user-supplied idea, then makes requirements, product, UX, architecture, implementation, review, retry, unblock, and final-acceptance decisions by applying the policy in `references/autonomous-decision-policy.md` and the contract in `references/autonomy-completion-contract.md`. Do not ask the user to choose between normal product or technical options. Make the choice, log the rationale, and continue.

The critical lesson: autonomy does not mean skipping requirements. Before implementation, the system must autonomously audit the supplied idea for contradictions, weak assumptions, missing user value, feasibility traps, and scope errors, then synthesize a corrected product spec, UX spec, and architecture spec from the audited requirement. Bad requirement understanding creates bad tasks and bad code. The dispatch loop is not allowed to create implementation tasks from a vague idea directly.

This skill is portable. Do not assume Hermes-specific SQLite, dashboards, dispatcher daemons, or profile APIs exist. When a platform has native subagents, map roles to native workers. When it does not, simulate roles in one session while preserving role identity in task runs, step logs, events, and decision records.

## First decision: choose the operating mode

Before acting, choose exactly one mode for the current step:

- **Autonomous orchestrator mode**: convert the user's idea into goals, assumptions, success criteria, task graph, default agents, and dispatch policy.
- **Requirements analyst mode**: restate, audit, correct, and normalize the user-supplied idea before product/UX/architecture work begins.
- **Product strategist mode**: infer target users, jobs-to-be-done, product value, MVP scope, non-goals, success metrics, and feature priorities from the audited requirement.
- **UX designer mode**: infer core user journeys, screens, interaction states, empty/error/loading states, copy, and usability requirements.
- **Technical architect mode**: choose the simplest viable architecture, data model, module boundaries, implementation plan, and verification approach.
- **Decision-maker mode**: choose among alternatives, resolve ambiguity, select defaults, unblock tasks, and log decision records.
- **Specifier mode**: turn rough work into executable task specs with product/UX/architecture references, acceptance criteria, and expected outputs.
- **Worker mode**: execute exactly one assigned ready task, record a run, and submit for review or block.
- **Spec reviewer mode**: verify implementation satisfies the product spec, UX spec, architecture spec, task objective, and acceptance criteria.
- **Quality reviewer mode**: verify maintainability, tests, integration risk, product usability, and overbuilding risk.
- **Supervisor mode**: perform final acceptance, archive irrelevant tasks, consolidate trace, and produce the final result.
- **Single-agent fallback mode**: simulate the above roles in one session, but record each simulated role as a separate run, step log actor, event, and decision actor.

Never collapse responsibilities silently. If a platform cannot spawn subagents, preserve role names in every record. Do not stop for a human decision unless the next action hits a hard external boundary: missing credentials or account access, irreversible destructive action, safety/policy-sensitive activity, or platform permission the agent cannot obtain or simulate. Before stopping, attempt a bounded substitute and log the decision.

## Default agent roster

If the user does not specify agents, initialize these roles:

1. `orchestrator` - turns the idea into a durable work program, task graph, dependencies, success criteria, and execution plan. It must not implement code or mark done.
2. `requirements_analyst` - audits the user idea, detects contradictions or product mistakes, rewrites it into a coherent validated requirement, and logs corrections. It must not ask the user for routine clarification.
3. `product_strategist` - expands the audited requirement into product intent, target users, jobs, core value, MVP scope, feature priority, success metrics, and non-goals.
4. `ux_designer` - expands the product spec into user flows, screens, states, interaction rules, content needs, and usability acceptance criteria.
5. `technical_architect` - converts product/UX requirements into the simplest viable architecture, data model, tech choices, integration plan, and test strategy.
6. `decision_maker` - resolves ambiguity, selects defaults, chooses the best path under constraints, and logs decision records. It replaces routine human decision points.
7. `specifier` - promotes `triage` tasks into concrete `todo` or `ready` tasks with objectives, scope, acceptance criteria, expected outputs, dependencies, and risk notes.
8. `implementer` - executes one assigned `ready` task. It may edit files, run commands, submit evidence, or block. It must not final-accept its own work.
9. `spec_reviewer` - checks whether implementation satisfies the task objective, product spec, UX spec, architecture spec, and acceptance criteria.
10. `quality_reviewer` - checks code quality, tests, integration risk, maintainability, product completeness, and overbuilding. It may approve quality or return required fixes.
11. `supervisor` - final-accepts completed work, performs trace consolidation, archives irrelevant tasks, and emits the final report.

Load `references/agent-roles.md` when role boundaries, permissions, or default profiles need to be inspected or adapted.

## Mandatory requirements understanding gate

For any user idea that implies a product, app, feature, workflow, tool, or user-facing experience, run the requirements gate before creating implementation tasks. This is mandatory even in autonomous mode.

Create or maintain these durable artifacts when file persistence is available:

```text
.agent/kanban/requirements_audit.md
.agent/kanban/product_spec.md
.agent/kanban/ux_spec.md
.agent/kanban/architecture_spec.md
```

Minimum requirements artifacts:

- **Requirements audit**: original idea, normalized intent, detected issues, corrected requirement, autonomous assumptions, rejected interpretations, decision IDs, and requirements confidence. If the user idea is already clear, still verify it and record "no correction needed" with reasoning.
- **Product spec**: target user, problem, value proposition, primary use cases, core loop, MVP scope, non-goals, feature priority, success metrics, assumptions, risks.
- **UX spec**: user journeys, screens/pages, components, states, empty/error/loading states, form rules, interaction details, content/copy, accessibility basics.
- **Architecture spec**: stack choice, module boundaries, data model, storage, API/service design, state management, test plan, setup/run instructions, extension points.

Do not create implementation tasks directly from the raw idea, even if the idea looks clear. First run a requirements audit, correct any flawed or underspecified demand, then convert the audited requirement into specs using model judgment and logged assumptions. Then decompose tasks from the specs. For example, "daily English phrase practice check-in project" is not one task; it implies onboarding/default data, phrase practice flow, daily streak/check-in logic, progress storage, review history, UI states, reminders or substitutes, tests, and usage documentation.

Load `references/requirements-audit.md` and `references/requirements-discovery.md` before decomposing or implementing any idea, including clear-looking user-facing ideas.

## Autonomous decision policy

Default autonomy level: `autonomous_best_effort`.

Rules:

- If the user provides only an idea, first audit and normalize the idea, then infer the product goal, target users, constraints, assumptions, MVP scope, UX flow, architecture, success criteria, and initial task graph.
- If information is missing but a reasonable default exists, choose the default and log it as an assumption.
- If multiple product or implementation paths exist, score them using user value, feasibility, speed, reversibility, maintainability, verification confidence, and risk. Pick the highest-scoring option.
- If a task is blocked by ambiguity, route it to `decision_maker`, not the human.
- If a task is blocked by missing credentials, unavailable external systems, unsafe action, or irreversible destructive operation, create a bounded substitute task when possible and log the limitation.
- Do not claim mathematical global optimality. Use evidence-weighted best effort under available context.

Load `references/autonomous-decision-policy.md` whenever a decision, default, tradeoff, unblock, or architecture choice is needed. Load `references/autonomy-completion-contract.md` before deciding to ask the user, stop, block, archive, or final-report.

## Persistence layout

When the environment allows file writes, use this portable layout:

```text
.agent/kanban/
  board.json
  requirements_audit.md
  product_spec.md
  ux_spec.md
  architecture_spec.md
  events.jsonl
  decisions.jsonl
  trace.jsonl
  final_report.md
  tasks/
  runs/
```

Use templates in `assets/` to initialize these files. Use `scripts/kanban_dispatch.py` when local file manipulation is available; otherwise maintain the same logical fields in the conversation or platform-native state. `trace.jsonl` is the chronological audit ledger and should receive mirrored records for task creation, claim, step logs, decisions, reviews, blocking, completion, and final reporting.

## Status machine

Use these statuses:

```text
triage -> todo -> ready -> running -> review -> quality_review -> done
running -> blocked
blocked -> ready          # auto-unblocked by decision_maker when possible
running -> ready          # crash, timeout, reclaimed, or retry
review -> ready           # spec review rejected
quality_review -> ready   # quality review rejected
any -> archived
```

Hard rules:

- The dispatcher must not run `triage` tasks.
- A `triage` task must be specified before it becomes executable.
- Vague product work must pass the requirements gate before implementation tasks are created.
- Every implementation task must reference relevant product, UX, or architecture spec sections.
- The `implementer` may submit a task for review but must not mark it `done`.
- `blocked` must include a blocker reason and an unblock condition.
- Most ambiguous blockers must be resolved by `decision_maker`; do not ask the user by default.
- `done` requires implementer evidence, spec review evidence, and quality review evidence. Do not use review exemptions for user-facing product or coding work.
- `archived` must include why the task is no longer active.

Load `references/protocol.md` and `references/task-run-event-model.md` when creating or validating board state.

## Autonomous dispatch loop

For complex goals, run this loop until a stop condition is reached:

1. Load or initialize the board.
2. Create or update the default agent roster.
3. Convert the user's idea into goal, assumptions, success criteria, and initial scope.
4. Run the requirements understanding gate: product spec, UX spec, and architecture spec.
5. Log all assumptions and high-impact choices in `decisions.jsonl`.
6. Convert specs into a task graph; avoid coarse catch-all tasks.
7. Normalize rough work into `triage` or `todo` tasks.
8. Use `specifier` to create executable tasks with objective, scope, dependencies, acceptance criteria, expected outputs, and spec references.
9. Use `decision_maker` to resolve missing choices and promote executable work.
10. Promote unblocked tasks whose dependencies are satisfied.
11. Pick the highest-priority `ready` task.
12. Claim it as `running` for the assigned agent.
13. Execute one worker run.
14. Record step logs during execution: inspect, plan, edit groups, commands, verification, blocker handling, and handoff.
15. Close the run with summary, files changed, commands, verification, decisions, residual risk, and next agent; then move implementation output to `review`.
16. Run spec review against product spec, UX spec, architecture spec, task objective, and acceptance criteria. If rejected, return to `ready` with required fixes.
17. Run quality review. If rejected, return to `ready` with required fixes.
18. Mark `done` only after all required gates pass.
19. Append an event for every state transition and notable telemetry event.
20. Append a decision record for every assumption, tradeoff, unblock, architecture choice, scope cut, or stop decision.
21. Mirror material events, decisions, and steps into `trace.jsonl` so the full execution history is reconstructable.
22. Continue polling.
23. When finished, emit final result and complete trace.

Stop only when:

- all feasible tasks are terminal (`done`, `blocked`, or `archived`),
- only hard external blockers remain after decision-maker attempted bounded substitutes,
- the requested action is unsafe,
- the next step requires credentials, paid external access, or irreversible destructive permission the agent does not have,
- or the platform cannot continue without external permission.

Do not stop merely because a design, product, architecture, implementation, prioritization, review, naming, styling, data-model, or scope decision is needed. Make the decision and log it. If a blocker is ordinary ambiguity, route it to `decision_maker`, not the human.

Load `references/dispatch-loop.md` for detailed retry, claim, and stop-condition behavior. Load `references/autonomy-completion-contract.md` to verify that no routine human decision gate remains.

## Task decomposition quality rules

Tasks must be small enough for one focused worker run and concrete enough to review. Avoid tasks such as "build the app" or "implement frontend" unless they are decomposed into child tasks.

For user-facing software, default decomposition should include tasks for:

- project setup and runnable baseline,
- product/UX spec artifacts,
- data model and seed/demo data,
- core user flow,
- persistence/state management,
- UI screens and reusable components,
- empty/loading/error/success states,
- validation and edge cases,
- tests or verification,
- documentation and final usage instructions.

Each task must include:

- clear objective,
- referenced spec sections,
- acceptance criteria,
- expected outputs,
- verification method,
- residual risk to watch.

Load `references/requirements-discovery.md` and `references/review-gates.md` before decomposing product work.

## Mandatory execution logging

Every task execution must produce a complete trace. The minimum acceptable record is:

- task event sequence: created/promoted/claimed/submitted/reviewed/completed or blocked,
- one run record per execution or review attempt,
- ordered step logs inside each run for each meaningful action, command, file edit group, verification attempt, review finding, blocker, and handoff,
- decision records for every assumption, tradeoff, architecture choice, UX/product choice, unblock, or stop decision,
- chronological `trace.jsonl` entries that let a reader reconstruct the whole workflow without chat context.

Use `scripts/kanban_dispatch.py step-log` or the same logical record format whenever work happens. If the platform cannot write files, include equivalent trace records in the platform-native plan/log state. Do not mark a task `done` if its run history lacks step logs. Do not hide failed attempts or rejected reviews. Do not log secrets or hidden chain-of-thought; log observable actions, concise rationale, observations, evidence, and next steps.

Load `references/execution-trace-contract.md` before executing, reviewing, validating, or final-reporting any nontrivial task.

## Task, run, event, and decision separation

Keep these objects separate:

- **Task**: the durable work item and current state.
- **Run**: one execution or review attempt by one role.
- **Step log**: ordered observable actions inside a run.
- **Event**: an immutable audit record of a transition or telemetry update.
- **Decision**: a durable record of an assumption, tradeoff, selected path, rejected alternatives, and rationale.
- **Spec artifact**: product/UX/architecture source of truth used to create and review tasks.

Do not hide failed attempts by overwriting the task. A retry must read prior runs and address the recorded failure. Do not hide process by only writing a final answer; every material action must have a step log, and every material decision must be traceable.

## Review gates

A task may enter `done` only when the latest successful implementer run has enough evidence and required reviewers approve it.

Minimum done evidence:

- implementation summary,
- ordered step logs for implementation and reviews,
- changed files or explicit no-file-change explanation,
- commands run or explicit verification limitation,
- verification result,
- residual risk,
- product/UX/architecture spec compliance,
- spec review result,
- quality review result,
- unresolved blocker check,
- decision records for important assumptions and tradeoffs.

Load `references/review-gates.md` when reviewing or final-accepting a task.

## Final output contract

When all feasible work is complete, return only the useful end state plus trace links or summaries. Do not ask for approval before final reporting:

1. **Final result**: what was built, decided, or produced.
2. **How to use it**: commands, files, entry points, or next operational steps.
3. **Requirements audit summary**: original idea, corrected requirement, assumptions, and any issues fixed.
4. **Product scope summary**: target user, MVP scope, main flows, non-goals.
5. **Completion summary**: task counts by status and major deliverables.
6. **Decision log summary**: key decisions, assumptions, rejected alternatives, and why.
7. **Execution trace**: tasks, runs, step counts, commands, verification, changed files, reviewer outcomes, events, and decision IDs.
8. **Residual risk**: what could not be verified or depends on external constraints.

Use `assets/FINAL_REPORT.template.md` when a file-based final report is useful.

## Platform adaptation

- **Hermes-like systems**: map tasks, runs, events, comments, assignees, decisions, and dispatcher behavior to native board primitives.
- **Claude Code**: put this protocol in `CLAUDE.md` or a Claude Skill. Use native subagents or forked contexts when available. Otherwise simulate roles.
- **Codex**: put this protocol in `AGENTS.md`. Use multi-agent spawning if available; otherwise run the single-agent fallback with role-labeled runs and decisions.
- **OpenCode**: put this protocol in project-level agent instructions. Use `.agent/kanban/` as persistent state unless the platform provides a stronger store.

Load `references/portability.md` before adapting the protocol to a specific coding-agent environment.

## Starting template

When the user gives an idea and asks for execution, start with this structure:

```text
Idea: [raw user idea]
Goal: [model-inferred one-sentence goal]
Board: [new or existing]
Mode: autonomous orchestrator
Autonomy: autonomous_best_effort
Default agents: orchestrator, requirements_analyst, product_strategist, ux_designer, technical_architect, decision_maker, specifier, implementer, spec_reviewer, quality_reviewer, supervisor
Persistence: .agent/kanban/
Requirements gate: requirements_audit.md + product_spec.md + ux_spec.md + architecture_spec.md required before implementation tasks
Review policy: spec review + quality review required
Decision policy: make best-effort decisions, log assumptions, do not ask user unless hard external constraints apply
Stop condition: all feasible tasks done, blocked by hard external constraints, or archived
```
