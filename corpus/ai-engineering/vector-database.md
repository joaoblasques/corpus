---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/how-cockroachdb-built-vector-indexing-at-scale.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/vector-search-in-manticore-search-a-deep-dive.md
    channel: web
    ingested_at: 2026-06-12
aliases:
  - vector database
  - vector search
  - vector index
  - ANN
  - approximate nearest neighbor
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-21
updated: 2026-06-12
---

# Vector Database

**TL;DR**: A database optimized for storing and querying high-dimensional embedding vectors via approximate-nearest-neighbor (ANN) similarity search, used in RAG pipelines and agent long-term memory stores [^src1][^src2].

## How vector search works

A vector (embedding) is a list of floats — typically a few hundred to a few thousand dimensions — that captures the meaning of text, an image, or audio; similar things produce similar vectors [^src1]. Standard B-tree indexes do not apply because vectors have no natural ordering [^src1]. Brute-force comparison against every stored vector works for thousands but becomes hopeless at millions [^src1].

Vector indexes solve this by giving up exact answers: they find **approximate** nearest neighbors, trading a small accuracy loss for orders-of-magnitude speed [^src1]. That accuracy/speed tradeoff is the foundation of every vector index [^src1].

### Similarity metrics

| Metric | Measures | Use |
|---|---|---|
| **Euclidean (L2)** | Straight-line distance; magnitude-sensitive | Geometric/image data where absolute difference matters [^src2] |
| **Cosine** | Angle between vectors; orientation not magnitude | Text/semantic search [^src2] |
| **Inner product (dot)** | Magnitude and direction | Normalized vectors, recommendations [^src2] |

The metric is not arbitrary — embedding models are trained with a specific measure in mind, and using a different one yields suboptimal results [^src2].

## Index algorithms

### HNSW (Hierarchical Navigable Small World)

The graph-based algorithm powering pgvector, Weaviate, Manticore, and many others [^src1][^src2]. It builds layered graphs: the bottom layer holds every vector; higher layers have fewer vectors with longer-range links. Search starts at the top layer to jump across the data, refining downward until it reaches the right neighborhood [^src2]. Key tunables [^src2]:

- `hnsw_m` (default 16) — connections per vector; more = better accuracy, more memory, slower queries.
- `hnsw_ef_construction` (default 200) — index build thoroughness; higher = better quality, slower build.
- `ef` (search-time) — how hard the algorithm tries; higher = more accurate, slower.

HNSW is excellent on accuracy benchmarks but builds its graph **in memory** and resists sharding [^src1]. HNSW indexes can require 2–3× the size of the vector data in RAM [^src2].

### C-SPANN (CockroachDB) — vector indexing at scale

When CockroachDB added vector search, popular algorithms failed its distributed-SQL constraints (no central coordinator, no large in-memory caches, minimal network hops, sharding-compatible, no hot spots, incremental updates) [^src1]. HNSW failed on memory and sharding; classic IVF assumes single-node; Pinecone-style specialized DBs are separate systems [^src1]. So they built **C-SPANN**, borrowing from Microsoft's SPANN (tree partitioning), SPFresh (incremental updates), and Google's ScaNN (quantization) [^src1]:

- **Hierarchical K-means tree** — vectors grouped into partitions by similarity, each with a centroid; centroids grouped recursively into a wide, shallow tree. Fanout ~100 means 1M vectors need 3 levels, 10B need 5 [^src1].
- **Index as table data** — each partition is stored as key-value rows inside CockroachDB ranges, so splitting, rebalancing, caching, replication, and multi-region behavior all work for free from existing machinery [^src1]. Nodes serve queries immediately after restart because the index lives on disk, not a warm-up cache [^src1].
- **Nearest-partition assignment** (from SPFresh) keeps the index accurate as partitions split/merge in the background, without full rebuilds [^src1].
- **RaBitQ quantization** reduces each dimension to a single bit (~200 bytes/vector, a 94% reduction vs ~3 KB for a 1,536-dim OpenAI embedding), with a **reranking** step that re-fetches full-precision vectors for top candidates to absorb quantization error [^src1].
- **Prefix columns** (`VECTOR INDEX (user_id, embedding)`) give each tenant a separate K-means tree, so a billion vectors across a million users behaves like a million-vector index per user; combined with `REGIONAL BY ROW` it partitions by geography for locality and data domiciling [^src1].

> The architectural lesson: treat the vector index as ordinary table data and inherit the distributed machinery for free — "the algorithm is the part that gets the headlines, but the integration is what makes the system possible." [^src1]

The cheap-approximate-filter-then-precise-rerank pattern (scan quantized vectors → fetch full-precision candidates → exact distances) recurs across vector systems [^src1].

## Engine vs distributed-DB trade-off

| Choose specialized/in-memory (HNSW engines, Pinecone, Manticore) | Choose distributed-DB vector index (CockroachDB C-SPANN) |
|---|---|
| Pure vector workloads, no transactional component [^src1] | Vectors and transactional data must coexist in one system [^src1] |
| Read-heavy, batch-updated, freshness not critical [^src1] | Real-time, transactional freshness required [^src1] |
| Every microsecond of latency matters [^src1] | Multi-tenant isolation and multi-region domiciling matter [^src1] |

C-SPANN does not win on pure latency vs specialized in-memory systems and (as of its 25.2 preview) supports only Euclidean distance with limited non-prefix filtering [^src1].

## Production concerns

- **RAM vs disk chunks** (Manticore): each disk chunk has its own HNSW graph; KNN across many chunks searches each separately, hurting accuracy and speed, so fewer larger chunks beat many small ones [^src2]. Vector ops are CPU-intensive; plan 2–3× vector-data size in RAM [^src2].
- **Transactionality** — vector inserts/replaces/deletes can be atomic and binary-logged; Manticore supports multi-master Galera replication for vector tables [^src2].
- **Hybrid filtering** — combine KNN with keyword/metadata filters in one query (e.g. find images similar to a vector *and* matching text "white") [^src2]. This is the storage-layer basis for hybrid search in [[ai-engineering/rag|RAG]].

## Referenced by

- [[ai-engineering/rag|RAG]] — vector database is the storage layer in the RAG pipeline; chunks are embedded and stored here, then retrieved at query time via similarity search
- [[ai-engineering/agent-memory|Agent Memory]] — vector database is the primary mechanism for agent long-term memory; stores past results and decisions, retrieved across sessions
- [[ai-engineering/context-window-management|Context Window Management]] — sub-agents use isolated context windows, reducing the need to load large vector memory into the main agent's context

## Known options

| Option | Type | Index | Notes |
|---|---|---|---|
| Pinecone | Cloud, managed | — | Separate system; pure-vector workloads [^src1] |
| Weaviate | Open source, self-hosted or cloud | HNSW | Builds graph in memory [^src1] |
| FAISS | In-process (Meta AI) | various | No persistence by default |
| ChromaDB | Local, file-based | — | Good for development |
| pgvector | Postgres extension | HNSW | SQL-native; graph in memory [^src1] |
| Manticore | Open source search engine | HNSW | Transactional, replicated; multilingual; SQL + HTTP APIs [^src2] |
| CockroachDB | Distributed SQL DB | C-SPANN | Vector index as table data; multi-tenant, multi-region [^src1] |

## See also

- [[ai-engineering/rag|RAG]] — primary use case; hybrid search and temporal blind spots are partly vector-index limitations
- [[ai-engineering/agent-memory|Agent Memory]] — long-term memory pattern; temporal knowledge graphs improve on flat vector memory
- [[ai-engineering/agentic-search|Agentic Search]] — vector search is one half of the grep-vs-vector comparison

---

[^src1]: [How CockroachDB Built Vector Indexing at Scale](../../raw/web/how-cockroachdb-built-vector-indexing-at-scale.md)
[^src2]: [Vector Search in Manticore Search: A Deep Dive](../../raw/web/vector-search-in-manticore-search-a-deep-dive.md)
