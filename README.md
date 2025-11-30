# minemizer
Minimize your stuff

## Using minemizer

The default output is optimized for LLM token efficiency:

```python
from minemizer import minemize

data = [
    {"name": "Marta", "role": "Engineer", "team": "Backend"},
    {"name": "James", "role": "Designer", "team": "Frontend"},
    {"name": "Sophie", "role": "Manager", "team": "Product"},
]
print(minemize(data))
```
```
name; role; team
Marta; Engineer; Backend
James; Designer; Frontend
Sophie; Manager; Product
```

### Nested data

```python
data = [
    {"id": 1, "name": "Yuki", "address": {"street": "12 Sakura Lane", "city": "Kyoto"}},
    {"id": 2, "name": "Lin", "address": {"street": "88 Garden Road", "city": "Taipei"}},
]
print(minemize(data))
```
```
id; name; address{ street; city}
1; Yuki; { 12 Sakura Lane; Kyoto}
2; Lin; { 88 Garden Road; Taipei}
```

### Nested non-uniform data with sparsity_threshold

Control how sparse fields are handled using `sparsity_threshold`. Fields appearing in fewer records than the threshold are shown inline in rows rather than in the header:

```python
data = [
    {"id": 1, "name": "Lukas", "location": {"city": "Vilnius", "floor": 3}},
    {"id": 2, "name": "Emma", "location": {"city": "Boston", "floor": 7, "desk": "A12"}},
    {"id": 3, "name": "Yuki", "location": {"city": "Tokyo", "floor": 5}},
    {"id": 4, "name": "Oliver", "location": {"city": "London", "floor": 2, "desk": "B04"}},
]

# Default (0.5): desk appears in 50% of records, included in schema
print(minemize(data))
```
```
id; name; location{ city; floor; desk}
1; Lukas; { Vilnius; 3; }
2; Emma; { Boston; 7; A12}
3; Yuki; { Tokyo; 5; }
4; Oliver; { London; 2; B04}
```

```python
# Strict (1.0): only fields in ALL records go in schema, desk becomes sparse
print(minemize(data, sparsity_threshold=1.0))
```
```
id; name; location{ city; floor; ...}
1; Lukas; { Vilnius; 3}
2; Emma; { Boston; 7; desk:A12}
3; Yuki; { Tokyo; 5}
4; Oliver; { London; 2; desk:B04}
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
Marta,Engineer,Backend
James,Designer,Frontend
Sophie,Manager,Product
```

### Markdown table

```python
print(minemize(data, preset=presets.markdown))
```
```
|name| role| team|
|---| ---| ---|
|Marta| Engineer| Backend|
|James| Designer| Frontend|
|Sophie| Manager| Product|
```

Rendered:

|name| role| team|
|---| ---| ---|
|Marta| Engineer| Backend|
|James| Designer| Frontend|
|Sophie| Manager| Product|

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
| `sparsity_threshold` | `0.5` | Key frequency threshold for header (0.0-1.0) |
| `sparse_indicator` | `"..."` | Indicator for sparse fields in schema |
| `header_separator` | `None` | Separator row after header (e.g., `"---"`) |
| `wrap_lines` | `None` | Wrap each line with this string (e.g., `"\|"`) |

## Installation