---
channel: email
source: gmail
gmail_message_id: 19e92bff69371a1c
from: "\"Ale from The Pipe & The Line\" <thepipeandtheline@substack.com>"
subject: "Claude Code For Data Engineers: Hands-On Projects For Your Daily Workflows"
date_received: 2026-06-04
pointer: false
collected_at: 2026-06-11
links:
  - {url: "https://substack.com/redirect/99af624a-9821-4aff-bf6d-71a837a10c40?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 8, file: raw/web/data-engineers-are-becoming-metadataops-engineers-and-you-do.md}
  - {url: "https://substack.com/redirect/7905aff1-42e4-4318-a90d-b6e57a5f9244?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 7, file: raw/web/end-to-end-agentic-data-modeling-using-ai-and-openmetadata-m.md}
corpus_ingested: true
corpus_ingested_at: 2026-06-12
corpus_pages:
  - corpus/data-engineering/claude-code-for-data-engineering.md
---

View this post on the web at https://thepipeandtheline.substack.com/p/claude-code-for-data-engineers-hands

Hi there! Alejandro here 😊
Subscribe if you like to read about technical data & AI learnings, deep dives!
Enjoy the reading and let me know in the comments what you think about it 👨🏻‍💻
📝 TL;DR
The foundation is three mechanisms: Skills encode best practices, MCPs connect to external tools, Hooks enforce quality gates and verything else builds on top.
Data modeling has the most mature ecosystem right now: from reading a business PRD in Miro to AI-ready dbt models with enriched metadata. Good thinking and context is still key.
Most of the complexity is in deciding what to automate, what to keep manual, and when the setup is working against you instead of for you.
Every section links to the hands-on work behind these ideas.
If you ask what my Claude Code setup actually looks like for day-to-day data engineering & AI work, the honest answer is: it depends on the week 😅
Six months ago I wasn’t using 10% of what I use now. Six weeks from now the current setup will feel outdated. Working at the edge means the line between production-ready and experiment shifts every few weeks.
What I can describe is the current snapshot: what I’ve built, what each part does, and where the rough edges still are. 
This article maps every piece of that work, with links to the hands-on articles behind each section.
The Foundation: Skills, MCPs & Hooks
Claude Code connects to the data stack through three mechanisms. They work independently, but the real value is chaining them.
MCPs connect Claude to external tools in real time: databases, orchestrators, metadata catalogs. 
All in place to avoid context switching with tool live during your session.
Skills encode best practices as instructions Claude follows automatically. dbt modeling patterns, testing conventions, documentation standards. 
You write them once and they run on every relevant task, not just when you remember to ask.
Hooks enforce quality gates before or after Claude acts. Run pytest before every commit, lint SQL on every write or tell Claude Code runs dbt test after every model change. 
The checks can’t be skipped because they’re not relying on Claude to remember them.
When I mapped all the data engineering integrations available right now — databases, orchestration, data quality, documentation, modeling — the picture was clearer than I expected. Some are production-ready. Others are early experiments. The article below has the full breakdown.
Recommended:
Thanks for reading The Pipe & The Line! This post is public so feel free to share it.
Data Modeling: From PRD to dbt 
The hardest part of data modeling has never been writing the SQL. 
The whole process end to end: translation from a business requirement in Miro to a grain definition in a schema YAML, from a sticky note about acquisition channels to a column in a mart model.
Normally translation is where context gets lost: Column names drift, grain shifts, and edge cases from Slack threads disappear entirely. 
That stakeholder talks about discrepancies in revenue and the models pre filter refunds. 
You end up in days or weeks endless debugging sessions because they keep insisting data is wrong, but most of the time that context is not properly captured and aligned, so all modeling efforts never get properly documented and enriched. 
The workflow I built chains four tools to automate that translation:
Miro MCP reads the business PRD from the board. Have meetings to only gather information and put together what you need. 
MCP Data Toolbox connects to the database and samples what’s actually there. The schema YAMLs tell you the names and allows Claude Code to discover feasibility, which helps avoiding modelling the wrong thing. 
A custom prd-to-dbt Skill maps business concepts to source tables and generates an implementation plan before writing any SQL. This is an example, you can go fancy here and adapt it to your complexity. 
dbt Agent Skills generate staging, intermediate, and marts models (descriptions, grain docs, and tests included), following the existing project’s patterns.
There’s an approval step: Claude proposes the ERD back on Miro before writing SQL and YOU review it. You can spend as much as you want here, since this part of the process will cascade into higher quality. 
Recommended:
Making Existing Models AI-Ready
Building new models is the easy part with AI. The harder problem is the dbt project that already exists, with schema YAMLs full of column names and zero useful descriptions for AI Agents to make semantic driven decisions.
When the consumer of your data was a human analyst, vague metadata was annoying to documented. When the consumer is an LLM, vague metadata becomes input for confident hallucinations. Total revenue from conversions as a column description is not enough anymore. An AI agent will invent edge cases it doesn’t know about. We discussed this heavily on Data Engineers Are Becoming MetadataOps Engineers [ https://substack.com/redirect/99af624a-9821-4aff-bf6d-71a837a10c40?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]
The metadata-ai-readiness skill of this project automates the enrichment loop: 
Audit what’s missing against dbt Skills documentation standards
Profile the actual data via Postgres MCP to find edge cases the YAMLs don’t mention
Write enriched descriptions back, and flag what it can’t fix automatically. 
That three-step loop (discover gaps, load relevant data, fix) is progressive disclosure applied to metadata.
What it surfaces in the repo is a key finding: 2 models with  opposite null-handling touching the same data points.
That’s the kind of thing that wastes precious time of debugging for anyone who doesn’t already know it. The enriched description captures it once, permanently.
Recommended:
Also take a look at our collab with the legend Erfan Hesami  on End To End Agentic Data Modeling [ https://substack.com/redirect/7905aff1-42e4-4318-a90d-b6e57a5f9244?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] → pushing enriched metadata into a catalog for lineage, impact analysis, and governance.
What’s Running Now, What’s Next
Settling to define something as definitive these days is missing the long run. 
These systems work amazingly when you give the harness ways of discovering data, making decisions based on solid patterns and foundations to rely on and working towards repeatble workflows that are as deterministic as possible, even for AI. 
The 3-layer debugging pattern applied to Airflow, and why the same principle governs how MCPs and semantic layers should load in any agent session.
The setup doesn’t stop and this is just a snapshot. Whenever I write about it in a few months, it would be different for sure!
If you want the full picture of the AI-native transition beyond the tooling: 
If you’re building a Claude Code setup for data engineering work and running into the same problems — or different ones — I’d like to hear where you are.
Hi, I am Alejandro Aboy. I am currently working as a Data Engineer. I started in digital marketing at 19. I gained experience in website tracking, advertising, and analytics. I also founded my agency. In 2021, I found my passion for data engineering. So, I shifted my career focus, despite lacking a CS degree. I’m now pursuing this path, leveraging my diverse experience and willingness to learn.

Unsubscribe https://substack.com/redirect/2/eyJlIjoiaHR0cHM6Ly90aGVwaXBlYW5kdGhlbGluZS5zdWJzdGFjay5jb20vYWN0aW9uL2Rpc2FibGVfZW1haWw_dG9rZW49ZXlKMWMyVnlYMmxrSWpveE1EY3pPREV4TENKd2IzTjBYMmxrSWpveU1EQTBPVGt5TkRRc0ltbGhkQ0k2TVRjNE1EVTNPRFV3T1N3aVpYaHdJam94T0RFeU1URTBOVEE1TENKcGMzTWlPaUp3ZFdJdE1URTVOakl5T1NJc0luTjFZaUk2SW1ScGMyRmliR1ZmWlcxaGFXd2lmUS5WR2NrNUpIbHdpWG5HX2VCaXZjNTJyNkJnNi03Qm1CcFY4SGNYejI5VzdRIiwicCI6MjAwNDk5MjQ0LCJzIjoxMTk2MjI5LCJmIjp0cnVlLCJ1IjoxMDczODExLCJpYXQiOjE3ODA1Nzg1MDksImV4cCI6MjA5NjE1NDUwOSwiaXNzIjoicHViLTAiLCJzdWIiOiJsaW5rLXJlZGlyZWN0In0.Zjtfh-lTbr8a-ELYi4fg_juck7q5tfLlI2eKfpcJthg?
