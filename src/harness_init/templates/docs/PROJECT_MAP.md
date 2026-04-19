---
project: {project_name}
package: {package_name}
version: "0.1.0"
map_type: static
audience: agent
last_updated: "{{generated_date}}"
---

# PROJECT_MAP — {project_name}

> Machine-readable project structure map.
> For the human-readable quick reference, see `AGENTS.md` §6 File Mapping.
> For deep architecture context, see `docs/context.md`.

## 1. Project Overview

| Attribute | Value |
|-----------|-------|
| Name | {project_name} |
| Package | {package_name} |
| Type | cli |
| Language | Python 3.11+ |

**Design philosophy**: Layered architecture with CLI → Core → Agents. Every layer is independently testable. `make verify` is the ground truth for correctness.

## 2. Directory Structure

```
{project_name}/
├── .harness/                    # Agent runtime workspace
│   ├── plans/                   # JSON execution plans (input)
│   ├── eval_feedback/           # Evaluation reports (output)
│   ├── state/                   # Persistent state files
│   ├── templates/               # Plan templates and boilerplate
│   ├── logs/                    # Execution logs
│   └── progress.json            # Session state source of truth
├── configs/                     # Environment-specific configuration
├── docs/                        # Project documentation
│   ├── PROJECT_MAP.md           # This file — machine-readable structure map
│   ├── context.md               # Deep context: architecture, conventions, tasks
│   └── decisions/               # Architecture Decision Records (ADR)
├── src/{package_name}/          # Main application source
│   ├── __init__.py              # Package marker
│   ├── cli.py                   # CLI entry point (thin)
│   ├── agents/                  # Agent role implementations
│   │   ├── __init__.py
│   │   ├── planner.py           # Planning logic
│   │   ├── generator.py         # Code generation logic
│   │   └── evaluator.py         # Evaluation logic
│   ├── harness/                 # Core workflow engine
│   │   ├── __init__.py
│   │   ├── runner.py            # Plan execution orchestrator
│   │   ├── evaluator.py         # Result evaluation engine
│   │   ├── state.py             # State management helpers
│   │   └── workflow.py          # Workflow definitions
│   ├── tools/                   # Tool functions and utilities
│   └── utils/                   # Shared helpers
├── tests/                       # Test suites
│   ├── __init__.py
│   ├── test_cli.py              # CLI tests
│   ├── agents/                  # Mirror src/{package_name}/agents/
│   ├── harness/                 # Mirror src/{package_name}/harness/
│   └── tools/                   # Mirror src/{package_name}/tools/
├── AGENTS.md                    # Agent quick-reference (50–100 lines)
├── Makefile                     # Verify, test, lint commands
├── opencode.yaml                # Codex / OpenCode configuration
├── pyproject.toml               # Project metadata and dependencies
├── README.md                    # Human-facing documentation (中文)
├── README.en.md                 # Human-facing documentation (English)
└── .gitignore                   # VCS exclusions
```

## 3. Key Files

### 3.1 Core Source

| File | Purpose | Agent Notes |
|------|---------|-------------|
| `src/{package_name}/cli.py` | CLI argument parsing and delegation | Keep thin; no business logic |
| `src/{package_name}/agents/planner.py` | Requirement analysis and plan creation | Planner role implementation |
| `src/{package_name}/agents/generator.py` | Code generation from approved plans | Generator role implementation |
| `src/{package_name}/agents/evaluator.py` | Code review and acceptance verification | Evaluator role implementation |
| `src/{package_name}/harness/runner.py` | Loads and executes JSON plans | Orchestrates the Generator |
| `src/{package_name}/harness/evaluator.py` | Evaluates execution results | Orchestrates the Evaluator |
| `src/{package_name}/harness/state.py` | Atomic file I/O for JSON state | write-then-rename pattern |
| `src/{package_name}/harness/workflow.py` | Workflow phase definitions | Phase transitions and guards |

### 3.2 Configuration & Build

| File | Purpose | Agent Notes |
|------|---------|-------------|
| `pyproject.toml` | Dependencies, build config, tool settings | Add new deps in `[project.dependencies]` |
| `Makefile` | `make verify`, `make test`, `make lint` | Always run `make verify` before commit |
| `configs/` | Environment configs (dev, test, prod) | Load via `configparser` or `pydantic-settings` |
| `opencode.yaml` | OpenCode / Codex agent configuration | Custom commands and workflows |

### 3.3 Documentation

| File | Purpose | Agent Notes |
|------|---------|-------------|
| `AGENTS.md` | Quick agent map and rules | Read first on every new session |
| `docs/context.md` | Deep architecture and conventions | Read before architectural decisions |
| `docs/decisions/` | ADR records | One file per major decision |
| `docs/PROJECT_MAP.md` | This file — structure reference | Use for file location lookups |

### 3.4 Runtime Artifacts

| File / Dir | Purpose | Agent Notes |
|------------|---------|-------------|
| `.harness/progress.json` | Session state source of truth | Atomic updates only |
| `.harness/plans/` | JSON execution plans | Created by Planner, consumed by Runner |
| `.harness/eval_feedback/` | Evaluation output | Created by Evaluator, read by human |
| `.harness/logs/` | Execution logs | Append-only, rotated |

## 4. Dependencies

Declared in `pyproject.toml`:

- **Runtime**: `typer`, `pydantic`
- **Dev**: `pytest`, `pytest-cov`, `ruff`
- **Optional**: `mypy` (type checking)

Install all: `pip install -e ".[dev]"`

## 5. Entry Points

| Entry Point | File | Description |
|-------------|------|-------------|
| CLI command | `src/{package_name}/cli.py` | Main user-facing interface |
| Python module | `python -m {package_name}` | Programmatic entry |
| Plan execution | `python -m {package_name} run <plan>` | Execute a JSON plan |
| Evaluation | `python -m {package_name} evaluate <result>` | Evaluate a result file |
| Verification | `make verify` | Run lint + tests (coverage >= 85%) |

## 6. Conventions for Agents

- **File length**: <= 200 lines; refactor early
- **Function length**: <= 30 lines
- **Test mirroring**: Every module in `src/` has a matching test in `tests/`
- **Naming**: `snake_case` modules, `PascalCase` classes, `snake_case` functions
- **State safety**: Use atomic write-then-rename for JSON files
- **Ground truth**: `make verify` output is the only valid correctness signal

---

*This map is static. For current runtime state, see `.harness/progress.json`.*
