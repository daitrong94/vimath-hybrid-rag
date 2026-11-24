"""Classify PDF pages before conversion.

Verdicts:
- ``text``: usable text layer;
- ``garbled``: a text layer exists but Vietnamese is broken (e.g. legacy TCVN3/VNI font encodings);
- ``scanned``: no usable text layer (image-only page).

Runs on the laptop (CPU). Output: ``data/processed/probe/{book_id}.json``.

Observed on g6v1 (2026-11-24): every page is a single full-page image with no text at all, so a
document-level shortcut ("image-only PDF": all pages ``scanned``) should be reported up front.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

Verdict = Literal["text", "garbled", "scanned"]


@dataclass(frozen=True)
class PageProbe:
    """Text-layer statistics of one PDF page."""

    page: int  # 1-based PDF page index
    n_chars: int
    valid_syllable_ratio: float  # share of tokens that are valid Vietnamese syllables
    image_area_ratio: float  # share of the page area covered by images
    verdict: Verdict


def probe_pdf(
    path: Path,
    *,
    min_chars_per_page: int,
    min_valid_syllable_ratio: float,
    max_image_area_ratio: float,
) -> list[PageProbe]:
    """Probe every page of ``path``; thresholds come from ``configs/corpus.yaml: probe``.

    TODO(M1):
      - open with pypdfium2 (permissive license; avoid PyMuPDF, which is AGPL) and read the
        text layer of each page;
      - count characters and estimate image coverage from the page objects;
      - check syllable validity with a Vietnamese syllable regex/lexicon to catch garbled fonts;
      - verdict: ``scanned`` if few characters or mostly image, ``garbled`` if the syllable ratio
        is low, else ``text``.
    """
    raise NotImplementedError("TODO(M1): probe_pdf")


def summarize(pages: Sequence[PageProbe]) -> dict[str, int]:
    """Number of pages per verdict. TODO(M1)."""
    raise NotImplementedError("TODO(M1): summarize")
