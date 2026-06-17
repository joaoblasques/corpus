---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/model-configuration-claude-code-docs.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-05-29-claude-opus-4-8-arrives.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/initial-impressions-of-claude-fable-5.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-06-10-claude-fable-5-is-here.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-06-10-claude-fable-spacex-ai1-apple-container.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-06-11-devs-love-and-hate-fable-5.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/notes/notes-clippings-best-practices-for-using-claude-opus-4-7-with-claude-code.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-claude-security-is-now-in-public-beta.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-claude-for-the-legal-industry.md
    channel: notes
    ingested_at: 2026-06-17
aliases:
  - Claude model lineup
  - Claude models
  - Opus 4.8
  - Claude Fable 5
  - Fable 5
  - Mythos 5
  - Sonnet 4.6
  - Haiku
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-12
updated: 2026-06-17
---

# Claude Model Lineup

**TL;DR.** The Claude model family from [[ai-engineering/anthropic|Anthropic]] spans Haiku (fast/cheap) → Sonnet → Opus → Fable/Mythos (frontier) [^src9]. In Claude Code, aliases point to recommended versions and update over time; Fable 5, Opus 4.6+, and Sonnet 4.6 support a 1M-token context window. This page tracks the lineup and per-model specifics; product specifics live on the [[ai-engineering/claude-code|Claude Code]] and [[ai-engineering/claude-cowork|Claude Cowork]] pages.

## Model lineup

In Claude Code, model **aliases** point to recommended versions and update over time [^src9]:

| Alias | Resolves to | Best for |
|---|---|---|
| `haiku` | latest Haiku | fast, simple tasks [^src9] |
| `sonnet` | Sonnet 4.6 | daily coding [^src9] |
| `opus` | Opus 4.8 | complex reasoning [^src9] |
| `fable` | Claude Fable 5 | hardest, longest-running tasks [^src9] |
| `best` | Fable 5 where available, else latest Opus | — [^src9] |

All of Fable 5, Opus 4.6+, and Sonnet 4.6 support a **1M-token context window**; append `[1m]` to an alias or pin it via env var [^src9]. Effort levels (`low`…`max`) control adaptive reasoning [^src9]. See [[ai-engineering/llm|LLM]] and [[ai-engineering/claude-code|Claude Code]] for configuration detail.

## Opus 4.8

Anthropic's flagship agentic-coding model as of late May 2026, "designed to run longer engineering tasks with less supervision" [^src4]. Claimed **69.2% on SWE-Bench Pro** (a record for a public model at the time) and ~4x less likely than Opus 4.7 to let flaws in its own code pass unflagged [^src4]. The launch added **dynamic workflows** to Claude Code, able to spin up hundreds of parallel subagents to drive large migrations end to end [^src4]. In Claude Code, `opus` resolves to Opus 4.8 (requires v2.1.154+) and it is the default model on Max / Team Premium / Enterprise pay-as-you-go / Anthropic API account types [^src9]. One independent reviewer called it "a modest but tangible improvement" over its predecessor [^src6].

## Fable 5 (and Mythos 5)

Released ~June 9 2026 and available across all Anthropic surfaces — claude.ai, Claude Code (web + CLI), and Cowork [^src6]. It "works more like a seasoned engineer: designed to investigate your codebase before it acts… and check its work before reporting it's done", excelling at long-running, asynchronous, multi-hour-to-multi-day sessions [^src5]. It is **not** the default model; select it with `/model fable`, ideally paired with `/goal` so it works until a completion condition is met [^src5].

Specs: **1M-token context window, 128K max output tokens, knowledge cutoff January 2026** [^src6]. Priced at **$10 / million input, $50 / million output** — twice the Opus 4.x price, with no premium for long context [^src5][^src6]. Independent testing described it as feeling "big": slow, expensive, knowing markedly more than Opus 4.8, "maybe the largest yet from any vendor" [^src6]. One reviewer used $110 of tokens in a day and had Fable write almost all of a library release (LLM 0.32a3), calling it "several days' worth of work" [^src6].

**Mythos 5** "shares Claude Fable 5's capabilities without the safety classifiers" [^src6]. Fable 5 is the same underlying model as Mythos 5 plus additional safeguards, particularly in cyber and bio domains — which is what allows the intelligence to be shared more broadly [^src5]. When a request touches a high-risk area, Fable 5 may **route it to Opus 4.8** automatically; the API has new mechanisms to signal this and an option to fall back automatically [^src6][^src7]. Fable 5 requires a limited data-retention period (used only to detect misuse, not for training) [^src5].

**Launch controversy.** Anthropic reportedly apologized for "secretly rerouting some requests to an older model", admitting it made the "wrong trade-off" — devs both loved and disliked the launch [^src8]. Around the same launch, Anthropic shipped a Swift package integrating Claude into Apple's Foundation Models framework as a server-side model (same API as the on-device model; requests go to the Claude API, never Apple's servers) [^src8].

## Opus 4.7

The model Anthropic positioned as the enterprise and legal-reasoning flagship before Opus 4.8 landed. Scored **90.9% on Harvey's BigLaw Bench** (highest of any Claude model at the time) — cited by Harvey as the model powering their legal intelligence platform [^src10]. Described as offering "stronger consistency across long documents, better handling of nuanced instructions, and improved reliability in high-stakes workflows" [^src10].

Claude Security (the vulnerability-scanning product) uses Opus 4.7 by default for all model-backed security reviews [^src10b].

**Key behavior differences from Opus 4.6** — documented for teams migrating harnesses [^src10c]:
- Updated tokenizer and a proclivity to think more at higher effort levels (especially on later turns in longer sessions) mean token usage can increase.
- Default effort level in Claude Code is **`xhigh`** (a new level between `high` and `max`).
- Adaptive thinking replaces fixed thinking budgets: the model decides per-step when to think more.
- Response length calibrated to task complexity; less verbose than 4.6 by default.
- Calls tools less often, reasons more between calls.
- Spawns fewer subagents by default — must be explicitly prompted for fan-out patterns.

See [[ai-engineering/claude-code|Claude Code]] (Opus 4.7 section) for the full usage guide.

## See also

- [[ai-engineering/anthropic|Anthropic]] — the lab behind these models (company, funding, learning resources)
- [[ai-engineering/llm|LLM]], [[ai-engineering/claude-api|Claude API]], [[ai-engineering/claude-code|Claude Code]]

[^src4]: [Claude Opus 4.8 arrives (The Code)](../../raw/email/email-2026-05-29-claude-opus-4-8-arrives.md)
[^src5]: [Claude Fable 5 is here (Claude Team)](../../raw/email/email-2026-06-10-claude-fable-5-is-here.md)
[^src6]: [Initial impressions of Claude Fable 5 (Simon Willison)](../../raw/web/initial-impressions-of-claude-fable-5.md)
[^src7]: [Claude Fable, SpaceX AI1, Apple container (TLDR)](../../raw/email/email-2026-06-10-claude-fable-spacex-ai1-apple-container.md)
[^src8]: [Devs love and hate Fable 5 (The Code)](../../raw/email/email-2026-06-11-devs-love-and-hate-fable-5.md)
[^src9]: [Model configuration — Claude Code docs](../../raw/web/model-configuration-claude-code-docs.md)
[^src10]: [Claude for the legal industry](../../raw/notes/notes-clippings-claude-for-the-legal-industry.md) — Anthropic (Harvey quote on Opus 4.7 BigLaw Bench score)
[^src10b]: [Claude Security is now in public beta](../../raw/notes/notes-clippings-claude-security-is-now-in-public-beta.md) — Anthropic
[^src10c]: [Best practices for using Claude Opus 4.7 with Claude Code](../../raw/notes/notes-clippings-best-practices-for-using-claude-opus-4-7-with-claude-code.md) — Anthropic
