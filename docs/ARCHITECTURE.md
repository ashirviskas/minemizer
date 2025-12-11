# Minemizer Architecture

This document describes the internal architecture of minemizer, a library for compacting JSON data into a token-efficient string format.

## Module Overview

```mermaid
graph TB
    subgraph Public API
        minemize["minemize()"]
    end

    subgraph Configuration
        Config["Config (dataclass)"]
        presets["presets (namespace)"]
        global_config["config (singleton)"]
    end

    subgraph Core Processing
        serialize["_serialize()"]
        build_header["_build_header()"]
        format_row["_format_row()"]
    end

    subgraph Schema Analysis
        analyze_keys["_analyze_keys()"]
        create_header["_create_header_element()"]
        KeyAnalysis["KeyAnalysis"]
        HeaderElement["HeaderElement"]
    end

    subgraph Value Formatting
        format_value["_format_value()"]
        format_dict["_format_dict()"]
        format_list["_format_list()"]
        format_sparse["_format_sparse_field()"]
        format_pairs["_format_dict_pairs()"]
    end

    minemize --> Config
    minemize --> serialize
    serialize --> build_header
    serialize --> format_row
    build_header --> create_header
    create_header --> analyze_keys
    analyze_keys --> KeyAnalysis
    create_header --> HeaderElement
    format_row --> format_value
    format_row --> format_sparse
    format_value --> format_dict
    format_value --> format_list
    format_sparse --> format_pairs
    format_dict --> format_value
```

## Data Flow

```mermaid
flowchart LR
    A[JSON Input] --> B[minemize]
    B --> C{dict or list?}
    C -->|dict| D[Wrap in list]
    C -->|list| E[Continue]
    D --> E
    E --> F[_serialize]
    F --> G[_build_header]
    F --> H[_format_row per item]
    G --> I[Header String]
    H --> J[Row Strings]
    I --> K[Join Lines]
    J --> K
    K --> L[Output String]
```

## Core Data Structures

### Config (config.py:7-44)

Configuration dataclass controlling output formatting:

| Property | Default | Description |
|----------|---------|-------------|
| `delimiter` | `";"` | Field separator |
| `use_spaces` | `True` | Add spaces around delimiters |
| `sparsity_threshold` | `0.5` | Key frequency threshold for header |
| `sparse_indicator` | `"..."` | Marker for sparse fields in header |
| `header_separator` | `None` | Row separator (e.g., `"---"` for markdown) |
| `wrap_lines` | `None` | Line wrapper (e.g., `"\|"` for markdown) |

Computed properties:
- `spaced_delimiter` → `"; "` or `";"`
- `spaced_kv_separator` → `": "` or `":"`
- `dict_open` → `"{ "` or `"{"`
- `list_open` → `"[ "` or `"["`

### KeyAnalysis (core.py:12-20)

Result of analyzing key frequency across items:

```python
@dataclass
class KeyAnalysis:
    common: list[str]   # Keys appearing >= threshold
    sparse: list[str]   # Keys appearing < threshold
```

### HeaderElement (core.py:24-53)

Schema definition for a single field:

```python
@dataclass
class HeaderElement:
    name: str
    type: str = "value"          # "value", "dict", "list"
    schema: list[HeaderElement]  # Nested schema for dicts/lists
    has_sparse: bool = False     # Whether nested dict has sparse keys
    list_type: str | None        # "dict" or "simple" for lists
```

## Processing Pipeline

### 1. Schema Building

```mermaid
flowchart TD
    A[Input: list of dicts] --> B[_build_header]
    B --> C[Collect all keys]
    C --> D[Filter by sparsity_threshold]
    D --> E[For each common key]
    E --> F[_create_header_element]
    F --> G{Value type?}
    G -->|all dicts| H[Recursive: analyze nested keys]
    G -->|all lists| I{List contents?}
    G -->|mixed/simple| J[type='value']
    I -->|all dicts| K[Recursive: analyze list items]
    I -->|simple| L[type='list', list_type='simple']
    H --> M[type='dict' + nested schema]
    K --> N[type='list', list_type='dict' + schema]
```

### 2. Row Formatting

```mermaid
flowchart TD
    A[Input: single dict item] --> B[_format_row]
    B --> C[Split: header keys vs sparse keys]
    C --> D[Format header values]
    C --> E[Format sparse fields]
    D --> F[_format_value per element]
    E --> G[_format_sparse_field per key]
    F --> H{Element type?}
    H -->|value| I[str conversion]
    H -->|dict| J[_format_dict]
    H -->|list| K[_format_list]
    J --> L["{ key:val; key:val}"]
    K --> M["[ item; item]"]
    G --> N["key:value or key{ pairs}"]
    I --> O[Join with delimiter]
    L --> O
    M --> O
    N --> O
```

## Output Format Example

Given input:
```json
[
  {"id": 1, "name": "Alice", "contact": {"email": "a@co.com"}},
  {"id": 2, "name": "Bob", "contact": {"email": "b@co.com", "phone": "555"}}
]
```

Processing:
1. **Header analysis**: `id`, `name`, `contact` are common (100%)
2. **Nested analysis**: `contact.email` is common, `contact.phone` is sparse (50%)
3. **Header schema**: `id; name; contact{ email; ...}`
4. **Row 1**: `1; Alice; { a@co.com}`
5. **Row 2**: `2; Bob; { b@co.com; phone: 555}`

Output:
```
id; name; contact{ email; ...}
1; Alice; { a@co.com}
2; Bob; { b@co.com; phone: 555}
```

## Presets (config.py:47-87)

| Preset | delimiter | use_spaces | header_separator | wrap_lines |
|--------|-----------|------------|------------------|------------|
| `default`/`llm` | `;` | `True` | - | - |
| `markdown` | `\|` | `True` | `---` | `\|` |
| `csv` | `,` | `False` | - | - |
| `tsv` | `\t` | `False` | - | - |
| `compact` | `;` | `False` | - | - |

## Function Reference

| Function | Location | Purpose |
|----------|----------|---------|
| `minemize()` | core.py:217 | Public API entry point |
| `_serialize()` | core.py:195 | Orchestrates header + rows |
| `_build_header()` | core.py:118 | Creates header schema |
| `_create_header_element()` | core.py:77 | Recursive schema builder |
| `_analyze_keys()` | core.py:63 | Identifies common/sparse keys |
| `_format_row()` | core.py:188 | Formats single item |
| `_format_value()` | core.py:159 | Dispatches by type |
| `_format_dict()` | core.py:134 | Formats nested dicts |
| `_format_list()` | core.py:148 | Formats lists |
| `_format_sparse_field()` | core.py:169 | Formats non-header fields |
| `_format_dict_pairs()` | core.py:130 | Formats dict as key:value pairs |
| `_normalize()` | core.py:59 | Converts bools to lowercase |
