---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-government-claude-by-anthropic-523b938e.md
    channel: web
    ingested_at: 2026-06-28
  - path: raw/web/web-claude-d9f04b5f.md
    channel: web
    ingested_at: 2026-06-28
  - path: raw/web/web-claude-30016237.md
    channel: web
    ingested_at: 2026-06-28
  - path: raw/web/web-behorden-claude-d4534954.md
    channel: web
    ingested_at: 2026-06-28
  - path: raw/web/web-secteur-public-claude-c856274e.md
    channel: web
    ingested_at: 2026-06-28
aliases:
  - Claude for Government
  - Claude Gov
  - Claude FedRAMP
  - Claude government
  - Claude for public sector
  - Claude IL5
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-28
updated: 2026-06-28
confidence: 0.8
last_confirmed: 2026-06-28
---

# Claude for Government

**TL;DR.** Anthropic's **Claude for Government** offering deploys Claude inside government environments with authorizations up to **FedRAMP High and IL5**, using procurement channels agencies already rely on. A dedicated **Claude Gov** model variant supports classified national-security missions on AWS [^src1].

## Deployment surfaces

Three paths are offered [^src1]:

| Surface | Authorization level | Infrastructure |
|---|---|---|
| **API** | Up to FedRAMP High + IL5 | AWS and Google Cloud |
| **Claude Gov models** | Classified environments | AWS only; built for national security missions |
| **Claude for Government app** | FedRAMP High | Hosted Claude application |

## Why agencies choose Claude

Anthropic markets three properties for the government segment [^src1]:

- **Intelligence for government complexity**: document analysis, regulatory review, and complex task automation; enhanced performance for government-specific workflows while maintaining accuracy.
- **Safety at its core**: "transparent reasoning you can trust in high-stakes decisions"; safety and responsible deployment baked into the model design rather than bolted on.
- **Secure, compliant, and accessible**: deploys via security frameworks agencies already use — "access advanced AI capabilities without compromising compliance requirements."

## Context

- The **FedRAMP** authorization track is shared with the financial services vertical — both require auditable, traceable outputs. See [Claude for Finance](/ai-engineering/claude-for-finance.md) for the finance-domain analogue.
- **Claude Gov models** (classified, AWS) represent a distinct product variant from the commercial lineup. No public performance details are available.
- For the underlying infrastructure: [Claude API](/ai-engineering/claude-api.md) covers the Claude Platform on AWS (commercial). For the security-research side of Anthropic's government relationship, see [Anthropic](/ai-engineering/anthropic.md) §Project Glasswing.
- Enterprise plan tier is the relevant procurement tier for non-classified government deployments; see [Claude Plans & Pricing](/ai-engineering/claude-plans.md).

## See also

- [Anthropic](/ai-engineering/anthropic.md) — company, Project Glasswing (security initiative), Claude Security product
- [Claude for Finance](/ai-engineering/claude-for-finance.md) — analogous vertical with SOC 2/FedRAMP compliance
- [Claude API](/ai-engineering/claude-api.md) — the underlying platform (commercial)
- [Claude Plans & Pricing](/ai-engineering/claude-plans.md) — Enterprise tier; HIPAA-ready offering available

---

[^src1]: [Government | Claude by Anthropic](../../raw/web/web-government-claude-by-anthropic-523b938e.md) — Anthropic solutions page; channel: web; collected 2026-06-28
