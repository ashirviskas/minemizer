# Benchmarks

Two types of benchmarks for minemizer:

1. **Compression** - Token efficiency across formats and tokenizers
2. **LLM Accuracy** - How well LLMs retrieve data from different formats

## Quick Start

```bash
# Install dependencies
uv sync --group benchmark

# Run compression benchmarks
uv run python -m benchmarks compression

# Generate synthetic data + run LLM benchmarks
uv run python -m benchmarks generate --sizes 50,100,1000,5000
uv run python -m benchmarks llm --model "qwen2.5:7b" --data nested_1000 --queries 50
```

## CLI Commands

### Generate Synthetic Data

```bash
uv run python -m benchmarks generate [--sizes 50,100,1000,5000] [--seed 42]
```

Creates fictional address data in `fixtures/llm_accuracy/`. Data is synthetic to avoid LLM memorization.

### Compression Benchmarks

```bash
uv run python -m benchmarks compression [--no-readme]
```

Measures token counts across formats (JSON, YAML, CSV, minemizer, etc.) using multiple tokenizers (gpt2, llama, qwen, deepseek).

**Output:**
- `results/compression/benchmark_results.json`
- `results/compression/benchmark_tokens.html`
- Updates main README.md (unless `--no-readme`)

### LLM Accuracy Benchmarks

```bash
uv run python -m benchmarks llm \
    --model MODEL_NAME \
    --data DATA_FILE \
    --queries N \
    [--endpoint URL] \
    [--concurrency 4] \
    [--seed 42]
```

Tests how accurately LLMs can retrieve information from data formatted in different ways.

**Options:**
- `--model` - Model name for results file (e.g., "qwen2.5:7b")
- `--data` - Dataset name without extension (e.g., "nested_1000")
- `--queries` - Number of queries per format
- `--endpoint` - LLM API endpoint (default: `http://host.docker.internal:8080/v1`)
- `--concurrency` - Parallel requests (default: 4)
- `--seed` - Random seed for reproducible queries (default: 42)

**Output:**
- `results/llm_accuracy/{model}_{date}.json`

### Generate Report

```bash
uv run python -m benchmarks report [--include-all] [--output PATH]
```

Generates HTML report from LLM benchmark results.

## Directory Structure

```
benchmarks/
├── fixtures/
│   ├── compression/     # Real-world test data (books, countries, etc.)
│   └── llm_accuracy/    # Generated synthetic data
├── results/
│   ├── compression/     # Token efficiency results
│   └── llm_accuracy/    # LLM accuracy results
├── core/                # Tokenizers, formats, fixtures loading
├── generators/          # Synthetic data generation
├── llm/                 # Async LLM client
├── runners/             # Benchmark runners
└── output/              # HTML/Markdown generation
```

## Synthetic Data Schema

```json
{
  "id": "a7x9k2",
  "person": {
    "name": "Kira Voss",
    "age": 34
  },
  "address": {
    "street": "42 Thornwick Lane",
    "city": "Millbrook",
    "zip": "X7K-2M9",
    "country": "Valdoria"
  }
}
```

All names, cities, and countries are fictional to prevent LLM memorization.

## Query Types

| Type | Example |
|------|---------|
| `find_by_id` | "What is the city for person with id a7x9k2?" |
| `find_by_field` | "What is the id of the person who lives on 42 Thornwick Lane?" |
| `exists` | "Is there anyone living in Millbrook? Answer yes or no." |

## Example Results

```
Format            Accuracy    Avg Latency
─────────────────────────────────────────
json_pretty       100%        1644ms
json_min          100%        809ms
yaml              100%        999ms
minemizer         100%        605ms
minemizer_compact 100%        595ms
```

minemizer formats are ~2.8x faster than JSON pretty for LLM processing.
