# Local-first LLM routing — design

> Date: 2026-06-16 · Status: approved (brainstorm) · Scope committed: **Phase 1**

## Problem & goal

The corpus system makes paid Claude API calls in several places. The goal is to **cut recurring Claude cost by routing mechanical LLM tasks to free, local, open-source models** (Ollama on the user's MacBook), while keeping Claude for high-judgment work where quality and safety matter.

**Stance (decided): surgical.** Keep Claude for the agentic ingest's safe-subset gating and for interactive ingest/query quality. Move only mechanical/classification tasks (link ranking, structured extraction, clustering hints, short summaries) to local models.

**Deployment (decided): local-first via Ollama.** Truly $0, fully private (corpus content never leaves the machine), always available when the Mac is awake (which it is for the 08:00 launchd job). Hosted free tiers are explicitly out of scope (privacy + rate-limit fragility).

## Current LLM-call surface

| Call site | Today | Judgment | Disposition |
|---|---|---|---|
| `bin/rank_links.py` — score email links 0–10 | `claude-haiku-4-5` (Anthropic SDK), heuristic fallback | low | **Phase 1: route to local** |
| `bin/scheduled_run.py::run_ingest` — daily agentic ingest | `claude --print` (Opus 4.8, agentic) | high | **Stays on Claude** (sub-steps → Phase 2) |
| Interactive `/ingest`, `/query`, `/lint` | session model (Opus) | high | Stays on Claude |

## Hardware reality (shapes model choices)

- **Intel MacBook Pro**, i5 (4 cores), **16 GB**, **CPU-only** inference (no Apple-Silicon/Metal GPU). Small models run, but slowly — fine for **unattended/batch** paths, too slow for interactive latency.
- Ollama already installed (v0.12.6); `llama3.1:8b` (4.9 GB) already pulled.
- Implication: route only **unattended/batch** tasks to local; keep interactive ops on Claude.

## Architecture

### The router — `bin/llm.py` (stdlib only)

```python
complete(prompt, *, tier, schema=None, system=None,
         max_tokens=1024, temperature=0.0) -> LLMResult
#   LLMResult = {text, provider, model, ok: bool, error}
```

**Capability tiers → provider chain** (config-driven):
- **`mechanical`** (score / classify / extract-JSON / short summary) → **local Ollama** → `ok=False`. The router does NOT silently call Claude for a mechanical task; the *caller* owns its domain fallback (e.g. `rank_links` → `heuristic_score`). An optional middle tier (Claude Haiku) can be enabled per-config (default off).
- **`reasoning`** (light multi-step) → local 8B → optional Claude Haiku. (No call sites in Phase 1.)
- **`judgment`** (agentic ingest, interactive) → Claude only — these do **not** route through `bin/llm.py`; they stay exactly as they are today.

**Provider — Ollama client.** Calls `POST http://localhost:11434/api/generate` with `format: "json"` for structured output, via stdlib `urllib` (no new dependency). Degrades gracefully and returns `ok=False` (never raises into the caller) on: server down (connection refused), model not pulled (404), timeout (generous, e.g. 120 s — the CPU is slow), or malformed response.

**Config — `bin/llm_config.py`** (a code module, not `corpus/_config.md` which is corpus-operational config): maps `tier → model`, Ollama host/port, per-tier timeout, a global `prefer_local` switch, and the optional `mechanical_haiku_fallback` flag (default off). Flipping a task back to Claude is a one-line change.

**Invariant:** the router degrades to a working fallback at every step. A down Ollama or a bad local result never breaks collection or ingest — it costs a Claude call (if configured) or uses the caller's heuristic.

### Model assignments (this hardware)

- **Tier-0 `mechanical` → `qwen2.5:3b`** (~2 GB) — pull it; fast on CPU, strong at classification + JSON. Used for link scoring (and future extraction).
- **Tier-1 `reasoning` → `llama3.1:8b`** (already pulled) — slower on CPU, unattended only. No Phase-1 caller.
- RAM budget: 3B (~2 GB) is comfortable alongside the OS + daily job.

### Ollama as a background service

The daily job needs the Ollama server running. Run it as a background service (`brew services start ollama` or its launch agent). The router falls back if it's ever down, so this is a performance/cost optimization, not a hard dependency.

## Phase 1 scope (committed)

1. **`bin/llm.py`** — the router + Ollama provider + tier config, stdlib-only, graceful fallback.
2. **`bin/llm_config.py`** — tier→model map, host, timeouts, switches.
3. **Migrate `bin/rank_links.py`** — `_llm_scores` routes through `complete(tier="mechanical")` on `qwen2.5:3b`; on `ok=False`, fall through to the existing `heuristic_score`. Default chain: **local → heuristic** (truly $0); Haiku middle tier opt-in via config.
4. **Usage log** — every router call appends one JSON line to gitignored `raw/.llm_usage.jsonl`: `{at, task, tier, provider, model, ok, latency_ms}`. A tiny `bin/llm_usage.py summary` reports local-vs-Claude counts over a window, so savings are measurable.
5. **Pull `qwen2.5:3b`** + document running Ollama as a service.

## Roadmap (not in Phase 1)

- **Phase 2 — ingest pre-survey.** A local model builds the Phase-1 condensed records (title + tags + first paragraph) + cluster/entity hints for the ≤`max` sources into a scratch file the `/ingest-auto` skill reads instead of re-deriving — shrinking Claude's token load per daily ingest. Claude keeps all judgment + gating.
- **Phase 3 — `/query` retrieval via local embeddings.** `nomic-embed-text` (Ollama) for retrieval instead of LLM-over-index; Claude still writes the cited answer.

## Testing

- **Router** (mock `urllib`, no live Ollama): success → `ok=True` + parsed text; connection-refused / timeout / 404 → `ok=False`; `format: json` parsing.
- **`rank_links`**: extend existing tests — local-success path (router returns scores) and local-fail → heuristic path; existing heuristic tests stay green.
- A separate manual smoke test exercises the real Ollama path.

## Observability

`raw/.llm_usage.jsonl` + `bin/llm_usage.py summary` answer "how many calls went local vs Claude, and how fast" — the feedback loop that proves the cost reduction.

## Non-goals / risks

- **Non-goal:** driving the agentic ingest with a local model (against the surgical stance; an 8B CPU model can't reliably do safe-subset gating or drive Claude Code's harness).
- **Non-goal:** hosted free-tier APIs (privacy + rate-limit fragility).
- **Risk — local quality:** a small model may score links worse than Haiku. Mitigation: the usage log + spot-checks; per-task config flip back to Claude/Haiku if quality disappoints.
- **Risk — CPU latency:** local calls add seconds–minutes; acceptable because only unattended/batch paths route local.
- **Risk — Ollama not running:** graceful fallback means correctness is preserved; only the cost saving is lost until the service is back.
