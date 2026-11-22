"""Public Python API for the other AI-Tutor modules and the Gradio demo.

Example::

    from vimath_rag.api import answer

    result = answer("Định lí Pythagore phát biểu thế nào?", grade=8, method="hybrid_rerank")
    print(result.answer)
    for source in result.sources:
        print(source.citation)

``AnswerResult.model_dump()`` returns a plain dict with ``answer``, ``sources``,
``retrieved_chunks``, ``method``, ``mode``, ``grade`` and ``usage``.
"""

from typing import Literal

from vimath_rag.schemas import GRADES, AnswerResult, RetrievedChunk

Method = Literal["none", "bm25", "dense", "graph", "hybrid", "hybrid_rerank"]
Mode = Literal["answer", "hint"]


def _check_grade(grade: int | None) -> None:
    if grade is not None and grade not in GRADES:
        raise ValueError(f"grade must be one of {GRADES} or None, got {grade!r}")


def retrieve(
    question: str,
    grade: int | None = None,
    method: Method = "hybrid",
    k: int | None = None,
) -> list[RetrievedChunk]:
    """Return the top-k textbook chunks for ``question``.

    Args:
        question: Vietnamese question.
        grade: student's grade (6-9). Chunks above it are filtered out
            (``configs/retrievers.yaml: grade_filter``); ``None`` disables the filter.
        method: a method from ``configs/retrievers.yaml: methods`` (``"none"`` is not valid here).
        k: number of chunks; defaults to ``generation.context_k`` in ``configs/models.yaml``.
    """
    _check_grade(grade)
    # TODO(M2): build the configured retriever once (functools.cache) and call .retrieve().
    raise NotImplementedError("retrieve() is not implemented yet (docs/ROADMAP.md, M2)")


def answer(
    question: str,
    grade: int | None = None,
    method: Method = "hybrid",
    mode: Mode = "answer",
    k: int | None = None,
) -> AnswerResult:
    """Answer (``mode="answer"``) or give hints without the final answer (``mode="hint"``),
    grounded in retrieved textbook chunks and citing them as "SGK Toán 8, Bài X".

    ``method="none"`` is the closed-book baseline (LLM without retrieval).
    """
    _check_grade(grade)
    # TODO(M4): retrieve -> generation.prompts.build_messages -> cached, cost-tracked LLM call
    #           -> map [n] markers to Source citations -> AnswerResult.
    raise NotImplementedError("answer() is not implemented yet (docs/ROADMAP.md, M4)")
