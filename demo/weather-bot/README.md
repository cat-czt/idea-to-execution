# Demo: Weather Bot — 5 分钟可跑通

## 场景

用户说："我想做一个每天早上给我发天气预报的 Telegram Bot"

我们用 `idea-to-execution` 模式执行，全程无人力干预。

---

## 执行步骤

### 1. 在你的项目目录初始化

```bash
mkdir weather-bot && cd weather-bot
```

### 2. 创建 CLAUDE.md（Claude Code 环境）

```markdown
# Idea to Execution

Use `idea-to-execution` protocol for complex tasks.

Rules:
- User may provide only an idea.
- Always audit requirements before implementation.
- Generate requirements_audit.md, product_spec.md, ux_spec.md, architecture_spec.md.
- Decompose tasks from specs, not from raw idea.
- Run autonomously under autonomous_best_effort unless blocked by credentials, permissions, or unsafe operations.
- Every task needs run logs, step logs, events, decisions, verification.
- implementer cannot mark its own task done.
- Done requires spec review and quality review.
- Continue until final_report.md is produced.

Skill location:
~/.agent/skills/idea-to-execution
```

### 3. 启动 Claude Code（或你使用的 Agent），输入：

```
Use idea-to-execution.
Idea: Build a Telegram bot that sends daily weather forecast to me every morning at 8am. Use free weather API. Bot should respond to /start and /weather commands.
Mode: autonomous_best_effort
```

### 4. Agent 会自动执行以下流程

```
✓ 读取 idea
✓ 初始化 .agent/kanban/
✓ requirements_analyst 审查需求
✓ decision_maker 补充假设（使用 openweathermap free tier）
✓ product_strategist 生成 product_spec.md
✓ ux_designer 生成 ux_spec.md
✓ technical_architect 生成 architecture_spec.md
✓ orchestrator 拆分任务图
✓ specifier 细化任务
✓ implementer 执行（Python + python-telegram-bot + openweathermap）
✓ spec_reviewer 验收
✓ quality_reviewer 检查
✓ supervisor 输出 final_report.md
```

---

## 预期输出

```
weather-bot/
├── .agent/kanban/
│   ├── board.json              # 任务状态
│   ├── requirements_audit.md    # 需求审查结果
│   ├── product_spec.md         # 产品规格
│   ├── ux_spec.md              # UX 规格
│   ├── architecture_spec.md    # 架构规格
│   ├── events.jsonl            # 事件日志
│   ├── decisions.jsonl         # 决策记录
│   ├── trace.jsonl             # 时间线
│   └── final_report.md         # 最终报告
├── bot.py                      # 主程序
├── requirements.txt
├── .env.example
└── README.md
```

---

## 你需要提供的

只有两件事：

1. **Telegram Bot Token** — 从 [@BotFather](https://t.me/BotFather) 获取
2. **OpenWeatherMap API Key** — 免费注册获取（免费 tier 足够）

其余所有决策（技术栈、目录结构、错误处理、轮询间隔、fallback）均由 Agent 自主完成。

---

## 验证方式

```bash
# 启动 bot
python bot.py

# 测试 /start 命令
curl -s "https://api.telegram.org/bot<YOUR_TOKEN>/sendMessage?chat_id=<YOUR_CHAT_ID>&text=/start"

# 测试 /weather 命令
curl -s "https://api.telegram.org/bot<YOUR_TOKEN>/sendMessage?chat_id=<YOUR_CHAT_ID>&text=/weather"

# 检查定时发送（第二天早上 8 点）
```

---

## 完整流程日志示例

Agent 执行完成后，你会在 `.agent/kanban/` 中看到完整的执行日志：

- `decisions.jsonl` — 为什么选择 Python 而非 Node.js、为什么用 APScheduler 而非 system cron
- `events.jsonl` — 每个任务的状态变化时间戳
- `final_report.md` — 最终交付物说明、启动方式、测试步骤

这就是 idea-to-execution 的核心价值：**不只是给你代码，还给你完整的决策和执行溯源**。