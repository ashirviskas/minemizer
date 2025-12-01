"""Compression benchmark runner."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from benchmarks.config import FORMATS
from benchmarks.core.formats import convert_to_format
from benchmarks.core.tokenizers import count_tokens

if TYPE_CHECKING:
    from transformers import PreTrainedTokenizerBase


@dataclass
class FormatResult:
    """Result for a single format conversion."""

    format_name: str
    chars: int | None
    tokens: dict[str, int | None]


@dataclass
class FixtureResult:
    """Results for a single fixture."""

    fixture_name: str
    results: list[FormatResult]


@dataclass
class BenchmarkResults:
    """Complete benchmark results."""

    fixtures: list[FixtureResult]
    timing: dict[str, float] = field(default_factory=dict)


class CompressionBenchmark:
    """Runs compression benchmarks across formats and tokenizers."""

    def __init__(
        self,
        formats: list[str] | None = None,
        verbose: bool = True,
    ):
        self.formats = formats or FORMATS
        self.verbose = verbose

    def run(
        self,
        fixtures: dict[str, list[dict]],
        tokenizers: dict[str, PreTrainedTokenizerBase],
    ) -> BenchmarkResults:
        """Run benchmarks on all fixtures.

        Args:
            fixtures: Dict mapping fixture names to data.
            tokenizers: Dict mapping tokenizer names to tokenizer instances.

        Returns:
            BenchmarkResults with all measurements.
        """
        results: list[FixtureResult] = []
        timing = {"total": 0.0, "conversion": 0.0, "tokenization": 0.0}

        total_start = time.perf_counter()

        for fixture_name, data in fixtures.items():
            fixture_result = self._benchmark_fixture(fixture_name, data, tokenizers, timing)
            results.append(fixture_result)

        timing["total"] = time.perf_counter() - total_start
        return BenchmarkResults(fixtures=results, timing=timing)

    def _benchmark_fixture(
        self,
        fixture_name: str,
        data: list[dict],
        tokenizers: dict[str, PreTrainedTokenizerBase],
        timing: dict[str, float],
    ) -> FixtureResult:
        """Benchmark a single fixture across all formats."""
        fixture_start = time.perf_counter()
        format_results: list[FormatResult] = []
        conv_time = 0.0
        tok_time = 0.0

        for format_name in self.formats:
            # Convert
            t0 = time.perf_counter()
            converted = convert_to_format(data, format_name)
            conv_time += time.perf_counter() - t0

            if converted is None:
                format_results.append(
                    FormatResult(
                        format_name=format_name,
                        chars=None,
                        tokens=dict.fromkeys(tokenizers),
                    )
                )
                continue

            # Tokenize
            t0 = time.perf_counter()
            tokens: dict[str, int | None] = {name: count_tokens(converted, tok) for name, tok in tokenizers.items()}
            tok_time += time.perf_counter() - t0

            format_results.append(
                FormatResult(
                    format_name=format_name,
                    chars=len(converted),
                    tokens=tokens,
                )
            )

        timing["conversion"] += conv_time
        timing["tokenization"] += tok_time

        if self.verbose:
            total = time.perf_counter() - fixture_start
            print(f"  {fixture_name}: {total:.2f}s (conv: {conv_time:.2f}s, tok: {tok_time:.2f}s)")

        return FixtureResult(fixture_name=fixture_name, results=format_results)
