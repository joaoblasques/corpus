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

# Opt-in HOSTED free fallback for the `mechanical` tier (default off). OpenRouter
# is OpenAI-compatible and serves ":free" open models — useful as a faster
# alternative when local Ollama is down/slow. Requires OPENROUTER_API_KEY in the
# env. Tried AFTER local Ollama, BEFORE Haiku.
#   PRIVACY: free models may be logged / trained on by the downstream provider.
#   Do NOT enable for private corpus content unless you've reviewed OpenRouter's
#   data settings (opt out of training; restrict to no-logging providers).
MECHANICAL_OPENROUTER_FALLBACK = False
OPENROUTER_HOST = os.environ.get("OPENROUTER_HOST", "https://openrouter.ai/api/v1")
OPENROUTER_MODEL = "meta-llama/llama-3.3-70b-instruct:free"

# Opt-in middle tier for the `mechanical` tier: if local fails and this is
# True, try Claude Haiku before giving up. Default off (truly $0: local -> caller heuristic).
MECHANICAL_HAIKU_FALLBACK = False
HAIKU_MODEL = "claude-haiku-4-5-20251001"

# Usage log (JSON lines), relative to repo root. Gitignored.
USAGE_LOG = "raw/.llm_usage.jsonl"
