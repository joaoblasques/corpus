---
type: concept
domain: ai-business
status: draft
confidence: 0.85
last_confirmed: 2026-08-17
sources:
  - path: raw/web/web-would-breaking-up-big-tech-work-what-would-benedict-evans-e5895f6d.md
    channel: web
  - path: raw/web/web-why-amazon-has-no-profits-benedict-evans-11c88595.md
    channel: web
  - path: raw/web/web-is-content-moderation-a-dead-end-benedict-evans-e5275a95.md
    channel: web
  - path: raw/web/web-the-death-of-the-newsfeed-benedict-evans-b0652643.md
    channel: web
  - path: raw/web/web-office-messaging-and-verbs-benedict-evans-0fcadd5c.md
    channel: web
aliases:
  - network effects
  - platform economics
  - big tech antitrust
tags:
  - platforms
  - network-effects
  - antitrust
  - social-media
  - tech-industry
created: 2026-08-17
updated: 2026-08-17
---

# Platform Dynamics

TL;DR: Network effects create structural dominance that persists independently of anti-competitive behavior. Breaking up platforms doesn't dissolve network effects. Content moderation is Sisyphean for the same reason — the answer is changing the model, not scaling the moderation. The real question for any tool is what underlying business *verb* it serves, not what features it has.

## Network Effects as Natural Monopoly

Network effects behave like natural monopolies: dominance persists not because of anti-competitive behavior but because of the product's mechanics.[^1] Market size determines how many networks can coexist — 50–100M PC users supported one network; 4B+ smartphone users gave room for iOS and Android.

The AT&T breakup (1982) created competition in long-distance and equipment but local access remained a natural monopoly (copper to every home). Normal consumers still had no choice. Separating Instagram from Facebook wouldn't change Instagram's network effects. "You don't use WhatsApp because Facebook owns it."[^1]

The "break them up and they'll compete with each other" argument — YouTube Inc. making a search engine; Google making a new video site — is "magical thinking" — they would be on the wrong side of network effects.[^1]

## What Antitrust Can Actually Do

The alternative to breakups is regulation that inserts competition or cuts prices by addressing internal mechanics, pricing, and infrastructure:[^1]

- **EU local loop unbundling**: gave competitors access to last-mile copper → incumbents fell below 50% DSL share in most European countries
- **EU roaming price caps** and **credit card interchange rate caps**: targeted interventions with measurable outcomes
- **CMA approach to Google/Facebook**: requiring Google to share click/query data with rivals; restricting default-position sales; requiring Facebook to offer contact-finding to third-party platforms

Technology markets change fast — Microsoft lost its dominance not to antitrust but to smartphones. Detailed line-by-line regulation risks being wrong before the ink dries.[^1]

## Amazon's Zero-Profit Strategy

Amazon reports near-zero net income deliberately. The company operates as dozens of semi-autonomous teams, each with their own internal P&L. Some mature and profitable; some are new startups losing money.[^2]

**Profit is opinion, cash is a fact.** Amazon focuses on free cash flow (FCF) and operating cash flow. Starting in 2009, capex/sales ratio exploded — invested into fulfillment centers (Prime flywheel) and AWS. Evidence suggests the existing business hasn't become more capex-intensive; the surge is investment in new businesses.[^2]

"Amazon is a bundle." Prime is the clearest expression: expensive content rights at high fixed cost and no marginal cost per subscriber, to enhance Prime membership, which drives more spending across Amazon.

At time of writing, Amazon had ~1% of US retail by value. Bezos's view: keep investing because taking profit would mean surrendering opportunity.[^2]

## Content Moderation as Structural Problem

The parallel between PC security (1990s–2000s) and social media content moderation is direct:[^3]

- Microsoft faced a "trustworthy computing" crisis when malware exploded. The malware targeted buffer overflows.
- Facebook faces the same structural inversion. The malware targets cognitive biases instead of buffer overflows. 30,000+ human moderators = content moderation as virus scanning.

Content moderation may be Sisyphean: society is online, so all society's problems are expressed and amplified online. A certain level of bad behavior may be irreducible — like cities, which have always had crime.

**But something came after trustworthy computing**: the shift to cloud + smartphones made whole classes of attack physically impossible (sandboxed apps; no point hacking a Chromebook). The answer was changing the model, not better virus scanners.

The parallel for social: instead of more moderators, change the mechanics that enable abuse. Examples: Instagram has no links; Clubhouse had no replies, quotes, or screenshots; email newsletters lack virality. Anonymous messaging apps showed that bullying was an inherent effect of their basic concept — they all shut down.[^3]

## The Newsfeed Overload Problem

Facebook's average user is eligible to see 1,500+ items/day. This stems from Dunbar's number (~200–300 genuine contacts) combined with "Zuckerberg's law" (people share more over time). The asymmetric feed normalizes high-frequency posting.[^4]

The **tragedy of the commons**: everyone is "supposed" to post, but by posting they overload everyone else's feeds.

The algorithmic feed is therefore logical — but unlike Google Search (explicit intent), a feed has no signal for what friends *need* you to see. A sample-based feed cannot carry important information reliably.[^4]

Responses to overload:
- **1:1 chat** (WhatsApp, iMessage, DMs): social dynamics work against overload; oversharing can be muted
- **Stories** (Snap's invention): bundle many shares into one unit, reducing load; structure goes into the content rather than the display

But Stories + group chats reproduce the overload problem at a different level — 10 WhatsApp groups × 50 people reasserts newsfeed logic.[^4]

## The Business Verb Framework

New productivity tools start by replicating old workflows, but over time workflows reshape to fit the tools (McLuhan).[^5]

The real question is not "what software to use" but what the underlying business *verb* is: analyze, delegate, report, confer, decide, track. Office's power users need complex features because making complex documents is their actual job. Everyone else uses Office because it's there, not because document creation is their job.

The way those others switch tools is not to a simpler Office clone, but to something that addresses the underlying need differently. "PowerPoint gets killed by things that aren't presentations at all." A SaaS dashboard with real-time data + Slack integration kills the Excel-to-PowerPoint-to-email workflow.[^5]

Hardware assumptions follow: if your task is flagging a few key changes on a dashboard, you may not need a keyboard, mouse, or windowed OS.[^5]

The verb framework connects directly to how software businesses are built today: the [Bootstrapped SaaS Playbook](/ai-business/bootstrapped-saas-playbook.md) makes the same point from the builder's side — a SaaS that merely transforms input→output has no moat once agents can do it natively, so the durable products are the ones serving an underlying *verb* rather than replicating a workflow. See also [AI Business Models](/ai-business/ai-business-models.md) for how these dynamics reshape one-person-business economics.

---

[^1]: [Would breaking up 'big tech' work?](raw/web/web-would-breaking-up-big-tech-work-what-would-benedict-evans-e5895f6d.md) — Benedict Evans, 2020
[^2]: [Why Amazon Has No Profits](raw/web/web-why-amazon-has-no-profits-benedict-evans-11c88595.md) — Benedict Evans, 2014/2021
[^3]: [Is content moderation a dead end?](raw/web/web-is-content-moderation-a-dead-end-benedict-evans-e5275a95.md) — Benedict Evans, 2021
[^4]: [The death of the newsfeed](raw/web/web-the-death-of-the-newsfeed-benedict-evans-b0652643.md) — Benedict Evans, 2018
[^5]: [Office, messaging and verbs](raw/web/web-office-messaging-and-verbs-benedict-evans-0fcadd5c.md) — Benedict Evans, 2015
