# idea-to-execution

English | [简体中文](README_ZH.md)

# [Installation Guide](README_INSTALL_QUICK.md)

## 1. What Is This Skill

`idea-to-execution` is a general-purpose Agent workflow Skill designed for complex task execution.

Its goal is not simply maintaining a to-do list. Instead, it automatically transforms a user-provided idea into a fully executable, auditable, and recoverable multi-Agent workflow:

```text
idea
→ requirements audit
→ product spec
→ UX spec
→ architecture spec
→ task decomposition
→ autonomous decisions
→ execution
→ process logs
→ spec review
→ quality review
→ auto-fix & retry
→ final result + complete audit trail
```

The default behavior is: **the user provides only an idea, and the model autonomously handles all product, technical, architectural, task decomposition, implementation, review, and fix decisions.** The user only needs to review the final result and execution logs.

---

## 2. When to Use This Skill

**Good fits:**

- Starting product, tool, app, script, or feature development from a vague idea.
- Tasks that need to be broken into multiple steps with the Agent driving continuous progress.
- You don't want to be involved in routine product/technical decisions — you just want the final result.
- You need a complete record of how each task was executed, why decisions were made, what changed, and what was verified.
- You want to reuse the same execution protocol across Claude Code, Codex, OpenCode, Hermes-like systems, or single-Agent environments.

**Not a good fit:**

- Single-sentence Q&A.
- Simple translation or rewriting.
- Decisions that require subjective human judgment — branding, legal, financial, or business commitments.
- Tasks that lack accounts, tokens, or external permissions and cannot be substituted with mocks or stubs.
- Tasks where the model is not allowed to make autonomous product or technical judgments.

---

## 3. Core Principles

### 3.1 Autonomous First

The default mode is:

```text
autonomous_best_effort
```

When facing routine choices, the model should **not** ask the user. Instead it should:

1. Infer from the idea and context.
2. Apply industry-standard defaults.
3. Choose the smallest verifiable MVP.
4. Prefer more reversible, lower-risk, easier-to-verify options.
5. Record the decision in `decisions.jsonl`.
6. Continue execution.

### 3.2 Audit Requirements Before Acting

A clearly stated requirement is not necessarily a correct one.

Every idea must first pass through:

```text
requirements_audit.md
```

The Skill checks for:

- Self-contradictory requirements.
- Missing core user loops.
- Scope that is too broad.
- Incorrect assumptions.
- Whether the scope can converge into a more reasonable MVP.
- Whether requirements need automatic correction before proceeding.

Corrected requirements become the foundation for subsequent product, UX, architecture, and task decomposition.

### 3.3 All Execution Must Be Traceable

Tasks cannot execute silently.

Every task must have:

- Task state transitions.
- Run records.
- Step logs.
- Command records.
- File change records.
- Verification records.
- Review records.
- Decision records.
- Trace timeline.

A task without execution logs cannot enter `done`.

### 3.4 The Implementer Cannot Self-Approve

The `implementer` can only submit implementation results.

A task entering `done` must go through:

```text
implementer submission
→ spec_reviewer approval
→ quality_reviewer approval
→ supervisor final acceptance
```

---

## 4. Default Agent Roles

The Skill uses the following roles by default. When the platform supports sub-Agents, they can be dispatched as real agents; otherwise, a single session simulates the roles, but role identity must be preserved in logs.

| Agent | Responsibility |
|---|---|
| `orchestrator` | Converts idea into execution plan, task graph, dependencies, and success criteria |
| `requirements_analyst` | Reviews, corrects, and standardizes user requirements |
| `product_strategist` | Generates product positioning, target users, MVP, success metrics, and non-goals |
| `ux_designer` | Generates user flows, pages, states, interactions, and copy requirements |
| `technical_architect` | Selects tech stack, data models, module boundaries, and verification strategy |
| `decision_maker` | Autonomously makes routine product/technical/architectural/scope decisions and logs rationale |
| `specifier` | Converts coarse tasks into executable task cards |
| `implementer` | Executes a single ready task, logs the process, and submits for review |
| `spec_reviewer` | Verifies that implementation satisfies requirements, specs, and acceptance criteria |
| `quality_reviewer` | Checks quality, maintainability, tests, risks, and over-engineering |
| `supervisor` | Final acceptance, archives irrelevant tasks, produces final report |

---

## 5. Persistent Directory Structure

When the environment allows file writes, the Skill uses the following directory as the task board:

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

Key files:

| File | Purpose |
|---|---|
| `board.json` | Current task pool, task states, dependencies, and role assignments |
| `requirements_audit.md` | Raw requirement review, issue identification, corrected requirements, and assumptions |
| `product_spec.md` | Product goals, users, MVP, non-goals, success metrics |
| `ux_spec.md` | Pages, flows, states, interactions, copy, and usability rules |
| `architecture_spec.md` | Tech stack, data models, module boundaries, tests, and runtime approach |
| `events.jsonl` | All state change events |
| `decisions.jsonl` | All key decisions with rationale |
| `trace.jsonl` | Global timeline for replaying the full process in chronological order |
| `runs/` | Detailed records of each execution or review attempt |
| `final_report.md` | Final result, usage instructions, task summary, decisions, and log index |

---

## 6. State Machine

Task state transitions:

```text
triage
  → todo
  → ready
  → running
  → review
  → quality_review
  → done
```

Exception transitions:

```text
running → blocked
blocked → ready
running → ready          # crash / timeout / retry
review → ready           # spec review rejected
quality_review → ready   # quality review rejected
any → archived
```

Rules:

- `triage` tasks cannot be executed directly.
- Ambiguous tasks must be refined by `specifier`.
- Only `ready` tasks can be executed.
- After `implementer` completes, the task enters `review` — never directly `done`.
- `blocked` tasks must document blocker reason and unblock condition.
- Routine ambiguity is resolved autonomously by `decision_maker`, not by asking the user.
- `done` requires implementation evidence, spec review evidence, and quality review evidence.

---

## 7. Full Autonomous Execution Flow

```text
1.  Read user idea
2.  Initialize .agent/kanban/
3.  requirements_analyst audits requirements
4.  decision_maker corrects flawed requirements or adds assumptions
5.  product_strategist generates product_spec.md
6.  ux_designer generates ux_spec.md
7.  technical_architect generates architecture_spec.md
8.  orchestrator decomposes task graph
9.  specifier refines tasks into executable task cards
10. implementer executes ready tasks
11. Records step_log, commands, files_changed, verification
12. spec_reviewer verifies requirement compliance
13. quality_reviewer verifies quality and maintainability
14. If rejected, return to ready and fix
15. If approved, mark done
16. Continue polling until all feasible tasks are done / blocked / archived
17. supervisor outputs final_report.md
```

---

## 8. When the Model May Stop and Ask the User

By default, do not ask the user about routine decisions.

**Allowed reasons to pause and request human input:**

- Missing accounts, tokens, API keys, or external permissions.
- Requires a paid external service.
- Requires irreversible destructive operations.
- Involves security, legal, privacy, or compliance risks.
- The platform lacks execution permissions and no mock/stub/local substitute is available.

**Not allowed reasons to stop:**

- Tech stack choice.
- UI style choice.
- Data model choice.
- File naming.
- Routine feature prioritization.
- MVP scope trimming.
- Requirements that are incomplete but can be reasonably inferred.
- Multiple viable implementation approaches exist.

All of these should be resolved by `decision_maker` and written to `decisions.jsonl`.

---

## 9. Usage in ChatGPT

After installing the Skill, use it like this:

```text
Use the idea-to-execution skill.

Idea:
I want to build a daily English phrase practice check-in app.

Execution mode:
autonomous_best_effort

Requirements:
1. Do not ask me for routine requirement details — let the model autonomously derive the best MVP.
2. Even if the requirement looks clear, always start with requirements_audit.
3. Automatically generate product_spec.md, ux_spec.md, architecture_spec.md.
4. Decompose tasks from spec documents — coarse tasks like "build app" are not allowed.
5. Every task must have run, step_log, event, and decision records.
6. The implementer cannot mark a task as done itself.
7. Done requires spec review and quality review.
8. After all tasks complete, give me only the final result and a complete execution log summary.
```

Shorter startup:

```text
Use idea-to-execution. Idea: I want to build a daily English phrase practice check-in app. Run autonomously and give me the result and execution log at the end.
```

---

## 10. Usage in Claude Code

Create or update at the project root:

```text
CLAUDE.md
```

Add the core rules:

```markdown
# Idea to Execution

For complex tasks, use `.agent/kanban/` as the durable task board.

Default mode: autonomous_best_effort.

Rules:
- User may provide only an idea.
- Always audit requirements before implementation.
- Generate requirements_audit.md, product_spec.md, ux_spec.md, architecture_spec.md.
- Decompose tasks from specs, not raw idea.
- Use default roles: orchestrator, requirements_analyst, product_strategist, ux_designer, technical_architect, decision_maker, specifier, implementer, spec_reviewer, quality_reviewer, supervisor.
- Every task execution creates a run and step logs.
- Every decision is recorded in decisions.jsonl.
- Every state change is recorded in events.jsonl.
- Full chronological trace goes to trace.jsonl.
- Implementer cannot final-accept its own work.
- Done requires spec review and quality review.
- Continue polling until all feasible tasks are done, blocked, or archived.
```

Then start with:

```text
Follow CLAUDE.md and use the idea-to-execution protocol.
Idea: I want to build a daily English phrase practice check-in app.
Run autonomously and give me only the final result plus trace summary.
```

---

## 11. Usage in Codex / OpenCode

Create or update at the project root:

```text
AGENTS.md
```

Add:

```markdown
# Idea to Execution Protocol

Use `.agent/kanban/` as the persistent execution board.

Workflow:
idea → requirements audit → product spec → UX spec → architecture spec → task graph → implementation → spec review → quality review → final report.

Do not ask the user for routine product or technical choices. Make best-effort autonomous decisions and log them.

Every task must include:
- objective
- spec references
- acceptance criteria
- expected outputs
- verification method
- residual risk

Every run must include:
- actor role
- step_log
- commands
- files_changed
- verification
- summary
- next_agent
```

Startup command:

```text
Follow AGENTS.md.
Use the idea-to-execution protocol.
Idea: [your project idea]
Execute autonomously until final report.
```

---

## 12. Script Usage

The Skill ships with:

```text
scripts/kanban_dispatch.py
```

Common commands:

```bash
python scripts/kanban_dispatch.py init
python scripts/kanban_dispatch.py status
python scripts/kanban_dispatch.py validate
python scripts/kanban_dispatch.py report
```

Add a task:

```bash
python scripts/kanban_dispatch.py add-task \
  --title "implement daily phrase card" \
  --objective "show today's English phrase with meaning and example" \
  --priority p0 \
  --status ready \
  --assignee implementer \
  --criteria "today phrase is visible" \
  --criteria "meaning and example sentence are visible" \
  --output "phrase card component" \
  --verify "run app and inspect phrase card"
```

Claim a task:

```bash
python scripts/kanban_dispatch.py next --claim --actor implementer
```

Log an execution step:

```bash
python scripts/kanban_dispatch.py step-log \
  --task T-001 \
  --actor implementer \
  --phase edit \
  --action "implemented phrase card" \
  --target "src/components/PhraseCard.tsx" \
  --observation "added phrase, translation, and example display" \
  --file "src/components/PhraseCard.tsx" \
  --result success
```

Submit implementation:

```bash
python scripts/kanban_dispatch.py submit \
  --task T-001 \
  --actor implementer \
  --summary "implemented daily phrase card" \
  --verification "npm test"
```

Log a decision:

```bash
python scripts/kanban_dispatch.py decide \
  --actor decision_maker \
  --question "Should MVP use account login?" \
  --selected "No account login for MVP; use local persistence" \
  --rejected "Account-based sync" \
  --rationale "Local persistence is faster, reversible, and enough to validate the core habit loop" \
  --assumption "Single-device MVP is acceptable" \
  --risk "No cross-device sync" \
  --impact T-001
```

Review:

```bash
python scripts/kanban_dispatch.py spec-review \
  --task T-001 \
  --actor spec_reviewer \
  --approve \
  --summary "matches product and UX spec"

python scripts/kanban_dispatch.py quality-review \
  --task T-001 \
  --actor quality_reviewer \
  --approve \
  --summary "implementation is maintainable and verified"
```

Generate final report:

```bash
python scripts/kanban_dispatch.py report
```

---

## 13. How to Inspect Execution

### 13.1 View the Final Result

```text
.agent/kanban/final_report.md
```

Should contain:

- What was ultimately delivered.
- How to run or use it.
- Completed task list.
- Key decision summary.
- Verification results.
- Residual risks.
- Log index.

### 13.2 View How Requirements Were Corrected

```text
.agent/kanban/requirements_audit.md
```

Key sections:

- Raw user idea.
- Restated intent.
- Detected issues.
- Corrected requirement.
- Assumptions.
- Confidence.

### 13.3 View Why a Decision Was Made

```text
.agent/kanban/decisions.jsonl
```

Each decision should document:

- What the question was.
- What was chosen.
- What was rejected.
- Why this choice was made.
- What assumptions were made.
- What the risks are.
- Which tasks are affected.

### 13.4 View the Full Timeline

```text
.agent/kanban/trace.jsonl
```

This is the most important audit file. It should allow the entire task execution process to be reconstructed in chronological order.

### 13.5 View Each Task Execution

```text
.agent/kanban/runs/
```

Each run should contain:

- actor.
- task_id.
- step_log.
- changed_files.
- commands.
- verification.
- summary.
- residual_risk.
- next_agent.

---

## 14. Example: Daily English Phrase Practice App

Input:

```text
I want to build a daily English phrase practice check-in app.
```

The Skill should **not** start writing code immediately. It should first derive:

```text
Target users: People who want to build an English phrase learning habit with minimal daily time.
Core loop: Open app → view today's phrase → read meaning and example → click complete → update streak and history.
MVP: Daily phrase card, meaning, example, check-in button, streak count, history, local persistence.
Non-goals: Account system, cloud sync, payments, complex reminders, AI-generated phrases.
```

A well-formed task breakdown looks like:

```text
1. Initialize runnable project
2. Define phrase and check-in data models
3. Prepare seed phrase data
4. Implement daily phrase selection logic
5. Implement check-in and streak calculation
6. Implement daily phrase card UI
7. Implement progress and history UI
8. Implement local persistence
9. Handle empty state, checked-in state, error state
10. Add verification or tests
11. Generate usage instructions and final report
```

An unacceptable task breakdown:

```text
build app
implement frontend
add UI
test everything
```

Tasks this coarse must be rejected.

---

## 15. Quality Checklist

A valid execution must satisfy:

- [ ] `requirements_audit.md` generated.
- [ ] `product_spec.md` generated.
- [ ] `ux_spec.md` generated.
- [ ] `architecture_spec.md` generated.
- [ ] Tasks are decomposed from specs, not directly from the raw idea.
- [ ] Every task has objective, acceptance criteria, expected outputs, and verification method.
- [ ] Every task has a run.
- [ ] Every run has a step_log.
- [ ] Every significant choice has a decision record.
- [ ] Every state change has an event.
- [ ] `trace.jsonl` can replay the full process.
- [ ] The implementer did not self-approve done.
- [ ] Done tasks passed spec review.
- [ ] Done tasks passed quality review.
- [ ] `final_report.md` generated.

---

## 16. Common Failure Modes

### Failure 1: Requirements Not Audited — Coding Started Immediately

Symptom: Code runs but the product loop is weak.

Fix: Require re-execution of the requirements gate; complete `requirements_audit.md`, `product_spec.md`, `ux_spec.md`, `architecture_spec.md`.

### Failure 2: Tasks Too Coarse

Symptom: Tasks named `build app`, `finish project`, `implement frontend`.

Fix: Return to specifier; re-decompose tasks from product/UX/architecture specs.

### Failure 3: No Execution Logs

Symptom: Only the final result is visible; no record of how it was produced.

Fix: Validate must fail. Complete run, step_log, event, decision, trace.

### Failure 4: Implementer Self-Approved Done

Symptom: No review process exists.

Fix: Return to review; spec_reviewer and quality_reviewer must verify.

### Failure 5: Asking the User About Routine Ambiguity

Symptom: Model frequently asks "what framework do you want?" or "what style do you prefer?"

Fix: decision_maker resolves autonomously, writes to decisions.jsonl, continues execution.

---

## 17. Recommended Startup Templates

### Template A: Fully Autonomous Product Development

```text
Use the idea-to-execution skill.

Idea:
[your project idea]

Execution mode: autonomous_best_effort

Requirements:
1. I provide only the idea.
2. Do not ask me for routine product, UX, architectural, or implementation choices.
3. Even if the idea looks clear, always start with requirements_audit.
4. Automatically correct flawed requirements and log the rationale.
5. Generate product_spec.md, ux_spec.md, architecture_spec.md.
6. Decompose and execute tasks from the specs.
7. Every task must have run, step_log, event, decision, and trace records.
8. Done requires spec review and quality review.
9. At the end, give me only the final result, usage instructions, and execution log summary.
```

### Template B: Add a Feature to an Existing Project

```text
Use the idea-to-execution skill.

Idea:
Add [feature description] to the current project.

Execution mode: autonomous_best_effort

Requirements:
1. First audit requirements and review the current project structure.
2. Automatically choose the least invasive implementation approach.
3. Record architectural judgment before making changes.
4. Write a step_log for every file modification.
5. Run verification after completion.
6. Auto-fix if review fails.
7. Output final_report and trace summary at the end.
```

### Template C: Resume an Existing Task Board

```text
Resume using the task board in .agent/kanban/.

Requirements:
1. Read board.json, events.jsonl, decisions.jsonl, trace.jsonl.
2. Find the next highest-priority ready task.
3. Continue the dispatch loop.
4. Do not repeat tasks already marked done.
5. Write all new actions to run, event, decision, and trace.
```

---

## 18. Real-World Boundaries

This Skill aims for:

```text
Best-effort traceable execution within current context and tool constraints.
```

It cannot guarantee mathematical global optimality.

What it does guarantee:

- No blind execution of user ideas.
- Automatic requirement review and correction.
- Automatic selection of a reasonable MVP.
- Automatic task decomposition and continuous progress.
- Automatic review and fix cycles.
- A complete auditable log throughout.
- Final result plus audit materials at the end.

This is its value: **elevating complex tasks from a one-shot prompt into a recoverable, auditable, autonomously-driven Agent execution system.**
