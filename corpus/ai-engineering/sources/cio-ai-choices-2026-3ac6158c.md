---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-the-cio-s-choices-are-clear-in-2026-3ac6158c.md
    channel: web
    ingested_at: 2026-08-24
aliases:
  - CIO AI choices 2026
  - enterprise AI spending 2026
  - software sector performance 2026
  - agent substitution software
  - payment processor vs software business
tags:
  - corpus/ai-engineering
  - source
  - enterprise-ai
  - market-analysis
  - saas
created: 2026-08-24
updated: 2026-08-24
---

# The CIO's Choices Are Clear in 2026: Public Market Signal on Enterprise AI Spending

**TL;DR.** Tom Tunguz analysis using public software sector returns as a proxy for CIO purchasing priorities in 2026. The pattern: fund the AI stack (infrastructure + security), cut horizontal business applications. Only 2 of 5 software sectors are positive 1Y. Agent substitution is beginning to bite seat-based SaaS. [^cio]

## Sector performance (1Y, as of ~mid-2026)

| Sector | 1Y Return | Revenue Growth | EV/Sales | Verdict |
|---|---|---|---|---|
| Infrastructure & Dev Tools (13 names) | **+68.5%** | 21.4% | 10.0x | CIOs buying: compute, data stack, developer tooling |
| Security (8 names) | **+17.6%** | 24.1% | 11.6x | Only other positive sector; fastest growth; highest multiple |
| AI & Mega-cap Platforms (9 names) | -5.9% | 21.5% | — | High growth insufficient; too mature / priced in |
| Communications & Collaboration (9 names) | -6.6% | 8.2% | 2.4x | Down sector; one exception: Twilio +62% |
| Business Applications (48 names) | **-36.2%** | 12.5% | 3.4x | "The carnage" — most of public SaaS; seat-priced layer |

Representative names [^cio]:
- Infrastructure leaders: DigitalOcean (+430% 1Y), Datadog, Snowflake, Cloudflare, MongoDB, Confluent
- Security: Palo Alto Networks, Fortinet, CrowdStrike, Okta
- Business Applications (declining): Salesforce, Workday, ServiceNow, Monday.com, HubSpot, Atlassian

## The key insight: growth doesn't separate winners from losers

Infrastructure, Security, and Mega-caps all grow around 21% revenue — yet their returns diverge sharply. "What separates them is category. The market pays premium multiples for sectors CIOs believe are necessary during AI, & punishes horizontal application software where AI threatens the seat-based model." [^cio]

## The Twilio exception — the "payment processor" model

Twilio is up +62% in a sector (Communications) down -6.6%. The explanation: AI agents send messages, and every agent needs a phone number. Twilio sits on the *token path* — agents consume its service at scale even as it displaces the humans who used the product before [^cio].

The framing from Tunguz: **payment processor vs. software business**. Companies on the token path (per-transaction infrastructure: DigitalOcean, Cloudflare, MongoDB, Twilio) benefit from agent volume. Horizontal seat-priced software is exposed to agent substitution — agents reduce headcount, headcount reduction reduces seat count [^cio].

## Agent substitution is arriving

Marc Benioff, The Logan Bartlett Show, September 2025: "I've reduced it from 9,000 heads to about 5,000, because I need less heads." Agentforce now handles ~50% of Salesforce's customer interactions; support costs down 17% [^cio].

"Every CIO running Service Cloud just heard that on the same podcast." [^cio] — the signal: Salesforce's own Agentforce is displacing Salesforce seats. CIOs are drawing the same inference for their own tools.

## Implication for the AI stack

CIOs are funding two categories:
1. **AI infrastructure** — compute, data platforms, dev tooling, vector stores, model APIs — because agents run on it
2. **Security** — because AI expands both attack and defense surfaces

Everything else is under scrutiny for agent substitution or defunding.

## Related corpus pages

- [AI Agent](/ai-engineering/ai-agent.md) — agent systems that are driving this substitution
- [Enterprise AI adoption](/ai-engineering/enterprise-ai-adoption.md) [unsourced — may not exist yet] — broader enterprise patterns

---

[^cio]: Tom Tunguz, "The CIO's Choices are Clear in 2026," tomtunguz.com, 2026-07-01. `raw/_inbox/web-the-cio-s-choices-are-clear-in-2026-3ac6158c.md`
