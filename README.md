# minemizer
Minimize your stuff

## Using minemizer

The default output is optimized for LLM token efficiency:

```python
from minemizer import minemize

data = [
    {"name": "Alice", "role": "Engineer", "team": "Backend"},
    {"name": "Bob", "role": "Designer", "team": "Frontend"},
    {"name": "Charlie", "role": "Manager", "team": "Product"},
]
print(minemize(data))
```
```
name; role; team
Alice; Engineer; Backend
Bob; Designer; Frontend
Charlie; Manager; Product
```

### Nested data

```python
data = [
    {"id": 1, "name": "Alice", "address": {"street": "123 Main St", "city": "Boston"}},
    {"id": 2, "name": "Bob", "address": {"street": "456 Oak Ave", "city": "NYC"}},
]
print(minemize(data))
```
```
id; name; address{ street; city}
1; Alice; { 123 Main St; Boston}
2; Bob; { 456 Oak Ave; NYC}
```

## Presets

Use built-in presets for common formats:

```python
from minemizer import minemize, presets
```

### CSV

```python
print(minemize(data, preset=presets.csv))
```
```
name,role,team
Alice,Engineer,Backend
Bob,Designer,Frontend
Charlie,Manager,Product
```

### Markdown table

```python
print(minemize(data, preset=presets.markdown))
```
```
|name| role| team|
|---| ---| ---|
|Alice| Engineer| Backend|
|Bob| Designer| Frontend|
|Charlie| Manager| Product|
```

Rendered:

|name| role| team|
|---| ---| ---|
|Alice| Engineer| Backend|
|Bob| Designer| Frontend|
|Charlie| Manager| Product|

### Available presets

| Preset | Description |
|--------|-------------|
| `presets.default` / `presets.llm` | Optimized for LLM token efficiency (semicolon, spaces) |
| `presets.markdown` | Proper markdown table with header separator |
| `presets.csv` | Comma-separated values |
| `presets.tsv` | Tab-separated values |
| `presets.compact` | Minimal tokens (semicolon, no spaces) |

See [examples/](examples/) for more detailed examples.

## Configuration

Set global defaults or use per-call overrides:

```python
from minemizer import config, minemize

# Configure globally
config.delimiter = "|"
config.use_spaces = False

data = [{"a": 1, "b": 2}]
print(minemize(data))  # a|b \n 1|2

# Override per-call
print(minemize(data, delimiter=","))  # a,b \n 1,2
```

### Config options

| Option | Default | Description |
|--------|---------|-------------|
| `delimiter` | `";"` | Field separator |
| `use_spaces` | `True` | Add space after delimiter |
| `threshold` | `0.5` | Key frequency threshold for header (0.0-1.0) |
| `sparse_indicator` | `"..."` | Indicator for sparse fields in schema |
| `header_separator` | `None` | Separator row after header (e.g., `"---"`) |
| `wrap_lines` | `None` | Wrap each line with this string (e.g., `"\|"`) |

## Installation