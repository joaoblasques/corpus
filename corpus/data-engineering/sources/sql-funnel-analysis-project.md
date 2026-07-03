---
type: source
domain: data-engineering
status: draft
sources:
  - path: raw/youtube/youtube-U-JlXWDqvco-watch-me-do-a-data-analyst-project-in-minutes-with-sql.md
    channel: youtube
    ingested_at: 2026-06-15
aliases:
  - SQL funnel analysis
  - sales funnel SQL
  - data analyst SQL project
  - conversion rate SQL
tags:
  - corpus/data-engineering
  - source
created: 2026-06-15
updated: 2026-06-15
---

# Source: End-to-End SQL Sales-Funnel Analysis (Lore So What)

**TL;DR.** A 30-minute end-to-end SQL data-analytics walkthrough (Lore So What, ex-Deloitte senior analyst / ex-AWS analytics lead) on **Google BigQuery**, using e-commerce event data to build a **sales-funnel analysis** [^src1]. The throughline: *SQL is a tool, not the goal* — the analyst's real job is turning queries into business insight and stakeholder recommendations [^src1]. A practical reference for funnel/conversion SQL patterns ([CTEs, conditional aggregation](/data-engineering/sql-window-functions.md)) tied to real domain reasoning.

## Setup

BigQuery (browser-based, free, no install) — upload CSV, auto-detect schema, skip 1 header row [^t0]. Data is e-commerce user events: `event_id`, `user_id`, `event_type` (page_view → add_to_cart → checkout_start → payment_info → purchase), `event_date`, `product_id`, `amount`, traffic `source` [^t286].

## Analyses built

1. **Funnel stage counts** — a CTE with `COUNT(DISTINCT CASE WHEN event_type = '<stage>' THEN user_id END)` per stage, filtered to the last 30 days via `event_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)` [^t338]. Result: users shrink down the funnel (~4,000 views → ~1,300 cart → …) [^t549].
2. **Conversion rates** — divide adjacent stages (`stage2_cart * 100 / stage1_views`) for view→cart, cart→checkout, etc., plus overall conversion [^t602]. *Insight:* payment→purchase ~92% (no technical bottleneck), view→cart ~30% is the weakest link → flag website/product-display experience [^t736].
3. **Funnel by traffic source** — `GROUP BY traffic_source` to compare channels [^t818]. *Insight:* social drives high views but low conversion (a **vanity metric**), while **email** converts far better (~63% cart rate) → recommend shifting budget from social to email [^t1054].
4. **Time-to-conversion** — `MIN(event_date)` per stage per user with a `HAVING` clause requiring an actual purchase, then `TIMESTAMP_DIFF(..., MINUTE)` for view→cart, cart→purchase, total-journey averages [^t1136]. Sanity-check for bot-like (too-fast) or stalled journeys [^t1320].
5. **Revenue funnel** — `COUNT(DISTINCT user_id)` visitors/buyers, `SUM(CASE WHEN purchase THEN amount)` revenue, and finance KPIs: **average order value (AOV)**, revenue/buyer, revenue/visitor [^t1428]. *Insight:* compare AOV against **CAC** (customer acquisition cost) to judge paid-ads profitability — AOV $107 vs $50 CAC is profitable; vs $150 CAC is a loss [^t1536].

## The takeaway

The deliverable is not the SQL — it's three stakeholder recommendations (UX: don't touch the working checkout flow; marketing: stop over-investing in social, double down on email; finance: watch AOV vs CAC), drafted for an email or slide deck [^t1641]. Demonstrates the ["business value first"](/data-engineering/data-engineer-role.md) principle in an analytics context.

## Techniques worth reusing

- Conditional aggregation (`COUNT(DISTINCT CASE WHEN …)`) to pivot event rows into funnel columns [^t364].
- Chained CTEs, building each analysis from the previous query [^t1107].
- Running a CTE alone as an intermediate debugging step [^t872].
- Honest, error-and-debug-as-you-go style (missed commas, wrong `DATE_SUB` syntax) modelling real analyst workflow [^t522].

## Related

- [SQL Window Functions](/data-engineering/sql-window-functions.md) — adjacent SQL-analytics reference
- [The Data Engineer Role](/data-engineering/data-engineer-role.md) — insight/recommendation over raw querying
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [Watch me Do a Data Analyst Project in minutes with SQL (Lore So What)](../../../raw/youtube/youtube-U-JlXWDqvco-watch-me-do-a-data-analyst-project-in-minutes-with-sql.md)
[^t0]: [02:10](../../../raw/youtube/youtube-U-JlXWDqvco-watch-me-do-a-data-analyst-project-in-minutes-with-sql.md#t=2:10)
[^t286]: [04:46](../../../raw/youtube/youtube-U-JlXWDqvco-watch-me-do-a-data-analyst-project-in-minutes-with-sql.md#t=4:46)
[^t338]: [05:38](../../../raw/youtube/youtube-U-JlXWDqvco-watch-me-do-a-data-analyst-project-in-minutes-with-sql.md#t=5:38)
[^t364]: [06:04](../../../raw/youtube/youtube-U-JlXWDqvco-watch-me-do-a-data-analyst-project-in-minutes-with-sql.md#t=6:04)
[^t522]: [08:42](../../../raw/youtube/youtube-U-JlXWDqvco-watch-me-do-a-data-analyst-project-in-minutes-with-sql.md#t=8:42)
[^t549]: [09:09](../../../raw/youtube/youtube-U-JlXWDqvco-watch-me-do-a-data-analyst-project-in-minutes-with-sql.md#t=9:09)
[^t602]: [10:02](../../../raw/youtube/youtube-U-JlXWDqvco-watch-me-do-a-data-analyst-project-in-minutes-with-sql.md#t=10:02)
[^t736]: [12:16](../../../raw/youtube/youtube-U-JlXWDqvco-watch-me-do-a-data-analyst-project-in-minutes-with-sql.md#t=12:16)
[^t818]: [13:38](../../../raw/youtube/youtube-U-JlXWDqvco-watch-me-do-a-data-analyst-project-in-minutes-with-sql.md#t=13:38)
[^t872]: [14:32](../../../raw/youtube/youtube-U-JlXWDqvco-watch-me-do-a-data-analyst-project-in-minutes-with-sql.md#t=14:32)
[^t1054]: [17:34](../../../raw/youtube/youtube-U-JlXWDqvco-watch-me-do-a-data-analyst-project-in-minutes-with-sql.md#t=17:34)
[^t1107]: [18:27](../../../raw/youtube/youtube-U-JlXWDqvco-watch-me-do-a-data-analyst-project-in-minutes-with-sql.md#t=18:27)
[^t1136]: [18:56](../../../raw/youtube/youtube-U-JlXWDqvco-watch-me-do-a-data-analyst-project-in-minutes-with-sql.md#t=18:56)
[^t1320]: [22:00](../../../raw/youtube/youtube-U-JlXWDqvco-watch-me-do-a-data-analyst-project-in-minutes-with-sql.md#t=22:00)
[^t1428]: [23:48](../../../raw/youtube/youtube-U-JlXWDqvco-watch-me-do-a-data-analyst-project-in-minutes-with-sql.md#t=23:48)
[^t1536]: [25:36](../../../raw/youtube/youtube-U-JlXWDqvco-watch-me-do-a-data-analyst-project-in-minutes-with-sql.md#t=25:36)
[^t1641]: [27:21](../../../raw/youtube/youtube-U-JlXWDqvco-watch-me-do-a-data-analyst-project-in-minutes-with-sql.md#t=27:21)
