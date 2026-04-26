"""Tests for _templates.py."""

from pathlib import Path

from harness_init._templates import (
    _gather_quick_bases,
    _resolve_quick_variant,
    _should_skip,
    copy_templates,
)


class TestShouldSkip:
    """Tests for _should_skip."""

    def test_skips_directories(self, tmp_path: Path) -> None:
        """应跳过目录。"""
        assert _should_skip(tmp_path / "dir") is True

    def test_skips_pyc_files(self, tmp_path: Path) -> None:
        """应跳过 .pyc 文件。"""
        pyc = tmp_path / "foo.pyc"
        pyc.write_text("x")
        assert _should_skip(pyc) is True

    def test_skips_cache_dirs(self, tmp_path: Path) -> None:
        """应跳过缓存目录中的文件。"""
        cache_dir = tmp_path / "__pycache__"
        cache_dir.mkdir()
        f = cache_dir / "foo.cpython-311.pyc"
        f.write_text("x")
        assert _should_skip(f) is True

    def test_keeps_normal_files(self, tmp_path: Path) -> None:
        """应保留普通文件。"""
        f = tmp_path / "cli.py"
        f.write_text("x")
        assert _should_skip(f) is False


class TestGatherQuickBases:
    """Tests for _gather_quick_bases."""

    def test_finds_quick_variants(self, tmp_path: Path) -> None:
        """应识别 .quick. 变体及其对应的基础文件。"""
        (tmp_path / "AGENTS.quick.md").write_text("quick")
        (tmp_path / "AGENTS.md").write_text("base")
        bases = _gather_quick_bases(tmp_path)
        assert "AGENTS.md" in bases

    def test_ignores_non_quick_files(self, tmp_path: Path) -> None:
        """应忽略非 .quick. 文件。"""
        (tmp_path / "README.md").write_text("readme")
        bases = _gather_quick_bases(tmp_path)
        assert "README.md" not in bases

    def test_handles_nested_paths(self, tmp_path: Path) -> None:
        """应处理嵌套路径中的 .quick. 变体。"""
        pkg_dir = tmp_path / "src" / "{package_name}"
        pkg_dir.mkdir(parents=True)
        (pkg_dir / "cli.quick.py").write_text("quick")
        (pkg_dir / "cli.py").write_text("base")
        bases = _gather_quick_bases(tmp_path)
        assert "src/{package_name}/cli.py" in bases


class TestResolveQuickVariant:
    """Tests for _resolve_quick_variant."""

    def test_quick_mode_replaces_quick_suffix(self, tmp_path: Path) -> None:
        """quick=True 时应将 .quick. 替换为 . 。"""
        src = tmp_path / "AGENTS.quick.md"
        rel = Path("AGENTS.quick.md")
        result = _resolve_quick_variant(src, rel, quick=True, quick_bases=set())
        assert result == Path("AGENTS.md")

    def test_quick_mode_skips_base_when_quick_exists(self) -> None:
        """quick=True 且存在 .quick. 变体时，应跳过基础文件。"""
        src = Path("AGENTS.md")
        rel = Path("AGENTS.md")
        result = _resolve_quick_variant(src, rel, quick=True, quick_bases={"AGENTS.md"})
        assert result is None

    def test_normal_mode_ignores_quick_variants(self) -> None:
        """quick=False 时应忽略 .quick. 变体。"""
        src = Path("AGENTS.quick.md")
        rel = Path("AGENTS.quick.md")
        result = _resolve_quick_variant(src, rel, quick=False, quick_bases=set())
        assert result is None

    def test_normal_mode_keeps_base_files(self) -> None:
        """quick=False 时应保留基础文件。"""
        src = Path("AGENTS.md")
        rel = Path("AGENTS.md")
        result = _resolve_quick_variant(src, rel, quick=False, quick_bases={"AGENTS.md"})
        assert result == Path("AGENTS.md")


class TestCopyTemplates:
    """Tests for copy_templates."""

    def test_copies_simple_template(self, tmp_path: Path) -> None:
        """应复制简单模板文件。"""
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        (templates_dir / "README.md").write_text("# {project_name}")

        project_path = tmp_path / "project"
        project_path.mkdir()

        copy_templates(
            templates_dir,
            project_path,
            "my-project",
            "my_project",
        )

        readme = project_path / "README.md"
        assert readme.exists()
        assert "my-project" in readme.read_text(encoding="utf-8")

    def test_replaces_package_name_in_paths(self, tmp_path: Path) -> None:
        """应在路径中替换 {package_name}。"""
        templates_dir = tmp_path / "templates"
        pkg_dir = templates_dir / "src" / "{package_name}"
        pkg_dir.mkdir(parents=True)
        (pkg_dir / "cli.py").write_text("# cli")

        project_path = tmp_path / "project"
        project_path.mkdir()

        copy_templates(
            templates_dir,
            project_path,
            "my-project",
            "my_project",
        )

        assert (project_path / "src" / "my_project" / "cli.py").exists()

    def test_quick_mode_excludes_files(self, tmp_path: Path) -> None:
        """quick=True 时应根据 is_excluded 回调排除文件。"""
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        (templates_dir / "AGENTS.md").write_text("agents")
        (templates_dir / "CLAUDE.md").write_text("claude")

        project_path = tmp_path / "project"
        project_path.mkdir()

        copy_templates(
            templates_dir,
            project_path,
            "my-project",
            "my_project",
            quick=True,
            is_excluded=lambda rel: rel == "CLAUDE.md",
        )

        assert (project_path / "AGENTS.md").exists()
        assert not (project_path / "CLAUDE.md").exists()

    def test_skips_ignored_files(self, tmp_path: Path) -> None:
        """应自动跳过缓存文件等被忽略的文件。"""
        templates_dir = tmp_path / "templates"
        cache_dir = templates_dir / "__pycache__"
        cache_dir.mkdir(parents=True)
        (cache_dir / "foo.cpython-311.pyc").write_text("x")

        project_path = tmp_path / "project"
        project_path.mkdir()

        copy_templates(
            templates_dir,
            project_path,
            "my-project",
            "my_project",
        )

        assert not any(project_path.rglob("*.pyc"))

    def test_quick_variant_replaces_base(self, tmp_path: Path) -> None:
        """quick=True 时应使用 .quick. 变体替换基础文件。"""
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        (templates_dir / "AGENTS.md").write_text("full")
        (templates_dir / "AGENTS.quick.md").write_text("quick")

        project_path = tmp_path / "project"
        project_path.mkdir()

        copy_templates(
            templates_dir,
            project_path,
            "my-project",
            "my_project",
            quick=True,
        )

        content = (project_path / "AGENTS.md").read_text(encoding="utf-8")
        assert content == "quick"
