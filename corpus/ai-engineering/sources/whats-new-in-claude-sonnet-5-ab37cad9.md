---
type: source
domain: ai-engineering
status: complete
sources:
  - path: raw/_inbox/web-whats-new-in-claude-sonnet-5-ab37cad9.md
    channel: web
    ingested_at: 2026-08-23
aliases:
  - What's new in Claude Sonnet 5
  - Simon Willison Sonnet 5 analysis
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-23
updated: 2026-08-23
---

# What's New in Claude Sonnet 5 (Simon Willison, 2026-06-30)

**Source**: simonwillison.net — `raw/_inbox/web-whats-new-in-claude-sonnet-5-ab37cad9.md`

## Summary

[Simon Willison](/ai-engineering/simon-willison.md) analyzed the Sonnet 5 launch, focusing on developer-facing API changes and the practical tokenizer cost impact. [^1]

## Key developer observations

**Sampling parameters removed**: `temperature`, `top_p`, `top_k` no longer accepted. [^1]

**Context**: 1M token context window, 128K max output tokens. [^1]

**Adaptive thinking**: On by default unless explicitly disabled with `"thinking": {"type": "disabled"}`. [^1]

**Pricing note**: Listed as the same as Sonnet 4.6 ($3/$15 per million input/output), but the new tokenizer effectively makes it more expensive for most content types. [^1]

## Tokenizer multiplier measurements

Willison measured token counts across multiple document types comparing Sonnet 4.6 to Sonnet 5 / Opus 4.7 (which share a tokenizer): [^1]

| Document | Sonnet 4.6 tokens | Sonnet 5 tokens | Multiplier |
|---|---|---|---|
| Universal Declaration of Human Rights (English) | 2,356 | 3,341 | 1.42x |
| Universal Declaration of Human Rights (Spanish) | 3,572 | 4,747 | 1.33x |
| Universal Declaration of Human Rights (Simplified Mandarin) | 3,334 | 3,360 | 1.01x |
| sqlite_utils/db.py (4,279 lines Python) | 44,014 | 56,113 | 1.27x |

**Practical implication**: "effectively a 30% price increase" for English-heavy workloads, at the standard post-intro pricing tier. [^1]

## Safety / export control note

Willison notes the system card explains why Sonnet 5 was released without the export controls that affected Fable 5 and Mythos 5: "Sonnet 5 is significantly less capable at cyber tasks than Mythos 5." [^1]

[^1]: raw/_inbox/web-whats-new-in-claude-sonnet-5-ab37cad9.md
