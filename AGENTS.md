# AGENTS.md - harness-init

> 这是 `harness-init` 项目本身的 Agent 操作手册。如果你是打开生成后项目的 Agent，请阅读该目录下的 `AGENTS.md`。

## 项目目标

构建 `harness-init` CLI 工具，用于快速初始化符合 Harness Engineering 规范的完整项目。生成的项目必须非空壳，可直接通过 `make verify`。

## 技术栈

- Python 3.11+
- CLI 框架：`typer`
- 测试：`pytest` + `pytest-cov`（覆盖率 ≥ 85%）
- 代码检查：`ruff`

## 目录结构

```
src/harness_init/
├── cli.py          # CLI 入口（仅参数解析，调用 core.py）
├── core.py         # 核心逻辑（生成目录、复制模板、初始化 Git、回滚）
└── templates/      # 目标项目模板（AGENTS.md、Makefile、runner.py、evaluator.py 等）
tests/              # 单元测试，与 src 结构对应
```

## 架构铁律（修改时不可违反）

1. `cli.py` **只负责**参数解析和调用 `core.py`
2. `core.py` **处理所有**文件生成和 Git 初始化逻辑
3. `templates/` **存放所有**目标项目的模板文件；长模板优先作为独立文件存放，避免 `core.py` 超过 200 行
4. 所有核心逻辑**必须有**单元测试
5. 每个函数 ≤ 30 行，每个文件 ≤ 200 行

## 开发流程

- 使用 **Sisyphus** 主编排任务
- 每完成一个子任务，**必须**运行 `make verify` 验证
- 测试覆盖率不达标时**禁止**提交

## 常用命令

| 命令 | 说明 |
|------|------|
| `make verify` | 项目验收标准：lint + test |
| `make test` | `pytest`，要求覆盖率 ≥ 85% |
| `make lint` | `ruff check src/` |
| `make install` | `pip install -e .` |

## 关键实现细节

- 生成的项目 CLI 使用 `typer.Typer()` 多命令模式（`run` / `evaluate` / `status`）
- `_init_git()` 会自动配置本地 `user.name` 和 `user.email`，不依赖全局 Git 配置
- 模板目录 `src/harness_init/templates/` 已被根 `pyproject.toml` 的 ruff 配置排除
- Windows 兼容：路径遍历防护、Git 失败自动回滚、模板渲染支持二进制文件

## 环境要求

- 首次开发前必须执行：`pip install -e .`（或 `make install`）
- 系统中必须安装 `git`，`core.py` 会调用 `git init` 和 `git commit`
- Windows 下 `make` 不可用时，可运行等价命令：
  - `ruff check src/`
  - `pytest tests/ -v --cov=src --cov-fail-under=85`
