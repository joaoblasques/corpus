---
type: source
domain: ai-engineering
status: complete
sources:
  - path: raw/_inbox/pdf-internet-advertising-an-interplay-among-advertiser-part-01.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-internet-advertising-an-interplay-among-advertiser-part-02.md
    channel: pdf
    ingested_at: 2026-07-17
  - path: raw/_inbox/pdf-internet-advertising-an-interplay-among-advertiser-part-03.md
    channel: pdf
    ingested_at: 2026-07-17
aliases:
  - computational advertising survey
  - internet advertising interplay
tags:
  - corpus/ai-engineering
  - source
created: 2026-07-17
updated: 2026-07-17
---

# Internet Advertising: An Interplay Among Advertisers, Online Publishers and Web Users

**Source type**: Academic survey paper (3 parts / ~120 pages)  
**Channel**: PDF  
**Topic**: Computational advertising — the ML, auction theory, and optimization problems in online advertising ecosystems

## Summary

A comprehensive survey of the internet advertising ecosystem covering the computational challenges from all three parties: advertisers (bidding, budget optimization), publishers (ad placement, pricing), and users (click modeling, behavioral targeting). Heavy on auction theory (GSP, second-price), algorithmic/ML components (CTR prediction, RTB bidding, relevance ranking), and privacy considerations [^src1].

## Structure

| Chapter | Topic |
|---|---|
| 1 | Introduction: ecosystem overview, stakeholder roles |
| 2 | Ad auction mechanisms: GSP, Vickrey, sponsored search |
| 3 | Relevance optimization: CTR prediction, semantic advertising, user intent |
| 4 | Real-Time Bidding (RTB): DSP/SSP/ADX/DX architecture |
| 5 | Display advertising: targeting, behavioral targeting, privacy |
| 6 | Mobile advertising: location-aware, push vs. pull |
| 7 | Future directions: click-through feedback, multi-armed bandits |
| A | Terminology glossary |

## Ecosystem Architecture

The survey maps the computational advertising stack [^src1]:

- **Advertiser** → sets bids, keywords, creatives, budgets
- **Ad Exchange (ADX / DX)**: marketplace where publishers sell impressions and advertisers buy them
- **Demand Side Platform (DSP)**: automated bidding platform for advertisers; participates in multiple auctions simultaneously
- **Supply Side Platform (SSP)**: automated platform for publishers; creates multiple auctions for same impression across exchanges
- **Data Exchange**: marketplace for user profiles (used in RTB)
- **Publisher** → sells ad slots; revenue depends on CTR and auction design

## Key ML/Computational Problems

**CTR Prediction**: predicting click-through rate for a (query, ad) pair. Key features: query-ad semantic match, user history, position, time. Techniques: logistic regression, gradient boosted trees, contextual bandits [^src1].

**Sponsored Search Auctions (GSP)**: advertiser pays the next highest bid (not own bid). GSP is not incentive-compatible (unlike VCG), but in practice bidders adopt symmetric Nash equilibria that make it efficient. Edelman et al. (2007) proved this [^src1].

**Real-Time Bidding (RTB)**: per-impression auction run in <100ms at serving time. Advertisers use Pre-Set Bidding (PSB) or adjust bids at runtime using context (user profile, page content). RTB is the dominant display ad mechanism as of the survey date [^src1].

**Relevance-Revenue Optimization**: publisher ranks ads by (bid × quality score) not just bid — ensures high-CTR ads appear higher. Google's AdWords uses this. Balances revenue (high bid) with user experience (relevant ads) [^src1].

**Behavioral Targeting**: profile users across sessions via cookies/browsing history. Privacy tension: PII identification risk vs. targeting revenue. Regulatory frameworks (IAB Self-Regulatory Principles) aim to limit cross-site PII aggregation [^src2].

**Semantic Advertising**: match ads to page content via topic models / keyword extraction. Reduces reliance on query keyword match — enables contextual ads on arbitrary web pages [^src2].

## Glossary (Key Terms)

| Term | Definition |
|---|---|
| CTR | Clicks / Impressions |
| CPC | Cost per Click (advertiser pays per click) |
| CPM | Cost per Mille-Impressions (per 1000 displays) |
| GSP | Generalized Second Price auction — pays next-highest bid |
| RTB | Real-Time Bidding — per-impression auction at serving time |
| DSP | Demand Side Platform — automated bidding for advertisers |
| SSP | Supply Side Platform — impression selling for publishers |
| PII | Personally Identifiable Information |
| Organic result | Non-paid search result |
| Landing page | Page shown after ad click |

## Related Corpus Pages

- Auction mechanisms and game theory: see [/ai-engineering/optimization-for-ml.md](/ai-engineering/optimization-for-ml.md) (duality, constrained optimization)
- ML methods (CTR prediction, bandits): [/ai-engineering/prompt-engineering.md](/ai-engineering/prompt-engineering.md) (adjacent: language models for ad generation)

---

[^src1]: [Internet Advertising Survey, Part 1 — ecosystem overview, GSP auctions, sponsored search, RTB](../../../raw/pdf/pdf-internet-advertising-an-interplay-among-advertiser-part-01.md)
[^src2]: [Internet Advertising Survey, Part 2 — relevance optimization, semantic advertising, behavioral targeting, privacy](../../../raw/pdf/pdf-internet-advertising-an-interplay-among-advertiser-part-02.md)
