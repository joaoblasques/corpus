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
  - path: raw/web/web-plans-pricing-claude-by-anthropic-eb3bbaf1.md
    channel: web
    ingested_at: 2026-06-28
  - path: raw/web/web-plans-pricing-claude-by-anthropic-9a6ae4fe.md
    channel: web
    ingested_at: 2026-06-28
  - path: raw/web/web-claude-d73a2735.md
    channel: web
    ingested_at: 2026-06-28
  - path: raw/web/web-preise-claude-890abd15.md
    channel: web
    ingested_at: 2026-06-28
  - path: raw/web/web-tarifs-claude-9fb676e7.md
    channel: web
    ingested_at: 2026-06-28
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
updated: 2026-06-28
---

# Claude Plans & Pricing (consumer / team subscriptions)

**TL;DR.** [Anthropic](/ai-engineering/anthropic.md) sells Claude through five subscription tiers — **Free, Pro, Max, Team, Enterprise** (plus an institutional **Education** plan) — gating usage limits, model access, and admin/governance features rather than capabilities per se [^src1]. This is the **consumer/seat-subscription** axis (claude.com), distinct from the per-million-token **API pricing** tracked on [Claude Model Lineup](/ai-engineering/claude-models.md). Snapshot collected 2026-06-27 from claude.com localized plan pages; prices are USD and may change.

The product framing across all plan pages: brainstorm in chat, then build in [Cowork](/ai-engineering/claude-cowork.md) [^src2]. Claude is positioned as an assistant "trained by Anthropic with Constitutional AI to be safe, accurate, and secure" [^src1].

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

**Free** [^src2] — chat on web/iOS/Android/desktop; code generation and data visualization; content writing/editing; text and image analysis; web search; file creation and code execution; desktop extensions; Slack and Google Workspace connectors; any context or tool via **remote [MCP](/ai-engineering/mcp.md) connectors**; extended thinking for complex work.

**Pro** (everything in Free, plus) [^src2] — more usage; **[Claude Code](/ai-engineering/claude-code.md)**; **[Cowork](/ai-engineering/claude-cowork.md)**; unlimited Projects; Research access; memory across conversations; more Claude models; **Claude in Excel**; **Claude in Chrome** (the Italian page lists **Claude for PowerPoint (beta)** in place of Chrome) [^src1].

**Max** (everything in Pro, plus) [^src1] — choose 5× or 20× Pro usage; recommended for Claude Code & Cowork; higher output limits on all tasks; early access to advanced Claude features; priority access during high-traffic periods.

**Team** (everything in Pro, plus) [^src1] — Claude Code and Cowork; connect Microsoft 365, Slack, and more; enterprise search across the organization; centralized billing and administration; single sign-on (SSO); domain verification; admin controls for remote and local connectors; enterprise deployment of the desktop app; **no model training on your content by default**; mix-and-match seat types.

**Enterprise** (governance layer) [^src1] — admin-set spend limits per user and org; Google Docs cataloging; role-based access with granular permissions; **SCIM** identity management; audit logs; a compliance API for observability/monitoring; custom data-retention controls; network-level access control and allowed-IP definitions; **HIPAA-compliant offering available**.

**Education** [^src1] — full access for an institution's students, faculty, and staff at discounted rates; an academic research-and-learning mode; dedicated API credits and education features; training and enablement resources for institution-wide adoption.

## Platform feature pricing (API / Claude Platform)

Discrete paid capabilities layered on top of token rates [^src6]:

| Feature | Cost | Notes |
|---|---|---|
| **Managed Agents** | $0.08 per active session-hour | Standard token rates also apply |
| **Web search** | $10 / 1,000 searches | Does not include tokens for processing |
| **Code execution** | $0.05 / hr per container | 50 free hours/day per org |

## Service tiers

Three request-priority levels for the Claude API [^src6]:

- **Priority** — when time, availability, and predictable pricing are most important
- **Standard** — default tier for piloting and everyday scaling
- **Batch** — asynchronous workloads processed together for better efficiency (50% cost savings vs Standard implied by the product description)

## US-only inference and fast mode

- **US-only inference**: for workloads that must run within the United States, available at **1.1× pricing** for input and output tokens [^src6].
- **Fast mode (Opus 4.8)**: up to **2.5× faster throughput** at **2× standard pricing** [^src6].
- **Prompt caching**: 5-minute TTL; extended caching available separately [^src6].

## Current and legacy models

**Active** (as of 2026-06-28): Fable 5 [^note-fable], Opus 4.8, Sonnet 4.6, Haiku 4.5 [^src6].

**Legacy** (still available): Opus 4.7, Opus 4.6, Sonnet 4.5, Opus 4.5, Opus 4.1 [^src6].

[^note-fable]: Fable 5 is currently unavailable due to US export control restrictions. See [Anthropic](/ai-engineering/anthropic.md) §Fable 5 launch controversy.

## Additional Enterprise features

The Enterprise tier adds **Claude Security** (beta) — a vulnerability-scanning product using Opus 4.7; see [Anthropic](/ai-engineering/anthropic.md) §Project Glasswing [^src6]. Enterprise also offers AWS Marketplace availability, committed-spend tiered incentives, trials, custom MSAs, and customer success support at certain spend thresholds [^src6].

## Feature flags visible in the comparison table

New features present in the 2026-06-28 pricing page not in earlier snapshots [^src6]:
- **@Claude** — available from Team tier and above
- **Claude Security** — Enterprise only (beta)
- **Claude for Chrome** — Pro and above
- **Research** — Pro and above
- **Memory** — Pro and above (user-level persistent memory)
- **Skills** — Team and above (organization-wide skills deployment at Enterprise)
- **Connectors** — Free tier gets remote MCP connectors; Enterprise gets admin controls for remote and local

## Notes

- The plan tiers gate **usage volume, model selection, and admin/compliance controls** — Claude Code and Cowork themselves start at the Pro tier [^src2].
- Subscription prices here are independent of **API token pricing** (e.g. Opus 4.8 at $5/$25 per M, Fable 5 at $10/$50 per M) — see [Claude Model Lineup](/ai-engineering/claude-models.md) for the per-model, per-token rates and which model is default on each account type.

## See also

- [Anthropic](/ai-engineering/anthropic.md) — the lab; company, funding, products
- [Claude Model Lineup](/ai-engineering/claude-models.md) — model family and per-token API pricing
- [Claude Code](/ai-engineering/claude-code.md) · [Claude Cowork](/ai-engineering/claude-cowork.md) — the products gated behind Pro+

[^src1]: [Claude by Anthropic — plans (it)](../../raw/web/web-claude-by-anthropic-90b51f29.md) — claude.com/it (most complete: Team/Enterprise/Education)
[^src2]: [Claude — plans (de)](../../raw/web/web-claude-796a7cce.md) — claude.com/de
[^src3]: [Claude — plans (ja)](../../raw/web/web-untitled-42cbd4cb.md) — claude.com/ja
[^src4]: [Claude — plans (ko)](../../raw/web/web-claude-2c35b97a.md) — claude.com/ko
[^src5]: [Claude — plans (fr)](../../raw/web/web-claude-4f6af6b8.md) — claude.com/fr
[^src6]: [Plans & Pricing | Claude by Anthropic (en)](../../raw/web/web-plans-pricing-claude-by-anthropic-eb3bbaf1.md) — claude.com/pricing; English pricing page; collected 2026-06-28; primary source for platform feature pricing, service tiers, fast mode, legacy models, and enterprise feature flags
