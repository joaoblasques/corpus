---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-beyond-one-model-fusion-in-vllm-semantic-router-9f81985e.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-vllm-semantic-router-v0-3-themis-from-signals-to-stateful-pr-fd130560.md
    channel: web
    ingested_at: 2026-07-02
aliases:
  - vLLM Semantic Router
  - vLLM-SR
  - vllm-sr
  - Semantic Router
  - Themis
  - Iris
  - Athena
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-02
updated: 2026-07-02
---

# vLLM Semantic Router

**TL;DR.** vLLM Semantic Router (vLLM-SR) is a routing control plane sitting in front of one or more model backends. It extracts **signals** from a request, normalizes them into **projections**, matches a **decision** (a named routing policy), runs a model-selection **algorithm**, and serves the request through a selected backend — while recording a replayable trace of the whole path. Releases are codenamed (Iris → Athena → Themis, v0.3); as of Themis it ranks #1 on the RouterArena leaderboard (weighted Arena Score 75.4) [^src2].

## Core pipeline (the v0.3 "Themis" contract)

```
signals → projections → decisions → algorithms → models
```

| Layer | What it owns |
|---|---|
| Signal | Extract evidence from the request/response/tools/language/domain/context/modality/identity/safety classifiers |
| Projection | Normalize raw evidence into policy-ready concepts (e.g. `support_fast`, `support_escalated`) |
| Decision | Match named routing policies by priority + explainable conditions |
| Algorithm | Choose among candidate models inside a matched decision |
| Model | Serve the request via the selected backend alias/provider |

This contract is consistent across the router core, CLI, dashboard, DSL, Helm chart, and Kubernetes deployment surfaces as of v0.3 [^src2].

## Fusion (Mixture-of-Models primitive)

**Fusion** lets a routing decision run a panel of models concurrently, have a **judge model** analyze consensus/contradictions/gaps, and synthesize one user-facing answer — while keeping policy, config, and traces inside the router [^src1].

- Entry paths: `model: "vllm-sr/auto"` (router decides whether to use Fusion at all), `model: "vllm-sr/fusion"` (Fusion-only, still signal-driven), or a request-level `plugins: [{id: "fusion", ...}]` override [^src1].
- Execution stages: resolve policy → run panel (concurrent, bounded by `max_concurrent`) → handle failures per `on_error: skip|fail` → judge analyzes disagreement → synthesis call returns one response (or an OpenAI-compatible `tool_calls` response) → trace + aggregated token usage returned [^src1].
- Fusion-registered model slugs cannot themselves be used as judge/panel models, preventing recursive Fusion calls [^src1].
- Motivated by OpenRouter's Fusion launch: on OpenRouter's DRACO benchmark, "Fusion: Fable 5 + GPT-5.5, synthesized by Opus 4.8" scored 69.0% vs. 65.3% for solo Fable 5, and a *budget* panel (Gemini 3 Flash + Kimi K2.6 + DeepSeek V4 Pro, synthesized by Opus 4.8) scored 64.7% — recovering quality a single cheap model lacks [^src1]. These are OpenRouter's numbers, not a vLLM-SR benchmark; vLLM-SR treats this as external evidence that model-panel composition deserves to be a first-class serving primitive, not a claim about its own Fusion quality [^src1].
- Framed explicitly as "a decision, not a default" — Fusion adds panel + judge + synthesis latency/cost, so the router (not a global setting) decides per-request whether it's worth it [^src1].

## Session-Aware Agentic Routing (SAAR)

New in Themis: router-owned session memory + hard locks that prevent unsafe model switches mid-session for agentic/tool-loop traffic [^src2].

- Problem: single-turn routing asks "which model for this prompt?"; agentic routing must also ask "is it safe to switch models inside this session right now?" [^src2]
- `session_aware` selection weighs quality gap, switch margin, stay bias, prefix locality, and remaining-turn priors before allowing a switch [^src2].
- Hard locks block switches during active tool loops or provider-state continuations (e.g. a provider-managed continuation ID must not be sent to a different backend) [^src2].
- Particularly relevant for coding agents / long-horizon tool loops, where losing prefix-cache locality or breaking a tool-loop mid-flight is costly [^src2].

## Themis release surface (v0.2 → v0.3 delta)

- **Canonical v0.3 config contract** — single `config.yaml` shape replaces overlapping Docker/dashboard/Helm/CRD layouts; `vllm-sr init` removed in favor of `vllm-sr serve` (dashboard-first) or `vllm-sr config migrate`/`config import` [^src2].
- **Broadened signal catalog** — 17 signal families including `authz`, `complexity`, `jailbreak`, `pii`, `kb` (knowledge-base), `modality` (AR/diffusion/multimodal), `event`, `fact_check` [^src2].
- **Protocol compatibility as a release surface** — native Anthropic `/v1/messages` ingress, Anthropic streaming via OpenAI SSE translation, response headers flagging lossy translation [^src2].
- **Dashboard as an operator console** — topology dry-run, replay-backed insights, policy version lifecycle (shadow/activate/revert) [^src2].
- **Long-context routing gets cheaper** — online-calibrated context-token estimation; chunked attention for the native mmBERT embedding path to bound memory on long inputs; named prompt-compression profiles (`default`, `coding`, `medical`, `security`, `multi_turn`) scoped only to signal evaluation (the user's actual prompt still reaches the serving model unmodified) [^src2].
- **RouterArena #1** — 75.4 weighted Arena Score, 76.0 accuracy, $0.11 cost/1K queries, 73.1 robustness, ahead of Sqwish Router, AgentForge Router, Nadir Router [^src2].
- **Next release ("Hermes")** — goal is a self-improving router: closed loop of GPU-scale performance research → DSL recipe tuning → codebase/encoder-model fine-tuning, with every change reviewable/replayable/rollback-safe [^src2].

## Related

- [[ai-engineering/vllm|vLLM]] — the inference-serving engine vLLM-SR routes requests to
- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] — Fusion's panel-judge-synthesis pattern is a Mixture-of-Models variant of multi-agent coordination
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [Beyond One Model: Fusion in vLLM Semantic Router](../../raw/web/web-beyond-one-model-fusion-in-vllm-semantic-router-9f81985e.md) — vLLM blog, 2026-06-16
[^src2]: [vLLM Semantic Router v0.3 Themis: From Signals to Stateful Production Routing](../../raw/web/web-vllm-semantic-router-v0-3-themis-from-signals-to-stateful-pr-fd130560.md) — vLLM blog, 2026-06-05
