---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-the-crawl-before-the-fall-of-referrals-understanding-ais-imp-009f8507.md
    channel: web
    ingested_at: 2026-08-24
aliases:
  - crawl referral ratio
  - Cloudflare AI Insights crawl ratio
  - Anthropic crawl referral 70900
tags:
  - corpus/ai-engineering
created: 2026-08-24
updated: 2026-08-24
---

# AI Crawl:Referral Ratio (Cloudflare Radar)

**TL;DR.** Cloudflare introduced a crawl:referral ratio metric on its AI Insights page, measuring how many HTML page requests an AI platform makes per referral it sends back to publishers. Anthropic (Claude) sits at 70,900:1 — it crawls ~71,000 pages for every page it refers. Mistral inverts this, sending 10× more referrals than crawls (0.1:1). The data shows AI platforms consume far more content than they return in traffic value. [^src1]

## Metric definition

**Crawl:referral ratio** = total HTML page requests from a platform's user agents ÷ total HTML page requests where the `Referer` header contains a hostname associated with that platform. Always normalized to a single referral request. [^src1]

Methodology notes [^src1]:
- Both training crawlers (e.g. `AIBot`) and user-request crawlers (e.g. `AIBot-User`) are aggregated under a single platform name.
- Traffic from Claude's native app lacks a `Referer` header, so native-app referrals are undercounted — stated ratios may overstate how little AI platforms refer, but by an unknown amount.
- Cloudflare's own ASN prefetch traffic (Google speculation rules) is excluded from referral counts.

## Sample ratios (week of June 19–26, 2025)

| Platform | Crawl:Referral ratio |
|---|---|
| Anthropic (Claude) | 70,900:1 |
| … (other AI platforms) | between |
| Mistral | 0.1:1 (sends 10× more referrals than crawls) |

Ratios vary week over week. Google saw a 19.4% decrease in ratio for that week (crawl traffic from GoogleBot dropped starting June 24). Yandex ratio grew due to increased crawling activity from June 21. [^src1]

## What this means for publishers

Search crawlers historically drove a virtuous cycle: crawl → index → send referral traffic → publisher monetizes. AI crawlers break this model. They consume more content, more frequently, while returning the same or less referral traffic relative to crawls. [^src1]

"These models continue to consume more content, more frequently, despite sending the same or less traffic to the source of its content." [^src1]

Cloudflare's response: new tools for publishers to block, charge, or allow AI crawlers on a per-platform basis. The crawl:referral ratio is published on the Cloudflare Radar **AI Insights page** with time-series and API access. [^src1]

## Related

- [AI Crawler Landscape 2025](/ai-engineering/sources/ai-crawlers-cloudflare-radar-2025-9abe6d87.md) — market share data for which bots are crawling
- [Pay-per-Crawl (Cloudflare)](/ai-engineering/sources/pay-per-crawl-cloudflare-8eb15448.md) — publisher monetization response
- [Web Scraping](/ai-engineering/web-scraping.md)

---

[^src1]: [The crawl before the fall of referrals: understanding AI's impact on content providers](../../../raw/web/web-the-crawl-before-the-fall-of-referrals-understanding-ais-imp-009f8507.md) — Cloudflare blog, 2025; introduces crawl:referral ratio metric, sample data June 19–26 2025
