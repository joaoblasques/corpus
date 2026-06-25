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
  - path: raw/_inbox/web-enable-and-use-web-search-claude-help-center.md
    channel: web
    ingested_at: 2026-06-24
  - path: raw/web/web-claude-haiku.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/web/web-migration-guide.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/email/email-2026-06-19-testing-mythos-and-fable-moving-beyond-swe-bench-nvidia-s-op.md
    channel: email
    ingested_at: 2026-06-25
  - path: raw/web/web-claude-opus-4-6.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/web/web-context-windows.md
    channel: web
    ingested_at: 2026-06-25
aliases:
  - Claude model lineup
  - Claude models
  - Opus 4.8
  - Claude Fable 5
  - Fable 5
  - Mythos 5
  - Sonnet 4.6
  - Opus 4.6
  - Haiku
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-12
updated: 2026-06-25
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

**"Verify the right work, not that the work is right."** The critical reframe: the human's job when using Fable is not to check whether each step was executed correctly (the model does that), but to verify that the *task itself* was worth doing — that the loop is producing the right outputs for the right problems. This connects to [[productivity/ai-augmented-knowledge-work|loop engineering]] and the verification-as-design discipline [^src11], and is the human-altitude case of [[ai-engineering/generator-evaluator-separation|generator–evaluator separation]] — once the model self-checks each step, the human evaluator relocates to the task level [^src11].

## Opus 4.6

Claude Opus 4.6 is Anthropic's strongest model as of late June 2026, positioned for high-stakes agentic work, long-context retrieval, and expert-domain reasoning [^src19].

**Highlights**:
- **Highest Terminal-Bench 2.0** score among all frontier models (agentic coding evaluation) [^src20]
- **Humanity's Last Exam**: leads all frontier models (53.0% with tools, domain-blocklist decontaminated) [^src20]
- **GDPval-AA**: outperforms GPT-5.2 by ~144 Elo points, Opus 4.5 by 190 points (finance, legal, knowledge-work) [^src20]
- **BrowseComp**: best score for locating hard-to-find information online [^src20]
- **MRCR v2 (8-needle 1M)**: 76% vs Sonnet 4.5's 18.5% — "a qualitative shift in how much context a model can actually use while maintaining peak performance" [^src20]
- **Context rot**: markedly better than predecessors on long-context degradation [^src20]
- **1M token context (beta)**: first Opus-class model with 1M context; premium pricing for >200k tokens ($10/$37.50 per M input/output) [^src20]
- **128k output tokens** — complete large-output tasks in a single pass [^src20]

**Agentic capabilities** [^src20]:
- "Breaks complex tasks into independent subtasks, runs tools and subagents in parallel, and identifies blockers with real precision"
- In a 40-case blind cybersecurity ranking vs Claude 4.5 models (up to 9 subagents, 100+ tool calls each), Opus 4.6 won 38/40 [^src20]
- Autonomously closed 13 issues and assigned 12 to team members in one day, managing a ~50-person org across 6 repositories [^src20]

**API / Platform additions at Opus 4.6 launch** [^src20]:
- **Adaptive thinking** — model dynamically allocates thinking when useful (default effort: `high`); four effort levels: `low`, `medium`, `high`, `max`
- **Context compaction (beta)** — server-side auto-summarization at a configurable threshold; see [[ai-engineering/context-window-management|Context Window Management]]
- **Agent teams in Claude Code (research preview)** — multiple subagents working in parallel on independent, read-heavy tasks; navigate with Shift+Up/Down or tmux
- **Claude in PowerPoint (research preview)** — reads layouts, fonts, slide masters; available on Max/Team/Enterprise

**Pricing**: $5/$25 per million input/output tokens (unchanged from Opus 4.5). Available on claude.ai, API, all major cloud platforms; model ID `claude-opus-4-6` [^src20].

## Web search model support

Web search (and web fetch) is available on the following models as of mid-2026 [^src16]:

- Fable 5
- Opus 4.8
- Opus 4.7
- Sonnet 4.6
- Opus 4.6
- Haiku 4.5

Web search requires the feature to be enabled (user toggle in chat, or admin-enabled at the workspace level for Team/Enterprise). Image results from Bing are included when web search is active. See [[ai-engineering/claude-cowork|Claude Cowork]] for workspace-level controls.

## Claude Haiku 4.5

Haiku 4.5 is Anthropic's fast, cost-efficient model in the Claude 4 generation [^src17]:

| Property | Value |
|---|---|
| **SWE-bench Verified** | 73.3% |
| **Coding / computer-use / agentic tasks** | Matches Claude Sonnet 4 |
| **Speed** | 4–5× faster than Claude Sonnet 4.5 |
| **Input cost** | $1 / M tokens |
| **Output cost** | $5 / M tokens |
| **Prompt caching** | Up to 90% cost savings |
| **Batch API** | Up to 50% cost savings |
| **API model ID** | `claude-haiku-4-5` |

Available on: Claude API, Amazon Bedrock, Google Vertex AI, Microsoft Foundry, and GitHub Copilot [^src17].

The key positioning: "built for fast, efficient performance on tasks that require computer use, agentic behaviors, and complex reasoning" without the cost of Sonnet-class models [^src17]. At 73.3% SWE-bench, it outperforms earlier Sonnet versions on coding while costing $1/$5 vs Sonnet 4.5's $3/$15 per million tokens.

## Migration guide — breaking API changes by model

The official migration guide documents per-model breaking changes and behavioral diffs for code running on the Anthropic Messages API [^src18]:

**Fable 5** [^src18]:
- Adaptive thinking always-on; `thinking: {type: "disabled"}` returns 400.
- Safety classifiers fire during generation: `stop_reason: "refusal"` (HTTP 200, not error) + `stop_details.category` (`cyber`, `bio`, `reasoning_extraction`, or `null`). Input tokens not billed on pre-generation refusal; already-streamed output billed on mid-stream refusal.
- 30-day mandatory data retention; not available under ZDR (zero data retention). Contact account team or configure per-workspace.
- Prompt caching minimum: **512 tokens** (vs 1,024 on Opus 4.8; 1,024 on Bedrock).
- Prefill removed (same as Opus 4.8+). No manual `budget_tokens`. Opt-in `fallbacks` beta parameter for auto-retry on refusal.
- Tool versions: `text_editor_20250728`, `code_execution_20250825`.
- Pricing: $10 / $50 per million input/output tokens.

**Mythos 5** [^src18]:
- Adaptive thinking always-on (same as Fable 5).
- No prefill. Raw CoT never returned — `thinking.display: "summarized"` to get readable summaries.
- Same tokenizer as Mythos Preview (Claude Opus 4.7 tokenizer — ~1–1.35x more tokens than pre-4.7 models).

**Opus 4.8** [^src18]:
- 1M context window default (no beta header needed).
- Effort default: `high`. Set `xhigh` explicitly for coding/agentic work.
- Prompt caching minimum: **1,024 tokens**.
- Accepts `role: "system"` entries inside the `messages` array mid-conversation (Opus 4.7 and earlier reject this).
- Effort levels recalibrated vs 4.7: `medium` allows more thinking, `high` allows less, `xhigh` substantially more.

**Opus 4.7** [^src18]:
- Sampling parameters (`temperature`, `top_p`, `top_k`) removed — any non-default value returns 400.
- Manual `budget_tokens` removed — replaced by adaptive thinking + `effort`.
- New tokenizer: ~1–1.35x more tokens than pre-4.7 models.
- `thinking.display` defaults to `"omitted"` (must set `"summarized"` to restore visible reasoning).
- Fewer subagent spawns by default; more literal instruction following.

**Sonnet 4.6** [^src18]: $3 / $15 per million input/output tokens. Effort default: `high`. No prefill. Fine-grained tool streaming GA.

**Haiku 4.5** [^src18]: $1 / $5 per million tokens.

`output_config.format` replaces `output_format`. Use `/claude-api migrate` skill in Claude Code to auto-apply migration changes across a codebase.

## Fable 5 safety classifiers (detail)

Fable 5 runs safety classifiers that refuse certain high-capability requests [^src19]:

- **Cyber category**: requests touching offensive cyber capabilities.
- **Bio category**: requests touching biological weapon synthesis or enhancement.
- **Reasoning extraction**: attempts to extract or reproduce the model's raw chain-of-thought.
- **Null**: refusal maps to no named category (other policy reasons).

In Claude Code specifically, flagged prompts are **routed to Opus 4.8** automatically (recorded in a separate log, not the main session log) rather than returning a bare refusal [^src19]. API usage (direct Messages API) returns an outright refusal with the stop reason. Fable 5 enforces a 30-day data retention for misuse-detection purposes; no training use [^src19].

See also [[ai-engineering/anthropic|Anthropic]] for the export control and AI sovereignty context from the same source.

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
[^src16]: [Enable and use web search (Claude Help Center)](../../raw/_inbox/web-enable-and-use-web-search-claude-help-center.md) — Anthropic
[^src17]: [Claude Haiku — claude.ai product page](../../raw/web/web-claude-haiku.md) — Anthropic
[^src18]: [Migration guide — Claude API](../../raw/web/web-migration-guide.md) — Anthropic
[^src19]: [Testing Mythos and Fable — The Batch (DeepLearning.AI)](../../raw/email/email-2026-06-19-testing-mythos-and-fable-moving-beyond-swe-bench-nvidia-s-op.md) — DeepLearning.AI
[^src20]: [Introducing Claude Opus 4.6](../../raw/web/web-claude-opus-4-6.md) — Anthropic official blog
