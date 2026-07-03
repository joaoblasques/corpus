---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/web/web-bi-as-code-for-data-engineers-faster-analytics-with-sql-mark.md
    channel: web
    ingested_at: 2026-06-17
aliases:
  - BI as Code
  - analytics as code
  - Evidence.dev
  - Lightdash
  - markdown dashboards
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-17
updated: 2026-06-17
---

# BI as Code

**TL;DR.** BI as Code treats dashboards as code artifacts: SQL queries embedded in Markdown files, version-controlled alongside dbt models, and deployable to static hosting [^src1]. Tools like Evidence.dev and Lightdash make this real. The entire analytics layer becomes a set of text files in Git — diff-able, reviewable in PRs, rollback-able, and portable across hosting providers without vendor lock-in [^src1].

## The problem with traditional BI

Traditional BI tools (Tableau, Power BI) suffer from four recurring failure modes [^src1]:

- A column name changes in the database → click through 15 dashboards to fix broken references.
- Someone asks "what changed?" → no diff, no commit history, just a screenshot someone took last month.
- Migrating to a different tool → rebuild everything from scratch because dashboards are locked in proprietary format.
- New team member joins → needs access, licenses, training on the specific tool, plus tribal knowledge.

The deeper problem: these tools treat analytics as a separate discipline from data engineering, while the rest of the stack (dbt, Airflow, pytest) is already code.

## How BI as Code works

The Example stack: PostgreSQL + dbt + Evidence.dev. The entire analytics layer is ~30 Markdown files [^src1]:

- Each file is a page.
- Each page has SQL queries embedded in code blocks.
- Queries pull from dbt models and render as interactive charts.
- Components handle rendering: `<BarChart>`, `<LineChart>`, `<BigValue>`, `<DataTable>`.

```markdown
```sql orders_by_channel
SELECT channel, count(*) as orders
FROM mart_orders
GROUP BY 1
```

<BarChart data={orders_by_channel} x=channel y=orders />
```

That is an entire dashboard page.

## Key advantages

### Native version control

Dashboards are just files in a repo [^src1]:

```
git diff reports/pages/channel-performance.md
```

Dashboard updates are reviewable in PRs. Breaking changes are rollback-able. If you know Git, BI as Code becomes dead easy.

### Co-location with data models

```
marketing-analytics/
├── dbt/
│   └── models/
│       ├── staging/
│       ├── intermediate/
│       └── marts/
└── reports/
    └── pages/
        ├── index.md
        ├── channels.md
        └── conversions.md
```

When you refactor a model, you update the queries in the same commit. Everything stays in sync because it is all just code — no more "the dashboard is broken because a column name changed and nobody told me" [^src1].

### Portable deployment

Evidence builds to static HTML. Deploy to Netlify, Vercel, GitHub Pages, or any static hosting. No vendor infrastructure, no special deployment process [^src1].

## When BI as Code makes sense

**Use it when** [^src1]:
- Your team already writes SQL and knows Git.
- You want analytics version-controlled alongside your data models.
- You value reproducibility and portability over fancy UI.

**Stick with traditional BI when** [^src1]:
- You need extremely complex interactivity (drill-through, dynamic filtering across 20 dimensions).
- You already have a mature BI practice with Tableau/Looker and it works fine.
- Your org requires specific compliance features only enterprise tools provide.

## Relationship to the data stack

BI as Code is the natural downstream evolution of **analytics as code** that started with dbt [^src1]. The progression: version-controlled transformations (dbt) → version-controlled dashboards (Evidence/Lightdash). It also pairs well with AI: Markdown is the language LLMs work well with, making it feasible to generate or refine dashboard pages with AI assistance.

> *"The future of analytics is as simple as SQL files within markdown pages that do exactly what you need."* [^src1]

Note: the source is from an author who advocates for this approach based on personal project experience — treat as practitioner opinion, not industry consensus.

## Related

- [dbt](/data-engineering/dbt.md) — provides the transformed models that BI as Code dashboards query
- [Semantic Layer](/data-engineering/semantic-layer.md) — complements BI as Code by providing a shared metric layer
- [Pipeline Layers](/data-engineering/pipeline-layers.md) — the marts layer that BI tools sit on top of
- [CI/CD for Data Infrastructure](/data-engineering/cicd-for-data-infrastructure.md) — the same Git-based workflow applies to dashboard deployment

[^src1]: [BI as Code for Data Engineers: Faster Analytics With SQL & Markdown](../../raw/web/web-bi-as-code-for-data-engineers-faster-analytics-with-sql-mark.md)
