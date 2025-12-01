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
        "body { font-family: system-ui, sans-serif; margin: 20px; }",
        "table { border-collapse: collapse; margin: 20px 0; }",
        "th, td { border: 1px solid #ddd; padding: 8px 12px; text-align: right; }",
        "th { background: #f0f0f0; }",
        "td:first-child { text-align: left; }",
        ".best { font-weight: bold; color: #228855; }",
        "</style>",
        "</head><body>",
        "<h1>LLM Accuracy Benchmarks</h1>",
    ]

    for _name, data in all_results:
        meta = data["meta"]
        results = data["results"]

        html.append(f"<h2>{meta['model']}</h2>")
        html.append(
            f"<p>Data: {meta['data_file']} ({meta['data_size']} records) | Queries: {meta['n_queries']} | Date: {meta['date'][:10]}</p>"  # noqa: E501
        )

        html.append("<table>")
        html.append("<tr><th>Format</th><th>Accuracy</th><th>Avg Latency</th></tr>")

        best_acc = max(r["accuracy"] for r in results.values())

        for fmt, res in results.items():
            cls = " class='best'" if res["accuracy"] == best_acc else ""
            html.append(
                f"<tr><td>{fmt}</td><td{cls}>{res['accuracy']:.1%}</td><td>{res['avg_latency_ms']:.0f}ms</td></tr>"
            )

        html.append("</table>")

    html.extend(["</body></html>"])
    return "\n".join(html)


if __name__ == "__main__":
    sys.exit(main())
