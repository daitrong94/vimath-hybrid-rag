"""Run the retrieval / generation benchmark on the golden set.

Examples:
    uv run python scripts/run_eval.py --golden data/golden_set/examples.jsonl --split all  # format check
    uv run python scripts/run_eval.py --methods bm25 dense --split dev
    uv run python scripts/run_eval.py --split test
"""

import argparse
from collections import Counter

from vimath_rag.config import load_config, resolve_path
from vimath_rag.schemas import load_golden_set


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate retrieval methods on the golden set.")
    parser.add_argument("--config", default="configs/eval.yaml", help="evaluation config")
    parser.add_argument("--golden", help="override the golden-set path from the config")
    parser.add_argument("--methods", nargs="+", help="override the methods from the config")
    parser.add_argument("--split", choices=["dev", "test", "all"], help="override the split")
    parser.add_argument("--no-generation", action="store_true", help="retrieval metrics only")
    parser.add_argument("--limit", type=int, help="evaluate only the first N questions")
    parser.add_argument("--run-id", help="name of results/runs/<run_id> (default: timestamp)")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    cfg = load_config(args.config)
    golden_path = resolve_path(args.golden or cfg["golden_set"])
    if not golden_path.exists():
        raise SystemExit(
            f"golden set not found: {golden_path}\n"
            "try the format check: --golden data/golden_set/examples.jsonl --split all"
        )
    items = load_golden_set(golden_path)
    split = args.split or cfg["split"]
    if split != "all":
        items = [item for item in items if item.split == split]
    if args.limit:
        items = items[: args.limit]
    methods = args.methods or cfg["methods"]
    print(f"{len(items)} questions (split={split}) from {golden_path.name}; methods={methods}")
    print(f"  by type: {dict(Counter(item.qtype.value for item in items))}")
    print(f"  by grade: {dict(sorted(Counter(item.grade for item in items).items()))}")
    # TODO(M2): validate gold ids against chunks.jsonl; run each method; compute
    #           eval.retrieval_metrics; write results/runs/<run_id>/ (config snapshot, env,
    #           per-question outputs) and results/tables/<run_id>_*.md|csv.
    # TODO(M5): generation metrics for cfg["generation"]["methods"] within cfg["budget"].
    raise SystemExit("[TODO] evaluation is not implemented yet (docs/ROADMAP.md, week 2)")


if __name__ == "__main__":
    main()
