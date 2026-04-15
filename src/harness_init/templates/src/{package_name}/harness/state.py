"""Simple JSON state manager."""

import json
from pathlib import Path
from typing import Any


class StateManager:
    """Manage JSON-based state persistence."""

    def __init__(self, state_path: str = ".harness/state/state.json") -> None:
        self.state_path = Path(state_path)
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self._data: dict[str, Any] = {}
        self.load()

    def load(self) -> dict[str, Any]:
        """Load state from disk."""
        if self.state_path.exists():
            with open(self.state_path, encoding="utf-8") as f:
                self._data = json.load(f)
        else:
            self._data = {}
        return self._data

    def save(self) -> None:
        """Save state to disk."""
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)

    def get(self, key: str, default: Any | None = None) -> Any:
        """Get a value by key."""
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a value by key and persist."""
        self._data[key] = value
        self.save()
