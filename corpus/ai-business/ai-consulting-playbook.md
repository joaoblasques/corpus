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
  - path: raw/email/email-2026-06-23-what-fires-the-moment-a-client-says-yes.md
    channel: email
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-03DjE7j0Suw-the-easiest-way-to-actually-make-money-with-ai.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-mKyaNr3jK-E-start-a-1-person-business-with-claude-4-hour-course-2026.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - AI mini assessment
  - free AI assessment
  - AI consulting client acquisition
  - two-call close
  - money question
  - AI concierge
  - AI audit
  - AI assessment business
  - Return My Time
  - voice agent assessment
  - 1-person AI agency
  - Claude Code agency
  - Upwork freelancing AI
tags:
  - corpus/ai-business
  - concept
created: 2026-06-17
updated: 2026-06-25
last_confirmed: 2026-06-25
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

## Client onboarding automation (the "invisible tax" on closing)

Every new client close triggers 3–5 hours of manual setup: welcome email, project folder, kickoff doc, onboarding questionnaire. Five clients/month = a full workday lost to admin before any billable work starts [^src3].

A Claude Cowork workflow reduces this to under four minutes once the contract is signed [^src3]:

**Tools**: Claude Cowork (desktop app) + Gmail connector + Google Drive connector (both built-in, free).

**Build time**: 20–25 minutes for initial setup.

**Step 1 — The skill**: create a `client-welcome` skill. Input: client name, company name, industry, project type, start date. Generates three outputs: (1) a 120-word welcome email (warm, first-48-hours roadmap); (2) a kickoff doc outline (overview, success metrics, key contacts, timeline, open questions); (3) eight onboarding questionnaire questions tailored to industry/project type [^src3].

**Step 2 — Connect tools**: authenticate Gmail and Google Drive in Cowork Connectors. Add HubSpot or CRM connector if available [^src3].

**Step 3 — Manual trigger task**: "When I paste a client's intake data and email address, run the client-welcome skill on that input, then send the welcome email to the client via Gmail, and save the kickoff doc to a new Google Drive folder named after the client." Questionnaire sent as a scheduled follow-up 30 minutes after the welcome email [^src3].

**Step 4 — Extract intake data from call transcripts**: a closing-call prompt — "Extract: client name, company name, industry, project type, and start date. Output as a five-line list" — produces the six fields needed to trigger the task with no reformatting [^src3].

**Calibration loop**: after the first three onboardings, ask Cowork what the welcome package missed for the specific industry; update the skill prompt. "By client four, the output reads like it was written specifically for them" [^src3].

**Reported result**: "Onboard 10 clients in under 15 minutes" [^src3].

**Key stat**: operators who send the onboarding questionnaire within one hour of signing see 40% faster completion rates than those who send it the next business day; the Cowork scheduled send handles that timing automatically [^src3].

**Industry routing**: add conditional logic in natural language — "If the client industry is legal, add a section to the kickoff doc about intake workflow and document review. If the industry is construction, add a section on job costing and scheduling tools." Two sentences of instruction produce permanently customized output [^src3].

**Advanced trigger**: HubSpot deal-stage integration (added in early 2026) lets you fire the onboarding task automatically when a deal moves to "Closed Won" — no manual trigger, no third-party automation [^src3].

## AI audit business: voice-agent + Claude pipeline

A productized AI audit for small business owners — pricing at $1,000 per engagement — runs a fully automated discovery pipeline and upsells into ongoing services [^src4].

**The evolution of the product** [^src4]:
1. Physical walkthrough (not scalable).
2. 45-minute Zoom call → transcript fed into Claude → report delivered.
3. Current: a **voice agent** (Annie, built on Retell.ai) calls the owner, conducts a 20–30 minute discovery conversation, pipes the transcript to a separate AI agent that builds the report. No Zoom calls, runs 24/7.

"99 out of 100 people need the service" — self-reported from 50–100 business owner conversations [^src4].

**Report structure** (delivered via Gamma AI): executive summary → effort vs. impact matrix (quick wins: low effort, high impact) → recommended solutions per pain point with tool name, cost, and estimated time saved. Example: a wedding venue operations manager spending 2 hours every Saturday manually pulling Google Analytics + Meta Ads + Google Ads into a PowerPoint → one off-the-shelf tool (Dash This, $42/month) eliminates the manual work, saving ~8 hours/month [^src4].

**Pricing ladder** (self-reported): started free for testimonials → $200 → $500 → $1,000 [^src4].

**Upsell**: "3 to $5,000 upsell all day" — the audit identifies pain points; you prescribe the tool; the close is "do you want me to implement it?" Same two-call-to-close motion as the mini assessment above. "99 out of a hundred people need the service" [^src4].

**Technical depth is not required**: "you just need to be one step ahead of your average client, which is literally you studying this stuff for 7 days" [^src4]. The durable parts: a Gamma template for consistent report formatting, Claude for tool research per pain point, a voice agent for scalable discovery.

Free audit template available at audittemplate.ai [^src4]. (Cited as a free resource by the presenter; treat as promotional.)

## 1-person AI agency: the beginner-to-client ladder

A structured beginner path to building a 1-person AI services business using Claude Code, with explicit skill/trust levels and outreach channels [^src5].

**The AI adoption gap as the opportunity** [^src5]:
- 84% of people have never used AI.
- 16% have used free chatbots.
- 0.3% pay $20/month for AI.
- 0.04% use max-tier models (Claude Code, Codex).

"This allows us, the 0.04%, to provide services to the rest of the 8 billion people that don't know how to use AI effectively yet. To these people, your AI services is going to seem like magic" [^src5].

**Three service tiers** [^src5]:
1. **AI-generated websites** — largest addressable market (~27–30% of US small businesses have no website = ~10M businesses); lowest technical bar; ideal first service.
2. **Automations and agents** — level up once websites are mastered; requires API/integration knowledge.
3. **Full AI systems** — aggregates automations from level 2 into a comprehensive AI OS for the business; highest value, requires the most expertise.

**Getting first clients** (before building anything) [^src5]:
- **Upwork** — create a profile as a freelancer in IT/automation; start at $0 and accept any project to build testimonials and reviews; proposal quality and profile completeness determine which listings you win.
- **Cold email** — build lead lists and run automated outreach campaigns.

**The trust-first trap**: "A wise man once said you have to get good before you can get rich." First clients may require free or discounted work to build testimonials [^src5]. The presenter's own first paid client closed after 4 months, at $400 [^src5].

**Claude Code as the delivery engine**: Claude Code handles 90–95% of the actual build work; the practitioner's role is requirements clarity, client communication, and taste/judgment. A private GitHub repo for the workspace is strongly recommended (recover from hardware failure) [^src5].

**The compounding flywheel**: post finished work publicly (LinkedIn, YouTube) → attracts inbound inquiries → reduces reliance on cold outreach over time [^src5].

## Gotchas / promo framing

- **Self-reported conversion.** The 30–50% close rate is the presenter's own claim with no independent evidence; utility-scored low (5) as business-tactics content [^src1].
- **AI audit source** is a podcast interview (The Koerner Office) with the assessment operator; all revenue numbers ($1K/assessment, $3–5K upsell) are self-reported and unverified [^src4].
- **1-person agency course** is a 4-hour promotional tutorial; presenter runs a paid community ("1% in AI") — treat client-acquisition and income claims as illustrative [^src5].
- **Lead-magnet funnel.** The episode repeatedly drives to a free Notion template (first/second-call scripts and checklists) and the presenter's "make money with AI / find clients" content stream — treat as marketing for the consulting business [^src1].
- **Tooling is incidental.** The named tools (There's An AI For That, Futurepedia, Claude Cowork, Claude skills) are illustrative; the durable part is the frequency × friction selection and the deliver-free-then-ask close.

[^src1]: [The free AI mini assessment — turn a cold business owner into a paying client](../../raw/youtube/youtube-n6t1kgxblqa.md) — AI consultant client-acquisition playbook; promotional (funnels to free Notion template + paid consulting)
[^src2]: [Turn a 15-Minute Call Into a $1,500 Offer](../../raw/email/email-2026-06-16-turn-a-15-minute-call-into-a-1-500-offer.md)
[^src3]: [What fires the moment a client says yes (Return My Time newsletter)](../../raw/email/email-2026-06-23-what-fires-the-moment-a-client-says-yes.md)
[^src4]: [The Easiest Way to Actually Make Money With AI](../../raw/youtube/youtube-03DjE7j0Suw-the-easiest-way-to-actually-make-money-with-ai.md) — The Koerner Office; AI audit/assessment business w/ voice agent; all revenue figures self-reported
[^src5]: [Start a 1-Person Business with Claude (4 Hour Course 2026)](../../raw/youtube/youtube-mKyaNr3jK-E-start-a-1-person-business-with-claude-4-hour-course-2026.md) — Albert Olgaard; beginner-to-client ladder for Claude Code agency; promotional (paid community CTA)
