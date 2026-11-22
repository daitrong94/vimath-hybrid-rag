"""Build retrieval indexes (BM25, dense) from ``data/processed/chunks/chunks.jsonl``.

Examples:
    uv run python scripts/build_index.py --retriever bm25
    uv run python scripts/build_index.py --retriever all
"""

import argparse

from vimath_rag.config import load_config, resolve_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build BM25 / dense indexes.")
    parser.add_argument("--config", default="configs/retrievers.yaml", help="retrievers config")
    parser.add_argument("--models", default="configs/models.yaml", help="models config")
    parser.add_argument("--retriever", choices=["bm25", "dense", "all"], default="all")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    cfg = load_config(args.config)
    models = load_config(args.models)
    chunks_path = resolve_path(cfg["chunks_path"])
    print(f"retriever={args.retriever} chunks={chunks_path} (exists={chunks_path.exists()})")
    print(
        f"embedding model={models['embedding']['name']} index_dir={resolve_path(cfg['index_dir'])}"
    )
    # TODO(M2): read chunks (schemas.read_jsonl), keep cfg["index_types"], then
    #           BM25Retriever.build/save and DenseRetriever.build/save under index_dir.
    raise SystemExit("[TODO] index building is not implemented yet (docs/ROADMAP.md, week 2)")


if __name__ == "__main__":
    main()
