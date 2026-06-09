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
aliases:
  - context window management
  - context management
  - context compaction
  - context compression
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-21
updated: 2026-06-09
---

# Context Window Management

**TL;DR**: The operational discipline of controlling what occupies the LLM's context window — deciding what to keep, compress, or drop — so the agent can operate effectively across long tasks without losing critical state [^src1].

Distinct from [[ai-engineering/context-engineering|Context Engineering]] (which governs *how* context is assembled at inference time). Context window management governs *what happens* when context fills up during a long-running task.

## The core problem

Context windows fill faster than expected in long-running agentic tasks. Every file read, every response, every revision consumes tokens. When the window fills:
- **Auto-compact** runs and compresses history
- Important details are lost in the compression
- The agent must re-read files to recover lost state — effectively paying the context cost twice [^src1]

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

This ensures the compression preserves the most critical context rather than applying uniform summarization.

### 2. Context resets

`/clear` performs a full context reset — fresh start with zero history. Use when a prior task is completely done and its context has no relevance to the next task [^src1].

### 3. Sub-agents (most powerful strategy)

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

### 4. Concise instructions

Counterintuitive: verbose instructions *hurt* performance. Extra tokens add to context and increase confusion. Treat the agent like a senior developer — provide clear specs upfront, let the agent ask when uncertain rather than pre-answering every possible edge case [^src1].

### 5. Tool selection

Not every iteration needs the same tool. Rapid back-and-forth revisions consume context fast — route those to lighter editors; reserve the main agent for building from specs [^src1].

### 6. Progressive disclosure via skills

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
