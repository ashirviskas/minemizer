"""Markdown output generation."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING

from benchmarks.config import FORMAT_LABELS, FORMATS, SHORT_NAMES

if TYPE_CHECKING:
    from benchmarks.runners.compression import BenchmarkResults


def generate_markdown(results: BenchmarkResults) -> str:
    """Generate markdown table for benchmark results."""
    lines = [f"_Last updated: {date.today().isoformat()}_", ""]

    fixture_names = [f.fixture_name for f in results.fixtures]
    total_fixtures = len(results.fixtures)

    # Compute normalized ratios (JSON pretty = 1.0x baseline)
    fixture_ratios, best_per_fixture = _compute_ratios(results)

    # Find best average among complete formats
    best_avg = _find_best_average(fixture_ratios, total_fixtures, fixture_names)

    # Build table
    lines.append("### Token efficiency (normalized, JSON pretty = 1.0x)")
    lines.append("")

    header = ["Format", *[SHORT_NAMES.get(f, f) for f in fixture_names], "avg"]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("|" + "|".join(["---"] * len(header)) + "|")

    for fmt in FORMATS:
        row = _format_row(fmt, fixture_names, fixture_ratios, best_per_fixture, best_avg, total_fixtures)
        lines.append("| " + " | ".join(row) + " |")

    lines.extend(
        [
            "",
            "_Higher is better. ✗ = format cannot represent this data type. \\*\\* = average from partial data._",
            "",
            "See [token visualization](benchmarks/results/compression/benchmark_tokens.html) for detailed "
            "tokenization comparison across different tokenizers.",
            "",
        ]
    )

    return "\n".join(lines)


def update_readme(content: str, readme_path: Path) -> bool:
    """Update README.md with benchmark results between markers.

    Returns True if updated, False if markers not found.
    """
    readme_text = readme_path.read_text()
    pattern = r"<!-- BENCHMARK_START -->.*<!-- BENCHMARK_END -->"
    replacement = f"<!-- BENCHMARK_START -->\n{content}<!-- BENCHMARK_END -->"

    updated = re.sub(pattern, replacement, readme_text, flags=re.DOTALL)

    if updated == readme_text:
        return False

    readme_path.write_text(updated)
    return True


def _compute_ratios(
    results: BenchmarkResults,
) -> tuple[dict[str, dict[str, float | None]], dict[str, float]]:
    """Compute normalized token ratios for each format/fixture."""
    fixture_ratios: dict[str, dict[str, float | None]] = {fmt: {} for fmt in FORMATS}
    best_per_fixture: dict[str, float] = {}

    for fixture in results.fixtures:
        # Get JSON pretty baseline
        json_pretty = next(r for r in fixture.results if r.format_name == "json_pretty")
        base_chars = json_pretty.chars
        assert base_chars is not None

        jp_tokens = sum(v for v in json_pretty.tokens.values() if v is not None)
        jp_tokens /= len(json_pretty.tokens)
        baseline = base_chars / jp_tokens

        best = 0.0
        for result in fixture.results:
            if result.chars is None:
                fixture_ratios[result.format_name][fixture.fixture_name] = None
                continue

            avg_tokens = sum(v for v in result.tokens.values() if v is not None)
            avg_tokens /= len(result.tokens)
            raw_ratio = base_chars / avg_tokens
            normalized = raw_ratio / baseline
            fixture_ratios[result.format_name][fixture.fixture_name] = normalized
            best = max(best, normalized)

        best_per_fixture[fixture.fixture_name] = best

    return fixture_ratios, best_per_fixture


def _find_best_average(
    fixture_ratios: dict[str, dict[str, float | None]],
    total_fixtures: int,
    fixture_names: list[str],
) -> float:
    """Find best average among formats with complete data."""
    best = 0.0
    for fmt in FORMATS:
        ratios = [fixture_ratios[fmt].get(f) for f in fixture_names]
        valid = [r for r in ratios if r is not None]
        if len(valid) == total_fixtures and valid:
            best = max(best, sum(valid) / len(valid))
    return best


def _format_row(
    fmt: str,
    fixture_names: list[str],
    fixture_ratios: dict[str, dict[str, float | None]],
    best_per_fixture: dict[str, float],
    best_avg: float,
    total_fixtures: int,
) -> list[str]:
    """Format a single table row."""
    label = FORMAT_LABELS[fmt]
    row = [label]
    ratios_list: list[float] = []

    for fixture_name in fixture_names:
        ratio = fixture_ratios[fmt].get(fixture_name)
        if ratio:
            ratios_list.append(ratio)
            val = f"{ratio:.1f}x"
            if ratio == best_per_fixture[fixture_name]:
                val = f"**{val}**"
            row.append(val)
        else:
            row.append("✗")

    # Average
    if ratios_list:
        avg = sum(ratios_list) / len(ratios_list)
        val = f"{avg:.1f}x"
        if len(ratios_list) == total_fixtures and avg == best_avg:
            val = f"**{val}**"
        elif len(ratios_list) < total_fixtures:
            val = f"{val}\\*\\*"
        row.append(val)
    else:
        row.append("N/A")

    return row
