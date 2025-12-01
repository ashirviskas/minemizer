"""Global configuration for minemizer."""

from dataclasses import dataclass, replace


@dataclass
class Config:
    """Configuration for minemize().

    Global singleton available as `minemizer.config`.
    Set attributes directly to change defaults:

        from minemizer import config
        config.delimiter = "|"
        config.sparsity_threshold = 0.9
    """

    delimiter: str = ";"
    use_spaces: bool = True
    sparsity_threshold: float = 0.5
    sparse_indicator: str = "..."
    header_separator: str | None = None
    wrap_lines: str | None = None
    common_optimizations: bool = True  # Use :true/:false/:null (single tokens in most tokenizers)

    @property
    def spaced_delimiter(self) -> str:
        return f"{self.delimiter} " if self.use_spaces else self.delimiter

    @property
    def spaced_kv_separator(self) -> str:
        return ": " if self.use_spaces else ":"

    def format_kv(self, key: str, value: str) -> str:
        """Format key-value pair."""
        return f"{key}{self.spaced_kv_separator}{value}"

    @property
    def dict_open(self) -> str:
        return "{ " if self.use_spaces else "{"

    @property
    def list_open(self) -> str:
        return "[ " if self.use_spaces else "["

    @property
    def dict_close(self) -> str:
        return "}"

    @property
    def list_close(self) -> str:
        return "]"

    def cleanup(self, text: str) -> str:
        """Apply all text optimizations."""
        if not self.use_spaces:
            return text

        d = self.spaced_delimiter
        kv = self.spaced_kv_separator
        openers = [self.dict_open, self.list_open]

        # Token optimizations: ": true" → ":true" etc (single tokens in most tokenizers)
        if self.common_optimizations:
            for val in ["true", "false", "null"]:
                text = text.replace(f"{kv}{val}", f":{val}")
                text = text.replace(f"{d}{val}", f"{d.rstrip()}{val}")

        # Fix: "; ;" → ";;" and "; {" → ";{" and "; [" → ";["
        for suffix in [d.lstrip()] + openers:
            text = text.replace(d + suffix, d.rstrip() + suffix)

        # Fix: ": {" → ":{" and ": [" → ":[" (kv separator before opener)
        for opener in openers:
            text = text.replace(kv + opener, kv.rstrip() + opener)

        # Fix: "[ {" → "[{" and "{ [" → "{[" etc (opener after opener)
        for op1 in openers:
            for op2 in openers:
                text = text.replace(op1 + op2, op1.rstrip() + op2)

        return text

    def derive(self, **overrides) -> "Config":
        """Create a new Config with non-None overrides applied."""
        filtered = {k: v for k, v in overrides.items() if v is not None}
        return replace(self, **filtered) if filtered else self


class presets:  # noqa: N801 - lowercase intentional for API style
    """Pre-configured Config instances for common formats.

    Usage:
        from minemizer import presets
        minemize(data, preset=presets.markdown)
        minemize(data, preset=presets.llm)  # alias for default
    """

    # Default: optimized for LLM token efficiency
    # - semicolon delimiter (single char, rarely appears in data)
    # - spaces for readability without excessive tokens
    # - 50% threshold balances schema info vs row verbosity
    default = Config()
    llm = default  # alias: explicit name for LLM-optimized preset

    # Markdown table: renders as proper table in markdown viewers
    markdown = Config(
        delimiter="|",
        use_spaces=True,
        header_separator="---",
        wrap_lines="|",
    )

    # CSV: standard comma-separated values
    csv = Config(
        delimiter=",",
        use_spaces=False,
    )

    # TSV: tab-separated values
    tsv = Config(
        delimiter="\t",
        use_spaces=False,
    )

    # Compact: minimal tokens, no spaces
    compact = Config(
        delimiter=";",
        use_spaces=False,
    )


# Module-level singleton (starts with default preset)
config = Config()
