"""Format conversion utilities."""

from __future__ import annotations

import csv
import io
import json

import tson
import yaml
from toon_format import encode as toon_encode

from minemizer import minemize, presets


def has_nested_structures(data: list[dict]) -> bool:
    """Check if any item has nested dicts or lists."""
    return any(isinstance(v, (dict, list)) for item in data for v in item.values())


def convert_to_format(data: list[dict], format_name: str) -> str | None:
    """Convert data to the specified format.

    Returns None if the format cannot represent this data structure.
    """
    converters = {
        "json_pretty": lambda d: json.dumps(d, indent=2),
        "json_min": lambda d: json.dumps(d, separators=(",", ":")),
        "csv": _to_csv,
        "tsv": _to_tsv,
        "yaml": lambda d: yaml.dump(d, default_flow_style=False, allow_unicode=True),
        "toon": toon_encode,
        "tson": tson.dumps,
        # minemizer variants - default now has header_repeat_interval=100
        "minemizer": minemize,
        "minemizer_no_repeat": lambda d: minemize(d, header_repeat_interval=None),
        "minemizer_compact": lambda d: minemize(d, preset=presets.compact),
        "minemizer_prefixed": lambda d: minemize(d, row_prefix="- ", schema_prefix="> ", header_repeat_interval=None),
        "minemizer_repeat10_prefixed": lambda d: minemize(
            d, row_prefix="- ", schema_prefix="> ", header_repeat_interval=10
        ),
        # Low sparsity threshold variants (0.2 = include keys appearing in 20%+ of records)
        "minemizer_low_sparsity": lambda d: minemize(d, sparsity_threshold=0.2),
        "minemizer_repeat10_prefixed_low_sparsity": lambda d: minemize(
            d, row_prefix="- ", schema_prefix="> ", header_repeat_interval=10, sparsity_threshold=0.2
        ),
        # Repeat keys every 10 rows (for flat data)
        "minemizer_repeat10": lambda d: minemize(d, header_repeat_interval=10),
        "minemizer_compact_repeat10": lambda d: minemize(d, preset=presets.compact, header_repeat_interval=10),
    }

    converter = converters.get(format_name)
    if not converter:
        raise ValueError(f"Unknown format: {format_name}")

    try:
        return converter(data)
    except Exception:
        return None


def _to_csv(data: list[dict]) -> str | None:
    if has_nested_structures(data):
        return None
    if not data:
        return ""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()


def _to_tsv(data: list[dict]) -> str | None:
    if has_nested_structures(data):
        return None
    if not data:
        return ""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys(), delimiter="\t")
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()
