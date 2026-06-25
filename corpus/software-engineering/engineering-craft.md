---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/email-2025-11-06-how-to-become-a-resourceful-engineer.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/_inbox/email-2026-05-12-junior-developers-listen-up.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/youtube/youtube-vtyx7ex-0ba.md
    channel: youtube
    ingested_at: 2026-06-17
  - path: raw/pdf/pdf-the-software-engineers-guidebook-v1-08-pdf.md
    channel: pdf
    ingested_at: 2026-06-25
aliases:
  - engineering craft
  - resourceful engineer
  - resourcefulness
  - learning to code
  - staying current
  - innovation budget
  - mutual amplification
  - adversarial mentor
  - senior engineer
tags:
  - corpus/software-engineering
  - concept
created: 2026-06-12
updated: 2026-06-25
---

# Engineering Craft

**TL;DR**: The durable, non-tool skills of a software engineer — resourcefulness, curiosity, and persistence through difficulty. In software development "it's not so much important what you know at the moment" as that "you are able to get the essential information quickly, if needed" [^src1].

## Resourcefulness is a timeless skill

Being resourceful is "not about knowing everything off the top of your head, but about being able to organize yourself and get the information that you need" [^src1]. The best engineers respond to the unknown with: "I don't know yet, but this is how I'll find out!" — openly admitting the gap and providing a concrete plan to close it [^src1]. Admitting "I don't know" is framed as a sign of seniority, indicating experience, maturity, and humility [^src1].

Resourcefulness is positioned as durable against AI: no matter how software development changes, it "is a timeless skill that is always going to be highly worth" having, and it is a large part of being good at solving problems — one of the two areas (with human-related skills) where engineers must do well in a Gen-AI world [^src1].

### Curiosity is the foundation

> "Curiosity equals growth mindset." [^src1]

A curious engineer explores how systems really work beneath the surface, learns from failures rather than avoiding them, and continually explores new tools and perspectives — turning unknowns into learning opportunities instead of obstacles [^src1]. A useful interview probe: "What new have you learned in the past 6 months?" — and the non-verbal enthusiasm in the answer signals genuine curiosity [^src1].

## Persistence through difficulty

If learning to code "feels harder than you expected, that does not mean you are doing it wrong. It simply means you are doing something that is actually hard." [^src2] Getting stuck for hours on one bug or setup issue is normal — even experienced developers "go to sleep annoyed, wake up, try again, and only then figure it out" [^src2].

Over time the relationship to difficulty changes: a hard problem stops being proof you're not good enough and becomes simply something to work through. Surviving enough stuck-then-unstuck cycles builds a confidence "that is hard to get any other way" — the belief that every problem can be solved [^src2]. Because people learn at completely different paces, comparing yourself to others (the "learned in a few months, great job at 19" stories) is counterproductive; what matters is whether you keep going [^src2].

## What "senior" means under AI

A Google Cloud panel (Richard Seroter with engineers Aja Hammerly, Ciera Jaspan, Addy Osmani) reframes seniority for the AI era [^src3]. The durable senior qualities don't change: a senior engineer breaks a problem into smaller component parts and does **trade-off analysis** (e.g. secure vs. performant, depending on the business case) [^src3]. Addy Osmani's gloss: seniority used to mean writing code others couldn't; now it means understanding code others can't — built "on top of already strong engineering fundamentals" [^src3]. The new pressure is that everyone, "including our most junior people graduating from college," now needs to operate at senior level, so the open problem is upskilling juniors fast [^src3].

Aja Hammerly's hiring lens connects this to the craft skills above: a senior engineer solves challenging technical problems "in a way that works for the business," and someone you "wouldn't mind debugging an issue with in prod at 2:00 AM" — plus, newly, a strong curiosity about the tech and a built-in practice for **staying up to date** [^src3]. Mentorship is part of the bar: not "spawning 20 agents and leaving the rest of the team to figure things out" — the juniors of today are the seniors of tomorrow and need deliberate investment [^src3].

## Staying current without FOMO

The same panel offers concrete habits for keeping pace when tools change weekly [^src3]:

- **Innovation budget / one-tool-at-a-time.** Treat experimentation time as finite and be picky. Ciera Jaspan learns "only one new tool a month," goes deep, then decides whether to keep it in rotation — and fails fast on tools that clearly won't fit [^src3]. Aja gives herself an explicit innovation budget; Addy looks specifically for approaches that are *not* converging (the genuinely new idea), since most agentic tools' UX is converging and skill transfers across them [^src3].
- **It depends; match risk tolerance.** A practice worth adopting is one that maps to a problem you actually have; a one-person startup can take more bleeding-edge risk than an enterprise team. X/social is a leading indicator, not a mandate — don't bring bleeding-edge ideas to work until others have stabilized them [^src3].
- **Tie learning to real work.** Build tools you actually use, ask peers "how'd you do that?", and cultivate relationships with smart people who surface signal — Aja has "a hard time getting motivated about a tool that doesn't solve a problem I currently have" [^src3].
- **Set aside dedicated time** ("work in progress" / "science fair" sessions, ~2 hours/week) because you cannot evaluate new techniques without hands-on experimentation [^src3].

## Learning loops: mutual amplification and the adversarial mentor

The panel's strongest craft contribution is treating the agent itself as a learning instrument, not just a code generator [^src3]:

- **Mutual amplification** (Addy Osmani) — over a day of use, *both* you and your agent should get better; capture each day's new insights into a reusable learnings/markdown file so "the mistakes I made yesterday are not the same ones I'm going to make tomorrow" [^src3]. Ciera does the same: at every step she has the agent update its instructions file, and each time it errs she asks it to diagnose why and record it — slower at first, faster overall [^src3].
- **Adversarial mentor** (Aja Hammerly) — end coding/writing sessions by asking the AI what was missed, what's unclear, what the objections will be; explicitly instruct it "don't be nice." Reframing quality over velocity this way "massively improved" her output, even though being told you missed things "does not feel good the first couple times" [^src3].

> "I treat all of those as an adversarial mentor." [^src3]

This is the craft-side complement to the deterministic guardrails and write→review shift in [[software-engineering/ai-assisted-development|AI-Assisted Development]]; the named failure mode that makes these habits necessary — letting the agent think for you — is [[software-engineering/cognitive-debt|Cognitive Debt and Cognitive Surrender]].

## Career leveling and ownership (Orosz)

The Software Engineer's Guidebook by Gergely Orosz (Pragmatic Engineer) frames career growth as the engineer's responsibility to own, not the manager's job to deliver [^src4]. Key observations: at Big Tech (Google L5, Meta E5), senior expectations are noticeably higher than at lower-tier companies — "it's not always those who work hardest or deliver the highest quality work who are awarded the biggest promotions" [^src4]. The book's structure mirrors the maturity ladder: competent developer → well-rounded senior → pragmatic tech lead → staff/principal. See [[software-engineering/sources/software-engineers-guidebook|The Software Engineer's Guidebook]] for the full source summary.

## See also

- [[software-engineering/ai-assisted-development|AI-Assisted Development]] — why fundamentals and human judgment matter more, not less, under AI
- [[software-engineering/cognitive-debt|Cognitive Debt and Cognitive Surrender]] — the erosion-of-understanding failure mode these learning loops guard against
- [[software-engineering/sources/software-engineers-guidebook|The Software Engineer's Guidebook]] — Orosz's full career arc reference
- [[software-engineering/README|Software Engineering hub]]

---

[^src1]: [How to Become a Resourceful Engineer](../../raw/email/email-2025-11-06-how-to-become-a-resourceful-engineer.md)
[^src2]: [Junior developers, listen up...](../../raw/email/email-2026-05-12-junior-developers-listen-up.md)
[^src3]: [What Modern Software Engineering Means (Google Cloud podcast — Seroter, Hammerly, Jaspan, Osmani)](../../raw/youtube/youtube-vtyx7ex-0ba.md)
[^src4]: [The Software Engineer's Guidebook v1.08 (Gergely Orosz)](../../raw/pdf/pdf-the-software-engineers-guidebook-v1-08-pdf.md)
