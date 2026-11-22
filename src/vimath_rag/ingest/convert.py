"""Convert a PDF to Markdown with LaTeX formulas and ``<!-- page: N -->`` markers.

Backends (``configs/corpus.yaml: ocr.backend``):
- ``text_layer``: extract the PDF text layer with pypdfium2 (fast, CPU; formulas are usually lost).
- ``marker`` / ``mineru``: run the OCR tool's command-line interface in a subprocess on Colab T4
  (extras ``ocr-marker`` / ``ocr-mineru``). Calling the CLI instead of importing the tool keeps
  its heavy, separately licensed stack and its pinned LLM SDK versions out of this package.

Each conversion writes ``{book_id}.md`` and ``{book_id}.manifest.json`` (tool, version, command,
time) under ``data/processed/md/`` so the corpus can be traced and rebuilt.
"""

from collections.abc import Sequence
from pathlib import Path
from typing import Literal

Backend = Literal["text_layer", "marker", "mineru"]


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
