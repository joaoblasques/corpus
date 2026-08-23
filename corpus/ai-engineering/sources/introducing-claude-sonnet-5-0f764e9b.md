---
type: source
domain: ai-engineering
status: complete
sources:
  - path: raw/_inbox/web-introducing-claude-sonnet-5-0f764e9b.md
    channel: web
    ingested_at: 2026-08-23
aliases:
  - Introducing Claude Sonnet 5
  - Claude Sonnet 5 launch blog
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-23
updated: 2026-08-23
---

# Introducing Claude Sonnet 5 (Anthropic, 2026-06-30)

**Source**: Anthropic official blog — `raw/_inbox/web-introducing-claude-sonnet-5-0f764e9b.md`

## Summary

Anthropic announced Claude Sonnet 5 as its most capable Sonnet-class model, narrowing the gap to Opus 4.8. [^1]

**Positioning**: "Its performance is close to that of Opus 4.8, but at lower prices." Default model for Free and Pro plans as of launch date. [^1]

**Pricing** (as of 2026-06-30): [^1]
- Introductory: $2 / million input tokens, $10 / million output tokens (through 2026-08-31)
- Standard: $3 / million input tokens, $15 / million output tokens

**New tokenizer**: The same input text produces approximately 1.0–1.35x more tokens than on Claude Sonnet 4.6 (content-type dependent). Introductory pricing set to make the transition roughly cost-neutral. [^1]

**Context window**: 1 million tokens; max output 128,000 tokens. [^1]

**Adaptive thinking**: On by default; `temperature`, `top_p`, `top_k` no longer supported. [^1]

**API ID**: `claude-sonnet-5` [^1]

**Availability**: Claude Free, Pro, Max, Team, Enterprise plans; Claude Code; Claude Platform API. [^1]

## Key agentic improvements

- Finishes complex multi-step tasks where previous Sonnet models would stop short [^1]
- Checks its own output without being explicitly asked [^1]
- Stronger agentic performance on BrowseComp (agentic search) and OSWorld-Verified (computer use) vs. Sonnet 4.6 [^1]

## Safety highlights

- Lower hallucination and sycophancy rates than Sonnet 4.6 [^1]
- Better at refusing malicious requests and resisting prompt injection [^1]
- Lower cyber capability than Opus 4.8 (explaining absence of export controls) [^1]
- Cyber safeguards enabled by default (same as Opus 4.7/4.8 tier, less strict than Fable 5) [^1]
- Part of Anthropic's Cyber Verification Program [^1]

## Partner testimonials (selected)

- "Finishes complex tasks where previous Sonnet models would stop short" — multiple early-access partners [^1]
- Legal research use: "sits on the Pareto frontier for Eve's plaintiff-law tasks" [^1]
- Computer use insurance workflows (Pace): "consistently takes the right action and does it quickly" [^1]

[^1]: raw/_inbox/web-introducing-claude-sonnet-5-0f764e9b.md
