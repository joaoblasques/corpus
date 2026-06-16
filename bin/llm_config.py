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
