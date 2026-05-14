# Autonomy Completion Contract

## Purpose

This contract makes the workflow idea-only and hands-off by default. The user supplies an idea. The agent system must audit and correct that idea when needed, infer requirements, choose a plan, execute, review, retry, and report without routine human decisions.

## Non-negotiable rule

Do not ask the user for normal product, requirements, UX, architecture, naming, implementation, prioritization, review, or scope decisions. Route uncertainty to `decision_maker`, record the assumption or tradeoff in `decisions.jsonl`, and continue.

## Hard external boundary

Human input is allowed only when the next action requires one of these external conditions and no bounded substitute exists:

1. Missing credentials, account access, paid service access, or private API keys.
2. Irreversible destructive operation such as deleting production data, force-pushing shared history, or making external purchases.
3. Safety, legal, privacy, or policy-sensitive action.
4. A platform permission that the agent cannot obtain or simulate.

Even then, first attempt a bounded substitute: mock/stub the integration, use local persistence, reduce scope to a verifiable vertical slice, or archive the blocked path with a decision record and continue remaining tasks.

## Autonomous default ladder

When information is missing, apply this ladder before stopping:

1. Infer from the user's idea and immediate context.
2. Inspect repository or existing project conventions.
3. Use common product and engineering defaults.
4. Choose the smallest complete vertical slice.
5. Prefer reversible and testable choices.
6. Use local-only substitutes for missing external systems.
7. Record assumptions and continue.

## Requirements audit loop

Before creating product, UX, architecture, or implementation tasks, create `requirements_audit.md`. Audit the raw idea, detect errors or hidden traps, write the corrected requirement, log assumptions, and continue. If the user provided a clear and coherent idea, still record the audit and state that no correction is needed.

The requirements audit must pass before the specs are accepted. If it is missing or generic, improve it autonomously rather than ask the user.

## Requirements-depth loop

Before creating implementation tasks, the requirements audit, product spec, UX spec, and architecture spec must pass their quality tests. If any spec is weak, incomplete, or generic, the system must improve the spec autonomously rather than ask the user.

A requirements/spec artifact is weak if it does not define:

- raw idea restatement and corrected requirement,
- detected issues or explicit "none" with rationale,
- target user and job-to-be-done,
- core loop and success criteria,
- MVP and explicit non-goals,
- screens, states, and interaction rules,
- data model and persistence,
- verification plan and run instructions.

## Task-quality loop

Before execution, tasks must be spec-backed and reviewable. If a task is too broad, split it. If it lacks acceptance criteria, expected outputs, verification method, or spec references, repair it autonomously.

## Review-and-retry loop

Review rejection is not a stop condition. It is a retry instruction. Return the task to `ready`, execute the required fixes, create a new run, and repeat review until approved, externally blocked, or archived by a logged decision.

## Completion rule

The workflow is complete only when all feasible tasks are terminal and the final report includes:

- final result,
- requirements audit summary and corrected requirement,
- how to run or use it,
- completed/blocked/archived task summary,
- product/UX/architecture summary,
- key decisions and assumptions,
- verification evidence,
- residual risks,
- trace completeness counts and trace file list.
