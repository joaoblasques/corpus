---
type: source
domain: ai-engineering
status: complete
sources:
  - path: raw/_inbox/web-impressions-from-visiting-openai-anthropic-cursor-cadb0581.md
    channel: web
    ingested_at: 2026-08-23
aliases:
  - Pragmatic Engineer AI labs visit
  - cloud agents mega-trend
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-23
updated: 2026-08-23
---

# Impressions from Visiting OpenAI, Anthropic & Cursor (Pragmatic Engineer, 2026-06-29)

**Source**: newsletter.pragmaticengineer.com — `raw/_inbox/web-impressions-from-visiting-openai-anthropic-cursor-cadb0581.md`

## Summary

The Pragmatic Engineer (Gergely Orosz) visited OpenAI, Anthropic, and Cursor offices during AI Engineer World's Fair 2026 and reported on four emerging industry trends. [^1]

## 1. Cloud agents as the next mega-trend

All three companies are betting heavily on agents running in the cloud rather than locally. [^1]

**Anthropic**: "Claude Managed Agents" — a hosted service for long-running agents — described as a "large, complex project" built over six months by Katelyn Lesse's team. The key differentiators vs. local Claude Code: no setup required, no tool context-switching, runs in cloud even when the developer's machine is closed. [^1]

**OpenAI**: Acquired Ona (formerly Gitpod), the cloud development environment (CDE) leader, specifically to provide sandboxed cloud environments for Codex agents running "hours or days rather than minutes." Actively hiring for a Cloud Agents team. [^1]

**Cursor**: Released Cloud Agents at the end of 2025. CTO Sualeh Asif shared two challenges: (1) long-running agents can't "complain" when things go wrong — Cursor invented "confessions" for agents to report issues at periodic intervals; (2) node termination mid-task is a non-trivial engineering problem. [^1]

**Why now** (author's hypothesis — four factors converging): [^1]
1. Coding models hit "good enough" threshold (Opus 4.5 / GPT-5.4)
2. MCP and skills matured (context injection better understood)
3. Context windows reached 1M tokens
4. Cloud GPU capacity now sufficient for large-scale agent deployment

## 2. Non-developer adoption of coding harnesses

At OpenAI, >95% of non-engineers use Codex (not ChatGPT) internally. The first Codex team engineer demonstrated non-technical employee usage as exceptional evidence of the tool's accessibility. [^1]

## 3. Engineering work shifting to agent efficiency

At Anthropic and Cursor, significant engineering effort now goes into building better environments, context scaffolding, and agent infrastructure — not model weights. The agent execution environment is becoming the primary leverage point. [^1]

## 4. Token cost optimization as platform engineering

Coinbase case study mentioned: platform teams are cutting per-token cost aggressively as AI spend becomes material. Top 1% of companies already spending at Anthropic-level compute ratios relative to payroll. [^1]

[^1]: raw/_inbox/web-impressions-from-visiting-openai-anthropic-cursor-cadb0581.md
