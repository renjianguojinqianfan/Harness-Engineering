"""Evaluator agent stub."""
from typing import Any


class EvaluatorAgent:
    """Evaluate results and return pass/fail dict."""

    def evaluate(self, result: dict[str, Any]) -> dict[str, Any]:
        """Return a simple pass/fail evaluation dict."""
        status = result.get("status", "failed")
        passed = status == "success"
        return {
            "passed": passed,
            "score": 100.0 if passed else 0.0,
            "feedback": "All checks passed." if passed else "Execution failed.",
        }
