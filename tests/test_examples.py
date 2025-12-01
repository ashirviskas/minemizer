"""Tests for generated examples."""

import json
from pathlib import Path

import pytest

from minemizer import minemize

EXAMPLES_DIR = Path(__file__).parent.parent / "examples"


def get_example_dirs() -> list[Path]:
    """Get all example directories."""
    if not EXAMPLES_DIR.exists():
        return []
    return [d for d in EXAMPLES_DIR.iterdir() if d.is_dir()]


@pytest.mark.parametrize("example_dir", get_example_dirs(), ids=lambda d: d.name)
def test_example_json_exists(example_dir: Path):
    """Test that each example has a JSON file."""
    json_file = example_dir / f"{example_dir.name}.json"
    assert json_file.exists(), f"Missing {json_file}"


@pytest.mark.parametrize("example_dir", get_example_dirs(), ids=lambda d: d.name)
def test_example_minemized_exists(example_dir: Path):
    """Test that each example has a minemized markdown file."""
    md_file = example_dir / f"{example_dir.name}_minemized.md"
    assert md_file.exists(), f"Missing {md_file}"


@pytest.mark.parametrize("example_dir", get_example_dirs(), ids=lambda d: d.name)
def test_example_json_valid(example_dir: Path):
    """Test that each example's JSON is valid."""
    json_file = example_dir / f"{example_dir.name}.json"
    data = json.loads(json_file.read_text())
    assert isinstance(data, list), "JSON should be a list"
    assert all(isinstance(item, dict) for item in data), "All items should be dicts"


def test_csv_style_output():
    """Test CSV-style output with comma delimiter."""
    from minemizer import presets

    data = [
        {"product": "Widget", "price": 9.99, "qty": 100},
        {"product": "Gadget", "price": 19.99, "qty": 50},
    ]
    result = minemize(data, preset=presets.csv)
    lines = result.split("\n")

    # Should look like CSV
    assert "," in lines[0]
    assert ";" not in lines[0]
    assert " " not in lines[0]  # no spaces


def test_markdown_table_output():
    """Test markdown table output with pipe delimiter."""
    from minemizer import presets

    data = [
        {"name": "Alice", "role": "Engineer"},
        {"name": "Bob", "role": "Designer"},
    ]
    result = minemize(data, preset=presets.markdown)
    lines = result.split("\n")

    # Should have pipes on both ends (proper markdown table)
    assert lines[0].startswith("|")
    assert lines[0].endswith("|")

    # Should have separator row
    assert "---" in lines[1]

    # All rows should be wrapped
    for line in lines:
        assert line.startswith("|") and line.endswith("|")


def test_nested_preserves_structure():
    """Test that nested data preserves structure indicators."""
    data = [
        {"name": "Alice", "meta": {"a": 1}},
        {"name": "Bob", "meta": {"a": 2}},
    ]
    result = minemize(data)

    # Should have nested dict indicator in header
    assert "meta{" in result or "meta {" in result


def test_uniform_no_sparse_indicators():
    """Test that uniform data has no sparse indicators."""
    data = [
        {"a": 1, "b": 2},
        {"a": 3, "b": 4},
    ]
    result = minemize(data)

    # No sparse indicator in header
    assert "..." not in result.split("\n")[0]


def test_non_uniform_has_sparse_fields():
    """Test that non-uniform data handles sparse fields."""
    data = [
        {"name": "Alice"},
        {"name": "Bob"},
        {"name": "Charlie", "extra": "value"},
    ]
    result = minemize(data, sparsity_threshold=0.5)

    # "extra" should be sparse (in row, not header)
    header = result.split("\n")[0]
    assert "extra" not in header
    assert "extra: value" in result
