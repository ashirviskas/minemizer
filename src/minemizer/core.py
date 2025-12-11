# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Core functionality for minemizer."""

from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from minemizer.config import _NOT_PROVIDED, Config
from minemizer.config import config as _global_config


@dataclass
class KeyAnalysis:
    """Results from analyzing which keys are common vs sparse."""

    common: list[str] = field(default_factory=list)
    sparse: list[str] = field(default_factory=list)

    @property
    def has_sparse(self) -> bool:
        return bool(self.sparse)


@dataclass
class HeaderElement:
    """Schema definition for a single field in the header."""

    name: str
    cfg: Config
    type: str = "value"  # "value", "dict", "list"
    schema: list["HeaderElement"] = field(default_factory=list)
    has_sparse: bool = False
    list_type: str | None = None

    @property
    def schema_keys(self) -> set[str]:
        """Get the set of key names in the schema."""
        return {el.name for el in self.schema}

    def to_string(self) -> str:
        if self.type == "value":
            return self.name

        c = self.cfg
        schema_str = c.spaced_delimiter.join(el.to_string() for el in self.schema)
        if self.has_sparse:
            schema_str = f"{schema_str}{c.spaced_delimiter}{c.sparse_indicator}" if schema_str else c.sparse_indicator

        if self.type == "dict":
            return f"{self.name}{c.dict_open}{schema_str}{c.dict_close}"
        elif self.type == "list" and self.list_type == "dict":
            return f"{self.name}{c.list_open}{c.dict_open}{schema_str}{c.dict_close}{c.list_close}"
        # Empty simple list
        return f"{self.name}{c.list_open.rstrip()}{c.list_close}"


# --- Pure functions ---


def _normalize(value: Any) -> str:
    return str(value).lower() if isinstance(value, bool) else str(value)


def _majority_type(values: list, threshold: float = 0.5) -> str | None:
    """Determine the majority type among values. Returns 'dict', 'list', or None."""
    if not values:
        return None

    dict_count = sum(1 for v in values if isinstance(v, dict))
    list_count = sum(1 for v in values if isinstance(v, list))
    total = len(values)

    if dict_count / total >= threshold:
        return "dict"
    if list_count / total >= threshold:
        return "list"
    return None


def _format_any_value(value: Any, cfg: Config) -> str:
    """Recursively format any value without schema."""
    if value is None:
        return ""
    if isinstance(value, dict):
        if not value:
            return f"{cfg.dict_open.rstrip()}{cfg.dict_close.lstrip()}"
        pairs = [cfg.format_kv(k, _format_any_value(v, cfg)) for k, v in value.items()]
        return f"{cfg.dict_open}{cfg.spaced_delimiter.join(pairs)}{cfg.dict_close}"
    if isinstance(value, list):
        if not value:
            return f"{cfg.list_open.rstrip()}{cfg.list_close.lstrip()}"
        formatted = [_format_any_value(x, cfg) for x in value]
        return f"{cfg.list_open}{cfg.spaced_delimiter.join(formatted)}{cfg.list_close}"
    return _normalize(value)


def _analyze_keys(items: list[dict], sparsity_threshold: float) -> KeyAnalysis:
    if not items:
        return KeyAnalysis()

    all_keys = list(dict.fromkeys(key for item in items for key in item))
    counts = Counter(key for item in items for key in item)
    total = len(items)

    return KeyAnalysis(
        common=[k for k in all_keys if counts[k] / total >= sparsity_threshold],
        sparse=[k for k in all_keys if counts[k] / total < sparsity_threshold],
    )


def _create_header_element(key: str, items: list[dict], cfg: Config) -> HeaderElement:
    values = [v for item in items if (v := item.get(key)) is not None]

    if not values:
        return HeaderElement(name=key, cfg=cfg)

    # Use majority-based type detection instead of all()
    majority = _majority_type(values, cfg.sparsity_threshold)

    if majority == "dict":
        # Filter to only dict values for schema analysis
        dict_values = [v for v in values if isinstance(v, dict)]
        analysis = _analyze_keys(dict_values, cfg.sparsity_threshold)
        nested_schema = [_create_header_element(k, dict_values, cfg) for k in analysis.common]
        return HeaderElement(name=key, cfg=cfg, type="dict", schema=nested_schema, has_sparse=analysis.has_sparse)

    if majority == "list":
        # Flatten all list items, filtering out None
        list_values = [v for v in values if isinstance(v, list)]
        all_items = [x for sublist in list_values for x in sublist if x is not None]

        # Use majority-based detection for list items too
        item_majority = _majority_type(all_items, cfg.sparsity_threshold)

        if item_majority == "dict":
            dict_items = [x for x in all_items if isinstance(x, dict)]
            analysis = _analyze_keys(dict_items, cfg.sparsity_threshold)
            nested_schema = [_create_header_element(k, dict_items, cfg) for k in analysis.common]
            return HeaderElement(
                name=key, cfg=cfg, type="list", list_type="dict", schema=nested_schema, has_sparse=analysis.has_sparse
            )

        return HeaderElement(name=key, cfg=cfg, type="list", list_type="simple")

    return HeaderElement(name=key, cfg=cfg)


def _build_header(items: list[dict], cfg: Config) -> list[HeaderElement]:
    if not items:
        return []

    all_keys = dict.fromkeys(key for item in items for key in item)
    return [
        _create_header_element(key, items, cfg)
        for key in all_keys
        if sum(1 for item in items if key in item) / len(items) >= cfg.sparsity_threshold
    ]


def _format_dict_pairs(data: dict, cfg: Config) -> list[str]:
    return [cfg.format_kv(k, _normalize(v)) for k, v in data.items()]


def _format_dict(data: dict, element: HeaderElement, cfg: Config) -> str:
    if not data:
        return f"{cfg.dict_open.rstrip()}{cfg.dict_close.lstrip()}"

    # Recursively format each child element
    common_values = [_format_value(data.get(child.name), child, cfg) for child in element.schema]
    sparse_pairs = []
    if element.has_sparse:
        # Use _format_any_value for recursive formatting of sparse values
        sparse_pairs = [
            cfg.format_kv(k, _format_any_value(v, cfg)) for k, v in data.items() if k not in element.schema_keys
        ]

    content = cfg.spaced_delimiter.join(common_values + sparse_pairs)
    return f"{cfg.dict_open}{content}{cfg.dict_close}"


def _format_list(data: list, element: HeaderElement, cfg: Config) -> str:
    if not data:
        return f"{cfg.list_open.rstrip()}{cfg.list_close.lstrip()}"

    if element.list_type == "dict":
        # Check each item type, fall back if not dict
        formatted = []
        for item in data:
            if isinstance(item, dict):
                formatted.append(_format_dict(item, element, cfg))
            else:
                formatted.append(_format_any_value(item, cfg))
        return f"{cfg.list_open}{cfg.spaced_delimiter.join(formatted)}{cfg.list_close}"

    # Simple list - use recursive formatter for all items (handles nested lists, mixed content)
    return f"{cfg.list_open}{cfg.spaced_delimiter.join(_format_any_value(x, cfg) for x in data)}{cfg.list_close}"


def _format_value(value: Any, element: HeaderElement, cfg: Config) -> str:
    if value is None:
        return ""

    # Check actual type matches expected schema type
    if element.type == "dict":
        if isinstance(value, dict):
            return _format_dict(value, element, cfg)
        # Type mismatch - fall back to recursive formatter
        return _format_any_value(value, cfg)

    if element.type == "list":
        if isinstance(value, list):
            return _format_list(value, element, cfg)
        # Type mismatch - fall back to recursive formatter
        return _format_any_value(value, cfg)

    return _normalize(value)


def _format_sparse_field(key: str, value: Any, cfg: Config) -> str:
    if isinstance(value, dict):
        if not value:
            return f"{key}{cfg.dict_open.rstrip()}{cfg.dict_close.lstrip()}"
        # Use _format_any_value for recursive formatting
        pairs = [cfg.format_kv(k, _format_any_value(v, cfg)) for k, v in value.items()]
        return f"{key}{cfg.dict_open}{cfg.spaced_delimiter.join(pairs)}{cfg.dict_close}"

    if isinstance(value, list):
        if not value:
            return f"{key}{cfg.list_open.rstrip()}{cfg.list_close.lstrip()}"
        # Use _format_any_value for all items (handles dicts, nested lists, etc.)
        formatted = [_format_any_value(x, cfg) for x in value]
        return f"{key}{cfg.list_open}{cfg.spaced_delimiter.join(formatted)}{cfg.list_close}"

    return cfg.format_kv(key, _normalize(value))


def _format_row(item: dict, header: list[HeaderElement], cfg: Config) -> str:
    header_keys = {el.name for el in header}
    header_parts = [_format_value(item.get(el.name), el, cfg) for el in header]
    sparse_parts = [_format_sparse_field(k, item[k], cfg) for k in item if k not in header_keys]
    return cfg.spaced_delimiter.join(header_parts + sparse_parts)


def _serialize(data: list[dict], cfg: Config) -> str:
    header = _build_header(data, cfg)
    rows = [cfg.cleanup(_format_row(item, header, cfg)) for item in data]
    header_str = cfg.cleanup(cfg.spaced_delimiter.join(h.to_string() for h in header))

    # Build header block (header + optional separator)
    header_block = [header_str]
    if cfg.header_separator:
        sep_row = cfg.spaced_delimiter.join(cfg.header_separator for _ in header)
        header_block.append(sep_row)

    # Insert header at start and optionally repeat every N rows
    lines = list(header_block)
    for i, row in enumerate(rows):
        lines.append(row)
        # Insert header after every N data rows (not after the last row)
        if cfg.header_repeat_interval and (i + 1) % cfg.header_repeat_interval == 0 and i < len(rows) - 1:
            lines.extend(header_block)

    # Wrap lines with delimiter (e.g., for markdown tables)
    if cfg.wrap_lines:
        w = cfg.wrap_lines
        lines = [f"{w}{line}{w}" for line in lines]
    text_str = "\n".join(lines)
    text_str = text_str.replace(" \n", "\n")
    # Strip trailing delimiter before newlines (but not for markdown tables)
    if cfg.strip_trailing_delimiter:
        for _ in range(3):
            text_str = text_str.replace(f"{cfg.delimiter}\n", "\n")
    if text_str.endswith(" "):
        return text_str[:-1]
    return text_str


# --- Public API ---


def minemize(
    data: list | dict,
    *,
    preset: Config | None = None,
    delimiter: str | None = _NOT_PROVIDED,
    use_spaces: bool | None = _NOT_PROVIDED,
    sparsity_threshold: float | None = _NOT_PROVIDED,
    sparse_indicator: str | None = _NOT_PROVIDED,
    header_separator: str | None = _NOT_PROVIDED,
    wrap_lines: str | None = _NOT_PROVIDED,
    common_optimizations: bool | None = _NOT_PROVIDED,
    header_repeat_interval: int | None = _NOT_PROVIDED,
) -> str:
    """Minimize your data into a compact string format.

    Args:
        data: A list of dicts or a single dict to minemize
        preset: Pre-configured Config (e.g., presets.markdown, presets.csv)
        delimiter: Field separator (default: ";")
        use_spaces: Whether to use spaces around delimiters (default: True)
        sparsity_threshold: Frequency threshold for including keys in header (default: 0.5)
        sparse_indicator: Indicator for sparse fields in header (default: "...")
        header_separator: Separator row after header, e.g., "---" for markdown tables
        wrap_lines: Wrap each line with this string (e.g., "|" for markdown tables)
        common_optimizations: Use :true/:false/:null for single-token encoding (default: True)
        header_repeat_interval: Repeat header/schema every N data rows (default: None = no repeat)

    Returns:
        str: The minemized representation

    Examples:
        # Using presets
        from minemizer import presets
        minemize(data, preset=presets.markdown)
        minemize(data, preset=presets.csv)

        # Custom options
        minemize(data, delimiter="|", header_separator="---")

        # Repeat header every 100 rows for better LLM context
        minemize(data, header_repeat_interval=100)
    """
    if isinstance(data, dict):
        data = [data]

    if not data or not isinstance(data, list):
        return ""

    # Start from preset or global config
    base = preset if preset is not None else _global_config

    cfg = base.derive(
        delimiter=delimiter,
        use_spaces=use_spaces,
        sparsity_threshold=sparsity_threshold,
        sparse_indicator=sparse_indicator,
        header_separator=header_separator,
        wrap_lines=wrap_lines,
        common_optimizations=common_optimizations,
        header_repeat_interval=header_repeat_interval,
    )
    return _serialize(data, cfg)
