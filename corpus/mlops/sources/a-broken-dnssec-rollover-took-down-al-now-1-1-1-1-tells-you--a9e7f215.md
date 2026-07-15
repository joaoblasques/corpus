---
type: source
domain: mlops
status: stub
sources:
  - path: raw/web/web-a-broken-dnssec-rollover-took-down-al-now-1-1-1-1-tells-you-a9e7f215.md
    channel: web
    ingested_at: 2026-07-15
aliases: []
tags:
  - corpus/mlops
  - source
  - doc-quick-intake
created: 2026-07-15
updated: 2026-07-15
provisional: false
url: https://blog.cloudflare.com/dnssec-nta-ede-33/
origin: obsidian-list
---

# A broken DNSSEC rollover took down .AL. Now 1.1.1.1 tells you when validation is bypassed

> **Quick intake** (obsidian-list). [open source](https://blog.cloudflare.com/dnssec-nta-ede-33/)

A DNSSEC rollover failure took down .AL domains, and Cloudflare's 1.1.1.1 DNS resolver implemented a Negative Trust Anchor to keep domains reachable, but without DNSSEC validation. A new EDE code (33) signals the presence of a Negative Trust Anchor in the DNS response. This brings transparency to DNSSEC failures and allows clients to understand the validation status of responses.

**Key topics**
- DNSSEC rollover failure
- Negative Trust Anchor
- Cloudflare 1.1.1.1
- Extended DNS Error (EDE) code 33
- DNSSEC validation status
