---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-tokenbudgeting-our-conversations-with-enterprises-on-token-s-2c43f8d2.md
    channel: web
    ingested_at: 2026-08-24
aliases:
  - tokenbudgeting
  - tokenmaxxing enterprise
  - enterprise AI token spend 2026
  - SemiAnalysis token budgets
tags:
  - corpus/ai-engineering
created: 2026-08-24
updated: 2026-08-24
---

# Enterprise Token Spend & Budgeting (SemiAnalysis, 2026)

**TL;DR.** SemiAnalysis interviewed 50+ enterprise customers (including Fortune 500s, at the Databricks AI Summit) about AI token spend in 1H 2026. The "Tokenmaxxing" trend (Meta consumed 60T tokens/30 days; Uber burned its annual Claude Code + Codex budget in 4 months) was driven by poor incentives at specific firms, not a market-wide blowout. Token budgets are now the norm, ranging $250–$40K/month. Companies are downgrading default models (Opus → Sonnet). >70% of OpenAI + Anthropic ARR is attributed to coding use cases. The 90th–99th percentile customers drive the bulk of AI lab revenue. [^src1]

## Tokenmaxxing: peak and correction

**Tokenmaxxing** (1H 2026): a short-lived trend where companies like Meta and Salesforce encouraged maximum AI token consumption to boost productivity [^src1].

Notable peaks [^src1]:
- **Meta**: consumed >60T tokens in 30 days; an internal "Claudeconomics" dashboard ranked the top 250 power users; the single highest individual consumed ~280B tokens. Employees competed for rankings like "Token Legend" and "Cache Wizard" — including running agents for hours just to burn tokens. Dashboard shut down after 2 days.
- **Uber**: burned through its annual Claude Code + Codex budget in 4 months; subsequently imposed a $1,500/month/employee limit (case-by-case exceptions above limit).

SemiAnalysis's view: these cases reflect poor incentives and lax oversight, not absence of high-ROI AI activities — and are not representative of the broader enterprise market. [^src1]

## Budget norms

As of mid-2026, budgets are the norm — but there is no consensus number [^src1]:

| Company type | Monthly budget per employee |
|---|---|
| Top 3 US aerospace/defense manufacturer | $250 |
| Large pharmaceutical | $500 |
| Global travel-tech (800 engineers) | $200 default, up to tens of thousands for senior/data science roles |
| Workday, Stripe | ~$2,000 |
| Cybersecurity (public): junior / senior / data scientists | $800 / $1,600–$4,000 / highest |

Anthropic's own documentation: average Claude Code usage $150–$250/month; only 10% of users spend >$30/day. [^src1]

**Revenue concentration**: 90th-percentile Ramp customers spend ~$7,300/year per employee; 99th-percentile ~$90,000/year per employee; median Ramp customer spends $136/year. Even Meta (spending ≥$50K/year per employee at list price) is estimated at only 3–5% of Anthropic's total customer revenue. [^src1]

## Model downgrade pattern

Companies are downgrading default models to manage spend [^src1]:
- Aerospace/defense firm: disabled Opus 4.8 and Fast-Mode; employees default to a lower tier.
- Global travel-tech: switched all 800 engineers from Opus default to Sonnet default; Opus remains available but requires a conscious selection.

Management rationale: prevent automation of tasks "that shouldn't be automated at all." SemiAnalysis disagrees — views this as a naive anti-automation stance given the long-term productivity trajectory of AI-native work. [^src1]

## Revenue structure

SemiAnalysis estimates [^src1]:
- **>70% of ARR across OpenAI and Anthropic** comes from coding use cases.
- Anthropic's ARR skews higher toward coding than OpenAI's, reflecting Anthropic's ~90% B2B mix vs OpenAI's ~60% B2B.
- Coding vertical economics (via Cursor, Loveable, GitHub Copilot, and direct Claude Code) are likely to be repeated at faster pace in: **Cyber** (dependent on Mythos re-release), then **white-collar knowledge work** (Cowork, Copilot, Codex, computer-use products).

## Conservative enterprise baseline

Among Fortune 500s contacted, most non-engineering departments spend well under $2,000/year per employee — the S-curve of enterprise adoption still has "plenty of runway." The financial industry has been particularly slow; employees are largely constrained to Microsoft Copilot through M365 Enterprise plans. [^src1]

Microsoft 365 Enterprise employees receive free, unlimited M365 Copilot access — which employees use to draft/synthesize before spending metered tokens on Claude or Codex, effectively gaming the budget system. [^src1]

## Related

- [Claude Models](/ai-engineering/claude-models.md) — model tiers (Opus vs Sonnet) referenced in downgrade pattern
- [Claude Code](/ai-engineering/claude-code.md)
- [Anthropic](/ai-engineering/anthropic.md)

---

[^src1]: [TokenBudgeting: Our Conversations with Enterprises on Token Spend](../../../raw/web/web-tokenbudgeting-our-conversations-with-enterprises-on-token-s-2c43f8d2.md) — SemiAnalysis, 2026; n=50+ enterprise interviews at Databricks AI Summit and via phone/Slack
