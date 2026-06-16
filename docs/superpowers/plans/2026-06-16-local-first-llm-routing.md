# Local-first LLM routing (Phase 1) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Cut recurring Claude cost by routing mechanical LLM tasks to a free local Ollama model, starting with email link-ranking, behind a small stdlib router with graceful fallback and a usage log.

**Architecture:** A `bin/llm.py` router exposes `complete(prompt, *, tier, ...)`. The `mechanical` tier calls local Ollama (`qwen2.5:3b`) over HTTP via stdlib `urllib`; on any failure it returns `ok=False` so the caller uses its own fallback. `bin/rank_links.py` is migrated to the router (local → its existing heuristic). Every call appends one line to `raw/.llm_usage.jsonl` for measurement. High-judgment work (agentic ingest, interactive ops) does NOT route here.

**Tech Stack:** Python 3.12 stdlib (`urllib`, `json`, `datetime`), Ollama (local, already installed), pytest. No new pip dependencies. `anthropic` SDK only on the opt-in Haiku middle tier (already a dependency via `rank_links`).

Spec: `docs/superpowers/specs/2026-06-16-local-first-llm-routing-design.md`.

---

## File structure

- **Create `bin/llm_config.py`** — tier→model map, Ollama host, timeouts, switches. One responsibility: configuration.
- **Create `bin/llm.py`** — the router: `complete()`, the Ollama HTTP provider, the opt-in Haiku fallback, usage logging. One responsibility: provider routing + fallback.
- **Create `bin/llm_usage.py`** — read `raw/.llm_usage.jsonl`, print a local-vs-Claude summary. One responsibility: reporting.
- **Modify `bin/rank_links.py`** — `_llm_scores` + `score_candidates` route through `bin/llm.py` instead of calling Anthropic directly.
- **Create `tests/test_llm.py`** — router + usage-log tests (Ollama HTTP mocked).
- **Modify `tests/test_rank_links.py`** — update the fallback test for the new router path.
- **Create `tests/test_llm_usage.py`** — summary reporting test.
- **Create `docs/llm-local-setup.md`** — Ollama service + model-pull setup.
- **Modify `.gitignore`** — ignore `raw/.llm_usage.jsonl`.

---

## Task 1: Config module

**Files:**
- Create: `bin/llm_config.py`
- Test: `tests/test_llm.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_llm.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import llm_config as cfg  # noqa: E402


def test_config_has_mechanical_tier_model():
    assert cfg.TIER_MODEL["mechanical"] == "qwen2.5:3b"
    assert cfg.TIER_TIMEOUT["mechanical"] >= 30
    assert cfg.OLLAMA_HOST.startswith("http")
    assert cfg.PREFER_LOCAL is True
    assert cfg.MECHANICAL_HAIKU_FALLBACK is False
    assert cfg.USAGE_LOG.endswith(".jsonl")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_llm.py::test_config_has_mechanical_tier_model -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'llm_config'`

- [ ] **Step 3: Write the config module**

```python
# bin/llm_config.py
#!/usr/bin/env python3
"""llm_config.py — configuration for the local-first LLM router (bin/llm.py)."""
from __future__ import annotations

import os

# Ollama HTTP endpoint (override with OLLAMA_HOST env var).
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

# Capability tier -> local Ollama model.
TIER_MODEL = {
    "mechanical": "qwen2.5:3b",   # fast classification/JSON on CPU
    "reasoning": "llama3.1:8b",   # slower; unattended only (no Phase-1 caller)
}

# Capability tier -> request timeout in seconds (CPU inference is slow).
TIER_TIMEOUT = {
    "mechanical": 60,
    "reasoning": 120,
}

# Master switch. When False, the router skips Ollama and returns ok=False
# immediately (callers fall back). Flip a single task back to Claude by
# editing the caller, or disable all local routing here.
PREFER_LOCAL = True

# Opt-in middle tier for the `mechanical` tier: if local fails and this is
# True, try Claude Haiku before giving up. Default off (truly $0: local -> caller heuristic).
MECHANICAL_HAIKU_FALLBACK = False
HAIKU_MODEL = "claude-haiku-4-5-20251001"

# Usage log (JSON lines), relative to repo root. Gitignored.
USAGE_LOG = "raw/.llm_usage.jsonl"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_llm.py::test_config_has_mechanical_tier_model -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add bin/llm_config.py tests/test_llm.py
git commit -m "feat(llm): config module for local-first router"
```

---

## Task 2: Router `complete()` — local happy path

**Files:**
- Create: `bin/llm.py`
- Test: `tests/test_llm.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_llm.py — append
import json
from unittest.mock import patch
import llm  # noqa: E402


class _FakeResp:
    """Minimal context-manager stand-in for urllib.request.urlopen()."""
    def __init__(self, payload):
        self._data = json.dumps(payload).encode()
    def __enter__(self):
        return self
    def __exit__(self, *a):
        return False
    def read(self):
        return self._data


def test_complete_mechanical_returns_local_text(tmp_path):
    payload = {"response": '{"scores":[{"index":0,"score":7}]}'}
    with patch.object(llm.urllib.request, "urlopen", return_value=_FakeResp(payload)):
        res = llm.complete("score these", tier="mechanical", task="unit",
                           log_path=tmp_path / "u.jsonl")
    assert res["ok"] is True
    assert res["provider"] == "ollama"
    assert res["model"] == "qwen2.5:3b"
    assert '"scores"' in res["text"]
    assert res["error"] is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_llm.py::test_complete_mechanical_returns_local_text -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'llm'`

- [ ] **Step 3: Write the router (local path only for now)**

```python
# bin/llm.py
#!/usr/bin/env python3
"""llm.py — local-first LLM router.

`complete(prompt, *, tier, ...)` routes mechanical tasks to a local Ollama
model and degrades gracefully (returns ok=False) so callers can fall back.
High-judgment work (agentic ingest, interactive ops) does NOT route here.
"""
from __future__ import annotations

import datetime
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

import llm_config as cfg  # same dir (bin/ is on sys.path for callers)

ROOT = Path(__file__).resolve().parent.parent


def _ollama_generate(prompt: str, model: str, *, system, timeout, as_json: bool) -> str:
    body = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.0},
    }
    if system:
        body["system"] = system
    if as_json:
        body["format"] = "json"
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        f"{cfg.OLLAMA_HOST}/api/generate",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    return payload.get("response", "")


def complete(prompt: str, *, tier: str, task: str | None = None, schema=None,
             system: str | None = None, max_tokens: int = 1024,
             temperature: float = 0.0, log_path=None) -> dict:
    """Route a completion to the cheapest capable provider for `tier`.

    Returns {"text", "provider", "model", "ok", "error"}. Never raises on a
    provider failure — returns ok=False so the caller can fall back.
    """
    model = cfg.TIER_MODEL.get(tier)
    timeout = cfg.TIER_TIMEOUT.get(tier, 60)
    result = {"text": "", "provider": None, "model": None, "ok": False, "error": None}
    started = time.monotonic()

    if cfg.PREFER_LOCAL and model:
        try:
            text = _ollama_generate(prompt, model, system=system,
                                    timeout=timeout, as_json=schema is not None)
            result = {"text": text, "provider": "ollama", "model": model,
                      "ok": True, "error": None}
        except (urllib.error.URLError, TimeoutError, OSError,
                json.JSONDecodeError, ValueError) as exc:
            result["error"] = f"ollama: {exc}"

    _log_usage(tier, task, result, time.monotonic() - started, log_path=log_path)
    return result


def _log_usage(tier, task, result, latency_s, *, log_path=None) -> None:
    path = Path(log_path) if log_path else (ROOT / cfg.USAGE_LOG)
    rec = {
        "at": datetime.datetime.now().isoformat(timespec="seconds"),
        "task": task,
        "tier": tier,
        "provider": result["provider"],
        "model": result["model"],
        "ok": result["ok"],
        "latency_ms": round(latency_s * 1000),
    }
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec) + "\n")
    except OSError:
        pass  # logging must never break the caller
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_llm.py -v`
Expected: PASS (both tests)

- [ ] **Step 5: Commit**

```bash
git add bin/llm.py tests/test_llm.py
git commit -m "feat(llm): router complete() with local Ollama happy path"
```

---

## Task 3: Graceful fallback (Ollama down / timeout)

**Files:**
- Modify: `bin/llm.py` (no change needed — verify behavior)
- Test: `tests/test_llm.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_llm.py — append
import urllib.error


def test_complete_returns_not_ok_when_ollama_down(tmp_path):
    boom = urllib.error.URLError("Connection refused")
    with patch.object(llm.urllib.request, "urlopen", side_effect=boom):
        res = llm.complete("x", tier="mechanical", task="unit",
                           log_path=tmp_path / "u.jsonl")
    assert res["ok"] is False
    assert res["provider"] is None
    assert "ollama" in res["error"]


def test_complete_returns_not_ok_on_timeout(tmp_path):
    with patch.object(llm.urllib.request, "urlopen", side_effect=TimeoutError("slow")):
        res = llm.complete("x", tier="mechanical", task="unit",
                           log_path=tmp_path / "u.jsonl")
    assert res["ok"] is False
    assert "ollama" in res["error"]


def test_prefer_local_false_skips_ollama(tmp_path, monkeypatch):
    monkeypatch.setattr(llm.cfg, "PREFER_LOCAL", False)
    # urlopen must NOT be called when PREFER_LOCAL is off
    with patch.object(llm.urllib.request, "urlopen", side_effect=AssertionError("called")):
        res = llm.complete("x", tier="mechanical", task="unit",
                           log_path=tmp_path / "u.jsonl")
    assert res["ok"] is False
    assert res["provider"] is None
```

- [ ] **Step 2: Run tests to verify they pass (behavior already implemented in Task 2)**

Run: `python3 -m pytest tests/test_llm.py -k "down or timeout or prefer_local" -v`
Expected: PASS for all three (Task 2's `complete()` already handles these). If any fails, fix `complete()` until green — do not weaken the test.

- [ ] **Step 3: Commit**

```bash
git add tests/test_llm.py
git commit -m "test(llm): lock graceful fallback on ollama down/timeout/disabled"
```

---

## Task 4: Usage log record

**Files:**
- Modify: `bin/llm.py` (no change — verify), `.gitignore`
- Test: `tests/test_llm.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_llm.py — append
def test_complete_appends_usage_log(tmp_path):
    log = tmp_path / "u.jsonl"
    payload = {"response": "ok"}
    with patch.object(llm.urllib.request, "urlopen", return_value=_FakeResp(payload)):
        llm.complete("x", tier="mechanical", task="rank_links", log_path=log)
    lines = log.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    rec = json.loads(lines[0])
    assert rec["task"] == "rank_links"
    assert rec["tier"] == "mechanical"
    assert rec["provider"] == "ollama"
    assert rec["ok"] is True
    assert "latency_ms" in rec and "at" in rec


def test_usage_log_records_failures_too(tmp_path):
    log = tmp_path / "u.jsonl"
    with patch.object(llm.urllib.request, "urlopen",
                      side_effect=urllib.error.URLError("down")):
        llm.complete("x", tier="mechanical", task="rank_links", log_path=log)
    rec = json.loads(log.read_text(encoding="utf-8").strip())
    assert rec["ok"] is False
    assert rec["provider"] is None
```

- [ ] **Step 2: Run tests to verify they pass (logging implemented in Task 2)**

Run: `python3 -m pytest tests/test_llm.py -k usage_log -v`
Expected: PASS (both). If not, fix `_log_usage` until green.

- [ ] **Step 3: Gitignore the real usage log**

Append to `.gitignore`:

```
# local-first LLM router usage log
raw/.llm_usage.jsonl
```

- [ ] **Step 4: Run the full suite**

Run: `python3 -m pytest -q`
Expected: PASS (all green; baseline + new llm tests)

- [ ] **Step 5: Commit**

```bash
git add tests/test_llm.py .gitignore
git commit -m "feat(llm): usage log record (success + failure); gitignore it"
```

---

## Task 5: Opt-in Haiku middle tier (mechanical)

**Files:**
- Modify: `bin/llm.py`
- Test: `tests/test_llm.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_llm.py — append
def test_haiku_fallback_used_when_enabled_and_local_fails(tmp_path, monkeypatch):
    monkeypatch.setattr(llm.cfg, "MECHANICAL_HAIKU_FALLBACK", True)
    with (
        patch.object(llm.urllib.request, "urlopen",
                     side_effect=urllib.error.URLError("down")),
        patch.object(llm, "_haiku", return_value='{"scores":[]}') as haiku,
    ):
        res = llm.complete("x", tier="mechanical", task="unit",
                           log_path=tmp_path / "u.jsonl")
    haiku.assert_called_once()
    assert res["ok"] is True
    assert res["provider"] == "anthropic"
    assert res["model"] == llm.cfg.HAIKU_MODEL


def test_haiku_not_used_when_disabled(tmp_path, monkeypatch):
    monkeypatch.setattr(llm.cfg, "MECHANICAL_HAIKU_FALLBACK", False)
    with (
        patch.object(llm.urllib.request, "urlopen",
                     side_effect=urllib.error.URLError("down")),
        patch.object(llm, "_haiku", side_effect=AssertionError("called")) as haiku,
    ):
        res = llm.complete("x", tier="mechanical", task="unit",
                           log_path=tmp_path / "u.jsonl")
    haiku.assert_not_called()
    assert res["ok"] is False
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_llm.py -k haiku -v`
Expected: FAIL — `module 'llm' has no attribute '_haiku'`

- [ ] **Step 3: Add the Haiku fallback to `complete()` and the `_haiku` helper**

In `bin/llm.py`, insert the fallback block in `complete()` immediately **before** the `_log_usage(...)` call:

```python
    # Opt-in middle tier for mechanical: try Claude Haiku if local failed.
    if not result["ok"] and tier == "mechanical" and cfg.MECHANICAL_HAIKU_FALLBACK:
        try:
            text = _haiku(prompt, system=system, max_tokens=max_tokens)
            result = {"text": text, "provider": "anthropic",
                      "model": cfg.HAIKU_MODEL, "ok": True, "error": result["error"]}
        except Exception as exc:  # noqa: BLE001 — fall through to ok=False
            result["error"] = f"{result['error']}; haiku: {exc}"
```

And add this helper near `_ollama_generate`:

```python
def _haiku(prompt: str, *, system: str | None, max_tokens: int) -> str:
    import anthropic  # only imported when the Haiku tier is actually used
    client = anthropic.Anthropic()
    kwargs = {"model": cfg.HAIKU_MODEL, "max_tokens": max_tokens,
              "messages": [{"role": "user", "content": prompt}]}
    if system:
        kwargs["system"] = system
    resp = client.messages.create(**kwargs)
    return "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_llm.py -k haiku -v`
Expected: PASS (both)

- [ ] **Step 5: Commit**

```bash
git add bin/llm.py tests/test_llm.py
git commit -m "feat(llm): opt-in Claude Haiku middle tier (default off)"
```

---

## Task 6: Usage summary CLI

**Files:**
- Create: `bin/llm_usage.py`
- Test: `tests/test_llm_usage.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_llm_usage.py
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import llm_usage as lu  # noqa: E402


def test_summarize_counts_by_provider(tmp_path):
    log = tmp_path / "u.jsonl"
    rows = [
        {"provider": "ollama", "ok": True, "latency_ms": 800, "tier": "mechanical"},
        {"provider": "ollama", "ok": True, "latency_ms": 1200, "tier": "mechanical"},
        {"provider": "ollama", "ok": False, "latency_ms": 30, "tier": "mechanical"},
        {"provider": "anthropic", "ok": True, "latency_ms": 500, "tier": "mechanical"},
    ]
    log.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    s = lu.summarize(log)
    assert s["total"] == 4
    assert s["by_provider"]["ollama"] == 3
    assert s["by_provider"]["anthropic"] == 1
    assert s["local_ok"] == 2
    assert s["local_fail"] == 1


def test_summarize_missing_file_is_empty(tmp_path):
    s = lu.summarize(tmp_path / "nope.jsonl")
    assert s["total"] == 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_llm_usage.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'llm_usage'`

- [ ] **Step 3: Write the summary module**

```python
# bin/llm_usage.py
#!/usr/bin/env python3
"""llm_usage.py — summarize raw/.llm_usage.jsonl (local vs Claude, ok rate)."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOG = ROOT / "raw" / ".llm_usage.jsonl"


def summarize(log_path=None) -> dict:
    path = Path(log_path) if log_path else DEFAULT_LOG
    by_provider: Counter = Counter()
    total = local_ok = local_fail = 0
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            total += 1
            by_provider[rec.get("provider")] += 1
            if rec.get("provider") == "ollama":
                local_ok += 1 if rec.get("ok") else 0
                local_fail += 0 if rec.get("ok") else 1
    return {"total": total, "by_provider": dict(by_provider),
            "local_ok": local_ok, "local_fail": local_fail}


def main(argv=None) -> int:
    s = summarize()
    claude = s["by_provider"].get("anthropic", 0)
    print(json.dumps({
        "total_calls": s["total"],
        "local_ollama": s["by_provider"].get("ollama", 0),
        "local_ok": s["local_ok"],
        "local_fail": s["local_fail"],
        "claude": claude,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_llm_usage.py -v`
Expected: PASS (both)

- [ ] **Step 5: Commit**

```bash
git add bin/llm_usage.py tests/test_llm_usage.py
git commit -m "feat(llm): usage summary CLI (local vs Claude)"
```

---

## Task 7: Migrate `rank_links.py` to the router

**Files:**
- Modify: `bin/rank_links.py`
- Modify: `tests/test_rank_links.py`

- [ ] **Step 1: Write the failing tests (new router behavior)**

Append to `tests/test_rank_links.py`:

```python
def test_score_candidates_uses_router_local(monkeypatch):
    """When the router returns ok=True with scores JSON, those scores are used."""
    monkeypatch.setattr(rl, "load_env", lambda *a, **k: None)
    import llm
    monkeypatch.setattr(
        llm, "complete",
        lambda *a, **k: {"text": '{"scores":[{"index":0,"score":9}]}',
                         "provider": "ollama", "model": "qwen2.5:3b",
                         "ok": True, "error": None},
    )
    scores = rl.score_candidates([{"url": "https://x/y", "description": "deep tutorial"}])
    assert scores == [9]


def test_score_candidates_falls_back_to_heuristic_when_router_not_ok(monkeypatch):
    """When the router returns ok=False, fall back to the heuristic scorer."""
    monkeypatch.setattr(rl, "load_env", lambda *a, **k: None)
    import llm
    monkeypatch.setattr(
        llm, "complete",
        lambda *a, **k: {"text": "", "provider": None, "model": None,
                         "ok": False, "error": "ollama: down"},
    )
    scores = rl.score_candidates([{"url": "https://github.com/x/y", "description": "tutorial"}])
    assert scores[0] >= 8  # heuristic path for a GitHub tutorial
```

Also UPDATE the existing `test_rank_fallback_used_without_key` (the old API-key gate is gone) so it drives the router to `ok=False`:

```python
def test_rank_fallback_used_without_key(monkeypatch):
    monkeypatch.setattr(rl, "load_env", lambda *a, **k: None)
    import llm
    monkeypatch.setattr(
        llm, "complete",
        lambda *a, **k: {"text": "", "provider": None, "model": None,
                         "ok": False, "error": "ollama: down"},
    )
    scores = rl.score_candidates([{"url": "https://github.com/x/y", "description": "tutorial"}])
    assert scores[0] >= 8  # heuristic path
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_rank_links.py -k "router or fallback" -v`
Expected: FAIL — `score_candidates` still calls Anthropic directly / gates on the key; the router patch has no effect.

- [ ] **Step 3: Rewrite `_llm_scores` and `score_candidates` to use the router**

In `bin/rank_links.py`, replace `_llm_scores` and `score_candidates` with:

```python
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
```

(`load_env` and the `import anthropic`/`RANK_MODEL` usages move out of `rank_links` — the router owns provider access now. Leave `RANK_MODEL`/`load_env` definitions in place; `load_env` is still imported by `scheduled_run.py`. Remove the now-unused `import anthropic` and the `os.environ.get("ANTHROPIC_API_KEY")` gate.)

- [ ] **Step 4: Run the rank_links + full suite**

Run: `python3 -m pytest tests/test_rank_links.py -v`
Expected: PASS (all, including the two new tests and the updated fallback test)

Run: `python3 -m pytest -q`
Expected: PASS (whole suite green)

- [ ] **Step 5: Commit**

```bash
git add bin/rank_links.py tests/test_rank_links.py
git commit -m "feat(llm): route rank_links link-scoring through the local-first router"
```

---

## Task 8: Pull the model, smoke-test the real path, document setup

**Files:**
- Create: `docs/llm-local-setup.md`

This task has no pytest — it provisions the local model and documents operations.

- [ ] **Step 1: Pull the Tier-0 model**

Run: `ollama pull qwen2.5:3b`
Expected: download completes; `ollama list` shows `qwen2.5:3b` (~2 GB).

- [ ] **Step 2: Ensure the Ollama server runs as a background service**

Run: `brew services start ollama` (or confirm `ollama serve` is running).
Verify: `curl -s http://localhost:11434/api/tags | head -c 80` returns JSON (not a connection error).

- [ ] **Step 3: Live smoke-test the router against real Ollama**

Run:
```bash
cd /Users/jonasblasques/Dev/corpus
python3 -c "import sys; sys.path.insert(0,'bin'); import llm; r=llm.complete('Reply with ONLY JSON {\"ok\":true}', tier='mechanical', task='smoke', schema={}); print(r['provider'], r['ok'], repr(r['text'])[:120])"
```
Expected: `ollama True '...{"ok": true}...'` (or similar JSON). Confirms the real local path works end-to-end.

- [ ] **Step 4: Live smoke-test rank_links end-to-end**

Run:
```bash
python3 -c "import sys; sys.path.insert(0,'bin'); import rank_links as rl; print(rl.rank([{'url':'https://github.com/x/y','description':'deep RAG tutorial'},{'url':'https://news.example/funding','description':'startup raises Series A'}], max_links=10, floor=4))"
```
Expected: the tutorial scores high (`fetch: True`), the funding news scores low (`fetch: False, reason: low-utility`). Then check the usage log recorded a local call:
```bash
python3 bin/llm_usage.py
```
Expected: JSON summary with `local_ollama >= 1`.

- [ ] **Step 5: Write `docs/llm-local-setup.md`**

```markdown
# Local LLM (Ollama) setup

The corpus tooling routes mechanical LLM tasks (currently email link-ranking)
to a local Ollama model via `bin/llm.py`, falling back gracefully to Claude or
a heuristic if Ollama is unavailable. This keeps recurring Claude cost down and
keeps content on-machine.

## One-time setup
1. Install Ollama (already installed here): https://ollama.com
2. Pull the Tier-0 model: `ollama pull qwen2.5:3b`
3. Run Ollama as a background service so the daily job can reach it:
   `brew services start ollama`

## How it routes
- `bin/llm_config.py` maps capability tiers to models and holds the switches.
- `mechanical` tier → `qwen2.5:3b` (local). On failure → caller's fallback
  (rank_links → heuristic). Optional Claude Haiku middle tier: set
  `MECHANICAL_HAIKU_FALLBACK = True`.
- High-judgment work (agentic ingest, interactive ops) does NOT route here.
- Disable all local routing: set `PREFER_LOCAL = False` in `bin/llm_config.py`.

## Measuring savings
`python3 bin/llm_usage.py` prints how many calls ran local vs Claude
(reads the gitignored `raw/.llm_usage.jsonl`).
```

- [ ] **Step 6: Commit**

```bash
git add docs/llm-local-setup.md
git commit -m "docs(llm): local Ollama setup + operations"
```

---

## Done criteria

- `python3 -m pytest -q` fully green (router, usage, rank_links, plus existing suite).
- `ollama list` shows `qwen2.5:3b`; the live smoke tests in Task 8 pass.
- `bin/rank_links.py` calls no provider directly — it routes through `bin/llm.py`.
- `python3 bin/llm_usage.py` reports local Ollama calls after a real rank.
- Agentic ingest and interactive ops are untouched (still Claude).
