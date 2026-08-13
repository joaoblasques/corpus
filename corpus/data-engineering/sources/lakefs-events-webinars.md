---
type: source
domain: data-engineering
status: stub
sources:
  - path: raw/_inbox/web-trust-isolation-and-reproducibility-for-agentic-ai-a8431426.md
    channel: web
    ingested_at: 2026-08-13
  - path: raw/_inbox/web-why-data-is-killing-your-ai-project-and-what-to-do-about-it-4c2deb2c.md
    channel: web
    ingested_at: 2026-08-13
  - path: raw/_inbox/web-scaling-a-data-lake-with-lakefs-best-practices-e0da2b52.md
    channel: web
    ingested_at: 2026-08-13
  - path: raw/_inbox/web-develop-spark-etl-pipelines-without-production-risk-4cb0d278.md
    channel: web
    ingested_at: 2026-08-13
  - path: raw/_inbox/web-optimize-object-storage-for-data-with-lakefs-dataops-poland-8eedb8f4.md
    channel: web
    ingested_at: 2026-08-13
  - path: raw/_inbox/web-a-new-chapter-for-dvc-passing-the-torch-to-lakefs-14e6f69f.md
    channel: web
    ingested_at: 2026-08-13
  - path: raw/_inbox/web-odsc-east-2026-networking-meetup-d01e349e.md
    channel: web
    ingested_at: 2026-08-13
  - path: raw/_inbox/web-subsurface-rethinking-ingestion-ci-cd-for-data-lakes-37f132f1.md
    channel: web
    ingested_at: 2026-08-13
  - path: raw/_inbox/web-what-s-the-future-of-metadata-after-hive-metastore-f6dec2cb.md
    channel: web
    ingested_at: 2026-08-13
aliases:
  - lakeFS webinars
  - lakeFS events
tags:
  - corpus/data-engineering
  - source
  - lakefs
  - data-version-control
  - data-lake
  - webinar
created: 2026-08-13
updated: 2026-08-13
---

# lakeFS Events and Webinars

TL;DR: Collection of lakeFS webinar landing pages and event descriptions covering data lake management, agentic AI data governance, Spark ETL isolation, and CI/CD for data lakes.

## Key Themes Across Events [^events]

**Agentic AI data readiness**: "97% of organizations report active AI initiatives, but only 5% say their data is adequately ready to support them" (Dun & Bradstreet AI Momentum Survey). The core lakeFS argument is that agents as a new class of data consumer require branch-isolated, auditable, reproducible data access — governance built for human-driven workflows does not close the gap.[^agentic]

**Data bottlenecks kill AI projects**: "83% of enterprises" cite broken data infrastructure (not compute or algorithms) as the top killer of AI projects. lakeFS frames data version control as the fix: treating data like code (branch/commit/merge) transforms chaos into repeatable, industrialized data pipelines.[^bottlenecks]

**Data lake best practices (scale)**: Three strategies for managing large-scale data lakes:[^scaling]
1. **Isolated Ingestion** — each ingestion pipeline works on its own branch, avoiding conflicts
2. **CI/CD data deployment** — data changes go through a review/test gate before merging to production
3. **Dataset Versioning** — reproducible snapshots of entire datasets at any point in time

**Spark ETL without production risk**: Standard ETL testing problem — testing on a sample is insufficient; creating full copies of production data is expensive. lakeFS zero-copy branches provide the full production dataset at metadata cost, enabling isolated test environments for end-to-end pipeline testing.[^spark] Workflow: set up environment → integrate lakeFS + Spark → execute git-like operations (commit, branch, revert) via the lakeFS Python client.

**DVC → lakeFS transition (Dec 2025)**: DVC co-founder Dmitry Petrov (DataChain Inc.) and lakeFS CTO Oz Katz discussed DVC "passing the torch" to lakeFS for data version control. DVC tracks data versions via metadata in Git (suited for ML experiment tracking); lakeFS operates at the object storage layer for large-scale, multi-user concurrent workloads.[^dvc]

**Hive Metastore future**: Industry panel on Hive Metastore's role in modern data stacks. Context: the two-part lakeFS blog series on Hive Metastore prompted an expert panel on what comes after it — Delta Lake, Iceberg REST Catalog, Unity Catalog, and open metastore alternatives.

## Cross-links

- [/data-engineering/lakefs.md](/data-engineering/lakefs.md) — main lakeFS entity page with architecture and use cases
- [/data-engineering/databricks.md](/data-engineering/databricks.md) — Unity Catalog comparison
- [/data-engineering/open-table-formats.md](/data-engineering/open-table-formats.md) — Hive Metastore and its successors

---

[^events]: Aggregated from lakeFS event/webinar landing pages — raw/_inbox/ (trust-isolation, data-killing-ai, scaling-data-lake, develop-spark-etl, optimize-object-storage, dvc-torch, odsc-meetup, subsurface, hive-metastore)
[^agentic]: raw/_inbox/web-trust-isolation-and-reproducibility-for-agentic-ai-a8431426.md
[^bottlenecks]: raw/_inbox/web-why-data-is-killing-your-ai-project-and-what-to-do-about-it-4c2deb2c.md
[^scaling]: raw/_inbox/web-scaling-a-data-lake-with-lakefs-best-practices-e0da2b52.md
[^spark]: raw/_inbox/web-develop-spark-etl-pipelines-without-production-risk-4cb0d278.md
[^dvc]: raw/_inbox/web-a-new-chapter-for-dvc-passing-the-torch-to-lakefs-14e6f69f.md
