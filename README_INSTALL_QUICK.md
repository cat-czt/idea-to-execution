## Quick Install

`idea-to-execution` can be installed directly from this repository with a Skillshub-style one-line command.

### 1. Install

Default installation uses a generic local skills directory:

```bash
curl -fsSL https://raw.githubusercontent.com/cat-czt/idea-to-execution/main/scripts/install-skill.sh | bash
```

Default destination:

```text
~/.agent/skills/idea-to-execution
```

### 2. Install for Claude-style local skills

```bash
curl -fsSL https://raw.githubusercontent.com/cat-czt/idea-to-execution/main/scripts/install-skill.sh | bash -s -- --target claude
```

Destination:

```text
~/.claude/skills/idea-to-execution
```

### 3. Install to a custom directory

```bash
curl -fsSL https://raw.githubusercontent.com/cat-czt/idea-to-execution/main/scripts/install-skill.sh | bash -s -- --dir "$HOME/.agent/skills"
```

Or use `SKILLS_DIR`:

```bash
SKILLS_DIR="$HOME/.agent/skills" \
  curl -fsSL https://raw.githubusercontent.com/cat-czt/idea-to-execution/main/scripts/install-skill.sh | bash
```

### 4. Upgrade

```bash
curl -fsSL https://raw.githubusercontent.com/cat-czt/idea-to-execution/main/scripts/install-skill.sh | bash -s -- --force
```

Install a specific branch or tag:

```bash
curl -fsSL https://raw.githubusercontent.com/cat-czt/idea-to-execution/main/scripts/install-skill.sh | bash -s -- --ref main --force
```

### 5. Verify

```bash
test -f "$HOME/.agent/skills/idea-to-execution/SKILL.md" && echo "installed"
```

For Claude target:

```bash
test -f "$HOME/.claude/skills/idea-to-execution/SKILL.md" && echo "installed"
```

### 6. Use in a project

For Codex/OpenCode-style agents, add this to `AGENTS.md`:

```markdown
# Idea to Execution

Use the `idea-to-execution` protocol for complex tasks.

Skill location:
`~/.agent/skills/idea-to-execution`

Rules:
- Start from the user's idea.
- Always run requirements audit before implementation.
- Generate `requirements_audit.md`, `product_spec.md`, `ux_spec.md`, and `architecture_spec.md`.
- Decompose tasks from specs, not from the raw idea.
- Run autonomously under `autonomous_best_effort` unless blocked by credentials, permissions, payment, unsafe operations, or legal/privacy risk.
- Every task needs run logs, step logs, events, decisions, verification, and review evidence.
- `implementer` cannot mark its own task done.
- Done requires spec review and quality review.
- Continue until all feasible tasks are done, blocked, or archived.
```

Then start the agent with:

```text
Use idea-to-execution.
Idea: [your idea]
Run autonomously until final_report.md is produced.
```

### 7. Uninstall

```bash
rm -rf "$HOME/.agent/skills/idea-to-execution"
```

For Claude target:

```bash
rm -rf "$HOME/.claude/skills/idea-to-execution"
```
