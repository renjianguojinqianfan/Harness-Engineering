"""Core logic for harness-init."""

import subprocess
from pathlib import Path


def _get_templates_dir() -> Path:
    """返回模板资源目录。"""
    return Path(__file__).parent / "templates"


def _ensure_dir(path: Path) -> None:
    """确保目录存在。"""
    path.mkdir(parents=True, exist_ok=True)


def _render_template(template_path: Path, output_path: Path, project_name: str) -> None:
    """渲染模板文件到目标路径。"""
    content = template_path.read_text(encoding="utf-8")
    content = content.replace("{project_name}", project_name)
    output_path.write_text(content, encoding="utf-8")


def _create_directories(project_path: Path) -> None:
    """创建项目标准目录结构。"""
    dirs = [
        ".agent/plans",
        "specs",
        "src",
        "tests",
    ]
    for d in dirs:
        _ensure_dir(project_path / d)


def _copy_templates(project_path: Path, project_name: str) -> None:
    """复制模板文件到项目目录。"""
    templates_dir = _get_templates_dir()
    files = {
        "AGENTS.md": "AGENTS.md",
        "Makefile": "Makefile",
        ".gitignore": ".gitignore",
        "opencode.yaml": "opencode.yaml",
    }
    for src_name, dst_name in files.items():
        src = templates_dir / src_name
        dst = project_path / dst_name
        if src.exists():
            _render_template(src, dst, project_name)


def _init_git(project_path: Path) -> None:
    """初始化 Git 仓库并创建初始提交。"""
    subprocess.run(
        ["git", "init"],
        cwd=project_path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "add", "."],
        cwd=project_path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        cwd=project_path,
        check=True,
        capture_output=True,
    )


def init_project(project_path: str) -> None:
    """初始化新项目。

    Args:
        project_path: 项目目标路径。
    """
    path = Path(project_path)
    project_name = path.name
    _create_directories(path)
    _copy_templates(path, project_name)
    _init_git(path)
