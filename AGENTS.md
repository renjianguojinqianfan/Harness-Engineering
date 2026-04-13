# AGENTS.md - harness-init

## 项目目标
构建 `harness-init` CLI 工具，用于快速初始化符合 Harness Engineering 规范的空项目。

## 技术栈
- Python 3.11+
- CLI 框架：`typer`
- 测试：`pytest` + `pytest-cov`（覆盖率 ≥ 85%）
- 代码检查：`ruff`

## 常用命令
| 命令 | 说明 |
|------|------|
| `make verify` | 运行 lint + test（项目验收标准） |
| `make test` | 运行 pytest，要求覆盖率 ≥ 85% |
| `make lint` | ruff 检查 `src/` |
| `make install` | `pip install -e .` |

## 目录结构约定
```
src/harness_init/
├── cli.py          # CLI 入口
├── core.py         # 核心逻辑
└── templates/      # 项目模板资源（生成目标项目的文件模板）
tests/              # 单元测试，与 src 结构对应
```

## 架构铁律
1. `cli.py` 只负责参数解析和调用 `core.py`
2. `core.py` 处理所有文件生成和 Git 初始化逻辑
3. `templates/` 存放目标项目的模板文件（AGENTS.md、Makefile、.gitignore 等）
4. 所有核心逻辑必须有单元测试
5. 每个函数 ≤ 30 行，每个文件 ≤ 200 行

## 开发流程
- 使用 **Sisyphus** 主编排任务
- 每完成一个子任务，必须运行 `make verify` 验证
- 测试覆盖率不达标时禁止提交

## 已知问题与环境提示
- 当前根目录的 Makefile 文件名为 `Makeflie`（拼写错误），执行 make 命令前需修正为 `Makefile`。
- Windows 环境下可能未安装 `make`，可直接运行等价命令：
  - `ruff check src/`（lint）
  - `pytest tests/ -v --cov=src --cov-fail-under=85`（test）
- 首次开发前请确保已安装依赖：`pip install -e .`（或通过 `make install`）
