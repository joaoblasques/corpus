---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-introducing-pay-per-crawl-enabling-content-owners-to-charge-8eb15448.md
    channel: web
    ingested_at: 2026-08-24
aliases:
  - pay per crawl
  - HTTP 402 AI crawlers
  - Cloudflare pay per crawl
tags:
  - corpus/ai-engineering
created: 2026-08-24
updated: 2026-08-24
---

# Pay-per-Crawl (Cloudflare)

**TL;DR.** Cloudflare's pay-per-crawl (private beta) gives content publishers a third option beyond blocking or allowing AI crawlers for free: charge per request. Built on HTTP 402 Payment Required. Cloudflare acts as Merchant of Record. The technical foundation uses Ed25519-signed requests and EIP-3009 crypto authorization. Signals a future where AI agents autonomously pay for content access. [^src1]

## The binary-choice problem

Before pay-per-crawl, publishers faced two options [^src1]:
1. **Allow** — open access, AI trains on your content, you receive no compensation.
2. **Block** — wall off your content via robots.txt or WAF; AI can't access it.

After hundreds of conversations with news organizations, publishers, and social media platforms, Cloudflare found consistent demand for a third option: allow access but charge for it. Historically this required negotiating individual deals — only accessible to publishers with enough scale and leverage. [^src1]

## Publisher controls

Three options per crawler [^src1]:
- **Allow** — free access granted.
- **Charge** — payment required at a flat, domain-wide price per request.
- **Block** — access denied entirely.

If a crawler lacks a billing relationship with Cloudflare and thus can't be charged, selecting "Charge" acts as a network-level block (HTTP 403) — but signals that a paid relationship could exist in the future. Publishers can exempt specific crawlers from charges (e.g. for free partnerships). [^src1]

Pay-per-crawl rules are enforced after existing WAF and bot management rules — existing security posture is preserved. [^src1]

## Technical mechanism

### Crawler registration

Crawlers register with Cloudflare by [^src1]:
1. Generating an Ed25519 key pair; hosting the JWK-formatted public key in a directory.
2. Registering the key directory URL and user-agent with Cloudflare.
3. Including `Signature-Agent`, `Signature-Input`, and `Signature` headers (HTTP Message Signatures) on every request.

This prevents spoofing — only a registered crawler with the correct key can make a credible signed request.

### Payment flows

**Reactive (discovery-first)** [^src1]:
1. Crawler requests URL → receives HTTP 402 with `crawler-price: USD XX.XX`.
2. Crawler retries with `crawler-exact-price: USD XX.XX` header to confirm payment.
3. Server responds HTTP 200 with `crawler-charged: USD XX.XX`.

**Proactive (max-price)** [^src1]:
1. Crawler sends `crawler-max-price: USD XX.XX` upfront.
2. If content price ≤ max-price, request succeeds and charges at the configured price.
3. If content price > max-price, server returns HTTP 402.

Only one price declaration header (`exact` or `max`) per request.

### Billing

Cloudflare aggregates billing events, charges the crawler, and distributes earnings to the publisher. Cloudflare acts as Merchant of Record. [^src1]

## Agentic future

Pay-per-crawl is explicitly designed with the agentic web in mind [^src1]: "Imagine asking your favorite deep research program to help you synthesize the latest cancer research… and then giving that agent a budget to spend to acquire the best and most relevant content." By anchoring on HTTP 402, it enables AI agents to programmatically negotiate content access — discoverable, priceable, and payable without human-in-the-loop approval.

Compare to [x402 protocol](/ai-engineering/mcp.md) (Coinbase/Linux Foundation) which applies the same HTTP 402 mechanism to agentic API tool calls.

## Related

- [AI Crawler Landscape 2025](/ai-engineering/sources/ai-crawlers-cloudflare-radar-2025-9abe6d87.md)
- [AI Crawl:Referral Ratio](/ai-engineering/sources/ai-crawl-referral-ratio-cloudflare-009f8507.md)
- [Selling to AI Agents](/ai-business/selling-to-ai-agents.md)
- [Web Scraping](/ai-engineering/web-scraping.md)
- [MCP](/ai-engineering/mcp.md) — x402 agentic payment protocol integrates with MCP

---

[^src1]: [Introducing pay per crawl: Enabling content owners to charge AI crawlers for access](../../../raw/web/web-introducing-pay-per-crawl-enabling-content-owners-to-charge-8eb15448.md) — Cloudflare blog, 2025; private beta announcement, HTTP 402 mechanism, publisher options, Ed25519 signing, agentic payment future
