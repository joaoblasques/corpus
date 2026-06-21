---
type: entity
domain: ai-engineering
status: draft
confidence: 0.8
last_confirmed: 2025-04-17
sources:
  - path: raw/email/email-2025-04-17-our-most-powerful-reasoning-models-gpt-4-1-codex-cli-and-new.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - OpenAI
  - GPT-4.1
  - o3
  - o4-mini
  - Codex CLI
  - GPT-4.1 mini
  - GPT-4.1 nano
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-19
updated: 2026-06-21
---

# OpenAI

**TL;DR**: OpenAI's developer model lineup as announced in its April 2025 Dev Digest — the **o3 / o4-mini** reasoning models, the developer-focused **GPT-4.1** family (up to 1M-token context), the open-source **Codex CLI** coding agent, a programmatic **Evals API**, and a new suite of audio models for voice agents [^src1]. Peer lab/models to Anthropic's Claude (contrast: [[ai-engineering/claude-models|Claude Model Lineup]]).

This page captures a single point-in-time announcement: OpenAI framed the release as "a slew of new models and features for developers" spanning coding, voice experiences, and "faster, more capable agentic apps" [^src1]. The lineup below therefore reads as four parallel tracks — reasoning, developer-first, coding agent, and audio — rather than one model.

## Reasoning models: o3 / o4-mini

- **o3** and **o4-mini** are available in the API [^src1]. o3 achieves leading performance on coding, math, science, and vision, and tops the SWE-Bench Verified leaderboard at **69.1%**, "making it the best model for agentic coding tasks" [^src1]. o4-mini is the faster, cost-efficient reasoning model [^src1].
- **Responses API recommended.** Both are available in the Chat Completions and Responses APIs, but the Responses API is recommended for the richest experience: it supports **reasoning summaries** (the model's thoughts stream while you wait for the final response) and enables smarter tool use by **preserving the model's prior reasoning between calls** [^src1].
- **Tier availability + org verification.** o4-mini is available on tiers 1–5; o3 on tiers 4–5. Developers on tiers 1–3 can gain o3 access by **verifying their organizations**; reasoning summaries and streaming also require verification [^src1].
- **Flex processing.** Significantly cheaper per-token prices in exchange for longer response times and lower availability — for optimizing cost on **non-urgent workloads such as background agents, evals, or data pipelines** [^src1].

## Developer-first models: GPT-4.1 family

- **GPT-4.1**, **GPT-4.1 mini**, and **GPT-4.1 nano** launched in the API, trained for developer use cases: **coding, instruction following, and function calling** [^src1].
- Larger context windows: **up to 1 million tokens** of context, with improved long-context comprehension to better use that context [^src1].

## Codex CLI

**Codex CLI** is an open-source **local coding agent** that turns natural language into working code — tell it what to build, fix, or explain [^src1]. It works with all OpenAI models, including o3, o4-mini, and GPT-4.1 [^src1]. A peer to [[ai-engineering/agentic-coding|Agentic Coding]] tools and to Anthropic's [[ai-engineering/claude-code|Claude Code]].

## Evals API

The **Evals API** lets developers programmatically define tests, automate evaluation runs, and iterate quickly on prompts [^src1]. See [[ai-engineering/agent-evaluation|Agent Evaluation]] for the broader evaluation methodology.

## Audio models & voice agents

- **Three new state-of-the-art audio models** in the API: two speech-to-text models that outperform Whisper, and a new TTS model that you can instruct on how to speak [^src1].
- The **Agents SDK** was updated to support audio [^src1].
- **Realtime API** powers low-latency voice agents — the spotlighted example is Lemonade's "AI Maya," using automatic voice detection and low latency for 24/7 multilingual phone support [^src1].

## See also

- [[ai-engineering/claude-models|Claude Model Lineup]] — peer lab/models for contrast
- [[ai-engineering/llm|LLM]] — the underlying model class
- [[ai-engineering/agentic-coding|Agentic Coding]] — Codex CLI sits in this space
- [[ai-engineering/claude-code|Claude Code]] — peer coding agent
- [[ai-engineering/agent-evaluation|Agent Evaluation]] — the Evals API operationalizes this

---

[^src1]: [OpenAI Dev Digest: reasoning models, GPT-4.1, Codex CLI, and new audio models](../../raw/email/email-2025-04-17-our-most-powerful-reasoning-models-gpt-4-1-codex-cli-and-new.md) — OpenAI, April 2025
