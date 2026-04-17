# harness-init

[![PyPI version](https://badge.fury.io/py/harness-init.svg)](https://badge.fury.io/py/harness-init)
[![Python Version](https://img.shields.io/pypi/pyversions/harness-init.svg)](https://pypi.org/project/harness-init/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A CLI tool to scaffold complete, ready-to-run Python projects that follow **Harness Engineering** conventions. Every generated project ships with a working harness core, agent stubs, test suites, and a validation pipeline — it passes `make verify` immediately after creation.

## Features

- **One-command scaffolding**: Package structure, CLI, tests, harness runtime, and Git initialization, all done automatically
- **Generate-and-verify**: Every project includes `make verify` (ruff + pytest with coverage >= 85%)
- **Agent-friendly**: Generated projects come with an enhanced `AGENTS.md` (with Planner / Generator / Evaluator three-role workflow), a standard plan template at `.harness/templates/plan_template.md`, state tracking via `.harness/progress.json`, plus `docs/context.md` and `opencode.yaml`, so external agents can understand the structure and workflow right away
- **Safe and robust**: Project name validation, path traversal protection, automatic rollback on Git failure, and atomic state writes
- **Bilingual documentation**: Generated projects include both Chinese and English README files for international collaboration
- **Modular design**: The generated `harness` core engine includes `runner`, `evaluator`, `state`, and `workflow` components, ready to use out of the box

## Installation

```bash
pip install harness-init
```

Or install from source:

```bash
git clone https://github.com/renjianguojinqianfan/Project-Bootstrap-Harness.git
cd Project-Bootstrap-Harness
pip install -e ".[dev]"
```

## Quick Start

```bash
# Create a new project
harness-init my-project

# Enter and verify
cd my-project
pip install -e ".[dev]"
make verify
```

After execution, `my-project/` will be created with:

- Full Python package structure (`src/my_project/`)
- Harness core engine: `runner.py` (task execution), `evaluator.py` (result evaluation), `state.py` (state persistence), `workflow.py` (workflow definition)
- Agent stubs: `planner.py`, `generator.py`, `evaluator.py`
- Runtime directories: `.harness/plans/`, `.harness/eval_feedback/`, `.harness/state/`, `.harness/templates/plan_template.md`, `.harness/progress.json`
- Multi-command CLI: `run`, `evaluate`, `status`
- `configs/` (dev/test/prod), `docs/context.md`, `docs/decisions/`, `AGENTS.md` (with three-role workflow), `opencode.yaml`
- `pyproject.toml`, `Makefile`, `.gitignore`, `README.md`, `README.en.md`
- Auto-initialized Git repository with an initial commit

## Generated Project Structure

```
my-project/
├── .harness/                 # Harness runtime directory
│   ├── plans/                # Execution plans
│   ├── eval_feedback/        # Evaluation feedback
│   ├── state/                # State persistence
│   ├── templates/            # Template files
│   │   └── plan_template.md  # Standard agent plan template
│   ├── logs/                 # Runtime logs
│   └── progress.json         # Task progress (current_stage, plans, last_updated)
├── configs/                  # Multi-environment config (dev/test/prod)
├── docs/                     # Documentation
│   ├── context.md            # Agent context
│   └── decisions/            # Architecture decision records
├── src/my_project/           # Main package
│   ├── __init__.py
│   ├── cli.py                # CLI entry point
│   ├── harness/              # Core engine
│   │   ├── runner.py
│   │   ├── evaluator.py
│   │   ├── state.py
│   │   └── workflow.py
│   ├── agents/               # Agent stubs
│   │   ├── planner.py
│   │   ├── generator.py
│   │   └── evaluator.py
│   ├── tools/                # Tool functions
│   └── utils/                # Utility helpers
├── tests/                    # Tests
├── .gitignore
├── AGENTS.md                 # Agent quick reference
├── opencode.yaml             # Workflow configuration
├── Makefile
├── pyproject.toml
├── README.md                 # Chinese documentation
└── README.en.md              # English documentation
```

## CLI Options

```bash
harness-init [OPTIONS] PROJECT_NAME
```

| Option | Short | Description |
|--------|-------|-------------|
| `--force` | `-f` | Force overwrite of an existing directory (old one is auto-backed up) |
| `--no-git` | | Skip Git initialization |
| `--yes` | `-y` | Skip all interactive prompts and use defaults |
| `--version` | `-v` | Show version number |

### Project Name Rules

To produce a valid Python package, the project name must:
- Start with a letter or underscore
- Contain only letters, digits, hyphens (`-`), and underscores (`_`)
- Not be empty, contain spaces, path separators, or `..`

**Valid examples**: `my-project`, `my_project`, `harness_v2`  
**Invalid examples**: `123project` (starts with a digit), `my project` (contains a space), `foo/../bar` (path traversal)

## Development Commands (for harness-init itself)

| Command | Description |
|---------|-------------|
| `make verify` | Run ruff + pytest (coverage >= 85%) |
| `make test` | Run pytest |
| `make lint` | Run ruff |
| `make install` | `pip install -e .` |

## Why Generated Projects Are Agent-Friendly

Generated projects are designed for external agents:

- **`AGENTS.md`**: Quick map with Planner / Generator / Evaluator three-role mandatory workflow so agents know exactly which role to play
- **`docs/context.md`**: Deep context with architecture details, naming conventions, and common task examples
- **`opencode.yaml`**: Explicit seven-stage workflow configuration
- **`.harness/templates/plan_template.md`**: Standard Markdown plan template for agents to copy and fill in
- **`.harness/progress.json`**: Task progress tracking (current_stage, plans, last_updated) to support multi-turn conversation breakpoints
- **`make verify`**: Unified validation entry point; agents get immediate quality feedback after any change

## Architecture

- `src/harness_init/cli.py` — CLI entry point (argument parsing)
- `src/harness_init/core.py` — Core project generation logic (validation, copying, rendering, Git initialization, rollback)
- `src/harness_init/_utils.py` — Name validation, template rendering, and utility helpers
- `src/harness_init/_git.py` — Git initialization and rollback helpers
- `src/harness_init/templates/` — Template files for the generated project

## License

MIT License

---

[Chinese Version](README.md)
