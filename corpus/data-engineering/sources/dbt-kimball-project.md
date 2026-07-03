---
type: source
domain: data-engineering
status: draft
sources:
  - path: raw/web/github-vutrinh274-dbt-kimball.md
    channel: web
    ingested_at: 2026-06-11
aliases:
  - dbt_kimball
  - vutrinh274/dbt_kimball
tags:
  - corpus/data-engineering
  - source
created: 2026-06-11
updated: 2026-06-11
---

# dbt Kimball reference project (vutrinh274/dbt_kimball)

**TL;DR**: A reference [dbt](/data-engineering/dbt.md) project demonstrating [Kimball dimensional modeling](/data-engineering/dimensional-modeling.md) — SCD Type 2 dimensions, fact tables with surrogate-key relationships, and incremental processing by snapshot date — implemented twice, for BigQuery and DuckDB [^src1].

**Repo**: https://github.com/vutrinh274/dbt_kimball

## Structure

Two parallel implementations targeting different warehouses [^src1]:

```
dbt_kimball/
├── dbt_bigquery/    # BigQuery implementation
├── dbt_duckdb/      # DuckDB implementation (local development)
└── requirements.txt
```

## Models

- **Staging**: `stg_products`, `stg_product_categories`, `stg_product_subcategories`, `stg_sales`, `stg_territories` [^src1].
- **Dimensions ([SCD Type 2](/data-engineering/scd2.md))**: `dim_product`, `dim_territories` [^src1].
- **Fact**: `fact_sale` (surrogate-key relationships to the SCD2 dimensions) [^src1].

## Running it

Incremental processing is driven by a `process_date` variable; re-running with successive dates simulates daily incremental loads [^src1]:

```bash
dbt deps && dbt seed
dbt run --vars '{"process_date": "2025-08-01"}'
dbt run --vars '{"process_date": "2025-08-02"}'   # incremental
```

DuckDB runs locally (file-based, pre-configured `profiles.yml`); BigQuery needs a service-account `profiles.yml` [^src1]. The DuckDB UI (`duckdb -ui`) can attach `database/dbt_kimball.duckdb` to explore models [^src1].

## BigQuery vs. DuckDB portability notes

The project documents warehouse SQL-dialect differences worth knowing for cross-warehouse dbt [^src1]:

| Feature | BigQuery | DuckDB |
|---|---|---|
| Wildcard tables | `_TABLE_SUFFIX` | `UNION ALL` |
| Date parsing | `PARSE_DATE()` | `strptime()::DATE` |
| Date arithmetic | `DATE_SUB(..., INTERVAL)` | `date - INTERVAL` |
| Partitioning | Supported | Not applicable |
| Incremental strategy | `insert_overwrite` | `delete+insert` |

## See also

- [Dimensional Modeling](/data-engineering/dimensional-modeling.md)
- [SCD Type 2](/data-engineering/scd2.md)
- [dbt](/data-engineering/dbt.md)

---

[^src1]: [vutrinh274/dbt_kimball](../../../raw/web/github-vutrinh274-dbt-kimball.md)
