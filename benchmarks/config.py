"""Benchmark configuration and constants."""

# Tokenizer models (all free, no auth required)
TOKENIZERS: dict[str, str] = {
    "gpt2": "openai-community/gpt2",
    "llama": "NousResearch/Llama-2-7b-hf",
    "qwen2.5": "Qwen/Qwen2.5-0.5B",
    "deepseek": "deepseek-ai/DeepSeek-V3",
    "devstral": "maxence-bouvier/Devstral-Small-2-24B-Instruct-SINQ-4bit",
}

# Output formats to benchmark
FORMATS = [
    "json_pretty",
    "json_min",
    "csv",
    "tsv",
    "yaml",
    "toon",
    "tson",
    "minemizer",
    "minemizer_compact",
]

FORMAT_LABELS = {
    "json_pretty": "JSON (pretty)",
    "json_min": "JSON (min)",
    "csv": "CSV",
    "tsv": "TSV",
    "yaml": "YAML",
    "toon": "TOON",
    "tson": "TSON",
    "minemizer": "minemizer",
    "minemizer_compact": "minemizer (compact)",
}

# Display settings
MAX_EXAMPLE_LINES = 25
MAX_EXAMPLE_CHARS = 5000
MAX_COPY_CHARS = 50000  # Limit for copyable data (50KB)

# Fixture display order
FIXTURE_ORDER = [
    "simple_flat",
    "nested_objects",
    "lists_of_primitives",
    "sparse_data",
    "complex_mixed",
]

# Short names for tables
SHORT_NAMES = {
    "simple_flat": "flat",
    "nested_objects": "nested",
    "lists_of_primitives": "lists",
    "sparse_data": "sparse",
    "complex_mixed": "complex",
    "large_non_uniform_nested_mixed": "large_mixed",
    "large_non_uniform_nested_numerical": "large_num",
    "large_non_uniform_nested_text": "large_text",
    "books": "books",
    "countries": "countries",
    "mcp_tools_list": "mcp_tools",
}

# LLM benchmark defaults
DEFAULT_LLM_ENDPOINT = "http://host.docker.internal:8080/v1"
DEFAULT_CONCURRENCY = 4
DEFAULT_SEED = 42
DATA_SIZES = [50, 100, 1000, 5000]
