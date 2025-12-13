"""HTML output generation for token visualization."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from benchmarks.config import (
    FORMAT_LABELS,
    FORMATS,
    MAX_COPY_CHARS,
    MAX_EXAMPLE_CHARS,
    MAX_EXAMPLE_LINES,
    SHORT_NAMES,
    TOKENIZERS,
)
from benchmarks.core.formats import convert_to_format


def _gradient_colors(ratio: float) -> tuple[str, str]:
    """Generate light and dark mode gradient colors for a ratio (0=bad, 1=good)."""
    lr, lg, lb = int(255 - ratio * 80), int(200 + ratio * 55), int(200 - ratio * 50)
    dr, dg, db = int(180 - ratio * 140), int(60 + ratio * 120), int(60 - ratio * 20)
    return f"#{lr:02x}{lg:02x}{lb:02x}", f"#{dr:02x}{dg:02x}{db:02x}"


def _gradient_cell(ratio: float, content: str, extra_cls: str = "", extra_style: str = "") -> str:
    """Generate a td with gradient colors."""
    light, dark = _gradient_colors(ratio)
    cls = f"gradient-cell {extra_cls}".strip()
    style = f"background-color:{light};{extra_style}"
    return f"<td class='{cls}' style='{style}' data-light='{light}' data-dark='{dark}'>{content}</td>"


if TYPE_CHECKING:
    from transformers import PreTrainedTokenizerBase

    from benchmarks.runners.compression import BenchmarkResults


def generate_html(
    results: BenchmarkResults,
    fixtures: dict[str, list[dict]],
    tokenizers: dict[str, PreTrainedTokenizerBase],
) -> str:
    """Generate HTML with token visualization."""
    tokenizer_names = list(tokenizers.keys())

    # Pre-compute all data for JS rendering
    data_blob = _build_data_blob(results, fixtures, tokenizers, tokenizer_names)

    html = [
        _html_head(),
        _html_intro(),
        _summary_table(results, tokenizer_names),
        _tokenizer_format_table(results, tokenizer_names),
        _comparison_section(results, tokenizer_names),
        f"<script>const BENCHMARK_DATA = {json.dumps(data_blob, separators=(',', ':'))};</script>",
        _html_script(tokenizer_names, results.fixtures[0].fixture_name),
        "</body></html>",
    ]

    return "\n".join(html)


def _build_data_blob(
    results: BenchmarkResults,
    fixtures: dict[str, list[dict]],
    tokenizers: dict[str, PreTrainedTokenizerBase],
    tokenizer_names: list[str],
) -> dict:
    """Build the data blob for JS rendering."""
    # Format outputs: fixture -> format -> {output, truncated, copyOutput} or None
    format_outputs: dict[str, dict[str, dict | None]] = {}

    # Token data: tokenizer -> fixture -> format -> [token strings] or None
    token_data: dict[str, dict[str, dict[str, list[str] | None]]] = {t: {} for t in tokenizer_names}

    # Stats: fixture -> format -> {chars, tokens: {tokenizer: count}} or None
    stats: dict[str, dict[str, dict | None]] = {}

    # Base chars for each fixture (JSON pretty chars)
    base_chars: dict[str, int] = {}

    for fixture in results.fixtures:
        fixture_name = fixture.fixture_name
        data = fixtures[fixture_name]

        format_outputs[fixture_name] = {}
        stats[fixture_name] = {}

        # Get base chars from JSON pretty
        json_result = next(r for r in fixture.results if r.format_name == "json_pretty")
        base_chars[fixture_name] = json_result.chars or 0

        for tok_name in tokenizer_names:
            token_data[tok_name][fixture_name] = {}

        for fmt in FORMATS:
            result = next(r for r in fixture.results if r.format_name == fmt)
            output = convert_to_format(data, fmt)

            if output is None:
                format_outputs[fixture_name][fmt] = None
                stats[fixture_name][fmt] = None
                for tok_name in tokenizer_names:
                    token_data[tok_name][fixture_name][fmt] = None
                continue

            # Truncate for display
            display_output, truncated = _truncate_output(output)

            # Truncate for copy (larger limit)
            copy_output = output[:MAX_COPY_CHARS] if len(output) > MAX_COPY_CHARS else output
            copy_truncated = len(output) > MAX_COPY_CHARS

            format_outputs[fixture_name][fmt] = {
                "display": display_output,
                "copy": copy_output,
                "truncated": truncated,
                "copyTruncated": copy_truncated,
                "fullChars": len(output),
            }

            # Stats
            stats[fixture_name][fmt] = {
                "chars": result.chars,
                "tokens": {t: result.tokens.get(t, 0) for t in tokenizer_names},
            }

            # Tokenize for each tokenizer
            for tok_name in tokenizer_names:
                tokenizer = tokenizers[tok_name]
                token_ids = tokenizer.encode(display_output)
                tokens = [_decode_token(tokenizer, tid) for tid in token_ids]
                token_data[tok_name][fixture_name][fmt] = tokens

    return {
        "formatOutputs": format_outputs,
        "tokenData": token_data,
        "stats": stats,
        "baseChars": base_chars,
        "formatLabels": FORMAT_LABELS,
        "formats": FORMATS,
        "tokenizerModels": TOKENIZERS,
    }


def _truncate_output(output: str) -> tuple[str, bool]:
    """Truncate output for display."""
    lines_list = output.split("\n")
    if len(lines_list) > MAX_EXAMPLE_LINES:
        return "\n".join(lines_list[:MAX_EXAMPLE_LINES]), True
    if len(output) > MAX_EXAMPLE_CHARS:
        return output[:MAX_EXAMPLE_CHARS], True
    return output, False


def _decode_token(tokenizer, token_id: int) -> str:
    """Decode a single token, handling GPT-2 style byte-level BPE encoding.

    Some tokenizers (GPT-2, Mistral, etc.) use byte-level BPE where bytes are
    mapped to unicode characters to avoid control characters in the vocab.
    Common mappings: Ġ = space, Ċ = newline, ĉ = tab.
    """
    decoded = tokenizer.decode([token_id])

    # GPT-2 style byte-level BPE character mappings
    # These unicode chars represent the actual bytes
    decoded = decoded.replace("Ġ", " ")  # U+0120 -> space
    decoded = decoded.replace("Ċ", "\n")  # U+010A -> newline
    decoded = decoded.replace("ĉ", "\t")  # U+0109 -> tab
    decoded = decoded.replace("č", "\r")  # U+010D -> carriage return

    return decoded


def _html_head() -> str:
    return """<!DOCTYPE html>
<html data-theme='dark'><head>
<meta charset='utf-8'>
<title>Minemizer Token Visualization</title>
<style>
:root {
  --bg: #1a1a2e; --bg-secondary: #16213e; --bg-tertiary: #0f3460;
  --text: #e8e8e8; --text-secondary: #a0a0a0; --border: #3a3a5a;
  --accent: #4a9eff; --accent-hover: #3a8eef;
  --best: #4ade80; --table-header: #252545;
  --token-bg: #2a2a4a; --token-border: #4a4a6a;
  --stat-chars-bg: #1e3a5f; --stat-chars-border: #2e5a8f; --stat-chars-text: #7cb3e8;
  --stat-tokens-bg: #3d2a4a; --stat-tokens-border: #5d4a6a; --stat-tokens-text: #c89ed8;
  --stat-og-bg: #1e3d2a; --stat-og-border: #2e5d4a; --stat-og-text: #7ed8a7;
  --stat-enc-bg: #3d2a1e; --stat-enc-border: #5d4a2e; --stat-enc-text: #d8a87e;
}
[data-theme='light'] {
  --bg: #ffffff; --bg-secondary: #f5f5f5; --bg-tertiary: #e8e8e8;
  --text: #333333; --text-secondary: #666666; --border: #dddddd;
  --accent: #4a9eff; --accent-hover: #3a8eef;
  --best: #228855; --table-header: #f0f0f0;
  --token-bg: #f5f5f5; --token-border: #cccccc;
  --stat-chars-bg: #e3f2fd; --stat-chars-border: #90caf9; --stat-chars-text: #1565c0;
  --stat-tokens-bg: #f3e5f5; --stat-tokens-border: #ce93d8; --stat-tokens-text: #7b1fa2;
  --stat-og-bg: #e8f5e9; --stat-og-border: #a5d6a7; --stat-og-text: #2e7d32;
  --stat-enc-bg: #fff3e0; --stat-enc-border: #ffcc80; --stat-enc-text: #e65100;
}
body { font-family: system-ui, sans-serif; margin: 0; padding: 20px;
  background: var(--bg); color: var(--text); transition: background 0.3s, color 0.3s; }
h1, h2, h3 { color: var(--text); }
a { color: var(--accent); }
.theme-toggle { position: fixed; top: 16px; right: 16px; padding: 8px 14px; cursor: pointer;
  border: 1px solid var(--border); border-radius: 6px; background: var(--bg-secondary);
  color: var(--text); font-size: 14px; transition: all 0.2s; z-index: 1000; }
.theme-toggle:hover { background: var(--bg-tertiary); border-color: var(--accent); }
.format { margin: 20px 0; }
.format-header { font-weight: bold; margin-bottom: 8px; color: var(--text-secondary); }
.tokens { font-family: monospace; font-size: 14px; line-height: 1.8; background: var(--bg-secondary);
  padding: 15px; border-radius: 4px; white-space: pre-wrap; word-break: break-all; }
.token { display: inline; border: 1px solid var(--token-border); border-radius: 3px; padding: 1px 2px; margin: 1px; }
.token-space { background: #4a2a2a !important; border-color: #6a4a4a !important; }
.token-newline { background: #3a2a4a !important; color: #999; border-color: #5a4a6a !important; }
[data-theme='light'] .token-space { background: #ffe8e8 !important; border-color: #daa !important; }
[data-theme='light'] .token-newline { background: #f0e8ff !important; border-color: #c8b8e8 !important; }
.na { color: var(--text-secondary); font-style: italic; }
table { border-collapse: collapse; margin: 20px 0; }
th, td { border: 1px solid var(--border); padding: 8px 12px; text-align: right; }
th { background: var(--table-header); font-weight: 600; }
td:first-child, th:first-child { text-align: left; }
.best { font-weight: bold; color: var(--best); }
.partial-best { font-weight: bold; }
.summary-section { margin-bottom: 30px; }
.page-layout { display: flex; gap: 20px; }
.sidebar { position: sticky; top: 20px; align-self: flex-start; width: 120px; flex-shrink: 0; }
.main-content { flex: 1; max-width: 1100px; }
.sidebar-label { font-weight: 600; color: var(--text-secondary); margin-bottom: 8px; font-size: 13px; }
.sidebar-tabs { display: flex; flex-direction: column; gap: 4px; }
.sidebar-tab { padding: 10px 14px; cursor: pointer; border: 1px solid var(--border);
  border-radius: 6px; background: var(--bg-secondary); transition: all 0.2s; user-select: none;
  text-align: center; font-size: 13px; color: var(--text); }
.sidebar-tab:hover { background: var(--bg-tertiary); border-color: var(--accent); }
.sidebar-tab.active { background: var(--accent); border-color: var(--accent); color: white; font-weight: bold; }
.tabs { display: flex; flex-wrap: wrap; gap: 0; margin-bottom: 0; border-bottom: 2px solid var(--border); }
.tab { padding: 10px 20px; cursor: pointer; border: 1px solid transparent; border-bottom: none;
  border-radius: 8px 8px 0 0; background: var(--bg-secondary); margin-bottom: -2px; transition: all 0.2s;
  user-select: none; color: var(--text); }
.tab:hover { background: var(--bg-tertiary); }
.tab.active { background: var(--bg); border-color: var(--border); border-bottom-color: var(--bg); font-weight: bold; }
.tab-content { display: none; }
.tab-content.active { display: block; }
.fixture-info { color: var(--text-secondary); font-size: 14px; margin: 15px 0; padding: 10px;
  background: var(--bg-secondary); border-radius: 4px; }
.comparison-table { font-size: 13px; margin: 15px 0 25px 0; }
.comparison-table th, .comparison-table td { padding: 6px 10px; }
.stats { color: var(--text-secondary); font-size: 13px; display: block; margin-top: 4px; }
.stat-item { display: inline-block; margin-right: 12px; padding: 3px 10px;
  border-radius: 4px; border: 1px solid; }
.stat-chars { background: var(--stat-chars-bg); border-color: var(--stat-chars-border); color: var(--stat-chars-text); }
.stat-tokens { background: var(--stat-tokens-bg); border-color: var(--stat-tokens-border); color: var(--stat-tokens-text); }
.stat-og { background: var(--stat-og-bg); border-color: var(--stat-og-border); color: var(--stat-og-text); }
.stat-enc { background: var(--stat-enc-bg); border-color: var(--stat-enc-border); color: var(--stat-enc-text); }
.format-header-row { display: flex; align-items: center; gap: 10px; }
.copy-btn { padding: 4px 10px; font-size: 12px; cursor: pointer; border: 1px solid var(--border);
  border-radius: 4px; background: var(--bg-secondary); color: var(--text); transition: all 0.2s; }
.copy-btn:hover { background: var(--bg-tertiary); border-color: var(--accent); }
.copy-btn.copied { background: #1e3d2a; border-color: #4ade80; color: #4ade80; }
[data-theme='light'] .copy-btn.copied { background: #d4edda; border-color: #28a745; color: #28a745; }
/* Gradient cells - dark mode colors set via JS */
.gradient-cell { color: #333; transition: background-color 0.3s, color 0.3s; }
.gradient-cell.incomplete { background-color: #e0e0e0; }
[data-theme='dark'] .gradient-cell { color: #fff; }
[data-theme='dark'] .gradient-cell.incomplete { background-color: #4a4a6a; color: #ccc; }
</style>
</head><body>
<button class='theme-toggle' onclick='toggleTheme()'>☀️ Light</button>"""


def _html_intro() -> str:
    return """<h1>Token Visualization</h1>
<p>Compare <a href='https://github.com/ashirviskas/minemizer'>minemizer</a>
to other encoding formats for LLM token efficiency.</p>
<div style='background: #f8f9fa; padding: 12px 16px; border-radius: 6px; margin: 16px 0;
border-left: 4px solid #4a9eff;'>
<strong>Metrics:</strong><br>
<b>chars_og/tok</b> — Original JSON chars per token (source data efficiency)<br>
<b>encoded_chars/tok</b> — Encoded format chars per token (format efficiency)
</div>"""


def _summary_table(results: BenchmarkResults, tokenizer_names: list[str]) -> str:
    """Generate the main summary table."""
    lines = [
        "<div class='summary-section'>",
        "<h2>Token Efficiency Summary</h2>",
        "<p><em>Normalized (JSON pretty = 1.0x, higher is better)</em></p>",
        "<table>",
    ]

    fixture_names = [f.fixture_name for f in results.fixtures]
    header = ["Format"] + [SHORT_NAMES.get(f, f) for f in fixture_names] + ["avg"]
    lines.append("<tr>" + "".join(f"<th>{h}</th>" for h in header) + "</tr>")

    # Compute ratios
    ratios, best_per, baselines = _compute_fixture_ratios(results)
    best_avg, format_complete = _compute_averages(ratios, fixture_names, len(results.fixtures))

    # Compute min/max per fixture column for gradients
    col_extremes: dict[str, tuple[float, float]] = {}
    for f in fixture_names:
        vals: list[float] = [v for fmt in FORMATS if (v := ratios[fmt].get(f)) is not None]
        if vals:
            col_extremes[f] = (min(vals), max(vals))

    # Compute min/max for avg column
    avgs: list[float] = []
    for fmt in FORMATS:
        vals = [v for f in fixture_names if (v := ratios[fmt].get(f)) is not None]
        if vals:
            avgs.append(sum(vals) / len(vals))
    if avgs:
        col_extremes["avg"] = (min(avgs), max(avgs))

    for fmt in FORMATS:
        row = _summary_row(fmt, fixture_names, ratios, best_per, best_avg, format_complete, col_extremes)
        lines.append("<tr>" + "".join(row) + "</tr>")

    lines.extend(["</table>", "</div>"])
    return "\n".join(lines)


def _tokenizer_format_table(results: BenchmarkResults, tokenizer_names: list[str]) -> str:
    """Generate tokenizer × format table."""
    lines = [
        "<div class='summary-section'>",
        "<h2>Tokenizer × Format</h2>",
        "<p><em>Average efficiency per tokenizer (normalized)</em></p>",
        "<table>",
    ]

    header = ["Format"] + tokenizer_names + ["avg"]
    lines.append("<tr>" + "".join(f"<th>{h}</th>" for h in header) + "</tr>")

    # Compute per-tokenizer averages
    table_data, completeness = _compute_tokenizer_data(results, tokenizer_names)
    col_extremes = _column_extremes(table_data, tokenizer_names, completeness)

    for fmt in FORMATS:
        row = _tokenizer_row(fmt, tokenizer_names, table_data, completeness, col_extremes)
        lines.append("<tr>" + "".join(row) + "</tr>")

    lines.extend(["</table>", "</div>"])
    return "\n".join(lines)


def _comparison_section(
    results: BenchmarkResults,
    tokenizer_names: list[str],
) -> str:
    """Generate interactive comparison section with placeholders for JS rendering."""
    lines = [
        "<div class='summary-section'>",
        "<h2>Comparisons</h2>",
        "<p><em>Select tokenizer and example to compare formats</em></p>",
        "</div>",
        "<div class='page-layout'>",
        _sidebar(tokenizer_names),
        "<div class='main-content'>",
        _fixture_tabs(results.fixtures),
    ]

    # Generate Overview panel for each tokenizer
    for i, tok_name in enumerate(tokenizer_names):
        active = " active" if i == 0 else ""
        content_id = f"content-{tok_name}-Overview"
        lines.append(
            f"<div class='tab-content{active}' id='{content_id}' data-tokenizer='{tok_name}' data-fixture='Overview'>"
        )
        lines.append(_compression_overview_panel(results, tok_name, tokenizer_names))
        lines.append("</div>")

    # Generate placeholder containers for each tokenizer × fixture combination
    for tok_name in tokenizer_names:
        for fixture in results.fixtures:
            content_id = f"content-{tok_name}-{fixture.fixture_name}"
            lines.append(
                f"<div class='tab-content' id='{content_id}' "
                f"data-tokenizer='{tok_name}' data-fixture='{fixture.fixture_name}'>"
                f"</div>"
            )

    lines.extend(["</div>", "</div>"])
    return "\n".join(lines)


def _compression_overview_panel(results: BenchmarkResults, tok_name: str, tokenizer_names: list[str]) -> str:
    """Generate overview panel for a tokenizer showing aggregated stats."""
    from benchmarks.config import FORMAT_LABELS

    lines = [
        f"<div class='fixture-info'><strong>Overview</strong> — Aggregated stats for {tok_name}</div>",
        "<h3>Format Efficiency (averaged across fixtures)</h3>",
        "<table>",
        "<tr><th>Format</th><th>Avg Efficiency</th><th>Avg Tokens</th><th>Avg chars_og/tok</th><th>Fixtures</th></tr>",
    ]

    # Compute averages for this tokenizer
    format_stats: dict[str, dict] = {}
    for fmt in FORMATS:
        efficiencies = []
        tokens_list = []
        og_per_tok_list = []

        for fixture in results.fixtures:
            jp = next(r for r in fixture.results if r.format_name == "json_pretty")
            base_chars = jp.chars or 0
            jp_tok = jp.tokens.get(tok_name) or 0
            if not jp_tok:
                continue
            baseline = base_chars / jp_tok

            result = next(r for r in fixture.results if r.format_name == fmt)
            tok_count = result.tokens.get(tok_name) or 0
            if result.chars and tok_count:
                norm = (base_chars / tok_count) / baseline
                efficiencies.append(norm)
                tokens_list.append(tok_count)
                og_per_tok_list.append(base_chars / tok_count)

        if efficiencies:
            format_stats[fmt] = {
                "efficiency": sum(efficiencies) / len(efficiencies),
                "tokens": sum(tokens_list) / len(tokens_list),
                "og_per_tok": sum(og_per_tok_list) / len(og_per_tok_list),
                "count": len(efficiencies),
                "total": len(results.fixtures),
            }

    # Find min/max for gradient coloring
    if format_stats:
        eff_vals = [s["efficiency"] for s in format_stats.values()]
        tok_vals = [s["tokens"] for s in format_stats.values()]
        og_vals = [s["og_per_tok"] for s in format_stats.values()]
        min_eff, max_eff = min(eff_vals), max(eff_vals)
        min_tok, max_tok = min(tok_vals), max(tok_vals)
        min_og, max_og = min(og_vals), max(og_vals)
    else:
        min_eff = max_eff = min_tok = max_tok = min_og = max_og = 0

    # Sort by efficiency descending
    for fmt in sorted(format_stats.keys(), key=lambda f: -format_stats[f]["efficiency"]):
        s = format_stats[fmt]
        label = FORMAT_LABELS.get(fmt, fmt)

        # Efficiency gradient (higher is better)
        eff_ratio = 0.5 if max_eff == min_eff else (s["efficiency"] - min_eff) / (max_eff - min_eff)
        eff_cell = _gradient_cell(eff_ratio, f"{s['efficiency']:.2f}x")

        # Tokens gradient (lower is better)
        tok_ratio = 0.5 if max_tok == min_tok else 1 - (s["tokens"] - min_tok) / (max_tok - min_tok)
        tok_cell = _gradient_cell(tok_ratio, f"{s['tokens']:,.0f}")

        # og_per_tok gradient (higher is better)
        og_ratio = 0.5 if max_og == min_og else (s["og_per_tok"] - min_og) / (max_og - min_og)
        og_cell = _gradient_cell(og_ratio, f"{s['og_per_tok']:.1f}")

        partial = "" if s["count"] == s["total"] else f" ({s['count']}/{s['total']})"
        lines.append(f"<tr><td>{label}</td>{eff_cell}{tok_cell}{og_cell}<td>{s['count']}{partial}</td></tr>")

    # Add formats with no data
    for fmt in FORMATS:
        if fmt not in format_stats:
            label = FORMAT_LABELS.get(fmt, fmt)
            lines.append(
                f"<tr><td>{label}</td><td class='na'>N/A</td><td class='na'>-</td><td class='na'>-</td><td>0</td></tr>"
            )

    lines.append("</table>")

    # Per-fixture breakdown
    lines.append("<h3>Per-Fixture Results</h3>")
    lines.append("<table>")
    header = ["Fixture", "Records", "Base Chars", "Best Format", "Tokens Saved"]
    lines.append("<tr>" + "".join(f"<th>{h}</th>" for h in header) + "</tr>")

    for fixture in results.fixtures:
        jp = next(r for r in fixture.results if r.format_name == "json_pretty")
        base_chars: int = jp.chars or 0
        jp_tok: int = jp.tokens.get(tok_name) or 0

        # Find best format for this fixture
        best_fmt: str | None = None
        best_tokens: int = jp_tok
        for result in fixture.results:
            tok_count: int = result.tokens.get(tok_name) or 0
            if tok_count and tok_count < best_tokens:
                best_tokens = tok_count
                best_fmt = result.format_name

        savings: float = ((jp_tok - best_tokens) / jp_tok * 100) if jp_tok else 0
        best_label = FORMAT_LABELS.get(best_fmt, best_fmt) if best_fmt else "json_pretty"
        name = SHORT_NAMES.get(fixture.fixture_name, fixture.fixture_name)

        # Records count (from fixture metadata if available)
        records = "—"

        lines.append(
            f"<tr><td>{name}</td><td>{records}</td><td>{base_chars:,}</td>"
            f"<td>{best_label}</td><td>{savings:.1f}%</td></tr>"
        )

    lines.append("</table>")
    return "\n".join(lines)


def _sidebar(tokenizer_names: list[str]) -> str:
    lines = [
        "<div class='sidebar'>",
        "<div class='sidebar-label'>Tokenizer</div>",
        "<div class='sidebar-tabs' id='tokenizer-tabs'>",
    ]
    for i, name in enumerate(tokenizer_names):
        active = " active" if i == 0 else ""
        lines.append(f"<div class='sidebar-tab{active}' data-tokenizer='{name}'>{name}</div>")
    lines.extend(["</div>", "</div>"])
    return "\n".join(lines)


def _fixture_tabs(fixtures: list) -> str:
    lines = ["<div class='tab-group'>", "<div class='tabs' id='fixture-tabs'>"]
    # Overview tab first
    lines.append("<div class='tab active' data-fixture='Overview'>Overview</div>")
    for fixture in fixtures:
        name = SHORT_NAMES.get(fixture.fixture_name, fixture.fixture_name)
        lines.append(f"<div class='tab' data-fixture='{fixture.fixture_name}'>{name}</div>")
    lines.extend(["</div>", "</div>"])
    return "\n".join(lines)


def _html_script(tokenizer_names: list[str], first_fixture: str) -> str:
    return f"""<script>
let currentTokenizer = '{tokenizer_names[0]}';
let currentFixture = 'Overview';
const renderedPanels = new Set();

// Switch gradient cells between light and dark colors
function applyGradientTheme(isDark) {{
  document.querySelectorAll('.gradient-cell:not(.incomplete)').forEach(cell => {{
    const color = isDark ? cell.dataset.dark : cell.dataset.light;
    if (color) cell.style.backgroundColor = color;
  }});
}}

// Theme toggle
function toggleTheme() {{
  const html = document.documentElement;
  const btn = document.querySelector('.theme-toggle');
  const isDark = html.dataset.theme !== 'dark';
  html.dataset.theme = isDark ? 'dark' : 'light';
  btn.textContent = isDark ? '☀️ Light' : '🌙 Dark';
  localStorage.setItem('theme', html.dataset.theme);
  applyGradientTheme(isDark);
  // Re-render tokens with new theme colors
  renderedPanels.clear();
  renderPanel(currentTokenizer, currentFixture);
}}

// Load saved theme and apply gradient colors
(function() {{
  const saved = localStorage.getItem('theme');
  if (saved) {{
    document.documentElement.dataset.theme = saved;
    const btn = document.querySelector('.theme-toggle');
    if (btn) btn.textContent = saved === 'dark' ? '☀️ Light' : '🌙 Dark';
  }}
  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', () => applyGradientTheme(document.documentElement.dataset.theme === 'dark'));
  }} else {{
    applyGradientTheme(document.documentElement.dataset.theme === 'dark');
  }}
}})();

// Golden ratio color generation - theme-aware
function hashColor(index) {{
  const golden = 0.618033988749895;
  const hue = (index * golden) % 1.0;
  const isDark = document.documentElement.dataset.theme === 'dark';
  const sat = isDark ? 0.6 : 0.5;
  const light = isDark ? 0.45 : 0.8;
  const q = light < 0.5 ? light * (1 + sat) : light + sat - light * sat;
  const p = 2 * light - q;

  function h2rgb(t) {{
    t = ((t % 1.0) + 1.0) % 1.0;
    if (t < 1/6) return Math.round((p + (q - p) * 6 * t) * 255);
    if (t < 1/2) return Math.round(q * 255);
    if (t < 2/3) return Math.round((p + (q - p) * (2/3 - t) * 6) * 255);
    return Math.round(p * 255);
  }}

  const r = h2rgb(hue + 1/3), g = h2rgb(hue), b = h2rgb(hue - 1/3);
  return '#' + [r, g, b].map(x => x.toString(16).padStart(2, '0')).join('');
}}

function escapeHtml(text) {{
  return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}}

function renderTokens(tokens, truncated) {{
  let html = '';
  const isDark = document.documentElement.dataset.theme === 'dark';
  const textColor = isDark ? '#fff' : '#333';
  for (let i = 0; i < tokens.length; i++) {{
    const token = tokens[i];
    const escaped = escapeHtml(token);
    if (token.includes('\\n')) {{
      const visible = escaped.replace(/\\n/g, '↵');
      html += "<span class='token token-newline'>" + visible + "</span><br>";
    }} else if (token.trim() === '' && token.length > 0) {{
      const visible = escaped.replace(/ /g, '·').replace(/\\t/g, '→');
      html += "<span class='token token-space'>" + visible + "</span>";
    }} else {{
      html += "<span class='token' style='background:" + hashColor(i) + ";color:" + textColor + "'>" + escaped + "</span>";
    }}
  }}
  if (truncated) {{
    html += "<br><em>... (truncated)</em>";
  }}
  return html;
}}

function renderFormatBlock(fmt, tokName, fixtureName) {{
  const data = BENCHMARK_DATA;
  const formatData = data.formatOutputs[fixtureName]?.[fmt];
  const label = data.formatLabels[fmt];

  if (!formatData) {{
    return "<div class='format'><div class='format-header'>" + label + ": <span class='na'>N/A</span></div></div>";
  }}

  const stats = data.stats[fixtureName][fmt];
  const baseChars = data.baseChars[fixtureName];
  const tokCount = stats.tokens[tokName] || 0;
  const charsCount = stats.chars || 0;
  const ogPer = tokCount ? (baseChars / tokCount).toFixed(1) : '0.0';
  const encPer = tokCount ? (charsCount / tokCount).toFixed(1) : '0.0';

  const tokens = data.tokenData[tokName][fixtureName][fmt] || [];
  const tokenHtml = renderTokens(tokens, formatData.truncated);

  const copyId = 'copy-' + fixtureName + '-' + fmt;

  return `<div class='format'>
<div class='format-header-row'>
  <span class='format-header'>${{label}}</span>
  <button class='copy-btn' onclick='copyText("${{copyId}}", "${{fixtureName}}", "${{fmt}}")'>Copy</button>
</div>
<div class='stats'>
  <span class='stat-item stat-chars'>chars: <b>${{charsCount.toLocaleString()}}</b></span>
  <span class='stat-item stat-tokens'>tokens: <b>${{tokCount.toLocaleString()}}</b></span>
  <span class='stat-item stat-og'>chars_og/tok: <b>${{ogPer}}</b></span>
  <span class='stat-item stat-enc'>enc_chars/tok: <b>${{encPer}}</b></span>
</div>
<div class='tokens'>${{tokenHtml}}</div>
</div>`;
}}

function gradientColors(ratio) {{
  // Same formula as Python _gradient_colors - returns [light, dark]
  const lr = Math.round(255 - ratio * 80), lg = Math.round(200 + ratio * 55), lb = Math.round(200 - ratio * 50);
  const dr = Math.round(180 - ratio * 140), dg = Math.round(60 + ratio * 120), db = Math.round(60 - ratio * 20);
  return [`rgb(${{lr}},${{lg}},${{lb}})`, `rgb(${{dr}},${{dg}},${{db}})`];
}}

function gradientCell(ratio, content, sortVal) {{
  // Generate cell with same structure as Python _gradient_cell
  const [light, dark] = gradientColors(ratio);
  const isDark = document.documentElement.dataset.theme === 'dark';
  const bg = isDark ? dark : light;
  return `<td class='gradient-cell' style='background-color:${{bg}}' data-light='${{light}}' data-dark='${{dark}}' data-sort='${{sortVal}}'>${{content}}</td>`;
}}

function renderComparisonTable(fixtureName, tokName) {{
  const data = BENCHMARK_DATA;
  const baseChars = data.baseChars[fixtureName];

  // First pass: collect all values to compute min/max
  const rows = [];
  let minChars = Infinity, maxChars = 0;
  let minToks = Infinity, maxToks = 0;
  let minOg = Infinity, maxOg = 0;
  let minEnc = Infinity, maxEnc = 0;

  for (const fmt of data.formats) {{
    const stats = data.stats[fixtureName]?.[fmt];
    if (!stats) {{
      rows.push({{ fmt, label: data.formatLabels[fmt], valid: false }});
    }} else {{
      const tokCount = stats.tokens[tokName] || 0;
      const ogPer = tokCount ? baseChars / tokCount : 0;
      const encPer = tokCount ? stats.chars / tokCount : 0;

      if (stats.chars) {{ minChars = Math.min(minChars, stats.chars); maxChars = Math.max(maxChars, stats.chars); }}
      if (tokCount) {{ minToks = Math.min(minToks, tokCount); maxToks = Math.max(maxToks, tokCount); }}
      if (ogPer) {{ minOg = Math.min(minOg, ogPer); maxOg = Math.max(maxOg, ogPer); }}
      if (encPer) {{ minEnc = Math.min(minEnc, encPer); maxEnc = Math.max(maxEnc, encPer); }}

      rows.push({{ fmt, label: data.formatLabels[fmt], valid: true, chars: stats.chars, tokens: tokCount, ogPer, encPer }});
    }}
  }}

  // Second pass: render with gradient cells (same structure as static tables)
  let html = `<table class='comparison-table'>
<tr><th>Format</th><th>Chars</th><th>Tokens</th><th>chars_og/tok</th><th>enc_chars/tok</th></tr>`;

  for (const row of rows) {{
    if (!row.valid) {{
      html += `<tr><td>${{row.label}}</td><td colspan='4' class='na'>N/A</td></tr>`;
    }} else {{
      // Chars: lower is better
      const charsRatio = maxChars === minChars ? 0.5 : 1 - (row.chars - minChars) / (maxChars - minChars);
      // Tokens: lower is better
      const toksRatio = maxToks === minToks ? 0.5 : 1 - (row.tokens - minToks) / (maxToks - minToks);
      // og_per_tok: higher is better
      const ogRatio = maxOg === minOg ? 0.5 : (row.ogPer - minOg) / (maxOg - minOg);
      // enc_per_tok: higher is better
      const encRatio = maxEnc === minEnc ? 0.5 : (row.encPer - minEnc) / (maxEnc - minEnc);

      html += `<tr><td>${{row.label}}</td>`;
      html += gradientCell(charsRatio, row.chars.toLocaleString(), row.chars);
      html += gradientCell(toksRatio, row.tokens.toLocaleString(), row.tokens);
      html += gradientCell(ogRatio, row.ogPer.toFixed(1), row.ogPer.toFixed(1));
      html += gradientCell(encRatio, row.encPer.toFixed(1), row.encPer.toFixed(1));
      html += `</tr>`;
    }}
  }}

  html += '</table>';
  return html;
}}

function attachTableSorting(container) {{
  // Attach sorting to all tables in container (same logic as full report)
  container.querySelectorAll('table th').forEach(th => {{
    th.style.cursor = 'pointer';
    th.addEventListener('click', () => {{
      const table = th.closest('table');
      const tbody = table.querySelector('tbody') || table;
      const rows = Array.from(tbody.querySelectorAll('tr')).filter(r => r.querySelector('td'));
      const idx = Array.from(th.parentNode.children).indexOf(th);
      const isAsc = th.classList.contains('sorted-asc');

      table.querySelectorAll('th').forEach(h => h.classList.remove('sorted-asc', 'sorted-desc'));
      th.classList.add(isAsc ? 'sorted-desc' : 'sorted-asc');

      rows.sort((a, b) => {{
        const aVal = a.children[idx]?.dataset.sort || a.children[idx]?.textContent || '';
        const bVal = b.children[idx]?.dataset.sort || b.children[idx]?.textContent || '';
        const aNum = parseFloat(aVal), bNum = parseFloat(bVal);
        const cmp = (!isNaN(aNum) && !isNaN(bNum)) ? aNum - bNum : aVal.localeCompare(bVal);
        return isAsc ? -cmp : cmp;
      }});

      rows.forEach(r => tbody.appendChild(r));
    }});
  }});
}}

function renderPanel(tokName, fixtureName) {{
  // Overview panels are pre-rendered server-side, just attach sorting
  if (fixtureName === 'Overview') {{
    const panelId = 'content-' + tokName + '-Overview';
    const panel = document.getElementById(panelId);
    if (panel && !renderedPanels.has(panelId)) {{
      attachTableSorting(panel);
      renderedPanels.add(panelId);
    }}
    return;
  }}

  const panelId = 'content-' + tokName + '-' + fixtureName;
  const panel = document.getElementById(panelId);
  if (!panel || renderedPanels.has(panelId)) return;

  const data = BENCHMARK_DATA;
  const baseChars = data.baseChars[fixtureName];
  const tokenizerModel = data.tokenizerModels[tokName] || '';

  let html = `<div class='fixture-info'><strong>${{fixtureName}}.json</strong> — Original: ${{baseChars}} chars — Tokenizer: ${{tokName}} (${{tokenizerModel}})</div>`;
  html += renderComparisonTable(fixtureName, tokName);

  for (const fmt of data.formats) {{
    html += renderFormatBlock(fmt, tokName, fixtureName);
  }}

  panel.innerHTML = html;
  attachTableSorting(panel);
  renderedPanels.add(panelId);
}}

function updateContent() {{
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
  const el = document.getElementById('content-' + currentTokenizer + '-' + currentFixture);
  if (el) {{
    el.classList.add('active');
    renderPanel(currentTokenizer, currentFixture);
  }}
}}

function copyText(id, fixtureName, fmt) {{
  const data = BENCHMARK_DATA;
  const formatData = data.formatOutputs[fixtureName]?.[fmt];
  if (!formatData) return;

  const text = formatData.copy;
  navigator.clipboard.writeText(text).then(() => {{
    const btn = document.querySelector(`button[onclick*="${{id}}"]`);
    if (btn) {{
      const wasTruncated = formatData.copyTruncated;
      btn.textContent = wasTruncated ? 'Copied (truncated)!' : 'Copied!';
      btn.classList.add('copied');
      setTimeout(() => {{ btn.textContent = 'Copy'; btn.classList.remove('copied'); }}, 2000);
    }}
  }});
}}

document.querySelectorAll('#tokenizer-tabs .sidebar-tab').forEach(tab => {{
  tab.addEventListener('click', () => {{
    document.querySelectorAll('#tokenizer-tabs .sidebar-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    currentTokenizer = tab.dataset.tokenizer;
    updateContent();
  }});
}});

document.querySelectorAll('#fixture-tabs .tab').forEach(tab => {{
  tab.addEventListener('click', () => {{
    document.querySelectorAll('#fixture-tabs .tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    currentFixture = tab.dataset.fixture;
    updateContent();
  }});
}});

// Render initial panel
document.addEventListener('DOMContentLoaded', () => {{
  renderPanel(currentTokenizer, currentFixture);
}});
</script>"""


# --- Helper computations ---


def _compute_fixture_ratios(results: BenchmarkResults):
    """Compute normalized ratios per format/fixture."""
    ratios: dict[str, dict[str, float | None]] = {fmt: {} for fmt in FORMATS}
    best_per: dict[str, float] = {}
    baselines: dict[str, float] = {}

    for fixture in results.fixtures:
        jp = next(r for r in fixture.results if r.format_name == "json_pretty")
        base = jp.chars or 0
        jp_tok = sum(v for v in jp.tokens.values() if v) / len(jp.tokens)
        baselines[fixture.fixture_name] = base / jp_tok

        best = 0.0
        for result in fixture.results:
            if result.chars is None:
                ratios[result.format_name][fixture.fixture_name] = None
                continue
            avg_tok = sum(v for v in result.tokens.values() if v) / len(result.tokens)
            norm = (base / avg_tok) / baselines[fixture.fixture_name]
            ratios[result.format_name][fixture.fixture_name] = norm
            best = max(best, norm)
        best_per[fixture.fixture_name] = best

    return ratios, best_per, baselines


def _compute_averages(ratios, fixture_names, total):
    """Compute format averages and completeness."""
    avgs: dict[str, float] = {}
    complete: dict[str, bool] = {}

    for fmt in FORMATS:
        vals = [ratios[fmt].get(f) for f in fixture_names]
        valid = [v for v in vals if v is not None]
        if valid:
            avgs[fmt] = sum(valid) / len(valid)
            complete[fmt] = len(valid) == total

    best = max((v for f, v in avgs.items() if complete.get(f)), default=0)
    return best, complete


def _summary_row(fmt, fixture_names, ratios, best_per, best_avg, complete, col_extremes):
    """Generate summary table row with gradient coloring."""
    label = FORMAT_LABELS[fmt]
    row = [f"<td>{label}</td>"]
    vals = []

    for f in fixture_names:
        r = ratios[fmt].get(f)
        if r is None:
            row.append("<td class='na'>✗</td>")
        else:
            vals.append(r)
            mn, mx = col_extremes.get(f, (r, r))
            ratio = 0.5 if mx == mn else (r - mn) / (mx - mn)
            extra_style = " font-weight:bold;" if r == best_per[f] else ""
            row.append(_gradient_cell(ratio, f"{r:.1f}x", extra_style=extra_style))

    if vals:
        avg = sum(vals) / len(vals)
        is_complete = complete.get(fmt, False)
        mn, mx = col_extremes.get("avg", (avg, avg))
        ratio = 0.5 if mx == mn else (avg - mn) / (mx - mn)
        extra_style = " font-weight:bold;" if is_complete and avg == best_avg else ""
        extra_cls = "" if is_complete else "partial-best"
        row.append(_gradient_cell(ratio, f"{avg:.1f}x", extra_cls=extra_cls, extra_style=extra_style))
    else:
        row.append("<td class='na'>N/A</td>")

    return row


def _compute_tokenizer_data(results, tokenizer_names):
    """Compute per-tokenizer averages."""
    data: dict[str, dict[str, float | None]] = {}
    complete: dict[str, dict[str, bool]] = {}
    total = len(results.fixtures)

    for fmt in FORMATS:
        data[fmt] = {}
        complete[fmt] = {}

        for tok in tokenizer_names:
            vals = []
            for fixture in results.fixtures:
                jp = next(r for r in fixture.results if r.format_name == "json_pretty")
                base = jp.chars or 0
                jp_tok = jp.tokens.get(tok)
                if not jp_tok:
                    continue
                baseline = base / jp_tok

                result = next(r for r in fixture.results if r.format_name == fmt)
                if result.chars and result.tokens.get(tok):
                    norm = (base / result.tokens[tok]) / baseline
                    vals.append(norm)

            data[fmt][tok] = sum(vals) / len(vals) if vals else None
            complete[fmt][tok] = len(vals) == total

        # Row average
        row_vals = [v for v in data[fmt].values() if v is not None]
        data[fmt]["avg"] = sum(row_vals) / len(row_vals) if row_vals else None
        complete[fmt]["avg"] = all(complete[fmt].get(t, False) for t in tokenizer_names)

    return data, complete


def _column_extremes(data, tokenizer_names, complete):
    """Find min/max per column for coloring."""
    cols = tokenizer_names + ["avg"]
    extremes: dict[str, tuple[float, float]] = {}

    for col in cols:
        vals = [data[f].get(col) for f in FORMATS if complete[f].get(col) and data[f].get(col)]
        if vals:
            extremes[col] = (min(vals), max(vals))

    return extremes


def _tokenizer_row(fmt, tokenizer_names, data, complete, extremes):
    """Generate tokenizer table row."""
    label = FORMAT_LABELS[fmt]
    row = [f"<td>{label}</td>"]

    for col in tokenizer_names + ["avg"]:
        val = data[fmt].get(col)
        is_complete = complete[fmt].get(col, False)

        if val is None:
            row.append("<td class='na'>✗</td>")
        elif not is_complete:
            row.append(f"<td class='gradient-cell incomplete'>{val:.1f}x</td>")
        else:
            mn, mx = extremes.get(col, (val, val))
            ratio = 0.5 if mx == mn else (val - mn) / (mx - mn)
            extra_style = " font-weight:bold;" if val == mx else ""
            row.append(_gradient_cell(ratio, f"{val:.1f}x", extra_style=extra_style))

    return row
