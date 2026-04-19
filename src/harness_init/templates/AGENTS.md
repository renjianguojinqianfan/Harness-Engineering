# AGENTS.md - {project_name}

> **Principle**: Keep this file to 50-100 lines. Deep context lives in `docs/context.md`.

## 1. Project Snapshot

**{project_name}** is a harness-ready project. {project_description}

**Maintainer**: {author_name}  
**Type**: {project_type}

## 2. Change Control Matrix (Feedforward)

| Error Type | Rollback Level | Mechanical Guard |
|------------|----------------|------------------|
| Requirement error | Re-clarify in `docs/context.md` | **FROZEN**: No spec change without PRD update |
| Design error | Update architecture decision | No code without ADR in `docs/decisions/` |
| Code error | Fix directly | `make verify` must pass; auto-fix <= 2 attempts |

## 3. Session Protocol

**One session = One atomic task**

1. **Orient**: Read `.harness/progress.json`
2. **Verify Baseline**: Run `make verify` → must pass before any edit
3. **Select Task**: Pick ONE item from `.harness/plans/*.json` → mark `in_progress`
4. **Implement**: Generate code → auto-trigger `make verify`
5. **Commit**: Write commit → update `.harness/progress.json`

## 4. Approval Workflow

All plans MUST pass human approval before execution.

| Status | Meaning | Gate |
|--------|---------|------|
| `proposed` | Plan drafted, awaiting review | Agent creates, human reviews |
| `approved` | Human approved, ready to implement | Human explicitly approves |
| `rejected` | Needs revision | Return to Planner |
| `completed` | Implemented and verified | Evaluator signs off |

**Rule**: No code generation from `proposed` plans. Human approval is mandatory.

## 5. Three-Role Workflow

Every session MUST declare its role before acting.

- **Planner**: Read `docs/context.md`, create plan via `.harness/templates/plan_template.json`, wait for approval
- **Generator**: Read approved plan, implement step-by-step, run `make verify` per unit, update `progress.json`
- **Evaluator**: Review against plan, verify acceptance criteria, run `make verify`, loop back if issues found

## 6. Security Guidelines

- **禁止自动执行未审查命令** — 所有 shell 命令须经人类审查后方可执行
- Secrets 禁止硬编码；使用环境变量或 `.env` 文件（已加入 `.gitignore`）
- 依赖变更须经 `make verify` 验证；禁止引入未扫描的第三方包
- 敏感文件（密钥、配置）修改需额外人工确认

## 7. Agent Rules

- **DO** read `docs/context.md` before architectural decisions
- **DO** run `make verify` after every change; Evaluator MUST NOT be skipped
- **DO** use `shlex.quote` and `subprocess.run(check=True)` for commands
- **DON'T** commit failing code; DON'T fix unrelated code during task
- **DON'T** add abstractions for single-use cases
- **DON'T** put deep context in this file

## 8. Key Constraints

- Code style: PEP 8, enforced by `ruff`
- Test coverage: >= 85%, enforced by `pytest-cov`
- Function length: <= 30 lines; File length: <= 200 lines
- State safety: atomic write-then-rename for JSON files
- **Auto-fix circuit breaker**: Max 2 attempts per error, then rollback
- **Agent self-evaluation ban**: ONLY `make verify` output is ground truth

## 9. File Mapping

| Type | Location | Description |
|------|----------|-------------|
| Source | `src/{package_name}/` | Main application code |
| Tests | `tests/` | Mirror `src/` structure |
| Plans | `.harness/plans/` | JSON execution plans |
| State | `.harness/progress.json` | Session state source of truth |
| Feedback | `.harness/eval_feedback/` | Evaluation reports |
| Context | `docs/context.md` | Architecture, conventions, tasks |
| Entry | `src/{package_name}/cli.py` | CLI entry point |

## 10. Commands

- `make verify`: Lint (`ruff`) + tests (`pytest`), coverage >= 85%
- `make fix`: Auto-fix linting; MUST re-run `make verify` after

## 11. Meta-Loop Validation

When used as harness template:
1. Verify `.harness/` structure inherited correctly
2. Test secondary heredity
3. Isomorphism check: directory similarity > 95%
4. Quality gate: `make verify` passes + `HARNESS_REPORT.md` generated
