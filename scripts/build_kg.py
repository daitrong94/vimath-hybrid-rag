"""Build and validate the curriculum knowledge graph.

Examples:
    uv run python scripts/build_kg.py --validate data/kg/example_graph.json   # works now
    uv run python scripts/build_kg.py                                          # TODO(M3)
"""

import argparse

from vimath_rag.config import load_config, resolve_path
from vimath_rag.kg.build import load_graph
from vimath_rag.kg.schema import KGValidationError, load_kg_schema, validate_graph


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build / validate the curriculum KG.")
    parser.add_argument("--config", default="configs/corpus.yaml", help="config with kg_build")
    parser.add_argument("--validate", metavar="GRAPH_JSON", help="only validate this graph file")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    cfg = load_config(args.config)["kg_build"]
    schema = load_kg_schema(resolve_path(cfg["schema"]))
    if args.validate:
        graph = load_graph(resolve_path(args.validate))
        try:
            validate_graph(graph, schema)
        except KGValidationError as exc:
            raise SystemExit(str(exc)) from exc
        print(
            f"OK {args.validate}: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges"
        )
        return
    # TODO(M3): kg.build.build_graph_from_curated(cfg["curated_dir"]) -> validate_graph
    #           -> kg.build.save_graph(cfg["output"]); report counts per node/edge type.
    raise SystemExit("[TODO] building from data/kg/curated/ is not implemented yet (week 3)")


if __name__ == "__main__":
    main()
