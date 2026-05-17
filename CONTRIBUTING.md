# Contributing to idea-to-execution

感谢你关注这个项目的演进。下面是你需要知道的一切。

---

## 如何本地测试这个 Skill

### 方式一：模拟运行（推荐）

在没有 AI agent 环境的情况下，验证 skill 的安装脚本和目录结构：

```bash
# 克隆仓库
git clone https://github.com/cat-czt/idea-to-execution.git
cd idea-to-execution

# 验证目录结构完整
test -f SKILL.md && test -d agents && test -d references && test -d scripts

# 验证安装脚本语法
bash -n scripts/install-skill.sh

# 模拟安装到临时目录
tmpdir=$(mktemp -d)
SKILLS_DIR="$tmpdir/.agent/skills" bash scripts/install-skill.sh
ls "$tmpdir/.agent/skills/idea-to-execution/"

# 验证安装结果
test -f "$tmpdir/.agent/skills/idea-to-execution/SKILL.md"
test -f "$tmpdir/.agent/skills/idea-to-execution/references/autonomous-decision-policy.md"
```

### 方式二：在 AI Agent 中运行

```bash
# 方式 A：通过环境变量
export SKILLS_DIR="$HOME/.agent/skills"
curl -fsSL https://raw.githubusercontent.com/cat-czt/idea-to-execution/main/scripts/install-skill.sh | bash

# 方式 B：在 Claude Code / Codex 中
# 在项目根目录创建 CLAUDE.md / AGENTS.md，引用 skill 路径
```

---

## Commit 规范

使用 [Conventional Commits](https://www.conventionalcommits.org/)：

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Type 枚举

| Type | 适用场景 |
|------|---------|
| `feat` | 新功能、新角色、新工作流 |
| `fix` | Bug 修复 |
| `docs` | 文档更新（README、CONTRIBUTING 等） |
| `refactor` | 重构（不影响行为的内部变更） |
| `test` | 添加或修改测试 |
| `chore` | 构建脚本、CI、依赖更新 |
| `ci` | CI workflow 修改 |

### Scope 可选

建议的 scope：
- `install` — 安装脚本相关
- `references` — 参考文档相关
- `agents` — agent 配置相关
- `workflow` — SKILL.md 工作流定义

### 示例

```
feat(references): 添加 autonomy-completion-contract.md
fix(install): 修复 --dir 参数在某些平台上路径拼接错误
docs: 更新 README 中的平台支持列表
ci: 添加 CI workflow 验证 SKILL.md 结构
```

---

## PR 流程

### 分支策略

```
main  ←  所有 PR 的目标分支（受保护）

feature/xxx  ←  功能分支
fix/xxx      ←  Bug 修复分支
docs/xxx     ←  文档改进分支
```

### PR 规范

1. **每个 PR 只做一件事**（一个功能、一个修复、一组相关文档）
2. **PR 描述必须包含**：
   - 改变了什么
   - 为什么需要这个改变
   - 如何验证（测试步骤或截图）
3. **CI 必须通过**才能合并：
   - `lint-skill-structure` — SKILL.md 结构、frontmatter、references 完整性
   - `lint-scripts` — ShellCheck 检查
   - `validate-install` — 安装脚本语法和模拟安装

### Review 要求

- 至少 1 个 approve 才能合并
- Reviewer 检查：SKILL.md 逻辑一致性、references 与主文档的引用关系、CI 是否足够

---

## Skill 结构变更规范

如果你的 PR 修改了以下内容，必须同步更新对应文件：

| 变更内容 | 必须同步检查 |
|---------|------------|
| 新增/删除/重命名 agent 角色 | `references/agent-roles.md`、`SKILL.md` 中的角色列表 |
| 修改状态机状态 | `SKILL.md` 状态机部分、`references/dispatch-loop.md` |
| 新增/删除 mandatory references | `.github/workflows/ci.yml` 中的 required_refs |
| 修改安装路径 | `README_INSTALL_QUICK.md`、`SKILL.md` 中的路径说明 |
| 新增文档模板 | 需在 `SKILL.md` 中说明用途和触发条件 |

---

## 发现 Bug 或提出功能建议

请使用 GitHub Issues，建议使用 issue templates（稍后添加）。

描述时包含：
- **环境**：哪个 agent 平台（Hermes / Claude Code / Codex）
- **复现步骤**：尽量简单明了
- **期望行为 vs 实际行为**

---

## Questions?

欢迎在 GitHub Discussions 中提问。