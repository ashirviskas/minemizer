"""Tests for the minemize function."""

import pytest

from minemizer import config, minemize


@pytest.fixture(autouse=True)
def reset_config():
    """Reset global config before each test."""
    original = (config.delimiter, config.use_spaces, config.threshold, config.sparse_indicator)
    yield
    config.delimiter, config.use_spaces, config.threshold, config.sparse_indicator = original


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


# Config tests


def test_global_config_delimiter():
    """Test that global config delimiter is used."""
    config.delimiter = "|"
    data = [{"name": "Alice", "age": 30}]
    result = minemize(data)
    assert result == "name| age\nAlice| 30"


def test_global_config_custom_delimiter_no_spaces():
    """Test custom delimiter without spaces."""
    config.delimiter = "|"
    config.use_spaces = False
    data = [{"name": "Alice", "age": 30}]
    result = minemize(data)
    assert result == "name|age\nAlice|30"


def test_override_global_config():
    """Test that function args override global config."""
    config.delimiter = "|"
    data = [{"name": "Alice", "age": 30}]
    result = minemize(data, delimiter=",")
    assert result == "name, age\nAlice, 30"


def test_global_config_sparse_indicator():
    """Test custom sparse indicator in header."""
    config.sparse_indicator = "*"
    config.threshold = 0.6  # b appears in 1/3 = 33%, below threshold
    data = [
        {"name": "Alice", "meta": {"a": 1}},
        {"name": "Bob", "meta": {"a": 2}},
        {"name": "Charlie", "meta": {"a": 3, "b": 4}},
    ]
    result = minemize(data)
    assert "meta{ a; *}" in result


def test_config_derive():
    """Test config.derive() creates independent copy."""
    derived = config.derive(delimiter="|")
    assert derived.delimiter == "|"
    assert config.delimiter == ";"  # Original unchanged
