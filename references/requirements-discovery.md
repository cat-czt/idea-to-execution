# Requirements Discovery and Specification Gate

## Purpose

This gate prevents the system from turning any raw idea directly into implementation tasks. A rough idea must first be audited and corrected, then become a product spec, UX spec, and architecture spec. A clear-looking idea must still be checked for contradictions, hidden scope, missing success criteria, and feasibility traps before execution. The model must make reasonable autonomous decisions, record assumptions, and then decompose tasks from those specs.

## Rule

Do not create implementation tasks from the raw idea. First create a requirements audit, then create specification artifacts, then derive tasks from the corrected requirement and specs.

Required artifacts when file persistence is available:

```text
.agent/kanban/requirements_audit.md
.agent/kanban/product_spec.md
.agent/kanban/ux_spec.md
.agent/kanban/architecture_spec.md
```

If file persistence is unavailable, keep equivalent structured records in the platform-native plan or conversation state.


## Requirements analyst output

Create `requirements_audit.md` before `product_spec.md`. The audit must include:

1. Raw user idea.
2. Restated intent.
3. Requirement quality assessment.
4. Detected issues, or `none` with reasoning.
5. Corrected requirement to implement.
6. Rejected interpretations.
7. Autonomous assumptions and linked decision IDs.
8. Handoff notes for product, UX, and architecture specs.

### Requirements audit quality test

Before product/UX/architecture specs are considered valid, the requirements audit must answer:

- What exactly will be built?
- What user value is being preserved?
- What raw idea elements were corrected, narrowed, deferred, or rejected?
- What assumptions did the model make instead of asking the user?
- What risks remain because the user did not provide more detail?

If the user idea is already good, still record the audit and explicitly state why no correction is needed.

## Product strategist output

Create `product_spec.md` with these sections:

1. Product sentence: "Build [product] for [user] so they can [job] and achieve [outcome]."
2. Target users and user contexts.
3. Core problem and why it matters.
4. Jobs-to-be-done.
5. Primary use cases.
6. MVP scope: must-have features only.
7. Non-goals: explicitly excluded features for this iteration.
8. Core loop: the repeated action that makes the product useful.
9. Success metrics and completion criteria.
10. Assumptions and decision IDs.
11. Risks and mitigation.

### Product quality test

Before tasks are created, the product spec must answer:

- Who is this for?
- What does the user do first?
- What does the user do every day or every session?
- What counts as success?
- What is intentionally not being built?
- What data must be created, stored, displayed, and updated?

If any answer is missing, the `product_strategist` or `decision_maker` must fill it with a logged assumption.

## UX designer output

Create `ux_spec.md` with these sections:

1. Main user journey.
2. Screen/page list.
3. Per-screen purpose.
4. Key components.
5. Interaction rules.
6. Empty/loading/error/success states.
7. Input validation and feedback.
8. Microcopy and labels.
9. Accessibility basics.
10. Edge cases.

### UX quality test

Before implementation tasks are created, the UX spec must answer:

- What screens exist?
- What can the user click, type, submit, reset, or view?
- What happens when there is no data?
- What happens after success?
- What happens when an action fails?
- How does the user know progress changed?

## Technical architect output

Create `architecture_spec.md` with these sections:

1. Stack and why it was chosen.
2. Project structure.
3. Data model.
4. State management.
5. Storage/persistence strategy.
6. Core modules/components.
7. APIs or service functions.
8. Test/verification plan.
9. Run instructions.
10. Extension points and non-goals.

### Architecture quality test

Before tasks are created, the architecture spec must answer:

- Where does each product capability live in code?
- What data structures are needed?
- How is state persisted?
- How can the app be run locally?
- What commands verify it?
- What is the smallest vertical slice that proves value?

## Task decomposition from specs

After the requirements audit and specs exist, create implementation tasks from the corrected requirement and spec sections. Do not make one large task for the whole product.

Default decomposition for user-facing apps:

1. Project setup and runnable baseline.
2. Data model and seed/demo data.
3. Core domain logic.
4. Primary screen or page shell.
5. Main user flow.
6. Persistence/state management.
7. Progress/history/stats display.
8. Empty/error/success states.
9. Tests or verification scripts.
10. Documentation and final report.

Each task must contain:

- objective,
- spec references to requirements_audit.md, product_spec.md, ux_spec.md, or architecture_spec.md,
- dependencies,
- acceptance criteria,
- expected outputs,
- verification method,
- residual risk to watch.

## Example: daily English phrase practice check-in project

A vague idea such as "I want to develop a daily English phrase practice check-in project" must be audited and expanded before implementation. A clearer idea such as "Build a daily English phrase practice check-in app with streak tracking and history" must also be audited to confirm scope and defer likely overreach.

Minimum inferred requirements audit:

- Raw idea: daily English phrase practice check-in project.
- Restated intent: build a small habit-forming app for practicing one English phrase per day.
- Detected issues: target user, phrase source, persistence, streak behavior, history, and MVP boundary are not explicit.
- Corrected requirement: build a local-first MVP with seed phrases, today phrase card, practice/check-in action, streak/progress persistence, and history review.
- Rejected interpretations: accounts, cloud sync, AI phrase generation, payments, and notification infrastructure for the first iteration.

Minimum inferred product spec:

- Target user: a learner who wants a short daily habit for English phrases.
- Core loop: open app -> see today's phrase -> read meaning/example -> mark practice/check-in -> streak/progress updates -> review past phrases.
- MVP scope: daily phrase card, example sentence, check-in button, streak/progress, history, local persistence, basic reset/demo data.
- Non-goals: accounts, cloud sync, notifications, payments, AI phrase generation unless explicitly available.
- Success: user can complete a daily practice loop and see progress persist after reload.

Minimum UX spec:

- Home/today page with phrase card and check-in action.
- Progress section with streak and completed count.
- History/review list.
- Empty data state, already checked-in state, reset/demo state.
- Clear labels: "Today's phrase", "Meaning", "Example", "Mark as practiced", "Current streak".

Minimum architecture spec:

- Data model: phrase, dailyPracticeRecord, streakSummary.
- Persistence: localStorage or platform-native equivalent for MVP.
- Core functions: getTodayPhrase, checkInToday, calculateStreak, listHistory.
- Tests/verification: run app, complete check-in, reload, verify persisted progress.

Minimum tasks:

- initialize runnable project baseline,
- define phrase/check-in data model and seed phrases,
- implement streak and check-in domain logic,
- build today phrase UI,
- build progress/history UI,
- add persistence and edge states,
- add verification/tests,
- write usage instructions and final trace.

## Failure patterns to reject

Reject these during review:

- Implementing a generic landing page without the core loop.
- Creating a task named "build app" with no subtasks.
- Building UI before defining data model and daily check-in behavior.
- No persistence for progress when the product requires check-in.
- No empty/already-done/reset states.
- No verification that the user can complete the core loop.
- No requirements audit or product/UX/architecture spec artifacts.
- Product/UX/architecture specs implement the raw idea even after the audit corrected the requirement.
