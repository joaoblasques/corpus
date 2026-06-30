---
type: concept
domain: ai-business
status: draft
sources:
  - path: raw/_inbox/web-we-re-in-1905-why-electricity-not-dot-com-is-the-right-ai-an-0390799e.md
    channel: web
    ingested_at: 2026-06-30
  - path: raw/_inbox/web-notes-from-the-field-ai-energy-shocks-the-end-of-the-old-pla-c8736206.md
    channel: web
    ingested_at: 2026-06-30
aliases:
  - 1905 analogy
  - dynamo and computer
  - Paul David AI
  - productivity paradox
  - electricity analogy AI
  - swapping motors not factories
tags:
  - corpus/ai-business
  - concept
created: 2026-06-30
updated: 2026-06-30
---

# AI Transition Economics: The 1905 Analogy

**TL;DR** — The correct historical analogy for AI is not the dot-com boom but electrification — specifically, 1905, the point when electricity existed but factories hadn't yet reorganized around it. Paul David's 1990 paper on "The Dynamo and the Computer" explains why productivity gains from general-purpose technologies are delayed by decades: the architecture must change, not just the tool [^src1].

## Paul David's productivity paradox

In 1990, economist Paul David published "The Dynamo and the Computer" to explain why US productivity growth slowed in the 1970s–80s despite the spread of computers. His finding: when factories switched from steam to electric motors (1880s–1920s), productivity initially *fell* — then surged once factories restructured around electricity rather than just swapping the motor into the old factory layout [^src1].

The key insight Joe Reis draws: **you can swap the motor (AI) into the old factory (existing data/software org) and get marginal gains, or you can rebuild the factory around the motor and get transformational gains** [^src1]. Most organizations are currently at the "swap the motor" stage.

The dot-com analogy implies this is a bubble about business models. The electricity analogy implies it's infrastructure that will transform productivity — but only after a long transition during which the architecture adapts [^src1].

## Why 1905, not 2000

1905 was the year electrification had widespread commercial availability but most factories hadn't yet reorganized around it. The productivity surge came ~20–30 years later as architectural assumptions changed [^src1]:
- Factory layouts (machines arranged around a central shaft vs. independent electric motors)
- Labor organization (specialized electric operators)
- Supply chain design (refrigerated transport, electric pumps)

The implication for the 2020s AI transition: we're in the early phase where the technology exists but the organizational, workflow, and architectural changes needed to capture value are still ahead of us [^src1].

## The data industry's specific failure mode

Joe Reis's field observation: data teams and MDS vendors are **repeatedly "swapping motors not factories"** [^src1]. Specific patterns he names:

- Using AI to accelerate existing ETL workflows rather than rethinking what data infrastructure should look like when AI is the primary consumer
- Data catalogs built for human querying, not for LLM context retrieval
- Dashboard-first BI tools pivoting to "AI features" rather than asking what dashboards are even for in an agentic world
- Vendors scrambling to add AI capabilities to products whose core assumption (human as analyst) is being disrupted

> "Dashboards are cooked." [^src2] — Zach Wilson (Data with Zach), agreeing with Joe Reis's framing that traditional BI is structurally misaligned with AI-first data consumption.

## Energy shocks and field uncertainty

As of mid-2026, Reis's field notes report MDS vendors in active pivot mode, uncertainty about which data infrastructure assumptions survive, and energy shocks as a real constraint on AI infrastructure scaling [^src2]. The "old playbook" (data lake → warehouse → BI tool → human analyst) is under pressure but the replacement architecture isn't settled [^src2].

## Strategic implications

For practitioners navigating the transition [^src1]:

1. **Understand which factory assumptions you're carrying**: which parts of current data architecture assume a human analyst as the end consumer?
2. **Bet on picks and shovels, not wrappers**: infrastructure that supports AI-first data consumption (semantic layers, context platforms) vs. thin AI wrappers on existing tools
3. **Expect a long transition**: the productivity gains are real but delayed; survival requires staying solvent through the architectural change period

See also [[ai-business/ai-and-the-job-market|AI and the Job Market]] for workforce implications, and [[data-engineering/ai-impact-on-data-engineering|AI's Impact on Data Engineering]] for the specific DE architectural rethink.

## See also

- [[ai-business/ai-and-the-job-market|AI and the Job Market]] — workforce implications of the transition
- [[data-engineering/ai-impact-on-data-engineering|AI's Impact on Data Engineering]] — the DE-specific architectural rethink
- [[data-engineering/semantic-layer|Semantic Layer]] — "context teams" as the factory-of-the-future framing
- [[ai-business/ai-economics-bubble|AI Economics & the Bubble Thesis]] — contrasting bear-case view

---

[^src1]: [We're in 1905 — Why Electricity, Not Dot-Com, Is the Right AI Analogy](../../raw/_inbox/web-we-re-in-1905-why-electricity-not-dot-com-is-the-right-ai-an-0390799e.md) — Joe Reis, 2026
[^src2]: [Notes from the Field: AI Energy Shocks, the End of the Old Playbook](../../raw/_inbox/web-notes-from-the-field-ai-energy-shocks-the-end-of-the-old-pla-c8736206.md) — Joe Reis, 2026
