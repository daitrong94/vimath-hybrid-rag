"""Build the chunk corpus: probe PDFs -> Markdown (text layer / OCR) -> normalize -> chunks.

Examples:
    uv run python scripts/build_corpus.py --stage probe
    python scripts/build_corpus.py --stage convert --backend marker      # on Colab T4
    uv run python scripts/build_corpus.py --stage chunk --books g8v1 g8v2
"""

import argparse

from vimath_rag.config import load_config, resolve_path

STAGES = ("probe", "convert", "chunk", "all")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the textbook chunk corpus.")
    parser.add_argument("--config", default="configs/corpus.yaml", help="corpus config (YAML)")
    parser.add_argument("--stage", choices=STAGES, default="all")
    parser.add_argument("--books", nargs="+", metavar="BOOK_ID", help="subset, e.g. g8v1 g8v2")
    parser.add_argument(
        "--backend", choices=["text_layer", "marker", "mineru"], help="override ocr.backend"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    cfg = load_config(args.config)
    books = [b for b in cfg["books"] if not args.books or b["book_id"] in args.books]
    raw_dir = resolve_path(cfg["paths"]["raw_dir"])
    backend = args.backend or cfg["ocr"]["backend"]
    print(f"stage={args.stage} backend={backend} corpus_version={cfg['corpus_version']}")
    for book in books:
        status = "found" if (raw_dir / book["file"]).exists() else "missing"
        print(f"  {book['book_id']}: {raw_dir / book['file']} ({status})")
    # TODO(M1): probe   -> vimath_rag.ingest.probe.probe_pdf  -> data/processed/probe/{book_id}.json
    #           convert -> vimath_rag.ingest.convert.convert_pdf (+ manifest.json)
    #           chunk   -> vimath_rag.ingest.normalize + chunker.chunk_markdown -> chunks.jsonl
    raise SystemExit(
        f"[TODO] stage {args.stage!r} is not implemented yet (docs/ROADMAP.md, week 1)"
    )


if __name__ == "__main__":
    main()
