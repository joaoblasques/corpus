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
  - path: raw/email/email-2026-06-12-two-weeks-with-claude-fable-5.md
    channel: email
    ingested_at: 2026-06-20
  - path: raw/notes/notes-clippings-claude-security-is-now-in-public-beta.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/notes/notes-clippings-claude-for-the-legal-industry.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/web/web-introducing-sonnet-4-6.md
    channel: web
    ingested_at: 2026-06-21
  - path: raw/web/web-introducing-claude-opus-4-8.md
    channel: web
    ingested_at: 2026-06-21
  - path: raw/web/web-adaptive-thinking.md
    channel: web
    ingested_at: 2026-06-21
  - path: raw/web/web-introducing-claude-4.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/web/web-introducing-claude-opus-4-7.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/web/web-pricing.md
    channel: web
    ingested_at: 2026-06-23
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
updated: 2026-06-23
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

Anthropic's flagship agentic-coding model as of late May 2026, "designed to run longer engineering tasks with less supervision" [^src4]. Claimed **69.2% on SWE-Bench Pro** (a record for a public model at the time) and ~4x less likely than Opus 4.7 to let flaws in its own code pass unflagged [^src4][^src14]. The launch added **dynamic workflows** to Claude Code (Enterprise/Team/Max plans), able to spin up hundreds of parallel subagents to drive large migrations end to end [^src4][^src14]. In Claude Code, `opus` resolves to Opus 4.8 (requires v2.1.154+) and it is the default model on Max / Team Premium / Enterprise pay-as-you-go / Anthropic API account types [^src9]. One independent reviewer called it "a modest but tangible improvement" over its predecessor [^src6].

**Official benchmarks** [^src14]:
- **Super-Agent benchmark**: the only model completing every case end-to-end across multi-step autonomous tasks
- **CursorBench**: exceeds all prior Opus models at every effort level on real engineering tasks
- **84% Online-Mind2Web**: leading score on web agent navigation benchmark
- **4x less likely** to let code flaws pass unremarked during code review

**Additional changes at Opus 4.8 launch** [^src14]:
- **Fast mode 3x cheaper**: `/fast` mode in Claude Code (Opus Fast) is now 3x cheaper than at Opus 4.7 launch; price otherwise unchanged ($5/$25/M input/output)
- **Messages API**: now accepts `system` role entries inside the `messages` array (not only as the top-level system parameter), enabling more flexible multi-turn system-instruction patterns

## Sonnet 4.6

Anthropic's **"most capable Sonnet model yet"** as of June 2026 [^src12]. The default model on Claude Free and Pro plans, and on API accounts in Claude Code.

**Pricing and context**: $3 / $15 per million input/output tokens — unchanged from Sonnet 4.5 [^src12]. **1M-token context window** in beta (June 2026) [^src12].

**Performance**: In Claude Code internal testing, Sonnet 4.6 was preferred over Sonnet 4.5 ~70% of the time, and — notably — preferred over Opus 4.5 ~59% of the time, meaning users chose it over a more powerful but more expensive model [^src12].

**Key improvements** [^src12]:
- **Computer use / OSWorld**: Significant improvements in visual grounding accuracy and UI interaction; see [[ai-engineering/computer-use|Computer Use]] for the model-selection table.
- **Prompt injection robustness**: "A major improvement compared to Sonnet 4.5, performs similarly to Opus 4.6" in agentic robustness evaluations [^src12]. See [[ai-engineering/agent-security|Agent Security]].
- **Agentic steering**: Enhanced ability to follow nuanced, multi-step instructions in long-horizon tasks [^src12].

In the Claude Code alias table, `sonnet` resolves to Sonnet 4.6.

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

## Claude 4 (original family: Opus 4 and Sonnet 4)

The original Claude 4 launch introduced hybrid reasoning models with extended thinking + tool use in parallel, and a raised capability bar for coding agents [^src15].

**Claude Opus 4** — world's best coding model at launch, SWE-bench 72.5%, Terminal-bench 43.2%. Designed for "sustained performance on long-running tasks that require focused effort and thousands of steps" [^src15]. Cursor cited it as "state-of-the-art for coding and a leap forward in complex codebase understanding"; Rakuten validated it on an open-source refactor running independently for 7 hours [^src15].

**Claude Sonnet 4** — SWE-bench 72.7% (higher than Opus 4 on this benchmark), balancing performance and efficiency; "enhanced steerability for greater control over implementations" [^src15]. GitHub used it to power the new coding agent in GitHub Copilot [^src15].

**Key model improvements** at the Claude 4 launch [^src15]:
- **Extended thinking with tool use (beta)** — models alternate between reasoning and tool calls during the same thinking block.
- **Parallel tool execution** — call multiple tools simultaneously.
- **Memory capabilities** — significantly improved; when given local file access, Opus 4 creates and maintains "memory files" that persist key facts.
- **65% less shortcut behavior** — less likely to use loopholes to complete tasks vs. Sonnet 3.7.
- **Thinking summaries** — a smaller model condenses lengthy thought processes.

**Claude Code GA** — reached general availability at this launch with VS Code and JetBrains extensions and the Claude Code SDK [^src15].

**Pricing at launch**: Opus 4 at $15/$75 per million tokens (input/output); Sonnet 4 at $3/$15 [^src15]. (Subsequent 4.x releases reduced Opus pricing significantly — see Opus 4.8 section above.)

## Adaptive thinking

Adaptive thinking is Anthropic's preferred mode for controlling model reasoning [^src13]. Rather than specifying a fixed token budget, the model decides per-step when and how much to reason.

**Per-model support** [^src13]:

| Model | Adaptive thinking | Manual budget_tokens |
|---|---|---|
| Fable 5, Mythos 5 | Always on (cannot disable) | Not accepted |
| Opus 4.8, Opus 4.7 | **Only mode supported** | Rejected with 400 error |
| Opus 4.6, Sonnet 4.6 | Recommended | Deprecated |

API usage: `thinking: {"type": "adaptive"}`. Effort levels: `low`, `medium`, `high` (default), `xhigh`, `max` [^src13]. Higher effort = more thinking tokens, better performance on hard tasks, higher cost.

**Key implication for harness builders**: any code passing `budget_tokens` to Opus 4.7 or later will receive a 400 error and must be updated to use adaptive mode. See [[ai-engineering/claude-api|Claude API]] for the API detail.

## Loop engineering and Fable 5 (stepping back)

Two weeks with Fable 5 surfaced a pattern shift in how to work with the model [^src11]:

**"Fable makes it worth stepping back."** Fable 5's capability for extended, well-defined tasks means the leverage has shifted from "write a better prompt" to "design a better loop" — a more powerful operating mode where the engineer defines the structure (what to do, what done means, what to check) and the model executes [^src11].

**Well-defined tasks + agent self-check**: the model performs better when tasks have explicit, verifiable success criteria baked in — not just "write tests" but "write tests and verify all pass before returning." This supports a self-checking loop without manual verification of every step [^src11].

**"Verify the right work, not that the work is right."** The critical reframe: the human's job when using Fable is not to check whether each step was executed correctly (the model does that), but to verify that the *task itself* was worth doing — that the loop is producing the right outputs for the right problems. This connects to [[productivity/ai-augmented-knowledge-work|loop engineering]] and the verification-as-design discipline [^src11].

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
[^src11]: [Two Weeks with Claude Fable 5 — Loop Engineering (email)](../../raw/email/email-2026-06-12-two-weeks-with-claude-fable-5.md)
[^src12]: [Introducing Claude Sonnet 4.6](../../raw/web/web-introducing-sonnet-4-6.md) — Anthropic official blog
[^src13]: [Adaptive Thinking — Claude API docs](../../raw/web/web-adaptive-thinking.md) — Anthropic
[^src14]: [Introducing Claude Opus 4.8](../../raw/web/web-introducing-claude-opus-4-8.md) — Anthropic official blog
[^src15]: [Introducing Claude 4](../../raw/web/web-introducing-claude-4.md) — Anthropic
