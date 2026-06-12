---
channel: email
source: gmail
gmail_message_id: 19e62b61533c5543
from: Vu Trinh <vutr@substack.com>
subject: 5 insights to help you learn any open table format faster
date_received: 2026-05-26
pointer: false
collected_at: 2026-06-11
links:
  - {url: "https://substack.com/redirect/ca97899d-e8fb-495f-b838-55df105b4cc8?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: false, score: 6, reason: duplicate}
  - {url: "https://substack.com/redirect/e0ce6e47-d489-4dc7-b15c-3cf67c7587c3?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: false, score: 1, reason: low-utility}
corpus_ingested: true
corpus_ingested_at: 2026-06-11
corpus_pages:
  - corpus/data-engineering/open-table-formats.md
---

View this post on the web at https://vutr.substack.com/p/5-insights-to-help-you-learn-any

I invite you to join my paid membership list for only 7$/month (pay annually) to get access to:
This article and 200+deep-dive data engineering articles
learn-spark: a CLI tool to master Apache Spark internals
learn-dbt: a CLI tool to master dbt from the ground up
learn_airflow: a CLI tool that equips you with all the Airflow fundamentals
All future learning tools → Tools Demo [ https://substack.com/redirect/ca97899d-e8fb-495f-b838-55df105b4cc8?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]
If you’re a student with an education email, use this 50% ANNUAL DISCOUNT [ https://substack.com/redirect/e0ce6e47-d489-4dc7-b15c-3cf67c7587c3?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]
If you’re a Vietnamese user, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get 50% OFF the annual plan.
Intro
Open table formats like Iceberg, Hudi, or Iceberg are still one of the hottest topics in data engineering. (AI is still the top 1).
The “table format” is not only a trendy or marketing term anymore.
It’s earning the trust of more and more organizations, making itself a key part of many companies’ data infrastructure. Besides the big three: Iceberg, Hudi, and Delta Lake, more players have entered the market, such as Paimon or DuckLake.
Thus, I find it helpful to have a guideline for learning these table formats faster, as I believe there are some fundamentals shared across these formats, and once you learn them, you can scale your learning super fast.
This article will do exactly that: a set of insights/observations that help you pick up any table formats in hours.
Note: This article doesn’t dive into any table format. For that purpose, please refer to my other articles.
The Metadata Layer
…as the Source of Truth
When you store data as Parquet files on S3, those are just objects.
However, we, as users, usually work with data in a more friendly abstraction: a table.
Thus, we must have a way to “see“ these files as a table.  More precisely, every database’s query engine must have a way. From Snowflake, BigQuery, Redshift, Databricks, or even PostgreSQL. All must have a “translator“ to help them “see” the files as a table.
To do this, all the databases have a metadata layer for this purpose. Believe it or not, this is the main idea behind any table format out there, from Iceberg to Delta Lake.
The biggest difference is that Iceberg, Delta Lake, or Hudi is a separate metadata layer.
No database dependence. That’s why they got the “open“ before the “table formats“. 
—
If you’re going to pick up any table formats, remember this:
I invite you to join my paid membership list for only 7$/month (pay annually) to get access to:
This article and 200+deep-dive data engineering articles
learn-spark: a CLI tool to master Apache Spark internals
learn-dbt: a CLI tool to master dbt from the ground up
learn_airflow: a CLI tool that equips you with all the Airflow fundamentals
All future learning tools → Tools Demo [ https://substack.com/redirect/ca97899d-e8fb-495f-b838-55df105b4cc8?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]
If you’re a student with an education email, use this 50% ANNUAL DISCOUNT [ https://substack.com/redirect/e0ce6e47-d489-4dc7-b15c-3cf67c7587c3?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]
If you’re a Vietnamese user, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get 50% OFF the annual plan...

Unsubscribe https://substack.com/redirect/2/eyJlIjoiaHR0cHM6Ly92dXRyLnN1YnN0YWNrLmNvbS9hY3Rpb24vZGlzYWJsZV9lbWFpbD90b2tlbj1leUoxYzJWeVgybGtJam94TURjek9ERXhMQ0p3YjNOMFgybGtJam94T1RneU1UVTRNVEFzSW1saGRDSTZNVGMzT1RjM01qVTFPQ3dpWlhod0lqb3hPREV4TXpBNE5UVTRMQ0pwYzNNaU9pSndkV0l0TVRrek1EY3dOU0lzSW5OMVlpSTZJbVJwYzJGaWJHVmZaVzFoYVd3aWZRLllSaDRRcjZrbFR1ZHlfbUhXSVFIVzJ2WFExeDlNcUdUQlhPTTFIcGFPejAiLCJwIjoxOTgyMTU4MTAsInMiOjE5MzA3MDUsImYiOnRydWUsInUiOjEwNzM4MTEsImlhdCI6MTc3OTc3MjU1OCwiZXhwIjoyMDk1MzQ4NTU4LCJpc3MiOiJwdWItMCIsInN1YiI6ImxpbmstcmVkaXJlY3QifQ.n75jinVOmJaifSPB0mkI6KUKGAYb-2dj7EN0vMCrjxI?
