---
type: entity
domain: data-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/Data Engineering - Just Use Postgres.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/github/github-pgr0ss-pgledger.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - PostgreSQL
  - Postgres
  - postgres
  - pgledger
  - double-entry ledger PostgreSQL
tags:
  - corpus/data-engineering
  - entity
created: 2026-05-21
updated: 2026-06-25
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

## PostgreSQL as a financial ledger (pgledger)

A lesser-known but powerful Postgres use case: **double-entry bookkeeping** implemented entirely in the database as SQL functions and views [^src2]. The `pgledger` project (pgr0ss, Go, ★474, Apache 2.0) demonstrates this pattern:

- **The primitive**: a ledger is a fundamental building block of any money-managing software — "it's incredibly important to know what money is where, how it got there, and what it's for" — yet most companies build it from scratch every time [^src2].
- **Why Postgres-native works**: the entire ledger is SQL tables, functions, and views; the application calls SQL functions and queries data via SQL views. No application-level code needed [^src2].
- **Transactional integrity**: because pgledger lives in Postgres, ledger writes are **atomic with the rest of the application** — "do some work, write to the ledger, and it all commits or doesn't atomically." Cross-service synchronization problems disappear when the ledger is in the same DB as the business logic [^src2].
- **API surface**: `pgledger_create_account(name, currency)` → returns account ID; `pgledger_transfer(...)` → debits one account and credits another in one atomic operation; queryable views expose balances and ledger history [^src2].
- **Installation**: single SQL file (`pgledger.sql`) plus ULID/UUID helper functions; integrates with any migration tool [^src2].

**Pattern implications for data engineers**: a financial audit log modeled as a double-entry ledger in Postgres is queryable, atomic, and avoids the consistency problems of application-level ledger logic. Combine with `pgcron` (scheduled reconciliation), `pg_audit` (change logging), and JSONB (flexible metadata) to build a full financial data platform without a separate ledger service.

## See also

- [[data-engineering/postgresql-views|PostgreSQL Views]] — views as rewrite-rule macros; the `SELECT *` trap, `security_invoker`/RLS, schema-evolution pain
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [[03_Resources/Study Notes/Data Engineering - Just Use Postgres|Data Engineering - Just Use Postgres]]
[^src2]: [pgledger — double-entry ledger implementation in PostgreSQL (pgr0ss/pgledger)](../../raw/github/github-pgr0ss-pgledger.md)
