"""Retriever interface and the grade filter shared by every retrieval method."""

from typing import Literal, Protocol, runtime_checkable

from vimath_rag.schemas import RetrievedChunk

GradeFilterMode = Literal["none", "le", "eq"]


@runtime_checkable
class Retriever(Protocol):
    """A retrieval method (BM25, dense, graph, hybrid)."""

    name: str

    def retrieve(self, query: str, k: int = 10, grade: int | None = None) -> list[RetrievedChunk]:
        """Return up to ``k`` chunks ranked by relevance, already filtered by ``grade``."""
        ...


def grade_allowed(
    chunk_grade: int, student_grade: int | None, mode: GradeFilterMode = "le"
) -> bool:
    """Whether a chunk may be used for a student (``configs/retrievers.yaml: grade_filter``).

    ``le`` (default): the student's grade or below; ``eq``: the same grade only;
    ``none`` or ``student_grade=None``: no filtering.
    """
    if student_grade is None or mode == "none":
        return True
    if mode == "le":
        return chunk_grade <= student_grade
    if mode == "eq":
        return chunk_grade == student_grade
    raise ValueError(f"unknown grade filter mode {mode!r}")
