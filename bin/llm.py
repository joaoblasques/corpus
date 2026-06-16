#!/usr/bin/env python3
"""llm.py — local-first LLM router.

`complete(prompt, *, tier, ...)` routes mechanical tasks to a local Ollama
model and degrades gracefully (returns ok=False) so callers can fall back.
High-judgment work (agentic ingest, interactive ops) does NOT route here.
"""
from __future__ import annotations

import datetime
import json
import os
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


def _openrouter_generate(prompt: str, model: str, *, system, timeout, as_json: bool) -> str:
    """Call OpenRouter's OpenAI-compatible chat endpoint with a `:free` model.

    Needs OPENROUTER_API_KEY in the env. Stdlib urllib (no new dependency).
    """
    messages = ([{"role": "system", "content": system}] if system else []) + \
               [{"role": "user", "content": prompt}]
    body = {"model": model, "messages": messages, "temperature": 0.0}
    if as_json:
        body["response_format"] = {"type": "json_object"}
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        f"{cfg.OPENROUTER_HOST}/chat/completions",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY', '')}",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    return payload["choices"][0]["message"]["content"]


def _haiku(prompt: str, *, system: str | None, max_tokens: int) -> str:
    import anthropic  # only imported when the Haiku tier is actually used
    client = anthropic.Anthropic()
    kwargs = {"model": cfg.HAIKU_MODEL, "max_tokens": max_tokens,
              "messages": [{"role": "user", "content": prompt}]}
    if system:
        kwargs["system"] = system
    resp = client.messages.create(**kwargs)
    return "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")


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

    # Opt-in hosted free fallback for mechanical: OpenRouter (needs an API key).
    if (not result["ok"] and tier == "mechanical"
            and cfg.MECHANICAL_OPENROUTER_FALLBACK
            and os.environ.get("OPENROUTER_API_KEY")):
        try:
            text = _openrouter_generate(prompt, cfg.OPENROUTER_MODEL, system=system,
                                        timeout=timeout, as_json=schema is not None)
            result = {"text": text, "provider": "openrouter",
                      "model": cfg.OPENROUTER_MODEL, "ok": True, "error": result["error"]}
        except Exception as exc:  # noqa: BLE001 — fall through to next fallback
            result["error"] = f"{result['error']}; openrouter: {exc}"

    # Opt-in middle tier for mechanical: try Claude Haiku if local failed.
    if not result["ok"] and tier == "mechanical" and cfg.MECHANICAL_HAIKU_FALLBACK:
        try:
            text = _haiku(prompt, system=system, max_tokens=max_tokens)
            result = {"text": text, "provider": "anthropic",
                      "model": cfg.HAIKU_MODEL, "ok": True, "error": result["error"]}
        except Exception as exc:  # noqa: BLE001 — fall through to ok=False
            result["error"] = f"{result['error']}; haiku: {exc}"

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
