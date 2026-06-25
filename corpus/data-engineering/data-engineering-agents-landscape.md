---
type: synthesis
domain: data-engineering
status: draft
sources:
  - path: raw/web/github-canner-wrenai-give-ai-agents-the-context-to-query-bus.md
    channel: web
    ingested_at: 2026-06-18
  - path: raw/web/github-vanna-ai-vanna-chat-with-your-sql-database-accurate-t.md
    channel: web
    ingested_at: 2026-06-18
  - path: raw/web/github-dataherald-dataherald-interact-with-your-sql-database.md
    channel: web
    ingested_at: 2026-06-18
  - path: raw/web/github-datus-ai-datus-agent-the-future-of-data-engineering-a.md
    channel: web
    ingested_at: 2026-06-18
  - path: raw/web/github-dbt-labs-dbt-mcp-a-mcp-model-context-protocol-server.md
    channel: web
    ingested_at: 2026-06-18
  - path: raw/web/genie-spaces-databricks-on-aws.md
    channel: web
    ingested_at: 2026-06-18
  - path: raw/github/github-dataherald-dataherald.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - data engineering agents
  - text-to-SQL agents
  - text2sql agents
  - OSS data agents
  - Vanna
  - WrenAI
  - Wren AI
  - Dataherald
  - Datus
  - Datus-agent
  - dbt MCP
  - dbt Agent Skills
  - Databricks Genie
  - Genie Spaces
  - build-time vs consume-time
tags:
  - corpus/data-engineering
  - synthesis
created: 2026-06-18
updated: 2026-06-25
provisional: false
---

# Data Engineering Agents — The Landscape

**TL;DR.** A wave of open-source "AI agents for data engineering" arrived 2025-2026 (Vanna, WrenAI, Dataherald, Datus-agent), alongside vendor entries (Databricks Genie, dbt's MCP/Agent Skills). The single most clarifying lens is **build-time vs consume-time**: almost all of these tools live at *consume-time* — they translate natural language into SQL against a **finished** warehouse/marts (text-to-SQL) and do **not** build the pipelines that produced those marts. The genuinely *build-time* agentic work — designing models, writing transformations, enforcing quality — is still done by general coding agents ([[ai-engineering/claude-code|Claude Code]] + [[ai-engineering/claude-md-conventions|CLAUDE.md]] + [[ai-engineering/agent-skills|Skills]] + [[data-engineering/data-quality|DQ]]-as-hooks), with dbt's MCP and Databricks' Lakeflow as the only tools in this set that meaningfully touch the build side. **Recommendation for a solo DE building a portfolio lakehouse: build with Claude Code + CLAUDE.md + Skills + DQ-as-hooks; optionally bolt on one OSS text-to-SQL agent (WrenAI or Vanna) as a demo "ask-your-data" layer over finished marts.** The distinction matters because the two layers have opposite failure modes and opposite review economics (see [[data-engineering/ai-impact-on-data-engineering|AI's Impact on Data Engineering]]).

## The central distinction: build-time vs consume-time

The corpus already separates the pipeline into [[data-engineering/pipeline-layers|staging -> warehouse -> marts]] and treats agents-as-consumers as a distinct shift [^src1-internal]. Map the tool landscape onto that pipeline:

| | **Build-time (produce the marts)** | **Consume-time (query the marts)** |
|---|---|---|
| **What the agent does** | Designs models, writes/edits SQL transformations, runs/tests/materializes, enforces DQ | Translates a natural-language question -> governed SQL -> results/charts over already-built tables |
| **Output** | dbt models, pipelines, tables, tests, lineage | An answer (SQL + table + chart + summary) |
| **Failure mode** | Silent wrong pipeline (wrong row counts, dropped columns) — corrupts the asset for everyone | Wrong-but-plausible answer to one question — bounded to that query |
| **Who reviews** | Engineer reviews code before merge (high-stakes, CI-gated) | User sees the SQL/provenance and re-asks (self-correcting) |
| **Tools in this survey** | dbt MCP/Agent Skills (partial), Databricks Lakeflow, **Claude Code + Skills + hooks** | **Vanna, WrenAI, Dataherald, Datus-agent, Databricks Genie**, dbt MCP `text_to_sql` |

The asymmetry is the whole point: a build-time error is **"wrong is worse than absent because you can't trust it"** [^src2-internal], so build-time agents need deterministic guardrails (tests, hooks, plan-mode review) baked in. A consume-time error is one bad answer a user can challenge. **Most OSS "data engineering agents" are actually consume-time text-to-SQL with a context/semantic layer bolted on** — they presuppose a warehouse someone else built.

## The tools

### Consume-time: text-to-SQL over finished warehouses

**Vanna** — *what:* a Python text-to-SQL framework; "Natural language -> SQL -> Answers," now (2.0) rebuilt around user-aware agents with row-level security, audit logs, rate limiting, a pre-built `<vanna-chat>` web component, and FastAPI/Flask integration [^vanna]. Pluggable across any LLM (OpenAI, Anthropic, Ollama, Bedrock, ...) and any database (Postgres, Snowflake, BigQuery, [[data-engineering/duckdb|DuckDB]], [[data-engineering/clickhouse|ClickHouse]], ...) [^vanna]. *License:* **MIT** [^vanna]. *Maturity:* established (a 2.0 "complete rewrite" with a legacy adapter for 0.x users), production-deployment oriented [^vanna]. *Fit:* the lowest-friction way to add a "chat with your marts" demo to a portfolio — embeddable component + bring-your-own-auth, RAG-style training on your schema/example queries.

**WrenAI** — *what:* repositions itself as **"the open context layer"** rather than a chat app — business semantics, examples, memory, and governance that *any* agent (Claude Code, Cursor, LangChain, Pydantic AI) queries through one shared interface, instead of each agent rediscovering business logic [^wren]. Ships a CLI + agent-skills install stub, a Rust semantic engine on Apache DataFusion (22+ data sources), a **Modeling Definition Language (MDL)** with row/column-level access control, and LanceDB-backed memory; everything is version-controlled and Git-friendly [^wren]. *License:* **Apache-2.0** (core, SDK, skills) [^wren]. *Maturity:* active but mid-pivot — the Wren Engine merged into the main repo (2026-05), the previous GenBI app was moved to a `legacy/v1` branch, and agent-native SDKs are still rolling out [^wren]. *Fit:* the strongest choice if you want the demo layer to double as a reusable [[data-engineering/semantic-layer|semantic layer]] across multiple agents; heavier than Vanna.

**Dataherald** — *what:* a natural-language-to-SQL **engine** for enterprise Q&A over relational data — set up an API from your DB that answers plain-English questions; four deployable services (Engine, Enterprise auth layer, Admin console, Slackbot), each Docker-composed [^dataherald][^dataherald-gh]. Aimed at letting business users self-serve without a data analyst, or embedding Q&A in a SaaS product [^dataherald-gh]. *License:* **Apache 2.0** [^dataherald-gh]. *Stars:* 3,635 on GitHub (Python, topics: ai, database, finetuning, llm, nl-to-sql, rag, sql, text-to-sql) [^dataherald-gh]. *Maturity:* enterprise-shaped (multi-service, auth/orgs/users, v1.0.3 released) but heavier to stand up; less momentum than Vanna/WrenAI in this survey. *Fit:* overkill for a solo portfolio — its value (orgs, auth, admin console) is multi-tenant enterprise plumbing, not portfolio signal.

**Datus-agent** — *what:* an "open-source data engineering agent" that frames DE as *"delivering scoped, domain-aware agents for analysts and business users,"* building an evolving context layer (schema metadata, reference SQL, semantic models, metrics, docs) that improves through a continuous-learning loop [^datus]. A Claude-Code-like CLI with **Plan Mode**, a node-based workflow engine (`schema_linking -> gen_sql -> reasoning -> selection -> execute_sql`), LanceDB knowledge base, MCP server *and* client, agentskills.io-style Skills, MetricFlow semantic adapters, and a built-in eval framework (BIRD, Spider 2.0-Snow) [^datus]. 10+ LLM providers, 11 databases incl. [[data-engineering/apache-spark|Spark]]/Trino/Snowflake adapters [^datus]. *License:* **open-source** (license not named in the excerpt; PyPI `datus-agent`, pinned versions ~0.2.x) [^datus]. *Maturity:* early/evolving (sub-1.0), but the most *DE-conscious* of the OSS set — it explicitly targets the build->deliver->iterate loop, not just one-shot SQL. *Fit:* interesting as a study of the "contextual data engineering" thesis; for a solo portfolio it overlaps heavily with the Claude-Code-native approach below and adds a second framework to maintain.

**Databricks Genie** — *what:* **Genie Spaces** are domain-specific natural-language chat interfaces inside Databricks; analysts curate each space with Unity-Catalog-registered datasets, example SQL, business-semantic SQL expressions, and text instructions, and users get back SQL + results + visualizations [^genie]. Part of a family: Genie One (cross-asset chat), **Genie Code** (the developer-facing assistant for writing code/pipelines/dashboards), plus an agent mode and a Conversation API for embedding [^genie]. *License:* **proprietary** (a managed [[data-engineering/databricks|Databricks]] platform feature). *Maturity:* GA commercial product. *Fit:* only relevant if the portfolio is already on Databricks; the curate-with-instructions pattern mirrors WrenAI's context layer but is vendor-locked.

### Build-time (and the consume/build straddlers)

**dbt MCP / dbt Agent Skills** — *what:* dbt Labs' official **MCP server** exposes dbt to any agent across dbt Core, Fusion, and Platform [^dbtmcp]. Its tools straddle both layers: *consume-time* — `text_to_sql` (NL->SQL using project context), `execute_sql`, and Semantic-Layer metric queries (`query_metrics`, `list_metrics`); *build-time* — `run`, `build`, `test`, `compile`, `parse`, plus codegen (`generate_model_yaml`, `generate_source`, `generate_staging_model`) and rich Discovery-API lineage/health tools [^dbtmcp]. The README warns these build tools "could modify your data models, sources, and warehouse objects" [^dbtmcp]. The companion **dbt Agent Skills** encode analytics-engineering workflows (build/modify models, unit tests, correct command flags); some are dbt-Core/OSS-compatible, others dbt-Cloud-only [^src3-internal]. *License:* open-source (dbt MCP repo); dbt Core is Apache-2.0. *Maturity:* official, actively maintained, ships an experimental `.mcpb` bundle per release [^dbtmcp]. *Fit:* **the single best add-on for a [[data-engineering/dbt|dbt]]-based portfolio** — it is the supported bridge between a coding agent and your dbt project, and it covers both building models and querying the semantic layer.

**Databricks Lakeflow** — *what:* not an "agent" but the **build-time declarative pipeline** layer (SQL/Python; formerly DLT) where you describe tables and the platform handles orchestration + incremental processing; interoperable with the open-sourced Apache Spark Declarative Pipelines but running as a Databricks SKU [^src4-internal]. *License:* proprietary. *Fit:* the build-side counterpart to Genie's consume-side on Databricks; out of scope for a non-Databricks lakehouse. See [[data-engineering/databricks|Databricks]].

**Claude Code + CLAUDE.md + Skills + DQ-as-hooks** — *what:* the general-purpose coding agent is the actual build-time workhorse: scaffold a dbt project, run the **PRD -> DB-exploration -> ERD -> dbt models** workflow, and enforce quality with hooks that act as **CI/CD inside the agent loop** (`pytest` on PreCommit, `sqlfluff lint` and `dbt test --select` on PostToolUse) — *"don't trust the AI to remember quality checks; automate them so they can't be skipped"* [^src5-internal]. This is build-time agentic DE done right, with deterministic [[data-engineering/data-quality|data-quality]] gates rather than a text-to-SQL box. *License:* commercial agent, but the *pattern* (CLAUDE.md + Skills + hooks) is portable and OSS-friendly. *Fit:* **the recommended core.**

## Why most "DE agents" are consume-time — and what that means

The recurring shape across Vanna, WrenAI, Dataherald, Datus, and Genie is identical: **a context/semantic layer + retrieval + an LLM that emits governed SQL against existing tables** [^vanna][^wren][^dataherald][^datus][^genie]. None of them *creates* the warehouse; they all assume staging/warehouse/[[data-engineering/data-mart|marts]] already exist. This is exactly the corpus's "**agents, not analysts, become the primary query drivers**" thesis [^src1-internal] — they are the new *consumer* of data engineering, which raises the value of the [[data-engineering/semantic-layer|semantic layer]] and clean, well-described marts, not the value of a second pipeline-building tool.

The build side has the opposite economics. A consume-time wrong answer is bounded and self-correcting; a **build-time** silent error (the API pagination cap that loaded 1,493 of 5,458 rows; dropped columns) *"required expert validation to catch"* and corrupts the asset for every downstream consumer [^src2-internal][^src5-internal]. That is why build-time agentic work needs determinism engineering — plan-mode, tests, hooks, colocated context — and why a solo DE should invest there with a controllable coding agent rather than outsource it to a text-to-SQL framework that doesn't build pipelines at all.

## Recommendation — solo DE building a portfolio lakehouse

1. **Build with Claude Code + CLAUDE.md + Skills + DQ-as-hooks.** Make conventions explicit in [[ai-engineering/claude-md-conventions|CLAUDE.md]], encode repeatable workflows as [[ai-engineering/agent-skills|Skills]], and enforce [[data-engineering/data-quality|data quality]] with hooks (`pytest`, `sqlfluff`, `dbt test`) so checks can't be skipped [^src5-internal]. This is the build-time layer and the portfolio's real signal: it shows you can produce trustworthy [[data-engineering/medallion-architecture|bronze->silver->gold]] marts, not just ask questions of them. Pair it with **dbt MCP / Agent Skills** if the stack is [[data-engineering/dbt|dbt]]-based — the supported agent-to-dbt bridge that also handles `run`/`build`/`test` [^dbtmcp].
2. **Optionally add ONE OSS text-to-SQL agent as a demo consume layer over finished marts.** Pick **WrenAI** if you want the demo to double as a reusable, Git-friendly [[data-engineering/semantic-layer|semantic/context layer]] (Apache-2.0) [^wren]; pick **Vanna** if you want the fastest embeddable "chat with your data" component (MIT) [^vanna]. Either makes a compelling "ask your lakehouse in English" headline on top of marts the build layer already produced.
3. **Skip** Dataherald (enterprise multi-tenant plumbing, no solo payoff) [^dataherald], **skip** Datus-agent unless you specifically want to study the contextual-DE thesis (it duplicates the Claude-Code-native loop and adds a second framework) [^datus], and treat **Genie/Lakeflow** as relevant only if the portfolio is already on [[data-engineering/databricks|Databricks]] [^genie][^src4-internal].

**One-line rule of thumb:** *build the lakehouse with a coding agent you control + deterministic DQ gates; demo it with at most one text-to-SQL agent on the finished marts — and never confuse the two.*

## See also

- [[data-engineering/claude-code-for-data-engineering|Claude Code for Data Engineering]] — the build-time playbook (Skills/MCPs/Hooks, PRD->ERD->dbt, hooks-as-CI/CD)
- [[data-engineering/ai-impact-on-data-engineering|AI's Impact on Data Engineering]] — agents as the new query consumer; the Markdown Team
- [[data-engineering/agentic-data-modeling|Agentic Data Modeling]] — agents on the design/change side (OpenMetadata MCP, SchemaFlow)
- [[data-engineering/semantic-layer|Semantic Layer]] — the context layer all these agents depend on
- [[data-engineering/data-quality|Data Quality]] — the DQ gates that make build-time agents safe
- [[data-engineering/dbt|dbt]] / [[data-engineering/databricks|Databricks]] / [[data-engineering/pipeline-layers|Pipeline Layers]]
- [[ai-engineering/mcp|MCP]] / [[ai-engineering/agent-skills|Agent Skills]] / [[ai-engineering/claude-md-conventions|CLAUDE.md Conventions]] — the underlying ai-engineering primitives
- [[data-engineering/README|Data Engineering hub]]

---

[^vanna]: [Vanna — Chat with your SQL database (GitHub: vanna-ai/vanna)](../../raw/web/github-vanna-ai-vanna-chat-with-your-sql-database-accurate-t.md)
[^wren]: [WrenAI — the open context layer for agents (GitHub: Canner/WrenAI)](../../raw/web/github-canner-wrenai-give-ai-agents-the-context-to-query-bus.md)
[^dataherald]: [Dataherald — interact with your SQL database in natural language (GitHub: Dataherald/dataherald)](../../raw/web/github-dataherald-dataherald-interact-with-your-sql-database.md)
[^dataherald-gh]: [Dataherald GitHub digest](../../raw/github/github-dataherald-dataherald.md)
[^datus]: [Datus — open-source data engineering agent (GitHub: Datus-ai/Datus-agent)](../../raw/web/github-datus-ai-datus-agent-the-future-of-data-engineering-a.md)
[^dbtmcp]: [dbt MCP server (GitHub: dbt-labs/dbt-mcp)](../../raw/web/github-dbt-labs-dbt-mcp-a-mcp-model-context-protocol-server.md)
[^genie]: [Genie Spaces (Databricks on AWS docs)](../../raw/web/genie-spaces-databricks-on-aws.md)
[^src1-internal]: [[data-engineering/ai-impact-on-data-engineering|AI's Impact on Data Engineering]] (corpus) — agents, not analysts, as the primary query drivers
[^src2-internal]: [[data-engineering/ai-impact-on-data-engineering|AI's Impact on Data Engineering]] (corpus) — Moffatt case: silent build-time failures; "wrong is worse than absent"
[^src3-internal]: [[data-engineering/claude-code-for-data-engineering|Claude Code for Data Engineering]] (corpus) — dbt Agent Skills (dbt-Core vs dbt-Cloud scope)
[^src4-internal]: [[data-engineering/databricks|Databricks]] (corpus) — Lakeflow Spark Declarative Pipelines
[^src5-internal]: [[data-engineering/claude-code-for-data-engineering|Claude Code for Data Engineering]] (corpus) — hooks as CI/CD inside the agent loop; build-time DQ gates
