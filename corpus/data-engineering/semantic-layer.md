---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/web/onboarding-ai-why-the-semantic-layer-matters.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/web/data-teams-should-become-context-teams.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/email/email-2026-05-20-i-started-my-career-in-tableau.md
    channel: email
    ingested_at: 2026-06-15
aliases:
  - semantic layer
  - metric layer
  - knowledge layer
  - context engineering
  - context team
  - agentic architect
  - knowledge architect
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-15
updated: 2026-06-15
---

# Semantic Layer

**TL;DR.** A **semantic layer** formalises the institutional knowledge that usually lives in senior analysts' heads — shared, findable, consistent definitions of what fields, metrics, and labels *mean* (what counts as "revenue", how "active user" is defined, that an "X" means soft-delete) [^src1]. It sits between raw data and consumers. Long treated as a "nice-to-have," it has become **critical AI infrastructure**: without it, LLMs hallucinate confident-but-wrong numbers; with it, accuracy can jump dramatically [^src1]. The role evolution: data analysts becoming **agentic / knowledge architects**, and data teams becoming **context teams** [^src3][^src2].

## What it is

In a data context, semantics is the *meaning* behind fields, metrics, and labels — usually learned informally over years [^src1]. A semantic layer replicates that knowledge formally, providing shared definitions easy to find and consistent across teams [^src1]. It ranges from [^src1]:
- a small **glossary** of business terms,
- a set of **taxonomies / entity definitions** (see [[data-engineering/data-modeling-meaning|meaning in data modeling]]),
- a simple **YAML metric definition**, e.g.:

```yaml
metrics:
  - name: monthly_recurring_revenue
    description: "MRR from paying customers, normalised to AUD"
    calculation: SUM(subscriptions.amount * exchange_rates.rate)
    filters:
      - subscriptions.status = 'active'
      - subscriptions.plan_type != 'trial'
```
- up to a full **knowledge graph** of how concepts relate [^src1].

Whatever the form, the purpose is the same: clear, reliable definitions of what data means — capturing not just metadata (tables/columns) but **business meaning** [^src1].

## Why it's now critical: onboarding AI

The semantic layer plays the role of *onboarding* for generative AI — giving the agent the context to do its job well immediately [^src1]. Ask an LLM "How much revenue last month?" without it, and it may count refunds, include deleted transactions, and mis-convert currency — confidently wrong, hard to detect [^src1]. Research cited (Sequeda & Allemang, 2025): pairing LLMs with business semantics via ontologies/knowledge graphs raised question-answering accuracy **from 16% to 72%** vs querying raw databases directly [^src1]. "Generative AI eats semantics for breakfast" — it cannot tap you on the shoulder to ask whether revenue includes refunds; it needs that written down and accessible [^src1].

This is the modeling complement to [[data-engineering/progressive-disclosure-analytics-agents|progressive disclosure]] — semantics is *what* the agent must know; progressive disclosure governs *when* to load it.

## Data teams → context teams

A provocative reframing: **AI agents today are the equivalent of a BI tool plugged straight into the production database** — it kind of works but you can't trust the answers [^src2]. We fixed that for data with data stacks; we need the same for context [^src2]:

> Context engineering = data governance + data engineering + data sciences [^src2].

- **Context governance** — a single, governed, versioned **source of truth** for company knowledge ("what's our refund policy?" shouldn't depend on which doc the agent finds first) [^src2].
- **Context stack (ETL for context)** — the missing middle layer: ingestion to pull context sources, transformation to pick the source of truth, a context layer, orchestration for freshness, and AI monitoring [^src2].
- **Context sciences** — treat it like ML: define success metrics (answer rate, accuracy, cost, speed), build prompt/expected-answer unit tests, change context, re-measure, keep what works [^src2].

Trade-off to optimise: too little context → wrong/no answers; too much → expensive (token cost) and confused by noise [^src2]. File-system AI agents (Claude Code, Cowork, Cursor, Codex) are a good starting point because context lives in editable, measurable files [^src2].

## The "agentic architect" role shift

From the Tableau Conference report: data analysts are no longer just building dashboards — they're becoming **agentic / knowledge architects** [^src3]. Key shifts [^src3]:
- **Knowledge is the new data** — AI agents can't act on data alone; every metric/business definition must be clearly defined (Tableau's Knowledge Engine cited as built on 33M semantic models).
- **Dashboards aren't the destination** — via headless analytics and secure MCP connections, insights surface directly in Slack, Teams, Claude, ChatGPT.
- **Conversational analytics** — natural language over the data, no SQL required.
- The CMO's framing: AI gives everyone *access to answers, but not the right answers* — someone must understand business context, define metrics correctly, and verify accuracy. That person — bridging raw data and trusted AI output — is the **agentic/knowledge architect** [^src3]. Example: Salesforce's "ACV" and Feb-start fiscal year are company-specific definitions an agent would otherwise guess at [^src3].

> Note: the Tableau source is a vendor-conference writeup; treat product/role claims as promotional framing of a real trend, not neutral analysis.

## Related

- [[data-engineering/data-modeling-meaning|Meaning in Data Modeling]] — semantics/ontology/taxonomy foundations
- [[data-engineering/progressive-disclosure-analytics-agents|Progressive Disclosure for Analytics Agents]] — *when* to load semantic context
- [[data-engineering/data-quality|Data Quality]] · [[data-engineering/dbt|dbt]] (dbt metrics)
- [[ai-engineering/context-engineering|Context Engineering]] · [[ai-engineering/rag|RAG]] (ai-engineering)
- [[data-engineering/ai-impact-on-data-engineering|AI's Impact on Data Engineering]]
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [Onboarding AI: Why the Semantic Layer Matters](../../raw/web/onboarding-ai-why-the-semantic-layer-matters.md)
[^src2]: [Data teams should become context teams](../../raw/web/data-teams-should-become-context-teams.md)
[^src3]: [I Started My Career in Tableau (Jess Ramos, Big Data Energy)](../../raw/email/email-2026-05-20-i-started-my-career-in-tableau.md)
