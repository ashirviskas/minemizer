"""Global configuration for minemizer."""

from dataclasses import dataclass, replace
from typing import Any

# Sentinel for "not provided" (distinct from None)
_NOT_PROVIDED: Any = object()


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
    header_repeat_interval: int | None = 100  # Repeat header every N data rows (None = no repeat)
    strip_trailing_delimiter: bool = True  # Strip trailing delimiter before newlines (disable for markdown)

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
        d_non_spaced = self.delimiter
        kv = self.spaced_kv_separator
        openers = [self.dict_open, self.list_open]
        closers = [self.dict_close, self.list_close]

        # Token optimizations: ": true" → ":true" etc (single tokens in most tokenizers)
        if self.common_optimizations:
            for val in ["true", "false", "null"]:
                text = text.replace(f"{kv}{val}", f":{val}")
                text = text.replace(f"{d}{val}", f"{d.rstrip()}{val}")

        all_stuff = [d, d_non_spaced, kv] + openers + closers
        # Fix: "; ;" → ";;" and "; {" → ";{" and "; [" → ";[" and "[ ;" → "[;" etc"
        for stuff_a in all_stuff:
            stuff_a_stripped = stuff_a.strip()
            for stuff_b in all_stuff:
                stuff_b_stripped = stuff_b.strip()
                # May be dumb, but it works.
                text = text.replace(f"{stuff_a_stripped}  {stuff_b_stripped}", f"{stuff_a_stripped} {stuff_b_stripped}")
                text = text.replace(f"{stuff_a_stripped} {stuff_b_stripped}", f"{stuff_a_stripped}{stuff_b_stripped}")

        text = text.replace(" \n", "\n")
        text = text.replace(" \n", "\n")

        return text

    def derive(self, **overrides) -> "Config":
        """Create a new Config with overrides applied.

        Uses _NOT_PROVIDED sentinel to distinguish between "not provided" and explicit None.
        """
        filtered = {k: v for k, v in overrides.items() if v is not _NOT_PROVIDED}
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
        strip_trailing_delimiter=False,  # Keep trailing | for proper markdown tables
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
