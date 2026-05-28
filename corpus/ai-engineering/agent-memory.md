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
aliases:
  - agent memory
  - memory
  - short-term memory
  - long-term memory
  - vector memory
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-21
updated: 2026-05-21
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

## The "Learn" loop step

In the 4-step agentic loop (Perceive → Reason → Act → **Learn**), the Learn step stores outcomes to long-term memory. This enables an agent to improve at similar tasks over time [^src1].

## See also

- [[ai-engineering/context-window-management|Context Window Management]] — strategies for what to keep, compress, or drop from short-term memory
- [[ai-engineering/context-engineering|Context Engineering]] — governs how context is assembled at inference time
- [[ai-engineering/rag|RAG]] — long-term memory retrieval is structurally identical to RAG
- [[ai-engineering/ai-agent|AI Agent]] — memory is one of the four core agent components

---

[^src1]: [[03_Resources/Study Notes/AI Dev - Agentic AI Architecture Explained|AI Dev - Agentic AI Architecture Explained]]
[^src2]: [[03_Resources/Study Notes/Claude Code - Solving the Memory Problem with Context Engineering|Claude Code - Solving the Memory Problem with Context Engineering]]
