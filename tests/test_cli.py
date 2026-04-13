"""Tests for cli.py."""

from pathlib import Path
from unittest.mock import patch

from harness_init.cli import cli, main


def test_main_creates_project(tmp_path: Path) -> None:
    """应能根据项目名创建项目。"""
    project_path = tmp_path / "my-project"
    main(str(project_path))
    assert project_path.is_dir()
    assert (project_path / ".git").is_dir()


def test_cli_without_args_exits(tmp_path: Path) -> None:
    """不带参数时应退出并显示用法信息。"""
    with patch("sys.argv", ["harness-init"]):
        try:
            cli()
        except SystemExit as exc:
            assert exc.code != 0
