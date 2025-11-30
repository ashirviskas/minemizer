# minemizer
Minimize your stuff

## Using minemizer

```python
from minemizer import minemize

data = [
    {"id": 1, "name": "Alice", "age": 30},
    {"id": 2, "name": "Bob", "age": 25},
    {"id": 3, "name": "Charlie", "age": 35},
]
print(minemize(data))
# id; name; age
# 1; Alice; 30
# 2; Bob; 25
# 3; Charlie; 35
```

### Nested data

```python
data = [
    {"id": 1, "name": "Alice", "address": {"street": "123 Main St", "city": "Boston"}},
    {"id": 2, "name": "Bob", "address": {"street": "456 Oak Ave", "city": "NYC"}},
]
print(minemize(data))
# id; name; address{ street; city}
# 1; Alice; { 123 Main St; Boston}
# 2; Bob; { 456 Oak Ave; NYC}
```

## Configuration

Set global defaults once, apply everywhere:

```python
from minemizer import config, minemize

# Configure globally
config.delimiter = "|"
config.use_spaces = False
config.threshold = 0.9
config.sparse_indicator = "~"

data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
print(minemize(data))
# name|age
# Alice|30
# Bob|25
```

### Per-call overrides

```python
from minemizer import config, minemize

config.delimiter = "|"

data = [{"a": 1, "b": 2}]
print(minemize(data))              # a| b
                                   # 1| 2

print(minemize(data, delimiter=","))  # a, b   (override just this call)
                                      # 1, 2
```

### Config options

| Option | Default | Description |
|--------|---------|-------------|
| `delimiter` | `";"` | Field separator |
| `use_spaces` | `True` | Add space after delimiter |
| `threshold` | `0.5` | Key frequency threshold for header (0.0-1.0) |
| `sparse_indicator` | `"..."` | Indicator for sparse fields in schema |

## Installation