"""Tests for the minemize function."""

import pytest

from minemizer import config, minemize


@pytest.fixture(autouse=True)
def reset_config():
    """Reset global config before each test."""
    original = (config.delimiter, config.use_spaces, config.sparsity_threshold, config.sparse_indicator)
    yield
    config.delimiter, config.use_spaces, config.sparsity_threshold, config.sparse_indicator = original


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
    assert result == "name; address{ city}\nAlice;{ Boston}\nBob;{ NYC}"


def test_minemize_list_of_primitives():
    """Test list of primitive values."""
    data = [
        {"name": "Alice", "tags": ["python", "rust"]},
        {"name": "Bob", "tags": ["go", "java"]},
    ]
    result = minemize(data)
    assert result == "name; tags[]\nAlice;[ python; rust]\nBob;[ go; java]"


def test_minemize_list_of_dicts():
    """Test list of dicts serialization."""
    data = [
        {"name": "Alice", "orders": [{"id": 1}, {"id": 2}]},
        {"name": "Bob", "orders": [{"id": 3}]},
    ]
    result = minemize(data)
    assert result == "name; orders[{ id}]\nAlice;[{ 1};{ 2}]\nBob;[{ 3}]"


def test_minemize_sparse_keys():
    """Test handling of sparse keys (not present in all items)."""
    data = [
        {"name": "Alice"},
        {"name": "Bob"},
        {"name": "Charlie", "city": "NYC"},
    ]
    result = minemize(data)
    assert result == "name\nAlice\nBob\nCharlie; city: NYC"


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
    config.sparsity_threshold = 0.6  # b appears in 1/3 = 33%, below threshold
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


# Preset tests


def test_preset_markdown():
    """Test markdown preset produces proper table."""
    from minemizer import presets

    data = [{"a": 1, "b": 2}]
    result = minemize(data, preset=presets.markdown)

    assert result.startswith("|")
    assert "---" in result
    assert result.count("\n") == 2  # header, separator, data row


def test_preset_csv():
    """Test CSV preset produces comma-separated output."""
    from minemizer import presets

    data = [{"a": 1, "b": 2}]
    result = minemize(data, preset=presets.csv)

    assert "," in result
    assert ";" not in result
    assert " " not in result


def test_preset_with_override():
    """Test that preset options can be overridden."""
    from minemizer import presets

    data = [{"a": 1, "b": 2}]
    # Use markdown preset but override delimiter
    result = minemize(data, preset=presets.markdown, delimiter=":")

    assert ":" in result
    assert "|" not in result.split("\n")[0].strip("|")  # delimiter changed


def test_preset_llm_alias():
    """Test that presets.llm is an alias for presets.default."""
    from minemizer import presets

    assert presets.llm is presets.default

    data = [{"a": 1, "b": 2}]
    assert minemize(data, preset=presets.llm) == minemize(data, preset=presets.default)


# =============================================================================
# Category A Tests: Sparse Formatting Bugs
# =============================================================================


def test_sparse_field_with_nested_dict():
    """Bug A1: Sparse field at row level with nested dict should not produce Python repr."""
    data = [
        {"name": "a", "extra": {"nested": {"deep": "value"}}},
        {"name": "b"},
        {"name": "c"},  # extra only in 1/3 = 0.33 < 0.5 threshold
    ]
    result = minemize(data)

    # Should NOT contain Python repr
    assert "{'deep': 'value'}" not in result
    # Should contain properly formatted nested structure
    assert "deep:" in result or "deep;" in result


def test_sparse_pairs_in_header_dict():
    """Bug A2: Sparse key-value pairs within a header dict should not produce Python repr."""
    data = [
        {"schema": {"type": "obj", "extra": {"x": 1}}},
        {"schema": {"type": "str"}},
        {"schema": {"type": "arr"}},  # extra only in 1/3
    ]
    result = minemize(data)

    # Should NOT contain Python repr
    assert "{'x': 1}" not in result
    # Should contain properly formatted nested structure
    assert "x:" in result or "x;" in result


def test_deeply_nested_sparse():
    """Bug A1+A2: Deeply nested sparse structure should not produce Python repr."""
    data = [
        {"a": {"b": {"c": {"d": {"e": "deep"}}}}},
        {"a": {"b": {}}},
        {"a": {"b": {}}},  # c only in 1/3
    ]
    result = minemize(data)

    # Should NOT contain Python repr
    assert "{'d':" not in result
    assert "{'e':" not in result


# =============================================================================
# Category B Tests: Type Detection Bugs
# =============================================================================


def test_mixed_dict_primitive_same_key():
    """Bug B1: One primitive should not break all dicts for same key."""
    data = [
        {"field": {"nested": "value"}},
        {"field": "just_string"},
    ]
    result = minemize(data)

    # Should NOT contain Python repr for the dict
    assert "{'nested': 'value'}" not in result
    # Dict should be properly formatted (key in header, value in data)
    # Header will have: field{ nested}
    # Data will have: { value}
    assert "nested" in result  # Key appears in header
    assert "value" in result  # Value appears in data row
    # String should still be there
    assert "just_string" in result


def test_mixed_list_content():
    """Bug B2: List with mixed dict/primitive content should not produce Python repr."""
    data = [
        {"items": [{"a": 1}, {"b": 2}]},
        {"items": ["str1", "str2"]},
    ]
    result = minemize(data)

    # Should NOT contain Python repr for dicts
    assert "{'a': 1}" not in result
    assert "{'b': 2}" not in result


def test_nested_lists():
    """Bug B3: List of lists should not produce Python repr."""
    data = [
        {"matrix": [[1, 2], [3, 4]]},
        {"matrix": [[5, 6], [7, 8]]},
    ]
    result = minemize(data)

    # Should NOT contain Python repr for inner lists
    assert "[1, 2]" not in result
    assert "[3, 4]" not in result


def test_dict_vs_list_type_mismatch():
    """Bug B4: Same key as dict in one row, list in another should not produce Python repr."""
    data = [
        {"field": {"a": 1}},
        {"field": [{"b": 2}]},
    ]
    result = minemize(data)

    # Should NOT contain Python repr
    assert "{'a': 1}" not in result
    assert "[{'b': 2}]" not in result


def test_none_in_list_items():
    """Bug B5: None inside list should not break dict detection."""
    data = [
        {"items": [None, {"a": 1}]},
        {"items": [{"b": 2}]},
    ]
    result = minemize(data)

    # Should NOT contain Python repr for dicts
    assert "{'a': 1}" not in result
    assert "{'b': 2}" not in result


def test_list_of_list_of_dicts():
    """Bug B6: Nested list containing dicts should not produce Python repr."""
    data = [
        {"matrix": [[{"cell": 1}], [{"cell": 2}]]},
        {"matrix": [[{"cell": 3}], [{"cell": 4}]]},
    ]
    result = minemize(data)

    # Should NOT contain Python repr
    assert "[{'cell': 1}]" not in result
    assert "{'cell':" not in result


# =============================================================================
# Regression Tests: Ensure existing behavior is preserved
# =============================================================================


def test_regression_uniform_dicts():
    """Ensure uniform dict data still works optimally."""
    data = [
        {"name": "Alice", "info": {"age": 30, "city": "Boston"}},
        {"name": "Bob", "info": {"age": 25, "city": "NYC"}},
    ]
    result = minemize(data)

    # Should have schema in header
    assert "info{ age; city}" in result or "info{ city; age}" in result
    # Should NOT have keys repeated in data rows
    lines = result.split("\n")
    assert "age:" not in lines[1]  # Data row should not have "age:" key
    assert "city:" not in lines[1]


def test_regression_uniform_list_of_dicts():
    """Ensure uniform list of dicts data still works optimally."""
    data = [
        {"orders": [{"id": 1, "qty": 2}, {"id": 3, "qty": 4}]},
        {"orders": [{"id": 5, "qty": 6}]},
    ]
    result = minemize(data)

    # Should have schema in header
    assert "orders[{ id; qty}]" in result or "orders[{ qty; id}]" in result


def test_regression_empty_structures():
    """Ensure empty dicts and lists still work."""
    data = [
        {"empty_dict": {}, "empty_list": []},
        {"empty_dict": {"a": 1}, "empty_list": [1, 2]},
    ]
    result = minemize(data)

    # Should handle empty structures gracefully
    assert "{}" in result
    assert "[]" in result


# =============================================================================
# Cleanup Optimization Tests
# =============================================================================


def test_cleanup_kv_before_dict():
    """Ensure ': {' is optimized to ':{'."""
    data = [
        {"name": "a", "extra": {"nested": {"deep": "value"}}},
        {"name": "b"},
        {"name": "c"},  # Makes 'extra' sparse
    ]
    result = minemize(data)

    # Should NOT have ": {" pattern (space before opener)
    assert ": {" not in result
    # Should have ":{" pattern
    assert ":{" in result


def test_cleanup_kv_before_list():
    """Ensure ': [' is optimized to ':[' in nested sparse structures."""
    data = [
        {"a": {"b": {"items": [1, 2, 3]}}},
        {"a": {"b": {}}},
        {"a": {"b": {}}},  # Makes 'items' sparse within 'b'
    ]
    result = minemize(data)

    # Should NOT have ": [" pattern (space before opener)
    assert ": [" not in result
    # Should have ":[" pattern for nested sparse list
    assert ":[" in result


def test_cleanup_nested_sparse_structures():
    """Ensure nested sparse structures have optimized formatting."""
    data = [
        {"a": {"b": {"c": {"d": "value"}}}},
        {"a": {"b": {}}},
        {"a": {"b": {}}},  # Makes 'c' sparse within 'b'
    ]
    result = minemize(data)

    # Should NOT have any ": {" patterns
    assert ": {" not in result
    # Nested sparse dicts should use ":{" pattern
    assert ":{" in result
