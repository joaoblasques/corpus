---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/cowork.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/cowork-0dd4601a.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-04-10-cowork.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/the-claude-cowork-stack-marketing-against-the-grain.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-05-19-top-5-claude-cowork-tips-i-wish-i-knew-from-day-one.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-06-10-stop-using-your-own-claude-at-work.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/cowork-toolkit-the-essential-starter-kit-for-claude-cowork.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-04-30-day-1-welcome-to-the-cowork-toolkit-lets-dive-in.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-05-01-day-2-teach-cowork-how-you-actually-write.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-05-02-day-3-build-your-first-cowork-workstation.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-05-05-day-6-how-to-scale-your-cowork-to-run-your-entire-life.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/shared-cowork-toolkit-templates-d1.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/shared-cowork-toolkit-templates-d2.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/shared-cowork-toolkit-templates-d6.md
    channel: web
    ingested_at: 2026-06-12
aliases:
  - Claude Cowork
  - Cowork
  - claude-cowork
  - Cowork OS
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-12
updated: 2026-06-12
---

# Claude Cowork

**TL;DR.** Claude Cowork is the desktop-app product for non-developers — described as "the non-developer version of Claude Code" [^src8]. New Anthropic capabilities land in [[ai-engineering/claude-code|Claude Code]] first and the best ones trickle down to Cowork over time [^src8]. It works against a **workspace folder** on your computer: each session starts by reading instruction and memory files (`CLAUDE.md`, `MEMORY.md`) plus an ABOUT-ME profile, so you never re-explain who you are [^src1][^src8]. The discipline that makes it powerful is **context economy** — keeping the always-loaded files lean so the context window is spent on the task, not the profile [^src1].

Access: download the desktop app at claude.com/download, open the **Cowork** tab (between Chat and Code), and select a folder as your workspace [^src1]. Three modes of Claude: **Chat** (ask/answer, won't read local files or take unrequested actions), **Code** (developers), **Cowork** (non-developers, file-aware, takes actions) [^src8].

## Workspace folder setup

Two competing folder conventions appear in the sources; both rest on the same principle (a lean, always-read profile + on-demand reference files).

**Ruben Hassid's ABOUT-ME pattern** [^src1]. A `Claude Cowork` folder with three subfolders:
- **ABOUT ME/** — the only folder Cowork reads automatically. Three core files: `about-me` (who you are, how you think, how you want Claude to write), `anti-ai-writing-style` (the words/patterns you hate, as rules), `my-company` (goals, strategy, what you're saying no to) [^src1].
- **OUTPUTS/** — one subfolder per project; Cowork never reads it on its own, saving tokens [^src1].
- **TEMPLATES/** — Cowork saves the skeleton of work you liked ("keeps the structure, strips the content") to reuse later [^src1].

**Global Instructions** (Settings → Cowork) tell Cowork to read every ABOUT ME/ file before every task and never touch OUTPUTS/ or TEMPLATES/ unless pointed at a file [^src1]. The key constraint: if ABOUT ME files stay small (under ~6,000 tokens total) Cowork reads them completely every session; if too big, it "starts summarizing them loosely instead of reading them carefully" [^src1].

**Jeff Su's "Cowork OS" pattern** (used by the Toolkit below) [^src9]. A flat workspace folder with `CLAUDE.md` + `MEMORY.md` at the root and a `00_Resources/` folder for reference files [^src9][^src10]. Critical detail: the root file **must** be named exactly `CLAUDE.md` (case-sensitive) or Cowork won't recognize it [^src9].

## CLAUDE.md vs MEMORY.md — the core distinction

Both files load every session and both are plain-text markdown [^src9]:

- **CLAUDE.md is prescriptive — what to DO.** Rules and standing instructions: "always X", "never Y", "when I ask about Z, do it this way" [^src9].
- **MEMORY.md is descriptive — what to KNOW.** Accumulated facts: active projects, decisions, contacts, preferences [^src9].

The test for where an entry belongs: if it contains "always"/"never" it's a CLAUDE.md rule; if it states a fact that could change tomorrow it goes in MEMORY.md [^src11]. Misfiling degrades output quality [^src11]. Over time this accumulation is "the difference between a tool that does what you say and an assistant that knows what you mean" — after 90 sessions you have 90 contextual facts applied automatically [^src11].

## The voice problem and reference files

To stop Cowork sounding like AI, create a `voice-principles.md` in `00_Resources/` capturing tone, sentence style, and words to avoid, and add a CLAUDE.md pointer: "Before producing any written content, read voice-principles.md" [^src12]. A **voice-extraction prompt** has Cowork analyze your last 30 sent emails (or pasted samples) and rewrite the file in your patterns [^src12].

This is the **reference-file pattern**: instead of putting everything in CLAUDE.md, create a separate file and point to it. Three reasons — size (keep CLAUDE.md under ~300 lines), modularity (different contexts load different files), maintainability (edit once, propagates) [^src12]. Rule of thumb: a long CLAUDE.md is a signal to pull content into a reference file and replace it with a one-line pointer [^src12].

## Token / credit economy

Cowork bills tokens, not messages, and re-reads the full conversation history on every turn — so "Message 30 costs 31x more tokens than message 1" [^src1]. Hacks [^src1]:
1. **Restart the conversation from an earlier message** rather than sending a follow-up.
2. **Start a fresh session every ~20 messages**; one developer found 98.5% of tokens went to re-reading history, only 1.5% to output [^src1].
3. **Batch tasks into one message** (one context reload, not three).
4. **Use Sonnet/Haiku for quick tasks**, reserve Opus + extended thinking for deep work [^src1].
5. **Keep ABOUT ME files small** [^src1].

Trimming the root CLAUDE.md from 600+ lines to ~250 dropped one user's token usage by roughly 25% [^src11]. See [[ai-engineering/context-window-management|Context Window Management]].

## Using personal Claude safely at work

Workers at 90%+ of companies use personal chatbots for work, often without telling IT; 57% have typed sensitive info at least once [^src6]. On personal plans, Anthropic may train on chats by default (consumer-terms change of August 2025), retained up to 5 years unless turned off — the opt-out applies going forward only [^src6]. Guidance: turn off training; never paste source code, customer/patient data, unreleased plans, financials, or credentials; anonymize before pasting; use a temporary chat for work tasks; and treat **connectors** as the most dangerous setting — a connected AI can be hijacked by content it reads (the "lethal trifecta": private-data access + untrusted content + outbound channel) [^src6]. Never connect work accounts to a personal AI; the clean answer for regulated data is a company-paid tool [^src6].

---

# Cowork Toolkit

A free email-course starter kit (Jeff Su / Cowork Academy) that builds a self-improving workspace [^src7]. It ships two pre-filled starter files (`CLAUDE.md`, `MEMORY.md`), a voice profile + extraction prompt, populate prompts for two workstations (Email HQ, Personal Finances), a first-project prompt, and a session-audit skill — tied together by routing logic and three-level inheritance [^src7]. (The shared Google-Drive template folders confirm the artifacts: `CLAUDE.md`/`MEMORY.md` [^src13], `voice-principles.md`/`voice-extraction-prompt.md` [^src14], `starter-session-audit.skill` [^src15].)

## Workstations

**Workstations** are domain folders inside the workspace, one per area of work; each has its own CLAUDE.md (domain rules) and MEMORY.md (domain context) [^src10]. Root rules cascade down automatically, so voice principles and preferences flow into every workstation without repetition [^src10]. Two types: **universal** (cut across everything — email, brand identity) and **dedicated** (own one area — personal finances, health) [^src10].

A **populate prompt** creates the workstation and fills it from your real data. Example (Email HQ): connect Gmail, scan the last 4 weeks of sent mail, extract editorial rules (greeting, sign-off, formality by recipient), build a contacts CRM of the top 10 recipients, and add a routing entry — showing everything before saving [^src10]. The Gmail connector reads but does not send; you always review and hit send [^src10].

## The three scaling mechanisms

A 3-month-old workspace beats a 3-day-old one through three mechanisms [^src11]:
1. **Accumulating memory** — each correction (a sign-off, a banned phrase) gets written to the right MEMORY.md and never needs repeating.
2. **Routing** — a routing table in the root CLAUDE.md (one sentence per row) loads only the workstation needed for the task, so adding workstations doesn't slow every session.
3. **Session audits** — saying "audit this session" has Cowork scan for uncaptured learnings and propose where to save each (which file, which section, exact wording), with your approval. "Two actions… are what make the workspace self-improving instead of static" [^src11].

Memory discipline: 1–2 sentences per entry; a 150-line ceiling on root MEMORY.md (fix by compression/archiving, never raising the ceiling); and an `ARCHIVE.md` that is *not* read every session, so it has no size cost — the "filing cabinet" to MEMORY.md's "whiteboard" [^src11].

## Skills vs workstations

If the process requires your judgment along the way, it's a **workstation**; if you already know exactly what the output should be and just need execution, it's a **skill** [^src11]. See [[ai-engineering/agent-skills|Agent Skills]].

## Other guides

`claude101.com` collects free Cowork-adjacent guides (Cowork setup, Cowork + Projects, slides, skills, sounding like you, avoiding usage limits) [^src8].

## See also

- [[ai-engineering/claude-code|Claude Code]] — the developer counterpart; capabilities land here first
- [[ai-engineering/anthropic|Anthropic]] — provider and model lineup
- [[ai-engineering/context-window-management|Context Window Management]], [[ai-engineering/agent-skills|Agent Skills]]

[^src1]: [Cowork (Ruben Hassid)](../../raw/web/cowork.md)
[^src2]: [Cowork 2.0 (Ruben Hassid, dup)](../../raw/web/cowork-0dd4601a.md)
[^src3]: [Cowork (email pointer)](../../raw/email/email-2026-04-10-cowork.md)
[^src4]: [The Claude Cowork Stack — marketing against the grain](../../raw/web/the-claude-cowork-stack-marketing-against-the-grain.md)
[^src5]: [Top 5 Claude Cowork Tips I Wish I Knew from Day One](../../raw/email/email-2026-05-19-top-5-claude-cowork-tips-i-wish-i-knew-from-day-one.md)
[^src6]: [Stop using your own Claude at work](../../raw/email/email-2026-06-10-stop-using-your-own-claude-at-work.md)
[^src7]: [Cowork Toolkit — the essential starter kit](../../raw/web/cowork-toolkit-the-essential-starter-kit-for-claude-cowork.md)
[^src8]: [Claude 101](../../raw/web/claude-101.md)
[^src9]: [Day 1: Welcome to the Cowork Toolkit](../../raw/email/email-2026-04-30-day-1-welcome-to-the-cowork-toolkit-lets-dive-in.md)
[^src10]: [Day 3: Build your first Cowork workstation](../../raw/email/email-2026-05-02-day-3-build-your-first-cowork-workstation.md)
[^src11]: [Day 6: How to scale your Cowork to run your entire life](../../raw/email/email-2026-05-05-day-6-how-to-scale-your-cowork-to-run-your-entire-life.md)
[^src12]: [Day 2: Teach Cowork how you actually write](../../raw/email/email-2026-05-01-day-2-teach-cowork-how-you-actually-write.md)
[^src13]: [Cowork Toolkit templates — Day 1](../../raw/web/shared-cowork-toolkit-templates-d1.md)
[^src14]: [Cowork Toolkit templates — Day 2](../../raw/web/shared-cowork-toolkit-templates-d2.md)
[^src15]: [Cowork Toolkit templates — Day 6](../../raw/web/shared-cowork-toolkit-templates-d6.md)
