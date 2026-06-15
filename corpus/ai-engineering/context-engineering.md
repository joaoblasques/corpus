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
  - path: raw/youtube/How AI agents & Claude skills work (Clearly Explained).md
    channel: youtube
    ingested_at: 2026-06-09
  - path: raw/_inbox/email-2026-06-03-fwd-introduction-to-ktx-the-open-source-context-layer-for-da.md
    channel: inbox
    ingested_at: 2026-06-12
  - path: raw/web/how-ingestion-works.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/introduction-to-ktx-the-open-source-context-layer-for-data-a.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/github-kaelio-ktx-ktx-is-an-executable-context-layer-for-dat.md
    channel: web
    ingested_at: 2026-06-12
aliases:
  - context engineering
  - context window engineering
  - context layer
  - semantic layer
  - executable context
  - ktx
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-07
updated: 2026-06-12
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

## "Less is more" — what belongs in context

One practitioner framing pushes minimalism: rely on the model's strengths and spend context only on **what is unique to you** [^src4].

- **Code is context.** "Code itself has become context" — telling an agent which framework a codebase uses is redundant when it can read the code. A solid template or foundation acts as context the agent builds on [^src4].
- **Don't encode general knowledge.** "Don't tell the model use React. It knows to use React." Reserve instructions for what the model *can't* infer — your specific workflow, taste, currency, methodology [^src4].
- **Performance, not just cost.** A fuller window degrades output quality, so minimal context is also a quality lever — see [[ai-engineering/context-window-management|Context Window Management]] [^src4].

This complements the [[ai-engineering/agent-skills|Agent Skills]] argument: codify your unique workflow into skills (loaded on demand) rather than always-on instruction files.

## A dedicated context layer for data agents (ktx)

A productized form of context engineering: a standing **context layer** that an agent consults *before* it acts, rather than rediscovering context every task. ktx (by Kaelio, YC-backed) targets the gap where "the agent isn't dumb, it's blind" — it can see a warehouse schema but not "the agreed-upon definitions, which joins are safe, what 'active customer' means" [^src5]. The result is plausible-but-wrong output: "The query runs without errors. It simply uses the wrong joins, filters, or metric logic, and nothing tells you that until someone checks the numbers" [^src5].

The architecture pairs two committed, git-tracked layers [^src5][^src6]:

| Layer | Contents | For |
|---|---|---|
| `semantic-layer/*.yaml` | **Executable** definitions: tables, grain, joins, measures, dimensions, filters | A compiler turns these into dialect-correct SQL, so agents never rewrite canonical queries from scratch |
| `wiki/*.md` | **Searchable** business knowledge: metric definitions, caveats, reporting policies, historical decisions | Human-reviewable; gives agents the *why* behind the data |

Three principles generalize the context-engineering thesis [^src5][^src6]:
- **Context as code.** Definitions live as plain files committed to Git — "diffable, mergeable, and reviewable exactly like code" — not in a separate platform. Self-improving ingest reconciles new warehouse/BI evidence with already-approved definitions.
- **Approved definitions over inference.** Instead of generating SQL immediately, the agent searches the wiki for context, finds the approved metric in the semantic layer, compiles it, then executes — turning "a plausible answer" into "a correct one" for governed metrics like revenue or ARR [^src5].
- **Agent-native access.** Exposed via CLI *and* an [[ai-engineering/mcp|MCP]] server, so Claude Code, Cursor, Codex, and any MCP client (and frameworks like LangChain) consume the same context; all DB connections are read-only [^src5][^src6].

The caveat is the core context-engineering truth: "a context layer is only as strong as the context that exists" — ktx surfaces and organizes what a team already knows but cannot invent missing definitions [^src5]. This is the data-warehouse instance of the same principle that drives [[ai-engineering/rag|RAG]] and [[ai-engineering/agent-memory|Agent Memory]]: agents need the metadata and business context that give data meaning, not just access.

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
- [[ai-engineering/agent-skills|Agent Skills]] — codifying unique workflow into on-demand skills rather than always-on context
- [[ai-engineering/agent-memory|Agent Memory]] — the two-tier memory model that context engineering operates on
- [[ai-engineering/tool-calling-and-context-engineering|Tool Calling & Context Engineering]] — synthesis: structural relationship between tool results and context window management

---

[^src1]: [[03_Resources/Articles/Context Engineering|Context Engineering]]
[^src2]: [[03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro|AI Agents - Complete Course Beginner to Pro]]
[^src3]: [[03_Resources/Study Notes/Claude Code - Solving the Memory Problem with Context Engineering|Claude Code - Solving the Memory Problem with Context Engineering]]
[^src4]: [How AI agents & Claude skills work (Clearly Explained)](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md>) — Greg Isenberg × Ras Mic, YouTube
[^src5]: [Introduction to ktx: The Open-Source Context Layer for Data Agents](../../raw/email/email-2026-06-03-fwd-introduction-to-ktx-the-open-source-context-layer-for-da.md) — Pipeline to Insights (Substack)
[^src6]: [ktx — Make analytics context usable by agents (docs)](../../raw/web/how-ingestion-works.md) — docs.kaelio.com
