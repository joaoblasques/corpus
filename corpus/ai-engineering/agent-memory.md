---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/AI Dev - Agentic AI Architecture Explained.md
    channel: notes
    ingested_at: 2026-05-21
  - path: 03_Resources/Study Notes/Claude Code - Solving the Memory Problem with Context Engineering.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/web/zep-a-temporal-knowledge-graph-architecture-for-agent-memory.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/rushdb-2-0-memory-infrastructure-for-the-agentic-era-rushdb.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-05-14-what-agents-need-memory-context-and-more.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/notes/notes-clippings-built-in-memory-for-claude-managed-agents.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/web/web-from-rag-to-ai-memory-systems-building-stateful-architecture.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/web/web-github-thedotmack-claude-mem-persistent-context-across-sessi.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/web/web-using-agent-memory.md
    channel: web
    ingested_at: 2026-06-23
  - path: raw/_inbox/youtube-bgXEDymiZCc-i-built-karpathys-llm-wiki-in-obsidian.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/_inbox/youtube-ib74sLgjIBM-build-a-claude-knowledge-base-that-self-improves.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/_inbox/youtube-HxEQ7bLKrqI-give-claude-your-files-and-watch-what-happens.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/_inbox/notes-00-inbox-clippings-youtube-raw-raw-watched-build-this-once-a-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/_inbox/notes-00-inbox-clippings-youtube-raw-raw-watched-how-to-build-the-report.md
    channel: notes
    ingested_at: 2026-06-25
aliases:
  - agent memory
  - memory
  - short-term memory
  - long-term memory
  - vector memory
  - temporal knowledge graph
  - bi-temporal memory
  - memory infrastructure
  - portable memory
  - vault architecture
  - unified agentic memory
  - typed memory
  - memory manager
  - promotion gate
  - policy memory
  - preference memory
  - fact memory
  - episodic memory
  - trace memory
  - claude-mem
  - LLM wiki
  - self-improving knowledge base
  - information hierarchy
  - friction tax
  - append-only log
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-21
updated: 2026-06-25
confidence: 0.85
---

# Agent Memory

**TL;DR**: The two-tier memory system of AI agents — short-term (the context window) and long-term (external storage or persistent documents) — that together determine what the agent knows and can act on [^src1][^src2].

## Two tiers

| Tier | Mechanism | Scope |
|---|---|---|
| **Short-term** | Conversation history in the context window | Current session; lost when context resets or compacts |
| **Long-term** | [[ai-engineering/vector-database\|Vector databases]] (Pinecone, Weaviate, FAISS) **or** persistent documents (CLAUDE.md) | Persists across sessions; retrieved or referenced at any time |

Short-term memory is bounded by the context window limit — see [[ai-engineering/context-window-management|Context Window Management]] for strategies to manage what stays in window.

Long-term memory retrieval is a RAG operation: embed the query, similarity-search the vector store, inject retrieved memories into context [^src1]. See [[ai-engineering/rag|RAG]].

## Two long-term memory patterns

### Vector database (runtime retrieval)
Store agent outcomes and past decisions as embeddings in a vector database. Retrieved at query time via similarity search [^src1].

Options: Pinecone (cloud), Weaviate (open source), FAISS (in-process), pgvector (Postgres extension).

### Persistent documents (always-on reference)
A document like CLAUDE.md acts as long-term memory — written once, available throughout the session, survives compaction [^src2]. This pattern suits instructions, constraints, and architectural decisions that must always be in scope.

> "CLAUDE.md = long-term memory (always available). Context window = short-term memory (what's happening right now)." [^src2]

### Temporal knowledge graph (the third pattern)

Plain vector-store memory is a "hoarder": three facts — "Priya is evaluating," "Priya's blocker is SOC 2," "SOC 2 shipped in Q2" — are stored as disconnected blobs, so a query for "is Priya ready to buy?" retrieves whichever chunks sound similar and never connects the blocker to the fix [^src5]. The structural fix is a **temporal knowledge graph**: decompose facts into nodes (entities), attributes, and **edges** (relationships), then store them as a walkable graph instead of inert prose [^src5].

The defining feature is **bi-temporal edges**: each edge carries the period for which it was true, not just the claim that it is. When a fact changes, the system marks the old edge expired, dates the new one, and keeps both — giving memory a sense of before and after [^src5]. Retrieval then traverses only the relevant subgraph and silently filters for what is currently true.

**Zep** is a memory-layer service built on this architecture, powered by its core engine **Graphiti** — a temporally-aware knowledge graph that synthesizes unstructured conversational data and structured business data while maintaining historical relationships [^src3]. Where standard RAG frameworks are "limited to static document retrieval," Zep handles dynamic knowledge integration from ongoing conversations [^src3]:

- Beats prior SOTA MemGPT on the Deep Memory Retrieval benchmark (94.8% vs 93.4%) [^src3].
- On the harder LongMemEval benchmark, up to 18.5% accuracy improvement while **reducing response latency by 90%** vs baseline, strongest on cross-session synthesis and long-term context maintenance [^src3].

This is the same graph-over-flat-vectors insight as GraphRAG applied to memory — see [[ai-engineering/rag|RAG]] (GraphRAG section).

### Memory infrastructure (the data layer)

A trend treats the data layer and the memory layer as the same thing: agents, humans, and applications all read and write the same graph with the same query language [^src4]. **RushDB 2.0** exemplifies this — "memory infrastructure for the agentic era" — folding what used to be four separate concerns (vector store, embedding pipeline, sync, graph DB) into one system [^src4]:

- **Native semantic search** built into the graph; embedding indexes are first-class on any string property, with prefilter mode (filter by structured `where` first, then rank by similarity) [^src4].
- **Ontology API** — `getOntologyMarkdown` surfaces labels, types, value ranges, and the relationship map at session start, so MCP agents stop hallucinating field names [^src4].
- **MCP server + OAuth** and a packaged `rushdb-agent-memory` skill teaching the store → link → recall pattern with a label taxonomy (SESSION, DECISION, ENTITY, TASK, PREFERENCE) [^src4].

> The goal: "a world where the data layer and the memory layer are the same thing" [^src4].

Both Zep/Graphiti and RushDB build on graph databases like Neo4j for storing nodes and edges at scale [^src4][^src3].

## The "Learn" loop step

In the 4-step agentic loop (Perceive → Reason → Act → **Learn**), the Learn step stores outcomes to long-term memory. This enables an agent to improve at similar tasks over time [^src1].

## Portable memory across harnesses

A recurring 2026 theme is making memory **portable** rather than locked to one tool. The framing: agents need "the best approximation of the abilities that make humans nimble and versatile: memory, transferable context, and a nuanced understanding of the task" [^src6]. Two patterns surfaced together [^src6]:
- **A portable knowledge layer ("vault architecture")** — an external, auto-updated store of context the agent reads from, decoupled from any single chat/session, so you don't "start from scratch every single time."
- **Unified agentic memory via hooks** — even when a tool ships built-in memory, maintaining and *moving it between platforms* is the hard part; lifecycle hooks (`SessionStart`/`Stop`) that save and load context make memory portable across harnesses.

This is the memory-layer counterpart to the harness-level persistence hooks in [[ai-engineering/agent-harness|Agent Harness]] (ECC's memory-persistence hooks) and the knowledge-folder pattern in the [[ai-engineering/sources/internal-operating-system-claude-projects|internal-operating-system]] approach — and it mirrors the `CLAUDE.md`/`MEMORY.md` files of [[ai-engineering/claude-cowork|Claude Cowork]].

## Production-scale filesystem memory (Claude Managed Agents)

Anthropic's [[ai-engineering/claude-managed-agents|Claude Managed Agents]] extends the filesystem-as-memory pattern to production at enterprise scale [^src7]. Key properties that go beyond the basic CLAUDE.md/MEMORY.md pattern:

- Memory mounts directly onto a filesystem so Claude uses the same bash and code tools it already knows — no new abstraction layer.
- **Scoped stores** — org-wide stores can be read-only; per-user stores allow writes; multiple agents can work against the same store concurrently without overwriting each other.
- **Full audit trail** — every write is attributed to an agent + session; rollback to any earlier version is supported.
- **OAuth credential vaults** — a specialized memory type for storing user OAuth tokens once and injecting them into MCP connections at session creation [^src7].

Real-world results: Rakuten's long-running agents using Managed Agents memory cut first-pass errors by 97%; Wisedocs' document-verification pipeline saw 30% speed improvement from cross-session pattern memory [^src7].

## Typed memory architecture (RAG → stateful memory)

The gap between basic RAG and a real memory system is the presence of a **durable write path** [^src8]. RAG is retrieval only: embeddings in, top-k chunks out, nothing the model says flows back into the store. A memory system adds a managed write path and maintains continuity across sessions. "RAG helps a model look things up. A memory system helps an application remember and continue across turns" [^src8].

Five types, each with its own schema, lifecycle, and retrieval strategy [^src8]:

| Type | Retrieval | Risk if wrong |
|---|---|---|
| **Policy** | Exact match by key/version | Silent guardrail drift |
| **Preference** | Exact match by user ID — every turn | System feels generic |
| **Fact** | Hybrid: lexical + vector, fused, scope-filtered first | Memory poisoning, drift |
| **Episodic** | Hybrid over summaries, with task_type filter | Precedent becomes policy |
| **Trace** | Replay by run_id; vector only for forensics | No replay, no debugging |

Anti-pattern: one catch-all vector store for all types. Policies and preferences use exact-match SQL, not similarity — "policy retrieval that uses similarity is a bug, because you'll silently drift away from the rule that's actually in force" [^src8].

### The memory manager's five responsibilities

1. **Write (promotion gate)**: decides what enters durable memory. Gate steps: classify and scope, dedup by content hash + scope tuple, type-specific verification. Status computed from scope and type — never accepted from the caller. High rejection rate is expected and desired [^src8].
2. **Update with invalidation**: supersede the old fact, mark it revoked, invalidate any cached projections — in one transaction [^src8].
3. **Summarize (compression after stabilization)**: compress trace memory into episodic/fact — but only after stabilizing meaning (resolve references, normalize entities, drop retractions). Summarizing noise compresses faster than signal [^src8].
4. **Retrieve by type**: two parallel retrieval paths — (A) known-scope lookup: exhaustive SQL for all active policies and preferences on every turn; (B) semantic discovery: hybrid vector + lexical over facts/episodes, scope-filtered *before* ranking [^src8].
5. **Decide context window**: reserve fixed slots for policy and preferences; fill ranked slots for facts, episodes, recent context until token budget exhausted; compact rather than truncate mid-record [^src8].

The rule that kills most teams: **filter by scope before ranking**. Ranking across all tenants then filtering is a data-leak waiting to happen [^src8]. The correct pattern: `WHERE tenant_id = :current_tenant ORDER BY vector_distance(...)`.

### Prompt reassembly vs accumulation

Long-context transcripts are "the most common anti-pattern in this space" [^src8]. The pattern that works: rebuild the prompt on every turn from durable memory (policies + preferences + top-k facts + top-k episodes + summary of recent turns). The transcript stays in trace memory; the prompt is a reconstruction, not an accumulation. "Accumulating grows forever, reassembling stays bounded" [^src8].

### Filesystem vs database memory

The filesystem-as-memory pattern (CLAUDE.md, markdown agent notes) works for single-tenant local agents — models trained on developer workflows are "unusually competent with developer-native interfaces" [^src8]. It breaks for multi-tenant SaaS: no tenant isolation, no transactional guarantees, no hybrid retrieval in one query plan, no deletion cascade. Local files are "a useful interface for single-developer agents and a poor substrate for everything else" [^src8].

## claude-mem — persistent cross-session memory plugin

**claude-mem** (github.com/thedotmack/claude-mem) is an open-source plugin that adds persistent memory to Claude Code via Claude Code lifecycle hooks [^src9]. Install with `npx claude-mem install` (or `/plugin marketplace add thedotmack/claude-mem`); works with Claude Code, Gemini CLI, OpenCode, OpenClaw, and others.

How it works [^src9]:
- Five lifecycle hooks (SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd) capture tool-usage observations during a session.
- A worker service compresses observations with AI and stores them in a local SQLite + Chroma vector database.
- Future sessions receive relevant context injected automatically — "context survives across sessions."

The `mem-search` skill and four MCP tools (`search`, `timeline`, `get_observations`, `get_observations`) expose the memory via a **3-layer progressive disclosure workflow**: `search` returns a compact index (~50-100 tokens/result); `timeline` gives chronological context; `get_observations` fetches full details for filtered IDs only (~500-1,000 tokens/result). This 10× token reduction over naive full-fetch is the key design principle [^src9].

Key feature: `<private>` tags let users exclude sensitive content from storage. A web viewer UI at `http://localhost:37777` shows the real-time memory stream [^src9].

## LLM wiki pattern (Karpathy / self-improving knowledge base)

A recurring practitioner pattern applies the corpus's own design back to personal knowledge management: an **LLM wiki** where Claude is the librarian, ingesting sources into a structured knowledge base that improves over time [^src10][^src11].

**Karpathy's LLM wiki (Obsidian implementation)** [^src10]:
- Three folders: `raw/` (source files), `wiki/` (derived corpus pages), `outputs/` (final artifacts from Claude)
- An append-only `log.md` captures every session's decisions, edits, and learnings — the memory that survives compaction
- A `CLAUDE.md` schema instructs Claude on what belongs where, how to cite, and when to create new pages vs. update existing ones
- Pi agent integration for mobile and always-available access; the agent writes to the local Obsidian vault
- "Memory bank" pattern: after each session, Claude updates a structured log so the next session inherits what was learned

**Self-improving knowledge base (5-step framework)** [^src11]:
1. **Ingest** — source files land in `raw/`; Claude reads and routes to the right domain
2. **Extract** — entities, concepts, and claims extracted and cited
3. **Write** — dense reference pages created or updated in `wiki/`
4. **Health check skill** — a 7-stage monthly audit: contradictions, orphaned references, source provenance, stale articles, new article candidates, domain balance, coverage gaps
5. **Schedule** — the health check runs on a cron; no manual trigger needed

The health check is the key mechanism for *self-improvement*: the agent audits its own output, flags staleness and gaps, and proposes updates. "The corpus should compress what sources say, not invent what they don't" [^src11]. The compounding effect: each ingest cycle makes future ingests cheaper (fewer duplicate lookups, richer cross-references) and the health check catches drift before it accumulates [^src11].

## Information hierarchy (portable context architecture)

An alternative framing of the same problem as the LLM wiki, from a non-technical creator's perspective: the **information hierarchy** as a portable context layer that survives tool changes [^src12].

**The core insight**: "You don't build agents. You build the information that they read. The AI is the disposable part. The hierarchy is the part that lasts." [^src12]

**Structure** [^src12]:
- **Top tier — "My Business" folder**: four files — About Me, About My Business, About My Voice, About My Offers. Changes infrequently. Tool-agnostic (plain markdown).
- **Per-project folders**: each with five subfolders — Instructions, Voice, References, Examples, Notes.
  - `Notes` is the **compounding file**: logging results ("this newsletter issue had a 42% open rate") teaches the AI what works over time.

**Portability test** [^src12]: the same folder, pointed at Claude → Claude drafts newsletter topics; pointed at Gemini → Gemini drafts equivalent topics. The AI changes; the hierarchy is unchanged. "Whatever's best this month, next month, next year, two years — you point it at your hierarchy and it already knows your business."

**Relationship to the friction tax** [^src12]: the problem this architecture solves is the "friction tax" — re-explaining yourself every new chat, every new tool. The information hierarchy is written once; every AI session starts informed. The cost structure inverts: setup time is a one-time investment; session startup time approaches zero.

**Building it with Claude Co-work** [^src12]: Claude can scaffold the entire folder structure (leaving files empty) from a natural-language description, then interview you to fill in the `My Business` files. The `Notes` file is updated manually with real-world feedback signals after each project run.

This is the creator-friendly version of the typed memory architecture (policy, preference, fact stores) described above — same principle, simpler implementation for solo practitioners.

## Claude Co-work: file system as memory

Claude Co-work's file access enables a distinct memory pattern: using a local folder as a persistent, queryable knowledge layer across sessions [^src13]:

**File operations supported** [^src13]:
- **Parallel file reading** — read multiple PDFs or documents simultaneously, returning a synthesized summary
- **Editing existing files** — append to a log, update a running document, modify a config
- **Creating new files** — generate reports, exports, or new knowledge pages
- **Folder organization** — sort and move files based on content or naming patterns
- **Historical data iteration** — process 18 years of health log files, synthesizing trends; 1500+ Obsidian notes scanned for cross-folder synthesis

**Mental model** [^src13]: "Obsidian = Finder 2.0." The vault is a plain folder of markdown files; any file-aware agent (Claude Co-work, Claude Code, VS Code + Claude) can read and write it. Tool-agnostic access means the same vault works with any AI surface.

**Practical workflow (AI second brain)** [^src13]:
1. Create a top-level `CLAUDE.md` context file ("KJ OS") — who you are, your projects, your voice
2. Organize notes in a PARA-style vault (00 Notes / 01 Journal / 02 Projects / 03 Reviews / 04 Skills)
3. Run Claude Co-work against the vault to: draft project outputs, synthesize across notes, generate feedback-loop artifacts
4. Close the loop by saving Claude's outputs back into the vault

This is the file-as-memory pattern from [[ai-engineering/claude-managed-agents|Claude Managed Agents]] simplified for solo practitioners — no database, no API, just a folder of markdown.

## See also

- [[ai-engineering/context-window-management|Context Window Management]] — strategies for what to keep, compress, or drop from short-term memory
- [[ai-engineering/context-engineering|Context Engineering]] — governs how context is assembled at inference time
- [[ai-engineering/rag|RAG]] — long-term memory retrieval is structurally identical to RAG; GraphRAG mirrors temporal-graph memory
- [[ai-engineering/agentic-search|Agentic Search]] — AI-native search uses the same hybrid-retrieval-over-subgraph pattern
- [[ai-engineering/vector-database|Vector Database]] — the flat-vector storage layer that temporal graphs improve upon
- [[ai-engineering/embeddings|Embeddings]] — long-term memory stores facts as embeddings; their blob-like flatness is exactly what typed/graph memory fixes
- [[ai-engineering/ai-agent|AI Agent]] — memory is one of the four core agent components
- [[ai-engineering/claude-managed-agents|Claude Managed Agents]] — production implementation of filesystem memory with audit, scoping, and vault patterns

---

[^src1]: [[03_Resources/Study Notes/AI Dev - Agentic AI Architecture Explained|AI Dev - Agentic AI Architecture Explained]]
[^src2]: [[03_Resources/Study Notes/Claude Code - Solving the Memory Problem with Context Engineering|Claude Code - Solving the Memory Problem with Context Engineering]]
[^src3]: [Zep: A Temporal Knowledge Graph Architecture for Agent Memory](../../raw/web/zep-a-temporal-knowledge-graph-architecture-for-agent-memory.md)
[^src4]: [RushDB 2.0: Memory Infrastructure for the Agentic Era](../../raw/web/rushdb-2-0-memory-infrastructure-for-the-agentic-era-rushdb.md)
[^src5]: [But Context First: A Field Guide to AI-Native Search](../../raw/email/email-2026-05-28-but-context-first-a-field-guide-to-ai-native-search.md)
[^src6]: [What Agents Need: Memory, Context, and More](../../raw/email/email-2026-05-14-what-agents-need-memory-context-and-more.md) — Towards Data Science newsletter
[^src7]: [Built-in memory for Claude Managed Agents](../../raw/notes/notes-clippings-built-in-memory-for-claude-managed-agents.md) — Anthropic
[^src8]: [From RAG to AI Memory Systems: Building Stateful Architectures](../../raw/web/web-from-rag-to-ai-memory-systems-building-stateful-architecture.md) — Oracle Developer Blog
[^src9]: [claude-mem: Persistent Context Across Sessions](../../raw/web/web-github-thedotmack-claude-mem-persistent-context-across-sessi.md) — Alex Newman (@thedotmack), GitHub
[^src10]: [I Built Karpathy's LLM Wiki in Obsidian](../../raw/_inbox/youtube-bgXEDymiZCc-i-built-karpathys-llm-wiki-in-obsidian.md) — YouTube
[^src11]: [Build a Claude Knowledge Base That Self-Improves](../../raw/_inbox/youtube-ib74sLgjIBM-build-a-claude-knowledge-base-that-self-improves.md) — YouTube
[^src12]: [Build This ONCE. Any AI You Use Will Get Smarter Forever.](../../raw/_inbox/notes-00-inbox-clippings-youtube-raw-raw-watched-build-this-once-a-report.md) — YouTube (processed report)
[^src13]: [How To Build The ULTIMATE AI Second Brain (Obsidian + Claude Code)](../../raw/_inbox/notes-00-inbox-clippings-youtube-raw-raw-watched-how-to-build-the-report.md) — YouTube (processed report)
