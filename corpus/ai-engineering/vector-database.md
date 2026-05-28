---
type: concept
domain: ai-engineering
status: stub
sources: []
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-21
updated: 2026-05-21
---

# Vector Database

**TL;DR**: A database optimized for storing and querying high-dimensional embedding vectors via similarity search, used in RAG pipelines and agent long-term memory stores.

> No primary source ingested yet. This page is backed by three corpus pages that each treat vector databases as a core component. See v0.6 `derived_from:` candidate in `corpus/_log.md`.

## Referenced by

- [[ai-engineering/rag|RAG]] — vector database is the storage layer in the RAG pipeline; chunks are embedded and stored here, then retrieved at query time via similarity search
- [[ai-engineering/agent-memory|Agent Memory]] — vector database is the primary mechanism for agent long-term memory; stores past results and decisions, retrieved across sessions
- [[ai-engineering/context-window-management|Context Window Management]] — sub-agents use isolated context windows, reducing the need to load large vector memory into the main agent's context

## Known options

| Option | Type | Notes |
|---|---|---|
| Pinecone | Cloud, managed | — |
| Weaviate | Open source, self-hosted or cloud | — |
| FAISS | In-process (Meta AI) | No persistence by default |
| ChromaDB | Local, file-based | Good for development |
| pgvector | Postgres extension | SQL-native |

> [unsourced — please verify]: specific trade-offs between these options require a dedicated primary source.

## See also

- [[ai-engineering/rag|RAG]] — primary use case
- [[ai-engineering/agent-memory|Agent Memory]] — long-term memory pattern

---
