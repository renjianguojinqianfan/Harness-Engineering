"""CLI entry point for the generated project."""

import asyncio
import importlib
import json
from pathlib import Path

import typer
from rich import print as rprint

runner_mod = importlib.import_module("{package_name}.harness.runner")
HarnessRunner = runner_mod.HarnessRunner

eval_mod = importlib.import_module("{package_name}.harness.evaluator")
HarnessEvaluator = eval_mod.HarnessEvaluator

state_mod = importlib.import_module("{package_name}.harness.state")
StateManager = state_mod.StateManager

workflow_mod = importlib.import_module("{package_name}.harness.workflow")
Stage = workflow_mod.Stage
get_next_stage = workflow_mod.get_next_stage

app = typer.Typer()


@app.command()
def run(plan: str) -> None:
    """Load a plan, execute it, and save the result."""
    runner = HarnessRunner()
    result = asyncio.run(runner.run_plan(plan))

    state = StateManager()
    state.set("last_plan", plan)
    state.set("stage", Stage.EXECUTE.value)

    result_path = Path(".harness/state/last_result.json")
    result_path.parent.mkdir(parents=True, exist_ok=True)
    with open(result_path, "w") as f:
        json.dump(result, f, indent=2)

    state.set("stage", get_next_stage(Stage.EXECUTE).value)

    rprint(f"[green]Plan executed:[/green] {result['plan_id']}")
    rprint(f"[blue]Status:[/blue] {result['status']}")
    rprint(f"[blue]Tasks:[/blue] {len(result['tasks'])}")


@app.command()
def evaluate(
    result_path: str = typer.Argument(".harness/state/last_result.json"),
) -> None:
    """Evaluate a result and save feedback."""
    with open(result_path) as f:
        result = json.load(f)

    evaluator = HarnessEvaluator()
    eval_result = evaluator.evaluate(result, {"min_score": 70})
    plan_id = result.get("plan_id", "unknown")
    feedback_path = evaluator.save_feedback(plan_id, eval_result)

    state = StateManager()
    state.set("stage", Stage.EVALUATE.value)

    rprint(f"[green]Score:[/green] {eval_result.score}")
    rprint(f"[blue]Passed:[/blue] {eval_result.passed}")
    rprint(f"[blue]Feedback saved to:[/blue] {feedback_path}")


@app.command()
def status() -> None:
    """Print current workflow stage and active plan."""
    state = StateManager()
    stage = state.get("stage", Stage.FEEDBACK.value)
    plan = state.get("last_plan", None)

    rprint(f"[blue]Current stage:[/blue] {stage}")
    if plan:
        rprint(f"[blue]Active plan:[/blue] {plan}")
    else:
        rprint("[yellow]No active plan.[/yellow]")


if __name__ == "__main__":
    app()
