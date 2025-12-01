"""Async LLM client for llama.cpp and OpenAI-compatible endpoints."""

from __future__ import annotations

import asyncio
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import httpx

from benchmarks.config import DEFAULT_CONCURRENCY, DEFAULT_LLM_ENDPOINT


@dataclass
class CompletionResult:
    """Result from a completion request."""

    text: str
    latency_ms: float
    tokens_prompt: int
    tokens_completion: int
    raw_response: dict[str, Any] | None = None


class LLMClient:
    """Async client for LLM completions.

    Compatible with llama.cpp server and OpenAI API.
    """

    def __init__(
        self,
        endpoint: str = DEFAULT_LLM_ENDPOINT,
        api_key: str | None = None,
        timeout: float = 600.0,  # 10 minutes for large contexts
        concurrency: int = DEFAULT_CONCURRENCY,
    ):
        """Initialize client.

        Args:
            endpoint: Base URL (e.g., http://localhost:8080/v1).
            api_key: Optional API key for authenticated endpoints.
            timeout: Request timeout in seconds.
            concurrency: Max concurrent requests.
        """
        self.endpoint = endpoint.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self._semaphore = asyncio.Semaphore(concurrency)

    async def complete(
        self,
        prompt: str,
        max_tokens: int = 64,
        temperature: float = 0.0,
        stop: list[str] | None = None,
    ) -> CompletionResult:
        """Send completion request.

        Args:
            prompt: The prompt text.
            max_tokens: Maximum tokens to generate.
            temperature: Sampling temperature (0 = deterministic).
            stop: Stop sequences.

        Returns:
            CompletionResult with generated text and metrics.
        """
        async with self._semaphore:
            return await self._do_complete(prompt, max_tokens, temperature, stop)

    async def _do_complete(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float,
        stop: list[str] | None,
    ) -> CompletionResult:
        """Internal completion logic using chat completions endpoint."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        # Use chat completions format
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if stop:
            payload["stop"] = stop

        start = time.perf_counter()

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.endpoint}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()

        latency = (time.perf_counter() - start) * 1000
        data = response.json()

        # Extract text from chat completion response
        # Handle both regular and reasoning models (DeepSeek, etc.)
        text = ""
        if "choices" in data and data["choices"]:
            choice = data["choices"][0]
            if "message" in choice:
                msg = choice["message"]
                # Try content first, fall back to reasoning_content for reasoning models
                text = msg.get("content") or msg.get("reasoning_content") or ""
            elif "text" in choice:
                text = choice["text"]

        usage = data.get("usage", {})

        return CompletionResult(
            text=text.strip(),
            latency_ms=latency,
            tokens_prompt=usage.get("prompt_tokens", 0),
            tokens_completion=usage.get("completion_tokens", 0),
            raw_response=data,
        )

    async def complete_batch(
        self,
        prompts: list[str],
        max_tokens: int = 64,
        temperature: float = 0.0,
        stop: list[str] | None = None,
        on_complete: Callable[[int, CompletionResult], None] | None = None,
    ) -> list[CompletionResult]:
        """Run multiple completions concurrently.

        Args:
            prompts: List of prompts.
            max_tokens: Max tokens per completion.
            temperature: Sampling temperature.
            stop: Stop sequences.
            on_complete: Optional callback(index, result) after each completion.

        Returns:
            List of results in same order as prompts.
        """

        async def run_one(idx: int, prompt: str) -> tuple[int, CompletionResult]:
            result = await self.complete(prompt, max_tokens, temperature, stop)
            if on_complete:
                on_complete(idx, result)
            return idx, result

        tasks = [run_one(i, p) for i, p in enumerate(prompts)]
        completed = await asyncio.gather(*tasks, return_exceptions=True)

        # Sort by index, handle exceptions
        results: list[CompletionResult] = [None] * len(prompts)  # type: ignore[list-item]
        for item in completed:
            if isinstance(item, BaseException):
                raise item
            idx, result = item
            results[idx] = result

        return results

    async def health_check(self) -> bool:
        """Check if endpoint is reachable."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # Try models endpoint, fall back to just checking connectivity
                response = await client.get(f"{self.endpoint}/models")
                return response.status_code in (200, 404)  # 404 OK - endpoint exists
        except Exception:
            return False
