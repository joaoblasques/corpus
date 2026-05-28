---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: 03_Resources/Articles/Context Engineering.md
    channel: notes
    ingested_at: 2026-05-07
  - path: 03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro.md
    channel: notes
    ingested_at: 2026-05-07
  - path: 03_Resources/Study Notes/Claude Code - Solving the Memory Problem with Context Engineering.md
    channel: notes
    ingested_at: 2026-05-21
aliases:
  - context engineering
  - context window engineering
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-07
updated: 2026-05-21
---

# Context Engineering

**TL;DR**: The discipline of dynamically building and optimizing the information provided to an LLM at inference time [^src1]. "How you structure context is more important than the model itself." [^src2]

## Core idea

Context engineering treats the LLM's context window as a first-class engineering artifact — not just a prompt, but a structured, dynamic input that must be deliberately designed, assembled, and optimized for each inference call.

Distinct from static prompt engineering: context engineering implies runtime construction (retrieval, filtering, compression, injection) rather than a fixed template.

## The four context components (in agentic systems)

| Component | Role |
|---|---|
| System prompt | Core instructions and constraints |
| Retrieved context | Relevant docs/data from [[ai-engineering/rag\|RAG]] |
| Conversation history | Prior turns |
| Tool results | Function call outputs |

The context window is the agent's entire view of the world at inference time — all it knows is what fits in the window [^src2].

## In agentic systems

Context engineering is identified as the single most impactful skill in agent development [^src2] — above model choice or framework selection. Each component of the context window must be deliberately managed: what to include, what to compress, what to drop.

In practice, this means CLAUDE.md functions as long-term memory (always in scope, survives compaction), while the context window is short-term memory for the current task [^src3]. See [[ai-engineering/agent-memory|Agent Memory]] for the full memory model.

See [[ai-engineering/ai-agent|AI Agent]] for how context slots into the broader agent architecture. See [[ai-engineering/context-window-management|Context Window Management]] for operational strategies (compaction, resets, sub-agents) when context fills.

## Related concepts (referenced in source 1, not yet ingested)

- `context-engineering-ace-self-improving-llm-workflows` — agentic/self-improving applications of context engineering
- `writing-good-claude-md-context-engineering` — CLAUDE.md as a context engineering artifact
- `The C.R.A.F.T.E.D. Prompt Framework for Software Engineers` — prompt framework built on context engineering principles

## See also

- [[ai-engineering/README|AI Engineering hub]]
- [[ai-engineering/ai-agent|AI Agent]]
- [[ai-engineering/tool-calling|Tool Calling]]
- [[ai-engineering/rag|RAG]] — implements the "Retrieved context" component
- [[ai-engineering/context-window-management|Context Window Management]] — operational strategies when context fills (compaction, sub-agents, resets)
- [[ai-engineering/agent-memory|Agent Memory]] — the two-tier memory model that context engineering operates on
- [[ai-engineering/tool-calling-and-context-engineering|Tool Calling & Context Engineering]] — synthesis: structural relationship between tool results and context window management

---

[^src1]: [[03_Resources/Articles/Context Engineering|Context Engineering]]
[^src2]: [[03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro|AI Agents - Complete Course Beginner to Pro]]
[^src3]: [[03_Resources/Study Notes/Claude Code - Solving the Memory Problem with Context Engineering|Claude Code - Solving the Memory Problem with Context Engineering]]
