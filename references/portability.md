# Portability

## Principle

Port the protocol, not the exact implementation. The same autonomous workflow can run with native subagents, simulated roles, or a platform-specific dispatcher.

## Claude Code

Place the protocol in `CLAUDE.md` or a Claude Skill. Use native subagents or forked contexts when available.

Recommended instruction:

```text
Use the idea-to-execution protocol in autonomous_best_effort mode. Treat me as the idea provider, not the decision router. Create .agent/kanban if missing. Make decisions using decision_maker, log them to decisions.jsonl, execute the dispatch loop, and return final result plus execution trace.
```

## Codex

Place the protocol in `AGENTS.md`. If multi-agent spawning is available, map roles to spawned agents. If not, run single-agent fallback with role-labeled runs.

Recommended instruction:

```text
Follow AGENTS.md. Use autonomous idea-to-execution. Do not ask for product or implementation choices; decide, log, and continue. Stop only for hard external blockers or unsafe actions.
```

## OpenCode

Place the protocol in project-level agent instructions. Use `.agent/kanban/` as persistent state when files are available.

Recommended instruction:

```text
Execute this idea using autonomous kanban dispatch. Simulate roles if native subagents are unavailable. Preserve task/run/step/event/decision/trace logs and produce final_report.md.
```

## Hermes-like systems

Map:

- board to native board,
- task to native card,
- run to execution attempt,
- event to transition log,
- decision to comment or decision table,
- role to profile or assignee,
- decision_maker to autonomous unblock/supervisor profile.

## Single-agent fallback

When only one model session exists, do not drop the protocol. Execute roles sequentially:

1. announce current role internally or in the log,
2. perform that role's work,
3. write a run or decision record with that role name,
4. move to the next role.

The final trace must still show distinct orchestrator, decision_maker, implementer, reviewer, and supervisor actions.

## Trace-first usage prompt

Use this when you want full provenance:

```text
Execute my idea autonomously with idea-to-execution.
I only want the final result at the end, but every task must be fully logged.
Maintain task records, run records, step logs, event logs, decision logs, and a chronological trace ledger.
Do not mark any task done unless its implementation and review runs have step logs and evidence.
Return final_report.md with task/run/step/event/decision counts and links or paths to trace files.
```
