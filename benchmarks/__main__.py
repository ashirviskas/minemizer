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
    llm_parser.add_argument("--name", help="Run name for output file (defaults to sanitized model name)")
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

    run_name = args.name  # Will be None if not provided, benchmark will use sanitized model name

    print("=" * 60)
    print("LLM Accuracy Benchmarks")
    print("=" * 60)
    print(f"Model: {args.model}")
    if run_name:
        print(f"Run name: {run_name}")
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
                run_name=run_name,
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
    for _name, data in all_results:
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
        model_data = dict(by_model[model])
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


def _get_data_type(dataset_name: str) -> str:
    """Determine data type from dataset name."""
    if dataset_name.startswith("flat_"):
        return "flat"
    elif dataset_name.startswith("sparse_"):
        return "sparse"
    return "nested"


def _llm_combined_summary(all_results: list[tuple[str, dict]]) -> str:
    """Generate combined summary tables, grouped by data type for fair comparison."""
    n_models = len({data["meta"]["model"] for _name, data in all_results})

    # Group results by data type
    by_type: dict[str, list[tuple[str, dict]]] = {"nested": [], "flat": [], "sparse": []}
    for name, data in all_results:
        dataset_name = data["meta"]["data_file"]
        dtype = _get_data_type(dataset_name)
        by_type[dtype].append((name, data))

    lines = ["<div class='summary-section'>", "<h2>LLM Accuracy Summary</h2>"]

    # Generate summary for each data type that has results
    for dtype in ["nested", "flat", "sparse"]:
        type_results = by_type[dtype]
        if not type_results:
            continue

        table_html = _build_type_summary_table(type_results, dtype, n_models)
        if table_html:
            lines.append(table_html)

    lines.extend(
        [
            "<p class='metric-explainer'><strong>Efficiency</strong> = Accuracy × (JSON tokens ÷ Format tokens). "
            "Higher is better — balances accuracy with token savings.</p>",
            "</div>",
        ]
    )

    return "\n".join(lines)


def _build_type_summary_table(results: list[tuple[str, dict]], dtype: str, n_models: int) -> str:
    """Build summary table for a specific data type."""
    # Aggregate stats for this data type
    format_stats: dict[str, dict] = {}
    base_chars_list: list[int] = []
    base_tokens_list: list[int] = []

    for _name, data in results:
        jp = data["results"].get("json_pretty", {})
        if jp.get("chars"):
            base_chars_list.append(jp["chars"])
        if jp.get("tokens"):
            base_tokens_list.append(jp["tokens"])

        for fmt, res in data["results"].items():
            if res.get("total_queries", 0) == 0:
                continue
            if fmt not in format_stats:
                format_stats[fmt] = {"acc": [], "tokens": [], "latency": []}
            format_stats[fmt]["acc"].append(res.get("accuracy", 0))
            format_stats[fmt]["tokens"].append(res.get("tokens", 0))
            format_stats[fmt]["latency"].append(res.get("avg_latency_ms", 0))

    if not format_stats:
        return ""

    base_chars = sum(base_chars_list) / len(base_chars_list) if base_chars_list else 0
    base_tokens = sum(base_tokens_list) / len(base_tokens_list) if base_tokens_list else 1
    n_datasets = len(results)

    # Compute averages
    avg_data = []
    for fmt, stats in format_stats.items():
        avg_acc = sum(stats["acc"]) / len(stats["acc"]) if stats["acc"] else 0
        avg_tokens = sum(stats["tokens"]) / len(stats["tokens"]) if stats["tokens"] else 0
        avg_latency = sum(stats["latency"]) / len(stats["latency"]) if stats["latency"] else 0
        og_cpt = base_chars / avg_tokens if avg_tokens else 0
        compression_ratio = base_tokens / avg_tokens if avg_tokens else 0
        efficiency = avg_acc * compression_ratio

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

    avg_data.sort(key=lambda x: -x["efficiency"])

    # Build HTML
    type_label = dtype.capitalize()
    lines = [
        f"<h3>{type_label} Data</h3>",
        f"<p><em>{n_datasets} dataset(s), {n_models} model(s). Sorted by efficiency.</em></p>",
    ]
    lines.append(_build_summary_table(avg_data, show_coverage=False))

    return "\n".join(lines)


def _build_summary_table(data: list[dict], show_coverage: bool = False) -> str:
    """Build an HTML summary table for format data."""
    if not data:
        return ""

    # Find min/max for gradients
    eff_vals = [d["efficiency"] for d in data if d["efficiency"] > 0]
    acc_vals = [d["acc"] for d in data]
    tok_vals = [d["tokens"] for d in data if d["tokens"] > 0]
    og_cpt_vals = [d["og_cpt"] for d in data if d["og_cpt"] > 0]
    lat_vals = [d["latency"] for d in data if d["latency"] > 0]

    eff_range = (min(eff_vals), max(eff_vals)) if eff_vals else (0, 1)
    acc_range = (min(acc_vals), max(acc_vals)) if acc_vals else (0, 1)
    tok_range = (min(tok_vals), max(tok_vals)) if tok_vals else (0, 1)
    og_cpt_range = (min(og_cpt_vals), max(og_cpt_vals)) if og_cpt_vals else (0, 1)
    lat_range = (min(lat_vals), max(lat_vals)) if lat_vals else (0, 1)

    best_eff = max(eff_vals) if eff_vals else 0
    best_acc = max(acc_vals) if acc_vals else 0
    best_tok = min(tok_vals) if tok_vals else 0
    best_og_cpt = max(og_cpt_vals) if og_cpt_vals else 0
    best_lat = min(lat_vals) if lat_vals else 0

    header = (
        "<tr><th>Format</th><th>Efficiency</th><th>Accuracy</th><th>Tokens</th><th>og_chars/tok</th><th>Latency</th>"
    )
    if show_coverage:
        header += "<th>Coverage</th>"
    header += "</tr>"

    lines = ["<table class='summary-table'>", header]

    for d in data:
        eff_style = _gradient_style_with_best(
            d["efficiency"], eff_range[0], eff_range[1], True, d["efficiency"] == best_eff
        )
        acc_style = _gradient_style_with_best(d["acc"], acc_range[0], acc_range[1], True, d["acc"] == best_acc)
        tok_style = _gradient_style_with_best(d["tokens"], tok_range[0], tok_range[1], False, d["tokens"] == best_tok)
        og_cpt_style = _gradient_style_with_best(
            d["og_cpt"], og_cpt_range[0], og_cpt_range[1], True, d["og_cpt"] == best_og_cpt
        )
        lat_style = _gradient_style_with_best(d["latency"], lat_range[0], lat_range[1], False, d["latency"] == best_lat)

        tok_display = f"{d['tokens'] / 1000:.1f}k" if d["tokens"] >= 1000 else f"{d['tokens']:.0f}"

        row = (
            f"<tr><td>{d['fmt']}</td>"
            f"<td{eff_style}>{d['efficiency']:.2f}</td>"
            f"<td{acc_style}>{d['acc']:.1%}</td>"
            f"<td{tok_style}>{tok_display}</td>"
            f"<td{og_cpt_style}>{d['og_cpt']:.1f}</td>"
            f"<td{lat_style}>{d['latency']:.0f}ms</td>"
        )
        if show_coverage:
            row += f"<td>{d['coverage']}</td>"
        row += "</tr>"
        lines.append(row)

    lines.append("</table>")
    return "\n".join(lines)


def _gradient_colors(ratio: float) -> tuple[str, str]:
    """Generate light and dark mode gradient colors for a ratio (0=bad, 1=good)."""
    # Light mode: pastel pink-to-green
    lr, lg, lb = int(255 - ratio * 80), int(200 + ratio * 55), int(200 - ratio * 50)
    # Dark mode: saturated red-to-green
    dr, dg, db = int(180 - ratio * 140), int(60 + ratio * 120), int(60 - ratio * 20)
    return f"#{lr:02x}{lg:02x}{lb:02x}", f"#{dr:02x}{dg:02x}{db:02x}"


def _gradient_cell_attrs(ratio: float, extra_cls: str = "") -> str:
    """Generate gradient cell attributes with light/dark colors."""
    light, dark = _gradient_colors(ratio)
    cls = f"gradient-cell {extra_cls}".strip()
    return f" class='{cls}' style='background-color:{light};' data-light='{light}' data-dark='{dark}'"


def _gradient_style_with_best(val: float, min_val: float, max_val: float, higher_better: bool, is_best: bool) -> str:
    """Generate cell style with gradient and bold for best value."""
    if max_val == min_val:
        ratio = 0.5
    else:
        ratio = (val - min_val) / (max_val - min_val)
        if not higher_better:
            ratio = 1 - ratio
    return _gradient_cell_attrs(ratio, "col-best" if is_best else "")


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


def _build_overview_type_table(datasets: dict[str, dict], dtype: str) -> str:
    """Build aggregated table for a specific data type in overview panel."""
    format_stats: dict[str, dict] = {}
    base_chars_list: list[int] = []
    base_tokens_list: list[int] = []

    for _ds_name, data in datasets.items():
        jp = data["results"].get("json_pretty", {})
        if jp.get("chars"):
            base_chars_list.append(jp["chars"])
        if jp.get("tokens"):
            base_tokens_list.append(jp["tokens"])

        for fmt, res in data["results"].items():
            if res.get("total_queries", 0) == 0:
                continue
            if fmt not in format_stats:
                format_stats[fmt] = {"acc": [], "tokens": [], "latency": []}
            format_stats[fmt]["acc"].append(res.get("accuracy", 0))
            format_stats[fmt]["tokens"].append(res.get("tokens", 0))
            format_stats[fmt]["latency"].append(res.get("avg_latency_ms", 0))

    if not format_stats:
        return ""

    base_chars = sum(base_chars_list) / len(base_chars_list) if base_chars_list else 0
    base_tokens = sum(base_tokens_list) / len(base_tokens_list) if base_tokens_list else 1

    avg_data = []
    for fmt, stats in format_stats.items():
        avg_acc = sum(stats["acc"]) / len(stats["acc"]) if stats["acc"] else 0
        avg_tokens = sum(stats["tokens"]) / len(stats["tokens"]) if stats["tokens"] else 0
        avg_latency = sum(stats["latency"]) / len(stats["latency"]) if stats["latency"] else 0
        og_cpt = base_chars / avg_tokens if avg_tokens else 0
        compression_ratio = base_tokens / avg_tokens if avg_tokens else 0
        efficiency = avg_acc * compression_ratio
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

    avg_data.sort(key=lambda x: -x["efficiency"])

    # Find min/max for gradients
    eff_vals = [d["efficiency"] for d in avg_data if d["efficiency"] > 0]
    acc_vals = [d["acc"] for d in avg_data]
    tok_vals = [d["tokens"] for d in avg_data if d["tokens"] > 0]
    og_cpt_vals = [d["og_cpt"] for d in avg_data if d["og_cpt"] > 0]
    lat_vals = [d["latency"] for d in avg_data if d["latency"] > 0]

    eff_range = (min(eff_vals), max(eff_vals)) if eff_vals else (0, 1)
    acc_range = (min(acc_vals), max(acc_vals)) if acc_vals else (0, 1)
    tok_range = (min(tok_vals), max(tok_vals)) if tok_vals else (0, 1)
    og_cpt_range = (min(og_cpt_vals), max(og_cpt_vals)) if og_cpt_vals else (0, 1)
    lat_range = (min(lat_vals), max(lat_vals)) if lat_vals else (0, 1)

    lines = [
        f"<h3>{dtype.capitalize()} Data ({len(datasets)} dataset(s))</h3>",
        "<table>",
        "<tr><th>Format</th><th>Efficiency</th><th>Accuracy</th><th>Tokens</th><th>og_chars/tok</th><th>Latency</th></tr>",
    ]

    for d in avg_data:
        eff_style = _gradient_cell_style(d["efficiency"], eff_range[0], eff_range[1], True)
        acc_style = _gradient_cell_style(d["acc"], acc_range[0], acc_range[1], True)
        tok_style = _gradient_cell_style(d["tokens"], tok_range[0], tok_range[1], False)
        og_cpt_style = _gradient_cell_style(d["og_cpt"], og_cpt_range[0], og_cpt_range[1], True)
        lat_style = _gradient_cell_style(d["latency"], lat_range[0], lat_range[1], False)

        tok_display = f"{d['tokens']:,.0f}" if d["tokens"] < 10000 else f"{d['tokens'] / 1000:.1f}k"

        lines.append(
            f"<tr><td>{d['fmt']}</td><td{eff_style}>{d['efficiency']:.2f}</td>"
            f"<td{acc_style}>{d['acc']:.1%}</td><td{tok_style}>{tok_display}</td>"
            f"<td{og_cpt_style}>{d['og_cpt']:.1f}</td><td{lat_style}>{d['latency']:.0f}ms</td></tr>"
        )

    lines.append("</table>")
    return "\n".join(lines)


def _llm_overview_panel(model: str, datasets: dict[str, dict], active: str) -> str:
    """Generate overview panel for a model showing aggregated stats by data type."""
    content_id = f"content-{model}-Overview".replace(" ", "_").replace(".", "_")

    lines = [
        f"<div class='tab-content{active}' id='{content_id}' data-model='{model}' data-dataset='Overview'>",
        f"<div class='meta-info'><strong>{model}</strong> — {len(datasets)} dataset(s)</div>",
    ]

    # Group datasets by type
    by_type: dict[str, dict[str, dict]] = {"nested": {}, "flat": {}, "sparse": {}}
    for ds_name, data in datasets.items():
        dtype = _get_data_type(ds_name)
        by_type[dtype][ds_name] = data

    # Generate table for each data type
    for dtype in ["nested", "flat", "sparse"]:
        type_datasets = by_type[dtype]
        if not type_datasets:
            continue

        table_html = _build_overview_type_table(type_datasets, dtype)
        if table_html:
            lines.append(table_html)

    if not any(by_type.values()):
        lines.append("<p>No results available.</p>")

    # Individual runs overview
    lines.append("<h3>Individual Runs</h3>")
    lines.append("<table>")
    lines.append(
        "<tr><th>Dataset</th><th>Records</th><th>Queries</th><th>Date</th><th>Best Format</th><th>Best Acc</th></tr>"
    )

    for dataset in sorted(datasets.keys()):
        data = datasets[dataset]
        meta = data["meta"]
        results = data["results"]

        # Find best format by accuracy (excluding failed ones)
        valid = {k: v for k, v in results.items() if v.get("total_queries", 0) > 0}
        if valid:
            best_fmt, best_res = max(valid.items(), key=lambda x: x[1].get("accuracy", 0))
            best_acc = best_res.get("accuracy", 0)
        else:
            best_fmt, best_acc = "-", 0

        lines.append(
            f"<tr><td>{dataset}</td><td>{meta['data_size']:,}</td><td>{meta['n_queries']}</td>"
            f"<td>{meta['date'][:10]}</td><td>{best_fmt}</td><td>{best_acc:.1%}</td></tr>"
        )

    lines.append("</table>")
    lines.append("</div>")

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

    # Get json_pretty as baseline for og_chars/tok and efficiency
    json_pretty = results.get("json_pretty", {})
    base_chars = json_pretty.get("chars", 0)
    base_tokens = json_pretty.get("tokens", 1)

    # Find min/max for highlighting across all metrics
    valid = {k: v for k, v in results.items() if v.get("total_queries", 0) > 0}
    if valid:
        acc_vals = [r["accuracy"] for r in valid.values()]
        tokens_vals = [r.get("tokens") for r in valid.values() if r.get("tokens")]
        latency_vals = [r.get("avg_latency_ms") for r in valid.values() if r.get("avg_latency_ms")]
        og_cpt_vals = [base_chars / r.get("tokens", 1) for r in valid.values() if r.get("tokens")]
        eff_vals = [r["accuracy"] * (base_tokens / r.get("tokens", 1)) for r in valid.values() if r.get("tokens")]

        min_acc, max_acc = min(acc_vals), max(acc_vals)
        min_tok, max_tok = (min(tokens_vals), max(tokens_vals)) if tokens_vals else (0, 0)
        min_lat, max_lat = (min(latency_vals), max(latency_vals)) if latency_vals else (0, 0)
        min_og_cpt, max_og_cpt = (min(og_cpt_vals), max(og_cpt_vals)) if og_cpt_vals else (0, 0)
        min_eff, max_eff = (min(eff_vals), max(eff_vals)) if eff_vals else (0, 0)
    else:
        min_acc = max_acc = min_tok = max_tok = min_lat = max_lat = 0
        min_og_cpt = max_og_cpt = min_eff = max_eff = 0

    # Results table
    lines.append("<table>")
    lines.append(
        "<tr><th>Format</th><th>Efficiency</th><th>Accuracy</th><th>Tokens</th><th>og_chars/tok</th><th>Latency</th></tr>"
    )

    for fmt, res in sorted(
        results.items(),
        key=lambda x: -(x[1].get("accuracy", 0) * (base_tokens / x[1].get("tokens", 1)) if x[1].get("tokens") else 0),
    ):
        acc = res.get("accuracy", 0)
        tokens = res.get("tokens", 0)
        latency = res.get("avg_latency_ms", 0)
        total = res.get("total_queries", 0)
        og_cpt = base_chars / tokens if tokens else 0
        efficiency = acc * (base_tokens / tokens) if tokens else 0

        if total == 0:
            lines.append(f"<tr><td>{fmt}</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td></tr>")
            continue

        eff_style = _gradient_cell_style(efficiency, min_eff, max_eff, True)
        acc_style = _gradient_cell_style(acc, min_acc, max_acc, True)
        tok_style = _gradient_cell_style(tokens, min_tok, max_tok, False)
        og_cpt_style = _gradient_cell_style(og_cpt, min_og_cpt, max_og_cpt, True)
        lat_style = _gradient_cell_style(latency, min_lat, max_lat, False)

        lines.append(
            f"<tr><td>{fmt}</td><td{eff_style}>{efficiency:.2f}</td><td{acc_style}>{acc:.1%}</td>"
            f"<td{tok_style}>{tokens:,}</td><td{og_cpt_style}>{og_cpt:.1f}</td><td{lat_style}>{latency:.0f}ms</td></tr>"
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


def _gradient_cell_style(val: float, min_val: float, max_val: float, higher_better: bool) -> str:
    """Generate gradient cell style for any metric.

    Args:
        val: The value to style.
        min_val: The minimum value in the range.
        max_val: The maximum value in the range.
        higher_better: True if higher values are better (accuracy), False if lower is better (tokens, latency).

    Returns:
        HTML attributes string with gradient styling.
    """
    if max_val == min_val:
        ratio = 0.5
    else:
        # Normalize to 0-1 range
        ratio = (val - min_val) / (max_val - min_val)
        # If lower is better, invert so low values get high ratio (green)
        if not higher_better:
            ratio = 1 - ratio

    # Determine if this is the best value
    is_best = (val == max_val) if higher_better else (val == min_val)
    return _gradient_cell_attrs(ratio, "col-best" if is_best else "")


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


def cmd_full_report(args: argparse.Namespace) -> int:
    """Generate combined benchmark report (HTML + MD)."""
    from benchmarks.core.fixtures import load_fixtures
    from benchmarks.core.tokenizers import load_tokenizers
    from benchmarks.runners.compression import CompressionBenchmark

    output_dir = args.output_dir or RESULTS_DIR

    # Load compression data (run benchmark if needed to get full results)
    compression_results = None
    compression_fixtures = None
    compression_tokenizers = None
    try:
        tokenizers, _ = load_tokenizers()
        fixtures = load_fixtures()
        benchmark = CompressionBenchmark()
        compression_results = benchmark.run(fixtures, tokenizers)
        compression_fixtures = fixtures
        compression_tokenizers = tokenizers
        print("Loaded compression benchmark data")
    except Exception as e:
        print(f"Could not load compression data: {e}")

    # Load LLM results
    llm_dir = RESULTS_DIR / "llm_accuracy"
    llm_results = []
    if llm_dir.exists():
        for path in sorted(llm_dir.glob("*.json")):
            if path.name != "llm_accuracy_report.html":
                data = json.loads(path.read_text())
                llm_results.append((path.stem, data))

    if not compression_results and not llm_results:
        print("No benchmark results found. Run benchmarks first.")
        return 1

    # Generate HTML report
    html_path = output_dir / "full_report.html"
    html = _generate_full_report_html(compression_results, compression_fixtures, compression_tokenizers, llm_results)
    html_path.write_text(html)
    print(f"HTML report saved to: {html_path}")

    # Generate MD report
    md_path = output_dir / "full_report.md"
    md = _generate_full_report_md(compression_results, llm_results)
    md_path.write_text(md)
    print(f"Markdown report saved to: {md_path}")

    return 0


def _generate_full_report_html(
    compression_results, compression_fixtures, compression_tokenizers, llm_results: list[tuple[str, dict]]
) -> str:
    """Generate combined HTML report with restructured layout.

    Structure:
    1. Token Efficiency summary (top level)
    2. Tokenizer x Format table (top level)
    3. Combined LLM Accuracy summary (averaged across all datasets)
    4. Tabs for: Compression details, LLM Accuracy details
    """
    import json

    from benchmarks.output.html import (
        _build_data_blob,
        _comparison_section,
        _html_script,
        _summary_table,
        _tokenizer_format_table,
    )

    has_compression = compression_results is not None
    has_llm = len(llm_results) > 0

    tokenizer_names = list(compression_tokenizers.keys()) if compression_tokenizers else []

    html = [
        "<!DOCTYPE html>",
        "<html data-theme='dark'><head>",
        "<meta charset='utf-8'>",
        "<title>Minemizer Benchmark Report</title>",
        "<style>",
        _full_report_css(),
        "</style>",
        "</head><body>",
        "<button class='theme-toggle' onclick='toggleTheme()'>☀️ Light</button>",
        "<h1>Minemizer Benchmark Report</h1>",
        "<p>Compare <a href='https://github.com/ashirviskas/minemizer'>minemizer</a> "
        "to other encoding formats for LLM token efficiency.</p>",
    ]

    # Token Efficiency summary at top level (from compression)
    if has_compression:
        html.append("<h2>Token Efficiency</h2>")
        html.append("<p>Normalized comparison across formats and tokenizers (JSON pretty = 1.0x).</p>")
        html.append(_summary_table(compression_results, tokenizer_names))
        html.append(_tokenizer_format_table(compression_results, tokenizer_names))

    # Combined LLM Accuracy summary (averaged across all datasets)
    if has_llm:
        html.append(_llm_combined_summary(llm_results))

    # Top-level section tabs for details
    html.append("<div class='section-tabs' id='section-tabs'>")
    if has_compression:
        html.append("<div class='section-tab active' data-section='compression'>Compression Details</div>")
    if has_llm:
        active = "" if has_compression else " active"
        html.append(f"<div class='section-tab{active}' data-section='llm'>LLM Accuracy Details</div>")
    html.append("</div>")

    # Compression section - detailed fixture comparisons
    if has_compression:
        data_blob = _build_data_blob(compression_results, compression_fixtures, compression_tokenizers, tokenizer_names)

        html.append("<div class='section-content active' id='section-compression' data-section='compression'>")
        html.append("<h2>Compression Details</h2>")
        html.append("<p>Detailed token visualization per fixture.</p>")
        html.append(_comparison_section(compression_results, tokenizer_names))
        html.append("</div>")

        html.append(f"<script>const BENCHMARK_DATA = {json.dumps(data_blob, separators=(',', ':'))};</script>")

    # LLM Accuracy section - detailed model/dataset breakdown
    if has_llm:
        active = "" if has_compression else " active"
        html.append(f"<div class='section-content{active}' id='section-llm' data-section='llm'>")
        html.append(_full_report_llm_section(llm_results))
        html.append("</div>")

    # Combined scripts
    html.append(_full_report_script())
    if has_compression:
        first_fixture = compression_results.fixtures[0].fixture_name if compression_results.fixtures else ""
        html.append(_html_script(tokenizer_names, first_fixture))

    html.append("</body></html>")

    return "\n".join(html)


def _full_report_css() -> str:
    """CSS for full report - includes compression HTML styles with dark/light mode."""
    return """
:root {
  --bg: #1a1a2e; --bg-secondary: #16213e; --bg-tertiary: #0f3460;
  --text: #e8e8e8; --text-secondary: #a0a0a0; --border: #3a3a5a;
  --accent: #4a9eff; --accent-hover: #3a8eef;
  --best: #4ade80; --worst: #f87171; --table-header: #252545;
  --token-bg: #2a2a4a; --token-border: #4a4a6a;
  --stat-chars-bg: #1e3a5f; --stat-chars-border: #2e5a8f; --stat-chars-text: #7cb3e8;
  --stat-tokens-bg: #3d2a4a; --stat-tokens-border: #5d4a6a; --stat-tokens-text: #c89ed8;
  --stat-og-bg: #1e3d2a; --stat-og-border: #2e5d4a; --stat-og-text: #7ed8a7;
  --stat-enc-bg: #3d2a1e; --stat-enc-border: #5d4a2e; --stat-enc-text: #d8a87e;
  --summary-box-bg: #1e3a5f; --summary-box-border: #2e5a8f; --summary-box-text: #7cb3e8;
  --correct-bg: #1e3d2a; --incorrect-bg: #3d1e1e;
}
[data-theme='light'] {
  --bg: #ffffff; --bg-secondary: #f5f5f5; --bg-tertiary: #e8e8e8;
  --text: #333333; --text-secondary: #666666; --border: #dddddd;
  --accent: #4a9eff; --accent-hover: #3a8eef;
  --best: #228855; --worst: #c62828; --table-header: #f0f0f0;
  --token-bg: #f5f5f5; --token-border: #cccccc;
  --stat-chars-bg: #e3f2fd; --stat-chars-border: #90caf9; --stat-chars-text: #1565c0;
  --stat-tokens-bg: #f3e5f5; --stat-tokens-border: #ce93d8; --stat-tokens-text: #7b1fa2;
  --stat-og-bg: #e8f5e9; --stat-og-border: #a5d6a7; --stat-og-text: #2e7d32;
  --stat-enc-bg: #fff3e0; --stat-enc-border: #ffcc80; --stat-enc-text: #e65100;
  --summary-box-bg: #e3f2fd; --summary-box-border: #90caf9; --summary-box-text: #1565c0;
  --correct-bg: #f1f8e9; --incorrect-bg: #ffebee;
}
body { font-family: system-ui, sans-serif; margin: 0; padding: 20px; max-width: 1400px;
  background: var(--bg); color: var(--text); transition: background 0.3s, color 0.3s; }
h1, h2, h3 { color: var(--text); }
a { color: var(--accent); }
.theme-toggle { position: fixed; top: 16px; right: 16px; padding: 8px 14px; cursor: pointer;
  border: 1px solid var(--border); border-radius: 6px; background: var(--bg-secondary);
  color: var(--text); font-size: 14px; transition: all 0.2s; z-index: 1000; }
.theme-toggle:hover { background: var(--bg-tertiary); border-color: var(--accent); }
table { border-collapse: collapse; margin: 15px 0; }
th, td { border: 1px solid var(--border); padding: 8px 12px; text-align: right; }
th { background: var(--table-header); font-weight: 600; }
td:first-child, th:first-child { text-align: left; }
.best { font-weight: bold; color: var(--best); }
.partial-best { font-weight: bold; }
.worst { color: var(--worst); }
.na { color: var(--text-secondary); font-style: italic; }

/* Summary table */
.summary-section { margin-bottom: 30px; }
.summary-table { width: auto; min-width: 680px; }
.summary-table th, .summary-table td { padding: 8px 12px; }
.summary-table th { cursor: pointer; user-select: none; }
.summary-table th:hover { background: var(--bg-tertiary); }
.summary-table th::after { content: ' ↕'; font-size: 10px; color: var(--text-secondary); }
.summary-table th.sorted-asc::after { content: ' ▲'; color: var(--text); }
.summary-table th.sorted-desc::after { content: ' ▼'; color: var(--text); }
.summary-table .col-best { font-weight: bold; }
.metric-explainer { font-size: 13px; color: var(--text-secondary); margin-top: 8px; }

/* Section tabs */
.section-tabs { display: flex; gap: 0; margin: 30px 0 0 0; border-bottom: 3px solid var(--accent); }
.section-tab { padding: 12px 24px; cursor: pointer; background: var(--bg-secondary); border: 1px solid var(--border);
  border-bottom: none; border-radius: 8px 8px 0 0; margin-right: 4px; font-weight: 500;
  transition: all 0.2s; user-select: none; color: var(--text); }
.section-tab:hover { background: var(--bg-tertiary); }
.section-tab.active { background: var(--accent); color: white; border-color: var(--accent); }
.section-content { display: none; padding: 20px 0; }
.section-content.active { display: block; }

/* Inner layout */
.page-layout { display: flex; gap: 20px; }
.sidebar { position: sticky; top: 20px; align-self: flex-start; width: 140px; flex-shrink: 0; }
.main-content { flex: 1; max-width: 1100px; }
.sidebar-label { font-weight: 600; color: var(--text-secondary); margin-bottom: 8px; font-size: 13px; }
.sidebar-tabs { display: flex; flex-direction: column; gap: 4px; }
.sidebar-tab { padding: 10px 14px; cursor: pointer; border: 1px solid var(--border);
  border-radius: 6px; background: var(--bg-secondary); transition: all 0.2s; user-select: none;
  text-align: center; font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: var(--text); }
.sidebar-tab:hover { background: var(--bg-tertiary); border-color: var(--accent); }
.sidebar-tab.active { background: var(--accent); border-color: var(--accent); color: white; font-weight: bold; }
.tabs { display: flex; flex-wrap: wrap; gap: 0; margin-bottom: 0; border-bottom: 2px solid var(--border); }
.tab { padding: 10px 20px; cursor: pointer; border: 1px solid transparent; border-bottom: none;
  border-radius: 8px 8px 0 0; background: var(--bg-secondary); margin-bottom: -2px; transition: all 0.2s;
  user-select: none; color: var(--text); }
.tab:hover { background: var(--bg-tertiary); }
.tab.active { background: var(--bg); border-color: var(--border); border-bottom-color: var(--bg); font-weight: bold; }
.tab-content { display: none; padding: 20px 0; }
.tab-content.active { display: block; }

/* Meta and details */
.meta-info { color: var(--text-secondary); font-size: 14px; margin: 15px 0; padding: 10px;
  background: var(--bg-secondary); border-radius: 4px; }
.fixture-info { color: var(--text-secondary); font-size: 14px; margin: 15px 0; padding: 10px;
  background: var(--bg-secondary); border-radius: 4px; }
.summary-box { background: var(--summary-box-bg); padding: 15px; border-radius: 8px; margin: 20px 0;
  border: 1px solid var(--summary-box-border); }
.summary-box h3 { margin: 0 0 10px 0; color: var(--summary-box-text); font-size: 14px; }
.summary-box p { margin: 5px 0; font-size: 13px; }
.query-breakdown { margin-top: 20px; }
.query-breakdown details { margin: 5px 0; }
.query-breakdown summary { cursor: pointer; padding: 8px 12px; background: var(--bg-secondary);
  border-radius: 4px; font-size: 13px; color: var(--text); }
.query-breakdown summary:hover { background: var(--bg-tertiary); }
.query-list { font-size: 12px; max-height: 400px; overflow-y: auto; border: 1px solid var(--border);
  border-radius: 4px; margin-top: 5px; }
.query-item { padding: 8px 12px; border-bottom: 1px solid var(--border); }
.query-item:last-child { border-bottom: none; }
.query-item.correct { background: var(--correct-bg); }
.query-item.incorrect { background: var(--incorrect-bg); }
.query-q { font-weight: 500; margin-bottom: 4px; }
.query-expected { color: var(--best); }
.query-actual { color: var(--text-secondary); }
.query-item.incorrect .query-actual { color: var(--worst); }

/* Compression token visualization */
.format { margin: 20px 0; }
.format-header { font-weight: bold; margin-bottom: 8px; color: var(--text-secondary); }
.format-header-row { display: flex; align-items: center; gap: 10px; }
.tokens { font-family: monospace; font-size: 14px; line-height: 1.8; background: var(--bg-secondary);
  padding: 15px; border-radius: 4px; white-space: pre-wrap; word-break: break-all; }
.token { display: inline; border: 1px solid var(--token-border); border-radius: 3px; padding: 1px 2px; margin: 1px; }
.token-space { background: #4a2a2a !important; border-color: #6a4a4a !important; }
.token-newline { background: #3a2a4a !important; color: #999; border-color: #5a4a6a !important; }
[data-theme='light'] .token-space { background: #ffe8e8 !important; border-color: #daa !important; }
[data-theme='light'] .token-newline { background: #f0e8ff !important; border-color: #c8b8e8 !important; }
.comparison-table { font-size: 13px; margin: 15px 0 25px 0; }
.comparison-table th, .comparison-table td { padding: 6px 10px; }
.stats { color: var(--text-secondary); font-size: 13px; display: block; margin-top: 4px; }
.stat-item { display: inline-block; margin-right: 12px; padding: 3px 10px; border-radius: 4px; border: 1px solid; }
.stat-chars { background: var(--stat-chars-bg); border-color: var(--stat-chars-border); color: var(--stat-chars-text); }
.stat-tokens { background: var(--stat-tokens-bg); border-color: var(--stat-tokens-border); color: var(--stat-tokens-text); }
.stat-og { background: var(--stat-og-bg); border-color: var(--stat-og-border); color: var(--stat-og-text); }
.stat-enc { background: var(--stat-enc-bg); border-color: var(--stat-enc-border); color: var(--stat-enc-text); }
.copy-btn { padding: 4px 10px; font-size: 12px; cursor: pointer; border: 1px solid var(--border);
  border-radius: 4px; background: var(--bg-secondary); color: var(--text); transition: all 0.2s; }
.copy-btn:hover { background: var(--bg-tertiary); border-color: var(--accent); }
.copy-btn.copied { background: #1e3d2a; border-color: #4ade80; color: #4ade80; }
[data-theme='light'] .copy-btn.copied { background: #d4edda; border-color: #28a745; color: #28a745; }

/* Gradient cells - colors adjusted by JS on theme change */
.gradient-cell { color: #333; transition: background 0.3s, color 0.3s; }
[data-theme='dark'] .gradient-cell { color: #fff; }
"""


def _full_report_llm_section(llm_results: list[tuple[str, dict]]) -> str:
    """Generate LLM accuracy section content."""
    import json as json_module

    # Group by model, tracking datasets per model
    by_model: dict[str, dict[str, dict]] = {}
    for _name, data in llm_results:
        model = data["meta"]["model"]
        dataset = data["meta"]["data_file"]
        if model not in by_model:
            by_model[model] = {}
        by_model[model][dataset] = data

    models = list(by_model.keys())
    if not models:
        return "<p>No LLM benchmark results found.</p>"

    first_model = models[0]
    # "Overview" is always first tab
    first_dataset = "Overview"

    # Build model -> datasets mapping for JS (Overview + actual datasets)
    model_datasets = {m: ["Overview"] + sorted(by_model[m].keys()) for m in models}

    lines = [
        "<h2>LLM Accuracy Benchmarks</h2>",
        "<p>Format comprehension across models and datasets.</p>",
        "<div class='page-layout'>",
        _llm_sidebar(models),
        "<div class='main-content'>",
        "<div class='tabs' id='dataset-tabs'></div>",  # Dynamically populated by JS
    ]

    # Generate Overview panel for each model
    for model in models:
        active = " active" if model == first_model else ""
        lines.append(_llm_overview_panel(model, by_model[model], active))

    # Generate content for each model × dataset (only for datasets that exist)
    for model in models:
        for dataset, data in by_model[model].items():
            lines.append(_llm_content_panel(model, dataset, data, ""))

    lines.extend(["</div>", "</div>"])  # main-content, page-layout

    # Add the LLM-specific JavaScript with dynamic tabs
    model_datasets_json = json_module.dumps(model_datasets)
    lines.append(f"""<script>
const MODEL_DATASETS = {model_datasets_json};
let currentModel = '{first_model}';
let currentDataset = '{first_dataset}';

function updateDatasetTabs() {{
  const datasets = MODEL_DATASETS[currentModel] || [];
  const container = document.getElementById('dataset-tabs');
  container.innerHTML = datasets.map((ds, i) =>
    `<div class="tab${{ds === currentDataset ? ' active' : ''}}" data-dataset="${{ds}}">${{ds}}</div>`
  ).join('');

  // Re-attach event listeners
  container.querySelectorAll('.tab').forEach(tab => {{
    tab.addEventListener('click', () => {{
      container.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      currentDataset = tab.dataset.dataset;
      updateLLMContent();
    }});
  }});

  // If current dataset not in new model, switch to first
  if (!datasets.includes(currentDataset) && datasets.length > 0) {{
    currentDataset = datasets[0];
    container.querySelector('.tab')?.classList.add('active');
  }}
}}

function updateLLMContent() {{
  document.querySelectorAll('#section-llm .tab-content').forEach(c => c.classList.remove('active'));
  const id = 'content-' + currentModel.replace(/ /g, '_').replace(/\\./g, '_') + '-' + currentDataset;
  const el = document.getElementById(id);
  if (el) el.classList.add('active');
}}

document.querySelectorAll('#model-tabs .sidebar-tab').forEach(tab => {{
  tab.addEventListener('click', () => {{
    document.querySelectorAll('#model-tabs .sidebar-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    currentModel = tab.dataset.model;
    updateDatasetTabs();
    updateLLMContent();
  }});
}});

// Initialize tabs on load
updateDatasetTabs();
</script>""")

    return "\n".join(lines)


def _full_report_script() -> str:
    """JavaScript for full report section tabs and sorting."""
    return """<script>
// Switch gradient cells between light and dark colors
function applyGradientTheme(isDark) {
  document.querySelectorAll('.gradient-cell:not(.incomplete)').forEach(cell => {
    const color = isDark ? cell.dataset.dark : cell.dataset.light;
    if (color) cell.style.backgroundColor = color;
  });
}

// Theme toggle
function toggleTheme() {
  const html = document.documentElement;
  const btn = document.querySelector('.theme-toggle');
  const isDark = html.dataset.theme !== 'dark';
  html.dataset.theme = isDark ? 'dark' : 'light';
  btn.textContent = isDark ? '☀️ Light' : '🌙 Dark';
  localStorage.setItem('theme', html.dataset.theme);
  applyGradientTheme(isDark);
}

// Load saved theme
(function() {
  const saved = localStorage.getItem('theme');
  if (saved) {
    document.documentElement.dataset.theme = saved;
    const btn = document.querySelector('.theme-toggle');
    if (btn) btn.textContent = saved === 'dark' ? '☀️ Light' : '🌙 Dark';
  }
  // Apply gradient colors after DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => applyGradientTheme(document.documentElement.dataset.theme === 'dark'));
  } else {
    applyGradientTheme(document.documentElement.dataset.theme === 'dark');
  }
})();

// Section tab switching
document.querySelectorAll('#section-tabs .section-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('#section-tabs .section-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.section-content').forEach(c => c.classList.remove('active'));
    tab.classList.add('active');
    const section = tab.dataset.section;
    document.getElementById('section-' + section)?.classList.add('active');
  });
});

// Table sorting
document.querySelectorAll('.summary-table th').forEach(th => {
  th.addEventListener('click', () => {
    const table = th.closest('table');
    const tbody = table.querySelector('tbody') || table;
    const rows = Array.from(tbody.querySelectorAll('tr')).filter(r => r.querySelector('td'));
    const idx = Array.from(th.parentNode.children).indexOf(th);
    const isAsc = th.classList.contains('sorted-asc');

    table.querySelectorAll('th').forEach(h => h.classList.remove('sorted-asc', 'sorted-desc'));
    th.classList.add(isAsc ? 'sorted-desc' : 'sorted-asc');

    rows.sort((a, b) => {
      const aVal = a.children[idx]?.dataset.sort || a.children[idx]?.textContent || '';
      const bVal = b.children[idx]?.dataset.sort || b.children[idx]?.textContent || '';
      const aNum = parseFloat(aVal), bNum = parseFloat(bVal);
      const cmp = (!isNaN(aNum) && !isNaN(bNum)) ? aNum - bNum : aVal.localeCompare(bVal);
      return isAsc ? -cmp : cmp;
    });

    rows.forEach(r => tbody.appendChild(r));
  });
});
</script>"""


def _generate_full_report_md(compression_results, llm_results: list[tuple[str, dict]]) -> str:
    """Generate combined Markdown report."""
    lines = [
        "# Minemizer Benchmark Report",
        "",
        "Compare [minemizer](https://github.com/ashirviskas/minemizer) to other encoding formats for LLM token efficiency.",
        "",
    ]

    # LLM Summary
    if llm_results:
        lines.extend(_md_llm_summary(llm_results))

    # Compression section
    if compression_results:
        lines.extend(_md_compression_section(compression_results))

    # LLM Accuracy section
    if llm_results:
        lines.extend(_md_llm_section(llm_results))

    return "\n".join(lines)


def _md_llm_summary(llm_results: list[tuple[str, dict]]) -> list[str]:
    """Generate markdown summary table."""
    lines = ["## Summary", "", "*Efficiency = Accuracy × (JSON tokens ÷ Format tokens)*", ""]

    # Group by dataset
    by_dataset: dict[str, list[dict]] = {}
    for _name, data in llm_results:
        dataset = data["meta"]["data_file"]
        if dataset not in by_dataset:
            by_dataset[dataset] = []
        by_dataset[dataset].append(data)

    for dataset, dataset_results in by_dataset.items():
        lines.append(f"### {dataset}")
        lines.append("")
        lines.append("| Format | Efficiency | Acc | Tokens | og_chars/tok |")
        lines.append("|--------|------------|-----|--------|--------------|")

        # Aggregate stats
        format_stats: dict[str, dict] = {}
        json_pretty_tokens_list = []
        json_pretty_chars_list = []

        for data in dataset_results:
            jp = data["results"].get("json_pretty", {})
            if jp.get("tokens"):
                json_pretty_tokens_list.append(jp["tokens"])
            if jp.get("chars"):
                json_pretty_chars_list.append(jp["chars"])
            for fmt, res in data["results"].items():
                if res.get("total_queries", 0) == 0:
                    continue
                if fmt not in format_stats:
                    format_stats[fmt] = {"acc": [], "tokens": []}
                format_stats[fmt]["acc"].append(res.get("accuracy", 0))
                format_stats[fmt]["tokens"].append(res.get("tokens", 0))

        base_tokens = sum(json_pretty_tokens_list) / len(json_pretty_tokens_list) if json_pretty_tokens_list else 1
        base_chars = sum(json_pretty_chars_list) / len(json_pretty_chars_list) if json_pretty_chars_list else 0

        avg_data = []
        for fmt, stats in format_stats.items():
            avg_acc = sum(stats["acc"]) / len(stats["acc"]) if stats["acc"] else 0
            avg_tokens = sum(stats["tokens"]) / len(stats["tokens"]) if stats["tokens"] else 0
            compression_ratio = base_tokens / avg_tokens if avg_tokens else 0
            efficiency = avg_acc * compression_ratio
            og_cpt = base_chars / avg_tokens if avg_tokens else 0
            avg_data.append({"fmt": fmt, "eff": efficiency, "acc": avg_acc, "tokens": avg_tokens, "og_cpt": og_cpt})

        avg_data.sort(key=lambda x: -x["eff"])

        for d in avg_data:
            tok_display = f"{d['tokens'] / 1000:.1f}k" if d["tokens"] >= 1000 else f"{d['tokens']:.0f}"
            lines.append(f"| {d['fmt']} | {d['eff']:.2f} | {d['acc']:.1%} | {tok_display} | {d['og_cpt']:.1f} |")

        lines.append("")

    return lines


def _md_compression_section(compression_results) -> list[str]:
    """Generate markdown compression section."""
    lines = ["## Compression Benchmarks", ""]

    for fixture in compression_results.fixtures:
        lines.append(f"### {fixture.fixture_name}")
        lines.append("")

        # Get tokenizer names from first result
        first_result = fixture.results[0] if fixture.results else None
        tokenizers = list(first_result.tokens.keys()) if first_result else []

        header = "| Format | Chars |"
        sep = "|--------|-------|"
        for tok in tokenizers:
            header += f" {tok} |"
            sep += "------|"
        lines.append(header)
        lines.append(sep)

        for result in fixture.results:
            chars = result.chars
            row = f"| {result.format_name} | {chars:,} |" if chars else f"| {result.format_name} | N/A |"
            for tok in tokenizers:
                tok_count = result.tokens.get(tok)
                row += f" {tok_count:,} |" if tok_count else " N/A |"
            lines.append(row)

        lines.append("")

    return lines


def _md_llm_section(llm_results: list[tuple[str, dict]]) -> list[str]:
    """Generate markdown LLM accuracy section."""
    lines = ["## LLM Accuracy Benchmarks", ""]

    for _name, data in llm_results:
        meta = data["meta"]
        results = data["results"]

        lines.append(f"### {meta['model']} on {meta['data_file']}")
        lines.append("")
        lines.append(f"*{meta['n_queries']} queries, {meta['date'][:10]}*")
        lines.append("")
        lines.append("| Format | Accuracy | Tokens | Latency |")
        lines.append("|--------|----------|--------|---------|")

        for fmt, res in sorted(results.items(), key=lambda x: -x[1].get("accuracy", 0)):
            if res.get("total_queries", 0) == 0:
                continue
            acc = res.get("accuracy", 0)
            tokens = res.get("tokens", 0)
            latency = res.get("avg_latency_ms", 0)
            tok_display = f"{tokens / 1000:.1f}k" if tokens >= 1000 else f"{tokens}"
            lines.append(f"| {fmt} | {acc:.1%} | {tok_display} | {latency:.0f}ms |")

        lines.append("")

    return lines


if __name__ == "__main__":
    sys.exit(main())
