"""Data contracts shared by every module (single source of truth for data formats).

- :class:`Chunk`: one retrievable unit of textbook content. Stored in ``data/processed/``
  (git-ignored, copyrighted text).
- :class:`GoldItem`: one golden-set question with its gold chunk ids. Stored in
  ``data/golden_set/`` (committed: questions + ids only).
- :class:`RetrievedChunk`, :class:`Source`, :class:`Usage`, :class:`AnswerResult`: API outputs.

Chunk ids follow ``g{grade}-{unit}-{type}-{nn}``, e.g. ``g8-b12-theorem-01`` (docs/DATA.md,
section 4.1). After changing :class:`GoldItem`, regenerate ``data/golden_set/schema.json`` with
``uv run python scripts/export_schemas.py``.
"""

import re
from collections.abc import Iterable
from enum import StrEnum
from pathlib import Path
from typing import Literal, Self, TypeVar

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

GRADES = (6, 7, 8, 9)


class ChunkType(StrEnum):
    """Kind of textbook block a chunk holds."""

    DEFINITION = "definition"  # định nghĩa, khái niệm
    THEOREM = "theorem"  # định lí, tính chất, quy tắc, hệ quả
    FORMULA = "formula"  # công thức
    EXAMPLE = "example"  # ví dụ kèm lời giải
    EXERCISE = "exercise"  # luyện tập, vận dụng, bài tập (no solution in the textbook)
    EXPLANATION = "explanation"  # expository text, activities (HĐ), remarks
    OTHER = "other"


class QuestionType(StrEnum):
    """Golden-set question types (docs/DATA.md, section 5.3)."""

    DEFINITION = "definition"
    FORMULA = "formula"
    PREREQUISITE = "prerequisite"
    APPLIED = "applied"


_TYPES = "|".join(t.value for t in ChunkType)
CHUNK_ID_RE = re.compile(
    rf"^(?P<unit>g[6-9](?:-[a-z0-9]+)+?)-(?P<type>{_TYPES})-(?P<ordinal>\d{{2,3}})$"
)
_GRADE_PREFIX_RE = re.compile(r"^g([6-9])-")


def parse_chunk_id(chunk_id: str) -> tuple[str, ChunkType, int]:
    """Split a chunk id into ``(unit_id, chunk_type, ordinal)``."""
    m = CHUNK_ID_RE.match(chunk_id)
    if m is None:
        raise ValueError(
            f"invalid chunk id {chunk_id!r}; expected g{{grade}}-{{unit}}-{{type}}-{{nn}}"
        )
    return m["unit"], ChunkType(m["type"]), int(m["ordinal"])


def make_chunk_id(unit_id: str, chunk_type: ChunkType | str, ordinal: int) -> str:
    """Build a chunk id, e.g. ``make_chunk_id("g8-b12", "theorem", 1) == "g8-b12-theorem-01"``."""
    if not 1 <= ordinal <= 999:
        raise ValueError(f"ordinal must be in 1..999, got {ordinal}")
    chunk_id = f"{unit_id}-{ChunkType(chunk_type).value}-{ordinal:02d}"
    parse_chunk_id(chunk_id)  # validates unit_id as well
    return chunk_id


def grade_of(unit_or_chunk_id: str) -> int:
    """Grade encoded in a unit id or chunk id (``"g8-b12-theorem-01"`` -> 8)."""
    m = _GRADE_PREFIX_RE.match(unit_or_chunk_id)
    if m is None:
        raise ValueError(f"no grade prefix in {unit_or_chunk_id!r}")
    return int(m[1])


class Chunk(BaseModel):
    """One retrievable unit of textbook content (docs/DATA.md, section 4)."""

    model_config = ConfigDict(extra="forbid")

    chunk_id: str
    grade: int = Field(ge=6, le=9)
    volume: int = Field(ge=1, le=2)
    unit_id: str = Field(
        description="Lesson-level unit, e.g. 'g8-b12'; also the KG lesson node id."
    )
    chapter: int | None = None
    chapter_title: str | None = None
    lesson: int | None = Field(default=None, description="None for non-lesson units.")
    lesson_title: str | None = None
    section: str | None = Field(default=None, description="Heading path inside the unit.")
    type: ChunkType
    label: str | None = Field(
        default=None, description="Visible label, e.g. 'Ví dụ 2', 'Bài 2.15'."
    )
    text: str = Field(description="Markdown with LaTeX ($...$). Copyrighted: never commit.")
    page_start: int = Field(ge=1, description="1-based PDF page index.")
    page_end: int = Field(ge=1)
    concepts: list[str] = Field(default_factory=list, description="Linked KG concept ids.")
    extraction: Literal["text_layer", "ocr"]
    source_file: str = Field(description="e.g. 'toan8_tap1.pdf'")
    corpus_version: str

    @model_validator(mode="after")
    def _check_consistency(self) -> Self:
        unit, chunk_type, _ = parse_chunk_id(self.chunk_id)
        if unit != self.unit_id:
            raise ValueError(f"chunk_id {self.chunk_id!r} does not belong to unit {self.unit_id!r}")
        if chunk_type != self.type:
            raise ValueError(f"chunk_id {self.chunk_id!r} does not match type {self.type!r}")
        if grade_of(self.unit_id) != self.grade:
            raise ValueError(f"unit {self.unit_id!r} does not match grade {self.grade}")
        if self.page_end < self.page_start:
            raise ValueError("page_end < page_start")
        return self


class GoldItem(BaseModel):
    """One golden-set question with gold chunk ids (docs/DATA.md, section 5)."""

    model_config = ConfigDict(extra="forbid")

    qid: str = Field(
        pattern=r"^(q\d{4}|ex-\d{3})$", description="'q0001'...; examples use 'ex-001'..."
    )
    question: str = Field(min_length=5, description="Written in the annotator's own words.")
    grade: int = Field(
        ge=6, le=9, description="Grade of the student asking; gold chunks must be <= it."
    )
    qtype: QuestionType
    gold_chunk_ids: list[str] = Field(
        min_length=1, description="Chunks that answer directly (relevance 2)."
    )
    supporting_chunk_ids: list[str] = Field(
        default_factory=list, description="Helpful but not sufficient (relevance 1)."
    )
    gold_concept_ids: list[str] = Field(
        default_factory=list, description="KG concept ids; required for prerequisite questions."
    )
    reference_answer: str | None = Field(default=None, description="Short answer, own words.")
    source: Literal["self", "dhmath", "synthetic"] = "self"
    split: Literal["dev", "test"]
    notes: str | None = None

    @field_validator("gold_chunk_ids", "supporting_chunk_ids")
    @classmethod
    def _valid_chunk_ids(cls, ids: list[str]) -> list[str]:
        for chunk_id in ids:
            parse_chunk_id(chunk_id)
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate chunk ids")
        return ids

    @model_validator(mode="after")
    def _check_consistency(self) -> Self:
        overlap = set(self.gold_chunk_ids) & set(self.supporting_chunk_ids)
        if overlap:
            raise ValueError(f"ids both gold and supporting: {sorted(overlap)}")
        all_ids = [*self.gold_chunk_ids, *self.supporting_chunk_ids]
        too_high = [c for c in all_ids if grade_of(c) > self.grade]
        if too_high:
            raise ValueError(f"chunks above the student's grade {self.grade}: {too_high}")
        if self.qtype == QuestionType.PREREQUISITE and not self.gold_concept_ids:
            raise ValueError("prerequisite questions need gold_concept_ids")
        return self

    @property
    def gold_unit_ids(self) -> list[str]:
        """Units (lessons) of the gold chunks, in order, for lesson-level metrics."""
        return list(dict.fromkeys(parse_chunk_id(c)[0] for c in self.gold_chunk_ids))

    def relevance(self) -> dict[str, int]:
        """Graded relevance for nDCG: gold = 2, supporting = 1."""
        return dict.fromkeys(self.supporting_chunk_ids, 1) | dict.fromkeys(self.gold_chunk_ids, 2)


class RetrievedChunk(BaseModel):
    """A ranked retrieval result."""

    chunk_id: str
    score: float
    rank: int = Field(ge=1)
    retriever: str = Field(description="'bm25', 'dense', 'graph', 'hybrid', 'hybrid_rerank'")
    chunk: Chunk | None = Field(default=None, description="Filled when the text is needed.")


class Source(BaseModel):
    """A citation shown to the student."""

    citation: str = Field(description="e.g. 'SGK Toán 8, Tập 1, Bài 12: <title>, tr. 45'")
    chunk_id: str
    grade: int
    unit_id: str
    page: int | None = Field(default=None, description="Printed page number, if known.")


class Usage(BaseModel):
    """Cost and latency of one API call."""

    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    latency_ms: dict[str, float] = Field(default_factory=dict, description="Per stage.")
    cached: bool = False


class AnswerResult(BaseModel):
    """Return value of :func:`vimath_rag.api.answer` (``.model_dump()`` gives a plain dict)."""

    answer: str
    sources: list[Source]
    retrieved_chunks: list[RetrievedChunk]
    method: str
    mode: Literal["answer", "hint"]
    grade: int | None
    usage: Usage = Field(default_factory=Usage)


ModelT = TypeVar("ModelT", bound=BaseModel)


def read_jsonl(path: str | Path, model: type[ModelT]) -> list[ModelT]:
    """Read a JSONL file into validated models; blank lines are skipped."""
    items: list[ModelT] = []
    with Path(path).open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                items.append(model.model_validate_json(line))
            except ValidationError as exc:
                raise ValueError(f"{path}:{lineno}: {exc}") from exc
    return items


def write_jsonl(path: str | Path, items: Iterable[BaseModel]) -> None:
    """Write models as UTF-8 JSONL (one object per line)."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="\n") as f:
        for item in items:
            f.write(item.model_dump_json() + "\n")


def load_golden_set(path: str | Path) -> list[GoldItem]:
    """Load and validate a golden-set JSONL file (unique qids)."""
    items = read_jsonl(path, GoldItem)
    seen: set[str] = set()
    for item in items:
        if item.qid in seen:
            raise ValueError(f"{path}: duplicate qid {item.qid!r}")
        seen.add(item.qid)
    return items
