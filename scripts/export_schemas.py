"""Export JSON Schemas generated from the pydantic data contracts.

Usage:
    uv run python scripts/export_schemas.py

``tests/test_smoke.py`` fails when the committed schema differs from the model.
"""

import json

from vimath_rag.config import PROJECT_ROOT
from vimath_rag.schemas import GoldItem

TARGETS = {PROJECT_ROOT / "data" / "golden_set" / "schema.json": GoldItem}


def main() -> None:
    for path, model in TARGETS.items():
        schema = model.model_json_schema()
        path.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
