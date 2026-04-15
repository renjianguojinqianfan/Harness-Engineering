"""Harness evaluator - minimal runnable version."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class EvaluationResult:
    passed: bool
    score: float
    criteria: dict[str, Any]
    feedback: str


class HarnessEvaluator:
    """Harness evaluator."""

    def __init__(self, feedback_dir: str = ".harness/eval_feedback") -> None:
        self.feedback_dir = Path(feedback_dir)
        self.feedback_dir.mkdir(parents=True, exist_ok=True)

    def evaluate(self, result: dict[str, Any], criteria: dict[str, Any]) -> EvaluationResult:
        """Evaluate execution result."""
        checks = []

        status_check = result.get("status") == "success"
        checks.append(("status", status_check, 40))

        tasks = result.get("tasks", [])
        if tasks:
            completed = sum(1 for t in tasks if t.get("status") == "success")
            completion_rate = completed / len(tasks)
            checks.append(("completion", completion_rate >= 0.8, 30))

        has_errors = any(t.get("error") for t in tasks)
        checks.append(("no_errors", not has_errors, 30))

        score = sum(weight for _, passed, weight in checks if passed)
        passed = score >= criteria.get("min_score", 70)

        feedback_parts = []
        for name, passed_check, weight in checks:
            status = "✓" if passed_check else "✗"
            feedback_parts.append(f"{status} {name} ({weight}pts)")

        return EvaluationResult(
            passed=passed,
            score=score,
            criteria={name: passed_check for name, passed_check, _ in checks},
            feedback="\n".join(feedback_parts),
        )

    def save_feedback(self, plan_id: str, result: EvaluationResult) -> Path:
        """Save evaluation feedback."""
        feedback_path = self.feedback_dir / f"eval_{plan_id}.json"

        feedback_data = {
            "plan_id": plan_id,
            "passed": result.passed,
            "score": result.score,
            "criteria": result.criteria,
            "feedback": result.feedback,
        }

        with open(feedback_path, "w", encoding="utf-8") as f:
            json.dump(feedback_data, f, indent=2)

        return feedback_path


if __name__ == "__main__":
    evaluator = HarnessEvaluator()

    result = {
        "plan_id": "plan_001",
        "status": "success",
        "tasks": [
            {"id": "task_1", "status": "success", "error": None},
            {"id": "task_2", "status": "success", "error": None},
        ],
    }

    criteria = {"min_score": 70}
    eval_result = evaluator.evaluate(result, criteria)
    print(f"Passed: {eval_result.passed}")
    print(f"Score: {eval_result.score}")
    print(f"Feedback:\n{eval_result.feedback}")
    evaluator.save_feedback("plan_001", eval_result)
