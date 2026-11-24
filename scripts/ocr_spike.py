"""OCR spike: compare OCR backends on a few textbook pages (docs/DATA.md, section 3.2).

Stages (meant for Colab T4; each OCR tool lives in its own venv, see
notebooks/colab_ocr_spike.ipynb):

    python scripts/ocr_spike.py prepare                        # page subsets + preview PNGs
    python scripts/ocr_spike.py run --variants marker_fast     # run with the venv's python
    python scripts/ocr_spike.py report                         # review.html, summary.json, scores.csv

Settings: ``configs/corpus.yaml: ocr_spike``. Outputs go to ``<out_dir>/<book_id>/`` under
``data/processed/`` (git-ignored: they contain textbook text and page images). A variant whose
executable is not installed in the current environment is skipped, so ``run`` can be called
once per tool environment and ``report`` merges every run found.
"""

import argparse
import csv
import html
import json
import os
import shlex
import shutil
import subprocess
import sys
import time
from importlib import metadata
from pathlib import Path
from typing import Any

from vimath_rag.config import load_config, resolve_path
from vimath_rag.ingest.convert import split_paginated_markdown
from vimath_rag.ingest.pdf_pages import extract_pages, render_page_png
from vimath_rag.ingest.quality import text_stats

SCORE_COLUMNS = ["diacritics_0_2", "latex_0_2", "structure_0_2", "tables_0_2", "notes"]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare OCR backends on sample pages.")
    parser.add_argument("stage", choices=["prepare", "run", "report"])
    parser.add_argument("--config", default="configs/corpus.yaml", help="config with ocr_spike")
    parser.add_argument("--variants", nargs="+", help="subset of ocr_spike.variants (run stage)")
    parser.add_argument("--scales", nargs="+", type=float, help="override ocr_spike.scales")
    return parser.parse_args(argv)


def _scale_tag(scale: float) -> str:
    return f"s{scale:g}"


class Spike:
    """Paths and settings of one spike (one book)."""

    def __init__(self, cfg: dict[str, Any], scales: list[float] | None = None) -> None:
        self.cfg = cfg
        self.spike = cfg["ocr_spike"]
        self.book = next(b for b in cfg["books"] if b["book_id"] == self.spike["book_id"])
        self.pages: list[int] = list(self.spike["pages"])
        self.scales: list[float] = scales or [float(s) for s in self.spike["scales"]]
        self.src = resolve_path(cfg["paths"]["raw_dir"]) / self.book["file"]
        self.root = resolve_path(self.spike["out_dir"]) / self.book["book_id"]

    def input_pdf(self, scale: float) -> Path:
        return self.root / "input" / f"{self.book['book_id']}_{_scale_tag(scale)}.pdf"

    def preview_png(self, page: int) -> Path:
        return self.root / "pages" / f"p{page:03d}.png"

    def run_dir(self, variant: str, scale: float) -> Path:
        return self.root / "runs" / f"{variant}_{_scale_tag(scale)}"


def prepare(sp: Spike) -> None:
    if not sp.src.exists():
        raise SystemExit(f"missing {sp.src}")
    for scale in sp.scales:
        dst = extract_pages(sp.src, sp.pages, sp.input_pdf(scale), scale=scale)
        print(f"wrote {dst} ({len(sp.pages)} pages, scale {scale:g})")
    for page in sp.pages:
        render_page_png(sp.src, page, sp.preview_png(page))
    print(f"wrote {len(sp.pages)} preview PNGs to {sp.root / 'pages'}")


def _tool_env(extra: dict[str, str]) -> dict[str, str]:
    env = os.environ.copy()
    # CLIs installed next to the running interpreter (the tool's venv) come first on PATH.
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")
    env.update({k: str(v) for k, v in extra.items()})
    return env


def _package_version(package: str | None) -> str | None:
    if not package:
        return None
    try:
        return metadata.version(package)
    except metadata.PackageNotFoundError:
        return None


def run(sp: Spike, variants: list[str] | None) -> None:
    all_variants: dict[str, dict[str, str]] = sp.spike["variants"]
    unknown = set(variants or []) - all_variants.keys()
    if unknown:
        raise SystemExit(f"unknown variants {sorted(unknown)}; known: {sorted(all_variants)}")
    env = _tool_env(sp.spike.get("env", {}))
    for name in variants or list(all_variants):
        spec = all_variants[name]
        exe = shlex.split(spec["command"])[0]
        if shutil.which(exe, path=env["PATH"]) is None:
            print(f"skip {name}: {exe!r} is not installed in this environment")
            continue
        for scale in sp.scales:
            pdf = sp.input_pdf(scale)
            if not pdf.exists():
                raise SystemExit(f"missing {pdf}; run the prepare stage first")
            out = sp.run_dir(name, scale)
            if out.exists():
                shutil.rmtree(out)
            out.mkdir(parents=True)
            command = spec["command"].format(pdf=pdf.as_posix(), out=out.as_posix(), stem=pdf.stem)
            print(f"run {name} {_scale_tag(scale)}: {command}", flush=True)
            record: dict[str, Any] = {
                "variant": name,
                "scale": scale,
                "command": command,
                "package": spec.get("package"),
                "package_version": _package_version(spec.get("package")),
                "n_pages": len(sp.pages),
            }
            start = time.perf_counter()
            with (out / "stdout.log").open("w") as so, (out / "stderr.log").open("w") as se:
                try:
                    proc = subprocess.run(
                        shlex.split(command),
                        stdout=so,
                        stderr=se,
                        env=env,
                        timeout=sp.spike.get("timeout_s", 3600),
                        check=False,
                    )
                    record["returncode"] = proc.returncode
                except subprocess.TimeoutExpired:
                    record["returncode"] = None
                    record["error"] = "timeout"
            seconds = time.perf_counter() - start
            record["seconds"] = round(seconds, 1)
            record["seconds_per_page"] = round(seconds / len(sp.pages), 2)
            (out / "run.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            status = "ok" if record["returncode"] == 0 else f"FAILED ({out / 'stderr.log'})"
            print(f"  -> {status}, {record['seconds']} s", flush=True)


def _read_markdown(run_dir: Path) -> str:
    files = sorted(p for p in run_dir.rglob("*.md") if p.is_file())
    return "\n\n".join(p.read_text(encoding="utf-8", errors="replace") for p in files)


def _per_page(markdown: str, n_pages: int) -> list[str] | None:
    """Per-page texts when the output is paginated with exactly one segment per page."""
    segments = [text for page_id, text in split_paginated_markdown(markdown) if page_id >= 0]
    return segments if len(segments) == n_pages else None


def report(sp: Spike) -> None:
    runs = []
    for run_json in sorted((sp.root / "runs").glob("*/run.json")):
        record = json.loads(run_json.read_text(encoding="utf-8"))
        markdown = _read_markdown(run_json.parent)
        record["stats"] = text_stats(
            markdown, sp.cfg["normalize"].get("strip_patterns", [])
        ).to_dict()
        record["per_page_split"] = _per_page(markdown, len(sp.pages)) is not None
        runs.append((run_json.parent.name, record, markdown))
    if not runs:
        raise SystemExit(f"no runs found under {sp.root / 'runs'}")

    summary = {"book_id": sp.book["book_id"], "pages": sp.pages, "runs": [r for _, r, _ in runs]}
    (sp.root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    scores = sp.root / "scores.csv"
    if not scores.exists():  # never overwrite manual scores
        with scores.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["page", "run", *SCORE_COLUMNS])
            for page in sp.pages:
                for run_name, _, _ in runs:
                    writer.writerow([page, run_name, *[""] * len(SCORE_COLUMNS)])

    _write_review_html(sp, runs)
    print(f"wrote {sp.root / 'summary.json'}, {scores.name}, review.html")
    for run_name, record, _ in runs:
        stats = record["stats"]
        print(
            f"  {run_name:24s} rc={record.get('returncode')} {record['seconds_per_page']:>6} s/page "
            f"diacritics={stats['diacritic_letter_ratio']:.2f} "
            f"math={stats['n_inline_math']}+{stats['n_display_math']} "
            f"watermark={stats['n_watermark_hits']} split={record['per_page_split']}"
        )


def _write_review_html(sp: Spike, runs: list[tuple[str, dict[str, Any], str]]) -> None:
    per_page = {name: _per_page(md, len(sp.pages)) for name, _, md in runs}
    cols = len(runs) + 1
    parts = [
        "<!doctype html><meta charset='utf-8'><title>OCR spike</title>",
        "<style>body{font-family:sans-serif;margin:16px}"
        f".row{{display:grid;grid-template-columns:repeat({cols},minmax(0,1fr));gap:8px}}"
        "img{width:100%;border:1px solid #ccc}"
        "pre{white-space:pre-wrap;font-size:12px;background:#f6f6f6;padding:6px;margin:0}"
        "h2{margin-top:32px}</style>",
        f"<h1>OCR spike: {html.escape(sp.book['book_id'])} (local only, copyrighted content)</h1>",
        "<p>Score each page in scores.csv (0 = unusable, 1 = needs fixes, 2 = good).</p>",
    ]
    for i, page in enumerate(sp.pages):
        parts.append(f"<h2>PDF page {page}</h2><div class='row'>")
        parts.append(f"<div><img src='pages/p{page:03d}.png' alt='page {page}'></div>")
        for name, _, _ in runs:
            pages = per_page[name]
            body = pages[i] if pages else "(output not split per page: see full text below)"
            parts.append(f"<div><b>{html.escape(name)}</b><pre>{html.escape(body)}</pre></div>")
        parts.append("</div>")
    for name, _, md in runs:
        if per_page[name] is None:
            parts.append(f"<h2>Full output: {html.escape(name)}</h2><pre>{html.escape(md)}</pre>")
    (sp.root / "review.html").write_text("\n".join(parts), encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    sp = Spike(load_config(args.config), args.scales)
    if args.stage == "prepare":
        prepare(sp)
    elif args.stage == "run":
        run(sp, args.variants)
    else:
        report(sp)


if __name__ == "__main__":
    main()
