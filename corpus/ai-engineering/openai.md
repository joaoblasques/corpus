---
type: entity
domain: ai-engineering
status: draft
confidence: 0.8
last_confirmed: 2026-07-12
sources:
  - path: raw/email/email-2025-04-17-our-most-powerful-reasoning-models-gpt-4-1-codex-cli-and-new.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/web/web-a-quote-from-openai-232e7d75.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-ainews-openai-launches-gpt-5-6-sol-terra-luna-codex-becomes-f7ffe7c7.md
    channel: web
    ingested_at: 2026-07-11
  - path: raw/web/web-ainews-not-much-happened-today-41160de5.md
    channel: web
    ingested_at: 2026-07-12
  - path: raw/web/web-chatgpt-atlas-dud-or-revolution-full-guide-9f17dd61.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/web/web-andrej-karpathy.md
    channel: web
    ingested_at: 2026-07-02
  - path: raw/youtube/youtube-ImPESBftwr8-i-spent-50-000-self-hosting-ai-models-you-should-too-0xsero.md
    channel: youtube
    ingested_at: 2026-07-02
  - path: raw/notes/notes-03-resources-articles-reflective-ai-systems-that-learn-from-their-mistakes.md
    channel: notes
    ingested_at: 2026-07-14
aliases:
  - OpenAI
  - GPT-4.1
  - o3
  - o4-mini
  - Codex CLI
  - GPT-4.1 mini
  - GPT-4.1 nano
  - GPT-5.6
  - Sol
  - Terra
  - Luna
  - ChatGPT Work
  - ChatGPT Atlas
consolidates:
  - corpus/ai-engineering/sources/a-quote-from-openai-232e7d75.md
  - corpus/ai-engineering/sources/ainews-not-much-happened-today-41160de5.md
  - corpus/ai-engineering/sources/ainews-openai-launches-gpt-5-6-sol-terra-luna-codex-becomes--f7ffe7c7.md
  - corpus/ai-engineering/sources/andrej-karpathy-aa.md
  - corpus/ai-engineering/sources/chatgpt-atlas-dud-or-revolution-full-guide-9f17dd61.md
  - corpus/ai-engineering/sources/i-spent-50-000-self-hosting-ai-models-you-should-too-0xsero-ImPESBftwr8.md
  - corpus/ai-engineering/sources/reflective-ai-systems-that-learn-from-their-mistakes-ae.md
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-19
updated: 2026-07-14
---

# OpenAI

**TL;DR**: OpenAI's developer model lineup as announced in its April 2025 Dev Digest — the **o3 / o4-mini** reasoning models, the developer-focused **GPT-4.1** family (up to 1M-token context), the open-source **Codex CLI** coding agent, a programmatic **Evals API**, and a new suite of audio models for voice agents [^src1]. By mid-2026 the lineup had moved on to the **GPT-5.6** frontier series — three sizes named **Sol**, **Terra**, and **Luna** [^src2] — while Codex was folded into a **ChatGPT Work** desktop app [^src4]. Peer lab/models to Anthropic's Claude (contrast: [Claude Model Lineup](/ai-engineering/claude-models.md)).

The April 2025 sections below capture a single point-in-time announcement: OpenAI framed the release as "a slew of new models and features for developers" spanning coding, voice experiences, and "faster, more capable agentic apps" [^src1]. That lineup therefore reads as four parallel tracks — reasoning, developer-first, coding agent, and audio — rather than one model. The GPT-5.6 material below is a later, separate generation and does not supersede the April 2025 claims so much as sit downstream of them.

## Reasoning models: o3 / o4-mini

- **o3** and **o4-mini** are available in the API [^src1]. o3 achieves leading performance on coding, math, science, and vision, and tops the SWE-Bench Verified leaderboard at **69.1%**, "making it the best model for agentic coding tasks" [^src1]. o4-mini is the faster, cost-efficient reasoning model [^src1].
- **Responses API recommended.** Both are available in the Chat Completions and Responses APIs, but the Responses API is recommended for the richest experience: it supports **reasoning summaries** (the model's thoughts stream while you wait for the final response) and enables smarter tool use by **preserving the model's prior reasoning between calls** [^src1].
- **Tier availability + org verification.** o4-mini is available on tiers 1–5; o3 on tiers 4–5. Developers on tiers 1–3 can gain o3 access by **verifying their organizations**; reasoning summaries and streaming also require verification [^src1].
- **Flex processing.** Significantly cheaper per-token prices in exchange for longer response times and lower availability — for optimizing cost on **non-urgent workloads such as background agents, evals, or data pipelines** [^src1].

## Developer-first models: GPT-4.1 family

- **GPT-4.1**, **GPT-4.1 mini**, and **GPT-4.1 nano** launched in the API, trained for developer use cases: **coding, instruction following, and function calling** [^src1].
- Larger context windows: **up to 1 million tokens** of context, with improved long-context comprehension to better use that context [^src1].

## Codex CLI

**Codex CLI** is an open-source **local coding agent** that turns natural language into working code — tell it what to build, fix, or explain [^src1]. It works with all OpenAI models, including o3, o4-mini, and GPT-4.1 [^src1]. A peer to [Agentic Coding](/ai-engineering/agentic-coding.md) tools and to Anthropic's [Claude Code](/ai-engineering/claude-code.md).

## Evals API

The **Evals API** lets developers programmatically define tests, automate evaluation runs, and iterate quickly on prompts [^src1]. See [Agent Evaluation](/ai-engineering/agent-evaluation.md) for the broader evaluation methodology.

## Audio models & voice agents

- **Three new state-of-the-art audio models** in the API: two speech-to-text models that outperform Whisper, and a new TTS model that you can instruct on how to speak [^src1].
- The **Agents SDK** was updated to support audio [^src1].
- **Realtime API** powers low-latency voice agents — the spotlighted example is Lemonade's "AI Maya," using automatic voice detection and low latency for 24/7 multilingual phone support [^src1].

## GPT-5.6: Sol / Terra / Luna (2026)

- OpenAI began a **limited preview of the GPT-5.6 series**, comprising **Sol**, **Terra**, and **Luna** [^src2]. The three are described as model **sizes**, priced per 1M tokens [^src2]. GPT-5.6 is characterised as a **frontier model** with improved performance and efficiency over its predecessors [^src4].
- **Competitive framing.** The series is reported to offer competitive performance, pricing, and features — among them **predictable prompt caching** [^src2]. On benchmarks, GPT-5.6 is reported to outperform previous models [^src4], though the strength is uneven: it appears **strongest in agentic coding, presentation, and science tasks, but not unambiguously dominant everywhere** [^src3].
- **Safety criticism.** Critics raised concerns about the model's **safety and security** [^src4]. The corpus has no resolution of that dispute; the two AINews items are the only sources here that touch it.

### Model/compute ladder and the Auto-routing stumble

The GPT-5.6 rollout introduced a **more explicit model/compute ladder**, but users found the **30+ configuration combinatorics and missing 'Auto' routing confusing** [^src3]. OpenAI **course-corrected fast, acknowledging that defaults nudged users toward overly expensive settings** [^src3]. This is a concrete agent-UX failure mode: exposing an effort/size matrix without a router shifts cost-selection onto the user, and a badly-chosen default is a billing decision, not just a preference. Contrast the flex-processing track above [^src1], which solves the same cost problem by naming an explicit non-urgent tier rather than by multiplying knobs.

## Codex → ChatGPT Work

Alongside GPT-5.6, OpenAI introduced **ChatGPT Work**, a **desktop app that merges Codex and GPT-5.6** [^src4]. Read against the April 2025 [Codex CLI](#codex-cli) entry [^src1], the trajectory is a terminal-resident open-source agent being absorbed into a packaged desktop surface — one source frames the result as Codex "becom[ing a] ChatGPT superapp" [^src4].

## ChatGPT Atlas

**ChatGPT Atlas** is described as a tool that **integrates AI into everyday tasks**, discussed alongside GPT-5 and AI agents [^src5]. The available source is a promotional how-to guide arguing that Atlas can help users become more skilled with AI and advance their goals [^src5]; it poses "dud or revolution?" as its own framing and does not settle it. Treat the productivity claims as vendor-adjacent advocacy rather than evaluated results.

## Positioning against other labs

- **Chinese open-weight models as a self-hosting alternative.** One practitioner account compares **GLM 5.2**, a Chinese AI model, against OpenAI and Anthropic across **coding, DevOps, and GPU programming**, weighing strengths and weaknesses [^src6]. The framing is that self-hosting is a live alternative to OpenAI's API rather than a strictly inferior one — see [Local LLM](/ai-engineering/localai.md) for the general trade-off.
- **Reflective AI.** OpenAI appears among the labs associated with **reflective AI** — systems that **evaluate and improve their own outputs**, improving accuracy **without requiring additional training data**, positioned as foundational to the next generation of autonomous agents [^src7]. This is the same judgement the eval layer applies externally; compare the [Evals API](#evals-api) [^src1] and [Agent Evaluation](/ai-engineering/agent-evaluation.md).

## People

**Andrej Karpathy** is associated with OpenAI; his career spans **research scientist, team lead, and instructor** in AI and deep learning, with work on **mid-training, synthetic data generation, and deep reinforcement learning** [^src8]. He taught **CS 231n**, one of the largest deep learning classes at Stanford [^src8].

## See also

- [Claude Model Lineup](/ai-engineering/claude-models.md) — peer lab/models for contrast
- [LLM](/ai-engineering/llm.md) — the underlying model class
- [Agentic Coding](/ai-engineering/agentic-coding.md) — Codex CLI sits in this space
- [Claude Code](/ai-engineering/claude-code.md) — peer coding agent
- [Agent Evaluation](/ai-engineering/agent-evaluation.md) — the Evals API operationalizes this
- [AI Agent](/ai-engineering/ai-agent.md) — reflection loops are foundational to autonomous agents
- [Local LLM](/ai-engineering/localai.md) — the self-hosting alternative GLM 5.2 is weighed against

---

[^src1]: [OpenAI Dev Digest: reasoning models, GPT-4.1, Codex CLI, and new audio models](../../raw/email/email-2025-04-17-our-most-powerful-reasoning-models-gpt-4-1-codex-cli-and-new.md) — OpenAI, April 2025
[^src2]: [A quote from OpenAI](../../raw/web/web-a-quote-from-openai-232e7d75.md) — Simon Willison, June 2026
[^src3]: [[AINews] not much happened today](../../raw/web/web-ainews-not-much-happened-today-41160de5.md) — Latent Space, July 2026
[^src4]: [[AINews] OpenAI launches GPT 5.6 Sol/Terra/Luna, Codex becomes ChatGPT superapp](../../raw/web/web-ainews-openai-launches-gpt-5-6-sol-terra-luna-codex-becomes-f7ffe7c7.md) — Latent Space, July 2026
[^src5]: [ChatGPT Atlas: Dud or Revolution? (Full Guide)](../../raw/web/web-chatgpt-atlas-dud-or-revolution-full-guide-9f17dd61.md) — Alex Finn
[^src6]: ["I spent $50,000 self-hosting AI models. You should too." - 0xSero](../../raw/youtube/youtube-ImPESBftwr8-i-spent-50-000-self-hosting-ai-models-you-should-too-0xsero.md) — David Ondrej, June 2026
[^src7]: [Reflective AI - Systems That Learn From Their Mistakes](../../raw/notes/notes-03-resources-articles-reflective-ai-systems-that-learn-from-their-mistakes.md) — Alex Wang
[^src8]: [Andrej Karpathy](../../raw/web/web-andrej-karpathy.md) — karpathy.ai
