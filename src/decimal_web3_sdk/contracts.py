from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class AbiRegistry:
    def __init__(self, abi_dir: Path | None = None) -> None:
        self.abi_dir = abi_dir or Path(__file__).parent / "abi"
        self._cache: dict[str, list[dict[str, Any]]] = {}

    def load(self, name: str) -> list[dict[str, Any]]:
        key = name.lower()
        if key in self._cache:
            return self._cache[key]

        path = self.abi_dir / name
        if not path.suffix:
            path = path.with_suffix(".json")
        if not path.exists():
            raise FileNotFoundError(f"ABI file not found: {path}")

        data = json.loads(path.read_text(encoding="utf-8"))
        abi = data["abi"] if isinstance(data, dict) and "abi" in data else data
        if not isinstance(abi, list):
            raise ValueError(f"Invalid ABI format: {path}")
        self._cache[key] = abi
        return abi

