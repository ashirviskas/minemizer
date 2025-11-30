#!/usr/bin/env python3
"""Generate example files for minemizer."""

import json
from dataclasses import dataclass, field
from pathlib import Path

from minemizer import minemize, presets
from minemizer.config import Config

EXAMPLES_DIR = Path(__file__).parent.parent / "examples"


@dataclass
class Example:
    name: str
    description: str
    data: list[dict]
    preset: Config | None = None
    options: dict = field(default_factory=dict)
    preset_name: str | None = None  # for display


EXAMPLES = [
    Example(
        name="uniform",
        description="All keys present in all items - clean tabular data (default preset)",
        data=[
            {"id": 101, "name": "Yuki Tanaka", "age": 29, "city": "Tokyo"},
            {"id": 102, "name": "Priya Sharma", "age": 34, "city": "Mumbai"},
            {"id": 103, "name": "Lucas Silva", "age": 27, "city": "São Paulo"},
            {"id": 104, "name": "Emma Nielsen", "age": 31, "city": "Copenhagen"},
        ],
        preset=presets.default,
        preset_name="presets.default",
    ),
    Example(
        name="non_uniform",
        description="Sparse keys - some fields only present in some items",
        data=[
            {"id": 1, "name": "Kenji Watanabe", "department": "Engineering"},
            {"id": 2, "name": "Sofia Rodriguez", "department": "Design", "remote": True},
            {"id": 3, "name": "Ahmed Hassan"},
            {"id": 4, "name": "Ingrid Larsson", "department": "Sales", "slack": "@ingrid"},
        ],
        options={"threshold": 0.5},
    ),
    Example(
        name="nested",
        description="Nested structures - dicts and lists within items",
        data=[
            {
                "id": "u1",
                "name": "Chen Wei",
                "location": {"office": "Shanghai HQ", "floor": 12},
                "skills": ["python", "kubernetes"],
            },
            {
                "id": "u2",
                "name": "Fatima Al-Rashid",
                "location": {"office": "Dubai Tech Park", "floor": 7},
                "skills": ["react", "typescript", "graphql"],
            },
            {
                "id": "u3",
                "name": "Oluwaseun Adeyemi",
                "location": {"office": "Lagos Hub", "floor": 3},
                "skills": ["rust"],
            },
        ],
    ),
    Example(
        name="csv_style",
        description="CSV preset - standard comma-separated values",
        data=[
            {"sku": "KB-2847", "item": "Mechanical Keyboard", "price": 149.99, "stock": 45},
            {"sku": "MS-1122", "item": "Ergonomic Mouse", "price": 79.50, "stock": 120},
            {"sku": "HC-9931", "item": "USB-C Hub 7-port", "price": 59.99, "stock": 67},
        ],
        preset=presets.csv,
        preset_name="presets.csv",
    ),
    Example(
        name="markdown_table",
        description="Markdown preset - renders as proper table in markdown viewers",
        data=[
            {"project": "Phoenix", "status": "Active", "lead": "Maria Santos"},
            {"project": "Titan", "status": "Planning", "lead": "James Okonkwo"},
            {"project": "Nebula", "status": "Complete", "lead": "Anika Patel"},
        ],
        preset=presets.markdown,
        preset_name="presets.markdown",
    ),
]


def format_call(example: Example) -> str:
    """Format the minemize call as Python code."""
    parts = ["minemize(data"]

    if example.preset_name:
        parts.append(f", preset={example.preset_name}")

    if example.options:
        opts = ", ".join(f"{k}={v!r}" for k, v in example.options.items())
        parts.append(f", {opts}")

    parts.append(")")
    return "".join(parts)


def generate_markdown_output(example: Example, output: str) -> str:
    """Generate markdown file content with metadata."""
    json_str = json.dumps(example.data, indent=2)

    lines = [
        f"# {example.name}",
        "",
        example.description,
        "",
        "## Input (JSON)",
        "",
        "```json",
        json_str,
        "```",
        "",
        "## Options",
        "",
        "```python",
        format_call(example),
        "```",
        "",
        "## Output",
        "",
    ]

    # For markdown preset, show both raw and rendered
    is_markdown = example.preset_name == "presets.markdown"
    if is_markdown:
        lines.extend(
            [
                "### Raw",
                "",
                "```",
                output,
                "```",
                "",
                "### Rendered",
                "",
                output,
                "",
            ]
        )
    else:
        lines.extend(
            [
                "```",
                output,
                "```",
                "",
            ]
        )

    return "\n".join(lines)


def generate_example(example: Example) -> None:
    """Generate files for a single example."""
    example_dir = EXAMPLES_DIR / example.name
    example_dir.mkdir(parents=True, exist_ok=True)

    # Generate JSON input
    json_path = example_dir / f"{example.name}.json"
    json_path.write_text(json.dumps(example.data, indent=2) + "\n")

    # Generate minemized output
    output = minemize(example.data, preset=example.preset, **example.options)

    # Generate markdown file with metadata
    md_path = example_dir / f"{example.name}_minemized.md"
    md_content = generate_markdown_output(example, output)
    md_path.write_text(md_content)

    print(f"Generated: {example.name}")
    print(f"  - {json_path.relative_to(EXAMPLES_DIR.parent)}")
    print(f"  - {md_path.relative_to(EXAMPLES_DIR.parent)}")


def main() -> None:
    """Generate all examples."""
    print("Generating examples...\n")

    for example in EXAMPLES:
        generate_example(example)

    print(f"\nGenerated {len(EXAMPLES)} examples in {EXAMPLES_DIR}")


if __name__ == "__main__":
    main()
