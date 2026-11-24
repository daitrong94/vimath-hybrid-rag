"""Cheap, reference-free signals of OCR output quality (OCR spike, corpus QA).

These are proxies, not accuracy: they flag obvious failures (lost diacritics, no math, leftover
watermarks) but a human still has to compare the text with the page image.
"""

import re
import unicodedata
from collections.abc import Sequence
from dataclasses import asdict, dataclass

_LETTER_RE = re.compile(r"[^\W\d_]")
_DISPLAY_MATH_RE = re.compile(r"\$\$.+?\$\$", re.DOTALL)
_INLINE_MATH_RE = re.compile(r"\$[^$\n]+\$")


@dataclass(frozen=True)
class TextStats:
    n_chars: int
    n_letters: int
    diacritic_letter_ratio: float  # share of letters that are not plain ASCII (ă, ê, ơ, ạ, ...)
    n_inline_math: int  # $...$
    n_display_math: int  # $$...$$
    n_watermark_hits: int

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


def text_stats(text: str, watermark_patterns: Sequence[str] = ()) -> TextStats:
    """Compute :class:`TextStats` for (NFC-normalized) ``text``.

    Vietnamese prose has a large share of letters with diacritics; a value near 0 on a
    Vietnamese page means the OCR dropped them. Watermark patterns are matched case-insensitively
    per line (``configs/corpus.yaml: normalize.strip_patterns``).
    """
    text = unicodedata.normalize("NFC", text)
    letters = _LETTER_RE.findall(text)
    non_ascii = sum(1 for ch in letters if not ch.isascii())
    n_display = len(_DISPLAY_MATH_RE.findall(text))
    n_inline = len(_INLINE_MATH_RE.findall(_DISPLAY_MATH_RE.sub(" ", text)))
    hits = sum(
        len(re.findall(pattern, text, flags=re.IGNORECASE | re.MULTILINE))
        for pattern in watermark_patterns
    )
    return TextStats(
        n_chars=len(text),
        n_letters=len(letters),
        diacritic_letter_ratio=non_ascii / len(letters) if letters else 0.0,
        n_inline_math=n_inline,
        n_display_math=n_display,
        n_watermark_hits=hits,
    )
