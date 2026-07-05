---
type: concept
domain: blockchain
status: draft
sources:
  - path: raw/web/web-nft-god-newsletter-the-daily-alpha-7-15-e6a45d10.md
    channel: web
    ingested_at: 2026-07-05
  - path: raw/web/web-nft-god-newsletter-the-daily-alpha-7-10-795069c2.md
    channel: web
    ingested_at: 2026-07-05
  - path: raw/web/web-nft-god-newsletter-the-daily-alpha-7-5-33d51221.md
    channel: web
    ingested_at: 2026-07-05
  - path: raw/web/web-opensea-paper-handed-your-email-76aa91e2.md
    channel: web
    ingested_at: 2026-07-05
  - path: raw/web/web-gta-6-includes-crypto-and-nft-s-77b84448.md
    channel: web
    ingested_at: 2026-07-05
aliases:
  - NFT market
  - NFT floor price
  - NFT royalties
  - NFT pump and dump
  - NFT market dynamics
tags:
  - corpus/blockchain
  - concept
created: 2026-07-05
updated: 2026-07-05
---

# NFT Market Dynamics

**TL;DR**: NFT market dynamics circa 2022 were characterized by floor-price speculation, creator-royalty extraction, pump-and-dump mechanics, and infrastructure vulnerabilities. Sources are from the "NFT God" newsletter written by Alex Finn (then an NFT commentator, later a vibe-coding entrepreneur), covering July 2022 — a bear market period following the crypto crash of that year.

> **Temporal note**: these sources date from July 2022. The NFT market landscape has changed substantially since then; treat this as historical record.

## Floor price mechanics

**Supply vs. demand framing**: the practitioner view at the time was that projects focused too much on supply count (number of NFTs) as a proxy for value, when demand is the actual driver of floor price [^src1]. Supply is easily manipulated (via burns, staking, unlocks); demand must be driven by genuine utility or narrative.

**Demand levers observed** (2022):
- Hype and anticipation of utility before utility exists ("anticipation is more valuable than actual utility right now" [^src3]) — framed as investor-perspective observation, not normative claim
- Airdrop chains (Moonbirds → Oddities → further drops) to maintain holding incentive
- Tech demos and roadmap reveals (Yuga's Otherside stress test as price catalyst)
- Brand cross-overs (RTFKT + Nike)

## Supply manipulation tactics

**Burn mechanics**: WZRDs NFT project (July 2022) began burning all listings below a floor price threshold — if an NFT was listed below ~$3,000, it was automatically destroyed [^src1]. The author's critique: this is market manipulation that hurts holders (particularly those needing liquidity), and is ineffective because it doesn't create demand — it only reduces supply artificially. "Nobody was paying anything remotely close to the floor price of 3 ETH." [^src1]

**Staking**: projects offered "staking" rewards in project-specific tokens with no external value, rewarding holders for not selling while creating artificial demand-signal through locked supply.

**Ecosystem expansion**: large projects (Yuga Labs' Otherside, Doodles with Genesis Box) released sub-collections or companion collections with the stated goal of broadening the ecosystem but the structural risk of diluting demand for the original collection [^src4]. "If even a fraction of this additional supply hits the market it'll send floor prices cratering." [^src5]

## Royalty economics

**Yawww marketplace** (Solana, July 2022) launched a zero-royalty marketplace by routing trades as OTC transfers rather than on-chain transactions, bypassing the royalty enforcement layer [^src1]. This triggered industry debate about whether decentralization principles (free markets, permissionless trading) are in tension with creator economics.

Author's prediction: if zero-royalty trading became dominant, creators would move to Web2 business models (subscriptions, microtransactions) rather than per-transaction royalties [^src1].

**NFT royalties as a fragile right**: on-chain royalty enforcement was technically optional/bypassable on most chains in 2022, depending entirely on marketplace compliance — not protocol enforcement.

## Pump-and-dump mechanics

**The pattern** (repeated in sources): a project mints, influential early holders (often with coordinated off-chain communication) pump it across platforms, floor price rises to attract retail buyers, influencers sell into the retail demand, price craters [^src2]. Projects named: "The Saudis," "God Hates NFTees," "Moonrunners" — all described as losing most of their value within days of launch.

**Critique from the author**: "sucking this kind of liquidity out of the market with cheap meme projects is bad for everyone" while also acknowledging "nobody is forcing us to get into these projects" — personal responsibility framing alongside systemic critique [^src2].

## Security: the OpenSea data breach

OpenSea (June 2022) had user email addresses stolen via a Customer.io vendor breach and distributed to the dark web [^src4]. The author's risk framing: NFT holders' email addresses in a breach are higher-risk than typical breaches because:
1. The email is linked to a digital asset wallet (the breach reveals *who* holds valuable assets)
2. Crypto wallets are easy targets for phishing (one click on a malicious link can drain a wallet)
3. Dark web databases can be cross-referenced for password reuse

**Implications for Web3 infrastructure**: single points of failure (centralized email vendors, centralized marketplaces) contradict the decentralization premise. "Hopefully increased competition will reduce single points of failure like this in the future." [^src4]

## ENS domain speculation

ENS (Ethereum Name Service) three-digit `.eth` domains experienced a speculative resurgence in July 2022, with `000.eth` selling for 300 ETH (~$328K at the time) [^src3]. The "license plate" analogy: short domains are internationally legible (numbers transcend language), which drove demand.

Author's counter-thesis: short numeric ENS domains have no genuine utility, are not more memorable than words, and the speculative premium will disappear when ENS gains genuine utility — at which point *words and brands* will be more valuable than number combinations.

## Gaming/crypto integration thesis (historical)

**GTA 6 rumor (July 2022)**: leaks suggested Bitcoin rewards and Rockstar Coins for in-game stock exchange in GTA 6, not yet released at the time [^src5]. The author's framing: mainstream gamers and crypto communities have significant overlap potential but were not aligned in 2022 — many gaming media comment sections showed strong anti-NFT sentiment. GTA 6's adoption would be "a giant step forward towards that adoption." [^src5]

> [unsourced — please verify]: the GTA 6 crypto rumor's accuracy and whether the game ultimately included these features.

## Investor heuristics (author-provided)

From the "Daily Alpha" newsletter, bear-market 2022 context [^src1][^src2]:
- "If you can't figure out how they can pay that much money, there's a good chance you are putting your money in danger" (re: Celsius-style yield schemes)
- Wait for right entry timing; "the worst thing you can do is buy after a pump"
- Focus on demand drivers over supply mechanics
- Diversify across asset classes; NFTs as one allocation, not a portfolio

## See also

- [Bitcoin](/blockchain/bitcoin.md) — the base-layer cryptocurrency underlying NFT market activity
- [Bittensor (TAO)](/blockchain/bittensor.md) — decentralized AI network; adjacent use of blockchain for coordination
- [Zero-Knowledge Proofs](/blockchain/zero-knowledge-proofs.md) — cryptographic primitives relevant to privacy-preserving NFT mechanics
- [Selling to AI Agents](/ai-business/selling-to-ai-agents.md) — how crypto infrastructure may evolve to serve AI agent purchasing patterns

---

[^src1]: [NFT God Newsletter - The Daily Alpha 7/15](../../raw/web/web-nft-god-newsletter-the-daily-alpha-7-15-e6a45d10.md) — Alex Finn (as NFT God), July 2022
[^src2]: [NFT God Newsletter - The Daily Alpha 7/10](../../raw/web/web-nft-god-newsletter-the-daily-alpha-7-10-795069c2.md) — Alex Finn, July 2022
[^src3]: [NFT God Newsletter - The Daily Alpha 7/5](../../raw/web/web-nft-god-newsletter-the-daily-alpha-7-5-33d51221.md) — Alex Finn, July 2022
[^src4]: [Opensea Paper Handed Your Email](../../raw/web/web-opensea-paper-handed-your-email-76aa91e2.md) — Alex Finn, June/July 2022
[^src5]: [GTA 6 Includes Crypto and NFT's???](../../raw/web/web-gta-6-includes-crypto-and-nft-s-77b84448.md) — Alex Finn, June 2022
