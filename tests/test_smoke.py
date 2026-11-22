"""Smoke tests: the package imports, configs parse, and the committed example data match
their schemas. Real unit tests are added with each implemented module."""

import json
from pathlib import Path

import networkx as nx
import pytest
from pydantic import ValidationError

import vimath_rag
from vimath_rag.config import CONFIG_DIR, PROJECT_ROOT, load_config
from vimath_rag.kg.build import load_graph
from vimath_rag.kg.schema import KGValidationError, load_kg_schema, validate_graph
from vimath_rag.schemas import GoldItem, load_golden_set, make_chunk_id, parse_chunk_id

GOLDEN_DIR = PROJECT_ROOT / "data" / "golden_set"
KG_DIR = PROJECT_ROOT / "data" / "kg"


def test_package_has_version() -> None:
    assert vimath_rag.__version__


@pytest.mark.parametrize("path", sorted(CONFIG_DIR.glob("*.yaml")), ids=lambda p: p.name)
def test_config_parses(path: Path) -> None:
    assert load_config(path)


def test_golden_examples_validate() -> None:
    items = load_golden_set(GOLDEN_DIR / "examples.jsonl")
    assert len(items) == 3
    assert {item.source for item in items} == {"synthetic"}


def test_golden_schema_json_matches_model() -> None:
    committed = json.loads((GOLDEN_DIR / "schema.json").read_text(encoding="utf-8"))
    assert committed == GoldItem.model_json_schema(), "run: uv run python scripts/export_schemas.py"


def test_gold_item_rejects_chunk_above_student_grade() -> None:
    with pytest.raises(ValidationError, match="above the student's grade"):
        GoldItem(
            qid="q0001",
            question="Câu hỏi thử nghiệm?",
            grade=7,
            qtype="definition",
            gold_chunk_ids=["g8-b01-definition-01"],
            split="dev",
        )


def test_chunk_id_roundtrip() -> None:
    chunk_id = make_chunk_id("g6-c02-ltc1", "exercise", 3)
    assert chunk_id == "g6-c02-ltc1-exercise-03"
    assert parse_chunk_id(chunk_id) == ("g6-c02-ltc1", "exercise", 3)


def test_example_kg_validates() -> None:
    schema = load_kg_schema(KG_DIR / "schema.yaml")
    graph = load_graph(KG_DIR / "example_graph.json")
    validate_graph(graph, schema)
    assert graph.number_of_nodes() > 0


def test_kg_validation_rejects_prerequisite_cycle() -> None:
    schema = load_kg_schema(KG_DIR / "schema.yaml")
    graph = nx.MultiDiGraph()
    for node in ("a", "b"):
        graph.add_node(node, type="concept", name=node, kind="concept", grade_introduced=6)
    graph.add_edge("a", "b", key="prerequisite_of", type="prerequisite_of")
    graph.add_edge("b", "a", key="prerequisite_of", type="prerequisite_of")
    with pytest.raises(KGValidationError, match="cycle"):
        validate_graph(graph, schema)
