"""LLM accuracy benchmark runner."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from benchmarks import FIXTURES_DIR, RESULTS_DIR
from benchmarks.config import DEFAULT_CONCURRENCY, DEFAULT_LLM_ENDPOINT, DEFAULT_SEED
from benchmarks.core.formats import convert_to_format
from benchmarks.generators.synthetic import Query, generate_queries, get_oneshot_example
from benchmarks.llm.client import LLMClient


@dataclass
class QueryResult:
    """Result of a single query."""

    type: str
    question: str
    expected: str
    actual: str
    correct: bool
    latency_ms: float


@dataclass
class FormatResults:
    """Results for a single format."""

    format_name: str
    accuracy: float
    avg_latency_ms: float
    total_queries: int
    tokens: int = 0  # Token count for formatted data
    chars: int = 0  # Char count for formatted data
    queries: list[QueryResult] = field(default_factory=list)


@dataclass
class BenchmarkMeta:
    """Metadata for a benchmark run."""

    model: str
    endpoint: str
    date: str
    data_file: str
    data_size: int
    n_queries: int
    seed: int


@dataclass
class LLMBenchmarkResults:
    """Complete LLM benchmark results."""

    meta: BenchmarkMeta
    results: dict[str, FormatResults] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            "meta": asdict(self.meta),
            "results": {
                fmt: {
                    "accuracy": r.accuracy,
                    "avg_latency_ms": r.avg_latency_ms,
                    "total_queries": r.total_queries,
                    "tokens": r.tokens,
                    "chars": r.chars,
                    "queries": [asdict(q) for q in r.queries],
                }
                for fmt, r in self.results.items()
            },
        }


class LLMAccuracyBenchmark:
    """Runs LLM accuracy benchmarks across formats."""

    def __init__(
        self,
        model: str,
        endpoint: str = DEFAULT_LLM_ENDPOINT,
        api_key: str | None = None,
        concurrency: int = DEFAULT_CONCURRENCY,
        formats: list[str] | None = None,
        save_interval: int = 10,
        verbose: bool = True,
    ):
        """Initialize benchmark runner.

        Args:
            model: Model name for metadata.
            endpoint: LLM endpoint URL.
            api_key: Optional API key.
            concurrency: Max concurrent requests.
            formats: Formats to test. Defaults to subset suitable for LLM.
            save_interval: Save results every N queries.
            verbose: Print progress.
        """
        self.model = model
        self.endpoint = endpoint
        self.concurrency = concurrency
        self.formats = formats or ["json_pretty", "json_min", "yaml", "minemizer", "minemizer_compact"]
        self.save_interval = save_interval
        self.verbose = verbose

        self.client = LLMClient(
            endpoint=endpoint,
            api_key=api_key,
            concurrency=concurrency,
        )

    async def run(
        self,
        data: list[dict],
        n_queries: int,
        seed: int = DEFAULT_SEED,
        data_file: str = "unknown",
        output_path: Path | None = None,
    ) -> LLMBenchmarkResults:
        """Run benchmark on data.

        Args:
            data: The dataset to benchmark.
            n_queries: Number of queries per format.
            seed: Random seed for query generation.
            data_file: Name of data file for metadata.
            output_path: Path to save results. Auto-generated if None.

        Returns:
            Complete benchmark results.
        """
        # Generate queries (same for all formats)
        queries = generate_queries(data, n_queries, seed)

        # Initialize results
        results = LLMBenchmarkResults(
            meta=BenchmarkMeta(
                model=self.model,
                endpoint=self.endpoint,
                date=datetime.now(UTC).isoformat(),
                data_file=data_file,
                data_size=len(data),
                n_queries=n_queries,
                seed=seed,
            )
        )

        output_path = output_path or self._default_output_path()

        # Run each format sequentially (KV cache optimization)
        for fmt in self.formats:
            if self.verbose:
                print(f"\nBenchmarking {fmt}...")

            format_results = await self._run_format(data, fmt, queries, output_path, results)
            results.results[fmt] = format_results

            # Save after each format
            self._save_results(results, output_path)

        return results

    async def _run_format(
        self,
        data: list[dict],
        format_name: str,
        queries: list[Query],
        output_path: Path,
        results: LLMBenchmarkResults,
    ) -> FormatResults:
        """Run benchmark for a single format."""
        # Convert data to format
        formatted = convert_to_format(data, format_name)
        if formatted is None:
            return FormatResults(
                format_name=format_name,
                accuracy=0.0,
                avg_latency_ms=0.0,
                total_queries=0,
            )

        # Format data once for all queries
        formatted_data = formatted
        chars = len(formatted_data)
        tokens = 0  # Will be set from first API response

        query_results: list[QueryResult] = []

        # Process queries
        for i, query in enumerate(queries):
            prompt = self._build_prompt(formatted_data, query.question)
            result = await self.client.complete(prompt, max_tokens=128, temperature=0.0, stop=["END_RESPONSE"])

            # Capture tokens from first response (prompt tokens are ~same for all queries)
            if i == 0:
                tokens = result.tokens_prompt
                if self.verbose:
                    print(f"  ({tokens:,} tokens, {chars:,} chars)")

            # Normalize and compare
            actual = self._normalize_answer(result.text)
            expected = self._normalize_answer(query.answer)
            correct = actual == expected

            query_results.append(
                QueryResult(
                    type=query.type,
                    question=query.question,
                    expected=query.answer,
                    actual=result.text.strip(),
                    correct=correct,
                    latency_ms=result.latency_ms,
                )
            )

            completed = i + 1

            if self.verbose and completed % 10 == 0:
                acc = sum(1 for q in query_results if q.correct) / len(query_results)
                print(f"  {completed}/{len(queries)} queries, accuracy: {acc:.1%}")

            # Incremental save
            if completed % self.save_interval == 0:
                partial = FormatResults(
                    format_name=format_name,
                    accuracy=sum(1 for q in query_results if q.correct) / len(query_results),
                    avg_latency_ms=sum(q.latency_ms for q in query_results) / len(query_results),
                    total_queries=len(query_results),
                    queries=query_results.copy(),
                )
                results.results[format_name] = partial
                self._save_results(results, output_path)

        # Final results for format
        accuracy = sum(1 for q in query_results if q.correct) / len(query_results) if query_results else 0
        avg_latency = sum(q.latency_ms for q in query_results) / len(query_results) if query_results else 0

        if self.verbose:
            print(f"  Final: {accuracy:.1%} accuracy, {avg_latency:.0f}ms avg latency")

        return FormatResults(
            format_name=format_name,
            accuracy=accuracy,
            avg_latency_ms=avg_latency,
            total_queries=len(query_results),
            tokens=tokens,
            chars=chars,
            queries=query_results,
        )

    def _build_prompt(self, formatted_data: str, question: str) -> str:
        """Build full prompt with one-shot example."""
        example_q, example_a = get_oneshot_example()
        return f"""{formatted_data}
---
Answer the questions. Response must start with A: ANSWER END_RESPONSE
Q: {example_q}
A: {example_a} END_RESPONSE
Q: {question}
"""

    def _normalize_answer(self, text: str) -> str:
        """Normalize answer for comparison.

        Extracts answer from "A: ANSWER" format.
        """
        import re

        text = text.strip()

        # Look for "A: answer" pattern
        match = re.search(r"^A:\s*(.+?)(?:\s*END_RESPONSE)?$", text, re.IGNORECASE | re.DOTALL)
        if match:
            text = match.group(1).strip()

        # Clean up common artifacts
        text = text.strip("`\"'").strip()

        return text.lower().rstrip(".")

    def _default_output_path(self) -> Path:
        """Generate default output path."""
        output_dir = RESULTS_DIR / "llm_accuracy"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Sanitize model name for filename
        safe_model = self.model.replace("/", "_").replace(":", "_")
        date_str = datetime.now().strftime("%Y-%m-%d")
        return output_dir / f"{safe_model}_{date_str}.json"

    def _save_results(self, results: LLMBenchmarkResults, path: Path) -> None:
        """Save results to JSON."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(results.to_dict(), indent=2))


async def run_benchmark(
    data_file: str,
    model: str,
    n_queries: int,
    endpoint: str = DEFAULT_LLM_ENDPOINT,
    api_key: str | None = None,
    concurrency: int = DEFAULT_CONCURRENCY,
    seed: int = DEFAULT_SEED,
    formats: list[str] | None = None,
    verbose: bool = True,
) -> LLMBenchmarkResults:
    """Convenience function to run benchmark.

    Args:
        data_file: Name of data file (without path/extension).
        model: Model name.
        n_queries: Number of queries per format.
        endpoint: LLM endpoint URL.
        api_key: Optional API key.
        concurrency: Max concurrent requests.
        seed: Random seed.
        formats: Formats to test.
        verbose: Print progress.

    Returns:
        Benchmark results.
    """
    # Load data
    data_path = FIXTURES_DIR / "llm_accuracy" / f"{data_file}.json"
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")

    data = json.loads(data_path.read_text())

    # Run benchmark
    benchmark = LLMAccuracyBenchmark(
        model=model,
        endpoint=endpoint,
        api_key=api_key,
        concurrency=concurrency,
        formats=formats,
        verbose=verbose,
    )

    return await benchmark.run(data, n_queries, seed, data_file)
