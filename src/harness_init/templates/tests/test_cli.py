"""Tests for cli.py."""

import json

from typer.testing import CliRunner

from {package_name}.cli import app

runner = CliRunner()


def test_status_shows_stage() -> None:
    """status should show current workflow stage."""
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "Current stage:" in result.output


def test_run_executes_plan(tmp_path) -> None:
    """run should execute a plan and save result."""
    plan = {
        "id": "plan_test",
        "tasks": [
            {"id": "t1", "name": "Hello", "command": "echo hello"},
        ],
    }
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan), encoding="utf-8")

    result = runner.invoke(app, ["run", str(plan_path)])
    assert result.exit_code == 0
    assert "Plan executed:" in result.output
    assert "plan_test" in result.output


def test_evaluate_reads_result(tmp_path) -> None:
    """evaluate should read result and produce feedback."""
    result_data = {
        "plan_id": "plan_test",
        "status": "success",
        "tasks": [
            {"id": "t1", "status": "success", "error": None},
        ],
    }
    result_path = tmp_path / "result.json"
    result_path.write_text(json.dumps(result_data), encoding="utf-8")

    result = runner.invoke(app, ["evaluate", str(result_path)])
    assert result.exit_code == 0
    assert "Score:" in result.output
    assert "Passed:" in result.output
