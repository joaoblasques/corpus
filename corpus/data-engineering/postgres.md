---
type: entity
domain: data-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/Data Engineering - Just Use Postgres.md
    channel: notes
    ingested_at: 2026-05-21
aliases:
  - PostgreSQL
  - Postgres
  - postgres
tags:
  - corpus/data-engineering
  - entity
created: 2026-05-21
updated: 2026-06-16
---

# PostgreSQL (Postgres)

**TL;DR**: A relational database that doubles as a full-stack data platform via extensions — covering caching, vector search, full-text search, real-time sync, auth, and analytics without additional services [^src1].

## Extensions as a platform strategy

Rather than defaulting to multiple specialized services, Postgres extensions can cover most data needs [^src1]:

| Need | Extension / Feature |
|---|---|
| Unstructured / NoSQL data | `JSONB` — queryable dynamic data within SQL |
| Cron / scheduled jobs | `pgcron` — schedule SQL queries directly |
| In-memory cache | Unlogged tables — skip disk writes |
| Vector search (AI/RAG) | `pgvector` — embeddings + nearest-neighbor search |
| Full-text + fuzzy search | `tsvector` — ranked results, typo tolerance |
| GraphQL API | `pg_graphql` — tables to GraphQL, no server |
| Real-time frontend sync | `ElectricSQL` — wraps Postgres |
| Auth (hashing, JWTs, RLS) | `pgcrypto` + `pgjwt` + row-level security |
| Analytics / columnar | `pgmeta` + DuckDB-style column storage |

## When to apply this

- MVPs and side projects where infrastructure cost predictability matters
- Teams reaching for 5+ separate services that Postgres extensions could replace
- Before defaulting to microservices complexity: "Why not Postgres first?" [^src1]

This is not a universal answer — at large scale or with specialized access patterns, purpose-built tools win. But the question is worth asking first.

## Hosting

**Neon** — serverless Postgres with branching, automatic scaling, and sane pricing. Suited for both prototypes and production [^src1].

## Note on `pgvector`

`pgvector` makes Postgres a viable option as a [[ai-engineering/vector-database|vector database]] for RAG pipelines at moderate scale. See [[ai-engineering/rag|RAG]] for the retrieval architecture context.

## See also

- [[data-engineering/postgresql-views|PostgreSQL Views]] — views as rewrite-rule macros; the `SELECT *` trap, `security_invoker`/RLS, schema-evolution pain
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [[03_Resources/Study Notes/Data Engineering - Just Use Postgres|Data Engineering - Just Use Postgres]]
