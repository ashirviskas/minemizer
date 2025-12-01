"""Benchmark runners."""

from benchmarks.runners.compression import CompressionBenchmark
from benchmarks.runners.llm_accuracy import LLMAccuracyBenchmark

__all__ = ["CompressionBenchmark", "LLMAccuracyBenchmark"]
