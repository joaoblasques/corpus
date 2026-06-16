---
type: entity
domain: data-engineering
status: draft
sources:
  - path: raw/web/github-bruin-data-ingestr-ingestr-is-a-cli-tool-to-copy-data.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/email/email-2026-06-04-dbt-core-v2-alpha-cart-prediction-with-llms-ray-vs-daft.md
    channel: email
    ingested_at: 2026-06-15
aliases:
  - ingestr
  - bruin ingestr
tags:
  - corpus/data-engineering
  - entity
created: 2026-06-15
updated: 2026-06-16
---

# ingestr

**TL;DR.** `ingestr` (by Bruin) is a **CLI ELT tool that copies data from any source into any destination using simple command-line flags — no code, no backend** [^src1]. Single-command install; broad connector coverage (databases + SaaS platforms) and incremental loading [^src1]. Positioned as the lightweight "EL" of the modern stack — move data with one command, then transform with [[data-engineering/dbt|dbt]] [^src2].

## What it does

One command copies a table from source to destination [^src1]:

```bash
ingestr ingest \
  --source-uri 'postgresql://admin:admin@localhost:8837/web' \
  --source-table 'public.some_data' \
  --dest-uri 'bigquery://<project>?credentials_path=/path/sa.json' \
  --dest-table 'ingestr.some_data'
```

- **Incremental loading** — `append`, `merge`, or `delete+insert` strategies [^src1].
- **Python SDK** — `ingestr.ingest(data, dest_uri=..., dest_table=...)` accepts rows, generators, and DataFrames; data is sent to the bundled binary as **Arrow IPC streams** by default (or `mmap` Arrow IPC files for very large materialised data) [^src1]. Push-style usage via a context manager; full CLI pass-through via `ingestr.run(...)` [^src1].

## Connectors

Databases (source ↔ dest): Athena, Redshift, ClickHouse, Databricks, [[data-engineering/duckdb|DuckDB]], BigQuery, [[data-engineering/postgres|Postgres]], MySQL, SQL Server, MongoDB, Snowflake, SQLite, Trino, MotherDuck, plus [[data-engineering/kafka|Kafka]] (source) [^src1]. Platforms (source-only): Stripe, HubSpot, Salesforce, GitHub, Notion, Google Ads/Analytics/Sheets, Shopify, Slack, Zendesk, and dozens more [^src1].

## Licensing

Source-available under the **Functional Source License 1.1** (free for internal production, dev, testing, education, research, professional services; cannot be used to offer a competing commercial ingestion/ELT product); each version becomes **Apache 2.0 two years after release** [^src1].

## Where it fits

ingestr is the **extract-and-load** stage feeding a warehouse/lake that [[data-engineering/dbt|dbt]] then transforms — the same EL→T separation in [[data-engineering/pipeline-layers|pipeline layers]]. Compare with full-load/incremental/CDC trade-offs in [[data-engineering/data-ingestion-patterns|data ingestion patterns]] and [[data-engineering/change-data-capture|CDC]].

## Related

- [[data-engineering/data-ingestion-patterns|Data Ingestion Patterns]] · [[data-engineering/change-data-capture|Change Data Capture]]
- [[data-engineering/dbt|dbt]] — the transform stage after EL
- [[data-engineering/incremental-pipeline-design|Incremental Pipeline Design]]
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [bruin-data/ingestr — CLI tool to copy data](../../raw/web/github-bruin-data-ingestr-ingestr-is-a-cli-tool-to-copy-data.md)
[^src2]: [TLDR Data — dbt Core v2 Alpha / Ray vs Daft (newsletter)](../../raw/email/email-2026-06-04-dbt-core-v2-alpha-cart-prediction-with-llms-ray-vs-daft.md)
