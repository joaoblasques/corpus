---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/how-llms-actually-work.md
    channel: web
    ingested_at: 2026-06-16
  - path: 03_Resources/Study Notes/AI - How Large Language Models Work.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/web/how-cockroachdb-built-vector-indexing-at-scale.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/vector-search-in-manticore-search-a-deep-dive.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/web-beyond-the-vector-store-building-the-full-data-layer-for-ai.md
    channel: web
    ingested_at: 2026-06-17
  - path: raw/web/7-temporal-blind-spots-breaking-enterprise-rag-news-from-gen.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/is-grep-all-you-need-the-harness-matters-more-than-the-searc.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/_inbox/youtube-zZsTVBXcbow-how-google-deepmind-is-researching-the-next-frontier-of-ai-f.md
    channel: youtube
    ingested_at: 2026-06-27
aliases:
  - embedding
  - embeddings
  - embedding model
  - dense vector
  - vector embedding
  - text embedding
  - embedding matrix
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-23
updated: 2026-06-23
---

# Embeddings

**TL;DR**: An embedding is a dense vector — a list of a few hundred to a few thousand floating-point numbers — that encodes the meaning of a piece of text (or image/audio) such that semantically similar things produce similar vectors [^src3]. Embeddings are the shared substrate beneath two layers of the LLM stack: they are how a transformer first represents tokens internally [^src1], and they are how retrieval systems (RAG, agent memory, semantic search) measure "similar in meaning" at query time [^src5]. This page consolidates what the corpus establishes about embeddings; the storage-and-indexing side lives in [Vector Database](/ai-engineering/vector-database.md) and the retrieval side in [RAG](/ai-engineering/rag.md).

## Two distinct senses of "embedding"

The word covers two related but different objects, and conflating them is a common source of confusion.

| Sense | What it is | Where it lives |
|---|---|---|
| **Token embedding** (internal) | The model's learned representation of a single vocabulary token, looked up at the start of every forward pass | Inside the [Transformer](/ai-engineering/transformer.md) |
| **Sentence/document embedding** (external) | A single vector summarizing a whole chunk of text, produced by an embedding model for retrieval | In a [Vector Database](/ai-engineering/vector-database.md) |

Both are dense vectors in which geometric closeness means semantic closeness, but the first is a building block of the LLM's own computation while the second is an artifact you store and query.

## Token embeddings (inside the model)

A token ID is just a row index with no inherent meaning. The **embedding matrix** is a lookup table with one row per vocabulary entry; each row is a long vector whose length is the model's **hidden size** (often 4,096 numbers per token in 7B-class models) [^src1]. The looked-up vector is the token's embedding — its learned representation of "meaning" [^src1].

Semantically similar tokens end up with similar vectors ("king" close to "queen", "Paris" close to "France"), emergent from training, not hard-coded [^src1]. Embedding arithmetic sometimes works — the famous example: **king − man + woman ≈ queen** [^src1].

Two facts about token embeddings shape everything downstream:

- **Position is separate.** Plain self-attention has no built-in word-order representation; the embedding for "dog" is identical at position 1 or position 5, so positional encoding (additive sinusoidal, or RoPE) injects position separately [^src1]. See [Transformer](/ai-engineering/transformer.md) §Positional encoding.
- **Meaning is contextual after layer 0.** The initial embedding is context-free; attention then updates each token's vector by mixing in the other tokens it can see, so the representation that flows through the residual stream is increasingly context-dependent [^src2][^src1].

## Sentence/document embeddings (for retrieval)

For retrieval, an **embedding model** maps an entire chunk of text to one dense vector. Convert each chunk to a dense vector using an embedding model; common options are `text-embedding-3-small` (OpenAI, API) and Sentence-Transformers (open source, runs locally on CPU) [^src5-rag]. A query is embedded the same way, and **similarity search** returns the K chunks whose vectors are closest to the query vector [^src5-rag].

A vector (embedding) is "a list of floats — typically a few hundred to a few thousand dimensions — that captures the meaning of text, an image, or audio; similar things produce similar vectors" [^src3]. Standard B-tree indexes do not apply because vectors have no natural ordering, and brute-force comparison against every stored vector works for thousands but becomes hopeless at millions [^src3] — which is why embeddings are stored in a [Vector Database](/ai-engineering/vector-database.md) with an approximate-nearest-neighbor index.

### Similarity metrics

How "closeness" is measured is not arbitrary — embedding models are trained with a specific measure in mind, and using a different one yields suboptimal results [^src4]:

| Metric | Measures | Typical use |
|---|---|---|
| **Cosine** | Angle between vectors; orientation not magnitude | Text/semantic search [^src4] |
| **Euclidean (L2)** | Straight-line distance; magnitude-sensitive | Geometric/image data [^src4] |
| **Inner product (dot)** | Magnitude and direction | Normalized vectors, recommendations [^src4] |

## The cost of dimensionality

Embedding vectors are large and the storage adds up fast: a 1,536-dimensional OpenAI embedding is roughly 3 KB per vector, so a corpus of millions of chunks runs into gigabytes [^src3]. Two responses recur across vector systems:

- **Quantization.** CockroachDB's C-SPANN uses **RaBitQ quantization** to reduce each dimension to a single bit (~200 bytes/vector, a 94% reduction vs ~3 KB), then a **reranking** step re-fetches full-precision vectors for top candidates to absorb the quantization error [^src3]. The cheap-approximate-filter-then-precise-rerank pattern (scan quantized vectors → fetch full-precision candidates → exact distances) recurs across vector systems [^src3].
- **RAM pressure from in-memory indexes.** HNSW indexes can require 2–3× the size of the vector data in RAM because the graph is built and held in memory [^src4]. Vector ops are CPU-intensive; plan 2–3× vector-data size in RAM [^src4]. This memory cost is a primary driver of the engine-vs-distributed-DB trade-off in [Vector Database](/ai-engineering/vector-database.md).

## Where embeddings fall short

Embeddings are powerful but lossy, and the corpus documents three recurring failure modes — each pointing to a different page for the fix.

### 1. Exact tokens get smoothed away

Embeddings encode *similarity*, which means precise terms (names, IDs, codes like "SOC 2") get fuzzed into nearby vectors and the literal match is lost [^src6]. A PwC study found plain lexical grep often beats vector search for long-memory conversational QA — by up to 23 points — because the answers hinge on exact entities, names, and dates that appear verbatim; exact string matching nails them while embeddings smooth them into similarity space and miss the literal token [^src6]. The production response is **hybrid search**: blend dense embeddings with sparse keyword (BM25) matching, then re-rank [^src5-rag]. See [Agentic Search](/ai-engineering/agentic-search.md) for the full grep-vs-vector evidence (and the caveat that grep does not always win — semantic generalization is where embeddings earn their keep).

### 2. Embeddings do not encode time

Vectors encode semantics but do not age — an embedding of a quarterly report looks as relevant months later as on release day, and a 2023 and 2025 report can embed near-identically so cosine similarity sees twins [^src5-rag2]. Time is treated as an afterthought in most embedding-based retrieval, producing silent, high-stakes failures [^src5-rag2]. The fix is structural: sparse metadata filters on publication/effective date, temporal query decomposition, and event-driven index invalidation. See [RAG](/ai-engineering/rag.md) §Temporal blind spots.

### 3. Embeddings store facts as disconnected blobs

Plain vector memory also fragments related facts into disconnected chunks: a query surfaces whatever sounds similar without connecting them, so over time a RAG narrative can fragment into "disconnected factoids that can mislead reasoning" [^src5-rag2]. A common structural response is to store entities and typed relationships as a walkable graph rather than inert vectors — the graph-over-flat-vectors idea developed (with its own sources) in [Agent Memory](/ai-engineering/agent-memory.md) and [RAG](/ai-engineering/rag.md) (GraphRAG section).

## DeepMind embeddings research: concept neurons

Google DeepMind's embeddings research (presented by Raia Hadsell, VP Research) explores how embeddings relate to neuroscientific principles of representation [^src8]:

**Jennifer Aniston neurons** — a classic neuroscience finding: individual neurons in the human hippocampus fire specifically for abstract *concepts* (Jennifer Aniston as a person) regardless of how the concept is presented — a photograph, her name written in text, a voice recording. These "concept neurons" are modality-invariant; they encode the concept, not the sensory form [^src8].

DeepMind's embedding research takes this as motivation: ideal learned embeddings should be **modality-invariant** — the same embedding (or a semantically close one) for "Jennifer Aniston" whether the input is an image, text, or audio. This is relevant to multi-modal model training for Gemini [^src8].

**Why it matters for retrieval**: if embeddings are modality-invariant, a text query can retrieve an image result (or vice versa) without a modality bridge; the similarity is in the concept space, not the token space. This is the theoretical foundation for cross-modal RAG [^src8].

Raia Hadsell's role at DeepMind: VP Research, previously known for robotics and continual learning ("CORe50" benchmark; learning without forgetting). The context of this research is embeddings for Gemini's multimodal foundation [^src8].

## The pre-filter rule

The single most impactful optimization when querying embeddings is to **filter by structured metadata *before* doing vector similarity search, not after** — narrowing to the relevant rows first is both faster and more accurate, and the source frames this relational pre-filter not as an optional optimization but as a hard boundary [^src5-rag3]. This is the same scope-before-ranking discipline that governs typed agent memory — filter by scope/tenant, then rank by vector distance. See [RAG](/ai-engineering/rag.md) §Beyond the vector store and [Agent Memory](/ai-engineering/agent-memory.md) §filter by scope before ranking.

## See also

- [Transformer](/ai-engineering/transformer.md) — token embeddings are the input layer; positional encoding adds order separately
- [Vector Database](/ai-engineering/vector-database.md) — how embeddings are indexed (HNSW, C-SPANN), quantized, and queried at scale
- [RAG](/ai-engineering/rag.md) — embeddings power the retrieval half of RAG; hybrid search, temporal blind spots, pre-filter
- [Agentic Search](/ai-engineering/agentic-search.md) — the grep-vs-vector comparison; when exact-token lexical search beats embeddings
- [Agent Memory](/ai-engineering/agent-memory.md) — vector embeddings as the flat-storage layer that temporal graphs improve upon
- [LLM](/ai-engineering/llm.md) — embeddings are the first transformation in the next-token pipeline

---

[^src8]: [How Google DeepMind Is Researching the Next Frontier of AI](../../raw/youtube/youtube-zZsTVBXcbow-how-google-deepmind-is-researching-the-next-frontier-of-ai-f.md) — DeepMind, YouTube; Raia Hadsell on concept neurons and modality-invariant embeddings
[^src1]: [How LLMs Actually Work](../../raw/web/how-llms-actually-work.md)
[^src2]: [AI - How Large Language Models Work](/03_Resources/Study Notes/AI - How Large Language Models Work.md)
[^src3]: [How CockroachDB Built Vector Indexing at Scale](../../raw/web/how-cockroachdb-built-vector-indexing-at-scale.md)
[^src4]: [Vector Search in Manticore Search: A Deep Dive](../../raw/web/vector-search-in-manticore-search-a-deep-dive.md)
[^src5-rag]: [AI Tools - Local RAG Complete Tutorial](/03_Resources/Study Notes/AI Tools - Local RAG Complete Tutorial.md)
[^src5-rag2]: [7 Temporal Blind Spots Breaking Enterprise RAG](../../raw/web/7-temporal-blind-spots-breaking-enterprise-rag-news-from-gen.md)
[^src5-rag3]: [Beyond the Vector Store: Building the Full Data Layer for AI](../../raw/web/web-beyond-the-vector-store-building-the-full-data-layer-for-ai.md) — Kevin Smith, Saturn Cloud blog
[^src6]: [Is Grep All You Need? The Harness Matters More Than the Search](../../raw/web/is-grep-all-you-need-the-harness-matters-more-than-the-searc.md)
