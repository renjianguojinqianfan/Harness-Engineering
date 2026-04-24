# AGENTS.md - {project_name}

> Keep this file to 80 lines or fewer. For deeper context, see `docs/context.md`.

## 1. Project Snapshot

**{project_name}** — {project_description}

**Maintainer**: {author_name}
**Type**: {project_type}

## 2. Quick Start (30 seconds)

1. Run `make verify` — confirm your environment is working
2. Run the test command — ensure existing tests pass
3. Locate the entry point — understand how the program runs

## 3. Multi-Agent Notice

This project supports multiple agents working concurrently. All agents share the rules in this file.

- If multiple agents are active, each should use an independent git worktree
- If you detect another agent modifying the same file, wait or choose a different task
- Check `.harness/progress.json` for the current project phase before starting work

## 4. Working Guidelines

You are a senior software engineer working in this project. Your code will be reviewed by peers.

### Before You Start

- Read `.harness/progress.json` to understand the current project phase and context
- Run `make verify` — the baseline must be clean before any change

### When Making Changes

- Before modifying code, state your plan clearly in the conversation:
  - What you intend to change
  - Why this change is needed
  - What parts of the project may be affected
- Keep each session focused on one atomic task. If the task scope grows, break it down first

### After You Finish

- Verify your changes against the task's acceptance criteria
- Run `make verify` to ensure quality gates are met
- If you find issues unrelated to your task, note them but do not fix them in the same session

### When You're Unsure

- Check `docs/decisions/` for relevant architecture decisions
- Check `docs/context.md` for deeper project context
- If you still cannot find the answer, ask the maintainer rather than assuming

### Code Quality

- All public APIs must have complete type hints and docstrings
- Follow the existing code style in the files you modify. When in doubt, look at nearby code
- Do not introduce abstractions for single-use cases

## 5. Critical Rules

- **Never commit code that fails `make verify`**
- Test coverage must remain at or above the threshold defined in the project
- Follow the project's existing code style; style rules are enforced by the linter configured in the Makefile
- One session, one atomic task
- **Auto-fix circuit breaker**: Max 2 attempts per error, then step back and re-evaluate
- **Self-evaluation ban**: Only `make verify` output is ground truth

## 6. Security Guidelines

- Never hardcode secrets. Use environment variables or `.env` files (`.env` is in `.gitignore`)
- All shell commands must be reviewed before execution
- Dependency changes must pass `make verify`; do not introduce unscanned third-party packages
- Changes to sensitive files (keys, configuration) require extra caution

## 7. Key Constraints

- Function length: 30 lines or fewer
- File length: 200 lines or fewer
- State safety: use atomic write-then-rename for persistent files
- Test coverage threshold is enforced by the test runner configured in the Makefile

## 8. File Mapping

| Location | Purpose |
|----------|---------|
| `src/` | Main application code |
| `tests/` | Tests (mirrors `src/` structure) |
| `docs/` | Documentation and architecture decisions |
| `tasks/` | Task breakdown (Spec Coding container) |
| `.harness/` | Project phase tracking and workspace isolation |

## 9. Commands

| Command | What it does |
|---------|--------------|
| `make verify` | Full quality check (lint + tests + coverage). Must pass before commit |
| `make test` | Run tests only |
| `make lint` | Run code style checks only |
| `make fix` | Auto-fix style issues where possible |