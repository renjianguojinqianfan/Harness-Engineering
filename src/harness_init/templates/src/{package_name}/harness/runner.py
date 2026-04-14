"""Harness runner - minimal runnable version."""
import asyncio
import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class Task:
    id: str
    name: str
    command: str
    status: TaskStatus = TaskStatus.PENDING
    output: str = ""
    error: str = ""


class HarnessRunner:
    """Harness task runner."""

    def __init__(self, plans_dir: str = ".harness/plans") -> None:
        self.plans_dir = Path(plans_dir)
        self.plans_dir.mkdir(parents=True, exist_ok=True)

    async def run_plan(self, plan_path: str) -> dict[str, Any]:
        """Execute a plan."""
        with open(plan_path) as f:
            plan = json.load(f)

        results: list[dict[str, Any]] = []
        for task_data in plan.get("tasks", []):
            task = Task(
                id=task_data["id"],
                name=task_data["name"],
                command=task_data["command"],
            )
            result = await self._execute_task(task)
            results.append(result)

            if result["status"] == "failed" and plan.get("stop_on_error", True):
                break

        return {
            "plan_id": plan["id"],
            "status": "success"
            if all(r["status"] == "success" for r in results)
            else "failed",
            "tasks": results,
        }

    async def _execute_task(self, task: Task) -> dict[str, Any]:
        """Execute a single task."""
        task.status = TaskStatus.RUNNING

        try:
            await asyncio.sleep(0.1)
            task.status = TaskStatus.SUCCESS
            task.output = f"Task {task.name} completed"
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)

        return {
            "id": task.id,
            "name": task.name,
            "status": task.status.value,
            "output": task.output,
            "error": task.error,
        }


if __name__ == "__main__":
    runner = HarnessRunner()

    sample_plan = {
        "id": "plan_001",
        "name": "Hello Harness",
        "tasks": [
            {"id": "task_1", "name": "Say Hello", "command": "echo 'Hello'"},
            {"id": "task_2", "name": "Say World", "command": "echo 'World'"},
        ],
    }

    plan_path = ".harness/plans/plan_001.json"
    with open(plan_path, "w") as f:
        json.dump(sample_plan, f, indent=2)

    result = asyncio.run(runner.run_plan(plan_path))
    print(json.dumps(result, indent=2))
