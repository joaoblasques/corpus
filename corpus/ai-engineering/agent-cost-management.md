---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/managing-agentic-ai-costs-at-scale.md
    channel: web
    ingested_at: 2026-06-16
  - path: raw/web/web-how-to-stop-hitting-claude-usage-limits.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/github/github-mnfst-manifest.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-n8rP6Ceskm4.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-9ToOfgZ4qqQ-i-stopped-hitting-claude-code-usage-limits-here-s-how.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/email/email-2026-06-21-how-to-run-claude-code-for-free.md
    channel: email
    ingested_at: 2026-06-25
aliases:
  - agentic AI costs
  - agent cost management
  - agentic cost at scale
  - cost per completed task
  - re-sent context
  - token multiplier
  - prompt caching
  - token conservation
  - usage limits
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-16
updated: 2026-06-25
---

# Agent Cost Management

**TL;DR.** Agentic AI economics differ fundamentally from per-token chatbot pricing: the relevant unit is "cost per completed task," not cost per prompt, because a single agentic task can trigger 10–20 model calls and consume 5–30× more tokens than a chatbot query [^src1]. Per-token intelligence cost dropped 98% since early 2024, yet enterprise bills still rise — because consumption growth outpaces falling unit cost [^src1]. Uber's CTO Praveen Neppalli Naga: "I'm back to the drawing board, because the budget I thought I would need is blown away already." [^src1] Gartner forecasts 40% of AI agent projects cancelled by 2027 due to cost overruns alone [^src1].

> Note: source is a CockroachDB vendor post; the database-as-control-loop framing at the end is product positioning. The cost mechanics it documents are corroborated by cited third-party research (Gartner, Stanford, Chroma, Menlo, Ramp).

## Why current budgets break

A chatbot query triggers one inference call; an agentic workflow reasons iteratively, calls tools, verifies, and self-corrects — 10–20 model calls per task [^src1]. Gartner's March 2026 analysis puts agentic models at 5–30× more tokens per task than a standard chatbot, a multiplier teams discover "only after their production bills arrived" [^src1]. Enterprise AI inference now represents 85% of total AI budgets [^src1]. Uber's [[ai-engineering/claude-code|Claude Code]] adoption jumped 32%→84% of its 5,000-engineer org (Dec 2025→Mar 2026); by April the annual AI budget was gone, with monthly API costs of $500–$2,000 per engineer [^src1]. Cheaper tokens won't lower bills: "Chief Product Officers should not confuse the deflation of commodity tokens with the democratization of frontier reasoning." [^src1]

## The four cost layers

Inference is only ~20% of total cost of ownership; the majority "lives in what surrounds the model" [^src1].

### Cost 1 — Inference and the re-sent context problem

Re-sent context is the repeated transmission of system prompts, tool definitions, instructions, and state history across calls in one workflow — "teams often pay for the model to reprocess information it has already seen." [^src1] Stanford Digital Economy Lab (2025) found **re-sent context accounts for 62% of total agent inference bills** [^src1]. It applies to proprietary APIs (per-token) and self-hosted models alike (GPU compute, memory pressure, lower throughput) [^src1]. Unit *price* fell ~$10→$2.50 per million tokens in a year (Ramp), but "the problem is not unit cost... the problem is unit count" — one team cut monthly API costs $40K→$24K purely by auditing usage and routing simpler subtasks to cheaper [[ai-engineering/claude-models|models]] [^src1].

### Cost 2 — Context management and context rot

[[ai-engineering/context-window-management|Context rot]] is output-quality degradation as context grows; Chroma's 2025 research tested 18 frontier models and "every single one gets worse as input length increases." [^src1] It is architectural — transformer attention scales as n² pairwise relationships — and degrades accuracy 30%+ in mid-window positions, noticeable after 20–30 turns [^src1]. A 1M-token window does not solve it; rot is distinct from context-window overflow and a 200K model can degrade significantly at 50K tokens [^src1]. Four levers [^src1]:

- **Compaction** — near the limit, summarize and restart with the summary (Claude Code preserves decisions/outstanding tasks while shedding tool outputs).
- **Layered tool calling** — tiered [[ai-engineering/tool-calling|tools]] so a coordinator holds high-level tools and activates focused sub-agents; a flat 40-tool design sends all 40 schemas every call.
- **Just-in-time retrieval** — pull context only when signaled; keeps working context under 8K tokens.
- **Sub-agent isolation** — [[ai-engineering/multi-agent-systems|sub-agents]] with clean windows return 1,000–2,000-token summaries.

"The challenge is no longer writing the right prompt. It is deciding what goes into context at every step." [^src1]

### Cost 3 — Retrieval (RAG) costs

[[ai-engineering/rag|RAG]] stack costs are "systematically underestimated" [^src1]: embeddings 3–8% of visible inference spend, vector-DB hosting/queries 5–12%, plus re-embedding/re-indexing (budget 20% of monthly) and data cleaning/preprocessing (30–50% of total RAG project cost) [^src1]. The RAG-vs-long-context trade-off flips with volume: at low volume a full RAG pipeline can exceed sending large context directly, but at high volume retrieving a few thousand tokens beats sending 1M per request — and for user-facing work, speed settles it [^src1]. Menlo Ventures shows RAG adoption rising 31%→51% in a year, so "RAG is dead" is contradicted by production data [^src1].

### Cost 4 — Orchestration and the hidden 80%

Beyond inference: orchestration (planning, retries, state), [[ai-engineering/agent-evaluation|evaluation/monitoring]] (LLM-as-judge at $0.01–$0.10 per eval, 100+ test cycles), governance/compliance (audit logs, human-in-the-loop), and **runaway loops** — "Autonomy is the main cost amplifier"; uncontrolled retries drive runaway spend, so escalate to humans at defined thresholds [^src1]. Real examples: OpenClaw creator Peter Steinberger spent $1.3M over 30 days (Fast Mode); one user burned 10 billion tokens over eight months on a $100/month plan; a healthcare firm's costs jumped $12K→$68K in six weeks from one agent's retrieval fault pulling documents 8× too large [^src1].

## Highest-return move: prompt caching

Prompt caching "delivers the highest return for the least implementation effort. Start here." [^src1] On Anthropic's platform, cache reads on Claude Sonnet 4.6 cost $0.30/M vs $3.00/M standard — a 90% reduction — with break-even at 2.3 reuses of the same prefix within the 1-hour TTL [^src1]. Structure prompts static-content-first, dynamic content last [^src1].

**The cache-killer:** timestamps and session IDs in the prefix destroy cache performance [^src1]. A team with a 60K-token system prompt got a 1% discount instead of 90% because it opened with today's date [^src1]. An OpenClaw issue (#19534, Feb 2026) showed a full 170K-token context reprocessed every request because a "Current Date & Time" field changed each turn, running 10× over expected cost [^src1]. LangChain's `create_react_agent` lands 0% cache hits by injecting unique IDs into serialized messages [^src1]. Keep out of the cached prefix: current timestamps, session/request IDs, dynamically discovered MCP tool registrations, per-call personalization [^src1]. One case study: 50,000 documents/month cost $8,000 with caching vs $45,000 without — 82% saved [^src1].

## Measure outcomes, not consumption

The Uber lesson "stems from a measurement failure" — nobody evaluated effectiveness before consumption "went parabolic" [^src1]. Microsoft pulled back thousands of internal Claude Code licenses (shifting to GitHub Copilot CLI) to control costs, and Cursor "operates at deeply negative gross margins because API costs scale faster than subscription revenue" [^src1]. Deloitte's 2025 survey: fewer than a third of organizations could attribute AI spend to measurable outcomes [^src1].

The right metric is **value per 1,000 tokens** against a business denominator (tasks completed, tickets resolved, revenue touched); if that is flat while consumption grows, "the economics are running in reverse." [^src1] Do not treat token consumption as an adoption proxy — Meta saw leaderboard-ranked staff leave agents running for hours with no task to climb the standings [^src1]. Disciplined organizations model cost before deploying, build usage dashboards alongside the product, and measure output rather than consumption — spending "60 to 70% less for equivalent output." [^src1] "The token is not the unit of value. The task outcome is." [^src1]

## Practitioner token-conservation habits (Claude Cowork / Code)

The root mechanic: Claude re-reads the entire conversation from the top on every message. Message 30 means 29 previous exchanges re-read before any new reasoning — so the conversation length determines the per-message cost [^src2].

**Highest-value habits** [^src2]:

| Habit | Why it works |
|---|---|
| Convert PDFs/images before uploading | 1 PDF page = 1,500–3,000 tokens; clean text = 2,000 for 15 pages |
| Plan in Chat, build in Cowork | Chat is lighter; Cowork reads files every task |
| Ask "ask me questions" instead of writing long prompts | Short prompts + AskUserQuestion clicks cost almost nothing |
| Batch multiple tasks into one message | Three prompts = three full context reloads; one prompt = one |
| Edit messages instead of follow-ups | Edit replaces history; follow-ups stack on it |
| Compact/restart at 15–20 messages | A 30-message session burns ~232K tokens; a 20-message session ~105K |
| Match model to task complexity | Haiku/Sonnet for drafts and summaries; Opus only for hard reasoning |
| Keep CLAUDE.md/ABOUT-ME under 2,000 words | These load every session — bloat multiplies across all tasks |
| Use Projects for recurring documents | Project files are cached; re-uploading the same PDF re-tokenizes it |
| Spread sessions across the day | Usage limits use a rolling 5-hour window |

**Prompt caching (structural)**: similar prompts used frequently get partially cached on Anthropic's platform — structure prompts static-content-first, dynamic content last [^src2]. This is the same discipline documented in [[ai-engineering/prompt-caching|Prompt Caching]].

**Skills vs CLAUDE.md**: skills load on demand; CLAUDE.md loads every session. Move recurring workflows into skills so they're only loaded when needed [^src2].

**One-shot clarity beats multi-message refinement**: "When you speak, you naturally give more context in one shot" — vague messages lead to correction messages, which stack on history and multiply context reloads [^src2].

## LLM routers and token proxies

**Manifest (mnfst)** is a TypeScript LLM router/gateway (★7,094) [^src3]. Core value: routes requests to the cheapest model that can handle the task, reducing costs up to 70%.

| Feature | Detail |
|---|---|
| **Routing logic** | Routes by complexity (query difficulty), specificity (domain match), HTTP headers (caller-specified override) |
| **BYOK** | Bring Your Own Key for all supported providers; no vendor lock-in |
| **Cost tracking** | Per-request and aggregate spend metrics; fallback on provider failure |
| **Supported providers** | OpenAI, Anthropic, Google, Mistral, Groq + any compatible API |
| **Model spec** | Declarative `model_spec.json` with capability requirements; Manifest selects the cheapest model meeting the spec |

Integration: drop-in replacement for OpenAI-compatible endpoint; add `X-Mnfst-Route: auto` header and Manifest handles the rest [^src3].

**Headroom** is an LLM token proxy positioned as "savings without the complexity of routing" [^src4]. Claims **median 4.8% savings** across real workloads (not synthetic benchmarks) by compressing prompt prefixes before send and decompressing before the model sees them. Works transparently — no model changes, no routing logic, no provider switching.

Contrast with Manifest: Manifest saves 30–70% by using cheaper models; Headroom saves ~5% on the same model, with zero behavioral change. They're complementary: route to cheaper models first, then compress the prompt [^src4].

## MCP server token overhead

Each connected MCP server adds tool descriptions to every session's context window. Measured practitioner data: **~18,000 tokens per MCP server** loaded at session start [^src5]. With 3 MCP servers active, that's ~54,000 tokens of fixed overhead before the first user message.

Mitigation: replace MCP calls with bash tool calls to the equivalent CLI (e.g., `gh` CLI instead of GitHub MCP). One practitioner reported **~40% context savings** by swapping MCP servers for CLI equivalents [^src5]. See [[ai-engineering/context-window-management|Context Window Management]] for the full analysis.

## Local LLMs as cost fallback

For high-volume low-stakes tasks (formatting, simple refactoring, lookup), running a local LLM via Ollama/LM Studio can eliminate API costs entirely [^src6]:

- **Setup**: `brew install ollama` → `ollama pull qwen2.5:7b` → set `ANTHROPIC_BASE_URL=http://localhost:11434/v1`
- **Trade-off**: local 7B models handle simple tasks well but fail on complex multi-step planning; use for high-frequency routine tasks, reserve API credits for complex reasoning
- **Quantization**: Q8 (larger file, better quality) vs Q4 (smaller, faster, lower quality) — Q4_K_M is a common middle ground

This is not a replacement strategy — it's a **tiered cost model** where local handles tier-1 tasks (simple, high-volume) and the API handles tier-2+ tasks (complex, low-volume) [^src6].

[^src1]: [Managing Agentic AI Costs at Scale](../../raw/web/managing-agentic-ai-costs-at-scale.md)
[^src2]: [How to stop hitting Claude usage limits — 23 habits](../../raw/web/web-how-to-stop-hitting-claude-usage-limits.md) — Ruben Hassid
[^src3]: [mnfst/manifest — GitHub ★7094](../../raw/github/github-mnfst-manifest.md)
[^src4]: [Top 10 GitHub repos for AI devs (YouTube)](../../raw/youtube/youtube-n8rP6Ceskm4.md) — Headroom entry at ~3:00
[^src5]: [I Stopped Hitting Claude Code Usage Limits — Here's How](../../raw/youtube/youtube-9ToOfgZ4qqQ-i-stopped-hitting-claude-code-usage-limits-here-s-how.md) — Brad, YouTube
[^src6]: [How to Run Claude Code for Free (Local LLMs)](../../raw/email/email-2026-06-21-how-to-run-claude-code-for-free.md) — email newsletter
</content>
