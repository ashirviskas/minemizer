#!/usr/bin/env python3
"""Benchmark minemizer against other serialization formats."""

from __future__ import annotations

import csv
import io
import json
import re
import time
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING

import tson
import yaml
from toon_format import encode as toon_encode
from transformers import AutoTokenizer

from minemizer import minemize, presets

if TYPE_CHECKING:
    from transformers import PreTrainedTokenizerBase

BENCHMARKS_DIR = Path(__file__).parent.parent / "benchmarks"
FIXTURES_DIR = BENCHMARKS_DIR / "fixtures"
README_PATH = Path(__file__).parent.parent / "README.md"

# Tokenizer configs (all free, no auth required)
# To benchmark others, just add HF model ID here
TOKENIZERS: dict[str, str] = {
    "gpt2": "openai-community/gpt2",
    "llama": "NousResearch/Llama-2-7b-hf",
    "qwen2.5": "Qwen/Qwen2.5-0.5B",
    "Deepseek-V3.2": "deepseek-ai/DeepSeek-V3.2",
}

# Output formats to benchmark
FORMATS = [
    "json_pretty",
    "json_min",
    "csv",
    "tsv",
    "yaml",
    "toon",
    "tson",
    "minemizer",
    "minemizer_compact",
    # "minemizer_33",
    # "minemizer_compact_33",
]

FORMAT_LABELS = {
    "json_pretty": "JSON (pretty)",
    "json_min": "JSON (min)",
    "csv": "CSV",
    "tsv": "TSV",
    "yaml": "YAML",
    "toon": "TOON",
    "tson": "TSON",
    "minemizer": "minemizer",
    "minemizer_33": "minemizer (33%)",
    "minemizer_compact": "minemizer (compact)",
    "minemizer_compact_33": "compact (33%)",
}

# Max lines/characters to show in example outputs (markdown and HTML)
MAX_EXAMPLE_LINES = 25
MAX_EXAMPLE_CHARS = 5000

# Fixture display order (others sorted alphabetically after these)
FIXTURE_ORDER = [
    "simple_flat",
    "nested_objects",
    "lists_of_primitives",
    "sparse_data",
    "coingecko_coins",
    "complex_mixed",
]

# Short display names for fixtures (used in tables)
SHORT_NAMES = {
    "simple_flat": "flat",
    "nested_objects": "nested",
    "lists_of_primitives": "lists",
    "sparse_data": "sparse",
    "coingecko_coins": "coingecko",
    "complex_mixed": "complex",
    "large_non_uniform_nested_mixed": "large_mixed",
    "large_non_uniform_nested_numerical": "large_numerical",
    "large_non_uniform_nested_text": "large_text",
    "books": "books",
    "countries": "countries",
    "mcp_tools_list": "mcp_tools",
}


@dataclass
class BenchmarkResult:
    """Result for a single format conversion."""

    format_name: str
    chars: int | None
    tokens: dict[str, int | None]


@dataclass
class FixtureResult:
    """Results for a single fixture file."""

    fixture_name: str
    results: list[BenchmarkResult]


def load_tokenizers() -> tuple[dict[str, PreTrainedTokenizerBase], float]:
    """Load all tokenizers from HuggingFace. Returns tokenizers and load time."""
    print("Loading tokenizers...")
    start = time.perf_counter()
    tokenizers = {}
    for name, model_id in TOKENIZERS.items():
        t0 = time.perf_counter()
        tokenizers[name] = AutoTokenizer.from_pretrained(model_id)
        elapsed = time.perf_counter() - t0
        print(f"  {name}: {elapsed:.2f}s")
    total = time.perf_counter() - start
    print(f"  Total: {total:.2f}s\n")
    return tokenizers, total


def load_fixtures() -> dict[str, list[dict]]:
    """Load all fixture JSON and JSONL files in specified order."""
    fixtures = {}

    # Load JSON files
    for path in sorted(FIXTURES_DIR.glob("*.json")):
        with path.open() as f:
            fixtures[path.stem] = json.load(f)

    # Load JSONL files (one JSON object per line)
    for path in sorted(FIXTURES_DIR.glob("*.jsonl")):
        with path.open() as f:
            fixtures[path.stem] = [json.loads(line) for line in f if line.strip()]

    # Reorder according to FIXTURE_ORDER
    ordered = {}
    for name in FIXTURE_ORDER:
        if name in fixtures:
            ordered[name] = fixtures.pop(name)
    # Add any remaining fixtures not in FIXTURE_ORDER
    for name in sorted(fixtures.keys()):
        ordered[name] = fixtures[name]
    return ordered


def fmt_num(n: int | float) -> str:
    """Format number with thousand separators."""
    if isinstance(n, float):
        return f"{n:,.1f}"
    return f"{n:,}"


def has_nested_structures(data: list[dict]) -> bool:
    """Check if any item has nested dicts or lists."""
    for item in data:
        for value in item.values():
            if isinstance(value, (dict, list)):
                return True
    return False


def convert_to_format(data: list[dict], format_name: str) -> str | None:
    """Convert data to the specified format. Returns None if conversion fails."""
    try:
        return _convert_to_format(data, format_name)
    except Exception:
        return None


def _convert_to_format(data: list[dict], format_name: str) -> str | None:
    """Internal conversion logic."""
    match format_name:
        case "json_pretty":
            return json.dumps(data, indent=2)

        case "json_min":
            return json.dumps(data, separators=(",", ":"))

        case "csv":
            if has_nested_structures(data):
                return None
            output = io.StringIO()
            if data:
                writer = csv.DictWriter(output, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            return output.getvalue()

        case "tsv":
            if has_nested_structures(data):
                return None
            output = io.StringIO()
            if data:
                writer = csv.DictWriter(output, fieldnames=data[0].keys(), delimiter="\t")
                writer.writeheader()
                writer.writerows(data)
            return output.getvalue()

        case "yaml":
            return yaml.dump(data, default_flow_style=False, allow_unicode=True)

        case "toon":
            return toon_encode(data)

        case "tson":
            return tson.dumps(data)

        case "minemizer":
            return minemize(data)

        case "minemizer_compact":
            return minemize(data, preset=presets.compact)

        case "minemizer_33":
            return minemize(data, sparsity_threshold=0.33)

        case "minemizer_75":
            return minemize(data, sparsity_threshold=0.75)

        case "minemizer_compact_33":
            return minemize(data, preset=presets.compact, sparsity_threshold=0.33)

        case "minemizer_compact_75":
            return minemize(data, preset=presets.compact, sparsity_threshold=0.75)

        case _:
            raise ValueError(f"Unknown format: {format_name}")


def count_tokens(text: str, tokenizer: PreTrainedTokenizerBase) -> int:
    """Count tokens in text using the given tokenizer."""
    return len(tokenizer.encode(text))


def run_benchmarks(
    fixtures: dict[str, list[dict]],
    tokenizers: dict[str, PreTrainedTokenizerBase],
) -> tuple[list[FixtureResult], dict[str, float]]:
    """Run all benchmarks. Returns results and timing stats."""
    results = []
    timing_stats: dict[str, float] = {
        "total": 0.0,
        "conversion": 0.0,
        "tokenization": 0.0,
    }

    total_start = time.perf_counter()

    for fixture_name, data in fixtures.items():
        fixture_start = time.perf_counter()
        fixture_results = []
        fixture_tok_time = 0.0
        fixture_conv_time = 0.0

        for format_name in FORMATS:
            conv_start = time.perf_counter()
            converted = convert_to_format(data, format_name)
            fixture_conv_time += time.perf_counter() - conv_start

            if converted is None:
                # Format doesn't support this data structure
                result = BenchmarkResult(
                    format_name=format_name,
                    chars=None,
                    tokens=dict.fromkeys(tokenizers),
                )
            else:
                tok_start = time.perf_counter()
                tokens: dict[str, int | None] = {name: count_tokens(converted, tok) for name, tok in tokenizers.items()}
                fixture_tok_time += time.perf_counter() - tok_start
                result = BenchmarkResult(
                    format_name=format_name,
                    chars=len(converted),
                    tokens=tokens,
                )

            fixture_results.append(result)

        fixture_total = time.perf_counter() - fixture_start
        timing_stats["conversion"] += fixture_conv_time
        timing_stats["tokenization"] += fixture_tok_time
        print(f"  {fixture_name}: {fixture_total:.2f}s (conv: {fixture_conv_time:.2f}s, tok: {fixture_tok_time:.2f}s)")

        results.append(FixtureResult(fixture_name=fixture_name, results=fixture_results))

    timing_stats["total"] = time.perf_counter() - total_start
    return results, timing_stats


def generate_markdown_table(results: list[FixtureResult], tokenizer_names: list[str]) -> str:
    """Generate markdown content for benchmark results."""
    lines = [f"_Last updated: {date.today().isoformat()}_", ""]

    # Collect stats per format, including per-run chars/token ratio
    format_stats: dict[str, dict] = {fmt: {"chars": [], "tokens": [], "ratios": []} for fmt in FORMATS}

    fixture_names = []
    total_fixtures = len(results)
    for fixture in results:
        fixture_names.append(fixture.fixture_name)
        # Get base chars from JSON pretty for this fixture
        json_pretty_result = next(r for r in fixture.results if r.format_name == "json_pretty")
        base_chars = json_pretty_result.chars
        assert base_chars is not None  # JSON always succeeds

        for result in fixture.results:
            if result.chars is not None:
                format_stats[result.format_name]["chars"].append(result.chars)
                # Average tokens across all tokenizers for this result
                avg_tokens = sum(v for v in result.tokens.values() if v is not None) / len(result.tokens)
                format_stats[result.format_name]["tokens"].append(avg_tokens)
                # Calculate chars/token ratio for this run
                ratio = base_chars / avg_tokens if avg_tokens > 0 else 0
                format_stats[result.format_name]["ratios"].append(ratio)

    # Build per-fixture ratios for detailed table (normalized to JSON pretty = 1.0x)
    fixture_ratios: dict[str, dict[str, float | None]] = {fmt: {} for fmt in FORMATS}
    json_pretty_baseline: dict[str, float] = {}  # baseline ratio per fixture

    for fixture in results:
        json_pretty_result = next(r for r in fixture.results if r.format_name == "json_pretty")
        base_chars = json_pretty_result.chars
        assert base_chars is not None  # JSON always succeeds

        # Calculate JSON pretty baseline (chars/tokens)
        json_pretty_tokens = sum(v for v in json_pretty_result.tokens.values() if v is not None) / len(
            json_pretty_result.tokens
        )
        json_pretty_baseline[fixture.fixture_name] = base_chars / json_pretty_tokens

        for result in fixture.results:
            if result.chars is not None:
                avg_tokens = sum(v for v in result.tokens.values() if v is not None) / len(result.tokens)
                raw_ratio = base_chars / avg_tokens
                # Normalize: how many times better than JSON pretty
                normalized = raw_ratio / json_pretty_baseline[fixture.fixture_name]
                fixture_ratios[result.format_name][fixture.fixture_name] = normalized
            else:
                fixture_ratios[result.format_name][fixture.fixture_name] = None

    # Detailed table with per-fixture ratios (normalized)
    lines.append("### Token efficiency (normalized, JSON pretty = 1.0x)")
    lines.append("")

    # Find best (highest) ratio for each fixture and for avg
    best_per_fixture: dict[str, float] = {}
    for fixture_name in fixture_names:
        ratios = [fixture_ratios[fmt].get(fixture_name) for fmt in FORMATS]
        valid = [r for r in ratios if r is not None]
        best_per_fixture[fixture_name] = max(valid) if valid else 0

    # Best average (only for formats that work on all fixtures)
    all_avgs = []
    for fmt in FORMATS:
        stats = format_stats[fmt]
        if len(stats["ratios"]) == total_fixtures:
            # Recalculate normalized average
            fmt_ratios = [fixture_ratios[fmt].get(f) for f in fixture_names]
            valid = [r for r in fmt_ratios if r is not None]
            if valid:
                all_avgs.append(sum(valid) / len(valid))
    best_avg = max(all_avgs) if all_avgs else 0

    header = ["Format", *[SHORT_NAMES.get(f, f) for f in fixture_names], "avg"]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("|" + "|".join(["---"] * len(header)) + "|")

    for fmt in FORMATS:
        label = FORMAT_LABELS[fmt]
        row = [label]

        fmt_ratios_list = []
        for fixture_name in fixture_names:
            ratio = fixture_ratios[fmt].get(fixture_name)
            if ratio:
                fmt_ratios_list.append(ratio)
                val = f"{ratio:.1f}x"
                if ratio == best_per_fixture[fixture_name]:
                    val = f"**{val}**"
                row.append(val)
            else:
                row.append("✗")

        # Average
        if fmt_ratios_list:
            avg_ratio = sum(fmt_ratios_list) / len(fmt_ratios_list)
            val = f"{avg_ratio:.1f}x"
            if len(fmt_ratios_list) == total_fixtures and avg_ratio == best_avg:
                val = f"**{val}**"
            elif len(fmt_ratios_list) < total_fixtures:
                val = f"{val}\\*\\*"  # partial data marker
            row.append(val)
        else:
            row.append("N/A")

        lines.append("| " + " | ".join(row) + " |")

    lines.append("")
    lines.append("_Higher is better. ✗ = format cannot represent this data type. \\*\\* = average from partial data._")
    lines.append("")
    lines.append(
        "See [token visualization](benchmarks/results/benchmark_tokens.html) for detailed "
        "tokenization comparison across different tokenizers (gpt2, llama, qwen2.5, phi4)."
    )
    lines.append("")

    return "\n".join(lines)


def update_readme(content: str) -> None:
    """Update the README.md with benchmark results."""
    readme_text = README_PATH.read_text()

    pattern = r"<!-- BENCHMARK_START -->.*<!-- BENCHMARK_END -->"
    replacement = f"<!-- BENCHMARK_START -->\n{content}<!-- BENCHMARK_END -->"

    updated = re.sub(pattern, replacement, readme_text, flags=re.DOTALL)

    if updated == readme_text:
        print("Warning: README.md was not updated. Make sure BENCHMARK markers exist.")
    else:
        README_PATH.write_text(updated)
        print(f"Updated {README_PATH}")


def _hash_color(index: int) -> str:
    """Generate a pastel color based on index using golden ratio distribution."""
    # Use golden ratio to distribute hues evenly
    golden_ratio = 0.618033988749895
    hue = (index * golden_ratio) % 1.0
    # Convert HSL to RGB (pastel: high lightness, medium saturation)
    saturation = 0.5
    lightness = 0.85

    def hsl_to_rgb(h: float, s: float, li: float) -> tuple[int, int, int]:
        if s == 0:
            r = g = b = int(li * 255)
        else:

            def hue_to_rgb(p: float, q: float, t: float) -> float:
                if t < 0:
                    t += 1
                if t > 1:
                    t -= 1
                if t < 1 / 6:
                    return p + (q - p) * 6 * t
                if t < 1 / 2:
                    return q
                if t < 2 / 3:
                    return p + (q - p) * (2 / 3 - t) * 6
                return p

            q = li * (1 + s) if li < 0.5 else li + s - li * s
            p = 2 * li - q
            r = int(hue_to_rgb(p, q, h + 1 / 3) * 255)
            g = int(hue_to_rgb(p, q, h) * 255)
            b = int(hue_to_rgb(p, q, h - 1 / 3) * 255)
        return r, g, b

    r, g, b = hsl_to_rgb(hue, saturation, lightness)
    return f"#{r:02x}{g:02x}{b:02x}"


def generate_token_visualization_html(
    results: list[FixtureResult],
    fixtures: dict[str, list[dict]],
    tokenizer_names: list[str],
    tokenizers: dict[str, PreTrainedTokenizerBase],
) -> str:
    """Generate HTML with token visualization for all tokenizers with tabs."""
    # Pre-compute stats for summary table

    html = [
        "<!DOCTYPE html>",
        "<html><head>",
        "<meta charset='utf-8'>",
        "<title>Minemizer Token Visualization</title>",
        "<style>",
        "body { font-family: system-ui, sans-serif; margin: 0; padding: 20px; }",
        "h1, h2, h3 { color: #333; }",
        ".format { margin: 20px 0; }",
        ".format-header { font-weight: bold; margin-bottom: 8px; color: #555; }",
        ".tokens { font-family: monospace; font-size: 14px; line-height: 1.8; background: #f5f5f5; "
        "padding: 15px; border-radius: 4px; white-space: pre-wrap; word-break: break-all; }",
        ".token { display: inline; border: 1px solid #ccc; border-radius: 3px; padding: 1px 2px; margin: 1px; }",
        ".token-space { background: #ffe8e8 !important; border-color: #daa !important; }",
        ".token-newline { background: #f0e8ff !important; color: #999; border-color: #c8b8e8 !important; }",
        ".na { color: #999; font-style: italic; }",
        # Summary table styles
        "table { border-collapse: collapse; margin: 20px 0; }",
        "th, td { border: 1px solid #ddd; padding: 8px 12px; text-align: right; }",
        "th { background: #f0f0f0; font-weight: 600; }",
        "td:first-child, th:first-child { text-align: left; }",
        ".best { font-weight: bold; color: #228855; }",
        ".partial-best { font-weight: bold; }",
        ".summary-section { margin-bottom: 30px; }",
        # Layout: sidebar + main content
        ".page-layout { display: flex; gap: 20px; }",
        ".sidebar { position: sticky; top: 20px; align-self: flex-start; width: 120px; flex-shrink: 0; }",
        ".main-content { flex: 1; max-width: 1100px; }",
        # Sidebar tokenizer tabs (vertical)
        ".sidebar-label { font-weight: 600; color: #555; margin-bottom: 8px; font-size: 13px; }",
        ".sidebar-tabs { display: flex; flex-direction: column; gap: 4px; }",
        ".sidebar-tab { padding: 10px 14px; cursor: pointer; border: 1px solid #ddd; "
        "border-radius: 6px; background: #f5f5f5; transition: all 0.2s; user-select: none; "
        "text-align: center; font-size: 13px; }",
        ".sidebar-tab:hover { background: #e8e8e8; border-color: #ccc; }",
        ".sidebar-tab.active { background: #4a9eff; border-color: #4a9eff; color: white; font-weight: bold; }",
        # Fixture tabs (horizontal)
        ".tabs { display: flex; flex-wrap: wrap; gap: 0; margin-bottom: 0; border-bottom: 2px solid #ddd; }",
        ".tab { padding: 10px 20px; cursor: pointer; border: 1px solid transparent; border-bottom: none; "
        "border-radius: 8px 8px 0 0; background: #f5f5f5; margin-bottom: -2px; transition: all 0.2s; "
        "user-select: none; }",
        ".tab:hover { background: #e8e8e8; }",
        ".tab.active { background: white; border-color: #ddd; border-bottom-color: white; font-weight: bold; }",
        ".tab-content { display: none; }",
        ".tab-content.active { display: block; }",
        ".tab-group { margin-bottom: 20px; }",
        ".tab-group-label { font-weight: 600; color: #555; margin-bottom: 8px; font-size: 14px; }",
        ".fixture-info { color: #666; font-size: 14px; margin: 15px 0; padding: 10px; "
        "background: #f9f9f9; border-radius: 4px; }",
        # Comparison table in tab content
        ".comparison-table { font-size: 13px; margin: 15px 0 25px 0; }",
        ".comparison-table th, .comparison-table td { padding: 6px 10px; }",
        # Stats display styles
        ".stats { color: #666; font-size: 13px; display: block; margin-top: 4px; }",
        ".stat-item { display: inline-block; margin-right: 12px; padding: 3px 10px; "
        "border-radius: 4px; border: 1px solid; }",
        ".stat-label { font-size: 12px; }",
        ".stat-value { font-weight: 600; }",
        ".stat-chars { background: #e3f2fd; border-color: #90caf9; color: #1565c0; }",
        ".stat-tokens { background: #f3e5f5; border-color: #ce93d8; color: #7b1fa2; }",
        ".stat-og { background: #e8f5e9; border-color: #a5d6a7; color: #2e7d32; }",
        ".stat-enc { background: #fff3e0; border-color: #ffcc80; color: #e65100; }",
        # Copy button styles
        ".format-header-row { display: flex; align-items: center; gap: 10px; }",
        ".copy-btn { padding: 4px 10px; font-size: 12px; cursor: pointer; border: 1px solid #ccc; "
        "border-radius: 4px; background: #fff; color: #555; transition: all 0.2s; }",
        ".copy-btn:hover { background: #f0f0f0; border-color: #999; }",
        ".copy-btn.copied { background: #d4edda; border-color: #28a745; color: #28a745; }",
        "</style>",
        "</head><body>",
        "<h1>Token Visualization</h1>",
        "<p>Compare <a href='https://github.com/ashirviskas/minemizer'>minemizer</a> "
        "to other encoding formats for LLM in token efficiency. Each token is colored uniquely.</p>",
        "<div style='background: #f8f9fa; padding: 12px 16px; border-radius: 6px; margin: 16px 0; "
        "border-left: 4px solid #4a9eff;'>",
        "<strong>Metrics explained:</strong><br>",
        "<b>chars_og/tok</b> &mdash; Original JSON characters encoded per token "
        "(how much source original data fits per token after converting to <b>format</b>)<br>",
        "<b>encoded_chars/tok</b> &mdash; Encoded format characters per token "
        "(raw compression efficiency of the format itself)",
        "</div>",
    ]

    # Generate summary table (normalized to JSON pretty = 1.0x)
    html.append("<div class='summary-section'>")
    html.append("<h2>Token Efficiency Summary</h2>")
    html.append("<p><em>Normalized efficiency (JSON pretty = 1.0x, higher is better)</em></p>")
    html.append("<table>")

    # Header row
    header = ["Format"] + [SHORT_NAMES.get(f.fixture_name, f.fixture_name) for f in results] + ["avg"]
    html.append("<tr>" + "".join(f"<th>{h}</th>" for h in header) + "</tr>")

    # Compute JSON pretty baseline per fixture
    json_pretty_baseline: dict[str, float] = {}
    for fixture in results:
        json_pretty = next(r for r in fixture.results if r.format_name == "json_pretty")
        base_chars = json_pretty.chars
        assert base_chars is not None
        json_pretty_tokens = sum(v for v in json_pretty.tokens.values() if v is not None) / len(json_pretty.tokens)
        json_pretty_baseline[fixture.fixture_name] = base_chars / json_pretty_tokens

    # Compute normalized ratios per format per fixture
    best_per_fixture: dict[str, float] = {}
    format_avgs: dict[str, float] = {}
    format_ratios: dict[str, dict[str, float | None]] = {fmt: {} for fmt in FORMATS}

    for fixture in results:
        json_pretty = next(r for r in fixture.results if r.format_name == "json_pretty")
        base_chars = json_pretty.chars
        assert base_chars is not None
        baseline = json_pretty_baseline[fixture.fixture_name]

        best_ratio = 0.0
        for result in fixture.results:
            if result.chars is not None:
                avg_tokens = sum(v for v in result.tokens.values() if v is not None) / len(result.tokens)
                raw_ratio = base_chars / avg_tokens if avg_tokens > 0 else 0
                normalized = raw_ratio / baseline
                format_ratios[result.format_name][fixture.fixture_name] = normalized
                best_ratio = max(best_ratio, normalized)
            else:
                format_ratios[result.format_name][fixture.fixture_name] = None
        best_per_fixture[fixture.fixture_name] = best_ratio

    # Compute format averages and track completeness
    total_fixtures = len(results)
    format_complete: dict[str, bool] = {}

    for fmt in FORMATS:
        ratios = [format_ratios[fmt].get(f.fixture_name) for f in results]
        valid = [r for r in ratios if r is not None]
        if valid:
            format_avgs[fmt] = sum(valid) / len(valid)
            format_complete[fmt] = len(valid) == total_fixtures

    # Best among complete formats (bold + green)
    complete_avgs = [format_avgs[f] for f in format_avgs if format_complete.get(f)]
    best_avg_complete = max(complete_avgs) if complete_avgs else 0

    # Best overall including partial (for bold-only on partial)
    best_avg_overall = max(format_avgs.values()) if format_avgs else 0

    # Data rows
    for fmt in FORMATS:
        label = FORMAT_LABELS[fmt]
        row = [f"<td>{label}</td>"]

        for fixture in results:
            ratio = format_ratios[fmt].get(fixture.fixture_name)

            if ratio is None:
                row.append("<td class='na'>✗</td>")
            else:
                css_class = " class='best'" if ratio == best_per_fixture[fixture.fixture_name] else ""
                row.append(f"<td{css_class}>{ratio:.1f}x</td>")

        # Average column
        if fmt in format_avgs:
            avg = format_avgs[fmt]
            is_complete = format_complete.get(fmt, False)
            if is_complete and avg == best_avg_complete:
                css_class = " class='best'"  # bold + green
            elif not is_complete and avg == best_avg_overall:
                css_class = " class='partial-best'"  # bold only
            else:
                css_class = ""
            row.append(f"<td{css_class}>{avg:.1f}x</td>")
        else:
            row.append("<td class='na'>N/A</td>")

        html.append("<tr>" + "".join(row) + "</tr>")

    html.append("</table>")
    html.append("</div>")

    # Second table: Tokenizer vs Format (averaged across all fixtures)
    html.append("<div class='summary-section'>")
    html.append("<h2>Tokenizer × Format</h2>")
    html.append("<p><em>Average efficiency per tokenizer (normalized, higher is better)</em></p>")
    html.append("<table>")

    # Header row: Format | tokenizer1 | tokenizer2 | ... | avg
    header = ["Format"] + list(tokenizer_names) + ["avg"]
    html.append("<tr>" + "".join(f"<th>{h}</th>" for h in header) + "</tr>")

    # First pass: compute all values and track completeness
    table_data: dict[str, dict[str, float | None]] = {}
    format_tok_complete: dict[str, dict[str, bool]] = {}  # Track if format+tokenizer ran on all fixtures
    for fmt in FORMATS:
        table_data[fmt] = {}
        format_tok_complete[fmt] = {}
        for tok_name in tokenizer_names:
            ratios = []
            for fixture in results:
                json_pretty = next(r for r in fixture.results if r.format_name == "json_pretty")
                base_chars = json_pretty.chars
                assert base_chars is not None
                jp_tokens = json_pretty.tokens.get(tok_name)
                if jp_tokens is None:
                    continue
                baseline = base_chars / jp_tokens

                result = next(r for r in fixture.results if r.format_name == fmt)
                if result.chars is not None:
                    tok_count = result.tokens.get(tok_name)
                    if tok_count:
                        raw_ratio = base_chars / tok_count
                        normalized = raw_ratio / baseline
                        ratios.append(normalized)

            table_data[fmt][tok_name] = sum(ratios) / len(ratios) if ratios else None
            format_tok_complete[fmt][tok_name] = len(ratios) == total_fixtures

        # Compute row average
        valid_vals = [v for v in table_data[fmt].values() if v is not None]
        table_data[fmt]["avg"] = sum(valid_vals) / len(valid_vals) if valid_vals else None
        # avg is complete only if all tokenizers are complete
        format_tok_complete[fmt]["avg"] = all(format_tok_complete[fmt].get(tok, False) for tok in tokenizer_names)

    # Find max/min per column for coloring (only from complete formats)
    all_cols = list(tokenizer_names) + ["avg"]
    col_max: dict[str, float] = {}
    col_min: dict[str, float] = {}
    for col in all_cols:
        col_vals = [
            v
            for fmt in FORMATS
            if format_tok_complete[fmt].get(col, False) and (v := table_data[fmt].get(col)) is not None
        ]
        if col_vals:
            col_max[col] = max(col_vals)
            col_min[col] = min(col_vals)

    def value_to_color(val: float, col: str) -> str:
        """Generate color from red (low) to green (high) within column range."""
        col_min_val = col_min.get(col, val)
        col_max_val = col_max.get(col, val)
        ratio = 0.5 if col_max_val == col_min_val else (val - col_min_val) / (col_max_val - col_min_val)
        # Interpolate from light red to light green
        r = int(255 - ratio * 80)
        g = int(200 + ratio * 55)
        b = int(200 - ratio * 50)
        return f"#{r:02x}{g:02x}{b:02x}"

    # Generate rows
    for fmt in FORMATS:
        label = FORMAT_LABELS[fmt]
        row = [f"<td>{label}</td>"]

        for col in all_cols:
            val = table_data[fmt].get(col)
            is_complete = format_tok_complete[fmt].get(col, False)

            if val is None:
                row.append("<td class='na'>✗</td>")
            elif not is_complete:
                # Grey background for incomplete formats (didn't run on all fixtures)
                row.append(f"<td style='background:#e0e0e0;'>{val:.1f}x</td>")
            else:
                bg_color = value_to_color(val, col)
                is_max = val == col_max.get(col)
                style = f"background:{bg_color};"
                if is_max:
                    style += " font-weight:bold;"
                row.append(f"<td style='{style}'>{val:.1f}x</td>")

        html.append("<tr>" + "".join(row) + "</tr>")

    html.append("</table>")
    html.append("</div>")

    # Comparisons section header
    html.append("<div class='summary-section'>")
    html.append("<h2>Comparisons</h2>")
    html.append("<p><em>Select a tokenizer and example to compare all formats</em></p>")
    html.append("</div>")

    # Start page layout with sidebar
    html.append("<div class='page-layout'>")

    # Sidebar with tokenizer tabs (sticky)
    html.append("<div class='sidebar'>")
    html.append("<div class='sidebar-label'>Tokenizer</div>")
    html.append("<div class='sidebar-tabs' id='tokenizer-tabs'>")
    for i, tok_name in enumerate(tokenizer_names):
        active = " active" if i == 0 else ""
        html.append(f"  <div class='sidebar-tab{active}' data-tokenizer='{tok_name}'>{tok_name}</div>")
    html.append("</div>")
    html.append("</div>")

    # Main content area
    html.append("<div class='main-content'>")

    # Fixture tabs (horizontal, in main content)
    html.append("<div class='tab-group'>")
    html.append("<div class='tab-group-label'>Example:</div>")
    html.append("<div class='tabs' id='fixture-tabs'>")
    for i, fixture in enumerate(results):
        active = " active" if i == 0 else ""
        display_name = SHORT_NAMES.get(fixture.fixture_name, fixture.fixture_name)
        html.append(f"  <div class='tab{active}' data-fixture='{fixture.fixture_name}'>{display_name}</div>")
    html.append("</div>")
    html.append("</div>")

    # Generate content for each tokenizer + fixture combination
    for i, tok_name in enumerate(tokenizer_names):
        tokenizer = tokenizers[tok_name]

        for j, fixture in enumerate(results):
            data = fixtures[fixture.fixture_name]
            json_pretty_result = next(r for r in fixture.results if r.format_name == "json_pretty")
            base_chars = json_pretty_result.chars
            assert base_chars is not None  # JSON always succeeds

            active = " active" if i == 0 and j == 0 else ""
            content_id = f"content-{tok_name}-{fixture.fixture_name}"
            html.append(
                f"<div class='tab-content{active}' id='{content_id}' "
                f"data-tokenizer='{tok_name}' data-fixture='{fixture.fixture_name}'>"
            )

            html.append("<div class='fixture-info'>")
            html.append(
                f"<strong>{fixture.fixture_name}.json</strong> &mdash; "
                f"Original size: {base_chars} chars &mdash; "
                f"Tokenizer: {tok_name} ({TOKENIZERS[tok_name]})"
            )
            html.append("</div>")

            # Comparison table for all formats
            html.append("<table class='comparison-table'>")
            html.append(
                "<tr><th>Format</th><th>Chars</th><th>Tokens</th><th>chars_og/tok</th><th>encoded_chars/tok</th></tr>"
            )
            for fmt in FORMATS:
                label = FORMAT_LABELS[fmt]
                result = next(r for r in fixture.results if r.format_name == fmt)
                if result.chars is None:
                    html.append(f"<tr><td>{label}</td><td colspan='4' class='na'>N/A</td></tr>")
                else:
                    tok_count = result.tokens[tok_name] or 0
                    chars_count = result.chars
                    og_per_tok = base_chars / tok_count if tok_count else 0
                    enc_per_tok = chars_count / tok_count if tok_count else 0
                    html.append(
                        f"<tr><td>{label}</td><td>{fmt_num(chars_count)}</td>"
                        f"<td>{fmt_num(tok_count)}</td><td>{og_per_tok:.1f}</td>"
                        f"<td>{enc_per_tok:.1f}</td></tr>"
                    )
            html.append("</table>")

            for fmt in FORMATS:
                label = FORMAT_LABELS[fmt]
                result = next(r for r in fixture.results if r.format_name == fmt)
                output = convert_to_format(data, fmt)

                html.append("<div class='format'>")

                if output is None:
                    html.append(f"<div class='format-header'>{label}: <span class='na'>N/A</span></div>")
                else:
                    token_count = result.tokens[tok_name] or 0
                    chars_count = result.chars or 0
                    chars_og_per_tok = base_chars / token_count if token_count else 0
                    encoded_per_tok = chars_count / token_count if token_count else 0
                    # Unique ID for copy functionality
                    copy_id = f"copy-{tok_name}-{fixture.fixture_name}-{fmt}"
                    html.append(
                        f"<div class='format-header-row'>"
                        f"<span class='format-header'>{label}</span>"
                        f"<button class='copy-btn' onclick='copyText(\"{copy_id}\")'>Copy</button>"
                        f"</div>"
                    )
                    # Hidden textarea with full output for copying
                    escaped_output = output.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    html.append(f"<textarea id='{copy_id}' style='display:none'>{escaped_output}</textarea>")
                    html.append(
                        f"<div class='stats'>"
                        f"<span class='stat-item stat-chars'><span class='stat-label'>chars:</span> "
                        f"<span class='stat-value'>{fmt_num(chars_count)}</span></span>"
                        f"<span class='stat-item stat-tokens'><span class='stat-label'>tokens:</span> "
                        f"<span class='stat-value'>{fmt_num(token_count)}</span></span>"
                        f"<span class='stat-item stat-og'><span class='stat-label'>chars_og/tok:</span> "
                        f"<span class='stat-value'>{chars_og_per_tok:.1f}</span></span>"
                        f"<span class='stat-item stat-enc'><span class='stat-label'>encoded_chars/tok:</span> "
                        f"<span class='stat-value'>{encoded_per_tok:.1f}</span></span>"
                        f"</div>"
                    )

                    # Tokenize and visualize (truncate by lines first, then chars)
                    display_output = output
                    truncated = False
                    lines_list = output.split("\n")
                    if len(lines_list) > MAX_EXAMPLE_LINES:
                        display_output = "\n".join(lines_list[:MAX_EXAMPLE_LINES])
                        truncated = True
                    elif len(output) > MAX_EXAMPLE_CHARS:
                        display_output = output[:MAX_EXAMPLE_CHARS]
                        truncated = True

                    token_ids = tokenizer.encode(display_output)
                    tokens = [tokenizer.decode([tid]) for tid in token_ids]

                    html.append("<div class='tokens'>")
                    token_spans = []
                    for idx, token in enumerate(tokens):
                        color = _hash_color(idx)
                        escaped = (
                            token.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
                        )
                        if "\n" in token:
                            visible = escaped.replace("\n", "↵")
                            token_spans.append(f"<span class='token token-newline'>{visible}</span><br>")
                        elif token.strip() == "" and token:
                            visible = escaped.replace(" ", "·").replace("\t", "→")
                            token_spans.append(f"<span class='token token-space'>{visible}</span>")
                        else:
                            token_spans.append(f"<span class='token' style='background:{color}'>{escaped}</span>")
                    if truncated:
                        token_spans.append("<br><em>... (truncated)</em>")
                    html.append("".join(token_spans))
                    html.append("</div>")

                html.append("</div>")

            html.append("</div>")  # end tab-content

    html.append("</div>")  # end main-content
    html.append("</div>")  # end page-layout

    # JavaScript for dual tab switching and copy functionality
    html.append(
        """
<script>
let currentTokenizer = '"""
        + tokenizer_names[0]
        + """';
let currentFixture = '"""
        + results[0].fixture_name
        + """';

function updateContent() {
  // Hide all content
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
  // Show selected combination
  const id = 'content-' + currentTokenizer + '-' + currentFixture;
  const el = document.getElementById(id);
  if (el) el.classList.add('active');
}

function copyText(id) {
  const textarea = document.getElementById(id);
  if (!textarea) return;

  navigator.clipboard.writeText(textarea.value).then(() => {
    // Find the button that triggered this
    const btn = document.querySelector(`button[onclick="copyText('${id}')"]`);
    if (btn) {
      btn.textContent = 'Copied!';
      btn.classList.add('copied');
      setTimeout(() => {
        btn.textContent = 'Copy';
        btn.classList.remove('copied');
      }, 2000);
    }
  }).catch(err => {
    console.error('Failed to copy:', err);
  });
}

document.querySelectorAll('#tokenizer-tabs .sidebar-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('#tokenizer-tabs .sidebar-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    currentTokenizer = tab.dataset.tokenizer;
    updateContent();
  });
});

document.querySelectorAll('#fixture-tabs .tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('#fixture-tabs .tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    currentFixture = tab.dataset.fixture;
    updateContent();
  });
});
</script>
"""
    )

    html.append("</body></html>")
    return "\n".join(html)


def save_raw_results(
    results: list[FixtureResult],
    tokenizer_names: list[str],
    fixtures: dict[str, list[dict]],
    tokenizers: dict[str, PreTrainedTokenizerBase],
) -> None:
    """Save raw benchmark results to JSON and detailed markdown."""
    results_dir = BENCHMARKS_DIR / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    # Convert to serializable format
    raw_data = {
        "date": date.today().isoformat(),
        "fixtures": {},
    }

    for fixture in results:
        raw_data["fixtures"][fixture.fixture_name] = {
            result.format_name: {
                "chars": result.chars,
                "tokens": result.tokens,
            }
            for result in fixture.results
        }

    # Save JSON
    json_path = results_dir / "benchmark_results.json"
    json_path.write_text(json.dumps(raw_data, indent=2) + "\n")
    print(f"Saved raw results to {json_path}")

    # Generate detailed markdown
    md_lines = [
        "# Benchmark Results (Full Detail)",
        "",
        f"_Generated: {date.today().isoformat()}_",
        "",
        f"Tokenizers: {', '.join(tokenizer_names)}",
        "",
    ]

    # Format to file extension mapping
    format_ext = {
        "json_pretty": "json",
        "json_min": "json",
        "csv": "csv",
        "tsv": "tsv",
        "yaml": "yaml",
        "toon": "toon",
        "tson": "tson",
        "minemizer": "txt",
        "minemizer_compact": "txt",
        "minemizer_33": "txt",
        "minemizer_75": "txt",
        "minemizer_compact_33": "txt",
        "minemizer_compact_75": "txt",
    }

    for fixture in results:
        data = fixtures[fixture.fixture_name]

        # Get base chars
        json_pretty = next(r for r in fixture.results if r.format_name == "json_pretty")
        base_chars = json_pretty.chars
        assert base_chars is not None  # JSON always succeeds

        md_lines.append(f"## {fixture.fixture_name}.json")
        md_lines.append("")
        md_lines.append(f"Original size (JSON pretty): **{base_chars} chars**")
        md_lines.append("")

        # Table header
        header = ["Format", "Chars", *tokenizer_names, "Avg Tokens", "Orig/Token"]
        md_lines.append("| " + " | ".join(header) + " |")
        md_lines.append("|" + "|".join(["---"] * len(header)) + "|")

        for result in fixture.results:
            label = FORMAT_LABELS[result.format_name]

            if result.chars is None:
                row = [label, "N/A", *["N/A"] * len(tokenizer_names), "N/A", "N/A"]
            else:
                row = [label, str(result.chars)]
                token_values = []
                for tok_name in tokenizer_names:
                    tok_count = result.tokens.get(tok_name)
                    row.append(str(tok_count) if tok_count else "N/A")
                    if tok_count:
                        token_values.append(tok_count)

                if token_values:
                    avg_tokens = sum(token_values) / len(token_values)
                    ratio = base_chars / avg_tokens
                    row.append(f"{avg_tokens:.1f}")
                    row.append(f"{ratio:.1f}")
                else:
                    row.extend(["N/A", "N/A"])

            md_lines.append("| " + " | ".join(row) + " |")

        md_lines.append("")

        # Show full output for each format
        md_lines.append("### Serialized outputs")
        md_lines.append("")

        for fmt in FORMATS:
            label = FORMAT_LABELS[fmt]
            result = next(r for r in fixture.results if r.format_name == fmt)
            output = convert_to_format(data, fmt)
            ext = format_ext[fmt]

            if output is None:
                md_lines.append(f"**{label}:** N/A")
                md_lines.append("```")
                md_lines.append("N/A - format cannot represent this data")
                md_lines.append("```")
            else:
                avg_tokens = sum(v for v in result.tokens.values() if v is not None) / len(result.tokens)
                md_lines.append(f"**{label}** ({result.chars} chars, {avg_tokens:.0f} tokens):")
                md_lines.append(f"```{ext}")
                display_output = output.rstrip()
                # Truncate by lines first, then by characters
                lines_list = display_output.split("\n")
                if len(lines_list) > MAX_EXAMPLE_LINES:
                    display_output = "\n".join(lines_list[:MAX_EXAMPLE_LINES]) + "\n... (truncated)"
                elif len(display_output) > MAX_EXAMPLE_CHARS:
                    display_output = display_output[:MAX_EXAMPLE_CHARS] + "\n... (truncated)"
                md_lines.append(display_output)
                md_lines.append("```")
            md_lines.append("")

        md_lines.append("---")
        md_lines.append("")

    # Save markdown
    md_path = results_dir / "benchmark_results.md"
    md_path.write_text("\n".join(md_lines))
    print(f"Saved detailed results to {md_path}")

    # Generate HTML with token visualization
    html_path = results_dir / "benchmark_tokens.html"
    html_content = generate_token_visualization_html(results, fixtures, tokenizer_names, tokenizers)
    html_path.write_text(html_content)
    print(f"Saved token visualization to {html_path}")


def main() -> None:
    """Run benchmarks and update README."""
    overall_start = time.perf_counter()

    print("=" * 60)
    print("Minemizer Benchmarks")
    print("=" * 60)
    print()

    # Load tokenizers
    tokenizers, load_time = load_tokenizers()
    tokenizer_names = list(tokenizers.keys())

    # Load fixtures
    fixtures = load_fixtures()
    print(f"Loaded {len(fixtures)} fixture files\n")

    # Run benchmarks
    print("Running benchmarks...")
    results, timing_stats = run_benchmarks(fixtures, tokenizers)
    print()

    # Generate markdown
    markdown = generate_markdown_table(results, tokenizer_names)

    # Print to console
    print("Results:")
    print("-" * 60)
    print(markdown)
    print("-" * 60)

    # Update README
    update_readme(markdown)

    # Save raw results
    save_raw_results(results, tokenizer_names, fixtures, tokenizers)

    # Print timing summary
    overall_time = time.perf_counter() - overall_start
    print()
    print("=" * 60)
    print("Timing Summary")
    print("=" * 60)
    print(f"  Tokenizer loading:  {load_time:>6.2f}s")
    print(f"  Format conversion:  {timing_stats['conversion']:>6.2f}s")
    print(f"  Tokenization:       {timing_stats['tokenization']:>6.2f}s")
    print(f"  Benchmark total:    {timing_stats['total']:>6.2f}s")
    print(f"  Overall total:      {overall_time:>6.2f}s")
    print("=" * 60)


if __name__ == "__main__":
    main()
