# Project-Bootstrap-Harness (PBH)

> A **Python project protocol template** designed for AI-assisted development.
> 
> It doesn't tell AI how to write code. Instead, from the very first second a project is born, it writes down "how we collaborate here" as a machine-readable contract.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/badge/pypi-harness--init-green.svg)](https://pypi.org/project/harness-init/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Why This Exists

When coding with Claude Code, Cursor, or Codex, you've likely hit these friction points:

- **Repeating rules in every new session**: "Remember to run tests", "Don't touch unrelated files", "Plan before coding"
- **AI writes code but never verifies it**: Small errors snowball, and humans end up cleaning the mess
- **Inconsistent AI direction across the team**: Colleague A tells AI to edit directly, Colleague B asks for a proposal first—code style becomes chaos

**The problem isn't that AI isn't smart enough. It's that the project itself lacks a "default collaboration protocol."**

PBH plants that protocol, quality gates, and state tracking into your project the moment you run `harness-init my-project`. From then on, any AI tool opening this project knows within one minute: what the workflow is, where the quality baseline sits, and what the last person (or AI) was doing.

---

## What It Does (and Doesn't Do)

### ✅ It's a "Collaboration Contract"

- **`AGENTS.md`**: A 50-100 line project-level system prompt defining the Planner → Generator → Evaluator workflow, change control matrix, and security guidelines
- **`docs/context.md`**: Deep context (architecture overview, naming conventions, common tasks)
- **`.harness/progress.json`**: Cross-session state tracking, helping AI resume context quickly in new sessions  
  (Example: `{"current_stage": "plan", "plans": [{"id": "plan_001", "status": "approved"}], "last_updated": "2026-04-20T12:00:00Z"}`)

### ✅ It's Quality Gate Infrastructure

- **`make verify`**: One-command runs ruff + pytest with ≥85% coverage threshold
- **GitHub Actions CI**: Checks run on every push
- **Git Hooks**: Catches style issues before commits

### ✅ It Includes Extensible Skeleton Code

Generated projects contain minimal runnable Harness components:
- `harness/runner.py`: Asynchronously executes command steps defined in JSON plan files (serial orchestration + single-task error halting)
- `harness/evaluator.py`: Three-dimensional scoring based on execution results (status/completion rate/errors)
- `harness/state.py`: Atomic JSON state reads/writes (`tempfile` + `os.replace` ensures write safety)
- `harness/workflow.py`: Seven-stage state machine (Feedback → Triage → Clarify → Plan → Execute → Evaluate → Done)

### ❌ It's NOT an Agent Runtime

PBH **does not enforce** agent behavior. It won't stop an AI from skipping Planner and writing code directly, nor will it automatically advance workflow states. It provides **protocols and tools**—whether an agent follows them depends on the agent tool's comprehension and human supervision.

### ❌ It's NOT a Code Generator

PBH does not generate business logic from natural language descriptions. It generates **project structure, configuration files, and interface skeletons**. The business logic is up to you (or your AI) to fill in.

---

## Quick Start

```bash
pip install harness-init

# Full mode (includes CI, IDE adapters, docs, Harness skeleton)
harness-init my-awesome-project

# Quick mode (minimal, 5-minute onboarding)
harness-init my-project --quick --yes
```

Enter the project and verify:

```bash
cd my-awesome-project
pip install -e ".[dev]"
make verify        # Should output ✔ Verification passed
```

### 💡 If make is not available

Windows users may not have make installed. If you see 'make' is not recognized, you can:

**Install make:**

- Windows: Install GnuWin32 Make or `winget install GnuWin32.Make`
- macOS: `xcode-select --install`
- Linux: `sudo apt install make`

**Run equivalent commands directly:**

```bash
ruff check src/ tests/
ruff format --check src/ tests/
mypy src/
pytest tests/ -v --cov=src --cov-fail-under=85
```

Invite AI to the party:

> "Please read AGENTS.md and help me plan a feature following the workflow defined there."

## Generated Project Structure

```text
my-awesome-project/
├── .harness/                 # Workspace
│   ├── plans/                # Plan files (JSON Schema)
│   ├── state/                # Persistent state
│   ├── templates/            # Plan templates
│   ├── logs/                 # Execution logs
│   └── progress.json         # Session state (AI's first stop in new sessions)
├── configs/                  # Multi-environment configs
├── docs/
│   ├── context.md            # Deep context (architecture, conventions, tasks)
│   └── decisions/            # Architecture Decision Records (ADR)
├── src/my_awesome_project/
│   ├── cli.py                # Optional CLI entry (Typer); delete or repurpose if not needed
│   ├── harness/              # Minimal runnable skeleton (runner/evaluator/state/workflow)
│   ├── agents/               # Agent interface placeholders (implement LLM calls yourself)
│   ├── tools/                # Utility functions
│   └── utils/                # Common helpers
├── tests/                    # Test suite
├── AGENTS.md                 # AI collaboration protocol (project-level system prompt)
├── Makefile                  # verify / fix / test
├── pyproject.toml            # Dependencies + tool configs
└── README.md
```

About harness/ and agents/ directories: These are interface skeletons and runnable examples, not production-grade agent runtimes. runner.py can execute JSON plan files, and evaluator.py scores against fixed dimensions, but orchestration is currently serial-only with no timeout controls or retry mechanisms. You can extend them or replace them entirely.

## Mode Comparison

| Feature | Full Mode | Quick Mode (--quick) |
|---------|-----------|---------------------|
| AGENTS.md | Full (90 lines, incl. approval workflow) | Minimal (30 lines, core workflow only) |
| Harness skeleton | ✅ runner + evaluator + state + workflow | ❌ |
| Agent placeholders | ✅ planner + generator + evaluator | ❌ |
| CI/CD | ✅ GitHub Actions | ❌ |
| IDE adapters | ✅ CLAUDE.md / .cursorrules / opencode.yaml | ❌ |
| Documentation | ✅ context.md / PROJECT_MAP / ADR | ❌ |
| Dependencies | typer + pydantic + pyyaml + rich | typer only |

## Core Value: Reducing Three Types of Friction

### Context Alignment Cost

When AI enters a new project, it no longer has to figure out "how things work here" from scratch. AGENTS.md + context.md provide a structured onboarding manual.

### Spec Drift Cost

When developers switch machines or AI tools start fresh sessions, .harness/progress.json records the current stage and pending tasks, reducing repetitive explanations.

### Quality Regression Cost

`make verify` hardens code style, unit tests, and coverage checks into a non-optional command. Whether an agent runs it proactively depends on its discipline, but the command itself is always available and consistent.

## Use Cases

**Good for:**

- Individual developers using AI tools (Claude Code / Cursor / Codex) to quickly bootstrap Python projects (CLI tools, script libraries, automation scripts, prototypes, etc.)
- Small teams unifying AI collaboration standards ("All our projects follow this structure")
- AI-assisted development workflows that require verifiability and handoff clarity

**Not ideal for:**

- Deterministic automation pipelines requiring guaranteed execution (PBH doesn't lock down agent behavior)
- Complex multi-agent autonomous systems (current runner only supports serial command execution)
- Non-Python projects (current templates only support Python 3.11+)

## Roadmap

- **v1.0.0**: Python project template, JSON plan format, quality gates, Quick mode, PyPI release
- **v1.1.0**: Multi-stack templates (Node.js / Go), template plugin system
- **v1.2.0**: Enhanced runner orchestration (timeout controls, retry mechanisms)

This project is maintained by an individual in spare time. The roadmap adjusts dynamically based on priorities and community feedback.

## Acknowledgments

- [Typer](https://typer.tiangolo.com/) — Elegant CLI framework
- [Ruff](https://docs.astral.sh/ruff/) — Blazingly fast Python linter
- [Pytest](https://docs.pytest.org/) — Reliable testing framework

Inspiration: Anthropic's Agentic Workflow and Context Engineering practices, OpenAI's Harness Engineering philosophy

## License

MIT © renjianguojinqianfan
