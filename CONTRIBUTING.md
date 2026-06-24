# Contributing to idea-to-execution

English | [简体中文](CONTRIBUTING_ZH.md)

Thank you for your interest in the evolution of this project. Here's everything you need to know.

---

## How to Test This Skill Locally

### Option 1: Simulated Run (Recommended)

Verify the Skill's installation script and directory structure without an AI agent environment:

```bash
# Clone the repository
git clone https://github.com/cat-czt/idea-to-execution.git
cd idea-to-execution

# Verify directory structure is complete
test -f SKILL.md && test -d agents && test -d references && test -d scripts

# Verify installation script syntax
bash -n scripts/install-skill.sh

# Simulate installation to a temporary directory
tmpdir=$(mktemp -d)
SKILLS_DIR="$tmpdir/.agent/skills" bash scripts/install-skill.sh
ls "$tmpdir/.agent/skills/idea-to-execution/"

# Verify installation result
test -f "$tmpdir/.agent/skills/idea-to-execution/SKILL.md"
test -f "$tmpdir/.agent/skills/idea-to-execution/references/autonomous-decision-policy.md"
```

### Option 2: Run Inside an AI Agent

```bash
# Option A: Via environment variable
export SKILLS_DIR="$HOME/.agent/skills"
curl -fsSL https://raw.githubusercontent.com/cat-czt/idea-to-execution/main/scripts/install-skill.sh | bash

# Option B: In Claude Code / Codex
# Create CLAUDE.md / AGENTS.md in the project root, referencing the skill path
```

---

## Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Type Reference

| Type | When to use |
|------|-------------|
| `feat` | New feature, new agent role, new workflow |
| `fix` | Bug fix |
| `docs` | Documentation updates (README, CONTRIBUTING, etc.) |
| `refactor` | Refactoring (internal changes that don't affect behavior) |
| `test` | Adding or modifying tests |
| `chore` | Build scripts, CI, dependency updates |
| `ci` | CI workflow changes |

### Scope (Optional)

Suggested scopes:
- `install` — installation script related
- `references` — reference documentation related
- `agents` — agent configuration related
- `workflow` — SKILL.md workflow definition

### Examples

```
feat(references): add autonomy-completion-contract.md
fix(install): fix path concatenation bug with --dir flag on certain platforms
docs: update platform support list in README
ci: add CI workflow to validate SKILL.md structure
```

---

## Pull Request Process

### Branch Strategy

```
main  ←  target branch for all PRs (protected)

feature/xxx  ←  feature branches
fix/xxx      ←  bug fix branches
docs/xxx     ←  documentation improvement branches
```

### PR Requirements

1. **Each PR does one thing** (one feature, one fix, or one related set of documentation changes).
2. **PR description must include**:
   - What changed
   - Why the change is needed
   - How to verify it (test steps or screenshots)
3. **CI must pass** before merging:
   - `lint-skill-structure` — SKILL.md structure, frontmatter, and references completeness
   - `lint-scripts` — ShellCheck validation
   - `validate-install` — installation script syntax and simulated install

### Review Requirements

- At least 1 approval required before merging.
- Reviewers check: SKILL.md logical consistency, reference-to-main-document relationships, and whether CI coverage is sufficient.

---

## Skill Structure Change Rules

If your PR modifies any of the following, you must update the corresponding files in sync:

| What changed | Must also check |
|---|---|
| Added / removed / renamed an agent role | `references/agent-roles.md`, agent role list in `SKILL.md` |
| Modified state machine states | State machine section in `SKILL.md`, `references/dispatch-loop.md` |
| Added / removed mandatory references | `required_refs` in `.github/workflows/ci.yml` |
| Changed installation path | `README_INSTALL_QUICK.md`, path descriptions in `SKILL.md` |
| Added a new document template | Must describe purpose and trigger conditions in `SKILL.md` |

---

## Reporting Bugs or Suggesting Features

Please use GitHub Issues. Issue templates will be added soon.

When describing an issue, include:
- **Environment**: which agent platform (Hermes / Claude Code / Codex)
- **Steps to reproduce**: as concise as possible
- **Expected behavior vs. actual behavior**

---

## Questions?

Feel free to ask in GitHub Discussions.
