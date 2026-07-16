---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-09.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-10.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-11.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-12.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-13.md
    channel: pdf
    ingested_at: 2026-07-16
  - path: raw/_inbox/pdf-data-mining-concepts-and-techniques-part-14.md
    channel: pdf
    ingested_at: 2026-07-16
aliases:
  - Online Analytical Processing
  - data cube
  - OLAP cube
  - multidimensional analysis
  - star schema
  - snowflake schema
  - data warehouse
tags:
  - corpus/data-engineering
  - concept
created: 2026-07-16
updated: 2026-07-16
---

# OLAP and Data Warehousing

TL;DR: OLAP (Online Analytical Processing) enables interactive multidimensional analysis of large datasets stored in data warehouses. The core abstraction is the **data cube** — a pre-aggregated, multidimensional structure that allows drill-down, roll-up, slice, and dice operations at interactive speeds. Schema design (star, snowflake, galaxy) and materialization strategy (full vs. partial vs. iceberg) are the primary engineering decisions.

## Data Warehouse Concepts

A **data warehouse** is a subject-oriented, integrated, time-variant, nonvolatile data collection organized for management decision making [^src1]. It contrasts with operational (OLTP) databases:

| | OLTP | OLAP/Warehouse |
|---|---|---|
| Purpose | Day-to-day transactions | Historical analysis |
| Update | Continuous reads/writes | Periodic bulk loads |
| Query | Simple, predefined | Complex, ad hoc |
| Data scope | Current, detailed | Historical, summarized |
| Schema | Normalized (3NF) | Denormalized (star/snowflake) |

A **three-tier architecture** is typical: bottom tier = relational warehouse DB; middle tier = OLAP server (ROLAP or MOLAP); top tier = client query/reporting tools [^src1].

## Schema Designs

### Star Schema

The simplest and most common form. One central **fact table** records measurements (metrics); surrounding **dimension tables** hold descriptive attributes [^src1]:

```
          time_dim        item_dim
              \               /
               \             /
          [FACT TABLE: sales]
               /             \
              /               \
         branch_dim       location_dim
```

Fact table rows: `(time_key, item_key, branch_key, location_key, dollars_sold, units_sold)`.

Each dimension table holds all attributes of that dimension in a single denormalized table — simple to query, faster joins, but introduces redundancy.

### Snowflake Schema

A normalization of the star schema where dimension tables are split into multiple related tables. The _location_ dimension might split into a `city` table linked from the main `location` table [^src1].

Trade-off: reduces storage redundancy but increases join complexity and typically **hurts query performance** — most systems prefer the star schema.

### Galaxy / Fact Constellation Schema

Multiple fact tables sharing dimension tables. Used for enterprise-wide data warehouses with related subjects (e.g., both a `sales` fact table and a `shipping` fact table share `time`, `item`, and `location` dimensions) [^src1].

## The Data Cube

A **data cube** is the core OLAP data structure. Given a fact table with n dimensions, the cube computes aggregates over every possible combination of dimension subsets (the **lattice of cuboids**) [^src2].

For a 3-D cube over dimensions {A, B, C}:
- Base cuboid: `ABC` (the full detail)
- 2-D cuboids: `AB`, `AC`, `BC`
- 1-D cuboids: `A`, `B`, `C`
- 0-D apex cuboid: `all` (total aggregate)

This lattice has 2^n cuboids for n dimensions.

### OLAP Operations

| Operation | Effect |
|---|---|
| **Roll-up** (drill-up) | Aggregate to a higher abstraction level (e.g., city → country) |
| **Drill-down** | Navigate from summary to detail (country → city → street) |
| **Slice** | Select a single value on one dimension (e.g., `time = Q1`) |
| **Dice** | Select ranges on multiple dimensions simultaneously |
| **Pivot** (rotate) | Reorient the data presentation |

### Concept Hierarchies

Dimension attributes form hierarchies used during roll-up/drill-down: `street < city < province < country` for location; `day < week < month < quarter < year` for time [^src1]. Sometimes the hierarchy is a lattice (partial order), not a total order.

## Cube Materialization Strategies

### No Materialization

Compute aggregates on-the-fly from the base cuboid. Extremely slow for ad hoc queries over large data.

### Full Materialization

Precompute all 2^n cuboids. Fast queries but exponential storage.

### Partial Materialization

Precompute a selected subset of cuboids. The main engineering challenge is choosing *which* cuboids to materialize based on query workload, access costs, and storage constraints [^src2].

**Iceberg cube**: only store cells with an aggregate value above a minimum support threshold. Eliminates the vast majority of sparse cells [^src2].

**Shell cube**: precompute cuboids for only a small number of dimensions (3–5). Queries on remaining dimension combinations compute on-the-fly. Good for very high-dimensional fact tables.

## Indexing OLAP Data

**Bitmap index**: for each attribute value, stores a bit vector with 1s in positions where that value occurs. Queries reduce to bitwise AND/OR — fast for low-cardinality dimensions [^src2].

**Join index**: precomputes which fact table rows join to which dimension values, eliminating expensive joins at query time. Especially useful in star schema where every query involves star joins [^src2].

## Data Cube Computation Methods (Ch. 5)

The base `ABC` cuboid can be computed by grouping and sorting. Efficient computation of all cuboids requires minimizing redundant scans.

**Multiway array aggregation**: partition the data array into chunks that fit in memory. Aggregate simultaneously across multiple dimensions within each chunk, sharing intermediate computations. Reduces I/O compared to sequential per-dimension passes [^src3].

**BUC (Bottom-Up Computation)**: generates the iceberg cube top-down, pruning branches where the aggregate count would fall below the minimum support threshold (Apriori-style antimonotonicity) [^src3].

**Shell-fragment approach**: for very high-dimensional data, precompute partial 2–3 dimension cuboids (shell fragments). Complex multi-dimensional aggregations are then composed on-the-fly from these fragments, with the fragment stored as an ID-measure array rather than full tuple data — more compact [^src3].

## Multidimensional Data Mining in Cube Space

**Attribute-oriented induction (AOI)**: generalize data from detail to higher conceptual levels using concept hierarchies. Does NOT require precomputing a full cube — runs online on a given query's result set. Useful for characterization and discrimination tasks [^src4].

**Discovery-driven exploration**: automated significance scores for each cell in a data cube — flags "interesting" cells whose deviation from an expected value exceeds a threshold. Allows analysts to focus on anomalies rather than brute-force browsing [^src5].

## Relationship to Corpus Pages

- Schema design details: [/data-engineering/dimensional-modeling.md](/data-engineering/dimensional-modeling.md)
- Data lake and warehouse integration: [/data-engineering/data-lake.md](/data-engineering/data-lake.md)
- Data mart concepts: [/data-engineering/data-mart.md](/data-engineering/data-mart.md)
- Materialized views (same idea applied in databases): [/data-engineering/materialized-views.md](/data-engineering/materialized-views.md)
- Full data mining context: [/data-engineering/data-mining.md](/data-engineering/data-mining.md)

---

[^src1]: [Data Mining: C&T Part 9 — Ch. 4 Data Warehousing and OLAP, star/snowflake/galaxy schemas](../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-09.md)
[^src2]: [Data Mining: C&T Part 10 — Ch. 4 OLAP implementation, partial materialization, bitmap/join indexes](../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-10.md)
[^src3]: [Data Mining: C&T Part 12 — Ch. 5 Data Cube computation (multiway array aggregation)](../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-12.md)
[^src4]: [Data Mining: C&T Part 11 — Ch. 4 attribute-oriented induction, OLAP summary](../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-11.md)
[^src5]: [Data Mining: C&T Part 14 — Ch. 5 multifeature cubes, discovery-driven exploration](../../raw/pdf/pdf-data-mining-concepts-and-techniques-part-14.md)
