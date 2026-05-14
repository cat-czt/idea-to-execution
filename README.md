# idea-to-execution 使用说明

## 1. 这个 Skill 是什么

`idea-to-execution` 是一个面向复杂任务执行的通用 Agent 工作流 Skill。

它的目标不是简单维护一个待办列表，而是把用户给出的 idea 自动转化为一套可执行、可审计、可恢复的多 Agent 工作流程：

```text
idea
→ 需求审查
→ 产品规格
→ UX 规格
→ 架构规格
→ 任务拆分
→ 自动决策
→ 执行
→ 过程日志
→ spec review
→ quality review
→ 修复重试
→ 最终结果 + 完整溯源日志
```

默认行为是：**用户只提供 idea，模型自主完成普通产品、技术、架构、任务拆解、实现、review 和修复决策**。用户只需要在最后查看结果和执行过程日志。

---

## 2. 适合什么场景

适合使用这个 Skill 的场景：

- 从一个模糊 idea 开始开发产品、工具、App、脚本或功能。
- 任务需要拆成多个步骤，并且希望 Agent 自动持续推进。
- 你不想频繁参与普通产品/技术决策，只想看最终结果。
- 你需要完整记录每个任务怎么被执行、为什么这么做、改了什么、验证了什么。
- 你希望在 Claude Code、Codex、OpenCode、Hermes-like 系统或单 Agent 环境中复用同一套执行协议。

不适合的场景：

- 一句话问答。
- 简单翻译或改写。
- 必须由真人做主观选择的品牌、法律、财务、商业承诺类决策。
- 缺少账号、token、外部权限，且无法用 mock/stub 替代的任务。
- 不允许模型自主做产品和技术判断的任务。

---

## 3. 核心原则

### 3.1 全自动优先

默认模式是：

```text
autonomous_best_effort
```

模型遇到普通选择时，不应该问用户，而应该：

1. 根据 idea 和上下文推断。
2. 使用行业默认方案。
3. 选择最小可验证 MVP。
4. 选择更可逆、更低风险、更容易验证的方案。
5. 把决策写入 `decisions.jsonl`。
6. 继续执行。

### 3.2 先审查需求，不盲目执行

用户需求说得清楚，不等于需求正确。

因此任何 idea 都必须先进入：

```text
requirements_audit.md
```

Skill 会检查：

- 需求是否自相矛盾。
- 是否缺少核心用户闭环。
- 是否范围过大。
- 是否假设错误。
- 是否可以收敛成更合理的 MVP。
- 是否需要自动修正需求再继续。

修正后的需求会成为后续产品、UX、架构和任务拆解的依据。

### 3.3 所有执行必须可追溯

任务不能静默执行。

每个任务必须有：

- task 状态变化。
- run 记录。
- step_log。
- command 记录。
- 文件变更记录。
- verification 记录。
- review 记录。
- decision 记录。
- trace 时间线。

没有执行日志的任务不能进入 `done`。

### 3.4 implementer 不能自己宣布完成

`implementer` 只能提交实现结果。

任务进入 `done` 必须经过：

```text
implementer submission
→ spec_reviewer approval
→ quality_reviewer approval
→ supervisor final acceptance
```

---

## 4. 默认 Agent 角色

Skill 默认使用以下角色。平台支持子 Agent 时，可以真实派发；不支持时，由单一会话模拟角色，但必须在日志里保留角色身份。

| Agent | 职责 |
|---|---|
| `orchestrator` | 把 idea 转成执行计划、任务图、依赖和成功标准 |
| `requirements_analyst` | 审查、纠偏和标准化用户需求 |
| `product_strategist` | 生成产品定位、目标用户、MVP、成功指标和非目标 |
| `ux_designer` | 生成用户路径、页面、状态、交互和文案要求 |
| `technical_architect` | 选择技术方案、数据模型、模块边界和验证策略 |
| `decision_maker` | 自主做普通产品/技术/架构/范围决策，并记录理由 |
| `specifier` | 把粗任务变成可执行任务卡 |
| `implementer` | 执行单个 ready 任务，记录过程并提交 review |
| `spec_reviewer` | 检查实现是否满足需求、规格和验收标准 |
| `quality_reviewer` | 检查质量、可维护性、测试、风险和过度设计 |
| `supervisor` | 最终验收、归档无关任务、整理最终报告 |

---

## 5. 持久化目录结构

当环境允许写文件时，Skill 使用以下目录作为任务板：

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

关键文件说明：

| 文件 | 作用 |
|---|---|
| `board.json` | 当前任务池、任务状态、依赖和角色分配 |
| `requirements_audit.md` | 原始需求审查、问题识别、修正后需求和假设 |
| `product_spec.md` | 产品目标、用户、MVP、非目标、成功指标 |
| `ux_spec.md` | 页面、流程、状态、交互、文案和可用性规则 |
| `architecture_spec.md` | 技术栈、数据模型、模块边界、测试和运行方式 |
| `events.jsonl` | 所有状态变化事件 |
| `decisions.jsonl` | 所有关键决策及其理由 |
| `trace.jsonl` | 全局时间线，可按时间顺序复盘全流程 |
| `runs/` | 每次执行或 review 尝试的详细记录 |
| `final_report.md` | 最终结果、使用方式、任务摘要、决策和日志索引 |

---

## 6. 状态机

任务状态流转如下：

```text
triage
  → todo
  → ready
  → running
  → review
  → quality_review
  → done
```

异常流转：

```text
running → blocked
blocked → ready
running → ready          # crash / timeout / retry
review → ready           # spec review rejected
quality_review → ready   # quality review rejected
any → archived
```

规则：

- `triage` 任务不能直接执行。
- 模糊任务必须由 `specifier` 规格化。
- `ready` 任务才能被执行。
- `implementer` 完成后进入 `review`，不能直接 `done`。
- `blocked` 必须写明 blocker reason 和 unblock condition。
- 普通歧义由 `decision_maker` 自动处理，不默认询问用户。
- `done` 必须有实现证据、spec review 证据和 quality review 证据。

---

## 7. 全自动执行流程

完整流程：

```text
1. 读取用户 idea
2. 初始化 .agent/kanban/
3. requirements_analyst 审查需求
4. decision_maker 修正错误需求或补充假设
5. product_strategist 生成 product_spec.md
6. ux_designer 生成 ux_spec.md
7. technical_architect 生成 architecture_spec.md
8. orchestrator 拆分任务图
9. specifier 把任务细化为可执行 task
10. implementer 执行 ready task
11. 记录 step_log、commands、files_changed、verification
12. spec_reviewer 验收需求符合度
13. quality_reviewer 验收质量和可维护性
14. 不通过则回到 ready 并修复
15. 通过则 done
16. 继续轮询直到所有可行任务 done / blocked / archived
17. supervisor 输出 final_report.md
```

---

## 8. 什么时候可以停下来问用户

默认不要问用户普通决策。

允许停止或请求人工输入的情况只有：

- 缺少账号、token、API key、外部权限。
- 需要付费外部服务。
- 需要执行不可逆破坏性操作。
- 涉及安全、法律、隐私、合规风险。
- 当前平台没有执行权限，也无法用 mock、stub 或本地替代方案继续。

不允许因为以下原因停下来问用户：

- 技术栈选择。
- UI 风格选择。
- 数据模型选择。
- 文件命名。
- 普通功能优先级。
- MVP 范围裁剪。
- 需求不够完整但可以合理推断。
- 有多个可行实现方式。

这些都应该由 `decision_maker` 选择，并写入 `decisions.jsonl`。

---

## 9. ChatGPT 中的使用方式

安装 Skill 后，可以直接这样使用：

```text
使用 idea-to-execution skill。

Idea:
我想开发一个每日英语短语练习打卡的项目。

执行模式：
autonomous_best_effort

要求：
1. 不要问我普通需求细节，由模型自主推导最优 MVP。
2. 即使需求看起来清楚，也先做 requirements_audit。
3. 自动生成 product_spec.md、ux_spec.md、architecture_spec.md。
4. 从规格文档拆任务，不允许出现 build app 这种粗任务。
5. 所有任务必须有 run、step_log、event、decision。
6. implementer 不能自己 done。
7. done 必须经过 spec review 和 quality review。
8. 所有任务结束后，只给我最终结果和完整执行日志摘要。
```

更短的启动方式：

```text
使用 idea-to-execution。Idea: 我想做一个每日英语短语练习打卡项目。全自动执行，最后给我结果和执行日志。
```

---

## 10. Claude Code 使用方式

在项目根目录创建或更新：

```text
CLAUDE.md
```

加入核心规则：

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

然后启动：

```text
Follow CLAUDE.md and use the idea-to-execution protocol.
Idea: 我想开发一个每日英语短语练习打卡项目。
Run autonomously and give me only the final result plus trace summary.
```

---

## 11. Codex / OpenCode 使用方式

在项目根目录创建或更新：

```text
AGENTS.md
```

加入：

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

启动命令：

```text
Follow AGENTS.md.
Use the idea-to-execution protocol.
Idea: [你的项目想法]
Execute autonomously until final report.
```

---

## 12. 脚本使用方式

Skill 附带脚本：

```text
scripts/kanban_dispatch.py
```

常用命令：

```bash
python scripts/kanban_dispatch.py init
python scripts/kanban_dispatch.py status
python scripts/kanban_dispatch.py validate
python scripts/kanban_dispatch.py report
```

添加任务：

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

领取任务：

```bash
python scripts/kanban_dispatch.py next --claim --actor implementer
```

记录执行步骤：

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

提交实现：

```bash
python scripts/kanban_dispatch.py submit \
  --task T-001 \
  --actor implementer \
  --summary "implemented daily phrase card" \
  --verification "npm test"
```

记录决策：

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

Review：

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

生成最终报告：

```bash
python scripts/kanban_dispatch.py report
```

---

## 13. 如何查看执行过程

### 13.1 看最终结果

```text
.agent/kanban/final_report.md
```

里面应该包含：

- 最终完成了什么。
- 如何运行或使用。
- 完成任务列表。
- 关键决策摘要。
- 验证结果。
- 剩余风险。
- 日志索引。

### 13.2 看需求是如何被修正的

```text
.agent/kanban/requirements_audit.md
```

重点看：

- Raw user idea。
- Restated intent。
- Detected issues。
- Corrected requirement。
- Assumptions。
- Confidence。

### 13.3 看为什么做某个决策

```text
.agent/kanban/decisions.jsonl
```

每条决策应该说明：

- 问题是什么。
- 选择了什么。
- 放弃了什么。
- 为什么这么选。
- 假设是什么。
- 风险是什么。
- 影响哪些任务。

### 13.4 看完整时间线

```text
.agent/kanban/trace.jsonl
```

这是最重要的溯源文件。它应该能按时间顺序重建整个任务执行过程。

### 13.5 看每次任务执行

```text
.agent/kanban/runs/
```

每个 run 都应该包含：

- actor。
- task_id。
- step_log。
- changed_files。
- commands。
- verification。
- summary。
- residual_risk。
- next_agent。

---

## 14. 示例：每日英语短语练习打卡项目

输入：

```text
我想开发一个每日英语短语练习打卡的项目。
```

Skill 不应该直接开始写代码，而应该先推导：

```text
目标用户：想每天用少量时间建立英语短语学习习惯的人。
核心循环：打开应用 → 查看今日短语 → 阅读释义和例句 → 点击完成练习 → 更新连续打卡和历史记录。
MVP：今日短语卡、释义、例句、打卡按钮、连续天数、历史记录、本地持久化。
非目标：账号系统、云同步、付费、复杂提醒、AI 自动生成短语。
```

合理任务拆分应该类似：

```text
1. 初始化可运行项目
2. 定义 phrase 和 check-in 数据模型
3. 准备 seed phrase 数据
4. 实现每日短语选择逻辑
5. 实现 check-in 和 streak 计算
6. 实现今日短语卡 UI
7. 实现进度和历史记录 UI
8. 实现本地持久化
9. 补齐空状态、已打卡状态、错误状态
10. 添加验证或测试
11. 生成使用说明和最终报告
```

不合格任务拆分：

```text
build app
implement frontend
add UI
test everything
```

这种拆分太粗，必须被 reject。

---

## 15. 质量检查清单

一次合格执行必须满足：

- [ ] 生成 `requirements_audit.md`。
- [ ] 生成 `product_spec.md`。
- [ ] 生成 `ux_spec.md`。
- [ ] 生成 `architecture_spec.md`。
- [ ] 任务不是从 raw idea 直接拆出来的。
- [ ] 每个任务有 objective、acceptance criteria、expected outputs、verification method。
- [ ] 每个任务都有 run。
- [ ] 每个 run 都有 step_log。
- [ ] 每个重要选择都有 decision 记录。
- [ ] 每个状态变化都有 event。
- [ ] `trace.jsonl` 能复盘全流程。
- [ ] implementer 没有自己标记 done。
- [ ] done 任务经过 spec review。
- [ ] done 任务经过 quality review。
- [ ] 最终生成 `final_report.md`。

---

## 16. 常见失败模式

### 失败 1：需求没审查，直接开写

症状：代码能跑，但产品闭环很弱。

处理：要求重新执行 requirements gate，补全 `requirements_audit.md`、`product_spec.md`、`ux_spec.md`、`architecture_spec.md`。

### 失败 2：任务太粗

症状：任务叫 `build app`、`finish project`、`implement frontend`。

处理：退回 specifier，按产品/UX/架构规格重新拆任务。

### 失败 3：没有执行日志

症状：只看到最终结果，不知道怎么做出来的。

处理：validate 必须失败。补齐 run、step_log、event、decision、trace。

### 失败 4：implementer 自己 done

症状：没有 review 过程。

处理：退回 review，必须由 spec_reviewer 和 quality_reviewer 验收。

### 失败 5：遇到普通歧义就问用户

症状：模型频繁问“你想用什么框架”“你想要什么样式”。

处理：decision_maker 自主选择，写入 decisions.jsonl，继续执行。

---

## 17. 推荐启动模板

### 模板 A：完全自动产品开发

```text
使用 idea-to-execution skill。

Idea:
[你的项目想法]

执行模式：autonomous_best_effort

要求：
1. 我只提供 idea。
2. 不要问我普通产品、UX、架构或实现选择。
3. 即使 idea 看起来清楚，也先做 requirements_audit。
4. 自动修正错误需求并记录理由。
5. 生成 product_spec.md、ux_spec.md、architecture_spec.md。
6. 从规格拆任务并执行。
7. 每个任务必须有 run、step_log、event、decision、trace。
8. done 必须经过 spec review 和 quality review。
9. 最后只给我最终结果、使用方式和执行日志摘要。
```

### 模板 B：已有项目里新增功能

```text
使用 idea-to-execution skill。

Idea:
在当前项目中新增 [功能描述]。

执行模式：autonomous_best_effort

要求：
1. 先审查需求和当前项目结构。
2. 自动选择最小侵入的实现方案。
3. 修改前记录架构判断。
4. 每次文件修改都写 step_log。
5. 完成后跑可用验证。
6. review 不通过就自动修复。
7. 最后输出 final_report 和 trace 摘要。
```

### 模板 C：继续已有任务板

```text
继续使用 .agent/kanban/ 中的任务板。

要求：
1. 读取 board.json、events.jsonl、decisions.jsonl、trace.jsonl。
2. 找出下一个最高优先级 ready task。
3. 继续 dispatch loop。
4. 不要重复已经 done 的任务。
5. 所有新动作继续写入 run、event、decision 和 trace。
```

---

## 18. 现实边界

这个 Skill 追求的是：

```text
在当前上下文和工具约束下，进行可追溯的最优努力执行。
```

它不能保证数学意义上的全局最优。

它能保证的是：

- 不盲目执行用户 idea。
- 自动审查和修正需求。
- 自动选择合理 MVP。
- 自动拆分任务并持续推进。
- 自动 review 和修复。
- 全程留下可审计日志。
- 最后给出结果和溯源材料。

这就是它的价值：**把复杂任务从一次性 prompt，升级成一个可恢复、可审计、可自动推进的 Agent 执行系统。**
