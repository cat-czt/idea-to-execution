# Review Gates

## Goal

Review gates prevent false completion, shallow requirements, and incomplete trace history. Autonomous execution does not mean self-deception. The model can make decisions, but it must still prove or explain completion.

## Requirements review gate

Before implementation tasks are accepted as ready, verify:

- `requirements_audit.md` or equivalent exists for any raw user idea,
- the requirements audit restates the idea, detects issues or explicitly states none, defines corrected requirement, and records assumptions,
- `product_spec.md` or equivalent exists for user-facing work,
- `ux_spec.md` or equivalent exists for user-facing work,
- `architecture_spec.md` or equivalent exists for software implementation,
- the requirements audit and specs define corrected requirement, core loop, MVP scope, non-goals, data model, screens/states, and verification plan,
- tasks reference relevant spec sections,
- tasks are not broad catch-all items.

If the gate fails, route back to `requirements_analyst`, `product_strategist`, `ux_designer`, `technical_architect`, or `specifier`.

## Spec review gate

The spec reviewer checks:

- implementation matches task objective,
- implementation satisfies the corrected requirement and relevant product spec sections,
- implementation satisfies relevant UX spec sections,
- implementation follows relevant architecture spec sections,
- acceptance criteria are satisfied,
- expected outputs exist,
- no scope item was silently dropped,
- assumptions were logged as decisions,
- deviations are justified.

Reject with concrete required fixes when any criterion is not met.

## Quality review gate

The quality reviewer checks:

- maintainability,
- integration fit,
- tests or verification,
- side effects,
- overbuilding,
- usability completeness for the core flow,
- security or privacy risks,
- residual risks are explicit.

Reject with concrete required fixes when quality is inadequate for the task risk.

## Done gate

A task may be marked `done` only when:

1. implementer submitted summary and evidence,
2. changed files are listed or no-file-change is explained,
3. commands and verification are listed or verification limitation is explained,
4. material decisions and assumptions are logged,
5. requirements audit and product/UX/architecture spec compliance is satisfied for relevant tasks,
6. spec review passed,
7. quality review passed,
8. no unresolved blocker remains,
9. supervisor final-accepted or automatic final acceptance is allowed by policy.

## Autonomous review behavior

Reviewers must not ask the user to judge normal quality or product questions. They should approve, reject, or route to `decision_maker` with a concrete decision question. The decision-maker then chooses a path and returns the task to `ready` or the appropriate review stage.

## Evidence levels

Use the strongest available evidence:

1. Passing tests or command output.
2. Static analysis or type checks.
3. File diff and manual inspection.
4. Generated artifact existence.
5. Reasoned explanation when execution is unavailable.

Lower evidence is acceptable only when higher evidence is impossible with available tools, and the limitation must be recorded.

## Product quality rejection patterns

Reject when:

- a user-facing app lacks a defined core loop,
- progress, persistence, or history is required by the idea but absent,
- screens exist but do not let the user complete the main job,
- UI is merely decorative landing-page content,
- empty/already-done/error/success states are missing for core actions,
- the implementation cannot be run or verified,
- task decomposition skipped requirements audit or product/UX/architecture specs.
- the implementation follows an uncorrected raw idea instead of the corrected requirement.

## Trace review gate

Before approving, reviewers must inspect the run history and reject if:

- the implementer run has no step logs,
- commands or verification are mentioned in the summary but absent from step logs,
- changed files are listed without an edit/action step,
- blocker resolution or assumptions are not linked to decision records,
- the reviewer cannot reconstruct what happened from requirements audit, specs, task, run, event, decision, and trace records.

A reviewer rejection must itself be recorded as a review run with a step log and required fixes.
