"""Synthetic data generator for LLM accuracy benchmarks.

Generates fictional address data that LLMs cannot have memorized.
All names, cities, and countries are procedurally generated.
"""

from __future__ import annotations

import json
import random
import string
from dataclasses import dataclass
from pathlib import Path

from benchmarks import FIXTURES_DIR
from benchmarks.config import DATA_SIZES, DEFAULT_SEED

# Syllables for generating fictional names
_FIRST_SYLLABLES = ["Ka", "Mi", "Lo", "Zu", "Ve", "Tha", "Ry", "Xa", "Jo", "Eli", "Nu", "Sa", "Ti", "Fe", "Bri"]
_LAST_SYLLABLES = ["ra", "vin", "lex", "dor", "nis", "ven", "mon", "kas", "zel", "ron", "lix", "mar", "tos", "wen"]

_CITY_PARTS = ["Brix", "Mond", "Kelt", "Zara", "Vorn", "Plex", "Asha", "Torn", "Mira", "Dusk", "Glen", "Crest"]
_CITY_SUFFIXES = ["vale", "burg", "ton", "wick", "ford", "haven", "more", "dale", "port", "hill"]

_COUNTRY_PARTS = ["Vor", "Kel", "Zan", "Myr", "Thel", "Ax", "Dra", "Vel", "Lor", "Sar"]
_COUNTRY_SUFFIXES = ["doria", "land", "stan", "via", "mark", "heim", "nia", "gard", "reich"]

_STREET_TYPES = ["Street", "Lane", "Road", "Avenue", "Way", "Drive", "Place", "Court"]
_STREET_NAMES = ["Ember", "Crystal", "Shadow", "Silver", "Golden", "Iron", "Stone", "Oak", "Willow", "Cedar"]


@dataclass
class Query:
    """A single query with expected answer."""

    type: str
    question: str
    answer: str


def generate_dataset(
    size: int,
    seed: int = DEFAULT_SEED,
) -> list[dict]:
    """Generate synthetic address dataset.

    Args:
        size: Number of records to generate.
        seed: Random seed for reproducibility.

    Returns:
        List of address records.
    """
    rng = random.Random(seed)
    records = []

    for _ in range(size):
        record = {
            "id": _random_id(rng),
            "person": {
                "name": _random_name(rng),
                "age": rng.randint(18, 85),
            },
            "address": {
                "street": _random_street(rng),
                "city": _random_city(rng),
                "zip": _random_zip(rng),
                "country": _random_country(rng),
            },
        }
        records.append(record)

    return records


def generate_queries(
    data: list[dict],
    n_queries: int,
    seed: int = DEFAULT_SEED,
) -> list[Query]:
    """Generate queries for the dataset.

    Queries are deterministic given the same data and seed.
    Distributes queries evenly across types: find_by_id, find_by_field, exists.

    Args:
        data: The dataset to query.
        n_queries: Number of queries to generate.
        seed: Random seed for reproducibility.

    Returns:
        List of Query objects.
    """
    rng = random.Random(seed)
    queries: list[Query] = []

    query_types = ["find_by_id", "find_by_field", "exists"]
    per_type = n_queries // len(query_types)
    remainder = n_queries % len(query_types)

    for i, qtype in enumerate(query_types):
        count = per_type + (1 if i < remainder else 0)
        for _ in range(count):
            record = rng.choice(data)
            query = _make_query(record, qtype, data, rng)
            queries.append(query)

    rng.shuffle(queries)
    return queries


def save_dataset(
    size: int,
    seed: int = DEFAULT_SEED,
    output_dir: Path | None = None,
) -> Path:
    """Generate and save dataset to fixtures directory.

    Args:
        size: Number of records.
        seed: Random seed.
        output_dir: Output directory. Defaults to fixtures/llm_accuracy/.

    Returns:
        Path to saved file.
    """
    output_dir = output_dir or FIXTURES_DIR / "llm_accuracy"
    output_dir.mkdir(parents=True, exist_ok=True)

    data = generate_dataset(size, seed)
    path = output_dir / f"nested_{size}.json"
    path.write_text(json.dumps(data, indent=2))

    return path


def generate_all_datasets(
    sizes: list[int] | None = None,
    seed: int = DEFAULT_SEED,
) -> list[Path]:
    """Generate all standard dataset sizes.

    Args:
        sizes: List of sizes. Defaults to DATA_SIZES.
        seed: Random seed.

    Returns:
        List of paths to saved files.
    """
    sizes = sizes or DATA_SIZES
    return [save_dataset(size, seed) for size in sizes]


# --- Private helpers ---


def _random_id(rng: random.Random) -> str:
    """Generate 6-char alphanumeric ID."""
    chars = string.ascii_lowercase + string.digits
    return "".join(rng.choices(chars, k=6))


def _random_name(rng: random.Random) -> str:
    """Generate fictional person name."""
    first = rng.choice(_FIRST_SYLLABLES) + rng.choice(_LAST_SYLLABLES)
    last = rng.choice(_FIRST_SYLLABLES) + rng.choice(_LAST_SYLLABLES)
    return f"{first} {last}"


def _random_street(rng: random.Random) -> str:
    """Generate fictional street address."""
    number = rng.randint(1, 999)
    name = rng.choice(_STREET_NAMES)
    stype = rng.choice(_STREET_TYPES)
    return f"{number} {name} {stype}"


def _random_city(rng: random.Random) -> str:
    """Generate fictional city name."""
    return rng.choice(_CITY_PARTS) + rng.choice(_CITY_SUFFIXES)


def _random_zip(rng: random.Random) -> str:
    """Generate fictional zip code."""
    letters = "".join(rng.choices(string.ascii_uppercase, k=2))
    numbers = "".join(rng.choices(string.digits, k=3))
    return f"{letters}{numbers}"


def _random_country(rng: random.Random) -> str:
    """Generate fictional country name."""
    return rng.choice(_COUNTRY_PARTS) + rng.choice(_COUNTRY_SUFFIXES)


def _make_query(
    record: dict,
    qtype: str,
    all_data: list[dict],
    rng: random.Random,
) -> Query:
    """Create a single query for a record."""
    if qtype == "find_by_id":
        # Ask about a field given the ID
        field = rng.choice(["city", "zip", "country"])
        answer = record["address"][field]
        question = f"What is the {field} for person with id {record['id']}?"
        return Query(type=qtype, question=question, answer=str(answer))

    elif qtype == "find_by_field":
        # Ask for ID given a unique field value
        street = record["address"]["street"]
        question = f"What is the id of the person who lives on {street}?"
        return Query(type=qtype, question=question, answer=record["id"])

    else:  # exists
        # Ask if someone lives in a city (always pick existing)
        city = record["address"]["city"]
        question = f"Is there anyone living in {city}? Answer yes or no."
        return Query(type=qtype, question=question, answer="yes")


def get_oneshot_example() -> tuple[str, str]:
    """Get the one-shot example for prompts.

    Returns nonsense data that won't appear in any generated dataset.
    """
    question = "What is the id of the person who lives on 12 Jumberbobr Street?"
    answer = "x9q7m2"
    return question, answer


# --- Flat data generator ---

_DEPARTMENTS = ["Engineering", "Sales", "Marketing", "Finance", "HR", "Operations", "Legal", "Support"]
_STATUSES = ["active", "inactive", "pending", "suspended"]
_LEVELS = ["junior", "mid", "senior", "lead", "principal"]


def generate_flat_dataset(
    size: int,
    seed: int = DEFAULT_SEED,
) -> list[dict]:
    """Generate flat dataset with 7+ columns, no nesting.

    Args:
        size: Number of records to generate.
        seed: Random seed for reproducibility.

    Returns:
        List of flat records.
    """
    rng = random.Random(seed)
    records = []

    for _ in range(size):
        record = {
            "id": _random_id(rng),
            "name": _random_name(rng),
            "email": _random_email(rng),
            "department": rng.choice(_DEPARTMENTS),
            "level": rng.choice(_LEVELS),
            "salary": rng.randint(30000, 200000),
            "status": rng.choice(_STATUSES),
            "years_employed": rng.randint(0, 25),
        }
        records.append(record)

    return records


def _random_email(rng: random.Random) -> str:
    """Generate fictional email."""
    user = _random_id(rng)
    domains = ["acme.co", "globex.io", "initech.net", "umbrella.org", "stark.dev"]
    return f"{user}@{rng.choice(domains)}"


def save_flat_dataset(
    size: int,
    seed: int = DEFAULT_SEED,
    output_dir: Path | None = None,
) -> Path:
    """Generate and save flat dataset."""
    output_dir = output_dir or FIXTURES_DIR / "llm_accuracy"
    output_dir.mkdir(parents=True, exist_ok=True)

    data = generate_flat_dataset(size, seed)
    path = output_dir / f"flat_{size}.json"
    path.write_text(json.dumps(data, indent=2))

    return path


def generate_flat_queries(
    data: list[dict],
    n_queries: int,
    seed: int = DEFAULT_SEED,
) -> list[Query]:
    """Generate queries for flat dataset."""
    rng = random.Random(seed)
    queries: list[Query] = []

    query_types = ["find_by_id", "find_by_field", "exists"]
    per_type = n_queries // len(query_types)
    remainder = n_queries % len(query_types)

    for i, qtype in enumerate(query_types):
        count = per_type + (1 if i < remainder else 0)
        for _ in range(count):
            record = rng.choice(data)
            query = _make_flat_query(record, qtype, data, rng)
            queries.append(query)

    rng.shuffle(queries)
    return queries


def _make_flat_query(
    record: dict,
    qtype: str,
    all_data: list[dict],
    rng: random.Random,
) -> Query:
    """Create a single query for flat record."""
    if qtype == "find_by_id":
        field = rng.choice(["department", "level", "status", "salary"])
        answer = record[field]
        question = f"What is the {field} for person with id {record['id']}?"
        return Query(type=qtype, question=question, answer=str(answer))

    elif qtype == "find_by_field":
        email = record["email"]
        question = f"What is the id of the person with email {email}?"
        return Query(type=qtype, question=question, answer=record["id"])

    else:  # exists
        dept = record["department"]
        question = f"Is there anyone in the {dept} department? Answer yes or no."
        return Query(type=qtype, question=question, answer="yes")


# --- Sparse nested data generator ---

_SKILLS = ["Python", "JavaScript", "Go", "Rust", "Java", "C++", "TypeScript", "Ruby", "Kotlin", "Swift"]
_CERTIFICATIONS = ["AWS", "GCP", "Azure", "K8s", "Docker", "Terraform", "PMP", "Scrum", "CISSP", "CKA"]
_HOBBIES = ["photography", "hiking", "gaming", "reading", "cooking", "music", "travel", "sports", "art", "writing"]
_LANGUAGES = [
    "English",
    "Spanish",
    "Mandarin",
    "French",
    "German",
    "Japanese",
    "Portuguese",
    "Korean",
    "Arabic",
    "Hindi",
]


def generate_sparse_dataset(
    size: int,
    seed: int = DEFAULT_SEED,
) -> list[dict]:
    """Generate sparse nested dataset.

    Most optional fields have ~0.7 sparsity (30% present),
    some have ~0.3 sparsity (70% present).

    Args:
        size: Number of records to generate.
        seed: Random seed for reproducibility.

    Returns:
        List of sparse nested records.
    """
    rng = random.Random(seed)
    records = []

    for _ in range(size):
        record = {
            "id": _random_id(rng),
            "name": _random_name(rng),
            "contact": {
                "email": _random_email(rng),  # always present
            },
            "employment": {
                "department": rng.choice(_DEPARTMENTS),  # always present
                "level": rng.choice(_LEVELS),  # always present
            },
        }

        # ~0.3 sparsity (70% present) - more common fields
        if rng.random() > 0.3:
            record["contact"]["phone"] = _random_phone(rng)
        if rng.random() > 0.3:
            record["employment"]["salary"] = rng.randint(30000, 200000)
        if rng.random() > 0.3:
            record["employment"]["years"] = rng.randint(0, 25)

        # ~0.7 sparsity (30% present) - rare fields
        if rng.random() > 0.7:
            record["contact"]["address"] = {
                "city": _random_city(rng),
                "country": _random_country(rng),
            }
        if rng.random() > 0.7:
            record["skills"] = rng.sample(_SKILLS, k=rng.randint(1, 4))
        if rng.random() > 0.7:
            record["certifications"] = rng.sample(_CERTIFICATIONS, k=rng.randint(1, 3))
        if rng.random() > 0.7:
            record["languages"] = rng.sample(_LANGUAGES, k=rng.randint(1, 3))
        if rng.random() > 0.7:
            record["hobbies"] = rng.sample(_HOBBIES, k=rng.randint(1, 3))
        if rng.random() > 0.7:
            record["metadata"] = {
                "created": f"2024-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}",
                "source": rng.choice(["manual", "import", "api", "migration"]),
            }

        records.append(record)

    return records


def _random_phone(rng: random.Random) -> str:
    """Generate fictional phone number."""
    return f"+1-{rng.randint(200, 999)}-{rng.randint(100, 999)}-{rng.randint(1000, 9999)}"


def save_sparse_dataset(
    size: int,
    seed: int = DEFAULT_SEED,
    output_dir: Path | None = None,
) -> Path:
    """Generate and save sparse dataset."""
    output_dir = output_dir or FIXTURES_DIR / "llm_accuracy"
    output_dir.mkdir(parents=True, exist_ok=True)

    data = generate_sparse_dataset(size, seed)
    path = output_dir / f"sparse_{size}.json"
    path.write_text(json.dumps(data, indent=2))

    return path


def generate_sparse_queries(
    data: list[dict],
    n_queries: int,
    seed: int = DEFAULT_SEED,
) -> list[Query]:
    """Generate queries for sparse dataset."""
    rng = random.Random(seed)
    queries: list[Query] = []

    query_types = ["find_by_id", "find_by_field", "exists"]
    per_type = n_queries // len(query_types)
    remainder = n_queries % len(query_types)

    for i, qtype in enumerate(query_types):
        count = per_type + (1 if i < remainder else 0)
        for _ in range(count):
            record = rng.choice(data)
            query = _make_sparse_query(record, qtype, data, rng)
            queries.append(query)

    rng.shuffle(queries)
    return queries


def _make_sparse_query(
    record: dict,
    qtype: str,
    all_data: list[dict],
    rng: random.Random,
) -> Query:
    """Create a single query for sparse record."""
    if qtype == "find_by_id":
        # Query fields that are always present
        field = rng.choice(["department", "level"])
        answer = record["employment"][field]
        question = f"What is the {field} for person with id {record['id']}?"
        return Query(type=qtype, question=question, answer=str(answer))

    elif qtype == "find_by_field":
        email = record["contact"]["email"]
        question = f"What is the id of the person with email {email}?"
        return Query(type=qtype, question=question, answer=record["id"])

    else:  # exists
        dept = record["employment"]["department"]
        question = f"Is there anyone in the {dept} department? Answer yes or no."
        return Query(type=qtype, question=question, answer="yes")
