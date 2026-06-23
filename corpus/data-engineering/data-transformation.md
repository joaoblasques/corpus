---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2025-04-16-understanding-the-t-in-etl-a-back-to-basics-guide-to-data-tr.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - data transformation
  - the T in ETL
  - the T in ELT
  - transform step
  - transform layer
  - SQL transformations
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-19
updated: 2026-06-23
---

# Data Transformation (the "T" in ETL/ELT)

**TL;DR.** The transform step is where raw data gets standardized, integrated, and turned into something accessible to analysts and the business [^src1]. Analytics and data engineers spend much of their time here, whether standardizing inputs or layering in business logic [^src1]. The "T" exists to solve four core problems — **business logic, standardization, data integration, and pre-aggregation** [^src1] — historically handled by hand-built stored procs / SSIS / cron and now by transform-focused tools like [[data-engineering/dbt|dbt]] (also SQLMesh and [[data-engineering/dataform|Dataform]]) [^src1]. The transform layer is itself a place messiness creeps back in (3000-line queries, dependency sprawl, unclear ownership), so it deserves real structure — typically a raw/stage/prod or [[data-engineering/medallion-architecture|bronze/silver/gold]] layering [^src1].

## What "transform" actually solves

The transform step depends on stack and use case, but exists to solve a few core problems [^src1]:

- **Business logic** — rules and definitions that make data useful to the business. Example: for a retailer, returns and purchases may live in different tables, or a return is only flagged in a field while its value is stored positive — so you build a process to accurately calculate total amount purchased [^src1].
- **Standardization** — every system has its own naming conventions, date formats, IDs, and categories; standardizing them as you build the data model makes it far easier for downstream users to work with consistent categories and names [^src1].
- **Data integration** — a core goal of a warehouse is to let end-users join datasets from different sources (CRM ↔ billing ↔ ERP). There's usually no magic join, so you integrate either at the application layer or in the warehouse, creating an ID that lets you join the information [^src1].
- **Pre-aggregation** — for metrics at scale it's often more efficient to pre-aggregate, so dashboards don't take minutes to load when end-users query [^src1].

## How transforms used to be done (and often still are)

Before modern tooling, transforms were either a homegrown system engineers built or an out-of-the-box low-code/drag-and-drop tool (e.g. SSIS) [^src1]. A homegrown solution typically meant [^src1]:

- Stored procedures or SQL scripts in the warehouse
- Python or Bash scripts to execute them
- Cron jobs, Task Scheduler, SQL Server Agent, Jenkins — "pick your scheduler poison"

This works, but with limitations depending on how it's set up. A recurring pain is the lack of an easy way to integrate stored procedures with **version control** — at one of the author's early companies they had to both push code into the repo *and* manually change it on the database, creating a real risk of pushing different code to the two locations [^src1].

## The rise of transform-focused tools

[[data-engineering/dbt|dbt]] wasn't the first transform tool — there were earlier drag-and-drop-plus-SQL platforms — but many companies adopted it, especially at startups during the **MDS (Modern Data Stack) boom of the early 2020s** [^src1]. It stood out because it embraced **version control, modular SQL, testing, and documentation**, and made SQL-based workflows accessible to a broader set of users [^src1]. It is not the only option: **SQLMesh** and [[data-engineering/dataform|Dataform]] are alternative SQL-based transform tools [^src1].

## Common transform types (with SQL)

### Value standardization (CASE / lookup table)

Systems often label the same concept differently; standardize them into one value. A `CASE` statement works when you have a few categories; with hundreds of values a **lookup table** is the better long-term strategy [^src1]. Given System A (`active`, `cancelled`, `trial`) and System B (`ACT`, `CXL`, `TRIAL_PERIOD`) [^src1]:

```sql
CASE
  WHEN status IN ('active', 'ACT') THEN 'active'
  WHEN status IN ('cancelled', 'CXL') THEN 'cancelled'
  WHEN status IN ('trial', 'TRIAL_PERIOD') THEN 'trial'
  ELSE 'unknown'
END AS standardized_status
```

This keeps downstream metrics and filters consistent regardless of source format [^src1].

### Data-type standardization (CAST, text-bool → bool)

Data from APIs or SFTP may arrive as numbers-as-strings, dates-as-text, booleans-as-"Yes"/"No" — clean it up so types match what's expected (avoiding five different date formats in the warehouse) [^src1]:

```sql
SELECT
  CAST(order_total AS NUMERIC) AS order_total,
  CAST(order_date  AS DATE)    AS order_date,
  LOWER(email)                 AS email
FROM raw.orders
```

```sql
CASE
  WHEN is_active = 'Yes' THEN TRUE
  WHEN is_active = 'No'  THEN FALSE
  ELSE NULL
END AS is_active
```

### Categorization for reporting

For reporting or segmentation you often add categories not present in the source — e.g. flagging `high_value` customers (which wouldn't exist in a POS but is useful for reporting/retargeting) [^src1]:

```sql
WITH recent_spending AS (
  SELECT customer_id, SUM(order_amount) AS total_spent
  FROM orders
  WHERE order_date >= DATEADD(MONTH, -6, CURRENT_DATE)
  GROUP BY customer_id
)
SELECT
  customer_id,
  total_spent,
  CASE WHEN total_spent >= 1000 THEN 'high_value' ELSE 'regular' END AS customer_segment
FROM recent_spending;
```

## Challenges with the transform layer

Even with tooling like dbt, the "T" layer can become as messy as the raw data it was meant to clean [^src1]:

- **3000-line queries.** Transform models grow organically — someone needs a metric, tacks on another CTE or join, repeat, and you get a *"3000-line SQL file, 17 CTEs deep, with a bunch of CASE WHEN logic buried in subqueries"* that technically works but nobody wants to touch [^src1]. The choice of *how* to structure those intermediate steps (CTE vs view vs temp table vs materialized view) is the subject of [[data-engineering/sql-intermediate-results|Storing Intermediate Results in SQL]].
- **Dependency sprawl.** The more models depend on each other, the more fragile things get; small upstream changes ripple downstream and break dashboards in non-obvious ways. Without clear lineage/dependency mapping you get a fragile system [^src1].
- **Lack of ownership.** In a "move fast" data world, engineers, analytics engineers, and even analysts all build transforms — so who owns the definitions, cleans up deprecated models, gets final say on business logic? Without clear ownership, speed eventually bites [^src1].

## Organizing the transform layer

To avoid chaos the transform logic needs structure. The author's original layering was **raw / stage / prod** ("prod" being a poor name if you also have dev/prod deployment environments) [^src1]. Two later approaches co-opted and renamed those same layers — what you encounter through [[data-engineering/dbt|dbt]] projects or the medallion architecture [^src1]:

- **Medallion** (Databricks-popularized) maps onto the same long-standing three-layer pattern: **bronze** = raw / as-is, **silver** = standardized/enriched (an enterprise view enabling self-service analytics/ML), **gold** = business-level aggregates/consumption-ready tables for dashboards and KPIs [^src1]. See [[data-engineering/medallion-architecture|Medallion Architecture]] for why these are lifecycle stages, not a data model.

## Other considerations

- **Data quality.** Each transform/SQL script is another opportunity to introduce errors, so unit tests and DQ checks *"aren't just nice to have, they're essential for catching issues before they hit production"* [^src1]. See [[data-engineering/data-quality|Data Quality]].
- **Ownership boundaries.** Tools like dbt broadened who can build platform layers — great for speed and collaboration, but it blurs where ownership of the core warehouse ends and use-case-specific layers begin [^src1].
- **Developer experience.** How safely can you develop and test changes? Pushing straight to production with no staging or review may be fine solo but is "a recipe for broken pipelines" in a shared, multi-dependency environment [^src1].

## See also

- [[data-engineering/dbt|dbt]] — the dominant transform-focused tool (modular SQL, version control, testing)
- [[data-engineering/dataform|Dataform]] — BigQuery-native SQL transform alternative (also SQLMesh)
- [[data-engineering/medallion-architecture|Medallion Architecture]] — bronze/silver/gold layering of the transform layer
- [[data-engineering/pipeline-layers|Pipeline Layers]] — staging → warehouse → marts separation pattern
- [[data-engineering/data-quality|Data Quality]] — tests and DQ checks at the transform layer
- [[data-engineering/sql-intermediate-results|Storing Intermediate Results in SQL]] — how to structure transform steps (CTE/view/temp table/materialized view) to avoid the 3000-line-query trap
- [[data-engineering/sql-window-functions|SQL Window Functions]] — a core SQL technique used inside transform models (ranking, running aggregates, period-over-period)
- [[data-engineering/etl-pipeline|ETL Pipeline]] — where transform sits in ETL vs ELT

---

[^src1]: [Understanding the "T" in ETL: A Back-to-Basics Guide to Data Transformations](../../raw/email/email-2025-04-16-understanding-the-t-in-etl-a-back-to-basics-guide-to-data-tr.md)
