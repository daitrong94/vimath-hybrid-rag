"""Split normalized Markdown into typed chunks with curriculum metadata.

Hierarchy: chapter -> unit (lesson, "Luyện tập chung", chapter review, ...) -> section -> block.
Each typed block (definition, theorem, formula, example with its solution, exercise) becomes one
chunk; long explanations are split at paragraph boundaries. Chunk ids follow
``g{grade}-{unit}-{type}-{nn}`` (docs/DATA.md, section 4.1) and are built with
:func:`vimath_rag.schemas.make_chunk_id`.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from vimath_rag.schemas import Chunk, ChunkType


@dataclass(frozen=True)
class BookMeta:
    """One textbook volume (an entry of ``configs/corpus.yaml: books``)."""

    book_id: str  # e.g. "g8v1"
    grade: int
    volume: int
    file: str  # e.g. "toan8_tap1.pdf"
    printed_page_offset: int | None = None  # pdf_page - printed_page


def chunk_markdown(
    markdown: str,
    *,
    book: BookMeta,
    cfg: Mapping[str, Any],
    corpus_version: str,
) -> list[Chunk]:
    """Chunk one volume's Markdown (with ``<!-- page: N -->`` markers).

    ``cfg`` is ``configs/corpus.yaml: chunking``.

    TODO(M1):
      - detect units with ``unit_markers`` and blocks with ``block_markers`` (case-insensitive);
      - count ordinals per (unit, type) so ids stay stable when other blocks change;
      - merge blocks shorter than ``min_chars``; split explanations longer than ``max_chars`` at
        paragraph boundaries; never split inside ``$$...$$`` or between an example and its solution;
      - set ``page_start``/``page_end`` from the page markers.
    """
    raise NotImplementedError("TODO(M1): chunk_markdown")


def detect_block_type(block_start: str, markers: Mapping[str, list[str]]) -> ChunkType:
    """Chunk type whose marker regex matches the start of a block (default: explanation). TODO(M1)."""
    raise NotImplementedError("TODO(M1): detect_block_type")
