---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/Claude Code - Solving the Memory Problem with Context Engineering.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/youtube/How AI agents & Claude skills work (Clearly Explained).md
    channel: youtube
    ingested_at: 2026-06-09
  - path: raw/notes/notes-clippings-using-claude-code-session-management-and-1m-context.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/web/web-using-claude-code-session-management-and-1m-context-claude.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/web/web-context-windows.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-9ToOfgZ4qqQ-i-stopped-hitting-claude-code-usage-limits-here-s-how.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-RzLV8sfFdMM-how-to-build-effective-claude-code-agents-in-2026.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-full-walkthrough-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/web/web-compaction.md
    channel: web
    ingested_at: 2026-06-25
aliases:
  - context window management
  - context management
  - context compaction
  - context compression
  - context rot
  - 1M context
  - rewind
  - compact_20260112
  - pause_after_compaction
  - server-side compaction
  - compaction API
  - smart zone
  - dumb zone
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-21
updated: 2026-06-25
---

# Context Window Management

**TL;DR**: The operational discipline of controlling what occupies the LLM's context window — deciding what to keep, compress, or drop — so the agent can operate effectively across long tasks without losing critical state [^src1].

Distinct from [Context Engineering](/ai-engineering/context-engineering.md) (which governs *how* context is assembled at inference time). Context window management governs *what happens* when context fills up during a long-running task.

## The core problem

Context windows fill faster than expected in long-running agentic tasks. Every file read, every response, every revision consumes tokens. When the window fills:
- **Auto-compact** runs and compresses history
- Important details are lost in the compression
- The agent must re-read files to recover lost state — effectively paying the context cost twice [^src1]

**Context rot** is the official framing: "model performance degrades as context grows because attention gets spread across more tokens, and older, irrelevant content starts to distract from the current task" [^src3]. The degradation is worst at compaction time — "the model is at its least intelligent point when compacting" — which is exactly when it needs to summarize accurately [^src3]. Claude Code's context window is one million tokens, which extends how long a session can run before compaction, but does not eliminate rot [^src3].

**Every turn is a branching point.** After any completed turn, the practitioner has five options [^src3]:

| Option | When |
|---|---|
| **Continue** | Context is still load-bearing; don't pay to rebuild it |
| **`/rewind` (Esc+Esc)** | Claude went down a wrong path; keep the useful file reads, drop the failed attempt, re-prompt with what you learned |
| **`/compact <hint>`** | Mid-task but session is bloated with stale debugging; steer with instructions |
| **`/clear`** | Starting a genuinely new task; you control exactly what carries forward |
| **Subagent** | Next step will generate lots of intermediate output you'll only need the conclusion from |

## The two-tier memory framing

| Tier | Mechanism | Characteristics |
|---|---|---|
| **Short-term** | Context window | What's happening right now; volatile; bounded |
| **Long-term** | CLAUDE.md / external documents | Always available; referred to at any time; survives compaction |

CLAUDE.md functions as the agent's long-term memory — instructions, constraints, and decisions written once and referenced across the entire session [^src1]. See [Agent Memory](/ai-engineering/agent-memory.md) for the full memory model.

## Strategies

### 1. Proactive compaction

Run `/compact` *before* the window fills, with explicit preservation instructions [^src1]:

```
/compact keep the database schema and the authentication logic
```

This ensures the compression preserves the most critical context rather than applying uniform summarization. **Bad autocompacts** occur when the model can't predict the direction of your work — e.g., after a debugging session, a stale reference to "that other warning" may be dropped because the session was focused elsewhere [^src3]. With 1M context, there is more runway to compact proactively with a steering description before the problem compounds [^src3].

### 2. Rewinding vs correcting

**`/rewind`** (double-Esc or `/rewind`) jumps back to any previous message and drops everything after that point from context [^src3]. This is often better than "that didn't work, try X instead" — which keeps the failed attempt in context and wastes tokens on correction: "rewind to just after the file reads, and re-prompt with what you learned" [^src3]. A useful tactic: ask Claude to "summarize from here" or use `/rewind` to produce a handoff message — a note from the current Claude to its earlier self about what it tried and why it failed [^src3].

### 3. Context resets

`/clear` performs a full context reset — fresh start with zero history. Use when a prior task is completely done and its context has no relevance to the next task [^src1]. The general rule: "when you start a new task, you should also start a new session" [^src3]. For adjacent tasks (e.g. writing docs for a feature just implemented), continuing the session avoids re-reading all the same files [^src3].

### 4. Sub-agents (most powerful strategy)

Delegating work to a sub-agent spins up a **fresh context window** isolated from the main agent's window. Work done by the sub-agent does not consume the main agent's tokens [^src1].

Observed token savings (from source): 3,500 / 7,000 / 9,000 tokens per sub-agent task. This is especially valuable when sub-agents perform tasks involving large [vector database](/ai-engineering/vector-database.md) retrievals — those results never enter the main agent's context window.

Common sub-agent specializations [^src1]:
| Sub-agent | Role |
|---|---|
| Context Fetcher | Reads files, extracts relevant info, returns summary |
| File Creator | Creates files/directories, applies templates |
| Git Workflow | Commits, PRs, branch management |
| Test Runner | Runs tests, reports failures back to main agent |

Set model per sub-agent — Haiku for simple/cheap tasks, Opus for complex reasoning [^src1].

**The Anthropic mental test for subagent use**: "Will I need this tool output again, or just the conclusion?" [^src3]. Codebase searches, verification passes, and doc-writing are canonical subagent use cases — the intermediate tool noise stays in the child's context; only the result comes back [^src3]. You can instruct Claude explicitly: "Spin up a subagent to verify the result of this work based on the following spec file" [^src3].

### 5. Concise instructions

Counterintuitive: verbose instructions *hurt* performance. Extra tokens add to context and increase confusion. Treat the agent like a senior developer — provide clear specs upfront, let the agent ask when uncertain rather than pre-answering every possible edge case [^src1].

### 6. Tool selection

Not every iteration needs the same tool. Rapid back-and-forth revisions consume context fast — route those to lighter editors; reserve the main agent for building from specs [^src1].

### 7. Progressive disclosure via skills

Putting reusable instructions in a skill rather than an always-on `AGENTS.md`/`CLAUDE.md` file keeps the window lean: only the skill's name + description occupy context until it's invoked, at which point the body loads on demand [^src2]. One measured example: 944 tokens as an always-on file vs 53 tokens as a skill's name + description [^src2]. See [Agent Skills](/ai-engineering/agent-skills.md).

## Why a lean window matters

Token efficiency is not only about cost. The source's framing: **"the model will get dumb as the context window closes"** — quality degrades as the window fills [^src2]. Practical target: keep usage roughly between the baseline already consumed by the system prompt (~10%) and ~70%; the closer to 90–100%, the worse the agent performs [^src2]. This is the performance argument (beyond cost) for compaction, sub-agents, and progressive disclosure.

## Context window sizes and capabilities (mid-2026)

Models with 1M-token context: Claude Opus 4.8, Mythos Preview, Opus 4.7, Opus 4.6, Sonnet 4.6, Fable 5, Mythos 5 [^src4]. Fable 5 and Mythos 5 default to 1M max and support up to 128k output tokens per request. Models with 200k context: Sonnet 4.5 and older.

**Context awareness** (Sonnet 4.6, 4.5, Haiku 4.5): these models explicitly receive information about their remaining token budget at conversation start and after each tool call — like a cooking-show clock that lets them allocate effort strategically rather than guessing when they'll run out [^src4].

**Extended thinking tokens**: previous thinking blocks are auto-stripped from the context window calculation between turns — they do not accumulate and count toward the limit [^src4]. The formula is: `context_window = (input_tokens − previous_thinking_tokens) + current_turn_tokens`.

**Server-side compaction (beta)**: automatic summarization and replacement of older context when a conversation approaches a configurable threshold. Available on Fable 5, Mythos 5, Opus 4.8, Mythos Preview, Opus 4.7, 4.6, and Sonnet 4.6 [^src4]. The recommended primary strategy for long-running agentic workloads.

**Compaction API parameters** (beta header `compact-2026-01-12`) [^src8]:

```python
context_management={"edits": [{"type": "compact_20260112",
    "trigger": {"type": "input_tokens", "value": 150000},  # min 50,000
    "pause_after_compaction": False,    # pause and return before continuing
    "instructions": None,               # custom summarization prompt (replaces default)
}]}
```

| Parameter | Default | Notes |
|---|---|---|
| `trigger` | 150K tokens | Minimum 50K. Check fires at each sampling iteration for server-tool workloads. |
| `pause_after_compaction` | `false` | When `true`, returns `stop_reason: "compaction"` with only the compaction block, letting you insert content before resumption. Use with compaction counter to enforce total-token budgets. |
| `instructions` | null | Completely replaces the default prompt (not additive). Include explicit "do not call any tools" instruction to prevent a known failure mode where the model calls a tool during summarization instead of writing a summary. |

**Billing via `usage.iterations[]`** [^src8]: the compaction step is a separate sampling iteration billed normally. `usage.iterations` contains `{"type":"compaction", "input_tokens": N, "output_tokens": M}` entries for each compaction. Top-level `input_tokens`/`output_tokens` are the sum of non-compaction iterations only. For accurate cost tracking, sum across all `iterations` entries.

**Prompt caching with compaction** [^src8]: add `cache_control` on the compaction block to cache the summary. Also add a cache breakpoint at end of system prompt — this keeps the system prompt cached separately so it doesn't need re-caching each time a new compaction summary is written.

**Token counting with existing compaction blocks** [^src8]: the `/v1/messages/count_tokens` endpoint applies existing compaction blocks (reports the compressed size) but does not trigger new compactions. Returns `count_response.context_management.original_input_tokens` for the pre-compaction size.

**Known failure mode** [^src8]: when tools are defined, the model occasionally calls a tool during the summarization step instead of writing a summary — result is `compaction.content: null`. Fix: set `instructions` to an explicit "respond with text only, do not call any tools" prompt.

## MCP server token cost (practitioner data)

Each MCP server connected to Claude Code adds a fixed overhead to every context window — because tool descriptions for all connected MCP tools load at session start. Measured practitioner data: **~18,000 tokens per MCP server** [^src5]. With 3+ MCP servers active, the baseline cost eats a significant fraction of available context before any work is done.

**CLI-over-MCP substitution** [^src5]: many MCP tools that fetch data or run operations can be replaced by a bash tool call to the equivalent CLI (e.g. `gh` for GitHub operations, `jq` for JSON processing). One practitioner reported **~40% context savings** by replacing MCP servers with CLI calls in bash — same functionality, 18K tokens saved per swapped-out MCP.

**Practical rules** derived from this [^src5]:
- Audit active MCP servers regularly; disable any not needed for the current task
- Prefer CLI (via bash) over MCP for operations where a good CLI exists and the schema overhead isn't justified
- Keep MCP servers for tasks requiring structured input/output or where the tool integration adds real value beyond CLI

## Progressive CLAUDE.md disclosure

Corollary to the skills pattern (§7): the root `CLAUDE.md` itself can be structured to load progressively. Pattern: keep the root `CLAUDE.md` under 300 lines with pointers to domain-specific files; those files only load when referenced by Claude [^src5]. The root file should contain only: critical constraints, build/test commands, and pointers — not every convention, preference, or background detail. Anything that isn't needed on every single turn is a candidate for an on-demand skill or sub-file.

**Auto-compact threshold override** [^src5]: Claude Code auto-compacts when the context reaches ~95% full by default. This threshold can be overridden (e.g. trigger at 75%) to compact earlier, while there's still headroom for the model to perform the compression well. Compacting at 95% means the model is already degraded when it tries to summarize. Compacting at 75% trades some context efficiency for much higher quality compaction.

**Bash output size** [^src5]: bash tool output accumulates fast. Long-running commands (test suites, build logs) that dump to stdout can consume 100K+ tokens of context if not managed. Pattern: redirect verbose output to files, then read only the relevant excerpt; or use a post-process step to summarize before injecting into context.

**Deny rules for scope control** [^src5]: `.claude/settings.json` supports `deny` patterns that prevent Claude from reading or acting on paths outside the intended scope. Using deny rules to exclude `node_modules/`, build output directories, and large binary asset directories reduces accidental context consumption when Claude explores the repo.

## The "dumb zone" at very long contexts

At approximately **250K tokens** context length, Opus 4 series models exhibit a quality degradation that practitioners call the "dumb zone" — reasoning quality noticeably drops even though the context limit is 1M tokens [^src6]. This is distinct from context rot (gradual degradation across turns) — it is a sharper threshold behavior observed with Opus specifically.

Implication: for tasks expected to consume 200K+ tokens, consider earlier context resets, tighter compaction, or subagent offloading to keep each individual context well below 250K [^src6].

## Smart Zone / Dumb Zone as a workflow model

A second framing of context quality degradation, applied to multi-phase workflows rather than single sessions [^src7]:

- **Smart Zone**: the early portion of a context window where output quality is high (~0–40% used, roughly 0–100K tokens for a 256K window)
- **Dumb Zone**: the later portion where model reasoning deteriorates — output becomes inconsistent, instructions get dropped, accumulated context contradicts earlier decisions

The key discipline: **keep every task small enough to complete before crossing into the Dumb Zone.** This drives the multi-phase plan pattern:
- **Single task**: fits entirely in Smart Zone — just run it
- **HITL multi-phase**: split the work into N phases, each in its own Smart Zone window; the human clears context and kicks off each phase
- **AFK multi-phase**: same as HITL but wrapped in an agent loop — phases run unattended
- **Ralph**: most autonomous — agent improvises its own plan phases in a continuous loop

**Clearing vs compacting** [^src7]:
- *Clearing*: reset context to empty between phases. Lossy (session history is gone) but every subsequent phase starts fresh and fully smart.
- *Compacting*: summarize existing context and continue. Retains semantic gist, but fidelity is lower — some details are compressed away. Better for tasks where prior decisions must carry forward.

The "Smart Zone tipping point" (~40% / ~100K tokens) is a practitioner heuristic, not a hard model boundary — it varies by model, task complexity, and prompt density [^src7].

## See also

- [Context Engineering](/ai-engineering/context-engineering.md) — governs how context is assembled at inference time
- [Agent Skills](/ai-engineering/agent-skills.md) — progressive disclosure as a context-saving technique
- [Agent Memory](/ai-engineering/agent-memory.md) — the two-tier memory model (short-term / long-term)
- [AI Agent](/ai-engineering/ai-agent.md) — the agentic loop that generates context growth
- [Agent Cost Management](/ai-engineering/agent-cost-management.md) — MCP token overhead and cost strategies

---

[^src1]: [Claude Code - Solving the Memory Problem with Context Engineering](/03_Resources/Study Notes/Claude Code - Solving the Memory Problem with Context Engineering.md)
[^src2]: [How AI agents & Claude skills work (Clearly Explained)](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md>) — Greg Isenberg × Ras Mic, YouTube
[^src3]: [Using Claude Code: session management and 1M context](../../raw/notes/notes-clippings-using-claude-code-session-management-and-1m-context.md) — Thariq Shihipar, Anthropic
[^src4]: [Context windows — Claude Platform docs](../../raw/web/web-context-windows.md) — Anthropic
[^src5]: [I Stopped Hitting Claude Code Usage Limits — Here's How](../../raw/youtube/youtube-9ToOfgZ4qqQ-i-stopped-hitting-claude-code-usage-limits-here-s-how.md) — Brad, YouTube
[^src6]: [How to Build Effective Claude Code Agents in 2026](../../raw/youtube/youtube-RzLV8sfFdMM-how-to-build-effective-claude-code-agents-in-2026.md) — Cole Medin, YouTube
[^src7]: [Full Walkthrough: Workflow for AI Coding — Matt Pocock](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-full-walkthrough-report.md) — Matt Pocock, AI Hero (conference talk notes report)
[^src8]: [Compaction — Claude Platform docs](../../raw/web/web-compaction.md) — Anthropic
