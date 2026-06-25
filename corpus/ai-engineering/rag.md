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
  - path: raw/email/email-2026-05-21-diving-deep-into-rag-document-extraction-and-more.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/7-temporal-blind-spots-breaking-enterprise-rag-news-from-gen.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/notes/notes-clippings-seeing-like-an-agent-how-we-design-tools-in-claude-code.md
    channel: notes
    ingested_at: 2026-06-17
  - path: raw/web/web-beyond-the-vector-store-building-the-full-data-layer-for-ai.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/youtube/youtube-2KVkpUGRtnk-build-real-time-knowledge-graph-for-documents-with-llm.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/github/github-the-pocket-pocketflow-tutorial-codebase-knowledge.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/github/github-google-langextract.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/github/github-canner-wrenai-give-ai-agents-the-context-to-query-bus.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-karpathy-s-obsidi-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-pfPi04pIfaw-claude-code-agentic-os-unstoppable.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/github/github-catchthetornado-text-extract-api.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/github/github-runanywhereai-rcli.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-build-real-time-k-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-2KVkpUGRtnk-build-real-time-knowledge-graph-for-documents-with-llm.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - RAG
  - retrieval-augmented generation
  - retrieval augmented generation
  - GraphRAG
  - graph RAG
  - temporal RAG
  - hybrid RAG
  - pre-filter pattern
  - pgvector unified store
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-21
updated: 2026-06-25
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

## Beyond the vector store: the full data layer

Production RAG systems require more than a vector database — the full data layer combines multiple storage types, each with a distinct role [^src6]:

| Layer | Type | Role | Best tool |
|---|---|---|---|
| **Semantic retrieval** | Vector DB | Similarity-based chunk lookup | pgvector, Pinecone |
| **Structured queries** | Relational DB | Exact filters (user, date, category) | PostgreSQL |
| **Fast lookups** | Cache | Recent queries, user prefs | Redis |
| **Document storage** | Object store / blob | Source files, attachments | S3, GCS |
| **Activity history** | Time-series / append-only | Audit log, conversation history | TimescaleDB, Postgres |

**The pre-filter pattern** (most impactful single optimization) [^src6]: filter by structured metadata *before* doing vector similarity search, not after.

Without pre-filter:
```sql
-- Poor: similarity over all 10M rows, then filter
SELECT * FROM chunks ORDER BY embedding <-> $query_vec LIMIT 20
HAVING user_id = $user AND category = 'legal'
```

With pre-filter:
```sql
-- Better: filter first, similarity only over the small matching set
SELECT * FROM chunks
WHERE user_id = $user AND category = 'legal'
ORDER BY embedding <-> $query_vec LIMIT 5
```

The gain: "similarity search over 5,000 relevant rows is far faster and more accurate than searching 10M rows and filtering after" [^src6]. This is also the scope-before-ranking rule from [[ai-engineering/agent-memory|Agent Memory]] applied to retrieval.

**Post-retrieval enrichment** — after vector retrieval, join with structured data before sending to the LLM [^src6]:
```python
# Get semantic matches
chunks = vector_db.search(query_embedding, k=20, filter=pre_filters)
# Enrich with user/document metadata from relational DB
enriched = db.query("SELECT u.name, u.tier, d.created_at, c.content
  FROM chunks c JOIN documents d ON ... JOIN users u ON ...
  WHERE c.id = ANY($chunk_ids)", [c.id for c in chunks])
# Send enriched context to LLM
```

**pgvector as a unified store**: for many applications, a single PostgreSQL + pgvector deployment handles both vector and relational needs, eliminating the operational overhead of running separate databases [^src6]. pgvector supports IVFFlat and HNSW indexing; HNSW gives better recall at the cost of more memory. "For many startups and medium-scale applications, pgvector in PostgreSQL is the pragmatic choice before scaling to a dedicated vector database" [^src6].

**Conversation history as a first-class data layer**: storing conversation history in a queryable database (not just in-memory) enables: (a) context retrieval beyond the current context window; (b) analytics on user intent trends; (c) personalization from past sessions [^src6]. Schema: `conversation_id`, `session_id`, `role`, `content`, `timestamp`, `token_count`.

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

## Real-time knowledge graph for documents (CocoIndex + Neo4j)

CocoIndex is an open-source incremental ETL framework for building knowledge graphs from documents with LLMs [^src7]. The pattern:

1. **Extract** — parse documents (PDF, markdown, etc.) into structured entities and relationships using LLM extraction
2. **Index** — build a knowledge graph in Neo4j (or similar); the "incremental" design means only changed documents re-trigger extraction, not the full corpus
3. **Query** — run Cypher queries over the graph from Claude or any LLM agent

Key insight vs flat vector RAG: a knowledge graph explicitly encodes entity relationships (A `uses` B, C `depends-on` D), enabling *traversal* queries ("what does X connect to?") rather than only similarity queries ("what's closest to this embedding?"). This is the graph RAG advantage from [^src3] operationalized as a real-time pipeline [^src7].

**Use case fit**: suited for document collections with rich cross-references (legal documents, technical specs, scientific papers, codebases). Less suited for large unstructured prose where entity extraction quality is unreliable [^src7].

See also: [[ai-engineering/embeddings|Embeddings]] for the underlying vector layer, and the GraphRAG section above for the theoretical framing.

## PocketFlow: codebase-to-knowledge pipeline

PocketFlow (`The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge`, 12K★, Python) applies the knowledge-extraction pattern specifically to code: it crawls a GitHub repository, identifies core abstractions and their interactions, and generates beginner-friendly tutorials with visualizations [^src8].

**Core capability**: given a repository URL, it:
1. Traverses the code
2. Uses an LLM to identify the key abstractions (classes, modules, protocols)
3. Maps their relationships
4. Generates a structured tutorial explaining how the codebase works

This is a specific application of the "knowledge graph from documents" pattern to codebases — converting graph structure implicit in code (imports, class hierarchies, function calls) into explicit LLM-queryable knowledge [^src8].

**Built on PocketFlow**, a 100-line LLM framework. Reached Hacker News front page (April 2025, 900+ upvotes) [^src8].

## LangExtract — structured extraction with source grounding

**LangExtract** (Google, github.com/google/langextract, ★36K) is a Python library for LLM-powered structured extraction that emphasizes **precise source grounding** — every extracted field is linked to the exact span in the source document from which it was drawn [^src9].

Key properties [^src9]:
- **Span-grounded extraction**: the library returns not just extracted values but also `source_spans` — character offsets in the original document. This lets you verify that "Customer: Acme Corp" came from line 3 of the contract, not a hallucination.
- **Structured output**: integrates with Pydantic schemas; returns type-safe structured objects
- **Multi-hop extraction**: can chase references across sections (e.g. "all items in section 3 that refer to the term defined in section 1")
- **Use case fit**: best for documents with a known schema (contracts, medical records, financial filings, invoice processing) where hallucination risk is high and auditability is required

LangExtract addresses a core RAG failure mode: when extraction is used to populate a structured database from documents, ungrounded extraction creates confident-sounding wrong answers. Source grounding turns extraction into an auditable operation [^src9].

## WrenAI — business semantic layer for text-to-SQL agents

**WrenAI** (github.com/Canner/WrenAI, ★8K+) is an open-source **context layer** for text-to-SQL agents. It provides:
- **MDL (Modeling Definition Language)**: a semantic layer that maps raw database tables/columns to business-friendly names, joins, metrics, and calculated fields. The LLM reasons about "Monthly Recurring Revenue" and "Churned Customers" rather than `SUM(amount) WHERE status='active'`
- **LanceDB memory**: conversation memory stored as embeddings, enabling multi-turn SQL refinement ("make that by region" correctly modifies the previous query rather than starting over)
- **Open context layer**: WrenAI positions itself as a standard for defining what "business context" an AI agent should have when querying a database

The core insight: text-to-SQL LLMs fail not because they can't write SQL, but because they don't know what the business's columns mean. WrenAI gives the agent a structured vocabulary [^src10].

## Karpathy's Obsidian file-system-as-RAG (no vectors)

A practitioner-discovered pattern: use a structured Markdown file hierarchy that Claude Code can navigate directly, eliminating the need for a vector database or retrieval pipeline [^src11]:

**Why it works**: Claude Code's file-browsing tools (list, read, grep) are sufficient for a corpus under thousands of documents. The `_master-index.md` narrows the search space in 2–3 tool calls instead of grepping everything.

**Structure** [^src11]:
- `raw/` — staging area for ingested articles, papers, GitHub repos (source files, unmodified)
- `wiki/` — LLM-generated knowledge pages indexed by a `_master-index.md` and per-subdomain index files
- Each wiki subdomain (`ai-agents/`, `rag-systems/`) has its own `index.md` listing all pages

**Traversal path** [^src11]: vault → `wiki/_master-index.md` → appropriate subdomain `index.md` → specific page. The master index is the entry point; without it, the agent would have to search the entire vault.

**CLAUDE.md as the schema** [^src11]: a single `claude.md` (or `CLAUDE.md`) encodes the traversal rules and note format (Wikilinks, front-matter schema) so the agent never re-derives conventions and navigation is token-efficient.

**Scale verdict** [^src11]: for solo operators and small teams under a few thousand documents, this approach is lightweight, essentially free, and good enough. True RAG (vector databases, embedding pipelines) only wins at the scale of millions of documents. "Just start with Obsidian and graduate to LightRAG/true RAG only if you clearly outgrow it."

This is the Karpathy RAG pattern implemented as a personal knowledge corpus — the same principle as [[ai-engineering/agent-memory|Agent Memory]] §LLM wiki pattern but focused on answering document-level factual queries.

## text-extract-api: PDF/Office extraction pipeline

`catchthetornado/text-extract-api` is a self-hosted extraction pipeline for feeding documents into RAG systems [^src12]:

- Converts PDF, DOCX, PPTX, images to markdown or JSON (clean, structured for embedding)
- EasyOCR for scanned documents; Ollama integration for local LLM-assisted extraction
- PII removal before documents leave the local environment (compliance use case)
- No cloud dependency — full local stack
- API-first: send a file, receive clean markdown/JSON

Target use case: private document collections (legal, medical, financial) where sending documents to cloud APIs is prohibited [^src12].

## RCLI: on-device voice + local RAG

`runanywhereai/rcli` is a macOS CLI tool that adds voice AI control with local RAG [^src13]:

- Speech-to-text + LLM + text-to-speech, all running locally on Apple Silicon
- Sub-200ms latency (vs 500ms+ for cloud voice APIs)
- 40+ macOS system actions available by voice (window management, app control, file operations)
- Local RAG: builds a semantic index over the user's documents; voice queries retrieve from this index rather than sending data to cloud
- Useful for private document Q&A at low latency

Combined with text-extract-api, forms a fully local document-intelligence pipeline: extract → embed → index → query via voice [^src13].

## See also

- [[ai-engineering/embeddings|Embeddings]] — the dense vectors RAG retrieves over; their limits (exact-token loss, no time, disconnected facts) drive hybrid search, temporal filters, and GraphRAG
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
[^src6]: [Beyond the Vector Store: Building the Full Data Layer for AI](../../raw/web/web-beyond-the-vector-store-building-the-full-data-layer-for-ai.md) — Kevin Smith, Saturn Cloud blog
[^src7]: [Build Real-Time Knowledge Graph for Documents with LLM](../../raw/youtube/youtube-2KVkpUGRtnk-build-real-time-knowledge-graph-for-documents-with-llm.md) — CocoIndex + Neo4j demo, YouTube
[^src8]: [The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge (12K★)](../../raw/github/github-the-pocket-pocketflow-tutorial-codebase-knowledge.md) — The-Pocket, GitHub
[^src9]: [google/langextract — Structured extraction with source grounding (★36K)](../../raw/github/github-google-langextract.md) — Google, GitHub
[^src10]: [Canner/WrenAI — Open context layer for AI agents querying business data](../../raw/github/github-canner-wrenai-give-ai-agents-the-context-to-query-bus.md) — Canner, GitHub
[^src11]: [Karpathy's Obsidian RAG + Claude Code = CHEAT CODE (notes report)](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-karpathy-s-obsidi-report.md) — Chase AI, YouTube (processed report)
[^src12]: [catchthetornado/text-extract-api — document extraction pipeline](../../raw/github/github-catchthetornado-text-extract-api.md) — GitHub
[^src13]: [runanywhereai/rcli — on-device voice AI with local RAG](../../raw/github/github-runanywhereai-rcli.md) — GitHub
[^src14]: [Build Real-Time Knowledge Graph For Documents with LLM (processed notes report)](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-build-real-time-k-report.md) — CocoaIndex + Neo4j tutorial, YouTube (processed report)
[^src14a]: [Build Real-Time Knowledge Graph For Documents with LLM (video)](../../raw/youtube/youtube-2KVkpUGRtnk-build-real-time-knowledge-graph-for-documents-with-llm.md) — CocoaIndex + Neo4j tutorial, YouTube

## Knowledge graph from documents (CocoaIndex + Neo4j)

An alternative to vector-only RAG: build a property-graph knowledge base from documents using LLM extraction and export to Neo4j [^src14].

**Architecture** [^src14]:

| Step | What happens |
|---|---|
| Document ingest | `CocoaIndex.LoadFromFile` → KTable of (filename, content) |
| Summary extraction | `ExtractByLLM` → `DocumentSummary(title, summary)` per doc |
| Relationship extraction | `ExtractByLLM` → list of `Relationship(subject, predicate, object)` triples |
| Entity mention | No extra LLM call — collect (entity, doc) pairs from subject/object of each triple |
| Neo4j export | Map docs → nodes, entities → nodes (deduped by primary key), relationships → edges |

**Property graph model** [^src14]: nodes have labels + primary keys; relationships have exactly one type; CocoaIndex deduplicates nodes by primary key so the same entity from many documents collapses into one node.

**CocoaIndex incremental processing** [^src14]: you declare mapping + transformation only; CocoaIndex handles create/update/delete to the target automatically. Cocoa Insight provides step-by-step data observability during the pipeline.

**When to use knowledge graphs over vector RAG** [^src14]:
- Questions requiring multi-hop reasoning: "What connects entity A to entity B?"
- Relationship-typed queries: "What does X cause?", "What does Y depend on?"
- Dense cross-document entity networks (many docs referring to shared named entities)
- Cases where chunk-level retrieval loses relational structure

**LLM extraction guidance** [^src14]: detailed docstrings in the `Relationship` data class ("the subject field must contain a named entity, predicate must be a verb phrase...") significantly improve triple quality. The structured extraction step is the most model-sensitive part of the pipeline.

See also: [[ai-engineering/rag|RAG]] (vector RAG patterns), [[ai-engineering/embeddings|Embeddings]] (the vector alternative to graph edges).
