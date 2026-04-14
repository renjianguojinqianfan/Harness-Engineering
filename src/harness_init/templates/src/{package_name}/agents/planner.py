"""Planner agent stub."""
from typing import Any


class PlannerAgent:
    """Create execution plans from goals."""

    def create_plan(self, goal: str) -> dict[str, Any]:
        """Return a simple plan dict with tasks list."""
        return {
            "id": "plan_001",
            "name": goal,
            "tasks": [
                {
                    "id": "task_1",
                    "name": "Initialize",
                    "command": "echo 'init'",
                },
                {
                    "id": "task_2",
                    "name": "Execute goal",
                    "command": f"echo '{goal}'",
                },
            ],
        }
