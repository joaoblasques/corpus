---
channel: email
source: gmail
gmail_message_id: 19e27dfc1828fa24
from: "\"Ale from The Pipe & The Line\" <thepipeandtheline@substack.com>"
subject: "How To Connect Data Models To Your BI With Claude Code,  dbt exposures & MCPs"
date_received: 2026-05-14
pointer: false
collected_at: 2026-06-11
links:
  - {url: "https://substack.com/redirect/89b07c7a-15b1-45fe-bbf3-5832453b514b?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 8, file: raw/web/github-getnao-nao-mcp-servers.md}
  - {url: "https://substack.com/redirect/711effa6-d0b7-45d8-95d6-7b274ed01e4c?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 8, file: raw/web/feat-add-metadata-exposure-enrichment-skill-and-metabase-mcp.md}
  - {url: "https://substack.com/redirect/25a98ef7-e8dc-446f-a09b-ac8889136f86?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 7, file: raw/web/github-aboyalejandro-agentic-data-modeling-showcasing-ai-dat.md}
  - {url: "https://substack.com/redirect/c4c796fb-f061-4f34-b409-929a665d2f2e?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: false, score: 7, reason: duplicate}
  - {url: "https://substack.com/redirect/ff8fb9df-2a20-42a2-95ce-d23cfe6153a6?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: false, score: 6, reason: duplicate}
  - {url: "https://substack.com/redirect/98592ffe-eb78-421f-b388-edcebd572119?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 6, file: raw/web/mcp-server-metabase-documentation.md}
  - {url: "https://substack.com/redirect/8d6c8abc-a2d3-4e2d-81c1-40ae7610f5ba?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 5, file: raw/web/add-exposures-to-your-dag-dbt-developer-hub.md}
  - {url: "https://substack.com/redirect/279c43a1-9732-4aa8-bb3b-e9f8188c9837?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 5, file: raw/web/the-ai-data-modeling-tax-working-on-human-readiness-before-a-e068d044.md}
  - {url: "http://localhost:3000/dashboard/2", fetched: false, score: 2, reason: low-utility}
corpus_ingested: true
corpus_ingested_at: 2026-06-11
corpus_pages:
  - corpus/data-engineering/dbt.md
---

View this post on the web at https://thepipeandtheline.substack.com/p/how-to-connect-data-models-to-your

Hi there! Alejandro here 😊
Subscribe if you like to read about technical data & AI learnings, deep dives!
Enjoy the reading and let me know in the comments what you think about it 👨🏻‍💻
📝 TL;DR
dbt exposures document which dashboards depend on your models, but nobody maintains them
A barebones exposure links to a dashboard but tells AI nothing about what’s inside it
A custom metadata-exposure-enrichment skill uses the nao-metabase-mcp-server to query Metabase directly: discover cards, map columns to dbt models, and write structured metadata back into your exposure
The result: enriched exposures work as a lean data catalog. End-to-end lineage from dbt models to dashboard cards, no metadata platform required
Let’s think of a typical scenario.
You rename total_conversions to conversions_total in your dbt model because consistency matters.
Everything green an deployed.
Three hours later your Slack blows up: “Executive dashboard is broken, CFO is asking questions.”
End to end lineage was a huge challenge and still is, but with AI it’s been proven that connecting the right dots you can save a lot of pain (I’ve been insisting with this lately so check any of my latest articles)
dbt exposures were designed to document which external assets such as dashboards, reports or ML pipelines depend on your dbt models. 
And it has gain more traction since you can enrich them to tweak your AI to understand what will break beyond your dbt project every time you touch something.
Let’s see how to leverage them with AI.
A Better Way Of Using Exposures 
dbt exposures [ https://substack.com/redirect/8d6c8abc-a2d3-4e2d-81c1-40ae7610f5ba?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] have been around for a while now and defining YAML files with metadata is quite simple.
In practice, you see that weekly_dbt_metrics asset relies on fct_dbt_projects and stg_github_starts
But then you have real life, with deadlines, pressure and “I have other priorities” statements where maintenance of these things becomes impossible. 
What actually happens:
Analytics engineer builds a new dashboard
Add exposure to the YAML (if they remember) 
Two months pass, someone changes the underlying model
Nobody updates the exposure definition
The exposure docs become outdated. Or was never written at all
Best case scenario, nobody checks the dashboards and no one complains, so you are silently happy. Worst case scenario, you are merging broken lineage consistenly.
Now with skills, slash commands, CLAUDE.md, and many other cool AI shiny things there’s no excuse for this. 
Thanks for reading The Pipe & The Line! This post is public so feel free to share it.
📦 End To End Lineage With Exposures
Let’s say you’re working with the agentic-data-modeling [ https://substack.com/redirect/25a98ef7-e8dc-446f-a09b-ac8889136f86?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] repo. 
You have a Metabase dashboard showing marketing campaign performance. 
Most teams would write something like this, if they write anything at all:
version: 2

exposures:
  - name: agentic_data_modeling_demo
    type: dashboard
    url: http://localhost:3000/dashboard/2
    depends_on:
      - ref('campaign_performance')
      - ref('daily_summary')
This links a dashboard to two dbt models. There’s no context about what’s in the dashboard, what questions it answers, which columns matter, or who cares if it breaks.
As we discussed in Data Engineers Are Becoming MetadataOps Engineers [ https://substack.com/redirect/ff8fb9df-2a20-42a2-95ce-d23cfe6153a6?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ], every description you write is now a prompt for AI reasoning. 
This barebones exposure is an incomplete prompt. If you ask Claude “what breaks if I rename total_conversions?”, it knows the dashboard depends on campaign_performance, but has no idea whether any card actually uses that column.
This is where most teams stop. The exposure exists, technically. But it’s a pointer with no payload.
The good news: this barebones version is all you need as a starting point. The AI can figure out the rest.
The Exposure Enrichment Skill 🔌
The metadata-exposure-enrichment skill automates the whole discovery loop. It uses the nao-metabase-mcp-server [ https://substack.com/redirect/89b07c7a-15b1-45fe-bbf3-5832453b514b?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] to give Claude Code direct access to your Metabase instance: dashboards, questions, metadata, everything.
⚠️ Disclaimer: I prepared this article before Metabase 60 included MCP server [ https://substack.com/redirect/98592ffe-eb78-421f-b388-edcebd572119?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ], but I am still preferring nao one since its way more rich in the tooling exposed. 
Here’s the workflow:
1. Discover the dashboard
metabase-list-dashboards to find what’s out there, then metabase-get-dashboard on the specific one. Claude gets the full card list and the dashboard structure.
2. Inspect each card
Each card on a Metabase dashboard is a saved question. metabase-get-question shows what MBQL query or native SQL each card runs, plus its display type.
For the “Agentic Data Modeling Demo” dashboard, Claude discovers 6 cards: ROAS (KPI scalar), CR% (KPI scalar), Target Revenue (progress bar), Daily Spend by Channel (bar chart), Desktop Per Channel (pie), and Mobile Per Channel (pie).
3. Map columns to models
metabase-get-database-metadata cross-references table and column structures. Now Claude knows exactly which columns each card pulls from which model: roas, conversion_rate, total_revenue, desktop_sessions, mobile_sessions from campaign_performance, and spend from campaigns_daily (the raw source table).
4. Write the metadata back
Claude takes everything it discovered and enriches the exposure:
And you get something like this:
version: 2

exposures:
  - name: agentic_data_modeling_demo
    type: dashboard
    maturity: low
    url: http://localhost:3000/dashboard/2
    description: >
      [Business Purpose] Marketing performance dashboard used to
      monitor campaign ROI, conversion efficiency, revenue targets,
      and channel-level spend and device breakdown. Supports daily
      decision-making on budget allocation and channel optimization.

      [Cards] 6 cards:
      (1) ROAS -- smartscalar showing average return on ad spend over time.
      (2) CR% -- smartscalar showing average conversion rate over time.
      (3) Target Revenue -- progress bar tracking cumulative revenue
      against a 100k goal.
      ...
    owner:
      name: The Pipe & The Line
      email: ...
    depends_on:
      - ref('campaign_performance')
      - ref('daily_summary')
      - source('marketing_raw', 'campaigns_daily')
The format follows the same bracketed-header pattern used in the agentic-data-modeling [ https://substack.com/redirect/25a98ef7-e8dc-446f-a09b-ac8889136f86?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] repo’s dbt schema: [Business Purpose], [Known Issues / Caveats], extended with [Cards], [Key Columns], and [Data Sources] for exposure-specific context. Same AI readiness checks from the MetadataOps article applied to the BI layer.
Maintenance goes from “tedious YAML editing nobody does” to “trigger the skill and let Claude refresh the exposure from Metabase.” That’s a workflow people actually follow.
The Pipe & The Line is a reader-supported publication. To receive new posts and support my work, consider becoming a free or paid subscriber.
Exposures as a Lean Data Catalog ⚡
With enriched exposures, you get end-to-end lineage from dbt models to dashboard cards without needing a metadata platform.
dbt already gives you model-to-model lineage. The enriched exposure closes the last mile: model-to-dashboard, all the way down to which card uses which column. 
There’s no need for a catalog platform or complex ingestion pipelines to configure at an early stage. Just dbt, Metabase, and a well-structured YAML file that AI keeps current.
Impact Analysis Without a Metadata Platform
The agentic-data-modeling [ https://substack.com/redirect/25a98ef7-e8dc-446f-a09b-ac8889136f86?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] repo includes an impact-analysis skill that traces lineage through OpenMetadata. With enriched exposures, you can do the same thing.
Say you want to rename roas in campaign_performance. Claude reads _exposures.yml, finds that the ROAS scalar card directly references that column, and the dashboard drives daily budget allocation decisions. Then it verifies the live state via Metabase MCP.
## Impact Analysis: campaign_performance.roas

### Direct downstream
| Entity         | Type  | Column references          |
|----------------|-------|----------------------------|
| daily_summary  | model | overall_roas (1 ref)       |

### Dashboard impact
| Dashboard                    | Cards affected | Risk |
|------------------------------|----------------|------|
| Agentic Data Modeling Demo   | 1 of 6 cards   | HIGH |

### Risk: HIGH
- 1 downstream model + 1 dashboard card affected
- Dashboard drives daily budget allocation decisions
Enriched exposures give you the specific answer: which cards break, who relies on them, and how critical the dependency is.
Recommended:
End To End Agentic Data Modeling: Using AI and OpenMetadata MCP [ https://substack.com/redirect/c4c796fb-f061-4f34-b409-929a665d2f2e?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]
⚠️ The Challenges
Let’s not oversell this.
I discussed many of those points in Modern Data 101 The AI Data Modeling Tax: Working On Human Readiness Before AI Readiness [ https://substack.com/redirect/279c43a1-9732-4aa8-bb3b-e9f8188c9837?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] in case you want to take a look on the topic, but let’s briefly break the most important ones.
MCP can be really good or just “decent”. Depending on your BI tooling, the MCP can help you discover a lot for this skill to make sense, or just be enough to catch the surface but miss detail.
Enrichment drifts. Dashboards change, cards get added, columns get swapped. The enriched description is a snapshot. Re-run the skill periodically to keep it current or find a way creatine a workflow-routine to ensure consistency over time.
Know the business. Don’t try to get away with murder. AI will assume stuff out of a simple query and will confidently write wrong things if you don’t take the time to contradict it and supervise it properly. Understand stakeholder, business knowledge and use cases to run this process with high quality outputs.
Companion repo: agentic-data-modeling [ https://substack.com/redirect/25a98ef7-e8dc-446f-a09b-ac8889136f86?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]. PR #10 [ https://substack.com/redirect/711effa6-d0b7-45d8-95d6-7b274ed01e4c?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] includes the metadata-exposure-enrichment skill alongside the existing metadata-ai-readiness, metadata-glossary, and metadata-impact-analysis skills.
Going further: If you want to push enriched descriptions into a metadata catalog for column-level lineage across all systems, the same repo adds OpenMetadata MCP on top of this same dbt foundation.
If you enjoyed the content, hit the like ❤️ button, share, comment, repost, and all those nice things people do when like stuff these days. Glad to know you made it to this part!
Hi, I am Alejandro Aboy. I am currently working as a Data Engineer. I started in digital marketing at 19. I gained experience in website tracking, advertising, and analytics. I also founded my agency. In 2021, I found my passion for data engineering. So, I shifted my career focus, despite lacking a CS degree. I’m now pursuing this path, leveraging my diverse experience and willingness to learn.

Unsubscribe https://substack.com/redirect/2/eyJlIjoiaHR0cHM6Ly90aGVwaXBlYW5kdGhlbGluZS5zdWJzdGFjay5jb20vYWN0aW9uL2Rpc2FibGVfZW1haWw_dG9rZW49ZXlKMWMyVnlYMmxrSWpveE1EY3pPREV4TENKd2IzTjBYMmxrSWpveE9UTTVPREV5TWpFc0ltbGhkQ0k2TVRjM09EYzROVFF6TXl3aVpYaHdJam94T0RFd016SXhORE16TENKcGMzTWlPaUp3ZFdJdE1URTVOakl5T1NJc0luTjFZaUk2SW1ScGMyRmliR1ZmWlcxaGFXd2lmUS5neDZYWVp1Y1A5ZGZWeXJneGtEcnoydElHU21OWGtjZW1wcm8xUVE1NDdNIiwicCI6MTkzOTgxMjIxLCJzIjoxMTk2MjI5LCJmIjp0cnVlLCJ1IjoxMDczODExLCJpYXQiOjE3Nzg3ODU0MzMsImV4cCI6MjA5NDM2MTQzMywiaXNzIjoicHViLTAiLCJzdWIiOiJsaW5rLXJlZGlyZWN0In0.VUOTFXn0IO-FYrwh39XCESfQV4FYctK2Bq-e3mmTwFA?
