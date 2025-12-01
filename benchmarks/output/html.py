"""HTML output generation for token visualization."""

from __future__ import annotations

from typing import TYPE_CHECKING

from benchmarks.config import FORMAT_LABELS, FORMATS, MAX_EXAMPLE_CHARS, MAX_EXAMPLE_LINES, SHORT_NAMES, TOKENIZERS
from benchmarks.core.formats import convert_to_format

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

    html = [
        _html_head(),
        _html_intro(),
        _summary_table(results, tokenizer_names),
        _tokenizer_format_table(results, tokenizer_names),
        _comparison_section(results, fixtures, tokenizers, tokenizer_names),
        _html_script(tokenizer_names, results.fixtures[0].fixture_name),
        "</body></html>",
    ]

    return "\n".join(html)


def _html_head() -> str:
    return """<!DOCTYPE html>
<html><head>
<meta charset='utf-8'>
<title>Minemizer Token Visualization</title>
<style>
body { font-family: system-ui, sans-serif; margin: 0; padding: 20px; }
h1, h2, h3 { color: #333; }
.format { margin: 20px 0; }
.format-header { font-weight: bold; margin-bottom: 8px; color: #555; }
.tokens { font-family: monospace; font-size: 14px; line-height: 1.8; background: #f5f5f5;
  padding: 15px; border-radius: 4px; white-space: pre-wrap; word-break: break-all; }
.token { display: inline; border: 1px solid #ccc; border-radius: 3px; padding: 1px 2px; margin: 1px; }
.token-space { background: #ffe8e8 !important; border-color: #daa !important; }
.token-newline { background: #f0e8ff !important; color: #999; border-color: #c8b8e8 !important; }
.na { color: #999; font-style: italic; }
table { border-collapse: collapse; margin: 20px 0; }
th, td { border: 1px solid #ddd; padding: 8px 12px; text-align: right; }
th { background: #f0f0f0; font-weight: 600; }
td:first-child, th:first-child { text-align: left; }
.best { font-weight: bold; color: #228855; }
.partial-best { font-weight: bold; }
.summary-section { margin-bottom: 30px; }
.page-layout { display: flex; gap: 20px; }
.sidebar { position: sticky; top: 20px; align-self: flex-start; width: 120px; flex-shrink: 0; }
.main-content { flex: 1; max-width: 1100px; }
.sidebar-label { font-weight: 600; color: #555; margin-bottom: 8px; font-size: 13px; }
.sidebar-tabs { display: flex; flex-direction: column; gap: 4px; }
.sidebar-tab { padding: 10px 14px; cursor: pointer; border: 1px solid #ddd;
  border-radius: 6px; background: #f5f5f5; transition: all 0.2s; user-select: none;
  text-align: center; font-size: 13px; }
.sidebar-tab:hover { background: #e8e8e8; border-color: #ccc; }
.sidebar-tab.active { background: #4a9eff; border-color: #4a9eff; color: white; font-weight: bold; }
.tabs { display: flex; flex-wrap: wrap; gap: 0; margin-bottom: 0; border-bottom: 2px solid #ddd; }
.tab { padding: 10px 20px; cursor: pointer; border: 1px solid transparent; border-bottom: none;
  border-radius: 8px 8px 0 0; background: #f5f5f5; margin-bottom: -2px; transition: all 0.2s;
  user-select: none; }
.tab:hover { background: #e8e8e8; }
.tab.active { background: white; border-color: #ddd; border-bottom-color: white; font-weight: bold; }
.tab-content { display: none; }
.tab-content.active { display: block; }
.fixture-info { color: #666; font-size: 14px; margin: 15px 0; padding: 10px;
  background: #f9f9f9; border-radius: 4px; }
.comparison-table { font-size: 13px; margin: 15px 0 25px 0; }
.comparison-table th, .comparison-table td { padding: 6px 10px; }
.stats { color: #666; font-size: 13px; display: block; margin-top: 4px; }
.stat-item { display: inline-block; margin-right: 12px; padding: 3px 10px;
  border-radius: 4px; border: 1px solid; }
.stat-chars { background: #e3f2fd; border-color: #90caf9; color: #1565c0; }
.stat-tokens { background: #f3e5f5; border-color: #ce93d8; color: #7b1fa2; }
.stat-og { background: #e8f5e9; border-color: #a5d6a7; color: #2e7d32; }
.stat-enc { background: #fff3e0; border-color: #ffcc80; color: #e65100; }
.format-header-row { display: flex; align-items: center; gap: 10px; }
.copy-btn { padding: 4px 10px; font-size: 12px; cursor: pointer; border: 1px solid #ccc;
  border-radius: 4px; background: #fff; color: #555; transition: all 0.2s; }
.copy-btn:hover { background: #f0f0f0; border-color: #999; }
.copy-btn.copied { background: #d4edda; border-color: #28a745; color: #28a745; }
</style>
</head><body>"""


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

    for fmt in FORMATS:
        row = _summary_row(fmt, fixture_names, ratios, best_per, best_avg, format_complete)
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
    fixtures: dict[str, list[dict]],
    tokenizers: dict[str, PreTrainedTokenizerBase],
    tokenizer_names: list[str],
) -> str:
    """Generate interactive comparison section."""
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

    # Generate content for each combination
    for i, tok_name in enumerate(tokenizer_names):
        for j, fixture in enumerate(results.fixtures):
            active = " active" if i == 0 and j == 0 else ""
            content = _fixture_content(tok_name, fixture, fixtures[fixture.fixture_name], tokenizers[tok_name], active)
            lines.append(content)

    lines.extend(["</div>", "</div>"])
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
    for i, fixture in enumerate(fixtures):
        active = " active" if i == 0 else ""
        name = SHORT_NAMES.get(fixture.fixture_name, fixture.fixture_name)
        lines.append(f"<div class='tab{active}' data-fixture='{fixture.fixture_name}'>{name}</div>")
    lines.extend(["</div>", "</div>"])
    return "\n".join(lines)


def _fixture_content(
    tok_name: str,
    fixture,
    data: list[dict],
    tokenizer: PreTrainedTokenizerBase,
    active: str,
) -> str:
    json_result = next(r for r in fixture.results if r.format_name == "json_pretty")
    base_chars = json_result.chars or 0

    content_id = f"content-{tok_name}-{fixture.fixture_name}"
    lines = [
        f"<div class='tab-content{active}' id='{content_id}' "
        f"data-tokenizer='{tok_name}' data-fixture='{fixture.fixture_name}'>",
        f"<div class='fixture-info'><strong>{fixture.fixture_name}.json</strong> — "
        f"Original: {base_chars} chars — Tokenizer: {tok_name} ({TOKENIZERS.get(tok_name, '')})</div>",
        _comparison_table(fixture, tok_name, base_chars),
    ]

    for fmt in FORMATS:
        result = next(r for r in fixture.results if r.format_name == fmt)
        lines.append(_format_block(fmt, result, data, tokenizer, tok_name, fixture.fixture_name, base_chars))

    lines.append("</div>")
    return "\n".join(lines)


def _comparison_table(fixture, tok_name: str, base_chars: int) -> str:
    lines = [
        "<table class='comparison-table'>",
        "<tr><th>Format</th><th>Chars</th><th>Tokens</th><th>chars_og/tok</th><th>enc_chars/tok</th></tr>",
    ]

    for fmt in FORMATS:
        result = next(r for r in fixture.results if r.format_name == fmt)
        label = FORMAT_LABELS[fmt]
        if result.chars is None:
            lines.append(f"<tr><td>{label}</td><td colspan='4' class='na'>N/A</td></tr>")
        else:
            tok_count = result.tokens.get(tok_name) or 0
            og_per = base_chars / tok_count if tok_count else 0
            enc_per = result.chars / tok_count if tok_count else 0
            lines.append(
                f"<tr><td>{label}</td><td>{result.chars:,}</td><td>{tok_count:,}</td>"
                f"<td>{og_per:.1f}</td><td>{enc_per:.1f}</td></tr>"
            )

    lines.append("</table>")
    return "\n".join(lines)


def _format_block(
    fmt: str,
    result,
    data: list[dict],
    tokenizer: PreTrainedTokenizerBase,
    tok_name: str,
    fixture_name: str,
    base_chars: int,
) -> str:
    label = FORMAT_LABELS[fmt]
    output = convert_to_format(data, fmt)

    if output is None:
        return f"<div class='format'><div class='format-header'>{label}: <span class='na'>N/A</span></div></div>"

    tok_count = result.tokens.get(tok_name) or 0
    chars_count = result.chars or 0
    og_per = base_chars / tok_count if tok_count else 0
    enc_per = chars_count / tok_count if tok_count else 0
    copy_id = f"copy-{tok_name}-{fixture_name}-{fmt}"

    escaped = output.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # Truncate for display
    display = output
    truncated = False
    lines_list = output.split("\n")
    if len(lines_list) > MAX_EXAMPLE_LINES:
        display = "\n".join(lines_list[:MAX_EXAMPLE_LINES])
        truncated = True
    elif len(output) > MAX_EXAMPLE_CHARS:
        display = output[:MAX_EXAMPLE_CHARS]
        truncated = True

    token_ids = tokenizer.encode(display)
    tokens = [tokenizer.decode([tid]) for tid in token_ids]
    token_html = _render_tokens(tokens, truncated)

    return f"""<div class='format'>
<div class='format-header-row'>
  <span class='format-header'>{label}</span>
  <button class='copy-btn' onclick='copyText("{copy_id}")'>Copy</button>
</div>
<textarea id='{copy_id}' style='display:none'>{escaped}</textarea>
<div class='stats'>
  <span class='stat-item stat-chars'>chars: <b>{chars_count:,}</b></span>
  <span class='stat-item stat-tokens'>tokens: <b>{tok_count:,}</b></span>
  <span class='stat-item stat-og'>chars_og/tok: <b>{og_per:.1f}</b></span>
  <span class='stat-item stat-enc'>enc_chars/tok: <b>{enc_per:.1f}</b></span>
</div>
<div class='tokens'>{token_html}</div>
</div>"""


def _render_tokens(tokens: list[str], truncated: bool) -> str:
    spans = []
    for idx, token in enumerate(tokens):
        color = _hash_color(idx)
        escaped = token.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        if "\n" in token:
            visible = escaped.replace("\n", "↵")
            spans.append(f"<span class='token token-newline'>{visible}</span><br>")
        elif token.strip() == "" and token:
            visible = escaped.replace(" ", "·").replace("\t", "→")
            spans.append(f"<span class='token token-space'>{visible}</span>")
        else:
            spans.append(f"<span class='token' style='background:{color}'>{escaped}</span>")
    if truncated:
        spans.append("<br><em>... (truncated)</em>")
    return "".join(spans)


def _hash_color(index: int) -> str:
    """Generate pastel color using golden ratio distribution."""
    golden = 0.618033988749895
    hue = (index * golden) % 1.0
    # HSL to RGB (pastel)
    sat, light = 0.5, 0.85
    q = light * (1 + sat) if light < 0.5 else light + sat - light * sat
    p = 2 * light - q

    def h2rgb(t: float) -> int:
        t = t % 1.0
        if t < 1 / 6:
            return int((p + (q - p) * 6 * t) * 255)
        if t < 1 / 2:
            return int(q * 255)
        if t < 2 / 3:
            return int((p + (q - p) * (2 / 3 - t) * 6) * 255)
        return int(p * 255)

    return f"#{h2rgb(hue + 1 / 3):02x}{h2rgb(hue):02x}{h2rgb(hue - 1 / 3):02x}"


def _html_script(tokenizer_names: list[str], first_fixture: str) -> str:
    return f"""<script>
let currentTokenizer = '{tokenizer_names[0]}';
let currentFixture = '{first_fixture}';

function updateContent() {{
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
  const el = document.getElementById('content-' + currentTokenizer + '-' + currentFixture);
  if (el) el.classList.add('active');
}}

function copyText(id) {{
  const textarea = document.getElementById(id);
  if (!textarea) return;
  navigator.clipboard.writeText(textarea.value).then(() => {{
    const btn = document.querySelector(`button[onclick="copyText('${{id}}')"]`);
    if (btn) {{
      btn.textContent = 'Copied!';
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


def _summary_row(fmt, fixture_names, ratios, best_per, best_avg, complete):
    """Generate summary table row."""
    label = FORMAT_LABELS[fmt]
    row = [f"<td>{label}</td>"]
    vals = []

    for f in fixture_names:
        r = ratios[fmt].get(f)
        if r is None:
            row.append("<td class='na'>✗</td>")
        else:
            vals.append(r)
            cls = " class='best'" if r == best_per[f] else ""
            row.append(f"<td{cls}>{r:.1f}x</td>")

    if vals:
        avg = sum(vals) / len(vals)
        is_complete = complete.get(fmt, False)
        if is_complete and avg == best_avg:
            row.append(f"<td class='best'>{avg:.1f}x</td>")
        elif not is_complete:
            row.append(f"<td class='partial-best'>{avg:.1f}x</td>")
        else:
            row.append(f"<td>{avg:.1f}x</td>")
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
            row.append(f"<td style='background:#e0e0e0;'>{val:.1f}x</td>")
        else:
            mn, mx = extremes.get(col, (val, val))
            ratio = 0.5 if mx == mn else (val - mn) / (mx - mn)
            r = int(255 - ratio * 80)
            g = int(200 + ratio * 55)
            b = int(200 - ratio * 50)
            style = f"background:#{r:02x}{g:02x}{b:02x};"
            if val == mx:
                style += " font-weight:bold;"
            row.append(f"<td style='{style}'>{val:.1f}x</td>")

    return row
