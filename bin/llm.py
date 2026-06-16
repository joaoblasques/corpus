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
