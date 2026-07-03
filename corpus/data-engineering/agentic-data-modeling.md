---
type: synthesis
domain: data-engineering
status: draft
sources:
  - path: raw/web/github-aboyalejandro-agentic-data-modeling-showcasing-ai-dat.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/end-to-end-agentic-data-modeling-using-ai-and-openmetadata-m.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/schemaflow-agentic-database-change-impact-analysis-sql-gener.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/pg-infer-1-0-0-released-transformer-model-knowledge-as-sql-r.md
    channel: web
    ingested_at: 2026-06-12
aliases:
  - AI data modeling
  - agentic schema change
  - AI for data modeling
  - agentic database change
tags:
  - corpus/data-engineering
  - synthesis
created: 2026-06-12
updated: 2026-06-12
---

# Agentic Data Modeling

**TL;DR**: AI agents are being applied to the design-and-change side of data engineering — proposing schemas, modeling tables, and analyzing the downstream impact of schema changes before any SQL ships. The recurring pattern is the same: **give the agent metadata and the ability to explore (lineage catalogs, warehouse access) so it can reason about impact, not just generate SQL** [^src1][^src2]. Concrete implementations span a self-contained AI data stack (dbt + Metabase + OpenMetadata + MCP) [^src1], a staged change-analysis pipeline that turns a natural-language change request into an auditable impact/plan/SQL bundle [^src3], and an experimental PostgreSQL extension that makes transformer-model knowledge itself SQL-queryable [^src4]. The cross-cutting thesis: **"a single change could silently break eight dashboards in production"**, so metadata that exposes lineage and impact is the precondition for safe agentic modeling [^src2].

## Why metadata is the precondition

A dbt model that "works" in isolation says nothing about safety; the danger is silent downstream breakage [^src2]. Even with AI, working with dbt is described as "meaningless if we can't see the impact on downstream systems" [^src2]. The fix is to make metadata **dynamic, accessible, and actionable** — something both humans and AI systems can interact with at runtime — and to expose it to agents over a standard interface (MCP) so context isn't "locked in dashboards, documentation, and catalogues" [^src2]. Metadata gives data meaning: what a dataset represents, how IDs map to the same real-world entity across systems, which fields are PII [^src2].

## Pattern 1 — Catalog-grounded modeling (OpenMetadata + MCP)

A self-contained stack wires [Claude Code](/ai-engineering/claude-code.md) to a data stack via **two MCP servers** so the agent has both metadata intelligence and raw data access [^src1]:

| MCP server | Purpose | Representative tools |
|---|---|---|
| OpenMetadata MCP | Metadata catalog — lineage, search, glossaries, entity details | `search_metadata`, `get_entity_lineage`, `get_entity_details` [^src1] |
| PostgreSQL MCP (via Google GenAI Toolbox) | Direct DB access — query, profile columns, validate models | `execute_sql`, `list_tables`, `list_table_stats` [^src1] |

The PostgreSQL MCP gives direct SQL access for **data profiling, edge-case discovery, and validation queries** — used heavily by an "AI Readiness" skill [^src1]. OpenMetadata acts as the central hub: ingest metadata from sources, dbt, and the BI layer; build end-to-end lineage (source tables → dbt models → dashboards); track dependencies and downstream impact [^src1]. Crucially, all ingestion is configured through **YAML files**, enabling Infrastructure-as-Code practices (version control, automation, reproducibility) rather than UI clicks [^src1].

Four custom Claude Code skills encode repeatable workflows as slash commands [^src1]:

- **metadata-impact-analysis** — traces lineage through dbt models and dashboards to identify what breaks if a column is renamed, dropped, or retyped [^src1].
- **metadata-ai-readiness** — audits/enriches dbt mart models for AI consumption; queries the DB to discover edge cases; writes fixes back to dbt YAML [^src1].
- **metadata-glossary** — derives an OpenMetadata glossary from dbt column names/descriptions, grouped into business categories [^src1].
- **metadata-enrich** — fills missing/drifted descriptions across all dbt layers, producing a coverage report classifying every table/column as OK, Drift, or Missing; writes to dbt YAML first (source of truth) before patching OpenMetadata [^src1].

The same setup is demonstrated end-to-end with four use-case questions — impact analysis on a column rename, data discovery/validation, lineage exploration, and ownership/governance — answered in natural language against the catalogue [^src2]. A Slack bot brings the catalog assistant and skills into channels, with **write operations always requiring explicit confirmation** before any file or catalog change [^src1]. Both Claude Code and Cursor are supported via the same MCP approach [^src2].

> This is the companion deep-dive to the [Claude Code](/ai-engineering/claude-code.md)-for-DE tooling map; see [Claude Code for Data Engineering](/data-engineering/claude-code-for-data-engineering.md) for the PRD→ERD→dbt workflow and the exposure-enrichment / Metabase-MCP variant.

## Pattern 2 — Staged change-analysis pipeline (SchemaFlow)

SchemaFlow treats a schema change as a multi-stage agent workflow rather than one black-box SQL generator [^src3]. A deceptively simple request — "add a nullable column and backfill it" — can affect "landing tables, staging models, dimensional tables, marts, reporting logic, lineage assumptions, validation checks, rollback procedures, and release sequencing" [^src3]. The pipeline breaks the task into specialized [agents](/ai-engineering/ai-agent.md), each producing a typed, inspectable output:

| Stage | Agent | Output |
|---|---|---|
| 1. Parse | Parse Agent | `change_json` — structured request (schema, table, operations) [^src3] |
| 2. Impact | Impact Agent | `impact_json` — impacted objects, risks, assumptions (optional PDF RAG grounding) [^src3] |
| 3. Plan | Plan Agent | `plan_json` — steps, prechecks, postchecks, rollback [^src3] |
| 4. SQL | SQL Agent | draft SQL across LANDING/STAGING/CORE/MARTS layers [^src3] |
| 5. Validate | deterministic checks | expected table/column presence, required keywords (`ALTER TABLE`, `UPDATE`, `CREATE INDEX`) [^src3] |

Key design choices:

- **Guardrail gates between stages** — deterministic checks catch obvious failures (e.g., a nullable request accidentally generating `NOT NULL`) before downstream stages consume bad state [^src3].
- **Artifact-centered** — the run produces an auditable JSON bundle (change request, impact, plan, SQL, validation, optional RAG metadata), not just a script [^src3].
- **No side effects** — it produces *draft* SQL and validation output; it does not execute SQL, apply migrations, or open PRs [^src3].
- **Eval-ready** — generates a Promptfoo harness (provider, assertions, config, reports) from live notebook state [^src3].

The stated motivation mirrors Pattern 1: change requests move through handoffs (product owner → data engineer → platform → analytics engineer → reviewer) and "important context can be lost at each step" [^src3]. (Implementation note: SchemaFlow is built on the OpenAI Agents SDK with Pydantic-typed outputs, a different provider stack from the Claude-based patterns above [^src3].)

## Pattern 3 — Model knowledge as a SQL data source (pg_infer)

A more experimental direction inverts the usual relationship: instead of an agent calling the database, `pg_infer` (a PostgreSQL 18+ extension) brings small transformer-model internals **into the query plan as an operator the planner can cost, schedule, parallelize, and join** [^src4]. It is explicitly *not* natural-language-to-SQL and has "no chat interface, no agent loop, no prompt template" [^src4]. Instead it exposes gate activations, learned associations, and labels as SQL-queryable relations: `describe('France')` returns relations the model has learned (capital → Paris, language → French), and an index-backed `<~>` operator orders rows by model-knowledge similarity, composing with `WHERE`/`JOIN`/aggregation [^src4]. It targets the typical PostgreSQL HA/DR profile — busy primary plus idle CPU-rich replicas — running CPU-only via BitNet ternary-weight models and f16 gate vectors [^src4]. Relevance here: it is a primitive for **model-driven joins and semantic relatedness inside the warehouse**, distinct from pgvector (which stores user-supplied embeddings) [^src4].

## Cross-cutting themes

- **Impact analysis before change** is the unifying use case across Patterns 1 and 2 — trace lineage / enumerate impacted objects so a column rename doesn't silently break dashboards [^src1][^src2][^src3].
- **Human-in-the-loop / no silent writes** — explicit confirmation before catalog/file writes (Pattern 1) [^src1]; draft-only, no DB side effects (Pattern 2) [^src3].
- **Metadata as first-class, version-controlled product** — YAML-driven, IaC ingestion; dbt YAML as the source of truth that the catalog mirrors [^src1].
- **Standardized agent access** — MCP turns a passive catalogue into an "active, conversational layer" agents query at runtime [^src2].

## See also

- [Claude Code for Data Engineering](/data-engineering/claude-code-for-data-engineering.md) — the tooling map (Skills/MCPs/Hooks), PRD→ERD→dbt workflow, exposure enrichment
- [dbt](/data-engineering/dbt.md) — the transformation framework these workflows target; exposures and lineage
- [Dimensional Modeling](/data-engineering/dimensional-modeling.md) — the modeling output (grain, dimensions, facts)
- [AI agent](/ai-engineering/ai-agent.md) · [MCP](/ai-engineering/mcp.md) · [Agent Skills](/ai-engineering/agent-skills.md) — the underlying ai-engineering primitives
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [Agentic Data Modeling — Showcasing AI Data Stack (aboyalejandro)](../../raw/web/github-aboyalejandro-agentic-data-modeling-showcasing-ai-dat.md)
[^src2]: [End To End Agentic Data Modeling: Using AI and OpenMetadata MCP for Impact Analysis](../../raw/web/end-to-end-agentic-data-modeling-using-ai-and-openmetadata-m.md)
[^src3]: [SchemaFlow: Agentic Database Change Impact Analysis & SQL Generation](../../raw/web/schemaflow-agentic-database-change-impact-analysis-sql-gener.md)
[^src4]: [pg_infer 1.0.0 Released — Transformer Model Knowledge as SQL Relations](../../raw/web/pg-infer-1-0-0-released-transformer-model-knowledge-as-sql-r.md)
