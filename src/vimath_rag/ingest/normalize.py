"""Text normalization for Vietnamese math Markdown (docs/DATA.md, section 3.3).

Display text keeps the textbook's spelling. Search keys (BM25 tokens, concept aliases) may be
normalized more aggressively: tone-mark placement, i/y variants, LaTeX rewriting.
"""

from typing import Literal

ToneStyle = Literal["old", "new"]


def normalize_unicode(text: str) -> str:
    """NFC-normalize and drop invisible characters (zero-width spaces, soft hyphens). TODO(M1)."""
    raise NotImplementedError("TODO(M1): normalize_unicode")


def normalize_tone_marks(text: str, style: ToneStyle = "old") -> str:
    """Place tone marks consistently (``hòa`` vs ``hoà``) for search keys. TODO(M1)."""
    raise NotImplementedError("TODO(M1): normalize_tone_marks")


def fold_i_y(text: str) -> str:
    """Fold i/y spelling variants (``lí``/``lý``, ``kĩ``/``kỹ``) for search keys (ablation A2). TODO(M2)."""
    raise NotImplementedError("TODO(M2): fold_i_y")


def normalize_latex(text: str, *, unify_frac: bool = True, strip_left_right: bool = True) -> str:
    """Canonicalize LaTeX: ``\\dfrac``/``\\tfrac`` -> ``\\frac``, drop ``\\left``/``\\right``,
    collapse whitespace inside ``$...$``; keep decimal commas (``3,5``). TODO(M1)."""
    raise NotImplementedError("TODO(M1): normalize_latex")


def strip_page_furniture(text: str, patterns: list[str]) -> str:
    """Remove running headers, footers and page numbers matching ``patterns`` (regexes). TODO(M1)."""
    raise NotImplementedError("TODO(M1): strip_page_furniture")


def latex_to_words(text: str) -> str:
    """Rewrite math for lexical search, e.g. ``\\sqrt{x}`` -> "căn bậc hai của x",
    ``x^2`` -> "x bình phương" (ablation A2). TODO(M4)."""
    raise NotImplementedError("TODO(M4): latex_to_words")
