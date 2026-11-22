"""Hybrid retrieval: Reciprocal Rank Fusion of several retrievers + optional reranking."""

from collections.abc import Mapping, Sequence

from vimath_rag.retrievers.base import Retriever
from vimath_rag.retrievers.reranker import CrossEncoderReranker
from vimath_rag.schemas import RetrievedChunk


def reciprocal_rank_fusion(
    rankings: Mapping[str, Sequence[str]],
    *,
    k: int = 60,
    weights: Mapping[str, float] | None = None,
) -> list[tuple[str, float]]:
    """Fuse ranked chunk-id lists (Cormack et al., 2009).

    ``score(d) = sum_r w_r / (k + rank_r(d))`` with 1-based ranks; a list that does not contain
    ``d`` contributes nothing. Returns ``(chunk_id, score)`` sorted by score descending, ties
    broken by best individual rank, then by chunk id.

    TODO(M4): implement, with a unit test on a hand-computed example.
    """
    raise NotImplementedError("TODO(M4): reciprocal_rank_fusion")


class HybridRetriever:
    """RRF over component retrievers (each already grade-filtered), then optional reranking."""

    def __init__(
        self,
        retrievers: Sequence[Retriever],
        *,
        rrf_k: int = 60,
        weights: Mapping[str, float] | None = None,
        candidate_k: int = 50,
        reranker: CrossEncoderReranker | None = None,
        rerank_top_n: int = 20,
    ) -> None:
        self.retrievers = list(retrievers)
        self.rrf_k = rrf_k
        self.weights = dict(weights or {})
        self.candidate_k = candidate_k
        self.reranker = reranker
        self.rerank_top_n = rerank_top_n
        self.name = "hybrid_rerank" if reranker is not None else "hybrid"

    def retrieve(self, query: str, k: int = 10, grade: int | None = None) -> list[RetrievedChunk]:
        """Each component returns ``candidate_k`` chunks -> RRF -> optional rerank -> top-k. TODO(M4)."""
        raise NotImplementedError("TODO(M4): HybridRetriever.retrieve")
