---
type: concept
domain: ai-business
status: draft
sources:
  - path: raw/web/ai-is-slowing-down.md
    channel: web
    ingested_at: 2026-06-16
aliases:
  - AI bubble
  - AI is slowing down
  - AI economics
  - AI unit economics
  - generative AI sustainability
  - token-based billing
  - AI ROI
  - Ed Zitron
  - Where's Your Ed At
  - AI capex
  - data center buildout
tags:
  - corpus/ai-business
  - concept
created: 2026-06-16
updated: 2026-06-16
provisional: false
confidence: 0.5
last_confirmed: 2026-06-16
---

# AI Economics & the Bubble Thesis

**TL;DR.** A caustic opinion/analysis piece by Ed Zitron (*Where's Your Ed At*) arguing that generative AI's business model is economically unviable: the data-center capex and compute commitments already made demand revenue growth that the author argues cannot plausibly materialize. The author's central claim — "AI cannot, under any circumstances, slow down" — is that Anthropic and OpenAI must roughly double their businesses yearly through ~2030 while becoming profitable and raising hundreds of billions [^src1]. The piece's load-bearing evidence for *ai-business* readers is the worker/spend reality: the Q1-2026 shift to **token-based billing** triggered enterprises (Uber, Brex, T-Mobile) to **cap per-employee AI spend** within months, which the author reads as demand already slowing [^src1]. This is an explicitly polemical short-position-free essay, not neutral reporting; treat figures as the author's framing of industry projections.

## The core thesis: AI can't afford to slow down

The author argues the infrastructure buildout and compute commitments require generative AI to generate "over $2 trillion in annual revenue by 2030" or "none of the data center capex makes sense" [^src1]. The framing: this isn't the author's judgment but the industry's own promises and projections [^src1].

Key figures the author attributes to the industry (presented as his reading of public statements/reports, not independently audited here):
- ~190GW of planned data centers (Sightline Climate, Feb) at Jensen Huang's stated $80–100B/GW implies a $9.5–15T buildout — the author says Bloomberg "incorrectly" called it a "$3 trillion" buildout [^src1].
- Anthropic: ~$330B in compute/chip commitments (Google, Amazon, Microsoft) plus $30B (CoreWeave) and $15B (SpaceX); must hit projected ~$174B/yr revenue by 2029 [^src1].
- OpenAI: projected to "burn at least $852 billion through the end of 2030," with >$770B in compute commitments, and the March $122B round called "insufficient" [^src1].
- The author claims Anthropic and OpenAI represent "at a minimum 70%, if not 80% to 90%" of all AI compute demand, and cites *The Information* that the two make up "89% of all AI startup revenues" [^src1].

The author's conclusion: justifying the compute being built "likely means at least two other OpenAI or Anthropic-scale companies" worth of additional demand [^src1].

> [unsourced — please verify] These dollar figures originate from the author's synthesis of third-party statements (Huang, Bloomberg, FT, *The Information*). They are the author's framing, not corpus-verified; cite the original reports before treating any as fact.

## The ai-business signal: token billing and capped spend

The most career/work-relevant claims — and the most concrete — concern enterprise reaction to **usage-based (token) billing**, which the author says Anthropic and OpenAI only moved customers to in **Q1 2026** [^src1]:

- **Spend caps appeared within months.** Uber "burned through its entire annual token budget in a single quarter," then capped employee spend at $1,500/month per user; T-Mobile followed temporarily at $2,000/month; Brex limits engineers to $500/week and non-engineers to "an astonishingly-low $5 a week" [^src1].
- **Cost visibility is poor.** The author cites a (then-unreleased) KPMG survey: 26% of companies say they have a comprehensive view of AI costs, 50% "some visibility," and 22% "no visibility or visibility after billing" [^src1].
- **ROI is contested.** The author cites Uber's COO saying it was "harder to justify spending money on AI tokens because it couldn't show a link between that spend and a meaningful increase in useful features" [^src1].

The author reads these as evidence demand is "slowing just as it needs to speed up" [^src1]. For a worker, the practical implication the piece surfaces (without endorsing the hype either way): AI tool spend is becoming a **measured, budgeted, ROI-scrutinized line item** rather than a subsidized free-for-all — and the subsidy ("$20, $100, or $200 for the entire month") historically hid model failures from users [^src1].

## The "loops" critique (agentic coding)

The author flags that Claude Code's Boris Cherny and OpenClaw's Peter Steinberger have urged users to "design loops for their agents" — which the author interprets as "creating ways to make their agents burn a bunch of tokens" to keep revenue up [^src1]. He notes both can expend "$130,000 to $1.3 million a month in tokens," i.e. they don't personally bear the cost [^src1]. This is a pointed counter-narrative to the prevailing agentic-coding enthusiasm; the author frames it as vendor incentive to maximize token consumption rather than a productivity practice.

## The author's framing and disclosures (read critically)

This is opinion, and the author is openly hostile to AI boosters; attribute its claims, don't adopt its conclusions wholesale:
- **Self-disclosed stance:** the author states he holds no short position, no "stocks, securities, or CFDs," and frames the piece as moral/journalistic rather than financial [^src1].
- **Promotional context:** the piece repeatedly markets the author's $70/yr premium newsletter and teases a forthcoming story he says "will likely confirm the absolute worst fears of the AI industry" [^src1].
- **Tone:** heavily polemical and profane ("Business Idiots," "paypigs," the extended "giant metal spider from Wild Wild West" analogy for unreliable, costly AI output) [^src1]. The author argues LLMs have produced mostly "shovelware … useless, insecure slopware" [^src1].
- **Worker sympathy:** the author claims tech workers are "in fucking agony" under "do as much AI as possible or we'll fire you" mandates and solicits anonymous sources [^src1].

## Relationship to other corpus claims

This page is a deliberate **counterweight** to the more pragmatic-bullish reads elsewhere in the domain. It does not contradict them on facts so much as on outlook:
- [AI and the Job Market](/ai-business/ai-and-the-job-market.md) argues the durable edge is *applying* AI to messy business context (AI-as-utility). This source agrees AI is hard to extract ROI from, but draws the opposite macro conclusion — that the spend itself is unsustainable, not just under-applied. Where that page sees new "appliance-building" roles, this one sees CFOs capping budgets [^src1]. (Deferred-update: the job-market synthesis may later be enriched with this contrarian/economic lens; not edited here.)
- [Monetizing Code](/ai-business/monetizing-code.md) — the "sell a result, prove the ROI" discipline is directly reinforced by the enterprise demand for measurable AI spend [^src1].

## Gotchas

- **Provenance of figures.** Nearly every dollar figure is the author's restatement of someone else's number (Huang, Bloomberg, FT, *The Information*, KPMG). Verify against primaries before citing as corpus fact.
- **Polemic ≠ data.** The piece mixes a handful of concrete, sourced enterprise facts (spend caps, KPMG survey) with sweeping rhetorical claims. Keep the two separate.
- **Time-sensitive.** Claims are pinned to mid-2026 projections and a "next two weeks" teased story; revisit `last_confirmed` if a newer source confirms or refutes the spend-cap / slowdown trend.

[^src1]: [AI Is Slowing Down — It Needs $3 Trillion Or More In Revenue By End Of 2030](../../raw/web/ai-is-slowing-down.md)
