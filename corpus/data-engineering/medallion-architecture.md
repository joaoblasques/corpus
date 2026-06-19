---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2025-09-08-medallion-architecture-is-not-a-data-model.md
    channel: inbox
    ingested_at: 2026-06-11
  - path: raw/web/data-identity-politics-and-the-kimball-vs-inmon-war.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/email/email-2025-11-20-the-medallion-data-architecture-pros-cons.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/email/email-2025-04-16-understanding-the-t-in-etl-a-back-to-basics-guide-to-data-tr.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - medallion
  - bronze silver gold
  - medallion architecture
  - bronze/silver/gold
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-11
updated: 2026-06-19
---

# Medallion Architecture

**TL;DR.** Medallion (bronze → silver → gold) is a set of **data lifecycle stages**, not a data model. Popularized by Databricks in the early 2020s, it describes how data is progressively refined as it traverses an analytical pipeline, usually under ELT [^src1]. The stages are **model-agnostic**: at no point does the medallion prescribe how data is modeled (star schema, Data Vault, 3NF, OBT, etc.) [^src1]. Medallion owns the *pipeline*; data modeling owns the *entities, grain, and keys*. They are orthogonal concerns [^src1]. In the modern lakehouse, the Kimball-vs-Inmon debate dissolves into a synthesis: Inmon-style governance for raw/bronze layers, Kimball-style dimensional models for gold/serving [^src2].

A common practitioner pain point reinforces the "lifecycle not model" framing: teams struggle to implement medallion correctly — unsure which logic belongs in which layer, or letting naming drift until the scheme is more complicated than it needs to be [^src3].

## The three stages

Each stage removes complexity for an increasingly broader, less technical audience: bronze (primarily technical) → silver (less technical) → gold (non-technical/business) [^src1].

- **Bronze — raw ingestion.** Append-only files or tables, minimal transformation, schema drift tolerated, heavy lineage focus [^src1]. A typical bronze source is a set of [[data-engineering/change-data-capture|CDC]] streams off the OLTP database, "warts and all" — duplicates, late-arriving records, soft deletes [^src1].
- **Silver — cleansed and conformed.** De-duplicated, typed, standardized IDs, business keys resolved, quality rules enforced [^src1]. Tables like `orders_clean` (order-line grain, de-duped), `customers_clean` (business keys resolved) [^src1].
- **Gold — business-ready.** Data modeled specifically for consumption: dashboards, reports, self-serve analytics [^src1].

Variations of the same pattern predate the medallion naming: Landing → Curated → Serving; Staging → Data Mart [^src1]. The intent is identical: progressively refine data so it is more useful for specific use cases [^src1].

From the transform-layer perspective, medallion (Databricks-popularized) is explicitly a **rename of the long-standing raw/stage/prod three-layer transform pattern** — one of two later approaches that "co-opted and renamed those layers," the other being how dbt projects are structured [^src4]. Its biggest advantage is often that the naming makes it easier for the business to understand what the data team is talking about [^src4]. Per that source, mapping onto the three layers [^src4]: **bronze** = raw or minimally cleaned data left "as-is" (equivalent to raw tables); **silver** = standardized and enriched data combining multiple bronze sources — *"The Silver layer brings the data from different sources into an Enterprise view and enables self-service analytics for ad-hoc reporting, advanced analytics and ML"* (Databricks); **gold** = business-level aggregates and reporting tables powering dashboards, KPIs, and executive reports — Databricks' *"consumption-ready 'project-specific' databases."* See [[data-engineering/data-transformation|Data Transformation]] for the transform-layer framing.

## Medallion is NOT a data model

This is the load-bearing claim of the primary source: *"The Medallion architecture is no more a data model approach than a parking lot is a type of car."* [^src1] The two are inverse processes serving a common goal:

- Data **simplifies** for the end-user as it moves bronze → gold (raw JSON → clean queryable table) [^src1].
- A data **model grows more complex** and specific as it moves conceptual → logical → physical (whiteboard sketch → DDL script) [^src1].

A data model answers questions the medallion stages never touch: What is a Customer, and how do we identify one? What is the grain of Orders — order, order line, or shipment? Which attributes are slowly changing? Where do constraints live? [^src1] *"None of these decisions is implied by Bronze vs Silver vs Gold. They're orthogonal to data modeling."* [^src1] See [[data-engineering/dimensional-modeling|dimensional modeling]] for the modeling concerns themselves.

### Who owns what

- **Medallion owns the pipeline**: ingestion patterns, file formats, schema-change handling between stages, orchestration, data quality checks [^src1].
- **Modeling owns the entities**: attributes, relationships, grain; the choice to normalize or denormalize; naming standards and semantic consistency [^src1].

> *"Medallion does not decide the data model, nor does the data model decide the data pipeline."* [^src1]

## "Gold = star schema"? Not necessarily

A common confusion is asserting gold is a star schema. Gold is simply business-ready data — historically the **data mart** (c. 1994), which can be modeled however the consumer needs [^src1]. The same bronze → silver → gold pipeline for a fictitious retailer (Customers, Orders, Products) can publish gold in several shapes [^src1]:

- **Star**: `fact_orders` (order-line grain), `dim_customer` ([[data-engineering/scd2|SCD2]]), `dim_product` (SCD1), optimized for BI slice-and-dice [^src1].
- **OBT (One Big Table)**: `orders_enriched` with ~69 flattened attributes for a fixed-question dashboard [^src1].
- **Data Vault → Data Mart**: Hubs/Links/Satellites in silver for lineage and history, publishing a star or OBT to gold [^src1].
- **ML features**: e.g. `customer_90d_order_count`, `avg_item_price_30d`, `days_since_last_order` [^src1].

There is no single best way to model gold (or any stage) — pick the approach that best serves the consumer [^src1].

## Can you skip silver (bronze → gold)?

In practice, yes — but the silver transformations (deduping, conforming attributes) will likely appear in your workflow regardless. Silver provides an opportunity to persist data at an intermediate stage [^src1]. This bronze→silver→gold staging is the lakehouse expression of the same idea as [[data-engineering/pipeline-layers|pipeline layers]].

## The Kimball-vs-Inmon war (and its resolution)

The Kimball-vs-Inmon "wars" are industry legend, fought from the 1990s/2000s [^src2]. Per the synthesis source (Joe Reis relaying Bill Inmon), the conflict was **not between Ralph Kimball and Bill Inmon personally** — they had no personal issues — but **between their disciples**, and the core dispute was over **ownership of the term "data warehouse"**; the secondary war was which architecture/methodology was superior [^src2].

Why no equivalent wars today? Fewer big ideas held practitioner mindshare back then, so you were expected to pick a side ("data identity politics"); the news cycle was slower (print/early online, no social media); and today's rapid permutation of formats and AI makes sustained obsession over one issue unlikely [^src2].

**The resolution — synthesis, not victory.** The industry chose **both**: *"modern Lakehouse architectures can use Inmon-style governance for the raw/bronze layers and Kimball-style dimensional models for the gold/serving layers."* [^src2] The winner was not Bill or Ralph but the **synthesis and adoption of their ideas** [^src2]. This maps cleanly onto medallion: Inmon-style integrated/governed raw at bronze, Kimball-style [[data-engineering/dimensional-modeling|dimensional models]] at gold.

## Gotchas

- Treating bronze/silver/gold as data models leads teams to debate colors when they should agree on grain, keys, and definitions — or to debate column-level semantics when the topic is orchestration [^src1].
- The confusion is *not* pedantic bikeshedding; it reflects a genuine gap in data-modeling knowledge among data engineers who over-focus on pipelines (moving data A→B) [^src1].
- "Is medallion truly an *architecture*?" is a separate debate the source declines; the practical point stands regardless [^src1].

[^src1]: [Medallion Architecture is NOT a Data Model](../../raw/email/email-2025-09-08-medallion-architecture-is-not-a-data-model.md)
[^src2]: [Data Identity Politics and The Kimball vs. Inmon War](../../raw/web/data-identity-politics-and-the-kimball-vs-inmon-war.md)
[^src3]: [The Medallion Data Architecture (Pros & Cons) (KahanDataSolutions)](../../raw/email/email-2025-11-20-the-medallion-data-architecture-pros-cons.md)
[^src4]: [Understanding the "T" in ETL: A Back-to-Basics Guide to Data Transformations](../../raw/email/email-2025-04-16-understanding-the-t-in-etl-a-back-to-basics-guide-to-data-tr.md)
