"""Core functionality for minemizer."""

from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from minemizer.config import Config
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
    type: str = "value"  # "value", "dict", "list"
    schema: list[str] = field(default_factory=list)
    has_sparse: bool = False
    list_type: str | None = None
    delimiter: str = "; "
    sparse_indicator: str = "..."

    def to_string(self) -> str:
        if self.type == "value":
            return self.name

        schema_str = self.delimiter.join(self.schema)
        if self.has_sparse:
            schema_str = f"{schema_str}{self.delimiter}{self.sparse_indicator}" if schema_str else self.sparse_indicator

        if self.type == "dict":
            return f"{self.name}{{ {schema_str}}}"
        elif self.type == "list" and self.list_type == "dict":
            return f"{self.name}[{{ {schema_str}}}]"
        return f"{self.name}[]"


# --- Pure functions ---


def _normalize(value: Any) -> str:
    return str(value).lower() if isinstance(value, bool) else str(value)


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
    delim = cfg.spaced_delimiter
    sparse = cfg.sparse_indicator

    if not values:
        return HeaderElement(name=key, delimiter=delim, sparse_indicator=sparse)

    if all(isinstance(v, dict) for v in values):
        analysis = _analyze_keys(values, cfg.sparsity_threshold)
        return HeaderElement(
            name=key,
            type="dict",
            schema=analysis.common,
            has_sparse=analysis.has_sparse,
            delimiter=delim,
            sparse_indicator=sparse,
        )

    if all(isinstance(v, list) for v in values):
        all_items = [x for sublist in values for x in sublist]
        if all_items and all(isinstance(x, dict) for x in all_items):
            analysis = _analyze_keys(all_items, cfg.sparsity_threshold)
            return HeaderElement(
                name=key,
                type="list",
                list_type="dict",
                schema=analysis.common,
                has_sparse=analysis.has_sparse,
                delimiter=delim,
                sparse_indicator=sparse,
            )
        return HeaderElement(name=key, type="list", list_type="simple", delimiter=delim, sparse_indicator=sparse)

    return HeaderElement(name=key, delimiter=delim, sparse_indicator=sparse)


def _build_header(items: list[dict], cfg: Config) -> list[HeaderElement]:
    if not items:
        return []

    all_keys = dict.fromkeys(key for item in items for key in item)
    return [
        _create_header_element(key, items, cfg)
        for key in all_keys
        if sum(1 for item in items if key in item) / len(items) >= cfg.sparsity_threshold
    ]


def _format_dict_pairs(data: dict) -> list[str]:
    return [f"{k}:{_normalize(v)}" for k, v in data.items()]


def _format_dict(data: dict, element: HeaderElement, cfg: Config) -> str:
    if not data:
        return "{}"

    common_values = [_normalize(data.get(key, "")) for key in element.schema]
    sparse_pairs = []
    if element.has_sparse:
        schema_keys = set(element.schema)
        sparse_pairs = [f"{k}:{_normalize(v)}" for k, v in data.items() if k not in schema_keys]

    content = cfg.spaced_delimiter.join(common_values + sparse_pairs)
    return f"{cfg.dict_open}{content}}}"


def _format_list(data: list, element: HeaderElement, cfg: Config) -> str:
    if not data:
        return "[]"

    if element.list_type == "dict":
        formatted = [_format_dict(item, element, cfg) for item in data]
        return f"{cfg.list_open}{cfg.spaced_delimiter.join(formatted)}]"

    return f"{cfg.list_open}{cfg.spaced_delimiter.join(str(x) for x in data)}]"


def _format_value(value: Any, element: HeaderElement, cfg: Config) -> str:
    if value is None:
        return ""
    if element.type == "dict":
        return _format_dict(value, element, cfg)
    if element.type == "list":
        return _format_list(value, element, cfg)
    return str(value)


def _format_sparse_field(key: str, value: Any, cfg: Config) -> str:
    if isinstance(value, dict):
        if not value:
            return f"{key}{{}}"
        pairs = _format_dict_pairs(value)
        return f"{key}{cfg.dict_open}{cfg.spaced_delimiter.join(pairs)}}}"

    if isinstance(value, list):
        if not value:
            return f"{key}[]"
        if all(isinstance(x, dict) for x in value):
            delim = cfg.spaced_delimiter
            formatted = [f"{cfg.dict_open}{delim.join(_format_dict_pairs(d))}}}" for d in value]
            return f"{key}{cfg.list_open}{delim.join(formatted)}]"
        return f"{key}{cfg.list_open}{cfg.spaced_delimiter.join(str(x) for x in value)}]"

    return f"{key}:{value}"


def _format_row(item: dict, header: list[HeaderElement], cfg: Config) -> str:
    header_keys = {el.name for el in header}
    header_parts = [_format_value(item.get(el.name), el, cfg) for el in header]
    sparse_parts = [_format_sparse_field(k, item[k], cfg) for k in item if k not in header_keys]
    return cfg.spaced_delimiter.join(header_parts + sparse_parts)


def _serialize(data: list[dict], cfg: Config) -> str:
    header = _build_header(data, cfg)
    rows = [_format_row(item, header, cfg) for item in data]
    header_str = cfg.spaced_delimiter.join(h.to_string() for h in header)

    lines = [header_str]
    if cfg.header_separator:
        sep_row = cfg.spaced_delimiter.join(cfg.header_separator for _ in header)
        lines.append(sep_row)
    lines.extend(rows)

    # Wrap lines with delimiter (e.g., for markdown tables)
    if cfg.wrap_lines:
        w = cfg.wrap_lines
        lines = [f"{w}{line}{w}" for line in lines]

    return "\n".join(lines)


# --- Public API ---


def minemize(
    data: list | dict,
    *,
    preset: Config | None = None,
    delimiter: str | None = None,
    use_spaces: bool | None = None,
    sparsity_threshold: float | None = None,
    sparse_indicator: str | None = None,
    header_separator: str | None = None,
    wrap_lines: str | None = None,
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

    Returns:
        str: The minemized representation

    Examples:
        # Using presets
        from minemizer import presets
        minemize(data, preset=presets.markdown)
        minemize(data, preset=presets.csv)

        # Custom options
        minemize(data, delimiter="|", header_separator="---")
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
    )
    return _serialize(data, cfg)
