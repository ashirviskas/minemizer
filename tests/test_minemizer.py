"""Tests for the minemize function."""

from minemizer import minemize


def test_minemize_basic():
    """Test basic minemize functionality."""
    data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
    result = minemize(data)
    assert isinstance(result, str)
    assert len(result) > 0
