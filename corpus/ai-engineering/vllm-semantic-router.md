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
  - path: raw/web/web-session-aware-agentic-routing-continuity-aware-model-selecti-1950138f.md
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

New in Themis: router-owned session memory + hard locks that prevent unsafe model switches mid-session for agentic/tool-loop traffic [^src2][^src3].

- Problem: single-turn routing asks "which model for this prompt?"; agentic routing must also ask "is it safe to switch models inside this session right now?" [^src2][^src3]
- `session_aware` selection weighs quality gap, switch margin, stay bias, prefix locality, and remaining-turn priors before allowing a switch [^src2].
- Hard locks block switches during active tool loops or provider-state continuations (e.g. a provider-managed continuation ID must not be sent to a different backend) [^src2].
- Particularly relevant for coding agents / long-horizon tool loops, where losing prefix-cache locality or breaking a tool-loop mid-flight is costly [^src2].

### SAAR design (five pieces of router memory + policy)

SAAR keeps the existing signal → decision → algorithm pipeline unchanged and adds a session-control layer around the result [^src3]:

| Piece | What it stores or decides | Why it matters |
|---|---|---|
| Router memory | Last physical model, matched decision, phase, switch count, idle time, cache evidence, replay metadata | Session context without becoming application/user memory |
| Hard locks | Block switching during active tool loops or non-portable provider-managed state | Correctness before cost/quality optimization |
| Reset boundaries | Allow reselection after idle timeout or decision drift | Prevents SAAR from degrading into plain sticky sessions |
| Switch economics | Prices handoff cost, switch history, remaining-turn priors, prefix-cache checkout | Makes switching asymmetric across model tiers and session lengths |
| Replay traces | Records why the router stayed, switched, or refused to switch | Makes a logical model like `auto` inspectable/debuggable |

**Two hard locks, treated as correctness boundaries (not cost tradeoffs)**: (1) *tool-loop continuity* — if a physical model asked for a tool call, the tool result must return to that same physical model, since it's part of a local execution loop, not a fresh prompt; (2) *provider-managed state* — a non-portable continuation ID belonging to one backend must not be silently routed to a different backend [^src3]. **Two reset boundaries reopen selection**: idle timeout (continuity value decays after a pause) and decision drift (the matched routing decision changes, e.g. user moves from code editing to synthesis) [^src3].

SAAR also prices a **cached-input checkout delta** — the gap between normal and cached-input price for a candidate physical model — so a long, warm 40-turn session on a frontier model is treated very differently from a cheap short retry on a small model when deciding whether a switch is worth it [^src3]. Backend-reported cached tokens are kept separate from router-estimated reuse and are never rewritten upstream [^src3].

### Evaluated results

Across a 21,600-turn deterministic policy matrix (balanced/tool-heavy/frontier-heavy/idle-heavy/provider-state-heavy/drift-heavy workloads, 5 seeds × 40 sessions × 18 turns): full SAAR cuts model switches 79.29% vs. single-turn routing and eliminates all 3,836 unsafe switches, at 78.71% estimated cost reduction [^src3].

| Policy | Switches | Unsafe switches | Cost reduction |
|---|---|---|---|
| Single-turn | 9,709 | 3,836 | 0.00% |
| Sticky session | 340 | 0 | 98.65% (quality delta -0.1433) |
| Full SAAR | 2,011 | 0 | 78.71% (quality delta -0.0453) |

SAAR is explicitly **not** just sticky-session routing: an ablation shows removing the drift-reset or idle-boundary mechanisms causes SAAR to "over-stick" after task drift or natural pauses, while removing the tool-lock or provider-state-lock mechanisms reintroduces unsafe switches (760 and 200 respectively) — each of SAAR's five pieces is independently load-bearing [^src3]. In live AMD ROCm serving (2,896 requests across balanced/stateful/idle workloads) and fault-injection tests (repeated HTTP 503s across provider-state/tool-loop/topic-drift phases), SAAR preserved **0 observed continuity violations**, with 100% session recovery after injected backend faults [^src3].

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
[^src3]: [Session-Aware Agentic Routing: Continuity-Aware Model Selection for Long-Horizon LLM Agents](../../raw/web/web-session-aware-agentic-routing-continuity-aware-model-selecti-1950138f.md) — vLLM blog, 2026-06-02
