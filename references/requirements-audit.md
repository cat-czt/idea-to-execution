# Requirements Audit and Correction Gate

## Purpose

This gate prevents two failure modes:

1. Treating a vague idea as enough to implement.
2. Treating a clear-looking user idea as automatically correct.

Every idea must be restated, audited, corrected if needed, and normalized before product, UX, architecture, or implementation tasks are created. The workflow remains autonomous: do not ask the user to resolve normal ambiguity. Fix the requirement using best-effort product judgment, log assumptions, and continue.

## Required artifact

Create `.agent/kanban/requirements_audit.md` when file persistence is available. If persistence is unavailable, maintain the same sections in platform-native state.

Required sections:

1. Raw user idea.
2. Restated intent in one sentence.
3. Requirement quality assessment.
4. Detected issues.
5. Corrected requirement.
6. Rejected interpretations.
7. Autonomous assumptions.
8. Decision records.
9. Requirements confidence.
10. Handoff to product, UX, and architecture specs.

## Audit questions

Before creating specs or tasks, answer these questions:

- Is the user asking for a product, feature, workflow, automation, analysis, or implementation?
- Is the core user value explicit or only implied?
- Does the idea contain contradictory goals?
- Does it imply external systems, accounts, paid services, or credentials?
- Does it overreach beyond an MVP?
- Is the success condition measurable?
- Is the core loop or main workflow clear?
- Are there hidden data, persistence, security, or privacy requirements?
- Are any terms ambiguous enough to cause a bad implementation?
- What is the simplest complete version that preserves the user's intent?

## Correction policy

If the idea is incomplete, contradictory, over-broad, or product-weak, correct it autonomously:

- Preserve the user's likely intent.
- Prefer the smallest complete vertical slice.
- Replace vague claims with concrete behaviors.
- Add missing success criteria, states, and data needs.
- Remove or defer non-essential features.
- Use local/mock substitutes for external dependencies.
- Record all assumptions and rejected interpretations in `decisions.jsonl`.

If the idea is already clear and sound, still write the audit. Use `Detected issues: none` and explain why the idea is coherent enough to proceed. Do not skip the artifact.

## Output template

```markdown
# Requirements Audit

## Raw user idea
[verbatim or faithful paraphrase]

## Restated intent
[one sentence]

## Requirement quality assessment
- Clarity: high|medium|low
- Completeness: high|medium|low
- Risk of misimplementation: high|medium|low
- Confidence: high|medium|low

## Detected issues
- [issue or "none"]

## Corrected requirement
[the requirement the workflow will actually implement]

## Rejected interpretations
- [interpretation] — [why rejected]

## Autonomous assumptions
- [assumption] — [rationale] — [decision id if available]

## Decision records
- [decision id] [question] -> [selected]

## Handoff to specs
- Product spec should focus on: [...]
- UX spec should focus on: [...]
- Architecture spec should focus on: [...]
```

## Examples

### Clear idea

Raw idea: "Build a daily English phrase practice check-in app with streak tracking and history."

Detected issues: none.

Corrected requirement: Build a local-first daily English phrase practice app where a learner can view today's phrase, study meaning and example usage, mark practice complete, see streak and total completions, and review practice history. Defer accounts, cloud sync, notifications, and AI phrase generation.

### Clear-looking but flawed idea

Raw idea: "Build a daily English phrase app with AI-generated phrases, social rankings, notifications, account sync, and payments."

Detected issues:

- Scope is too broad for an autonomous MVP.
- Requires external services, accounts, notifications, and payment setup.
- Core learning loop is buried under platform features.

Corrected requirement: Build a local-first MVP that proves the daily phrase practice loop with seed phrases, check-in, streak, history, and clear extension points for future AI generation, accounts, notifications, and payments.

## Review failure patterns

Reject downstream specs or tasks if:

- They do not reference the corrected requirement.
- They implement the raw idea's flawed scope after the audit corrected it.
- They skip a stated user value, core loop, or success condition.
- They build ornamental UI without the corrected workflow.
- They omit assumptions or rejected interpretations that materially affect implementation.
