---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-claude-by-anthropic-90b51f29.md
    channel: web
    ingested_at: 2026-06-27
  - path: raw/web/web-untitled-42cbd4cb.md
    channel: web
    ingested_at: 2026-06-27
  - path: raw/web/web-claude-2c35b97a.md
    channel: web
    ingested_at: 2026-06-27
  - path: raw/web/web-claude-796a7cce.md
    channel: web
    ingested_at: 2026-06-27
  - path: raw/web/web-claude-4f6af6b8.md
    channel: web
    ingested_at: 2026-06-27
aliases:
  - Claude plans
  - Claude pricing
  - Claude subscription plans
  - Claude Pro
  - Claude Max
  - Claude Team
  - Claude Enterprise
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-27
updated: 2026-06-27
---

# Claude Plans & Pricing (consumer / team subscriptions)

**TL;DR.** [[ai-engineering/anthropic|Anthropic]] sells Claude through five subscription tiers — **Free, Pro, Max, Team, Enterprise** (plus an institutional **Education** plan) — gating usage limits, model access, and admin/governance features rather than capabilities per se [^src1]. This is the **consumer/seat-subscription** axis (claude.com), distinct from the per-million-token **API pricing** tracked on [[ai-engineering/claude-models|Claude Model Lineup]]. Snapshot collected 2026-06-27 from claude.com localized plan pages; prices are USD and may change.

The product framing across all plan pages: brainstorm in chat, then build in [[ai-engineering/claude-cowork|Cowork]] [^src2]. Claude is positioned as an assistant "trained by Anthropic with Constitutional AI to be safe, accurate, and secure" [^src1].

## Tier comparison

| Plan | Price (USD) | Positioning |
|---|---|---|
| **Free** | $0 [^src2][^src3] | Limited usage, no payment required [^src1] |
| **Pro** | $17/mo on annual ($200 billed up front); $20/mo monthly [^src1][^src2] | Everyday productivity [^src2] |
| **Max** | from $100/mo [^src2][^src3] | 5× or 20× Pro usage; recommended for Claude Code & Cowork [^src1] |
| **Team** | per seat/mo, billed annually; $25/mo (standard) or $125/mo (premium) on monthly billing [^src1] | Collaboration + central admin [^src1] |
| **Enterprise** | custom [^src1] | Org-wide governance, security, compliance [^src1] |
| **Education** | institutional [^src1] | Students/faculty/staff at discounted rates [^src1] |

## What each tier adds

**Free** [^src2] — chat on web/iOS/Android/desktop; code generation and data visualization; content writing/editing; text and image analysis; web search; file creation and code execution; desktop extensions; Slack and Google Workspace connectors; any context or tool via **remote [[ai-engineering/mcp|MCP]] connectors**; extended thinking for complex work.

**Pro** (everything in Free, plus) [^src2] — more usage; **[[ai-engineering/claude-code|Claude Code]]**; **[[ai-engineering/claude-cowork|Cowork]]**; unlimited Projects; Research access; memory across conversations; more Claude models; **Claude in Excel**; **Claude in Chrome** (the Italian page lists **Claude for PowerPoint (beta)** in place of Chrome) [^src1].

**Max** (everything in Pro, plus) [^src1] — choose 5× or 20× Pro usage; recommended for Claude Code & Cowork; higher output limits on all tasks; early access to advanced Claude features; priority access during high-traffic periods.

**Team** (everything in Pro, plus) [^src1] — Claude Code and Cowork; connect Microsoft 365, Slack, and more; enterprise search across the organization; centralized billing and administration; single sign-on (SSO); domain verification; admin controls for remote and local connectors; enterprise deployment of the desktop app; **no model training on your content by default**; mix-and-match seat types.

**Enterprise** (governance layer) [^src1] — admin-set spend limits per user and org; Google Docs cataloging; role-based access with granular permissions; **SCIM** identity management; audit logs; a compliance API for observability/monitoring; custom data-retention controls; network-level access control and allowed-IP definitions; **HIPAA-compliant offering available**.

**Education** [^src1] — full access for an institution's students, faculty, and staff at discounted rates; an academic research-and-learning mode; dedicated API credits and education features; training and enablement resources for institution-wide adoption.

## Notes

- The plan tiers gate **usage volume, model selection, and admin/compliance controls** — Claude Code and Cowork themselves start at the Pro tier [^src2].
- Subscription prices here are independent of **API token pricing** (e.g. Opus 4.8 at $5/$25 per M, Fable 5 at $10/$50 per M) — see [[ai-engineering/claude-models|Claude Model Lineup]] for the per-model, per-token rates and which model is default on each account type.

## See also

- [[ai-engineering/anthropic|Anthropic]] — the lab; company, funding, products
- [[ai-engineering/claude-models|Claude Model Lineup]] — model family and per-token API pricing
- [[ai-engineering/claude-code|Claude Code]] · [[ai-engineering/claude-cowork|Claude Cowork]] — the products gated behind Pro+

[^src1]: [Claude by Anthropic — plans (it)](../../raw/web/web-claude-by-anthropic-90b51f29.md) — claude.com/it (most complete: Team/Enterprise/Education)
[^src2]: [Claude — plans (de)](../../raw/web/web-claude-796a7cce.md) — claude.com/de
[^src3]: [Claude — plans (ja)](../../raw/web/web-untitled-42cbd4cb.md) — claude.com/ja
[^src4]: [Claude — plans (ko)](../../raw/web/web-claude-2c35b97a.md) — claude.com/ko
[^src5]: [Claude — plans (fr)](../../raw/web/web-claude-4f6af6b8.md) — claude.com/fr
