---
type: concept
domain: productivity
status: draft
sources:
  - path: raw/_inbox/email-2026-05-25-reclaim-6-hours-of-your-week-in-10-mins.md
    channel: inbox
    ingested_at: 2026-06-12
  - path: raw/_inbox/email-2026-05-03-you-re-just-a-text-file.md
    channel: inbox
    ingested_at: 2026-06-12
  - path: raw/_inbox/email-2026-06-08-loop-engineering.md
    channel: inbox
    ingested_at: 2026-06-12
aliases:
  - AI workflow
  - voice file
  - about-me file
  - loop engineering
  - reclaim hours
tags:
  - corpus/productivity
  - concept
created: 2026-06-12
updated: 2026-06-12
---

# AI-Augmented Knowledge Work

**TL;DR** — Set up reusable AI scaffolding once so each task costs seconds, not a cold re-explanation. Three escalating moves: (1) **standing instructions and projects** so the model already knows who you are; (2) **a compressed "about-me" file** that captures your voice and taste for any model; (3) **loop engineering** — designing systems that prompt agents instead of you prompting them. Across all three, *judgment and verification stay human* [^src1][^src2][^src3].

## 1. Standing context (the weekly setup ritual)

The anti-pattern: opening a blank chat every morning and re-explaining yourself — "like onboarding a new employee daily and firing them at 5pm" [^src1]. Spend ~15 minutes once; every later check-in takes 30 seconds [^src1].

- **Profile preferences**: tell the model exactly how to behave (skip preamble, lead with the answer, give a real recommendation not a neutral list, push back on bad ideas) [^src1].
- **Projects as memory**: a workspace where instructions and files ride into every chat; train 2–3 on your real samples [^src1].
- **Make it interrogate you first**: have the model attack then steel-man your plan before giving an opinion — "two minutes answering > twenty minutes correcting" [^src1].
- **Prompting mechanics** (attributed to Anthropic's guidance): say what *to* do not what to avoid; explain the *why*; 3–5 examples is the sweet spot for steering tone; **query-last ordering** (long doc on top, question at the bottom) can improve answers up to 30% on big inputs [^src1]. See [[ai-engineering/prompt-engineering|Prompt Engineering]] if present.

## 2. The about-me / voice file

"Give me 2 hours. One file. And any AI becomes you" [^src2]. The claim: your voice and taste are patterns, and patterns fit in a portable text file usable across Claude, ChatGPT, Gemini, etc. [^src2].

- **Two-step extraction**: a "Taste Interviewer" prompt runs ~100 questions across beliefs, writing mechanics, aesthetic crimes, voice, structure, hard nos, red flags — then a "Voice Compiler" prompt compresses the 20k-word dump to a 2–4k-token, XML-structured file (hard ceiling 5k) [^src2].
- **Compression test**: keep a line only if removing it would change how the AI writes, edits, judges, refuses, or decides — "maximum behavioral fidelity per token" [^src2].
- **Why compress**: the raw dump "eats too much of your context window" and re-costs tokens every turn [^src2].
- **Payoff**: you become *portable* (hand the file to a teammate or ghostwriter) and *consistent* — "a resource instead of a bottleneck." Edit the file often, because taste changes [^src2].
- **Caveat surfaced by the source**: consistency makes you predictable; the file is a tool to free time for thinking and choosing the right task, not just to go faster [^src2].

## 3. Loop engineering

"You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents" (Steinberger); "My job is to write loops" (Boris Cherny, Claude Code lead) [^src3]. A loop is a recursive goal: define a purpose, the AI iterates until complete [^src3].

- **Five building blocks plus memory**, present in both Claude Code and Codex [^src3]:
  1. **Automations** — scheduled discovery/triage (the "heartbeat"); Claude Code via `/loop`, cron, hooks, or GitHub Actions.
  2. **Worktrees** — isolated checkouts so parallel agents don't collide.
  3. **Skills** — project knowledge written once (a `SKILL.md`) so the loop stops re-deriving intent every cycle.
  4. **Plugins / connectors** (MCP) — let the loop act in real tools (issue tracker, DB, Slack).
  5. **Sub-agents** — separate the maker from the checker; the model that wrote code grades its own homework too kindly. (`/goal` runs until a verifiable condition holds, with a fresh model judging "done.")
  - **Memory** — a markdown file or board outside the conversation: "The agent forgets, the repo doesn't" [^src3].
- **What the loop does NOT remove** [^src3]: verification is still yours ("done" is a claim, not a proof); **comprehension debt** grows faster as the loop ships code you didn't write; and the comfortable posture — "cognitive surrender" — is the dangerous one. "Build the loop. Stay the engineer."

> Two people can build the same loop and get opposite results — one to move faster on work they understand, the other to avoid understanding it. "The loop doesn't know the difference. You do" [^src3].

This is the productivity face of agent orchestration; see [[ai-engineering/agentic-coding|Agentic Coding]] / loop and harness pages in the ai-engineering domain for the engineering depth, and [[productivity/shipping-and-scope|Shipping and Scope]] for why verification of outcomes is the durable skill.

---

[^src1]: [Reclaim 6 Hours of your Week in 10 mins](../../raw/email/email-2026-05-25-reclaim-6-hours-of-your-week-in-10-mins.md)
[^src2]: [You're just a text file.](../../raw/email/email-2026-05-03-you-re-just-a-text-file.md)
[^src3]: [Loop Engineering](../../raw/email/email-2026-06-08-loop-engineering.md)
