"""CLI entry point for benchmarks.

Usage:
    python -m benchmarks generate [--sizes 50,100,1000,5000] [--seed 42]
    python -m benchmarks compression
    python -m benchmarks llm --model MODEL [--endpoint URL] [--data FILE] [--queries N]
    python -m benchmarks report [--include-all]
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

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate HTML report")
    report_parser.add_argument("--include-all", action="store_true", help="Include all LLM results")
    report_parser.add_argument("--output", type=Path, help="Output path")

    args = parser.parse_args()

    if args.command == "generate":
        return cmd_generate(args)
    elif args.command == "compression":
        return cmd_compression(args)
    elif args.command == "llm":
        return asyncio.run(cmd_llm(args))
    elif args.command == "report":
        return cmd_report(args)

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
    """Generate HTML report for LLM results."""
    html = [
        "<!DOCTYPE html>",
        "<html><head>",
        "<meta charset='utf-8'>",
        "<title>LLM Accuracy Benchmarks</title>",
        "<style>",
        "body { font-family: system-ui, sans-serif; margin: 20px; max-width: 1200px; }",
        "h1 { color: #333; }",
        "h2 { color: #555; margin-top: 30px; }",
        ".meta { color: #666; background: #f9f9f9; padding: 12px; border-radius: 6px; margin: 10px 0; }",
        ".meta strong { color: #333; }",
        "table { border-collapse: collapse; margin: 20px 0; width: 100%; }",
        "th, td { border: 1px solid #ddd; padding: 10px 14px; text-align: right; }",
        "th { background: #f0f0f0; font-weight: 600; }",
        "td:first-child, th:first-child { text-align: left; }",
        ".best { font-weight: bold; color: #228855; background: #e8f5e9; }",
        ".worst { color: #c62828; background: #ffebee; }",
        ".tokens { color: #1565c0; }",
        ".chars { color: #7b1fa2; }",
        ".efficiency { color: #2e7d32; }",
        ".summary-box { background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 20px 0; }",
        ".summary-box h3 { margin: 0 0 10px 0; color: #1565c0; }",
        ".query-breakdown { margin-top: 20px; }",
        ".query-breakdown details { margin: 5px 0; }",
        ".query-breakdown summary { cursor: pointer; padding: 5px; background: #f5f5f5; border-radius: 4px; }",
        ".query-list { font-size: 13px; max-height: 300px; overflow-y: auto; }",
        ".query-item { padding: 8px; border-bottom: 1px solid #eee; }",
        ".query-item.correct { background: #e8f5e9; }",
        ".query-item.incorrect { background: #ffebee; }",
        ".query-q { font-weight: 500; }",
        ".query-expected { color: #2e7d32; }",
        ".query-actual { color: #c62828; }",
        "</style>",
        "</head><body>",
        "<h1>LLM Accuracy Benchmarks</h1>",
    ]

    for _name, data in all_results:
        meta = data["meta"]
        results = data["results"]

        html.append(f"<h2>{meta['model']}</h2>")
        html.append("<div class='meta'>")
        html.append(f"<strong>Dataset:</strong> {meta['data_file']} ({meta['data_size']:,} records)<br>")
        html.append(f"<strong>Queries:</strong> {meta['n_queries']}<br>")
        html.append(f"<strong>Date:</strong> {meta['date'][:10]}<br>")
        html.append(f"<strong>Endpoint:</strong> {meta['endpoint']}<br>")
        html.append(f"<strong>Seed:</strong> {meta['seed']}")
        html.append("</div>")

        # Find best/worst for highlighting
        valid_results = {k: v for k, v in results.items() if v.get("total_queries", 0) > 0}
        if valid_results:
            best_acc = max(r["accuracy"] for r in valid_results.values())
            worst_acc = min(r["accuracy"] for r in valid_results.values())
            min_tokens = min(r.get("tokens", float("inf")) for r in valid_results.values() if r.get("tokens"))
        else:
            best_acc = worst_acc = 0
            min_tokens = 0

        # Main results table
        html.append("<table>")
        html.append(
            "<tr><th>Format</th><th>Accuracy</th><th class='tokens'>Tokens</th>"
            "<th class='chars'>Chars</th><th class='efficiency'>Chars/Token</th>"
            "<th>Avg Latency</th><th>Queries</th></tr>"
        )

        for fmt, res in results.items():
            acc = res.get("accuracy", 0)
            tokens = res.get("tokens", 0)
            chars = res.get("chars", 0)
            latency = res.get("avg_latency_ms", 0)
            total = res.get("total_queries", 0)
            chars_per_tok = chars / tokens if tokens else 0

            # Determine row class
            acc_cls = ""
            if acc == best_acc and total > 0:
                acc_cls = " class='best'"
            elif acc == worst_acc and total > 0 and best_acc != worst_acc:
                acc_cls = " class='worst'"

            tok_cls = " class='best'" if tokens == min_tokens and tokens > 0 else ""

            html.append(
                f"<tr><td>{fmt}</td>"
                f"<td{acc_cls}>{acc:.1%}</td>"
                f"<td{tok_cls}>{tokens:,}</td>"
                f"<td>{chars:,}</td>"
                f"<td>{chars_per_tok:.2f}</td>"
                f"<td>{latency:.0f}ms</td>"
                f"<td>{total}</td></tr>"
            )

        html.append("</table>")

        # Summary box comparing minemizer variants
        minemizer_results = {k: v for k, v in results.items() if "minemizer" in k.lower()}
        json_results = {k: v for k, v in results.items() if "json" in k.lower()}

        if minemizer_results and json_results:
            html.append("<div class='summary-box'>")
            html.append("<h3>Minemizer vs JSON Comparison</h3>")

            # Get best minemizer and json_pretty for comparison
            best_mine = max(minemizer_results.items(), key=lambda x: x[1].get("accuracy", 0))
            json_pretty = json_results.get("json_pretty", list(json_results.values())[0] if json_results else {})

            mine_tok = best_mine[1].get("tokens", 0)
            json_tok = json_pretty.get("tokens", 0) if isinstance(json_pretty, dict) else 0
            token_savings = (1 - mine_tok / json_tok) * 100 if json_tok else 0

            mine_acc = best_mine[1].get("accuracy", 0)
            json_acc = json_pretty.get("accuracy", 0) if isinstance(json_pretty, dict) else 0
            acc_diff = (mine_acc - json_acc) * 100

            html.append(f"<p><strong>Best minemizer variant:</strong> {best_mine[0]}</p>")
            html.append(f"<p><strong>Token savings vs JSON:</strong> {token_savings:.1f}%</p>")
            html.append(f"<p><strong>Accuracy difference:</strong> {acc_diff:+.1f}%</p>")
            html.append("</div>")

        # Query breakdown per format (collapsible)
        html.append("<div class='query-breakdown'>")
        html.append("<h3>Query Details</h3>")

        for fmt, res in results.items():
            queries = res.get("queries", [])
            if not queries:
                continue

            correct_count = sum(1 for q in queries if q.get("correct"))
            html.append(f"<details><summary>{fmt}: {correct_count}/{len(queries)} correct</summary>")
            html.append("<div class='query-list'>")

            for q in queries:
                status_cls = "correct" if q.get("correct") else "incorrect"
                html.append(f"<div class='query-item {status_cls}'>")
                html.append(f"<div class='query-q'>Q: {q.get('question', '')}</div>")
                html.append(f"<div class='query-expected'>Expected: {q.get('expected', '')}</div>")
                html.append(f"<div class='query-actual'>Actual: {q.get('actual', '')}</div>")
                html.append("</div>")

            html.append("</div></details>")

        html.append("</div>")

    html.extend(["</body></html>"])
    return "\n".join(html)


if __name__ == "__main__":
    sys.exit(main())
