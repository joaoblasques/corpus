---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-from-googlebot-to-gptbot-whos-crawling-your-site-in-2025-9abe6d87.md
    channel: web
    ingested_at: 2026-08-24
aliases:
  - AI crawler landscape 2025
  - GPTBot ClaudeBot crawler share
  - Cloudflare Radar AI crawlers
tags:
  - corpus/ai-engineering
created: 2026-08-24
updated: 2026-08-24
---

# AI Crawler Landscape 2025 (Cloudflare Radar)

**TL;DR.** Cloudflare Radar data (May 2024 → May 2025) shows GPTBot displaced Bytespider as the dominant AI crawler, surging from 5% to 30% of AI-only crawler share; Meta-ExternalAgent entered at 19%; ClaudeBot fell from 27% to 21%. About 30% of global web traffic is bots. robots.txt compliance is voluntary; Cloudflare's AI Audit tools offer enforceable blocking. [^src1]

## AI-only crawler share shift (May 2024 → May 2025)

Data based on AI-only crawler user-agent matching, as a share of all AI crawler traffic [^src1]:

| Rank | Bot (May 2024) | Share | Rank | Bot (May 2025) | Share |
|---|---|---|---|---|---|
| 1 | Bytespider (ByteDance) | 42% | 1 | GPTBot (OpenAI) | 30% |
| 2 | ClaudeBot (Anthropic) | 27% | 2 | ClaudeBot (Anthropic) | 21% |
| 3 | Amazonbot | 21% | 3 | Meta-ExternalAgent (Meta) | 19% |
| 4 | GPTBot (OpenAI) | 5% | 4 | Amazonbot | 11% |
| 5 | Applebot | 4.1% | 5 | Bytespider | 7.2% |

**Key bot purposes** [^src1]:
- **GPTBot** — OpenAI crawler for training/improving ChatGPT-class LLMs
- **ClaudeBot** — Anthropic crawler for training and updating Claude
- **Meta-ExternalAgent** — Meta; likely LLM training/fine-tuning
- **Bytespider** — ByteDance; linked to Ernie or TikTok AI training
- **ChatGPT-User** — API/browser usage of ChatGPT interacting with web content

## Broader AI + search crawler trends

Measuring a fixed cohort of Cloudflare customers to remove customer-growth bias [^src1]:
- Total AI + search crawler traffic grew **+18%** from May 2024 to May 2025.
- Including new customers added in the period, the growth was **+48%**.
- Peak crawling in April 2025: **+32%** vs May 2024.
- **Googlebot** (search indexing) grew **+96%** in requests; its share of all tracked crawling jumped from 30% to 50%.

### Raw request volume changes (May 2024 → May 2025)

Selected significant movers [^src1]:

| Bot | Raw requests growth |
|---|---|
| ChatGPT-User | +2,825% |
| PerplexityBot | +157,490% |
| GPTBot | +305% |
| Googlebot | +96% |
| ClaudeBot | -46% |
| Bytespider | -85% |

## robots.txt and blocking

As of June 6, 2025, among 3,816 of the top 10,000 domains with a parseable robots.txt [^src1]:
- **~14%** had Allow or Disallow directives targeting AI bots specifically.
- **GPTBot** was the most blocked (312 domains: 250 fully, 62 partially) — and also the most explicitly allowed (61 domains).
- Trend: sites moving from passive robots.txt signals to active WAF-based blocking.

robots.txt compliance is **voluntary** for crawlers; Cloudflare's **AI Audit** tools allow enforceable blocking at the network level. [^src1]

## Context

AI crawlers collect data for LLM training, unlike search crawlers which index for search results. The content-access model is fundamentally different: AI crawlers repackage content inside their applications without driving referral traffic back to publishers. See [AI Crawl:Referral Ratio](/ai-engineering/sources/ai-crawl-referral-ratio-cloudflare-009f8507.md) for the economic impact, and [Pay-per-Crawl](/ai-engineering/sources/pay-per-crawl-cloudflare-8eb15448.md) for Cloudflare's publisher monetization response.

See also: [Web Scraping](/ai-engineering/web-scraping.md)

---

[^src1]: [From Googlebot to GPTBot: Who's crawling your site in 2025](../../../raw/web/web-from-googlebot-to-gptbot-whos-crawling-your-site-in-2025-9abe6d87.md) — Cloudflare blog, 2025; Cloudflare Radar data covering May 2024–May 2025 AI crawler market share shifts
