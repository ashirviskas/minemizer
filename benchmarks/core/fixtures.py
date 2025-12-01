"""Fixture loading utilities."""

from __future__ import annotations

import json
from pathlib import Path

from benchmarks import FIXTURES_DIR
from benchmarks.config import FIXTURE_ORDER


def load_fixtures(
    fixtures_dir: Path | None = None,
    subdirectory: str = "compression",
) -> dict[str, list[dict]]:
    """Load all fixture JSON and JSONL files.

    Args:
        fixtures_dir: Base fixtures directory. Defaults to FIXTURES_DIR.
        subdirectory: Subdirectory within fixtures_dir to load from.

    Returns:
        Dict mapping fixture names to their data.
    """
    fixtures_dir = (fixtures_dir or FIXTURES_DIR) / subdirectory
    fixtures: dict[str, list[dict]] = {}

    # Load JSON files
    for path in fixtures_dir.glob("*.json"):
        with path.open() as f:
            fixtures[path.stem] = json.load(f)

    # Load JSONL files
    for path in fixtures_dir.glob("*.jsonl"):
        with path.open() as f:
            fixtures[path.stem] = [json.loads(line) for line in f if line.strip()]

    # Reorder according to FIXTURE_ORDER
    return _reorder_fixtures(fixtures)


def _reorder_fixtures(fixtures: dict[str, list[dict]]) -> dict[str, list[dict]]:
    """Reorder fixtures according to FIXTURE_ORDER, then alphabetically."""
    ordered: dict[str, list[dict]] = {}

    for name in FIXTURE_ORDER:
        if name in fixtures:
            ordered[name] = fixtures.pop(name)

    for name in sorted(fixtures.keys()):
        ordered[name] = fixtures[name]

    return ordered
