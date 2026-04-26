"""Tests for notebooks."""

import json
from pathlib import Path


def test_example_notebook_is_valid_json() -> None:
    """example.ipynb should be valid JSON."""
    notebook_path = Path("notebooks/example.ipynb")
    if not notebook_path.exists():
        notebook_path = Path(__file__).parent.parent / "notebooks" / "example.ipynb"
    content = notebook_path.read_text(encoding="utf-8")
    data = json.loads(content)
    assert "cells" in data
    assert len(data["cells"]) >= 1
