---
type: source
domain: software-engineering
status: draft
sources:
  - path: raw/web/web-14-more-lessons-from-14-years-at-google.md
    channel: web
    ingested_at: 2026-07-18
aliases: []
tags:
  - corpus/software-engineering
  - source
  - team-dynamics
  - trust
  - reliability
  - observability
created: 2026-07-18
updated: 2026-08-12
provisional: false
url: https://open.substack.com/pub/addyo/p/14-more-lessons-from-14-years-at
origin: obsidian-list
---

# 14 More lessons from 14 years at Google

**TL;DR:** 14 practitioner lessons from a Google engineering career focused on teams, decisions, and the systems around code — not individual craft. The through-line: "making it easier for normal people to do extraordinary things on a normal day."[^1]

**Source:** [open source](https://open.substack.com/pub/addyo/p/14-more-lessons-from-14-years-at)

---

## Problem selection & prioritization

**Lesson 1 — Pick the right problems.** Engineers who create disproportionate impact are ruthless about what deserves attention; they let wrong things stay undone.[^1] Saying yes to every bug and feature request fills calendars with others' priorities and turns one's own roadmap into a "graveyard of half-finished ideas."[^1] Protecting bandwidth from "nice to have" work is analogous to protecting production from outages.[^1]

---

## Meetings & decisions

**Lesson 2 — Know the decision before calling the meeting.** Meetings fail because they are "disguised journaling" — smart people talk around a problem without naming what they need.[^1] A useful frame: every meeting ask should map to one of four types — approve, choose, unblock, or inform.[^1] If you can't pick one, you're not ready to take anyone's time.

**Lesson 3 — Convert intentions into specific commitments.** "We should" is not a plan; "On Tuesday, I will" is.[^1] Vague intentions create anxiety; specific commitments create momentum.[^1] The next action must have a name and a date.

**Lesson 4 — Slow decisions are the disease; slow code is only a symptom.** When projects drag, the root causes are typically missing context, unclear ownership, or fear of accountability — not velocity.[^1] The fastest team the author worked with made decisions "in hours instead of weeks because the authority was clear, the context was shared, and being wrong wasn't a career risk."[^1]

---

## Reliability & observability

**Lesson 5 — Reliability is a product feature.** Reliability work is invisible until it fails, making it chronically under-resourced.[^1] Error budgets make the tradeoff explicit: a 99.9% SLO gives a 0.1% downtime budget to spend on innovation; burning through it forces a reliability focus.[^1] High-performing teams treat reliability as a first-class feature with its own roadmap, metrics, and advocates.[^1]

**Lesson 9 — Observability is part of the definition of done.** "A feature without telemetry is a liability in disguise."[^1] Shipping without logs, traces, dashboards, and alerts ships uncertainty — features can silently fail for a significant fraction of users with no detection.[^1] The best engineers treat observability as a completeness criterion, not ops work.

---

## Team interfaces & coordination

**Lesson 6 — You can't communicate your way out of a bad team interface.** Cross-team pain comes from undefined boundaries and unclear contracts, not insufficient meetings.[^1] Team interaction modes — collaboration, service (clear API/SLA), or facilitation — should be chosen deliberately; papering over a bad interface with more Slack channels burns collaborative people without fixing underlying dysfunction.[^1]

**Lesson 11 — Adding a team adds edges, not just nodes.** Coordination cost grows faster than headcount; new hires add communication overhead with every person they need to align with.[^1] The solution is reducing edges through clear ownership, autonomous teams with minimal dependencies, and interfaces that enable parallel work.[^1]

---

## Escalation & trust

**Lesson 7 — The best escalation comes with a proposal.** Identifying a problem is necessary but insufficient; presenting two options with tradeoffs and a recommendation is how you get unblocked and build trust.[^1] It gives decision-makers something specific to react to and earns increasing autonomy.

**Lesson 14 — Trust is a latency optimization.** In high-trust environments, decisions that take weeks in low-trust ones take hours.[^1] "Every time you deliver on a promise, every time you're honest about a mistake, every time you make someone else's life easier, you're depositing into an account that will pay dividends for years."[^1] Engineers with modest technical skills who are trusted can accomplish more than brilliant engineers nobody will take calls from.[^1]

---

## Systems design & culture

**Lesson 8 — Avoid hero culture; build systems that don't require heroes.** Recurring heroism is a failure mode, not a badge of honor.[^1] When the "hero" leaves, teams discover nobody else knows how things work. The goal is making the normal path the default — "design for the average Tuesday, not the exceptional crisis."[^1]

**Lesson 10 — Small PRs are kindness.** Small changes ship faster (no waiting for a reviewer to find an hour for a thousand-line diff), are easier to revert, and force incremental thinking where each piece gets feedback independently.[^1] Large PRs optimize for the author's convenience at the expense of reviewers' sanity.[^1]

**Lesson 12 — A migration is never just a migration.** Migrations routinely stretch from one quarter to years because the human work — convincing teams to prioritize your migration, supporting undocumented edge cases, maintaining two systems in parallel — is underestimated.[^1] Migrations that finish share three traits: an engaged sponsor past kickoff, a team that truly owns it (not a side quest), and a deprecation date people believe is real.[^1] "If you're not willing to fund the finish, don't start the migration."[^1]

---

## AI & taste

**Lesson 13 — AI makes drafts cheap; taste becomes expensive.** When AI can produce ten versions of anything in the time it used to take to produce one, the scarce resource becomes judgment: "what to build, what to delete, what to simplify, what not to ship."[^1] Engineers who thrive will be curators, not generators. "Production is cheap. Editing is expensive. Selection is everything."[^1]

---

## Related corpus pages

- [/software-engineering/README.md](/software-engineering/README.md)

---

[^1]: [14 More lessons from 14 years at Google](raw/web/web-14-more-lessons-from-14-years-at-google.md) — Addy Osmani, Substack (collected 2026-07-18)
