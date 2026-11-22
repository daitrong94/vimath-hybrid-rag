"""LLM-assisted extraction of KG candidates for manual curation.

For each lesson, an LLM (``configs/corpus.yaml: kg_build.extraction_llm``; Gemini free tier by
default) proposes concepts, aliases and prerequisite/related edges. Candidates are written to
``data/kg/candidates/{unit_id}.csv`` with ``status=candidate`` and **chunk ids as evidence, never
textbook text**. A human then accepts or edits them into ``data/kg/curated/``.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from vimath_rag.generation.llm import LLMClient
from vimath_rag.schemas import Chunk


@dataclass(frozen=True)
class ConceptCandidate:
    concept_id: str
    name: str
    kind: str
    aliases: tuple[str, ...]
    unit_id: str
    role: Literal["introduced", "used"]
    evidence_chunk_ids: tuple[str, ...]


@dataclass(frozen=True)
class EdgeCandidate:
    source: str
    target: str
    type: str
    evidence_chunk_ids: tuple[str, ...]
    rationale: str  # short, in the model's own words; never a textbook quote


def extract_lesson_candidates(
    unit_id: str,
    chunks: Sequence[Chunk],
    llm: LLMClient,
    *,
    known_concepts: Sequence[str] = (),
) -> tuple[list[ConceptCandidate], list[EdgeCandidate]]:
    """Ask the LLM for concepts and edges of one lesson, reusing ``known_concepts`` ids where
    possible. TODO(M3): JSON-mode prompt, validation, deduplication against the curated set."""
    raise NotImplementedError("TODO(M3): extract_lesson_candidates")


def write_candidates_csv(
    concepts: Sequence[ConceptCandidate],
    edges: Sequence[EdgeCandidate],
    out_dir: Path,
) -> None:
    """Write candidates to ``out_dir`` with ``status=candidate`` for curation. TODO(M3)."""
    raise NotImplementedError("TODO(M3): write_candidates_csv")
