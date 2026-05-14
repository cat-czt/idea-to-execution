# Protocol

## Core abstraction

This skill implements a portable autonomous agent workflow kernel:

```text
idea -> requirements audit -> product spec -> ux spec -> architecture spec -> task graph -> agent dispatch -> runs -> reviews -> done -> final report
```

It is not a UI kanban board. It is a durable work queue with autonomous requirements audit, correction, and synthesis, role-based execution, model-made decisions, traceable evidence, and final reporting.

## Required primitives

- **Board**: persistent project-level state.
- **Requirements audit**: raw idea validation, corrected requirement, rejected interpretations, assumptions, and handoff to specs.
- **Spec artifact**: product, UX, and architecture source of truth derived from the corrected requirement.
- **Task**: durable unit of work with status, owner role, criteria, dependencies, expected outputs, and spec references.
- **Run**: one execution or review attempt by one role.
- **Step log**: ordered observable actions within a run.
- **Event**: immutable status transition or telemetry record.
- **Decision**: logged assumption, tradeoff, selected path, rejected alternatives, and rationale.
- **Agent role**: logical worker identity, even when simulated in one session.
- **Gate**: rule that prevents unsupported completion.

## Default autonomous lifecycle

```text
idea
  -> orchestrator initializes board and success criteria
  -> requirements_analyst audits and corrects the idea
  -> product_strategist creates product spec
  -> ux_designer creates UX spec
  -> technical_architect creates architecture spec
  -> decision_maker resolves ambiguity and logs choices
  -> specifier makes spec-backed tasks executable
  -> implementer executes ready work
  -> spec_reviewer checks spec compliance
  -> quality_reviewer checks quality and verification
  -> supervisor final-accepts and reports trace
```

## Statuses

Use:

```text
triage, todo, ready, running, review, quality_review, blocked, done, archived
```

`blocked` should be rare in autonomous mode. Before blocking, the agent must try assumptions, conventional defaults, bounded substitutes, mocks, scope reduction, and retry. Hard blockers are external access, missing credentials, unsafe actions, or impossible operations with available tools.

## Requirements gate

A user-facing idea cannot move directly into implementation. The board must first contain a requirements audit, product spec, UX spec, and architecture spec, or equivalent logical records. Implementation tasks must be derived from those specs.

Reject task graphs that contain only broad tasks such as:

- build the app,
- implement frontend,
- create backend,
- polish UI,
- test everything.

Instead decompose by feature slice, data model, user flow, state handling, verification, and documentation.

## Human interaction

The user is an idea provider and final result consumer by default. The user is not a decision router. Do not ask the user to resolve routine product, UX, architecture, or implementation ambiguity. Only ask or stop when the next step cannot be safely or honestly performed without external permission or missing access.

## Traceability

The final answer must be traceable back to:

- requirements audit and product/UX/architecture specs,
- task records,
- run summaries,
- step logs,
- event transitions,
- decision records,
- commands and verification,
- reviewer outcomes,
- residual risk.

If the platform lacks file persistence, keep the same logical records in the conversation or platform-native plan state.
