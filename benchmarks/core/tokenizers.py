"""Tokenizer loading and token counting."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from benchmarks.config import TOKENIZERS

if TYPE_CHECKING:
    from transformers import PreTrainedTokenizerBase


def load_tokenizers(
    tokenizer_ids: dict[str, str] | None = None,
    verbose: bool = True,
) -> tuple[dict[str, PreTrainedTokenizerBase], float]:
    """Load tokenizers from HuggingFace.

    Args:
        tokenizer_ids: Map of name -> HuggingFace model ID. Defaults to TOKENIZERS.
        verbose: Print loading progress.

    Returns:
        Tuple of (tokenizers dict, total load time in seconds).
    """
    from transformers import AutoTokenizer

    tokenizer_ids = tokenizer_ids or TOKENIZERS

    if verbose:
        print("Loading tokenizers...")

    start = time.perf_counter()
    tokenizers = {}

    for name, model_id in tokenizer_ids.items():
        t0 = time.perf_counter()
        tokenizers[name] = AutoTokenizer.from_pretrained(model_id)
        if verbose:
            print(f"  {name}: {time.perf_counter() - t0:.2f}s")

    total = time.perf_counter() - start
    if verbose:
        print(f"  Total: {total:.2f}s\n")

    return tokenizers, total


def count_tokens(text: str, tokenizer: PreTrainedTokenizerBase) -> int:
    """Count tokens in text using the given tokenizer."""
    return len(tokenizer.encode(text))
