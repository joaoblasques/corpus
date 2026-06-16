#!/usr/bin/env python3
"""rank_links.py — score candidate links by learning utility, apply floor + cap.

Primary path: routes through bin/llm.py (local Ollama → ok=True → scores used).
Fallback (router ok=False or any error): collect_email.heuristic_score.
"""
from __future__ import annotations

import json
import os
import pathlib
import sys

BIN = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
import collect_email as ce  # noqa: E402

RANK_MODEL = "claude-haiku-4-5-20251001"


def load_env(path: str | None = None) -> None:
    """Load KEY=VALUE lines from a gitignored .env into os.environ (no overwrite)."""
    p = pathlib.Path(path) if path else (BIN.parent / ".env")
    if not p.exists():
        return
    try:
        text = p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _llm_scores(candidates: list[dict]) -> list[int]:
    import llm  # bin/ is on sys.path

    listing = "\n".join(
        f"{i}. {c['url']} — {c['description']}" for i, c in enumerate(candidates)
    )
    prompt = (
        "Score each link 0-10 for LEARNING/KNOWLEDGE utility to a practitioner "
        "building AI and data systems. High (7-10): concepts, how-tos, tutorials, "
        "GitHub repos, tools, deep technical explainers. Low (0-3): ephemeral news, "
        "product launches, funding/acquisitions, company announcements.\n\n"
        f"{listing}\n\n"
        'Respond with ONLY JSON: {"scores":[{"index":0,"score":7}, ...]}'
    )
    res = llm.complete(prompt, tier="mechanical", task="rank_links",
                       schema={"scores": []}, max_tokens=1024)
    if not res["ok"]:
        raise RuntimeError(res["error"] or "llm router unavailable")
    text = res["text"]
    data = json.loads(text[text.index("{"): text.rindex("}") + 1])
    scores = {int(s["index"]): int(s["score"]) for s in data["scores"]}
    return [max(0, min(10, scores.get(i, 0))) for i in range(len(candidates))]


def score_candidates(candidates: list[dict]) -> list[int]:
    load_env()
    try:
        return _llm_scores(candidates)
    except Exception:
        return [ce.heuristic_score(c["url"], c["description"]) for c in candidates]


def rank(candidates: list[dict], max_links: int = 10, floor: int = 4) -> list[dict]:
    """Score, sort by score desc (stable), then apply quality floor and cap.

    Returns one disposition per candidate:
      {url, description, score, fetch: bool, reason: 'low-utility'|'over-cap'|None}
    """
    if not candidates:
        return []
    scores = score_candidates(candidates)
    ranked = sorted(
        zip(range(len(candidates)), candidates, scores),
        key=lambda t: (-t[2], t[0]),
    )
    out, kept = [], 0
    for _, c, s in ranked:
        d = {"url": c["url"], "description": c["description"], "score": s}
        if s < floor:
            d.update(fetch=False, reason="low-utility")
        elif kept >= max_links:
            d.update(fetch=False, reason="over-cap")
        else:
            d.update(fetch=True, reason=None)
            kept += 1
        out.append(d)
    return out
