# minemizer
Minimize your data to decrease LLM token usage

See some pretty comparisons at [benchmarks](https://ashirviskas.github.io/)

PRs are very welcome!

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

### Some explanation of defaults
- **Delimiter**: `;` - Chosen mostly arbitrarily as it is not used too often in text data, but is used often enough to be recognized as a separator by LLMs.
- **Use spaces**: `True` - Renders strings as `{  somevalue; othervalue}` instead of `{somevalue;othervalue}` for better tokenization efficiency. It does introduce more tokens on average (~3-5% in my testing), but more the tokens more often preserve whole words. Example `{Hana;pyramid}` will tokenize to `{|H|ana|;p|yramid}` (5 tokens and words are split), while `{ Hana; pyramid}` tokenizes to `{| Hana|;| pyramid|}` (still 5 tokens, but the words are preserved). This will not matter much for bigger LLMs, but for smaller models it can make a difference. If you use a model that is 100B+ parameters, you can probably set this to `False` and save some tokens. Real benchmarks are more than welcome.
- **Sparsity threshold**: `0.5` - If some value appears in less than 50% of records, 

## Presets

I added some presets just for fun if you want your data to look more like something else that might help your LLM understand it better. It does not guarantee the format will be compliant and **will likely not load with old school non-LLM parsers**.

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

## Benchmarks

<!-- BENCHMARK_START -->
_Last updated: 2025-12-01_

### Token efficiency (normalized, JSON pretty = 1.0x)

| Format | flat | nested | lists | sparse | coingecko | complex | avg |
|---|---|---|---|---|---|---|---|
| JSON (pretty) | 1.0x | 1.0x | 1.0x | 1.0x | 1.0x | 1.0x | 1.0x |
| JSON (min) | 2.1x | 2.2x | 2.5x | 2.2x | 1.8x | 2.3x | 2.2x |
| CSV | 3.6x | ✗ | ✗ | ✗ | 2.7x | ✗ | 3.1x\*\* |
| TSV | 3.6x | ✗ | ✗ | ✗ | 2.7x | ✗ | 3.2x\*\* |
| YAML | 1.8x | 1.8x | 1.8x | 1.8x | 1.7x | 1.7x | 1.8x |
| TOON | 3.2x | 1.6x | 1.9x | 1.6x | 2.6x | 1.6x | 2.1x |
| TSON | 3.6x | 3.5x | **3.8x** | 2.1x | 2.8x | 2.7x | 3.1x |
| minemizer | **4.1x** | **3.6x** | 3.6x | **3.3x** | **2.8x** | **3.1x** | **3.4x** |
| minemizer (compact) | 3.8x | 3.5x | 3.6x | 3.2x | 2.8x | 3.0x | 3.3x |

_Higher is better. ✗ = format cannot represent this data type. \*\* = average from partial data._

See [token visualization](benchmarks/results/benchmark_tokens.html) for detailed tokenization comparison across different tokenizers (gpt2, llama, qwen2.5, phi4).
<!-- BENCHMARK_END -->

## Installation





## Future work

- Deal with auto formatting numbers (floats, i.e. do python `{number:.5g} maybe as optional.), dates (ISO8601 FTW, llms do like it very much) etc.
- Create presets for different LLM tokenizers/models to maximize token efficiency (less tokens) and/or performance (better benchmarks)
- Support for type hints to optimize formatting (e.g., dates, numbers).
- Per field configuration (custom date format, number precision, unix to datetime etc.)