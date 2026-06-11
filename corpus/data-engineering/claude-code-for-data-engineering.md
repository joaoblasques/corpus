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
  # Cross-domain: also relevant to ai-engineering (agentic coding, Skills, MCP)
aliases:
  - Claude Code dbt
  - AI data modeling
  - AI-assisted dbt
tags:
  - corpus/data-engineering
  - synthesis
created: 2026-06-11
updated: 2026-06-11
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

## Exposure enrichment / BI lineage

A third, closely related application: using Claude Code to enrich [[data-engineering/dbt|dbt]] **exposures** so they form a lean data catalog with end-to-end model → dashboard → card/column lineage — without a dedicated metadata platform. See [[data-engineering/dbt|dbt]] § Exposures and lineage for the detailed workflow (Metabase MCP discovery loop, impact analysis).

## What it changes — and the limits

**Before**: business PRD → engineer manually writes technical spec → writes models → manually adds docs → PR review catches naming issues → rework [^src1]. **After**: the agent drives the mechanical translation, leaving humans to focus on scoping high-quality business requirements [^src1].

Stated limits and preconditions:
- Output quality depends on **input quality** — pre-process and dump the best possible business requirements ("as always") [^src1].
- The **people problem** (good requirements) and the **tooling problem** (right mix of workflows/tools to remove ambiguity) are both required [^src1].
- AI will "confidently write wrong things" if not supervised — you must understand the business, stakeholders, and use cases [^src1].
- Human review of generated code remains mandatory [^src2].

## Cross-domain note

This page lives in **data-engineering** because the deliverable is dbt models and data architecture. The underlying techniques — agentic coding, custom **Skills**, and **MCP** servers — belong to the **ai-engineering** domain. When an ai-engineering hub exists, cross-link from there.

## See also

- [[data-engineering/dbt|dbt]] — the transformation framework these workflows target; exposure enrichment detail
- [[data-engineering/dimensional-modeling|Dimensional Modeling]] — the modeling output (grain, dimensions, facts)
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [Hands-On Claude Code for Data Engineers: Data Modeling with dbt, Miro & PostgreSQL](../../raw/web/hands-on-claude-code-for-data-engineers-data-modeling-with-d.md)
[^src2]: [Create a dbt Project From Scratch w/ Claude Code](../../raw/email/email-2026-04-08-create-a-dbt-project-from-scratch-w-claude-code.md)
