"""Output generation for benchmarks."""

from benchmarks.output.html import generate_html
from benchmarks.output.markdown import generate_markdown

__all__ = ["generate_markdown", "generate_html"]
