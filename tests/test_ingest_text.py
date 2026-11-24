"""Tests for pure-text ingest helpers: OCR quality signals and Marker page splitting."""

import pytest

from vimath_rag.ingest.convert import split_paginated_markdown
from vimath_rag.ingest.quality import text_stats

SEP = "-" * 48


def test_text_stats_counts_math_and_diacritics() -> None:
    stats = text_stats("Số nguyên tố $p$ và $q$.\n\n$$a^2 + b^2 = c^2$$\n")
    assert stats.n_inline_math == 2
    assert stats.n_display_math == 1
    assert 0.0 < stats.diacritic_letter_ratio < 1.0


def test_text_stats_flags_lost_diacritics() -> None:
    assert text_stats("So nguyen to la gi").diacritic_letter_ratio == 0.0


def test_text_stats_counts_watermark_lines_case_insensitively() -> None:
    text = "Bài 8\nKẾT NỐI TRI THỨC\nnội dung\nkết nối tri thức\n"
    stats = text_stats(text, [r"^\s*KẾT NỐI TRI THỨC\s*$"])
    assert stats.n_watermark_hits == 2


def test_text_stats_empty_text() -> None:
    stats = text_stats("")
    assert stats.n_letters == 0
    assert stats.diacritic_letter_ratio == 0.0


@pytest.mark.parametrize("fmt", ["{{{n}}}{sep}", "{n}{sep}"])
def test_split_paginated_markdown(fmt: str) -> None:
    md = "\n\n".join(f"{fmt.format(n=n, sep=SEP)}\n\nTrang {n} nội dung" for n in range(3))
    pages = split_paginated_markdown(md)
    assert [page_id for page_id, _ in pages] == [0, 1, 2]
    assert pages[1][1] == "Trang 1 nội dung"


def test_split_paginated_markdown_keeps_head_and_handles_plain_text() -> None:
    md = f"tiêu đề\n\n{{0}}{SEP}\n\nnội dung"
    assert split_paginated_markdown(md) == [(-1, "tiêu đề"), (0, "nội dung")]
    assert split_paginated_markdown("không có dấu phân trang") == []
