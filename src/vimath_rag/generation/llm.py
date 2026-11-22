"""LLM client abstraction shared by generation, LLM-as-judge and KG extraction.

Backends (``configs/models.yaml: llm``):
- ``gemini``: google-genai SDK, key in ``GEMINI_API_KEY`` (dev, free tier)
- ``openai``: openai SDK, key in ``OPENAI_API_KEY``
- ``anthropic``: anthropic SDK, key in ``ANTHROPIC_API_KEY``
- ``ollama``: local models through Ollama's OpenAI-compatible endpoint (``OLLAMA_BASE_URL``)

Every LLM call in the project goes through :func:`get_llm_client`, so the disk cache and the
:class:`~vimath_rag.eval.tracking.CostTracker` budget cap see it. Requires the ``llm`` extra;
import the SDKs lazily inside the client classes.
"""

import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal, Protocol

from vimath_rag.eval.tracking import CostTracker

Role = Literal["system", "user", "assistant"]
Backend = Literal["gemini", "openai", "anthropic", "ollama"]


@dataclass(frozen=True)
class Message:
    role: Role
    content: str


@dataclass(frozen=True)
class LLMResponse:
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    cached: bool = False


class LLMClient(Protocol):
    backend: str
    model: str

    def generate(
        self, messages: Sequence[Message], *, temperature: float = 0.0, max_tokens: int = 1024
    ) -> LLMResponse: ...


def cache_key(backend: str, model: str, messages: Sequence[Message], **params: Any) -> str:
    """Stable SHA-256 key of a request, used by the disk cache."""
    payload = {
        "backend": backend,
        "model": model,
        "messages": [asdict(m) for m in messages],
        "params": params,
    }
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


class GeminiClient:
    """google-genai client. TODO(M4): pass system messages as ``system_instruction``; read token
    counts from the response usage metadata."""

    backend = "gemini"

    def __init__(self, model: str, api_key_env: str = "GEMINI_API_KEY") -> None:
        self.model = model
        self.api_key_env = api_key_env

    def generate(
        self, messages: Sequence[Message], *, temperature: float = 0.0, max_tokens: int = 1024
    ) -> LLMResponse:
        raise NotImplementedError("TODO(M4): GeminiClient.generate")


class OpenAIClient:
    """openai client. With ``base_url`` set it also serves Ollama (``backend="ollama"``). TODO(M4)."""

    def __init__(
        self,
        model: str,
        api_key_env: str = "OPENAI_API_KEY",
        *,
        base_url: str | None = None,
        backend: Backend = "openai",
    ) -> None:
        self.model = model
        self.api_key_env = api_key_env
        self.base_url = base_url
        self.backend = backend

    def generate(
        self, messages: Sequence[Message], *, temperature: float = 0.0, max_tokens: int = 1024
    ) -> LLMResponse:
        raise NotImplementedError("TODO(M4): OpenAIClient.generate")


class AnthropicClient:
    """anthropic client. TODO(M4): system messages go in the ``system`` parameter, not in
    ``messages``; read token counts from ``usage``."""

    backend = "anthropic"

    def __init__(self, model: str, api_key_env: str = "ANTHROPIC_API_KEY") -> None:
        self.model = model
        self.api_key_env = api_key_env

    def generate(
        self, messages: Sequence[Message], *, temperature: float = 0.0, max_tokens: int = 1024
    ) -> LLMResponse:
        raise NotImplementedError("TODO(M4): AnthropicClient.generate")


class CachedLLMClient:
    """Wraps a client with a JSON disk cache and cost tracking.

    TODO(M4): key = :func:`cache_key`; on a hit return the stored response with ``cached=True``
    (cost 0); on a miss call ``tracker.check()`` with an estimate first, then the inner client,
    then ``tracker.record()``, then write the cache file.
    """

    def __init__(
        self, inner: LLMClient, cache_dir: Path, tracker: CostTracker | None = None
    ) -> None:
        self.inner = inner
        self.cache_dir = cache_dir
        self.tracker = tracker
        self.backend = inner.backend
        self.model = inner.model

    def generate(
        self, messages: Sequence[Message], *, temperature: float = 0.0, max_tokens: int = 1024
    ) -> LLMResponse:
        raise NotImplementedError("TODO(M4): CachedLLMClient.generate")


def get_llm_client(
    role: str,
    models_cfg: Mapping[str, Any],
    *,
    tracker: CostTracker | None = None,
) -> LLMClient:
    """Build the cached client for ``models_cfg["llm"][role]`` (role: dev | final | judge | local).

    TODO(M4): refuse ``model: TBD`` with a clear message pointing at configs/models.yaml; load keys
    with :func:`vimath_rag.config.load_env`; wrap in :class:`CachedLLMClient` when caching is on.
    """
    raise NotImplementedError(f"TODO(M4): get_llm_client({role!r})")
