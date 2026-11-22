"""Generation metrics with an LLM judge (docs/EVALUATION.md, section 4).

The judge model comes from a different family than the generator
(``configs/models.yaml: llm.judge``), runs at temperature 0 with Vietnamese rubrics, and is
calibrated against 30 hand-scored dev answers before it is used on the test split.
RAGAS may be used as a cross-check but is not the primary metric.
"""

from collections.abc import Collection, Sequence
from dataclasses import dataclass

from vimath_rag.generation.llm import LLMClient


@dataclass(frozen=True)
class JudgeResult:
    score: float  # normalized to [0, 1]
    rationale: str
    raw: str  # raw judge output, kept for auditing (local run outputs only)


def faithfulness(
    question: str, answer: str, contexts: Sequence[str], judge: LLMClient
) -> JudgeResult:
    """Share of the answer's claims supported by ``contexts`` (claim split + per-claim check).
    TODO(M5)."""
    raise NotImplementedError("TODO(M5): faithfulness")


def answer_relevance(question: str, answer: str, judge: LLMClient) -> JudgeResult:
    """How directly the answer addresses the question (1-5 rubric, normalized). TODO(M5)."""
    raise NotImplementedError("TODO(M5): answer_relevance")


def correctness(question: str, answer: str, reference_answer: str, judge: LLMClient) -> JudgeResult:
    """Agreement with the annotator's reference answer (definition/formula questions). TODO(M5)."""
    raise NotImplementedError("TODO(M5): correctness")


def citation_accuracy(cited_unit_ids: Sequence[str], gold_unit_ids: Collection[str]) -> float:
    """Share of citations that point to a gold unit (lesson); 0.0 when nothing is cited. TODO(M5)."""
    raise NotImplementedError("TODO(M5): citation_accuracy")
