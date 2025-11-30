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

    @property
    def spaced_delimiter(self) -> str:
        return f"{self.delimiter} " if self.use_spaces else self.delimiter

    @property
    def dict_open(self) -> str:
        return "{ " if self.use_spaces else "{"

    @property
    def list_open(self) -> str:
        return "[ " if self.use_spaces else "["

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
