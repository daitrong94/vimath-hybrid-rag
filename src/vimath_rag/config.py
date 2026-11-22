"""Configuration helpers: YAML files in ``configs/`` and secrets from ``.env``.

Scripts take ``--config`` paths. Code used by scripts must not hard-code paths, model ids,
k values or prompts; they come from the YAML configs (see CLAUDE.md).

TODO(M2): typed pydantic models for each config file, validated at load time.
"""

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

#: Repository root; override with the ``VIMATH_ROOT`` environment variable.
PROJECT_ROOT = Path(os.environ.get("VIMATH_ROOT") or Path(__file__).resolve().parents[2])
CONFIG_DIR = PROJECT_ROOT / "configs"


def resolve_path(path: str | Path) -> Path:
    """Resolve ``path`` against the project root unless it is absolute."""
    p = Path(path)
    return p if p.is_absolute() else PROJECT_ROOT / p


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML config file as a dict.

    Args:
        path: a file path (absolute, or relative to the project root) or a bare config name
            such as ``"retrievers"``, which resolves to ``configs/retrievers.yaml``.
    """
    p = Path(path)
    if not p.suffix and len(p.parts) == 1:
        p = CONFIG_DIR / f"{p}.yaml"
    p = resolve_path(p)
    with p.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{p}: expected a YAML mapping, got {type(data).__name__}")
    return data


def load_env(dotenv_path: str | Path | None = None) -> bool:
    """Load API keys from ``.env`` if present, without overriding variables that are already set."""
    return load_dotenv(dotenv_path or PROJECT_ROOT / ".env", override=False)
