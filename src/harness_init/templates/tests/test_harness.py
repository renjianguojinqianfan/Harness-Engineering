"""Tests for harness core modules."""

import asyncio
import json
from pathlib import Path

from {package_name}.agents.evaluator import EvaluatorAgent
from {package_name}.agents.generator import GeneratorAgent
from {package_name}.agents.planner import PlannerAgent
from {package_name}.harness.evaluator import EvaluationResult, HarnessEvaluator
from {package_name}.harness.runner import HarnessRunner, TaskStatus
from {package_name}.harness.state import StateManager
from {package_name}.harness.workflow import Stage, get_allowed_transitions, get_next_stage


class TestRunner:
    """Tests for HarnessRunner."""

    def test_task_status_enum(self) -> None:
        """TaskStatus should have expected values."""
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.SUCCESS.value == "success"

    def test_run_plan_success(self, tmp_path: Path) -> None:
        """run_plan should execute all tasks successfully."""
        plan = {
            "id": "plan_1",
            "tasks": [
                {"id": "t1", "name": "A", "command": "echo a"},
                {"id": "t2", "name": "B", "command": "echo b"},
            ],
        }
        plan_path = tmp_path / "plan.json"
        plan_path.write_text(json.dumps(plan), encoding="utf-8")

        runner = HarnessRunner(plans_dir=str(tmp_path))
        result = asyncio.run(runner.run_plan(str(plan_path)))

        assert result["status"] == "success"
        assert len(result["tasks"]) == 2
        assert all(t["status"] == "success" for t in result["tasks"])

    def test_run_plan_stop_on_error(self, tmp_path: Path) -> None:
        """run_plan should stop on error when configured."""
        plan = {
            "id": "plan_2",
            "stop_on_error": True,
            "tasks": [
                {"id": "t1", "name": "A", "command": "echo a"},
            ],
        }
        plan_path = tmp_path / "plan.json"
        plan_path.write_text(json.dumps(plan), encoding="utf-8")

        runner = HarnessRunner(plans_dir=str(tmp_path))
        result = asyncio.run(runner.run_plan(str(plan_path)))
        assert result["status"] == "success"


class TestEvaluator:
    """Tests for HarnessEvaluator."""

    def test_evaluate_pass(self, tmp_path: Path) -> None:
        """evaluate should pass for successful result."""
        evaluator = HarnessEvaluator(feedback_dir=str(tmp_path))
        result = {
            "plan_id": "p1",
            "status": "success",
            "tasks": [
                {"id": "t1", "status": "success", "error": None},
            ],
        }
        eval_result = evaluator.evaluate(result, {"min_score": 70})
        assert eval_result.passed is True
        assert eval_result.score == 100

    def test_evaluate_fail_low_completion(self, tmp_path: Path) -> None:
        """evaluate should fail if completion rate is low."""
        evaluator = HarnessEvaluator(feedback_dir=str(tmp_path))
        result = {
            "plan_id": "p1",
            "status": "failed",
            "tasks": [
                {"id": "t1", "status": "failed", "error": "oops"},
            ],
        }
        eval_result = evaluator.evaluate(result, {"min_score": 70})
        assert eval_result.passed is False

    def test_save_feedback(self, tmp_path: Path) -> None:
        """save_feedback should write JSON file."""
        evaluator = HarnessEvaluator(feedback_dir=str(tmp_path))
        er = EvaluationResult(passed=True, score=100, criteria={}, feedback="ok")
        path = evaluator.save_feedback("p1", er)
        assert path.exists()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["passed"] is True


class TestState:
    """Tests for StateManager."""

    def test_get_set(self, tmp_path: Path) -> None:
        """get and set should persist values."""
        state_path = tmp_path / "state.json"
        state = StateManager(str(state_path))
        state.set("key", "value")
        assert state.get("key") == "value"

        state2 = StateManager(str(state_path))
        assert state2.get("key") == "value"

    def test_default(self, tmp_path: Path) -> None:
        """get should return default for missing keys."""
        state_path = tmp_path / "state.json"
        state = StateManager(str(state_path))
        assert state.get("missing", "default") == "default"


class TestWorkflow:
    """Tests for workflow transitions."""

    def test_get_next_stage(self) -> None:
        """get_next_stage should return default next stage."""
        assert get_next_stage(Stage.FEEDBACK) == Stage.TRIAGE
        assert get_next_stage(Stage.EXECUTE) == Stage.EVALUATE
        assert get_next_stage(Stage.EVALUATE) == Stage.DONE

    def test_get_allowed_transitions(self) -> None:
        """get_allowed_transitions should return all allowed stages."""
        assert Stage.PLAN in get_allowed_transitions(Stage.CLARIFY)
        assert Stage.DONE in get_allowed_transitions(Stage.EVALUATE)
        assert Stage.PLAN in get_allowed_transitions(Stage.EVALUATE)


class TestAgents:
    """Tests for agent stubs."""

    def test_planner_create_plan(self) -> None:
        """PlannerAgent should return a plan dict."""
        planner = PlannerAgent()
        plan = planner.create_plan("test goal")
        assert "tasks" in plan
        assert plan["name"] == "test goal"

    def test_generator_generate(self) -> None:
        """GeneratorAgent should return a placeholder string."""
        generator = GeneratorAgent()
        result = generator.generate({"name": "test_task"})
        assert "test_task" in result

    def test_evaluator_evaluate(self) -> None:
        """EvaluatorAgent should return pass/fail dict."""
        evaluator = EvaluatorAgent()
        result = evaluator.evaluate({"status": "success"})
        assert "passed" in result
