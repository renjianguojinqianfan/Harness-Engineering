# harness-init

快速初始化符合 Harness Engineering 规范的**完整 Harness Engineering 项目**。

## 安装

```bash
git clone https://github.com/renjianguojinqianfan/Harness-Engineering.git
cd Harness-Engineering
pip install -e ".[dev]"
```

## 使用

```bash
harness-init my-project
```

执行后会在当前目录创建 `my-project/`，包含：
- 完整的 Python 包结构（`src/my_project/`）
- Harness 核心引擎（`src/my_project/harness/runner.py`、`evaluator.py`、`state.py`、`workflow.py`）
- 智能体 stubs（`src/my_project/agents/planner.py`、`generator.py`、`evaluator.py`）
- 运行时目录（`.harness/plans/`、`.harness/eval_feedback/`、`.harness/state/`、`.harness/logs/`）
- 多命令 CLI（`run`、`evaluate`、`status`）
- `configs/`（dev/test/prod）、`docs/context.md`、`AGENTS.md`
- `pyproject.toml`、`Makefile`、`.gitignore`、`opencode.yaml`
- 自动初始化的 Git 仓库和初始提交

进入生成的项目即可运行验证：

```bash
cd my-project
pip install -e ".[dev]"
make verify
```

## 开发命令

| 命令 | 说明 |
|------|------|
| `make verify` | 运行 ruff + pytest（覆盖率 ≥ 85%） |
| `make test` | 运行 pytest |
| `make lint` | 运行 ruff |
| `make install` | `pip install -e ".[dev]"` |

## 要求

- Python 3.11+
- Git

## 架构

- `src/harness_init/cli.py` — CLI 入口
- `src/harness_init/core.py` — 项目生成逻辑
- `src/harness_init/templates/` — 目标项目的模板文件
