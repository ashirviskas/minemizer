"""Core functionality for minemizer."""

from collections import Counter
from dataclasses import dataclass, field
from typing import Any


@dataclass
class KeyAnalysis:
    """Results from analyzing which keys are common vs sparse."""

    common: set[str] = field(default_factory=set)
    sparse: set[str] = field(default_factory=set)

    @property
    def has_sparse(self) -> bool:
        return bool(self.sparse)


@dataclass
class HeaderElement:
    """Schema definition for a single field in the header."""

    name: str
    type: str = "value"  # "value", "dict", "list"
    schema: list[str] = field(default_factory=list)  # For dict/list of dict
    has_sparse: bool = False
    list_type: str | None = None  # "dict" or "simple" for lists

    def to_string(self) -> str:
        """Convert this header element to its string representation."""
        if self.type == "value":
            return self.name

        schema_str = "; ".join(self.schema)
        if self.has_sparse:
            schema_str = f"{schema_str}; ..." if schema_str else "..."

        if self.type == "dict":
            return f"{self.name}{{ {schema_str}}}"
        elif self.type == "list" and self.list_type == "dict":
            return f"{self.name}[{{ {schema_str}}}]"
        else:  # list with simple type
            return f"{self.name}[]"


@dataclass
class SerializerConfig:
    """Configuration for the serializer."""

    threshold: float = 0.9
    use_spaces: bool = True

    @property
    def delimiter(self) -> str:
        return "; " if self.use_spaces else ";"

    @property
    def dict_open(self) -> str:
        return "{ " if self.use_spaces else "{"

    @property
    def list_open(self) -> str:
        return "[ " if self.use_spaces else "["


class SchemaMinemizer:
    def __init__(self, config: SerializerConfig | None = None):
        self.config = config or SerializerConfig()

    def minemize(self, data: list | dict) -> str:
        """Main entry point - converts data to our schema format."""
        if isinstance(data, dict):
            data = [data]

        if not data or not isinstance(data, list):
            return ""

        header = self._build_header(data)
        rows = [self._format_row(item, header) for item in data]
        header_str = self.config.delimiter.join(h.to_string() for h in header)
        return "\n".join([header_str] + rows)

    def _analyze_keys(self, items: list[dict]) -> KeyAnalysis:
        """Analyze which keys appear frequently enough for the header."""
        if not items:
            return KeyAnalysis()

        key_counts = Counter(key for item in items for key in item)
        total = len(items)
        threshold = self.config.threshold

        return KeyAnalysis(
            common={key for key, count in key_counts.items() if count / total >= threshold},
            sparse={key for key, count in key_counts.items() if count / total < threshold},
        )

    def _build_header(self, items: list[dict]) -> list[HeaderElement]:
        """Build the header schema from data."""
        if not items:
            return []

        all_keys = {key for item in items for key in item}
        return [
            self._create_header_element(key, items)
            for key in all_keys
            if self._should_include_key(key, items)
        ]

    def _create_header_element(self, key: str, all_items: list) -> HeaderElement:
        """Create a header element with type information from ALL values."""
        values = [v for item in all_items if (v := item.get(key)) is not None]

        if not values:
            return HeaderElement(name=key)

        if all(isinstance(v, dict) for v in values):
            analysis = self._analyze_keys(values)
            return HeaderElement(
                name=key,
                type="dict",
                schema=list(analysis.common),
                has_sparse=analysis.has_sparse,
            )

        if all(isinstance(v, list) for v in values):
            all_list_items = [item for sublist in values for item in sublist]
            if all_list_items and all(isinstance(item, dict) for item in all_list_items):
                analysis = self._analyze_keys(all_list_items)
                return HeaderElement(
                    name=key,
                    type="list",
                    list_type="dict",
                    schema=list(analysis.common),
                    has_sparse=analysis.has_sparse,
                )
            return HeaderElement(name=key, type="list", list_type="simple")

        return HeaderElement(name=key)

    def _should_include_key(self, key: str, items: list) -> bool:
        """Check if key appears in enough items to include in header."""
        return sum(1 for item in items if key in item) / len(items) >= self.config.threshold

    def _format_row(self, item: dict, header: list[HeaderElement]) -> str:
        """Format a data row according to the header schema."""
        header_keys = {element.name for element in header}

        # Format header fields
        header_parts = [self._format_value(item.get(element.name), element) for element in header]

        # Format sparse fields
        sparse_parts = [
            self._format_sparse_field(key, item[key]) for key in item if key not in header_keys
        ]

        return self.config.delimiter.join(header_parts + sparse_parts)

    def _format_value(self, value: Any, element: HeaderElement) -> str:
        """Format a value according to its element type."""
        if value is None:
            return ""
        if element.type == "dict":
            return self._format_dict(value, element)
        if element.type == "list":
            return self._format_list(value, element)
        return str(value)

    def _normalize_value(self, value: Any) -> str:
        """Normalize a value for output (handles booleans)."""
        return str(value).lower() if isinstance(value, bool) else str(value)

    def _format_dict_pairs(self, data: dict) -> list[str]:
        """Format dict items as key:value pairs."""
        return [f"{k}:{self._normalize_value(v)}" for k, v in data.items()]

    def _format_sparse_field(self, key: str, value: Any) -> str:
        """Format a sparse field (not in header) with key prefix."""
        if isinstance(value, dict):
            if not value:
                return f"{key}{{}}"
            pairs = self._format_dict_pairs(value)
            return f"{key}{self.config.dict_open}{self.config.delimiter.join(pairs)}}}"

        if isinstance(value, list):
            if not value:
                return f"{key}[]"
            if all(isinstance(item, dict) for item in value):
                formatted = [
                    f"{self.config.dict_open}{self.config.delimiter.join(self._format_dict_pairs(d))}}}"
                    for d in value
                ]
                return f"{key}{self.config.list_open}{self.config.delimiter.join(formatted)}]"
            items_str = self.config.delimiter.join(str(item) for item in value)
            return f"{key}{self.config.list_open}{items_str}]"

        return f"{key}:{value}"

    def _format_dict(self, data: dict, element: HeaderElement) -> str:
        """Format a dict according to its schema."""
        if not data:
            return "{}"

        # Common keys in schema order
        common_values = [self._normalize_value(data.get(key, "")) for key in element.schema]

        # Sparse keys as key:value
        sparse_pairs = []
        if element.has_sparse:
            schema_keys = set(element.schema)
            sparse_pairs = [
                f"{k}:{self._normalize_value(v)}" for k, v in data.items() if k not in schema_keys
            ]

        content = self.config.delimiter.join(common_values + sparse_pairs)
        return f"{self.config.dict_open}{content}}}"

    def _format_list(self, data: list, element: HeaderElement) -> str:
        """Format a list according to its schema."""
        if not data:
            return "[]"

        if element.list_type == "dict":
            formatted = [self._format_dict(item, element) for item in data]
            return f"{self.config.list_open}{self.config.delimiter.join(formatted)}]"

        items_str = self.config.delimiter.join(str(item) for item in data)
        return f"{self.config.list_open}{items_str}]"


def minemize(data: list | dict, threshold: float = 0.5, use_spaces: bool = True) -> str:
    """Minimize your data into a compact string format.

    Args:
        data: A list of dicts or a single dict to minemize
        threshold: Frequency threshold for including keys in header (0.0-1.0)
        use_spaces: Whether to use spaces around delimiters

    Returns:
        str: The minemized representation
    """
    config = SerializerConfig(threshold=threshold, use_spaces=use_spaces)
    return SchemaMinemizer(config).minemize(data)
