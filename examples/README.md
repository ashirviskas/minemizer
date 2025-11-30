# Examples

This directory contains generated examples demonstrating different minemizer configurations.

## Structure

Each example has its own directory containing:
- `{name}.json` - Input data
- `{name}_minemized.md` - Output with options and rendered result

## Examples

| Example | Description | Preset |
|---------|-------------|--------|
| [uniform](uniform/) | All keys present in all items | `presets.default` |
| [non_uniform](non_uniform/) | Sparse keys (some fields missing) | custom threshold |
| [nested](nested/) | Nested dicts and lists | `presets.default` |
| [csv_style](csv_style/) | Comma-separated output | `presets.csv` |
| [markdown_table](markdown_table/) | Proper markdown table | `presets.markdown` |

## Regenerating Examples

Examples are generated using the script:

```bash
uv run python scripts/generate_examples.py
```

The script is located at [`scripts/generate_examples.py`](../scripts/generate_examples.py).

## Adding New Examples

Edit `scripts/generate_examples.py` and add a new `Example` to the `EXAMPLES` list:

```python
Example(
    name="my_example",
    description="Description of what this demonstrates",
    data=[...],  # Your test data
    preset=presets.csv,  # Optional: use a preset
    preset_name="presets.csv",  # For display in docs
    options={"threshold": 0.8},  # Optional: additional overrides
)
```

Then regenerate with the script above.
