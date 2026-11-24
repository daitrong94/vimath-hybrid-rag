# CLAUDE.md

Context for AI coding sessions on **vimath-hybrid-rag**. Detailed docs (Vietnamese) live in `docs/`.

## Project
- Solo NLP course project (HUS, VNU), topic #8 "IR & RAG" of an AI Tutor program for Vietnamese secondary-school math (grades 6-9). Also a portfolio project: keep it clean and reproducible.
- Hybrid RAG over the *Kết nối tri thức* Toán 6-9 textbooks (8 PDFs) + a curriculum knowledge graph. Retrieved chunks ground LLM explanations/hints with citations ("SGK Toán 8, Bài X"); never use knowledge above the student's grade.
- Main result: one table comparing BM25 / Dense (bge-m3) / Graph / Hybrid (RRF) / Hybrid+Rerank on a 160-question golden set (32 dev / 128 test): Recall@k, MRR, nDCG@k, faithfulness, answer relevance, latency, cost.
- Deadline ≈ 2027-01-03. MVR checkpoint (BM25 + Dense + eval end-to-end): 2026-12-06. Plan: `docs/ROADMAP.md`.
- Compute: laptop CPU (Windows); Colab T4 for OCR and GPU work. LLM API budget ≤ 10 USD in total.

## Hard rules
1. **Copyright**: never commit textbook PDFs, OCR/Markdown output, chunk text, indexes, or outputs containing retrieved text. They live in `data/raw/`, `data/processed/`, `results/runs/` (git-ignored; pre-commit and CI block them). Commit only code, configs, golden-set questions + chunk ids, KG structure, synthetic examples and aggregated metrics.
2. **No fabricated results**: never write metrics, dataset statistics or claims that no code run produced. Use `TBD`. Every reported number must trace to a `run_id`.
3. **No secrets**: API keys only in `.env` (template: `.env.example`).
4. **Reproducible**: every step is a script in `scripts/` driven by `configs/*.yaml`; notebooks are for exploration only.
5. **Ask, don't guess**: ask the user about missing or ambiguous inputs; state trivial defaults explicitly. Never commit or push unless asked.
6. **Budget**: every LLM call goes through `generation/llm.py` (disk cache + `CostTracker` hard cap). Dev: Gemini Flash free tier; final and judge models are TBD in `configs/models.yaml`.

## Layout
- `src/vimath_rag/`: `ingest/` (probe -> convert -> normalize -> chunk), `retrievers/` (bm25, dense, graph, hybrid, reranker), `kg/` (schema, extract, build), `generation/` (prompts, llm), `eval/` (retrieval/generation metrics, tracking), `schemas.py` (data contracts), `config.py`, `api.py` (`answer`, `retrieve`).
- `scripts/`: build_corpus, build_index, build_kg, run_eval, export_schemas. `app/gradio_app.py`: local single-turn demo.
- Committed data: `data/golden_set/` (questions + ids), `data/kg/` (`schema.yaml` is the KG source of truth).

## Conventions
- Python 3.12 (`.python-version`), `requires-python >= 3.11`; uv manages the env and `uv.lock` (committed).
- Type hints everywhere. Pydantic models in `schemas.py` define all data formats; after changing `GoldItem`, run `scripts/export_schemas.py` (a test compares `schema.json`).
- ruff for lint + format (line length 100, Black-compatible style); pytest; add tests with every implemented function.
- Config-driven: no hard-coded paths, model ids, k values or prompts in code used by scripts.
- Light core deps (no torch). Heavy deps are extras: `ingest`, `ml`, `llm`, `viseg`, `demo`, `analysis`. `ocr-marker`/`ocr-mineru` are Colab-only and conflict with `llm`. Import heavy libraries lazily.
- Version pins: `>=x,<next major` (0.x packages: `<next minor`); exact versions live in `uv.lock`.
- Chunk ids `g{grade}-{unit}-{type}-{nn}` (e.g. `g8-b12-theorem-01`); unit ids (`g8-b12`) double as KG lesson node ids.
- Language: code, docstrings, comments and commit messages in English; README and `docs/` in Vietnamese.
- Mark unimplemented code `TODO(Mx)` with its roadmap milestone (M1-M6).

## Commands
```bash
uv sync                                                     # core + dev
uv sync --extra ingest --extra ml --extra llm --extra demo  # full laptop env
uv run ruff check . && uv run ruff format --check .
uv run pytest
uv run pre-commit install                                   # once per clone
uv run python scripts/build_corpus.py --stage probe|convert|chunk
python scripts/ocr_spike.py prepare|run|report              # OCR comparison (Colab notebook)
uv run python scripts/build_index.py --retriever bm25|dense|all
uv run python scripts/build_kg.py --validate data/kg/example_graph.json
uv run python scripts/run_eval.py --methods bm25 dense --split dev
uv run python app/gradio_app.py
```
