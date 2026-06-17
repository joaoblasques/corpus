---
type: synthesis
domain: data-engineering
status: draft
sources:
  - path: raw/web/hands-on-claude-code-for-data-engineers-data-modeling-with-d.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/email/email-2026-04-08-create-a-dbt-project-from-scratch-w-claude-code.md
    channel: email
    ingested_at: 2026-06-11
  - path: raw/web/intro-to-claude-code-for-data-engineers-skills-mcps-hooks-fo.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-06-04-claude-code-for-data-engineers-hands-on-projects-for-your-da.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/how-anthropic-enables-self-service-data-analytics-with-claud.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-06-08-anthropics-automated-analytics-postgresql-19-beta-mckinney-o.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/plan-mode-all-the-time-substrait-over-sql-and-the-end-of-the.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/feat-add-metadata-exposure-enrichment-skill-and-metabase-mcp.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/web-claude-code-isnt-going-to-replace-data-engineers-yet.md
    channel: web
    ingested_at: 2026-06-17
  # Cross-domain: also relevant to ai-engineering (agentic coding, Skills, MCP)
aliases:
  - Claude Code dbt
  - AI data modeling
  - AI-assisted dbt
  - Claude Code for data engineers
  - self-service analytics with Claude
tags:
  - corpus/data-engineering
  - synthesis
created: 2026-06-11
updated: 2026-06-17
---

# Claude Code for Data Engineering

**TL;DR**: AI coding agents (Claude Code) can automate the most mechanical parts of analytics engineering — scaffolding a new [[data-engineering/dbt|dbt]] project, and translating business requirements through a **PRD → database exploration → ERD → dbt models** workflow [^src1][^src2]. The leverage comes from making conventions explicit (via `CLAUDE.md`, custom Skills) and giving the agent **exploration tools** (warehouse/BI MCP servers) rather than asking it to guess from YAML alone [^src1]. This is a data-engineering-primary topic that overlaps the **ai-engineering** domain (agentic coding, Skills, MCP).

## Two complementary patterns

### 1. Scaffold a dbt project from scratch
Use Claude Code to go from zero to a structured, clean dbt project [^src2]:

- Use a **`CLAUDE.md`** file to clarify the project's purpose and design up front [^src2].
- **Upload a sample dbt project** as a reference so the agent matches an existing style and produces a better result [^src2].
- Create **"rules"** that continuously improve the project's quality over the long term [^src2].

Caveat stated plainly: this does not remove code review — "Blindly trust the AI outputs at your own risk" — but it expedites grunt work and gets you from zero to one faster [^src2]. A related warning: using AI "just for the sake of using AI" mainly helps you "hurry up to make a mess" [^src2].

### 2. PRD → ERD → dbt modeling workflow
A repeatable workflow that closes the gap between conceptual design and physical models — noting that "90% of data modeling happens outside the tools that implement it" [^src1]:

| Step | What Claude Code does | Tooling |
|---|---|---|
| **1. Read PRD + explore DB** | Reads business requirements (business language, no column names/grain) and samples raw tables to check assumptions | Miro MCP (board), MCP Data Toolbox (warehouse) [^src1] |
| **2. Translate to plan** | Maps business concepts → source tables, identifies gaps, produces a plan (models per layer, grain, joins) — "the step most teams skip" | custom `prd-to-dbt` Skill [^src1] |
| **3. Propose schema** | Draws an ERD on the board for stakeholder review/pushback before any SQL is written | Miro MCP [^src1] |
| **4. Implement + validate** | Generates models across all layers plus schema YAMLs with descriptions, grain docs, and tests, following the existing project's patterns | dbt Agent Skills [^src1] |

**Key division of labor**: the custom Skill handles the **what** (which models, scoped to the project); the dbt Agent Skills handle the **how** (best-practice implementation). This split keeps output consistent across different PRDs and projects [^src1].

## The foundation: Skills, MCPs & Hooks

Beyond the two modeling workflows, the broader "Claude Code for DE" setup rests on **three mechanisms** that connect the agent to the data stack [^src3][^src4]:

- **MCP servers** — connect Claude to external tools in real time: databases, orchestrators, metadata catalogs; avoid context switching during a session [^src3][^src4].
- **Skills** — encode best practices the agent follows automatically (dbt modeling patterns, testing conventions, documentation standards); written once, run on every relevant task [^src3][^src4].
- **Hooks** — enforce quality gates before/after the agent acts; "the checks can't be skipped because they're not relying on Claude to remember them" [^src4].

"The real value is chaining them" [^src4]. Data modeling has the most mature ecosystem today [^src3][^src4].

### dbt Agent Skills
Encode analytics-engineering workflows as instructions. dbt-Core/OSS-compatible ones include `using-dbt-for-analytics-engineering` (build/modify models, debug, explore sources), `adding-dbt-unit-test` (TDD), `running-dbt-commands` (correct flags/selectors), and `fetching-dbt-docs`; semantic-layer building, NL queries, job troubleshooting, and Fusion migration are dbt-Cloud-only [^src3]. They improve documentation by default and keep projects compatible with dbt best practices [^src3].

### MCP Data Toolbox (unified DB access)
Google's open-source unified layer supports **30+ databases through a single `tools.yaml`** config — schema discovery, query execution with connection pooling, result caching — instead of one MCP per database [^src3]. Recommended pattern: Data Toolbox as the default plus one specialized MCP for the primary warehouse (e.g., Snowflake MCP for Cortex, PostgreSQL MCP Pro for index recommendations) [^src3]. For orchestration, an Airflow MCP (Astronomer's, works with any OSS Airflow 2.x/3.x via the REST API) exposes `explore_dag`, `diagnose_dag_run`, and `get_system_health` [^src3].

### Hooks as CI/CD inside the agent loop
Three high-value examples [^src3]:

- `pytest` on `PreCommit` — failing tests block the commit [^src3].
- `sqlfluff lint` on `PostToolUse` (Write/Edit of `.sql`) — catches style/naming/anti-patterns before review [^src3].
- `dbt test --select <model>` on `PostToolUse` — schema/data-test failures surface immediately, not in production [^src3].

"Don't trust the AI to remember quality checks. Automate them so they can't be skipped." [^src3] A tip: have Claude build a single "validation" skill that bundles these gates [^src3]. To prevent hallucinated API signatures, inject current docs via a **docs-as-MCP** approach (Context7, gitingest, docs-mcp-server) [^src3].

### Making existing models AI-ready
Building new models is the easy part; the harder problem is an existing dbt project with column names and "zero useful descriptions for AI Agents" [^src4]. When the consumer shifts from a human analyst to an LLM, "vague metadata becomes input for confident hallucinations" [^src4]. The `metadata-ai-readiness` skill automates the enrichment loop — audit what's missing against dbt documentation standards, profile actual data via Postgres MCP to find edge cases the YAMLs don't mention, write enriched descriptions back, and flag what it can't fix — described as **progressive disclosure applied to metadata** [^src4]. A surfaced example: two models with opposite null-handling touching the same data points, captured once in an enriched description [^src4].

## Exposure enrichment / BI lineage

A third, closely related application: using Claude Code to enrich [[data-engineering/dbt|dbt]] **exposures** so they form a lean data catalog with end-to-end model → dashboard → card/column lineage — without a dedicated metadata platform. See [[data-engineering/dbt|dbt]] § Exposures and lineage for the detailed workflow (Metabase MCP discovery loop, impact analysis).

The concrete mechanism: a `/metadata-exposure-enrichment` skill queries Metabase dashboards via the **Metabase MCP** (`nao-metabase-mcp-server`), discovers cards and column references, cross-references them to dbt models, audits `_exposures.yml` for gaps, and writes enriched metadata back [^src5]. In the showcase run against a dashboard (ID=2), the skill auto-discovered 6 cards, parsed each card's MBQL query to identify source tables and columns, resolved Metabase internal table IDs to real names, cross-referenced tables to dbt `ref()`/`source()`, found 5 gaps (missing description, owner, maturity, card documentation, and a missing source dependency), and wrote the enriched YAML — using **Metabase MCP + Postgres MCP only, no OpenMetadata dependency** [^src5]. This is the catalog-free counterpart to the OpenMetadata-based [[data-engineering/agentic-data-modeling|agentic data modeling]] stack.

## Anthropic's own self-service analytics

Anthropic's data team reports **95% of business analytics queries are automated via Claude, with ~95% accuracy in aggregate** [^src6][^src7]. Their central thesis: accurate self-service analytics is "mostly a context and verification problem, not a SQL generation issue" [^src6][^src7]. The hard part is mapping a user's question to the correct, up-to-date entities in the data model; once that's done, "the resulting execution and SQL becomes trivial" [^src6].

**Three failure modes** account for most inaccurate responses [^src6]:
- **Concept ↔ entity ambiguity** — the agent can't pick the right fields among many plausible candidates (e.g., what counts as an "active" user) [^src6].
- **Data staleness** — sources, definitions, and schemas change; assets and agent knowledge rot [^src6].
- **Retrieval failure** — the right info exists and is annotated, but the agent doesn't find it in a vast search space [^src6].

**The agentic analytics stack** attacks each [^src6]:
- **Data foundations** — curate a small set of canonical, single-source-of-truth datasets and aggressively deprecate near-duplicates; enforce via tooling, CI, and mandate; **colocate** all data code (modeling, semantic layer, docs, dashboard defs) in one repo so a breaking change and its fix ship in the same PR; treat metadata as a first-class product [^src6].
- **Sources of truth** (descending trust) — semantic layer first (agents are *structurally required* to try it first), then lineage/transformation graph, then a query corpus (distilled into reference docs, **not** read raw — direct grep access moved accuracy <1 point), then a company knowledge graph for business context [^src6].
- **Skills** — "Without skills, Claude's ability to answer analytics questions accurately didn't exceed 21%... Adding skills gets these numbers consistently above 95%" [^src6]. Pattern: a thin **knowledge skill** routes to ~30 curated reference files per domain (the answer to retrieval failure), plus reference docs written *for LLM retrieval* (grain, scope, gotchas, explicit routing triggers) [^src6].
- **Validation** — offline evals pinned to snapshot dates and wired into CI; PR-granularity ablations ("design for null results"); online adversarial review (+6% accuracy at +32% tokens, +72% latency); a provenance footer (source tier, freshness, owner); and **active correction harvesting** — a scheduled agent scans Slack for correction language and opens a fix PR [^src6].

**Maintenance is the crux**: offline accuracy drifted from ~95% to ~65% over a month before they colocated skill markdown with the transformation models and added a hook flagging any reporting-model change that doesn't touch a skill file — now ~90% of data-model PRs include a skill change in the same diff [^src6]. The same skill must give the same answer across Slack, IDE, dashboards, and standalone sessions, achieved via one canonical source auto-synced to a plugin marketplace, cloud blobs, and MCP resources [^src6]. The hardest unsolved case is the **silent failure**: an answer that is wrong but plausible and used without objection [^src6].

> Practitioner echo: Chris Riccomini frames the same discipline as **"live in plan mode all the time"** — iterate the plan over many rounds until "there's no possible way the LLM can't implement the plan incorrectly" — plus quality gates (define → measure → enforce thresholds, e.g. a commit hook enforcing >90% coverage) and a Ralph-Loop for context management [^src8]. He argues AI will do the majority of DE work, and (speculatively) that "LLMs should speak Substrait, not SQL" — a transformation IR that expresses physical operators, enabling client-side query optimization and fewer tokens — while conceding LLMs are far more familiar with SQL [^src8].

## What it changes — and the limits

**Before**: business PRD → engineer manually writes technical spec → writes models → manually adds docs → PR review catches naming issues → rework [^src1]. **After**: the agent drives the mechanical translation, leaving humans to focus on scoping high-quality business requirements [^src1].

Stated limits and preconditions:
- Output quality depends on **input quality** — pre-process and dump the best possible business requirements ("as always") [^src1].
- The **people problem** (good requirements) and the **tooling problem** (right mix of workflows/tools to remove ambiguity) are both required [^src1].
- AI will "confidently write wrong things" if not supervised — you must understand the business, stakeholders, and use cases [^src1].
- Human review of generated code remains mandatory [^src2].

## Robin Moffatt's hands-on dbt assessment

A practitioner evaluation of Claude Code building a dbt project from scratch, using real data (UK Environment Agency flood monitoring API, DuckDB), run in March 2026 (Opus 4.6) — notable as an independent, less favorable data point compared to the vendor-friendly evaluations above [^src9].

**What Claude handled well** [^src9]:
- Autonomous ingestion loop via the Environment Agency API (6,190 stations, `curl` + `jq` shell script) without explicit instruction.
- Correct staging → dim/fact model structure with relational integrity and data contracts.
- Incremental fact table (`materialized='incremental'`, `unique_key=['date_time', 'measure_id']`).
- Handling messy pipe-delimited multi-value source columns (`split_part(value, '|', 1)`).
- SCD2 snapshots for station metadata.
- Autonomous debugging of `dbt build` failures: Jinja2 escape issues, deprecated test syntax, DuckDB direct queries to validate data quality.

**The failure modes** [^src9]:
- **Silent data scope error**: Python script capped at the API's default 2000-item limit; 5,458 actual stations, only 1,493 loaded. *"Wrong is worse than absent because you can't trust it."*
- **Silent column omissions**: dropped `gridReference`, `datumOffset`, `unit` without comment.
- **Scope taken too literally**: only implemented SCD2 for stations (as specified), not for measures — an engineer would have challenged that assumption.

**The headline conclusion** [^src9]: *"Claude Code is an amazing productivity companion. Do not, if you value your job, use it to one-shot a dbt project."* Claude produced 16 files including tests, documentation, and a README in minutes; a human junior engineer would take 3+ days. But the silent errors — wrong row counts, missing columns, a brittle ingestion script — required expert validation to catch.

> Moffatt's advice on context: the quality of output depended heavily on the dbt-agent-skills (from dbt Labs) provided in the prompt — Sonnet 4.5 with good skills produced respectable results; Opus 4.6 without skills was inconsistent. This directly supports the Anthropic analytics team's finding that *"without skills, accuracy didn't exceed 21%"* [^src6].

See [[data-engineering/dbt|dbt]] for the building-a-dbt-project-with-Claude-Code overview and [[data-engineering/ai-impact-on-data-engineering|AI's Impact on Data Engineering]] for the role-level framing.

## Cross-domain note

This page lives in **data-engineering** because the deliverable is dbt models and data architecture. The underlying techniques — agentic coding, custom **Skills**, and **MCP** servers — belong to the **ai-engineering** domain. When an ai-engineering hub exists, cross-link from there.

## See also

- [[data-engineering/agentic-data-modeling|Agentic Data Modeling]] — AI agents for schema design and impact analysis (OpenMetadata MCP, SchemaFlow, pg_infer)
- [[data-engineering/dbt|dbt]] — the transformation framework these workflows target; exposure enrichment detail
- [[data-engineering/dimensional-modeling|Dimensional Modeling]] — the modeling output (grain, dimensions, facts)
- [[ai-engineering/agent-skills|Agent Skills]] · [[ai-engineering/mcp|MCP]] — the underlying ai-engineering primitives
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [Hands-On Claude Code for Data Engineers: Data Modeling with dbt, Miro & PostgreSQL](../../raw/web/hands-on-claude-code-for-data-engineers-data-modeling-with-d.md)
[^src2]: [Create a dbt Project From Scratch w/ Claude Code](../../raw/email/email-2026-04-08-create-a-dbt-project-from-scratch-w-claude-code.md)
[^src3]: [Intro To Claude Code For Data Engineers (Skills, MCPs & Hooks)](../../raw/web/intro-to-claude-code-for-data-engineers-skills-mcps-hooks-fo.md)
[^src4]: [Claude Code For Data Engineers: Hands-On Projects For Your Daily Workflows](../../raw/email/email-2026-06-04-claude-code-for-data-engineers-hands-on-projects-for-your-da.md)
[^src5]: [feat: add metadata-exposure-enrichment skill and Metabase MCP (PR #10)](../../raw/web/feat-add-metadata-exposure-enrichment-skill-and-metabase-mcp.md)
[^src6]: [How Anthropic Enables Self-Service Data Analytics with Claude](../../raw/web/how-anthropic-enables-self-service-data-analytics-with-claud.md)
[^src7]: [TLDR Data: Anthropic's Automated Analytics, PostgreSQL 19 Beta, McKinney on Agentic Engineering](../../raw/email/email-2026-06-08-anthropics-automated-analytics-postgresql-19-beta-mckinney-o.md)
[^src8]: [Plan Mode All the Time, Substrait over SQL, and the End of the Data Engineer (Chris Riccomini interview)](../../raw/web/plan-mode-all-the-time-substrait-over-sql-and-the-end-of-the.md)
[^src9]: [Claude Code isn't going to replace data engineers (yet)](../../raw/web/web-claude-code-isnt-going-to-replace-data-engineers-yet.md)
