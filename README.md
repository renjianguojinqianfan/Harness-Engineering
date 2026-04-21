# Project-Bootstrap-Harness (PBH)

> 一个为 AI 辅助编程设计的 **Python 项目协议模板**。
> 
> 它不指挥 AI 怎么写代码，而是在项目诞生的第一秒，就把"这里应该怎么协作"写成一份机器可读的合同。

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/badge/pypi-harness--init-green.svg)](https://pypi.org/project/harness-init/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 为什么需要这个？

用 Claude Code、Cursor 或 Codex 写代码时，你大概率遇到过这些摩擦：

- **每次新会话都要重新交代规则**："记得跑测试"、"别改无关文件"、"先写计划再编码"
- **AI 写了代码却不验证**：小错误滚雪球，最后人类来兜底
- **团队协作时，每个人对 AI 的指挥方式不一样**：A 同事让 AI 直接改，B 同事让 AI 先写方案，代码风格混乱

**问题不在于 AI 不够聪明，而在于项目本身缺少一份"默认协作协议"。**

PBH 在 `harness-init my-project` 的瞬间，把协议、质量门禁和状态记录种进项目。从此，任何打开这个项目的 AI 工具都能在 1 分钟内知道：这里的工作流是什么、质量底线在哪里、上一棒跑到哪了。

---

## 它做了什么（以及没做什么）

### ✅ 它是一份"协作合同"

- **`AGENTS.md`**：50-100 行的项目级系统提示，定义 Planner → Generator → Evaluator 三角色工作流、变更控制矩阵、安全规范
- **`docs/context.md`**：深层上下文（架构概览、命名约定、常见任务）
- **`.harness/progress.json`**：跨会话状态记录，让 AI 在新会话中快速恢复上下文  
  （示例：`{"current_stage": "plan", "plans": [{"id": "plan_001", "status": "approved"}], "last_updated": "2026-04-20T12:00:00Z"}`）

### ✅ 它是质量门禁的基础设施

- **`make verify`**：一键运行 ruff + pytest，覆盖率门槛 ≥ 85%
- **GitHub Actions CI**：推送即触发检查
- **Git Hooks**：提交前自动拦截风格问题

### ✅ 它带有一套可扩展的骨架代码

生成项目包含最小可运行的 Harness 组件：
- `harness/runner.py`：异步执行 JSON 计划文件中的命令步骤（串行编排 + 单任务错误熔断）
- `harness/evaluator.py`：基于执行结果的三维度评分（状态/完成率/错误）
- `harness/state.py`：原子化 JSON 状态读写（`tempfile` + `os.replace` 保证写入安全）
- `harness/workflow.py`：七阶段状态机定义（Feedback → Triage → Clarify → Plan → Execute → Evaluate → Done）

### ❌ 它不是 Agent 运行时

PBH **不强制执行** Agent 的行为。它不会阻止 AI 跳过 Planner 直接写代码，也不会自动推进工作流状态。它提供的是**协议和工具**，Agent 是否遵守，取决于 Agent 工具自身的理解能力和人类的即时监督。

### ❌ 它不是代码生成器

PBH 不根据自然语言描述生成业务代码。它生成的是**项目结构、配置文件和接口骨架**，业务逻辑需要你自己（或你的 AI）填充。

---

## 快速开始

```bash
pip install harness-init

# 完整模式（含 CI、IDE 适配、文档体系、Harness 骨架）
harness-init my-awesome-project

# 快速模式（最小可用，5 分钟上手）
harness-init my-project --quick --yes
```

进入项目并验证：

```bash
cd my-awesome-project
pip install -e ".[dev]"
make verify        # 应输出 ✔ 验证通过
```

### 💡 如果 make 命令不可用

Windows 用户可能未安装 make。若提示 'make' 不是内部或外部命令，你可以：

**安装 make：**

- Windows：安装 GnuWin32 Make 或 `winget install GnuWin32.Make`
- macOS：`xcode-select --install`
- Linux：`sudo apt install make`

**直接运行等价命令：**

```bash
ruff check src/ tests/
ruff format --check src/ tests/
mypy src/
pytest tests/ -v --cov=src --cov-fail-under=85
```

邀请 AI 入场：

> "请阅读 AGENTS.md，按里面的工作流帮我规划一个功能。"

## 生成的项目结构

```text
my-awesome-project/
├── .harness/                 # 工作区
│   ├── plans/                # 计划文件（JSON Schema）
│   ├── state/                # 状态持久化
│   ├── templates/            # 计划模板
│   ├── logs/                 # 运行日志
│   └── progress.json         # 会话状态（AI 新会话的第一站）
├── configs/                  # 多环境配置
├── docs/
│   ├── context.md            # 深层上下文（架构、约定、任务）
│   └── decisions/            # 架构决策记录（ADR）
├── src/my_awesome_project/
│   ├── cli.py                # 可选 CLI 入口（Typer），如不需要可直接删除或改为模块入口
│   ├── harness/              # 最小可运行骨架（runner/evaluator/state/workflow）
│   ├── agents/               # Agent 接口占位符（需自行实现 LLM 调用）
│   ├── tools/                # 工具函数目录
│   └── utils/                # 通用辅助
├── tests/                    # 测试套件
├── AGENTS.md                 # AI 协作协议（项目级系统提示）
├── Makefile                  # verify / fix / test
├── pyproject.toml            # 依赖 + 工具配置
└── README.md
```

关于 harness/ 和 agents/ 目录：生成的是接口骨架和可运行示例，不是生产级 Agent 运行时。runner.py 能执行 JSON 计划文件，evaluator.py 能按固定维度评分，但任务编排目前只支持串行、无超时控制、无重试机制。你可以在此基础上扩展，也可以完全替换为自己的实现。

## 两种模式对比

| 特性 | 完整模式 | 快速模式 (--quick) |
|------|----------|-------------------|
| AGENTS.md | 完整版（90 行，含审批工作流） | 精简版（30 行，保留核心工作流） |
| Harness 骨架 | ✅ runner + evaluator + state + workflow | ❌ |
| Agent 占位符 | ✅ planner + generator + evaluator | ❌ |
| CI/CD | ✅ GitHub Actions | ❌ |
| IDE 适配 | ✅ CLAUDE.md / .cursorrules / opencode.yaml | ❌ |
| 文档体系 | ✅ context.md / PROJECT_MAP / ADR | ❌ |
| 依赖 | typer + pydantic + pyyaml + rich | 仅 typer |

## 核心价值：降低三类成本

### 上下文对齐成本

AI 进入新项目时，不再需要从零摸索"这里怎么工作"。AGENTS.md + context.md 提供了结构化的入职手册。

### 规范遗忘成本

人类开发者换机器、AI 工具开新会话时，.harness/progress.json 记录了当前阶段和未完成任务，减少重复交代。

### 质量回归成本

`make verify` 把代码风格、单元测试、覆盖率检查固化为不可绕过的命令。Agent 是否主动运行取决于其自律性，但命令本身始终可用且标准统一。

## 使用场景

**适合：**

- 个人开发者用 AI 工具（Claude Code / Cursor / Codex）快速启动 Python 项目（CLI 工具、脚本库、自动化脚本、原型项目等）
- 小团队统一 AI 协作规范（"我们团队的项目都按这个结构来"）
- 需要可验证、可交接的 AI 辅助开发流程

**不适合：**

- 需要确定性自动化的无人值守流水线（PBH 不锁死 Agent 行为）
- 复杂多 Agent 自主协作系统（当前 runner 只支持串行命令执行）
- 非 Python 项目（当前模板仅支持 Python 3.11+）

## 路线图

- **v1.0.0**：Python 项目模板、JSON 计划格式、质量门禁、Quick 模式、PyPI 发布
- **v1.1.0**：多技术栈模板（Node.js / Go）、模板插件系统
- **v1.2.0**：增强 runner 编排能力（超时控制、重试机制）

本项目由个人业余维护，路线图按优先级和社区反馈动态调整。

## 致谢

- [Typer](https://typer.tiangolo.com/) — 优雅的 CLI 框架
- [Ruff](https://docs.astral.sh/ruff/) — 极速 Python Linter
- [Pytest](https://docs.pytest.org/) — 可靠的测试框架

灵感来源：Anthropic 的 Agentic Workflow 与 Context Engineering 实践、OpenAI 的 Harness Engineering 理念

## License

MIT © renjianguojinqianfan
