"""Latency, token and cost tracking with a hard budget cap (total API budget <= 10 USD).

Prices come from ``configs/models.yaml: prices_usd_per_mtok`` and must be copied from the
providers' pricing pages before paid runs; unknown models are refused rather than priced at 0.
"""

import time
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path


class BudgetExceededError(RuntimeError):
    """Raised before an LLM call would push spending over the configured cap."""


@dataclass(frozen=True)
class Price:
    """USD per million tokens."""

    input_per_mtok: float
    output_per_mtok: float


@dataclass
class CostTracker:
    """Accumulates LLM spending and enforces ``budget_usd`` (``configs/eval.yaml: budget``).

    ``ledger_path`` is an append-only JSONL file shared across runs (git-ignored, ``.cache/``),
    so the total cap holds over the whole project, not just one run.
    """

    prices: Mapping[str, Price]
    budget_usd: float | None = None
    ledger_path: Path | None = None
    spent_usd: float = 0.0
    calls: int = 0

    def estimate(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Cost in USD; ``KeyError`` for models missing from ``prices``. TODO(M4)."""
        raise NotImplementedError("TODO(M4): CostTracker.estimate")

    def check(self, estimated_usd: float) -> None:
        """Raise :class:`BudgetExceededError` if ledger total + spent + estimate exceeds the
        budget. TODO(M4)."""
        raise NotImplementedError("TODO(M4): CostTracker.check")

    def record(
        self, model: str, input_tokens: int, output_tokens: int, *, cached: bool = False
    ) -> float:
        """Add one call (cached calls cost 0), append it to the ledger, return its cost. TODO(M4)."""
        raise NotImplementedError("TODO(M4): CostTracker.record")


@contextmanager
def timer(store: dict[str, float], key: str) -> Iterator[None]:
    """Measure the wall-clock milliseconds of a ``with`` block into ``store[key]``."""
    start = time.perf_counter()
    try:
        yield
    finally:
        store[key] = (time.perf_counter() - start) * 1000.0
