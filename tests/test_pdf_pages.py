"""Tests for PDF page utilities on a synthetic PDF (needs the ``ingest`` extra)."""

from pathlib import Path

import pytest

pdfium = pytest.importorskip("pypdfium2")
pytest.importorskip("PIL")

from vimath_rag.ingest.pdf_pages import extract_pages, render_page_png  # noqa: E402


@pytest.fixture
def blank_pdf(tmp_path: Path) -> Path:
    path = tmp_path / "blank.pdf"
    pdf = pdfium.PdfDocument.new()
    for _ in range(3):
        pdf.new_page(200, 300)
    pdf.save(path)
    pdf.close()
    return path


def _page_sizes(path: Path) -> list[tuple[float, float]]:
    pdf = pdfium.PdfDocument(path)
    try:
        return [tuple(pdf[i].get_size()) for i in range(len(pdf))]
    finally:
        pdf.close()


def test_extract_pages_keeps_selected_pages(blank_pdf: Path, tmp_path: Path) -> None:
    out = extract_pages(blank_pdf, [1, 3], tmp_path / "sub.pdf")
    assert _page_sizes(out) == [(200, 300), (200, 300)]


def test_extract_pages_upscales(blank_pdf: Path, tmp_path: Path) -> None:
    out = extract_pages(blank_pdf, [2], tmp_path / "sub_s2.pdf", scale=2)
    assert _page_sizes(out) == [(400, 600)]


def test_extract_pages_rejects_bad_pages(blank_pdf: Path, tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="out of range"):
        extract_pages(blank_pdf, [0, 4], tmp_path / "bad.pdf")


def test_render_page_png(blank_pdf: Path, tmp_path: Path) -> None:
    out = render_page_png(blank_pdf, 1, tmp_path / "p1.png")
    assert out.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
