"""Cross-encoder reranking (``BAAI/bge-reranker-v2-m3`` via sentence-transformers ``CrossEncoder``).

Requires the ``ml`` extra; import sentence-transformers lazily.
"""

from collections.abc import Sequence

from vimath_rag.schemas import RetrievedChunk


class CrossEncoderReranker:
    """Re-scores (query, chunk text) pairs and re-sorts the candidates."""

    def __init__(
        self,
        model_name: str,
        *,
        device: str = "cpu",
        batch_size: int = 8,
        max_length: int = 512,
    ) -> None:
        self.model_name = model_name
        self.device = device
        self.batch_size = batch_size
        self.max_length = max_length

    def rerank(
        self, query: str, candidates: Sequence[RetrievedChunk], top_n: int
    ) -> list[RetrievedChunk]:
        """Rerank the first ``top_n`` candidates (they must carry ``chunk``), renumber ranks,
        keep the rest after them. TODO(M4): measure CPU latency per query."""
        raise NotImplementedError("TODO(M4): CrossEncoderReranker.rerank")
