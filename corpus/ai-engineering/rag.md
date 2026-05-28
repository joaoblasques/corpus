---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/AI Tools - Local RAG Complete Tutorial.md
    channel: notes
    ingested_at: 2026-05-21
aliases:
  - RAG
  - retrieval-augmented generation
  - retrieval augmented generation
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-21
updated: 2026-05-21
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
- [[ai-engineering/agent-evaluation|Agent Evaluation]] — retrieval quality as a measured metric

---

[^src1]: [[03_Resources/Study Notes/AI Tools - Local RAG Complete Tutorial|AI Tools - Local RAG Complete Tutorial]]
