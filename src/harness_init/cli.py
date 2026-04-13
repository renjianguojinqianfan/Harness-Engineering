"""CLI entry for harness-init."""

import typer

from harness_init.core import init_project


def main(project_name: str) -> None:
    """初始化一个新的 Harness Engineering 项目。

    Args:
        project_name: 项目名称或目标路径。
    """
    init_project(project_name)


def cli() -> None:
    """CLI entry point."""
    typer.run(main)


if __name__ == "__main__":
    cli()
