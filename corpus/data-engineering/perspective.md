---
type: entity
domain: data-engineering
status: stub
sources:
  - path: raw/github/github-perspective-dev-perspective.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - Perspective
  - perspective-dev
  - @finos/perspective
  - perspective-python
  - WebAssembly analytics
  - streaming data visualization
tags:
  - corpus/data-engineering
  - entity
created: 2026-06-25
updated: 2026-06-25
---

# Perspective

**TL;DR.** Perspective (perspective-dev/perspective, ★10,974, C++) is an open-source **interactive analytics and data visualization component** optimized for large and/or streaming datasets [^src1]. It powers user-configurable reports, dashboards, notebooks, and applications via a high-performance query engine compiled to WebAssembly, Python, and Rust. Especially well-suited for real-time data pipelines where the visualization layer must keep up with high-throughput streams.

## Core capabilities

- **Framework-agnostic UI** — packaged as a [Custom Element](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_custom_elements); connects to a Data Model in-browser (via WebAssembly) or remotely (via WebSocket with Python, Node.js, Rust integration). Includes a data grid and 10+ chart types: line, bar, area, scatter, heatmap, treemap, sunburst, candlestick, and more [^src1].
- **Pluggable data model** — the Data Model API supports external query engines (e.g. **DuckDB**) translating view configurations into native queries [^src1].
- **Streaming Data Model (built-in)** — written in C++, compiled for WebAssembly, Python, and Rust; supports read/write/streaming for **Apache Arrow** with a columnar expression language based on ExprTK [^src1].
- **JupyterLab widget** — first-class Jupyter integration for data exploration in notebooks.

## Language targets

| Runtime | Use |
|---|---|
| WebAssembly | In-browser analytics, zero-server compute |
| Python | Server-side data model (`perspective-python`); Jupyter widget |
| Rust | Low-level embedding, custom integrations |
| Node.js | Server-side JS integration |

[^src1]

## Positioning in the data stack

Perspective sits at the **visualization/serving layer** — the consumer of processed data, not the producer. In a [[data-engineering/modern-data-stack|modern data stack]] context, it connects downstream of the transformation layer (dbt, Spark) to provide real-time or near-real-time dashboards without requiring a separate BI tool. Its WebAssembly engine enables query execution in the browser, reducing server-side compute costs for interactive analytics.

The DuckDB integration is particularly notable: it positions Perspective alongside [[data-engineering/duckdb|DuckDB]] as part of a lightweight, embeddable analytics stack that can process large datasets locally without cloud warehouse compute. See also [[data-engineering/bi-as-code|BI as Code]] for the broader SQL-first visualization paradigm.

## Related

- [[data-engineering/duckdb|DuckDB]] — DuckDB is one of the supported external Data Model query engines
- [[data-engineering/bi-as-code|BI as Code]] — broader concept of code-driven analytics dashboards
- [[data-engineering/stream-processing|Stream Processing]] — Perspective is designed for streaming data visualization
- [[data-engineering/apache-spark|Apache Spark]] / [[data-engineering/kafka|Apache Kafka]] — typical upstream producers for streaming data Perspective visualizes
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [perspective-dev/perspective — Data visualization and analytics component for large/streaming datasets (GitHub)](../../raw/github/github-perspective-dev-perspective.md)
