"""Page-level PDF utilities: page subsets, upscaling and preview images.

Requires the ``ingest`` extra (pypdfium2, Pillow); both are imported lazily.
Page numbers are 1-based PDF page indices throughout.
"""

from collections.abc import Sequence
from pathlib import Path


def _check_pages(pages: Sequence[int], n_pages: int) -> None:
    if not pages:
        raise ValueError("no pages given")
    bad = [p for p in pages if not 1 <= p <= n_pages]
    if bad:
        raise ValueError(f"pages out of range 1..{n_pages}: {bad}")


def extract_pages(src: Path, pages: Sequence[int], dst: Path, *, scale: float = 1.0) -> Path:
    """Write ``pages`` of ``src`` to a new PDF ``dst`` and return ``dst``.

    ``scale == 1`` copies the pages losslessly. ``scale > 1`` renders each page at ``scale`` and
    re-embeds it as a lossless image page: glyphs get larger for OCR, but no detail is added.
    """
    import pypdfium2 as pdfium

    if scale <= 0:
        raise ValueError(f"scale must be > 0, got {scale}")
    src_pdf = pdfium.PdfDocument(src)
    out = pdfium.PdfDocument.new()
    try:
        _check_pages(pages, len(src_pdf))
        if scale == 1:
            out.import_pages(src_pdf, [p - 1 for p in pages])
        else:
            for p in pages:
                page = src_pdf[p - 1]
                width, height = page.get_size()
                image = pdfium.PdfImage.new(out)
                image.set_bitmap(page.render(scale=scale))
                image.set_matrix(pdfium.PdfMatrix().scale(width * scale, height * scale))
                new_page = out.new_page(width * scale, height * scale)
                new_page.insert_obj(image)
                new_page.gen_content()
        dst.parent.mkdir(parents=True, exist_ok=True)
        out.save(dst)
    finally:
        out.close()
        src_pdf.close()
    return dst


def render_page_png(src: Path, page: int, dst: Path, *, scale: float = 1.0) -> Path:
    """Render one page of ``src`` to a PNG file ``dst`` (for visual review)."""
    import pypdfium2 as pdfium

    pdf = pdfium.PdfDocument(src)
    try:
        _check_pages([page], len(pdf))
        dst.parent.mkdir(parents=True, exist_ok=True)
        pdf[page - 1].render(scale=scale).to_pil().save(dst)
    finally:
        pdf.close()
    return dst
