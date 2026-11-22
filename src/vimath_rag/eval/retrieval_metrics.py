"""Retrieval metrics (docs/EVALUATION.md, section 3). All functions score one question;
the evaluation script macro-averages them over questions.

``retrieved`` is a ranked list of chunk ids (best first); ``gold`` is the set of gold chunk ids.
"""

from collections.abc import Collection, Mapping, Sequence


def hit_at_k(retrieved: Sequence[str], gold: Collection[str], k: int) -> float:
    """1.0 if any gold chunk is in the top-k, else 0.0. TODO(M1)."""
    raise NotImplementedError("TODO(M1): hit_at_k")


def recall_at_k(retrieved: Sequence[str], gold: Collection[str], k: int) -> float:
    """Number of gold chunks in the top-k divided by the number of gold chunks. TODO(M1)."""
    raise NotImplementedError("TODO(M1): recall_at_k")


def mrr_at_k(retrieved: Sequence[str], gold: Collection[str], k: int = 10) -> float:
    """1 / rank of the first gold chunk within the top-k (1-based), 0.0 if none. TODO(M1)."""
    raise NotImplementedError("TODO(M1): mrr_at_k")


def ndcg_at_k(retrieved: Sequence[str], relevance: Mapping[str, int], k: int = 10) -> float:
    """nDCG@k with graded relevance (gold = 2, supporting = 1, else 0):
    ``DCG = sum_i (2**rel_i - 1) / log2(i + 1)`` over ranks i = 1..k, normalized by the ideal DCG.
    TODO(M1)."""
    raise NotImplementedError("TODO(M1): ndcg_at_k")


def unit_hit_at_k(retrieved: Sequence[str], gold_units: Collection[str], k: int) -> float:
    """1.0 if a top-k chunk belongs to a gold unit (right lesson, i.e. citation level). TODO(M1)."""
    raise NotImplementedError("TODO(M1): unit_hit_at_k")


def out_of_grade_at_k(retrieved_grades: Sequence[int], student_grade: int, k: int) -> float:
    """Share of top-k chunks whose grade is above the student's grade (measured before the grade
    filter, RQ3). TODO(M1)."""
    raise NotImplementedError("TODO(M1): out_of_grade_at_k")
