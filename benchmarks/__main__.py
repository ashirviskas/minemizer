"""CLI entry point for benchmarks.

Usage:
    python -m benchmarks generate [--sizes 50,100,1000,5000] [--seed 42]
    python -m benchmarks compression
    python -m benchmarks llm --model MODEL [--endpoint URL] [--data FILE] [--queries N]
    python -m benchmarks report [--include-all]
    python -m benchmarks full-report [--output-dir PATH]
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from benchmarks import FIXTURES_DIR, RESULTS_DIR
from benchmarks.config import DATA_SIZES, DEFAULT_CONCURRENCY, DEFAULT_LLM_ENDPOINT, DEFAULT_SEED


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="python -m benchmarks",
        description="Minemizer benchmark suite",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate synthetic datasets")
    gen_parser.add_argument(
        "--sizes",
        type=str,
        default=",".join(map(str, DATA_SIZES)),
        help=f"Comma-separated sizes (default: {','.join(map(str, DATA_SIZES))})",
    )
    gen_parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help=f"Random seed (default: {DEFAULT_SEED})")

    # Compression command
    comp_parser = subparsers.add_parser("compression", help="Run compression benchmarks")
    comp_parser.add_argument("--no-readme", action="store_true", help="Skip README update")

    # LLM command
    llm_parser = subparsers.add_parser("llm", help="Run LLM accuracy benchmarks")
    llm_parser.add_argument("--model", required=True, help="Model name (e.g., qwen2.5:7b)")
    llm_parser.add_argument(
        "--endpoint", default=DEFAULT_LLM_ENDPOINT, help=f"API endpoint (default: {DEFAULT_LLM_ENDPOINT})"
    )
    llm_parser.add_argument("--api-key", help="API key (optional)")
    llm_parser.add_argument("--data", help="Data file name (e.g., nested_1000) or 'all' for all datasets")
    llm_parser.add_argument("--queries", type=int, default=50, help="Number of queries (default: 50)")
    llm_parser.add_argument(
        "--concurrency",
        type=int,
        default=DEFAULT_CONCURRENCY,
        help=f"Concurrent requests (default: {DEFAULT_CONCURRENCY})",
    )
    llm_parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help=f"Random seed (default: {DEFAULT_SEED})")
    llm_parser.add_argument(
        "--formats", help="Comma-separated formats (default: json_pretty,json_min,yaml,minemizer,minemizer_compact)"
    )
    llm_parser.add_argument(
        "--no-think", action="store_true", help="Prepend /no_think to disable reasoning (Qwen3 models)"
    )

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate HTML report")
    report_parser.add_argument("--include-all", action="store_true", help="Include all LLM results")
    report_parser.add_argument("--output", type=Path, help="Output path")

    # Full report command
    full_parser = subparsers.add_parser("full-report", help="Generate combined benchmark report (HTML + MD)")
    full_parser.add_argument("--output-dir", type=Path, help="Output directory (default: benchmarks/results/)")

    args = parser.parse_args()

    if args.command == "generate":
        return cmd_generate(args)
    elif args.command == "compression":
        return cmd_compression(args)
    elif args.command == "llm":
        return asyncio.run(cmd_llm(args))
    elif args.command == "report":
        return cmd_report(args)
    elif args.command == "full-report":
        return cmd_full_report(args)

    return 1


def cmd_generate(args: argparse.Namespace) -> int:
    """Generate synthetic datasets."""
    from benchmarks.generators.synthetic import save_dataset

    sizes = [int(s.strip()) for s in args.sizes.split(",")]
    print(f"Generating datasets: sizes={sizes}, seed={args.seed}")

    for size in sizes:
        path = save_dataset(size, args.seed)
        print(f"  Created: {path}")

    print("Done!")
    return 0


def cmd_compression(args: argparse.Namespace) -> int:
    """Run compression benchmarks."""
    from benchmarks.core.fixtures import load_fixtures
    from benchmarks.core.tokenizers import load_tokenizers
    from benchmarks.output.html import generate_html
    from benchmarks.output.markdown import generate_markdown, update_readme
    from benchmarks.runners.compression import CompressionBenchmark

    print("=" * 60)
    print("Compression Benchmarks")
    print("=" * 60)
    print()

    # Load tokenizers
    tokenizers, load_time = load_tokenizers()

    # Load fixtures
    fixtures = load_fixtures()
    print(f"Loaded {len(fixtures)} fixtures\n")

    # Run benchmarks
    print("Running benchmarks...")
    benchmark = CompressionBenchmark()
    results = benchmark.run(fixtures, tokenizers)

    # Generate outputs
    markdown = generate_markdown(results)
    print("\nResults:")
    print("-" * 60)
    print(markdown)
    print("-" * 60)

    # Update README
    if not args.no_readme:
        readme_path = Path(__file__).parent.parent / "README.md"
        if update_readme(markdown, readme_path):
            print(f"\nUpdated {readme_path}")
        else:
            print("\nWarning: README markers not found")

    # Save results
    results_dir = RESULTS_DIR / "compression"
    results_dir.mkdir(parents=True, exist_ok=True)

    # JSON results
    json_path = results_dir / "benchmark_results.json"
    json_data = {
        "fixtures": {
            f.fixture_name: {r.format_name: {"chars": r.chars, "tokens": r.tokens} for r in f.results}
            for f in results.fixtures
        }
    }
    json_path.write_text(json.dumps(json_data, indent=2))
    print(f"Saved: {json_path}")

    # HTML visualization
    html_path = results_dir / "benchmark_tokens.html"
    html_content = generate_html(results, fixtures, tokenizers)
    html_path.write_text(html_content)
    print(f"Saved: {html_path}")

    # Timing
    print(f"\nTiming: {results.timing['total']:.2f}s total")

    return 0


async def cmd_llm(args: argparse.Namespace) -> int:
    """Run LLM accuracy benchmarks."""
    from benchmarks.runners.llm_accuracy import run_benchmark

    formats = args.formats.split(",") if args.formats else None

    # Get list of datasets to run
    llm_fixtures = FIXTURES_DIR / "llm_accuracy"
    if not llm_fixtures.exists() or not list(llm_fixtures.glob("*.json")):
        print("No datasets found. Run 'uv run python -m benchmarks generate' first.")
        return 1

    if args.data and args.data.lower() != "all":
        data_files = [args.data]
    else:
        # Run all available datasets
        data_files = sorted([f.stem for f in llm_fixtures.glob("*.json")])

    print("=" * 60)
    print("LLM Accuracy Benchmarks")
    print("=" * 60)
    print(f"Model: {args.model}")
    print(f"Endpoint: {args.endpoint}")
    print(f"Datasets: {', '.join(data_files)}")
    print(f"Queries: {args.queries}")
    print(f"Concurrency: {args.concurrency}")
    print(f"Seed: {args.seed}")
    print()

    all_results = []

    for data_file in data_files:
        print(f"\n{'=' * 60}")
        print(f"Dataset: {data_file}")
        print("=" * 60)

        try:
            results = await run_benchmark(
                data_file=data_file,
                model=args.model,
                n_queries=args.queries,
                endpoint=args.endpoint,
                api_key=args.api_key,
                concurrency=args.concurrency,
                seed=args.seed,
                formats=formats,
                no_think=args.no_think,
            )
            all_results.append((data_file, results))
        except FileNotFoundError as e:
            print(f"Error: {e}")
            continue
        except Exception as e:
            print(f"Error: {e}")
            continue

        # Summary for this dataset
        print(f"\n{data_file} Summary:")
        for fmt, res in results.results.items():
            print(f"  {fmt}: {res.accuracy:.1%} accuracy, {res.avg_latency_ms:.0f}ms avg, {res.tokens:,} tokens")

    if not all_results:
        print("No benchmarks completed successfully.")
        return 1

    # Overall summary
    print("\n" + "=" * 60)
    print("Overall Summary")
    print("=" * 60)
    for data_file, results in all_results:
        print(f"\n{data_file}:")
        for fmt, res in results.results.items():
            print(f"  {fmt}: {res.accuracy:.1%} acc, {res.avg_latency_ms:.0f}ms, {res.tokens:,} tok")

    # Ask about HTML report
    print()
    try:
        response = input("Generate HTML report? [y/N]: ").strip().lower()
        if response == "y":
            include_all = input("Include all other LLM results? [y/N]: ").strip().lower() == "y"
            cmd_report_internal(include_all)
    except EOFError:
        pass

    return 0


def cmd_report(args: argparse.Namespace) -> int:
    """Generate HTML report."""
    return cmd_report_internal(args.include_all, args.output)


def cmd_report_internal(include_all: bool = False, output_path: Path | None = None) -> int:
    """Internal report generation."""
    results_dir = RESULTS_DIR / "llm_accuracy"

    if not results_dir.exists():
        print("No LLM results found")
        return 1

    # Load all results
    all_results = []
    for path in results_dir.glob("*.json"):
        data = json.loads(path.read_text())
        all_results.append((path.stem, data))

    if not all_results:
        print("No LLM results found")
        return 1

    if not include_all:
        # Use most recent only
        all_results = [all_results[-1]]

    # Generate simple HTML report
    output_path = output_path or results_dir / "llm_accuracy_report.html"
    html = _generate_llm_report_html(all_results)
    output_path.write_text(html)
    print(f"Report saved to: {output_path}")

    return 0


def _generate_llm_report_html(all_results: list[tuple[str, dict]]) -> str:
    """Generate HTML report for LLM results with sidebar/tabs structure."""
    # Group results by model and dataset
    by_model: dict[str, list[tuple[str, dict]]] = {}
    datasets: set[str] = set()
    for name, data in all_results:
        model = data["meta"]["model"]
        dataset = data["meta"]["data_file"]
        datasets.add(dataset)
        if model not in by_model:
            by_model[model] = []
        by_model[model].append((dataset, data))

    models = list(by_model.keys())
    datasets_list = sorted(datasets)
    first_model = models[0] if models else ""
    first_dataset = datasets_list[0] if datasets_list else ""

    html = [
        "<!DOCTYPE html>",
        "<html><head>",
        "<meta charset='utf-8'>",
        "<title>LLM Accuracy Benchmarks</title>",
        "<style>",
        _llm_report_css(),
        "</style>",
        "</head><body>",
        "<h1>LLM Accuracy Benchmarks</h1>",
        "<p>Compare format comprehension across models and datasets.</p>",
        _llm_summary_table(all_results, models),
        "<div class='page-layout'>",
        _llm_sidebar(models),
        "<div class='main-content'>",
        _llm_dataset_tabs(datasets_list),
    ]

    # Generate content for each model × dataset combination
    for model in models:
        model_data = {ds: d for ds, d in by_model[model]}
        for dataset in datasets_list:
            if dataset not in model_data:
                continue
            data = model_data[dataset]
            active = " active" if model == first_model and dataset == first_dataset else ""
            html.append(_llm_content_panel(model, dataset, data, active))

    html.extend(
        [
            "</div>",  # main-content
            "</div>",  # page-layout
            _llm_report_script(first_model, first_dataset),
            "</body></html>",
        ]
    )

    return "\n".join(html)


def _llm_report_css() -> str:
    """CSS for LLM report."""
    return """
body { font-family: system-ui, sans-serif; margin: 0; padding: 20px; }
h1, h2, h3 { color: #333; }
table { border-collapse: collapse; margin: 15px 0; width: 100%; }
th, td { border: 1px solid #ddd; padding: 8px 12px; text-align: right; }
th { background: #f0f0f0; font-weight: 600; }
td:first-child, th:first-child { text-align: left; }
.best { font-weight: bold; color: #228855; }
.worst { color: #c62828; }
.summary-section { margin-bottom: 30px; }
.summary-table { width: auto; min-width: 680px; }
.summary-table th, .summary-table td { padding: 8px 12px; }
.summary-table th { cursor: pointer; user-select: none; }
.summary-table th:hover { background: #e0e0e0; }
.summary-table th::after { content: ' ↕'; font-size: 10px; color: #999; }
.summary-table th.sorted-asc::after { content: ' ▲'; color: #333; }
.summary-table th.sorted-desc::after { content: ' ▼'; color: #333; }
.summary-table .col-best { font-weight: bold; }
.metric-explainer { font-size: 13px; color: #666; margin-top: 8px; }
.page-layout { display: flex; gap: 20px; }
.sidebar { position: sticky; top: 20px; align-self: flex-start; width: 140px; flex-shrink: 0; }
.main-content { flex: 1; max-width: 1100px; }
.sidebar-label { font-weight: 600; color: #555; margin-bottom: 8px; font-size: 13px; }
.sidebar-tabs { display: flex; flex-direction: column; gap: 4px; }
.sidebar-tab { padding: 10px 14px; cursor: pointer; border: 1px solid #ddd;
  border-radius: 6px; background: #f5f5f5; transition: all 0.2s; user-select: none;
  text-align: center; font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.sidebar-tab:hover { background: #e8e8e8; border-color: #ccc; }
.sidebar-tab.active { background: #4a9eff; border-color: #4a9eff; color: white; font-weight: bold; }
.tabs { display: flex; flex-wrap: wrap; gap: 0; margin-bottom: 0; border-bottom: 2px solid #ddd; }
.tab { padding: 10px 20px; cursor: pointer; border: 1px solid transparent; border-bottom: none;
  border-radius: 8px 8px 0 0; background: #f5f5f5; margin-bottom: -2px; transition: all 0.2s; user-select: none; }
.tab:hover { background: #e8e8e8; }
.tab.active { background: white; border-color: #ddd; border-bottom-color: white; font-weight: bold; }
.tab-content { display: none; padding: 20px 0; }
.tab-content.active { display: block; }
.meta-info { color: #666; font-size: 14px; margin: 15px 0; padding: 10px; background: #f9f9f9; border-radius: 4px; }
.summary-box { background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 20px 0; }
.summary-box h3 { margin: 0 0 10px 0; color: #1565c0; font-size: 14px; }
.summary-box p { margin: 5px 0; font-size: 13px; }
.query-breakdown { margin-top: 20px; }
.query-breakdown details { margin: 5px 0; }
.query-breakdown summary { cursor: pointer; padding: 8px 12px; background: #f5f5f5; border-radius: 4px; font-size: 13px; }
.query-breakdown summary:hover { background: #e8e8e8; }
.query-list { font-size: 12px; max-height: 400px; overflow-y: auto; border: 1px solid #eee; border-radius: 4px; margin-top: 5px; }
.query-item { padding: 8px 12px; border-bottom: 1px solid #eee; }
.query-item:last-child { border-bottom: none; }
.query-item.correct { background: #f1f8e9; }
.query-item.incorrect { background: #ffebee; }
.query-q { font-weight: 500; margin-bottom: 4px; }
.query-expected { color: #2e7d32; }
.query-actual { color: #555; }
.query-item.incorrect .query-actual { color: #c62828; }
"""


def _llm_summary_table(all_results: list[tuple[str, dict]], models: list[str]) -> str:
    """Generate summary table with all formats averaged per dataset."""
    # Group by dataset
    by_dataset: dict[str, list[dict]] = {}
    for _name, data in all_results:
        dataset = data["meta"]["data_file"]
        if dataset not in by_dataset:
            by_dataset[dataset] = []
        by_dataset[dataset].append(data)

    lines = [
        "<div class='summary-section'>",
        "<h2>Summary</h2>",
        "<p><em>Averaged across models per dataset, sorted by accuracy</em></p>",
    ]

    for dataset, dataset_results in by_dataset.items():
        lines.append(f"<h3>{dataset}</h3>")

        # Aggregate format stats across models
        format_stats: dict[str, dict] = {}
        json_pretty_chars_list: list[int] = []
        for data in dataset_results:
            # Get json_pretty chars as baseline for og_chars/tok
            jp = data["results"].get("json_pretty", {})
            if jp.get("chars"):
                json_pretty_chars_list.append(jp["chars"])
            for fmt, res in data["results"].items():
                if res.get("total_queries", 0) == 0:
                    continue
                if fmt not in format_stats:
                    format_stats[fmt] = {"acc": [], "tokens": [], "chars": [], "latency": []}
                format_stats[fmt]["acc"].append(res.get("accuracy", 0))
                format_stats[fmt]["tokens"].append(res.get("tokens", 0))
                format_stats[fmt]["chars"].append(res.get("chars", 0))
                format_stats[fmt]["latency"].append(res.get("avg_latency_ms", 0))

        if not format_stats:
            continue

        # Baseline: average json_pretty chars and tokens
        base_chars = sum(json_pretty_chars_list) / len(json_pretty_chars_list) if json_pretty_chars_list else 0
        json_pretty_tokens_list = [
            data["results"].get("json_pretty", {}).get("tokens", 0)
            for data in dataset_results
            if data["results"].get("json_pretty", {}).get("tokens")
        ]
        base_tokens = sum(json_pretty_tokens_list) / len(json_pretty_tokens_list) if json_pretty_tokens_list else 1

        # Compute averages
        avg_data = []
        for fmt, stats in format_stats.items():
            avg_acc = sum(stats["acc"]) / len(stats["acc"]) if stats["acc"] else 0
            avg_tokens = sum(stats["tokens"]) / len(stats["tokens"]) if stats["tokens"] else 0
            avg_latency = sum(stats["latency"]) / len(stats["latency"]) if stats["latency"] else 0
            og_cpt = base_chars / avg_tokens if avg_tokens else 0  # original chars per token
            compression_ratio = base_tokens / avg_tokens if avg_tokens else 0
            efficiency = avg_acc * compression_ratio  # Accuracy × Compression Ratio
            avg_data.append(
                {
                    "fmt": fmt,
                    "acc": avg_acc,
                    "tokens": avg_tokens,
                    "og_cpt": og_cpt,
                    "latency": avg_latency,
                    "efficiency": efficiency,
                }
            )

        # Sort by efficiency descending (default)
        avg_data.sort(key=lambda x: -x["efficiency"])

        # Find min/max for gradients and best values
        eff_vals = [d["efficiency"] for d in avg_data if d["efficiency"] > 0]
        acc_vals = [d["acc"] for d in avg_data]
        tok_vals = [d["tokens"] for d in avg_data if d["tokens"] > 0]
        og_cpt_vals = [d["og_cpt"] for d in avg_data if d["og_cpt"] > 0]

        eff_range = (min(eff_vals), max(eff_vals)) if eff_vals else (0, 1)
        acc_range = (min(acc_vals), max(acc_vals)) if acc_vals else (0, 1)
        tok_range = (min(tok_vals), max(tok_vals)) if tok_vals else (0, 1)
        og_cpt_range = (min(og_cpt_vals), max(og_cpt_vals)) if og_cpt_vals else (0, 1)

        # Best values (highest eff/acc/og_cpt, lowest tokens)
        best_eff = max(eff_vals) if eff_vals else 0
        best_acc = max(acc_vals) if acc_vals else 0
        best_tok = min(tok_vals) if tok_vals else 0
        best_og_cpt = max(og_cpt_vals) if og_cpt_vals else 0

        lines.append("<table class='summary-table'>")
        lines.append(
            "<tr><th>Format</th><th>Efficiency</th><th>Acc</th><th>Tokens</th><th>og_chars/tok</th><th>Latency (WIP)</th></tr>"
        )

        for d in avg_data:
            eff_style = _gradient_style_with_best(
                d["efficiency"], eff_range[0], eff_range[1], True, d["efficiency"] == best_eff
            )
            acc_style = _gradient_style_with_best(d["acc"], acc_range[0], acc_range[1], True, d["acc"] == best_acc)
            tok_style = _gradient_style_with_best(
                d["tokens"], tok_range[0], tok_range[1], False, d["tokens"] == best_tok
            )
            og_cpt_style = _gradient_style_with_best(
                d["og_cpt"], og_cpt_range[0], og_cpt_range[1], True, d["og_cpt"] == best_og_cpt
            )

            # Compact token display (32k instead of 32,441)
            tok_display = f"{d['tokens'] / 1000:.1f}k" if d["tokens"] >= 1000 else f"{d['tokens']:.0f}"

            lines.append(
                f"<tr><td data-sort='{d['fmt']}'>{d['fmt']}</td>"
                f"<td{eff_style} data-sort='{d['efficiency']:.4f}'>{d['efficiency']:.2f}</td>"
                f"<td{acc_style} data-sort='{d['acc']:.4f}'>{d['acc']:.1%}</td>"
                f"<td{tok_style} data-sort='{d['tokens']:.0f}'>{tok_display}</td>"
                f"<td{og_cpt_style} data-sort='{d['og_cpt']:.4f}'>{d['og_cpt']:.1f}</td>"
                f"<td data-sort='{d['latency']:.0f}'>{d['latency']:.0f}ms</td></tr>"
            )

        lines.append("</table>")
        lines.append(
            "<p class='metric-explainer'><strong>Efficiency</strong> = Accuracy × (JSON tokens ÷ Format tokens). "
            "Higher is better — balances accuracy with token savings.</p>"
        )

    lines.append("</div>")
    return "\n".join(lines)


def _gradient_style(val: float, min_val: float, max_val: float, higher_better: bool) -> str:
    """Generate cell background gradient style."""
    if max_val == min_val:
        return ""
    ratio = (val - min_val) / (max_val - min_val)
    if not higher_better:
        ratio = 1 - ratio  # Invert for "lower is better"
    # Green gradient: bad=red-ish, good=green-ish
    r = int(255 - ratio * 80)
    g = int(200 + ratio * 55)
    b = int(200 - ratio * 50)
    return f" style='background:#{r:02x}{g:02x}{b:02x};'"


def _gradient_style_with_best(val: float, min_val: float, max_val: float, higher_better: bool, is_best: bool) -> str:
    """Generate cell style with gradient and bold for best value."""
    if max_val == min_val:
        ratio = 0.5
    else:
        ratio = (val - min_val) / (max_val - min_val)
        if not higher_better:
            ratio = 1 - ratio
    r = int(255 - ratio * 80)
    g = int(200 + ratio * 55)
    b = int(200 - ratio * 50)
    cls = " class='col-best'" if is_best else ""
    return f"{cls} style='background:#{r:02x}{g:02x}{b:02x};'"


def _llm_sidebar(models: list[str]) -> str:
    """Generate model selector sidebar."""
    lines = [
        "<div class='sidebar'>",
        "<div class='sidebar-label'>Model</div>",
        "<div class='sidebar-tabs' id='model-tabs'>",
    ]
    for i, model in enumerate(models):
        active = " active" if i == 0 else ""
        # Truncate long model names for display
        display = model[:18] + "..." if len(model) > 20 else model
        lines.append(f"<div class='sidebar-tab{active}' data-model='{model}' title='{model}'>{display}</div>")
    lines.extend(["</div>", "</div>"])
    return "\n".join(lines)


def _llm_dataset_tabs(datasets: list[str]) -> str:
    """Generate dataset tabs."""
    lines = ["<div class='tab-group'>", "<div class='tabs' id='dataset-tabs'>"]
    for i, dataset in enumerate(datasets):
        active = " active" if i == 0 else ""
        lines.append(f"<div class='tab{active}' data-dataset='{dataset}'>{dataset}</div>")
    lines.extend(["</div>", "</div>"])
    return "\n".join(lines)


def _llm_content_panel(model: str, dataset: str, data: dict, active: str) -> str:
    """Generate content panel for a model × dataset combination."""
    meta = data["meta"]
    results = data["results"]
    content_id = f"content-{model}-{dataset}".replace(" ", "_").replace(".", "_")

    lines = [
        f"<div class='tab-content{active}' id='{content_id}' data-model='{model}' data-dataset='{dataset}'>",
        f"<div class='meta-info'><strong>{model}</strong> on {dataset} "
        f"({meta['data_size']:,} records) — {meta['n_queries']} queries — {meta['date'][:10]}</div>",
    ]

    # Find best/worst for highlighting
    valid = {k: v for k, v in results.items() if v.get("total_queries", 0) > 0}
    if valid:
        best_acc = max(r["accuracy"] for r in valid.values())
        worst_acc = min(r["accuracy"] for r in valid.values())
        tokens_list = [r.get("tokens") for r in valid.values() if r.get("tokens")]
        min_tokens = min(tokens_list) if tokens_list else 0
    else:
        best_acc = worst_acc = min_tokens = 0

    # Results table
    lines.append("<table>")
    lines.append(
        "<tr><th>Format</th><th>Accuracy</th><th>Tokens</th><th>Chars</th><th>Chars/Tok</th><th>Latency</th></tr>"
    )

    for fmt, res in sorted(results.items(), key=lambda x: -x[1].get("accuracy", 0)):
        acc = res.get("accuracy", 0)
        tokens = res.get("tokens", 0)
        chars = res.get("chars", 0)
        latency = res.get("avg_latency_ms", 0)
        total = res.get("total_queries", 0)
        cpt = chars / tokens if tokens else 0

        acc_style = _accuracy_cell_style(acc, best_acc, worst_acc, total > 0)
        tok_style = " class='best'" if tokens == min_tokens and tokens > 0 else ""

        lines.append(
            f"<tr><td>{fmt}</td><td{acc_style}>{acc:.1%}</td>"
            f"<td{tok_style}>{tokens:,}</td><td>{chars:,}</td>"
            f"<td>{cpt:.1f}</td><td>{latency:.0f}ms</td></tr>"
        )

    lines.append("</table>")

    # Minemizer vs JSON comparison box
    minemizer = {k: v for k, v in results.items() if "minemizer" in k.lower() and v.get("total_queries", 0) > 0}
    json_res = results.get("json_pretty", {})

    if minemizer and json_res.get("total_queries", 0) > 0:
        best_mine = max(minemizer.items(), key=lambda x: x[1].get("accuracy", 0))
        mine_tok = best_mine[1].get("tokens", 0)
        json_tok = json_res.get("tokens", 0)
        token_savings = (1 - mine_tok / json_tok) * 100 if json_tok else 0
        acc_diff = (best_mine[1].get("accuracy", 0) - json_res.get("accuracy", 0)) * 100

        lines.append("<div class='summary-box'>")
        lines.append("<h3>Minemizer vs JSON</h3>")
        lines.append(f"<p><strong>Best variant:</strong> {best_mine[0]}</p>")
        lines.append(f"<p><strong>Token savings:</strong> {token_savings:.1f}%</p>")
        lines.append(f"<p><strong>Accuracy diff:</strong> {acc_diff:+.1f}%</p>")
        lines.append("</div>")

    # Query details (collapsible)
    lines.append("<div class='query-breakdown'>")
    lines.append("<h3>Query Details</h3>")

    for fmt, res in sorted(results.items(), key=lambda x: -x[1].get("accuracy", 0)):
        queries = res.get("queries", [])
        if not queries:
            continue

        correct = sum(1 for q in queries if q.get("correct"))
        lines.append(
            f"<details><summary>{fmt}: {correct}/{len(queries)} correct ({100 * correct / len(queries):.0f}%)</summary>"
        )
        lines.append("<div class='query-list'>")

        for q in queries:
            cls = "correct" if q.get("correct") else "incorrect"
            lines.append(f"<div class='query-item {cls}'>")
            lines.append(f"<div class='query-q'>Q: {q.get('question', '')}</div>")
            lines.append(f"<div class='query-expected'>Expected: {q.get('expected', '')}</div>")
            lines.append(f"<div class='query-actual'>Actual: {q.get('actual', '')}</div>")
            lines.append("</div>")

        lines.append("</div></details>")

    lines.append("</div>")  # query-breakdown
    lines.append("</div>")  # tab-content

    return "\n".join(lines)


def _accuracy_cell_style(acc: float, best: float, worst: float, valid: bool) -> str:
    """Generate cell style based on accuracy value."""
    if not valid:
        return ""
    if acc == best:
        return " class='best'"
    if acc == worst and best != worst:
        return " class='worst'"
    # Gradient between worst and best
    if best > worst:
        ratio = (acc - worst) / (best - worst)
        r = int(255 - ratio * 80)
        g = int(200 + ratio * 55)
        b = int(200 - ratio * 50)
        return f" style='background:#{r:02x}{g:02x}{b:02x};'"
    return ""


def _llm_report_script(first_model: str, first_dataset: str) -> str:
    """JavaScript for interactive tabs and sorting."""
    return f"""<script>
let currentModel = '{first_model}';
let currentDataset = '{first_dataset}';

function updateContent() {{
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
  const id = 'content-' + currentModel.replace(/ /g, '_').replace(/\\./g, '_') + '-' + currentDataset;
  const el = document.getElementById(id);
  if (el) el.classList.add('active');
}}

document.querySelectorAll('#model-tabs .sidebar-tab').forEach(tab => {{
  tab.addEventListener('click', () => {{
    document.querySelectorAll('#model-tabs .sidebar-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    currentModel = tab.dataset.model;
    updateContent();
  }});
}});

document.querySelectorAll('#dataset-tabs .tab').forEach(tab => {{
  tab.addEventListener('click', () => {{
    document.querySelectorAll('#dataset-tabs .tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    currentDataset = tab.dataset.dataset;
    updateContent();
  }});
}});

// Table sorting
document.querySelectorAll('.summary-table th').forEach(th => {{
  th.addEventListener('click', () => {{
    const table = th.closest('table');
    const tbody = table.querySelector('tbody') || table;
    const rows = Array.from(tbody.querySelectorAll('tr')).filter(r => r.querySelector('td'));
    const idx = Array.from(th.parentNode.children).indexOf(th);
    const isAsc = th.classList.contains('sorted-asc');

    // Clear other sort indicators
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
</script>"""


if __name__ == "__main__":
    sys.exit(main())
