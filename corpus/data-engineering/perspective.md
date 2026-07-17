---
type: entity
domain: data-engineering
status: draft
sources:
  - path: raw/github/github-perspective-dev-perspective.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - Perspective
  - perspective-dev
  - "@finos/perspective"
  - perspective-python
  - WebAssembly analytics
  - streaming data visualization
tags:
  - corpus/data-engineering
  - entity
created: 2026-06-25
updated: 2026-07-17
---

# Perspective

**TL;DR.** Perspective (perspective-dev/perspective, ★10,974, C++) is an open-source **interactive analytics and data visualization component** optimized for large and/or streaming datasets [^src1]. It powers user-configurable reports, dashboards, notebooks, and applications via a high-performance query engine compiled to WebAssembly, Python, and Rust. Especially well-suited for real-time data pipelines where the visualization layer must keep up with high-throughput streams.

## Core capabilities

- **Framework-agnostic UI** — packaged as a [Custom Element](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_custom_elements); connects to a Data Model in-browser (via WebAssembly) or remotely (via WebSocket with Python, Node.js, Rust integration). Includes a data grid and 10+ chart types: line, bar, area, scatter, heatmap, treemap, sunburst, candlestick, and more [^src1].
- **Pluggable data model** — the Data Model API supports external query engines (e.g. **DuckDB**) translating view configurations into native queries [^src1].
- **Streaming Data Model (built-in)** — written in C++, compiled for WebAssembly, Python, and Rust; supports read/write/streaming for **Apache Arrow** with a columnar expression language based on ExprTK [^src1].
- **JupyterLab widget** — first-class Jupyter integration via `perspective.widget`; also ships a Python client library for interactive data analysis in notebooks [^src1].
- **Virtual servers** — pluggable server backends for ClickHouse (`perspective.virtual_servers.clickhouse`) and DuckDB (`perspective.virtual_servers.duckdb`) let Perspective translate UI view configurations into native engine queries [^src1].
- **Python async handlers** — integrations for `aiohttp`, `starlette`, and `tornado` enable serving the Perspective WebSocket protocol from standard Python web frameworks [^src1].

## Distribution packages

| Package | Registry | Language |
|---|---|---|
| `@perspective-dev/client` | npm | JavaScript (browser + Node.js) |
| `@perspective-dev/viewer` | npm | Web Component |
| `perspective-python` | PyPI | Python |
| `perspective` | crates.io | Rust |

Latest release at collection time: **v4.5.1** [^src1].

## Language targets

| Runtime | Use |
|---|---|
| WebAssembly | In-browser analytics, zero-server compute |
| Python | Server-side data model (`perspective-python`); Jupyter widget; aiohttp/starlette/tornado handlers |
| Rust | Low-level embedding; `perspective-server` + `perspective-client` crates |
| Node.js | Server-side JS integration via `@perspective-dev/client` |

[^src1]

## Positioning in the data stack

Perspective sits at the **visualization/serving layer** — the consumer of processed data, not the producer. In a [modern data stack](/data-engineering/modern-data-stack.md) context, it connects downstream of the transformation layer (dbt, Spark) to provide real-time or near-real-time dashboards without requiring a separate BI tool. Its WebAssembly engine enables query execution in the browser, reducing server-side compute costs for interactive analytics.

The DuckDB integration is particularly notable: it positions Perspective alongside [DuckDB](/data-engineering/duckdb.md) as part of a lightweight, embeddable analytics stack that can process large datasets locally without cloud warehouse compute. See also [BI as Code](/data-engineering/bi-as-code.md) for the broader SQL-first visualization paradigm.

## Related

- [DuckDB](/data-engineering/duckdb.md) — DuckDB is one of the supported external Data Model query engines
- [BI as Code](/data-engineering/bi-as-code.md) — broader concept of code-driven analytics dashboards
- [Stream Processing](/data-engineering/stream-processing.md) — Perspective is designed for streaming data visualization
- [Apache Spark](/data-engineering/apache-spark.md) / [Apache Kafka](/data-engineering/kafka.md) — typical upstream producers for streaming data Perspective visualizes
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [perspective-dev/perspective — Data visualization and analytics component for large/streaming datasets (GitHub)](../../raw/github/github-perspective-dev-perspective.md)
