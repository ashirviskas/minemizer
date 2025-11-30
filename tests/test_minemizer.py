"""Tests for the minemize function."""

from minemizer import minemize


def test_minemize_basic():
    """Test basic minemize functionality."""
    data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
    result = minemize(data)
    assert result == "name; age\nAlice; 30\nBob; 25"


def test_minemize_single_dict():
    """Test that a single dict is handled (auto-wrapped in list)."""
    data = {"name": "Alice", "age": 30}
    result = minemize(data)
    assert result == "name; age\nAlice; 30"


def test_minemize_empty_list():
    """Test that empty list returns empty string."""
    assert minemize([]) == ""


def test_minemize_nested_dict():
    """Test nested dict serialization."""
    data = [
        {"name": "Alice", "address": {"city": "Boston"}},
        {"name": "Bob", "address": {"city": "NYC"}},
    ]
    result = minemize(data)
    assert result == "name; address{ city}\nAlice; { Boston}\nBob; { NYC}"


def test_minemize_list_of_primitives():
    """Test list of primitive values."""
    data = [
        {"name": "Alice", "tags": ["python", "rust"]},
        {"name": "Bob", "tags": ["go", "java"]},
    ]
    result = minemize(data)
    assert result == "name; tags[]\nAlice; [ python; rust]\nBob; [ go; java]"


def test_minemize_list_of_dicts():
    """Test list of dicts serialization."""
    data = [
        {"name": "Alice", "orders": [{"id": 1}, {"id": 2}]},
        {"name": "Bob", "orders": [{"id": 3}]},
    ]
    result = minemize(data)
    assert result == "name; orders[{ id}]\nAlice; [ { 1}; { 2}]\nBob; [ { 3}]"


def test_minemize_sparse_keys():
    """Test handling of sparse keys (not present in all items)."""
    data = [
        {"name": "Alice"},
        {"name": "Bob"},
        {"name": "Charlie", "city": "NYC"},
    ]
    result = minemize(data)
    assert result == "name\nAlice\nBob\nCharlie; city:NYC"


def test_minemize_no_spaces():
    """Test use_spaces=False option."""
    data = [{"name": "Alice", "age": 30}]
    result = minemize(data, use_spaces=False)
    assert result == "name;age\nAlice;30"
