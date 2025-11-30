#!/usr/bin/env python3
"""Benchmark minemizer against other serialization formats."""

from __future__ import annotations

import csv
import io
import json
import re
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
TOKENIZERS: dict[str, str] = {
    "gpt2": "openai-community/gpt2",
    "llama": "NousResearch/Llama-2-7b-hf",
    "qwen2.5": "Qwen/Qwen2.5-0.5B",
    "phi4": "microsoft/phi-4",
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
    "minemizer_compact": "minemizer (compact)",
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


def load_tokenizers() -> dict[str, PreTrainedTokenizerBase]:
    """Load all tokenizers from HuggingFace."""
    print("Loading tokenizers...")
    tokenizers = {}
    for name, model_id in TOKENIZERS.items():
        print(f"  Loading {name} ({model_id})...")
        tokenizers[name] = AutoTokenizer.from_pretrained(model_id)
    print()
    return tokenizers


def load_fixtures() -> dict[str, list[dict]]:
    """Load all fixture JSON files."""
    fixtures = {}
    for path in sorted(FIXTURES_DIR.glob("*.json")):
        with path.open() as f:
            fixtures[path.stem] = json.load(f)
    return fixtures


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

        case _:
            raise ValueError(f"Unknown format: {format_name}")


def count_tokens(text: str, tokenizer: PreTrainedTokenizerBase) -> int:
    """Count tokens in text using the given tokenizer."""
    return len(tokenizer.encode(text))


def run_benchmarks(
    fixtures: dict[str, list[dict]],
    tokenizers: dict[str, PreTrainedTokenizerBase],
) -> list[FixtureResult]:
    """Run all benchmarks."""
    results = []

    for fixture_name, data in fixtures.items():
        print(f"Benchmarking {fixture_name}...")
        fixture_results = []

        for format_name in FORMATS:
            converted = convert_to_format(data, format_name)

            if converted is None:
                # Format doesn't support this data structure
                result = BenchmarkResult(
                    format_name=format_name,
                    chars=None,
                    tokens=dict.fromkeys(tokenizers),
                )
            else:
                tokens: dict[str, int | None] = {name: count_tokens(converted, tok) for name, tok in tokenizers.items()}
                result = BenchmarkResult(
                    format_name=format_name,
                    chars=len(converted),
                    tokens=tokens,
                )

            fixture_results.append(result)

        results.append(FixtureResult(fixture_name=fixture_name, results=fixture_results))

    return results


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

    # Build per-fixture ratios for detailed table
    fixture_ratios: dict[str, dict[str, float | None]] = {fmt: {} for fmt in FORMATS}
    for fixture in results:
        json_pretty_result = next(r for r in fixture.results if r.format_name == "json_pretty")
        base_chars = json_pretty_result.chars
        assert base_chars is not None  # JSON always succeeds
        for result in fixture.results:
            if result.chars is not None:
                avg_tokens = sum(v for v in result.tokens.values() if v is not None) / len(result.tokens)
                fixture_ratios[result.format_name][fixture.fixture_name] = base_chars / avg_tokens
            else:
                fixture_ratios[result.format_name][fixture.fixture_name] = None

    # Detailed table with per-fixture ratios
    lines.append("### Token efficiency (original chars encoded per token)")
    lines.append("")

    # Header with fixture names (shortened)
    short_names = {
        "simple_flat": "flat",
        "nested_objects": "nested",
        "lists_of_primitives": "lists",
        "sparse_data": "sparse",
        "complex_mixed": "complex",
    }

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
            all_avgs.append(sum(stats["ratios"]) / len(stats["ratios"]))
    best_avg = max(all_avgs) if all_avgs else 0

    header = ["Format", *[short_names.get(f, f) for f in fixture_names], "avg"]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("|" + "|".join(["---"] * len(header)) + "|")

    for fmt in FORMATS:
        label = FORMAT_LABELS[fmt]
        stats = format_stats[fmt]
        row = [label]

        for fixture_name in fixture_names:
            ratio = fixture_ratios[fmt].get(fixture_name)
            if ratio:
                val = f"{ratio:.1f}"
                if ratio == best_per_fixture[fixture_name]:
                    val = f"**{val}**"
                row.append(val)
            else:
                row.append("✗")

        # Average
        if stats["ratios"]:
            avg_ratio = sum(stats["ratios"]) / len(stats["ratios"])
            val = f"{avg_ratio:.1f}"
            if len(stats["ratios"]) == total_fixtures and avg_ratio == best_avg:
                val = f"**{val}**"
            elif len(stats["ratios"]) < total_fixtures:
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
        "body { font-family: system-ui, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }",
        "h1, h2, h3 { color: #333; }",
        ".format { margin: 20px 0; }",
        ".format-header { font-weight: bold; margin-bottom: 8px; color: #555; }",
        ".tokens { font-family: monospace; font-size: 14px; line-height: 1.8; background: #f5f5f5; "
        "padding: 15px; border-radius: 4px; white-space: pre-wrap; word-break: break-all; }",
        ".token { display: inline; border: 1px solid #ccc; border-radius: 3px; padding: 1px 2px; margin: 1px; }",
        ".token-space { background: #ffe8e8 !important; border-color: #daa !important; }",
        ".token-newline { background: #f0e8ff !important; color: #999; border-color: #c8b8e8 !important; }",
        ".stats { color: #666; font-size: 14px; }",
        ".na { color: #999; font-style: italic; }",
        # Summary table styles
        "table { border-collapse: collapse; margin: 20px 0; }",
        "th, td { border: 1px solid #ddd; padding: 8px 12px; text-align: right; }",
        "th { background: #f0f0f0; font-weight: 600; }",
        "td:first-child, th:first-child { text-align: left; }",
        ".best { font-weight: bold; color: #228855; }",
        ".partial-best { font-weight: bold; }",
        ".summary-section { margin-bottom: 30px; }",
        # Tab styles
        ".tabs { display: flex; flex-wrap: wrap; gap: 0; margin-bottom: 0; border-bottom: 2px solid #ddd; }",
        ".tab { padding: 10px 20px; cursor: pointer; border: 1px solid transparent; border-bottom: none; "
        "border-radius: 8px 8px 0 0; background: #f5f5f5; margin-bottom: -2px; transition: all 0.2s; "
        "user-select: none; }",
        ".tab:hover { background: #e8e8e8; }",
        ".tab.active { background: white; border-color: #ddd; border-bottom-color: white; font-weight: bold; }",
        ".tab-content { display: none; }",
        ".tab-content.active { display: block; }",
        ".tab-group { margin-bottom: 30px; }",
        ".tab-group-label { font-weight: 600; color: #555; margin-bottom: 8px; font-size: 14px; }",
        ".fixture-info { color: #666; font-size: 14px; margin: 15px 0; padding: 10px; "
        "background: #f9f9f9; border-radius: 4px; }",
        "</style>",
        "</head><body>",
        "<h1>Token Visualization</h1>",
        "<p>Compare <a href='https://github.com/ashirviskas/minemizer'>minemizer</a> "
        "to other methods of encoding various data for LLMs. Each token is colored uniquely.</p>",
    ]

    # Generate summary table (like markdown version)
    html.append("<div class='summary-section'>")
    html.append("<h2>Token Efficiency Summary</h2>")
    html.append("<p><em>Original characters encoded per token on average (higher is better)</em></p>")
    html.append("<table>")

    # Header row
    header = ["Format"] + [f.fixture_name.replace("_", " ") for f in results] + ["avg"]
    html.append("<tr>" + "".join(f"<th>{h}</th>" for h in header) + "</tr>")

    # Compute best values per column
    best_per_fixture: dict[str, float] = {}
    format_avgs: dict[str, float] = {}

    for fixture in results:
        json_pretty = next(r for r in fixture.results if r.format_name == "json_pretty")
        base_chars = json_pretty.chars
        assert base_chars is not None  # JSON always succeeds
        best_ratio = 0.0
        for result in fixture.results:
            if result.chars is not None:
                avg_tokens = sum(v for v in result.tokens.values() if v is not None) / len(result.tokens)
                ratio = base_chars / avg_tokens if avg_tokens > 0 else 0
                best_ratio = max(best_ratio, ratio)
        best_per_fixture[fixture.fixture_name] = best_ratio

    # Compute format averages and track completeness
    total_fixtures = len(results)
    format_complete: dict[str, bool] = {}

    for fmt in FORMATS:
        ratios = []
        for fixture in results:
            json_pretty = next(r for r in fixture.results if r.format_name == "json_pretty")
            base_chars = json_pretty.chars
            assert base_chars is not None  # JSON always succeeds
            result = next(r for r in fixture.results if r.format_name == fmt)
            if result.chars is not None:
                avg_tokens = sum(v for v in result.tokens.values() if v is not None) / len(result.tokens)
                ratios.append(base_chars / avg_tokens if avg_tokens > 0 else 0)
        if ratios:
            format_avgs[fmt] = sum(ratios) / len(ratios)
            format_complete[fmt] = len(ratios) == total_fixtures

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
            json_pretty = next(r for r in fixture.results if r.format_name == "json_pretty")
            base_chars = json_pretty.chars
            assert base_chars is not None  # JSON always succeeds
            result = next(r for r in fixture.results if r.format_name == fmt)

            if result.chars is None:
                row.append("<td class='na'>✗</td>")
            else:
                avg_tokens = sum(v for v in result.tokens.values() if v is not None) / len(result.tokens)
                ratio = base_chars / avg_tokens if avg_tokens > 0 else 0
                css_class = " class='best'" if ratio == best_per_fixture[fixture.fixture_name] else ""
                row.append(f"<td{css_class}>{ratio:.1f}</td>")

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
            row.append(f"<td{css_class}>{avg:.1f}</td>")
        else:
            row.append("<td class='na'>N/A</td>")

        html.append("<tr>" + "".join(row) + "</tr>")

    html.append("</table>")
    html.append("</div>")

    # Tokenizer tabs
    html.append("<div class='tab-group'>")
    html.append("<div class='tab-group-label'>Tokenizer:</div>")
    html.append("<div class='tabs' id='tokenizer-tabs'>")
    for i, tok_name in enumerate(tokenizer_names):
        active = " active" if i == 0 else ""
        html.append(f"  <div class='tab{active}' data-tokenizer='{tok_name}'>{tok_name}</div>")
    html.append("</div>")
    html.append("</div>")

    # Fixture tabs
    html.append("<div class='tab-group'>")
    html.append("<div class='tab-group-label'>Example:</div>")
    html.append("<div class='tabs' id='fixture-tabs'>")
    for i, fixture in enumerate(results):
        active = " active" if i == 0 else ""
        display_name = fixture.fixture_name.replace("_", " ")
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

            for fmt in FORMATS:
                label = FORMAT_LABELS[fmt]
                result = next(r for r in fixture.results if r.format_name == fmt)
                output = convert_to_format(data, fmt)

                html.append("<div class='format'>")

                if output is None:
                    html.append(f"<div class='format-header'>{label}: <span class='na'>N/A</span></div>")
                else:
                    token_count = result.tokens[tok_name]
                    ratio = base_chars / token_count if token_count else 0
                    html.append(
                        f"<div class='format-header'>{label} "
                        f"<span class='stats'>({result.chars} chars, {token_count} tokens, "
                        f"{ratio:.1f} orig/tok)</span></div>"
                    )

                    # Tokenize and visualize
                    token_ids = tokenizer.encode(output)
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
                    html.append("".join(token_spans))
                    html.append("</div>")

                html.append("</div>")

            html.append("</div>")  # end tab-content

    # JavaScript for dual tab switching
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

document.querySelectorAll('#tokenizer-tabs .tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('#tokenizer-tabs .tab').forEach(t => t.classList.remove('active'));
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
                    row.append(f"{ratio:.2f}")
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
                md_lines.append(output.rstrip())
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
    print("=" * 60)
    print("Minemizer Benchmarks")
    print("=" * 60)
    print()

    # Load tokenizers
    tokenizers = load_tokenizers()
    tokenizer_names = list(tokenizers.keys())

    # Load fixtures
    fixtures = load_fixtures()
    print(f"Loaded {len(fixtures)} fixture files\n")

    # Run benchmarks
    results = run_benchmarks(fixtures, tokenizers)
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


if __name__ == "__main__":
    main()
