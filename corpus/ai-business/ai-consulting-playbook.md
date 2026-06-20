---
type: concept
domain: ai-business
status: draft
sources:
  - path: raw/youtube/youtube-n6t1kgxblqa.md
    channel: youtube
    ingested_at: 2026-06-17
  - path: raw/email/email-2026-06-16-turn-a-15-minute-call-into-a-1-500-offer.md
    channel: email
    ingested_at: 2026-06-20
aliases:
  - AI mini assessment
  - free AI assessment
  - AI consulting client acquisition
  - two-call close
  - money question
  - AI concierge
tags:
  - corpus/ai-business
  - concept
created: 2026-06-17
updated: 2026-06-17
confidence: 0.5
last_confirmed: 2026-06-17
---

# AI Consulting Playbook

**TL;DR.** A **free "AI mini assessment"** is a two-call client-acquisition framework for AI consultants: call one is a 15-minute, prescribe-nothing discovery using five questions; between calls you pick the single bottleneck at the intersection of *frequency × friction*; call two delivers one free fix and then asks "the money question" to upsell into a paid build. The presenter claims this converts 30–50% of free assessments into paying clients [^src1]. Self-reported and promotional (funnels to a free Notion template + the presenter's own consulting), but the discovery structure is concrete and reusable. This is the *client-acquisition* counterpart to the *offer-positioning* discipline in [[ai-business/monetizing-code|Monetizing Code]].

## The lens: three levers of ROI

Every assessment is framed against three ROI levers the prescription must serve [^src1]:
- **Effectiveness** — make them more revenue.
- **Efficiency** — return hours to their week.
- **Quality** — improve the product/service (happier customers).

The whole assessment goal is narrow: "find one bottleneck, prescribe one tool, and then upsell them to a paid assessment" [^src1].

## Call one — 15-minute discovery (prescribe nothing)

Purely fact-finding: ask, listen, and name the pain points back to them. "The key in this first call is we prescribe nothing" — the common trap is prescribing tools/solutions on call one [^src1]. Five questions [^src1]:

1. **Forking question** — what matters most: more money, hours back, or happier customers? (Selects the ROI lever.)
2. **Repetition question** — "what is your most repeated weekly task?" One usually stands out.
3. **Friction question** — where do things stall or slip through the cracks? Good candidates for AI/automation.
4. **ROI anchor** — quantify the value of time: how many hours/week does this cost, and what is that time worth? (Example: 2 hrs/week × \$200/hr = \$400/week recoverable.) Have the owner quantify it *in their own words* [^src1].
5. **Magic-wand question** — "if you could wave the magic wand and this ran itself… what would change?" (Presenter's favorite.)

Close call one by naming the single highest-opportunity bottleneck back to them and booking the follow-up [^src1].

## Between calls — frequency × friction

Research the uncovered bottlenecks and select the one at "the intersection of frequency and friction" — most ripe for AI — always weighted back to the lever the owner chose. Scope discipline: "we're focused on one bottleneck only. This is a free assessment… we want to give them value, but… not too much" [^src1].

## Call two — prescribe one solution (15–20 min)

A **three-way prescription decision tree** based on the bottleneck type [^src1]:
- **Common task** (email, call notes — pain points most owners share) → an **off-the-shelf tool**. Find it via the AI-tool directories *There's An AI For That* and *Futurepedia.io*, searchable by industry [^src1].
- **Task requiring judgment / writing / research** → **Claude Cowork**.
- **Repeatable workflow unique to their business** → a **custom Claude skill** — but you only describe *what* it would look like, not *how* to build it (this seeds the upsell): "you tell them the what, you don't give them the how" [^src1].

Bring three deliverables to call two: the **name** of the tool/prescription, its **cost**, and the **first step** they could take this week to implement it themselves [^src1].

## The money question

Deliver the free fix first (builds trust; raises the perceived value of the paid service), then ask "the money question" [^src1]:

> [verbatim] "do you want me to hand this off so that you can go implement it yourself or do you want me to build it with you or even build it for you" [^src1].

The claim: 30–50% of the time (sometimes more), the owner asks you to build it with/for them — converting to a paid client. Upsell paths named: the full (paid) assessment, an "AI concierge," or other services [^src1]. The rationale for giving away the "how": busy owners usually prefer to pay rather than DIY [^src1].

## The $1,500 AI assessment offer (15-minute call)

A concrete AI-consulting offer structure: convert a **15-minute discovery call** into a **$999–$1,999 AI assessment** [^src2]:

**The trigger**: during a brief introductory conversation, identify whether the prospect has manual, repetitive workflows. If yes, offer a formal assessment instead of a free consult.

**The ai-assessment Cowork skill**: a Claude Cowork skill that runs the assessment session automatically. It scores the prospect's workflow across three dimensions:
- **Effectiveness** — is the workflow achieving its goal?
- **Efficiency** — is it taking the right amount of time/effort?
- **Quality** — is the output meeting standards?

**Output deliverables** [^src2]:
1. Identified time sinks (the specific repetitive steps eating hours).
2. **Impact-Effort matrix** — maps each identified pain point by implementation effort vs. ROI.
3. Specific AI tool or automation recommendations per pain point.
4. ROI calculation: "here's what you get back per week if we fix this."

**Pricing** [^src2]: $999 for a standard assessment; $1,999 for enterprises or high-complexity workflows. Positioned as a professional service, not a free consult — the paid frame makes the output more actionable and the client more committed.

**The close**: present the assessment findings, identify the highest-ROI item, and ask "do you want me to build it?" — same two-call motion as the discovery-and-close playbook above, but with a paid gate between discovery and prescription.

## Relationship to other pages

- **vs. [[ai-business/monetizing-code|Monetizing Code]].** Monetizing Code covers *selling a result* and the *positioning one-pager* (articulating the offer); this page is the *operational discovery-and-close motion* that finds the result to sell. They reference the same "paid assessment as sales mechanism" idea — Monetizing Code's "the assessment is the pitch" and the asset-library "pull the matching skill, tune it, deliver" model — applied here as a structured two-call script with a custom-Claude-skill prescription path.
- **vs. [[ai-business/ai-synthetic-focus-group|AI Synthetic Focus Group]].** Sibling business-tactics source from the same newsletter ecosystem; both are concrete AI-monetization playbooks rather than capability/research content.

## Gotchas / promo framing

- **Self-reported conversion.** The 30–50% close rate is the presenter's own claim with no independent evidence; utility-scored low (5) as business-tactics content [^src1].
- **Lead-magnet funnel.** The episode repeatedly drives to a free Notion template (first/second-call scripts and checklists) and the presenter's "make money with AI / find clients" content stream — treat as marketing for the consulting business [^src1].
- **Tooling is incidental.** The named tools (There's An AI For That, Futurepedia, Claude Cowork, Claude skills) are illustrative; the durable part is the frequency × friction selection and the deliver-free-then-ask close.

[^src1]: [The free AI mini assessment — turn a cold business owner into a paying client](../../raw/youtube/youtube-n6t1kgxblqa.md) — AI consultant client-acquisition playbook; promotional (funnels to free Notion template + paid consulting)
[^src2]: [Turn a 15-Minute Call Into a $1,500 Offer](../../raw/email/email-2026-06-16-turn-a-15-minute-call-into-a-1-500-offer.md)
