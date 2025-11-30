"""Global configuration for minemizer."""

from dataclasses import dataclass, replace


@dataclass
class Config:
    """Configuration for minemize().

    Global singleton available as `minemizer.config`.
    Set attributes directly to change defaults:

        from minemizer import config
        config.delimiter = "|"
        config.threshold = 0.9
    """

    delimiter: str = ";"
    use_spaces: bool = True
    threshold: float = 0.5
    sparse_indicator: str = "..."

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


# Module-level singleton - Python guarantees single instantiation
config = Config()
