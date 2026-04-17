# Plan: [Task Name]

## Goal

One-sentence description of the task objective.

## Context

Relevant background information, dependencies, constraints.

## Steps

1. [ ] Step one description
2. [ ] Step two description
3. [ ] Step three description

## Affected Files

- `path/to/file.py` — description of change
- `path/to/new_file.py` — new file to create

## Acceptance Criteria

- [ ] `make verify` passes (ruff + pytest, coverage >= 85%)
- [ ] Specific behavioral criterion 1
- [ ] Specific behavioral criterion 2

## Rollback Plan

If issues arise:
1. Revert the last commit: `git reset --hard HEAD~1`
2. Or manually undo changes in affected files
3. Re-run `make verify` to confirm clean state