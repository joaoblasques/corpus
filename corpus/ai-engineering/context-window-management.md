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
aliases:
  - context window management
  - context management
  - context compaction
  - context compression
  - context rot
  - 1M context
  - rewind
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-21
updated: 2026-06-17
---

# Context Window Management

**TL;DR**: The operational discipline of controlling what occupies the LLM's context window — deciding what to keep, compress, or drop — so the agent can operate effectively across long tasks without losing critical state [^src1].

Distinct from [[ai-engineering/context-engineering|Context Engineering]] (which governs *how* context is assembled at inference time). Context window management governs *what happens* when context fills up during a long-running task.

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

CLAUDE.md functions as the agent's long-term memory — instructions, constraints, and decisions written once and referenced across the entire session [^src1]. See [[ai-engineering/agent-memory|Agent Memory]] for the full memory model.

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

Observed token savings (from source): 3,500 / 7,000 / 9,000 tokens per sub-agent task. This is especially valuable when sub-agents perform tasks involving large [[ai-engineering/vector-database|vector database]] retrievals — those results never enter the main agent's context window.

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

Putting reusable instructions in a skill rather than an always-on `AGENTS.md`/`CLAUDE.md` file keeps the window lean: only the skill's name + description occupy context until it's invoked, at which point the body loads on demand [^src2]. One measured example: 944 tokens as an always-on file vs 53 tokens as a skill's name + description [^src2]. See [[ai-engineering/agent-skills|Agent Skills]].

## Why a lean window matters

Token efficiency is not only about cost. The source's framing: **"the model will get dumb as the context window closes"** — quality degrades as the window fills [^src2]. Practical target: keep usage roughly between the baseline already consumed by the system prompt (~10%) and ~70%; the closer to 90–100%, the worse the agent performs [^src2]. This is the performance argument (beyond cost) for compaction, sub-agents, and progressive disclosure.

## See also

- [[ai-engineering/context-engineering|Context Engineering]] — governs how context is assembled at inference time
- [[ai-engineering/agent-skills|Agent Skills]] — progressive disclosure as a context-saving technique
- [[ai-engineering/agent-memory|Agent Memory]] — the two-tier memory model (short-term / long-term)
- [[ai-engineering/ai-agent|AI Agent]] — the agentic loop that generates context growth

---

[^src1]: [[03_Resources/Study Notes/Claude Code - Solving the Memory Problem with Context Engineering|Claude Code - Solving the Memory Problem with Context Engineering]]
[^src2]: [How AI agents & Claude skills work (Clearly Explained)](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md>) — Greg Isenberg × Ras Mic, YouTube
[^src3]: [Using Claude Code: session management and 1M context](../../raw/notes/notes-clippings-using-claude-code-session-management-and-1m-context.md) — Thariq Shihipar, Anthropic
