"""Generator agent stub."""
from typing import Any


class GeneratorAgent:
    """Generate artifacts from tasks."""

    def generate(self, task: dict[str, Any]) -> str:
        """Return a placeholder generated string."""
        task_name = task.get("name", "unknown")
        return f"# Generated output for task: {task_name}\n"
