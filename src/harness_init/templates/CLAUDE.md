# CLAUDE.md - {project_name}

> **Claude Code / Claude Desktop Quick Reference**
> Full workflow details: `AGENTS.md`

## Project Context

**{project_name}** — {project_description}  
**Maintainer**: {author_name} | **Type**: {project_type}

- Deep context lives in `docs/context.md`
- State of truth: `.harness/progress.json`
- Plans: `.harness/plans/*.json`

## Agent Workflow

Every session MUST declare a role before acting.

### 1. Planner
- Read `docs/context.md`
- Create plan via `.harness/templates/plan_template.json`
- Mark status `proposed`; **wait for human approval**
- No code generation from `proposed` plans

### 2. Generator
- Read approved plan (status: `approved`)
- Implement step-by-step
- Run `make verify` per unit of work
- Update `.harness/progress.json`

### 3. Evaluator
- Review implementation against plan
- Verify acceptance criteria
- Run `make verify`; loop back if issues found
- Sign off: mark plan `completed`

## Constraints

| Rule | Limit |
|------|-------|
| Function length | <= 30 lines |
| File length | <= 200 lines |
| Test coverage | >= 85% (enforced by `pytest-cov`) |
| Auto-fix attempts | Max 2 per error, then rollback |
| One session | One atomic task |

## Common Commands

```bash
make verify    # lint (ruff) + tests (pytest), coverage >= 85%
make fix       # auto-fix linting; MUST re-run `make verify` after
```

## Quick Rules

- **DO** read `docs/context.md` before architectural decisions
- **DO** run `make verify` after every change; never skip Evaluator
- **DON'T** commit failing code; don't fix unrelated code during task
- **DON'T** add abstractions for single-use cases
- **DON'T** execute shell commands without human review

## Reference

| File | Purpose |
|------|---------|
| `AGENTS.md` | Full workflow, change control matrix, security guidelines |
| `docs/context.md` | Architecture, conventions, task backlog |
| `.harness/progress.json` | Session state and current task status |
