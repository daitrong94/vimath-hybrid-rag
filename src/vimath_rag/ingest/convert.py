"""Convert a PDF to Markdown with LaTeX formulas and ``<!-- page: N -->`` markers.

Backends (``configs/corpus.yaml: ocr.backend``):
- ``text_layer``: extract the PDF text layer with pypdfium2 (fast, CPU; formulas are usually lost).
- ``marker`` / ``mineru``: run the OCR tool's command-line interface in a subprocess on Colab T4
  (extras ``ocr-marker`` / ``ocr-mineru``). Calling the CLI instead of importing the tool keeps
  its heavy, separately licensed stack and its pinned LLM SDK versions out of this package.

Each conversion writes ``{book_id}.md`` and ``{book_id}.manifest.json`` (tool, version, command,
time) under ``data/processed/md/`` so the corpus can be traced and rebuilt.
"""

import re
from collections.abc import Sequence
from pathlib import Path
from typing import Literal

Backend = Literal["text_layer", "marker", "mineru"]

# Marker --paginate_output puts a line "{N}" + 48 dashes before each page (N = 0-based page id).
# Braces are optional here so that both renderings of the README format are accepted.
_MARKER_PAGE_SEP_RE = re.compile(r"^\{?(\d+)\}?-{48}[ \t]*$", re.MULTILINE)


def split_paginated_markdown(markdown: str) -> list[tuple[int, str]]:
    """Split Marker ``--paginate_output`` Markdown into ``(page_id, text)`` pairs.

    ``page_id`` is the number in the separator (0-based in Marker). Text before the first
    separator, if any, is returned with ``page_id = -1``. Returns ``[]`` when there is no separator.
    """
    matches = list(_MARKER_PAGE_SEP_RE.finditer(markdown))
    if not matches:
        return []
    pages: list[tuple[int, str]] = []
    head = markdown[: matches[0].start()].strip()
    if head:
        pages.append((-1, head))
    for m, nxt in zip(matches, [*matches[1:], None], strict=True):
        end = nxt.start() if nxt is not None else len(markdown)
        pages.append((int(m[1]), markdown[m.end() : end].strip()))
    return pages


def convert_pdf(
    pdf_path: Path,
    out_dir: Path,
    *,
    backend: Backend,
    command: str | None = None,
    pages: Sequence[int] | None = None,
) -> Path:
    """Convert ``pdf_path`` (optionally only ``pages``, 1-based) and return the Markdown path.

    Args:
        command: CLI template for the OCR backends with ``{pdf}`` and ``{out}`` placeholders
            (``configs/corpus.yaml: ocr.<backend>.command``, TBD after the OCR spike).

    TODO(M1): implement the three backends; turn each backend's page separators into
    ``<!-- page: N -->`` markers; record tool name and version (``importlib.metadata``)
    in the manifest.
    """
    raise NotImplementedError("TODO(M1): convert_pdf")
