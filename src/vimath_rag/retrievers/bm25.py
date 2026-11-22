"""Sparse retrieval: BM25 (``bm25s``) over Vietnamese syllables or word segments."""

from collections.abc import Sequence
from pathlib import Path
from typing import Literal, Self

from vimath_rag.schemas import Chunk, RetrievedChunk

TokenizerMode = Literal["syllable", "word"]


def tokenize_vi(
    text: str, mode: TokenizerMode = "syllable", *, keep_latex_commands: bool = True
) -> list[str]:
    """Tokenize Vietnamese math text for BM25.

    TODO(M2): lowercase and keep diacritics; split on whitespace/punctuation (``syllable``) or
    use ``underthesea.word_tokenize`` (``word``, extra ``viseg``); turn LaTeX commands into tokens
    (``\\frac`` -> ``frac``); keep decimal numbers such as ``3,5`` as one token.
    """
    raise NotImplementedError("TODO(M2): tokenize_vi")


class BM25Retriever:
    """BM25 over the indexed chunks (``configs/retrievers.yaml: bm25``)."""

    name = "bm25"

    def __init__(
        self,
        *,
        method: str = "lucene",
        k1: float = 1.5,
        b: float = 0.75,
        tokenizer: TokenizerMode = "syllable",
    ) -> None:
        self.method = method
        self.k1 = k1
        self.b = b
        self.tokenizer = tokenizer

    def build(self, chunks: Sequence[Chunk]) -> None:
        """Index ``chunks``. TODO(M2): tokenize with :func:`tokenize_vi`, build a ``bm25s.BM25`` index
        (check that bm25s accepts pre-tokenized input; otherwise map tokens to ids first)."""
        raise NotImplementedError("TODO(M2): BM25Retriever.build")

    def save(self, index_dir: Path) -> None:
        """Persist the index and the chunk-id order. TODO(M2)."""
        raise NotImplementedError("TODO(M2): BM25Retriever.save")

    @classmethod
    def load(cls, index_dir: Path) -> Self:
        """Load an index written by :meth:`save`. TODO(M2)."""
        raise NotImplementedError("TODO(M2): BM25Retriever.load")

    def retrieve(self, query: str, k: int = 10, grade: int | None = None) -> list[RetrievedChunk]:
        """Score the query, apply the grade filter, return the top-k. TODO(M2)."""
        raise NotImplementedError("TODO(M2): BM25Retriever.retrieve")
