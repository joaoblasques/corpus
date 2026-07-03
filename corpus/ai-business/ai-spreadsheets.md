---
type: concept
domain: ai-business
status: draft
sources:
  - path: raw/email/email-2026-05-24-stop-learning-excel.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/web/cowork.md
    channel: web
    ingested_at: 2026-06-15
aliases:
  - stop learning Excel
  - AI spreadsheets
  - Excel with AI
  - spreadsheets with AI
  - Claude Cowork for Excel
  - data skill shift
tags:
  - corpus/ai-business
  - concept
created: 2026-06-15
updated: 2026-06-15
---

# AI Spreadsheets & the Data-Skill Shift

**TL;DR** — A practitioner playbook arguing the marketable skill is shifting from *operating* a spreadsheet tool to *directing AI* to build and edit spreadsheets — "Stop learning Excel" [^src1]. The leverage isn't the tool; it's a repeatable **prompt structure** that forces the AI to expose its assumptions before executing, plus a folder/context setup so the AI already knows your business. Source is a creator newsletter (Ruben Hassid) with heavy promo framing, but the underlying direct-response principle — own the spec, make the AI do the grunt work — is consistent. Tooling specifics live in ai-engineering; the *career/monetization* read is captured here.

## The claim: direct the tool, don't master it

The author benchmarked "every single AI to make spreadsheets" and ranks them, concluding Claude Cowork is best to build from scratch and a ChatGPT Google Sheets extension is best to edit; Copilot, Grok, and bare Gemini underperformed [^src1]. The strategic takeaway for the job market: the differentiating skill becomes **writing a precise build spec and controlling the AI**, not memorizing Excel formulas — "I am the one controlling the AI, not the other way around" [^src1].

This is a concrete instance of the broader thesis in [AI and the Job Market](/ai-business/ai-and-the-job-market.md): raw tool operation commoditizes; the durable edge is *applying* AI to a real deliverable. And it overlaps with [Monetizing Code](/ai-business/monetizing-code.md) — board-ready models and consulting deliverables are exactly the "boring, valuable workflow" worth selling.

## The reusable prompt structure

The portable asset is a **spreadsheet build template** with four labeled sections [^src1]:

1. **Data** — file path, folder, or pasted data (uploading is best).
2. **Purpose** — one sentence on who uses it and what decision it supports.
3. **Sheets needed** — per sheet: columns, what a row represents, calculations/formulas.
4. **Formatting** — currency/date formats, conditional highlighting, frozen header, totals.

The load-bearing line, appended to every build [^src1]:

> "Before building, list your top 10 assumptions so I can sanity-check them, then execute."

This **assumptions-first gate** is the transferable technique — it keeps a human in control of judgment before the AI commits work, the same human-in-the-loop discipline seen in [Monetizing Code](/ai-business/monetizing-code.md). A worked example (a 12-month revenue forecast for a consulting firm) keeps every assumption "as a labeled, editable input on the Assumptions sheet — never hardcoded inside a downstream formula — so each one can be challenged and the model updates instantly" [^src1] — i.e. good modeling hygiene, AI or not.

## Context setup beats per-task prompting

The deeper move (from the linked Cowork guide) is **standing context** so you never re-explain yourself: a `Claude Cowork` folder with an `ABOUT ME/` subfolder holding three lean files Claude reads before every task — `about-me`, `anti-ai-writing-style`, `my-company` — plus `OUTPUTS/` and `TEMPLATES/`, wired together by Global Instructions [^src2]. Keep the ABOUT ME files small (the author trimmed his about-me from 22,000 to under 2,000 tokens) because a bloated profile is "thousands of tokens burned before any real work starts," and an oversized file gets *summarized loosely* instead of read carefully [^src2].

Token-economy habits that lower the cost of this workflow [^src2]: restart/branch conversations instead of stacking follow-ups (every message re-reads the whole history); start fresh sessions every ~20 messages; batch tasks into one prompt; use Sonnet/Haiku for light tasks and reserve Opus + extended thinking for deep work.

> Cross-domain: the Cowork product, its folder/Global-Instructions mechanics, context-window economy, and the about-me/voice file are owned by ai-engineering — see [Claude Cowork](/ai-engineering/claude-cowork.md) — and, on the productivity side, [AI-Augmented Knowledge Work](/productivity/ai-augmented-knowledge-work.md). This page keeps only the spreadsheet/career angle.

## Gotchas / promo framing

- Single-author, self-reported benchmark; model rankings are opinion, not a controlled test, and name specific model versions ("Opus 4.7") that date quickly [^src1].
- Both sources are list-building newsletters funneling to a paid Substack, a Circle community, and a consulting firm (GPC); "Claude & Anthropic do not pay me" is stated repeatedly [^src1][^src2].
- The "best AI for X" verdicts are time-sensitive — treat the *method* (assumptions-first spec + standing context) as the durable lesson, not the leaderboard.

## Related

- [AI and the Job Market](/ai-business/ai-and-the-job-market.md) — the skill-shift / "apply AI to messy real work" thesis this instantiates.
- [Monetizing Code](/ai-business/monetizing-code.md) — turning a spreadsheet/automation deliverable into a paid offer.

[^src1]: [Stop learning Excel.](../../raw/email/email-2026-05-24-stop-learning-excel.md) (Ruben Hassid newsletter)
[^src2]: [Cowork (Claude Cowork for Excel, updated guide)](../../raw/web/cowork.md) (fetched via the source email)
