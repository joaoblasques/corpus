---
type: entity
domain: data-engineering
status: draft
sources:
  - path: raw/web/web-api-fundamentals-for-data-engineers-part-3-building-a-produc.md
    channel: web
    ingested_at: 2026-06-20
aliases:
  - dlt
  - data load tool
  - dlthub
  - dlt AI Workbench
  - RESTAPIConfig
tags:
  - corpus/data-engineering
  - entity
created: 2026-06-20
updated: 2026-06-20
---

# dlt (data load tool)

**TL;DR**: An open-source Python ELT library that describes REST API pipelines via configuration objects (`RESTAPIConfig`) instead of imperative loops. Handles authentication, pagination, schema normalization, and nested JSON flattening automatically. An AI-assisted extension called the **dlt AI Workbench** runs inside coding assistants (Claude Code, Cursor, Codex) to guide pipeline construction step-by-step [^src1].

## Core concept: describe, don't loop

Instead of writing `requests.get()` loops with custom pagination and header injection, dlt uses a declarative configuration object [^src1]:

```python
RESTAPIConfig = {
    "base_url": "https://api.openweathermap.org/data/3.0",
    "auth": BearerTokenAuth(token=secrets["api_key"]),
    "resources": [
        {
            "name": "current_weather",
            "endpoint": "/onecall",
            "params": {"lat": 37.7749, "lon": -122.4194}
        }
    ]
}
```

What dlt handles automatically:
- **Base URL + auth**: configured once, injected into every request.
- **Pagination**: auto-detects pattern (cursor, offset, next link) or set explicitly — `SinglePagePaginator`, `CursorPaginator`, `OffsetPaginator`, etc.
- **Nested JSON normalization**: deeply nested response objects are flattened into relational tables automatically.
- **Secrets management**: credentials live in `.dlt/secrets.toml`, never in code.

> "What used to be a manual loop of `requests.get()` calls with custom header injection is now a structured, readable configuration object." [^src1]

## dlt AI Workbench

An AI-powered extension that runs inside coding assistants. It installs as a toolkit:

```bash
uv run dlt ai toolkit rest-api-pipeline install
# then start Claude Code and describe the pipeline
```

Workflow for a new API source [^src1]:
1. Check 9,700+ pre-built REST API configurations at `dlthub.com/context`.
2. If no match, read API docs and build `RESTAPIConfig` from scratch.
3. Run and fix errors iteratively (agent handles most common issues).
4. Validate schema and data quality.
5. Extend with more endpoints.

The Workbench compresses setup work (reading API docs, writing config, handling pagination, debugging schema) that would normally take hours. It does not eliminate debugging entirely — real authentication errors, rate limits, and schema issues still require human judgment [^src1].

## Pagination patterns supported

| Pattern | dlt class | When used |
|---|---|---|
| Single-page | `SinglePagePaginator` | Endpoint returns everything in one response |
| Cursor-based | `CursorPaginator` | API returns a `next_cursor` field |
| Offset/limit | `OffsetPaginator` | API uses `offset` + `limit` params |
| Next link | `LinkPaginator` | API returns a `next` URL |

dlt auto-detects when not specified explicitly [^src1].

## Why it matters for data engineers

- Pagination loops are "tedious to write and easy to get wrong" — a missed next link or wrong cursor increment silently produces incomplete data [^src1].
- `RESTAPIConfig` separates *what you want* from *how to get it*: describe the API shape, dlt figures out the calls.
- Pipelines are reusable: add endpoints as items to the `resources` list.

## See also

- [Data Ingestion Patterns](/data-engineering/data-ingestion-patterns.md) — dlt fits the REST API pattern
- [ETL Pipeline](/data-engineering/etl-pipeline.md) — overall pipeline taxonomy
- [Data Quality](/data-engineering/data-quality.md) — schema validation that dlt enables
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [API Fundamentals for Data Engineers Part 3 — Building a Production-Ready Pipeline with dlt](../../raw/web/web-api-fundamentals-for-data-engineers-part-3-building-a-produc.md) — Pipeline to Insights
