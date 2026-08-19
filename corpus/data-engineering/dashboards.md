---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/_inbox/web-what-are-dashboards-7f0a8254.md
    channel: web
    ingested_at: 2026-08-19
aliases:
  - dashboard
  - BI dashboard
  - business intelligence dashboard
  - operational dashboard
  - analytical dashboard
  - strategic dashboard
  - tactical dashboard
  - AI/BI dashboard
confidence: 0.9
last_confirmed: 2026-08-19
tags:
  - data-engineering
  - bi
  - analytics
  - dashboards
created: 2026-08-19
updated: 2026-08-19
---

# Dashboards

**TL;DR**: A dashboard is a live visual interface combining multiple metrics and charts into one screen so users can see performance at a glance, spot anomalies, and decide what to do next. Distinguished from reports (static, narrative) and scorecards (KPI-against-target only). Modern dashboards query data directly rather than storing copies.

## Definition and architecture

A dashboard is the visual layer on top of data: data source → query/pipeline → visualization layer → user interface. Modern dashboards refresh on a schedule or in real time as underlying data changes, querying directly rather than storing a separate copy.[^databricks]

Test for whether a dashboard is well-designed: "What is this dashboard for?" — a single sentence answer. Knowing the audience and purpose determines refresh cadence, metric selection, interactivity needs, and permissions.[^databricks]

## Dashboard types

| Type | Primary audience | Time horizon | Update frequency | Example metrics |
|---|---|---|---|---|
| **Operational** | Frontline teams, ops managers | Right now / today | Real-time or near real-time | Live order volume, system uptime, support queue length |
| **Analytical** | Analysts, data teams | Days to months | Daily or on-demand | Funnel conversion, cohort retention, root-cause breakdowns |
| **Strategic** | Executives, leadership | Quarter, year, multi-year | Weekly or monthly | Revenue vs. plan, market share, customer growth |
| **Tactical** | Mid-level managers, department leads | Weeks to a quarter | Daily or weekly | Campaign performance, sprint velocity, regional sales targets |

In practice these overlap — a single dashboard often serves multiple audiences. Think of them as design starting points, not rigid containers.[^databricks]

## Dashboard vs. report vs. scorecard

| Term | What it is | Primary purpose | Updates |
|---|---|---|---|
| **Dashboard** | Live visual interface, multiple metrics | Monitor and act | Refreshes automatically |
| **Report** | Structured document on a specific question/period | Explain what happened | Generated on schedule or one-off |
| **Scorecard** | Focused view tracking a small set of KPIs vs. targets | Show whether goals are being hit | Usually periodic |
| **Data visualization** | Single chart or graphic | Communicate one pattern | As needed |

## What a good dashboard answers

Seven questions a well-designed dashboard should answer clearly:[^databricks]
1. What happened?
2. When did it happen?
3. How big was the change?
4. What should be compared against it?
5. Why does the result look the way it does?
6. Who is responsible for it?
7. What should the viewer do next?

Most dashboards handle questions 1–4 well. Questions 5–7 require intentional design: drill-downs, clear data ownership, action-oriented layout.

## Static vs. real-time vs. interactive

- **Static**: fixed snapshot, doesn't auto-refresh — useful for periodic reporting, quarter-close archiving
- **Real-time**: refreshes continuously (seconds to minutes) — common in operations, security, support; higher infrastructure cost
- **Interactive**: users can filter, drill down, change date ranges — most modern BI dashboards; moves users from passive consumers to active investigators[^databricks]

These are orthogonal dimensions, not exclusive categories.

## AI and the evolution of dashboards

AI tooling (e.g., Databricks Genie) allows business users to ask questions in plain English and get answers grounded in governed data. Dashboards handle predefined views teams return to regularly; conversational AI handles ad-hoc questions outside those views.[^databricks]

Key limitation: AI-generated dashboards are only as good as the data and governance behind them. If "revenue" means different things in different systems, AI will confidently surface both and call them the same metric. Good governance and consistent metric definitions at the data layer are prerequisites.[^databricks]

The Databricks AI/BI design principle: dashboards run directly on governed data with integrated semantics ensuring one version of the truth across BI dashboards, AI agents, and downstream tools.[^databricks]

## Common failure modes

Dashboards fail not because of the tool but because of design choices:[^databricks]
- No clear single purpose
- Audience not defined
- Metric definitions inconsistent across sources ("revenue" mismatch)
- No governance layer; AI additions amplify inconsistency

## Related

- [/data-engineering/bi-as-code.md](/data-engineering/bi-as-code.md)
- [/data-engineering/semantic-layer.md](/data-engineering/semantic-layer.md)
- [/data-engineering/data-quality.md](/data-engineering/data-quality.md)
- [/data-engineering/modern-data-stack.md](/data-engineering/modern-data-stack.md)
- [/data-engineering/databricks.md](/data-engineering/databricks.md)

[^databricks]: Databricks, "What are Dashboards?" databricks.com/blog, 2026. `raw/_inbox/web-what-are-dashboards-7f0a8254.md`
