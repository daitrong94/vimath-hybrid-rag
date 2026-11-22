"""Dense retrieval: bge-m3 embeddings (sentence-transformers) + FAISS exact search.

Requires the ``ml`` extra. Import torch / faiss / sentence-transformers lazily inside methods so
that the core package stays importable without them.
"""

from collections.abc import Sequence
from pathlib import Path
from typing import Self

from vimath_rag.schemas import Chunk, RetrievedChunk


class DenseRetriever:
    """Embeds chunks and searches a FAISS ``IndexFlatIP`` over L2-normalized vectors.

    bge-m3 needs no query instruction prefix. Encoding the whole corpus on the laptop CPU may be
    slow; it can run on Colab, with the index files copied back to ``data/processed/indexes/dense``.
    """

    name = "dense"

    def __init__(
        self,
        model_name: str,
        *,
        device: str = "cpu",
        batch_size: int = 16,
        max_seq_length: int = 512,
        normalize: bool = True,
    ) -> None:
        self.model_name = model_name
        self.device = device
        self.batch_size = batch_size
        self.max_seq_length = max_seq_length
        self.normalize = normalize

    def build(self, chunks: Sequence[Chunk]) -> None:
        """Encode ``chunks`` and build the FAISS index. TODO(M2)."""
        raise NotImplementedError("TODO(M2): DenseRetriever.build")

    def save(self, index_dir: Path) -> None:
        """Write the FAISS index, chunk-id order and model name. TODO(M2)."""
        raise NotImplementedError("TODO(M2): DenseRetriever.save")

    @classmethod
    def load(cls, index_dir: Path, *, device: str = "cpu") -> Self:
        """Load an index written by :meth:`save` (refuse if the model name differs). TODO(M2)."""
        raise NotImplementedError("TODO(M2): DenseRetriever.load")

    def retrieve(self, query: str, k: int = 10, grade: int | None = None) -> list[RetrievedChunk]:
        """Encode the query, search, apply the grade filter, return the top-k. TODO(M2)."""
        raise NotImplementedError("TODO(M2): DenseRetriever.retrieve")
