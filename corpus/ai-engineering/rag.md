---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/AI Tools - Local RAG Complete Tutorial.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/web/from-local-to-global-a-graph-rag-approach-to-query-focused-s.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/_inbox/email-2026-05-21-diving-deep-into-rag-document-extraction-and-more.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/7-temporal-blind-spots-breaking-enterprise-rag-news-from-gen.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/notes/notes-clippings-seeing-like-an-agent-how-we-design-tools-in-claude-code.md
    channel: notes
    ingested_at: 2026-06-17
aliases:
  - RAG
  - retrieval-augmented generation
  - retrieval augmented generation
  - GraphRAG
  - graph RAG
  - temporal RAG
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-21
updated: 2026-06-17
---

# RAG (Retrieval-Augmented Generation)

**TL;DR**: A pattern that solves LLM knowledge cutoff, private-data blindness, and hallucination by injecting relevant, current documents into the context window at query time [^src1].

## Why it exists

Three core LLM limitations that RAG addresses [^src1]:

| Limitation | RAG fix |
|---|---|
| Knowledge cutoff | Retrieved documents can be current |
| No private data | Your documents are retrieved locally or from private store |
| Hallucination | Grounding the response in retrieved context reduces confabulation |

## Architecture

```
Documents → Chunks → Embeddings → Vector DB
                                      ↑
User Query → Embed Query → Similarity Search → Retrieved Chunks
                                              ↓
                                   LLM + Context → Response
```
[^src1]

## Implementation steps

### 1. Document processing (chunking)
Split documents into segments of typically 500–1000 tokens with overlap. Preserve structure where possible (headers, paragraphs) [^src1].

### 2. Embedding
Convert each chunk to a dense vector using an embedding model. Options:
- `text-embedding-3-small` (OpenAI, API)
- Sentence-Transformers (open source, runs locally on CPU)

### 3. Vector database
Store embeddings alongside original text in a [[ai-engineering/vector-database|vector database]]. At query time, similarity search returns the K most relevant chunks.

| Option | Type | Notes |
|---|---|---|
| ChromaDB | Local, file-based | No server required; good for dev |
| pgvector | Postgres extension | SQL-native; production-ready |
| Pinecone | Cloud | Managed; suited for scale |

### 4. Query pipeline

```python
query_embedding = embed_model.encode(user_query)
similar_chunks = vector_db.similarity_search(query_embedding, k=5)
context = "\n".join([chunk.text for chunk in similar_chunks])
response = llm.complete(f"Context: {context}\n\nQuestion: {user_query}")
```
[^src1]

## Local vs cloud RAG

| Local | Cloud |
|---|---|
| Private/sensitive data | Scale needed |
| No API cost | Best model performance |
| Air-gapped environments | Team access or compliance needs |
| Development/testing | Production deployments |

Local stack: Sentence-Transformers (embeddings) + ChromaDB (vector store) + Ollama (LLM) [^src1].

## Document extraction (the ingest front-end)

Before chunking and embedding, source documents (PDFs, scans, forms) must be parsed into text. Two approaches, with a documented trade-off [^src2]:

| Approach | Tooling | When it wins |
|---|---|---|
| **Rule-based / OCR** | pytesseract + regex rules | Structured, predictable layouts (e.g. B2B order forms); deterministic, cheap, auditable |
| **LLM-based** | Ollama + LLaMA 3 (local) or API | Messy, variable layouts; tolerates format drift but slower and can be "a suboptimal choice" for rigid structured extraction [^src2] |

A side-by-side build of the same B2B document extractor found neither approach dominates — rule-based extraction outperformed the LLM on the realistic structured-order scenario [^src2]. Extraction quality bounds retrieval quality: garbage parsed in is garbage retrieved.

## Hybrid search and re-ranking

Pure semantic (dense vector) retrieval is often insufficient in production [^src2]. **Hybrid search** blends dense embeddings with sparse keyword (BM25) matching, then applies a **re-ranker** to reorder candidates. This recovers exact-token matches (names, IDs, codes like "SOC 2") that pure embeddings smooth away [^src2]. See [[ai-engineering/agentic-search|Agentic Search]] for the grep-vs-vector evidence on when lexical matching beats semantic search.

## GraphRAG: local-to-global retrieval

Conventional RAG fails on **global** questions over an entire corpus — e.g. "What are the main themes in the dataset?" — because such queries are query-focused summarization (QFS), not explicit retrieval [^src3]. GraphRAG (Microsoft Research) addresses this with an LLM-built graph index in two stages [^src3]:

1. **Entity knowledge graph** — derive entities and relationships from source documents.
2. **Community summaries** — pre-generate summaries for groups of closely related entities.

At query time, each community summary produces a partial response; partials are summarized into a final answer. On global sensemaking questions over ~1M-token datasets, GraphRAG substantially improves answer **comprehensiveness and diversity** over a conventional RAG baseline [^src3]. The graph structure beats flat vector retrieval specifically on big-picture questions spanning the whole corpus [^src3].

> "RAG fails on global questions directed at an entire text corpus … since this is inherently a query-focused summarization task" [^src3].

This connects to agent memory: temporal knowledge graphs apply the same graph-over-vectors insight to long-term memory. See [[ai-engineering/agent-memory|Agent Memory]].

## Temporal blind spots (enterprise failure modes)

Vectors encode semantics but do not age — an embedding of a quarterly report looks as relevant months later as on release day [^src4]. Time is treated as an afterthought in most RAG architectures, producing silent, high-stakes failures [^src4]. The seven documented temporal blind spots [^src4]:

| # | Blind spot | Failure |
|---|---|---|
| 1 | **Stale indexes** | Index is a snapshot frozen at build time; daily refresh lags six-hour user expectations |
| 2 | **Time-blind embeddings** | A 2023 and 2025 report embed near-identically; cosine similarity sees twins |
| 3 | **Query-to-context time mismatch** | "current policy" emits no date keyword; retriever ignores the implicit time constraint |
| 4 | **Temporal hallucination** | Facts true at some past point linger (e.g. "the UK is a member of the EU") |
| 5 | **Evaluation gaps** | RAGAS-style metrics ignore temporality; a system scores perfectly while serving outdated answers |
| 6 | **Chunking against the clock** | Semantic chunking breaks chronological narrative (cause severed from effect) |
| 7 | **Cost overruns** | Naive hourly re-indexing can triple vector DB cost for unnoticed accuracy gains |

Countermeasures [^src4]: event-driven index invalidation, sparse metadata filters that boost/filter by publication or effective date, **temporal query decomposition** (parse time cues, inject structured time filters), bi-temporal validity intervals, structure-aware chunking with temporal anchors, interval-aware test suites, and a **tiered freshness model** (high-urgency data streams real-time; medium refreshes hourly via delta indexes; low updates nightly) tied to business-impact SLAs.

> A vector index without temporal awareness is "a museum, not a live knowledge base" [^src4].

## RAG vs. agentic search

A design-level distinction: in RAG the agent is *given* pre-retrieved context; in agentic search the agent *finds* its own context using tools like Grep [^src5]. Claude Code started with RAG internally (a vector DB pre-indexed the codebase, snippets handed to Claude before each response) but moved to agentic search because (a) RAG requires indexing and setup, (b) is fragile across environments, and (c) fundamentally positions the agent as a passive recipient of context rather than an active searcher [^src5]. As models improve at building their own context when given the right tools, the balance tilts further toward agentic search for coding tasks. See [[ai-engineering/agentic-search|Agentic Search]] for the full treatment.

## Role in context engineering

Retrieved chunks are one of the four context components injected into an agent's context window. See [[ai-engineering/context-engineering|Context Engineering]] — "Retrieved context" slot.

## Key terms

| Term | Definition |
|---|---|
| **Chunk** | A segment of a source document |
| **Embedding** | Dense vector representation of text |
| **Similarity search** | Find chunks whose embeddings are closest to the query embedding |
| **K** | Number of top chunks to retrieve |

## See also

- [[ai-engineering/context-engineering|Context Engineering]] — RAG provides the "Retrieved context" component
- [[ai-engineering/ai-agent|AI Agent]] — retrieval quality is a key agent evaluation metric
- [[ai-engineering/agent-evaluation|Agent Evaluation]] — retrieval quality as a measured metric; temporal accuracy is a missing eval dimension
- [[ai-engineering/agentic-search|Agentic Search]] — agent-orchestrated retrieval; grep-vs-vector trade-offs
- [[ai-engineering/agent-memory|Agent Memory]] — temporal knowledge graphs extend GraphRAG's graph-over-vectors insight to memory
- [[ai-engineering/vector-database|Vector Database]] — the storage layer; temporal blind spots are partly a vector-indexing limitation

---

[^src1]: [[03_Resources/Study Notes/AI Tools - Local RAG Complete Tutorial|AI Tools - Local RAG Complete Tutorial]]
[^src2]: [Diving Deep into RAG, Document Extraction, and More](../../raw/email/email-2026-05-21-diving-deep-into-rag-document-extraction-and-more.md)
[^src3]: [From Local to Global: A Graph RAG Approach to Query-Focused Summarization](../../raw/web/from-local-to-global-a-graph-rag-approach-to-query-focused-s.md)
[^src4]: [7 Temporal Blind Spots Breaking Enterprise RAG](../../raw/web/7-temporal-blind-spots-breaking-enterprise-rag-news-from-gen.md)
[^src5]: [Seeing like an agent: how we design tools in Claude Code](../../raw/notes/notes-clippings-seeing-like-an-agent-how-we-design-tools-in-claude-code.md) — Thariq Shihipar, Anthropic
