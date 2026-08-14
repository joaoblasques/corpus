---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-how-we-built-an-internal-data-analytics-agent-1c1b2656.md
    channel: web
    ingested_at: 2026-08-14
aliases: []
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-14
updated: 2026-08-14
---

# How GitHub Built Qubot: An Internal Data Analytics Agent

**TL;DR.** GitHub's Qubot is a Copilot-powered analytics agent that lets any employee query the data warehouse in natural language via Slack, VS Code, or the Copilot CLI. Its key architectural lesson: a well-curated context layer makes the agent three times faster at returning correct answers.[^src1]

## Architecture: three components

1. **User interface**: Slack (zero config, spawns a Copilot Cloud Agent per question), VS Code plugin, Copilot CLI plugin.[^src1]
2. **Context layer**: Federated; each product/business team owns their domain context. A context agent ingests, organizes, and normalizes contributions via a standardized template. Context is loaded at runtime via the GitHub MCP Server.[^src1] The layer is enriched continuously via ETL pipelines.
3. **Query engine**: Kusto (fast, recent event data) + Trino (complex joins, historical analysis). Qubot defaults to Kusto and auto-switches to Trino when the question demands it.[^src1]

## Key lessons

- **Context layer is decisive**: structured, well-curated context made Qubot 3× faster at finding the right answer vs. unstructured experiments.[^src1]
- **Analytics context becomes a first-class artifact**: the quality of the context layer matters as much as data modeling — it surfaces analytics knowledge that was previously in people's heads.[^src1]
- **Hub-and-spoke execution**: Qubot acts as a gravitational center; partner teams contribute context to a single shared tool rather than building their own siloed agents.[^src1]
- **Eval-before-ship**: every change to the context layer is evaluated offline before merging — a CI pipeline for agent quality.[^src1]
- **Results archived as PRs**: answers are stored as markdown reports in pull requests, giving users a stable reference to refine queries or feed into dashboards.[^src1]

## Impact

Hundreds of users running thousands of queries. Volume of basic data questions in Slack channels dropped significantly; non-technical users gained direct data warehouse access for the first time.[^src1]

[^src1]: [How we built an internal data analytics agent](https://github.blog/ai-and-ml/github-copilot/how-we-built-an-internal-data-analytics-agent/) — GitHub Blog, 2026-06-29 (raw/web/web-how-we-built-an-internal-data-analytics-agent-1c1b2656.md)
