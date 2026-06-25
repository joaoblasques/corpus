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
  - path: raw/web/web-effective-context-engineering-for-ai-agents.md
    channel: web
    ingested_at: 2026-06-21
  - path: raw/youtube/-h9VVJIqtvA-context-engineering-in-29-minutes-complete-course.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-stop-learning-obs-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/github/github-incomestreamsurfer-context-engineering-intro.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/github/github-addyosmani-context-buddy.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/github/github-coleam00-context-engineering-intro.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - context engineering
  - context window engineering
  - context layer
  - semantic layer
  - executable context
  - ktx
  - PRP
  - product requirements prompt
  - INITIAL.md
  - generate-prp
  - execute-prp
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-07
updated: 2026-06-25

---

# Context Engineering

**TL;DR**: The discipline of dynamically building and optimizing the information provided to an LLM at inference time [^src1]. "How you structure context is more important than the model itself." [^src2]

## Core idea

Context engineering treats the LLM's context window as a first-class engineering artifact — not just a prompt, but a structured, dynamic input that must be deliberately designed, assembled, and optimized for each inference call.

Distinct from static prompt engineering: context engineering implies runtime construction (retrieval, filtering, compression, injection) rather than a fixed template.

**Anthropic's authoritative definition**: "the discipline of filling the context window with just the right information, in the right format, at the right time, for the LLM to optimally complete a task" [^src9]. Context itself is "the set of tokens included when sampling from an LLM."

### Context rot

Performance degrades as context grows: "as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases" [^src9]. The mechanism: transformers compute n² pairwise attention relationships across all tokens. As context grows, the same finite attention bandwidth is shared across more and more relationships — so any individual relationship gets less "attention budget." This is true even with extended-context models; capacity scales, but so does the cost of filling it.

**Practical consequence**: a full context window is not the same as a well-filled one. Irrelevant information actively degrades performance by consuming attention budget that would otherwise focus on what matters [^src9].

### System prompt altitude

System prompts sit in a "Goldilocks zone" between too rigid and too vague [^src9]:

- **Too rigid**: brittle to edge cases; the agent can't handle variation the system prompt didn't anticipate
- **Too vague**: agent behavior becomes variable and unpredictable; no stable baseline
- **The zone**: clear constraints + enough flex for the model to handle variation within bounds

"Bloated tool sets that cover too much functionality" are the most common production failure mode — they consume context budget, increase selection uncertainty, and degrade performance. Prefer fewer, well-described tools [^src9]. See [[ai-engineering/mcp|MCP]] for the "One Thing" principle.

### Four storage types

Context engineering spans four tiers of information storage [^src9]:

| Type | Scope | Examples |
|---|---|---|
| **In-context** | Current inference | Retrieved docs, tool results, conversation history |
| **External** | Persistent store | Vector DB, key-value store, files, databases |
| **In-weights** | Baked into model | Pre-training knowledge, fine-tuning |
| **In-cache** | Reused computation | Prompt cache (KV cache for prefix reuse) |

Context engineering primarily operates on the in-context tier, but retrieval (from external) and caching (reducing in-context cost) are adjacent disciplines.

### Just-in-time context strategies

**Structured note-taking (NOTES.md)**: agents that run long tasks write key decisions and intermediate results to a scratchpad file, then load only the relevant section at the next step — keeping the context lean while preserving state across the session [^src9].

**Compaction**: when context nears the window limit, summarize the conversation and open a fresh context window with the summary plus only the still-relevant state. The summary becomes the new "start" — preserving what matters, discarding token-dense verbatim history. See [[ai-engineering/context-window-management|Context Window Management]] for operational mechanics [^src9].

**Sub-agent architectures**: for tasks that inherently exceed a single context window (long research, multi-day migrations), route sub-tasks to fresh agent instances rather than trying to fit everything in one window. Each sub-agent has a clean, focused context; the orchestrator holds only summaries. See [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] [^src9].

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

## LangChain's four strategies (Write / Select / Compress / Isolate)

LangChain published a widely cited framework that organizes every context-engineering technique into four categories [^src10]:

| Strategy | Problem solved | Techniques |
|---|---|---|
| **Write** | Agents forget across compaction | Scratch pads (agent takes notes mid-task), rules files (CLAUDE.md loaded each session), memory extraction (facts saved for cross-session retrieval) |
| **Select** | Context overload — don't give everything at once | Agentic RAG (agent decides what to search for, not a static pipeline), episodic/semantic/procedural memory selection |
| **Compress** | History grows unboundedly | Conversation summarization (trim oldest turns while keeping key decisions), context prioritization |
| **Isolate** | Accumulating tool-call noise | Parallel sub-agents each with clean context; multi-agent swarms (e.g. 300 sub-agents, each with fresh context, reporting back to orchestrator) |

The "Write" strategy includes the Anthropic **think tool** — a dedicated scratchpad workspace for Claude; on one benchmark, adding it improved performance by 54% on certain tasks [^src10].

## Seven categories competing for context (agent systems)

In a running agent, seven categories of information compete for the context budget [^src10]:

1. **System prompt** — identity, behavioral rules, control flow, architecture directives (can be several hundred tokens in complex agents)
2. **Tool definitions** — schema for every callable tool (even unused tools cost tokens)
3. **Tool results** — web retrieval: 5–10K tokens per call; file reads: similar
4. **Retrieved knowledge** — RAG documents, search results, API responses
5. **Conversation history** — grows linearly every turn; includes agent reasoning and prior decisions
6. **Memory** — short-term (session) and long-term (previous sessions); user preferences, learned patterns
7. **Agent state** — current plan, to-do list, progress markers, scratchpad notes

**Lost-in-the-middle**: a U-shaped attention curve means information at the start and end of context is best retained, while middle content degrades — measured as a 30+ percentage-point drop in accuracy when relevant info moves from beginning to middle. Original instructions buried under 50K tokens of tool outputs "effectively disappear" [^src10].

## Context engineering as the natural progression of prompt engineering

Anthropic describes context engineering as "the natural progression of prompt engineering" — it includes everything prompt engineering does (clear instructions, examples, structured formatting) plus a whole layer on top: managing tools, external data, message history, memory systems, and dynamic state [^src10]. "Prompt engineering is a subset of context engineering."

The LLM-as-OS analogy (LangChain): the model is the CPU (does the thinking), and the context window is RAM (working memory). "Just like your computer slows down when RAM fills up, your agent's reasoning degrades when your context window gets crowded" [^src10].

**Chroma's study** (18 frontier models including GPT-4.1, Claude 4, Gemini 2.5): every model's performance degrades as input length increases, even well below the stated context window limit. A 200K-token window may show significant degradation at 50K tokens. The decline is continuous, not a sudden cliff [^src10].

## Learn the framework, not the syntax

A practitioner corollary: "We are past the era where you need to learn how to do things. We are in an era where you need to learn what the framework is." Context engineering — knowing *what* capabilities exist and *when* to use them — is the meta-skill. An architect specifies intent; the AI (builder) executes the syntax [^src11].

Applied to Obsidian: telling Claude "build me a table that tracks X" is context engineering. Memorizing markdown table syntax is not. The same principle applies to any structured domain (Canvas JSON, Bases schema, SQL dialects) — delegate format correctness to domain-specific skills (see [[ai-engineering/agent-skills|Agent Skills]]) [^src11].

## Related concepts (referenced in source 1, not yet ingested)

- `context-engineering-ace-self-improving-llm-workflows` — agentic/self-improving applications of context engineering
- `writing-good-claude-md-context-engineering` — CLAUDE.md as a context engineering artifact
- `The C.R.A.F.T.E.D. Prompt Framework for Software Engineers` — prompt framework built on context engineering principles

## PRP workflow: INITIAL.md → /generate-prp → /execute-prp

A concrete, lightweight context engineering workflow centered on the **Product Requirements Prompt (PRP)** [^src12]:

1. **`INITIAL.md`** — write the feature request in plain English: what you want, key constraints, and what "done" looks like
2. **`/generate-prp INITIAL.md`** — Claude reads the initial request, researches the codebase, and produces a comprehensive PRP (detailed implementation plan, edge cases, test criteria) saved to `PRPs/<feature-name>.md`
3. **`/execute-prp PRPs/<feature-name>.md`** — Claude reads the PRP as its context spec and implements the feature end-to-end

The PRP separates **problem definition** (your job) from **implementation** (Claude's job). "Context engineering is 10× better than prompt engineering and 100× better than vibe coding" — the PRP is the artifact that compresses your intent into a context Claude can act on without ambiguity [^src12].

Standard project-level context files in this template: `CLAUDE.md` (project-specific guidelines), `examples/` folder (reference code examples — "highly recommended"), `PRPs/` folder (one PRP per feature). The `examples/` folder is especially important because it gives Claude concrete patterns to follow rather than relying on general training [^src12].

A highly starred variant (★13,479) from coleam00 follows the same pattern with nearly identical file structure and the declaration: "Context Engineering is 10× better than prompt engineering and 100× better than vibe coding" [^src14]. The wide adoption of these templates confirms PRP + examples folder as the community-consensus starting structure for context-engineered Claude Code projects.

## 10-section prompt structure (Context Buddy)

A visual framework for building well-structured prompts, implementing the 10-section methodology from Anthropic [^src13]:

| # | Section | Purpose |
|---|---|---|
| 1 | Task Context | Define AI's role and primary objective |
| 2 | Tone Context | Communication style and personality |
| 3 | Background Data | Reference materials, documents, data |
| 4 | Task Description & Rules | Requirements and constraints |
| 5 | Examples | Desired input/output patterns |
| 6 | Conversation History | Relevant prior context |
| 7 | Immediate Task | The current specific request |
| 8 | Thinking Steps | Encourage step-by-step reasoning |
| 9 | Output Formatting | Response structure |
| 10 | Prefilled Response | Starting text or format |

Context Buddy (★52, addyosmani/context-buddy) implements this as a visual interactive web app with template library and one-click copy [^src13]. The 10 sections map directly to the prompt engineering principle of separating *who you are*, *what you know*, *what you need* — the same taxonomy as the [[ai-engineering/ai-operating-system|AI OS]] layers.

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

[^src9]: [Effective Context Engineering for AI Agents](../../raw/web/web-effective-context-engineering-for-ai-agents.md) — Anthropic engineering blog

[^src1]: [[03_Resources/Articles/Context Engineering|Context Engineering]]
[^src2]: [[03_Resources/Study Notes/AI Agents - Complete Course Beginner to Pro|AI Agents - Complete Course Beginner to Pro]]
[^src3]: [[03_Resources/Study Notes/Claude Code - Solving the Memory Problem with Context Engineering|Claude Code - Solving the Memory Problem with Context Engineering]]
[^src4]: [How AI agents & Claude skills work (Clearly Explained)](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md>) — Greg Isenberg × Ras Mic, YouTube
[^src5]: [Introduction to ktx: The Open-Source Context Layer for Data Agents](../../raw/email/email-2026-06-03-fwd-introduction-to-ktx-the-open-source-context-layer-for-da.md) — Pipeline to Insights (Substack)
[^src6]: [ktx — Make analytics context usable by agents (docs)](../../raw/web/how-ingestion-works.md) — docs.kaelio.com
[^src10]: [Context Engineering in 29 Minutes: Complete Course](../../raw/youtube/-h9VVJIqtvA-context-engineering-in-29-minutes-complete-course.md) — Marina Wyss (Twitch), YouTube
[^src11]: [Stop Learning Obsidian](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-stop-learning-obs-report.md) — YouTube (notes report)
[^src12]: [IncomeStreamSurfer/context-engineering-intro (★267) — PRP workflow template](../../raw/github/github-incomestreamsurfer-context-engineering-intro.md) — IncomeStreamSurfer, GitHub
[^src13]: [addyosmani/context-buddy (★52) — 10-section prompt structure builder](../../raw/github/github-addyosmani-context-buddy.md) — Addy Osmani, GitHub
[^src14]: [coleam00/context-engineering-intro (★13479) — PRP template](../../raw/github/github-coleam00-context-engineering-intro.md) — coleam00, GitHub
