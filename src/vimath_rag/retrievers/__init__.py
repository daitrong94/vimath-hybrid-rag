"""Retrieval methods compared in the benchmark (``configs/retrievers.yaml``).

- :mod:`.bm25`: sparse (bm25s) over Vietnamese syllables or word segments
- :mod:`.dense`: bge-m3 embeddings + FAISS
- :mod:`.graph`: curriculum knowledge graph (concept linking + PPR/BFS expansion)
- :mod:`.hybrid`: Reciprocal Rank Fusion + grade filter + optional :mod:`.reranker`
"""

from collections.abc import Mapping
from typing import Any

from vimath_rag.retrievers.base import Retriever, grade_allowed

__all__ = ["Retriever", "get_retriever", "grade_allowed"]


def get_retriever(
    method: str,
    retrievers_cfg: Mapping[str, Any],
    models_cfg: Mapping[str, Any],
) -> Retriever:
    """Build the retriever for ``method`` (a key of ``retrievers_cfg["methods"]``).

    TODO(M2): bm25, dense. TODO(M3): graph. TODO(M4): hybrid, hybrid_rerank.
    Heavy dependencies (torch, faiss) must be imported lazily inside the concrete retrievers.
    """
    raise NotImplementedError(f"TODO: get_retriever({method!r})")
