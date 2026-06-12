---
channel: email
source: gmail
gmail_message_id: 19e5edc62f8b85ee
from: Pipeline to Insights <pipeline2insights@substack.com>
subject: When (and when not) to use Databricks
date_received: 2026-05-25
pointer: false
collected_at: 2026-06-11
links:
  - {url: "https://substack.com/redirect/ebe23f5b-9121-4a14-825b-13ff13b6479b?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 8, file: raw/web/databricks-pricing-flexible-plans-for-data-and-ai-solutions.md}
  - {url: "https://substack.com/redirect/415e2669-bd20-49e4-a425-e835ff2b8995?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 8, file: raw/web/unity-catalog.md}
  - {url: "https://substack.com/redirect/85a0aa5e-5b66-4c13-bcb8-65052c58435b?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 8, file: raw/web/lakeflow-spark-declarative-pipelines-databricks-on-aws.md}
  - {url: "https://substack.com/redirect/501cc3b5-7f6d-41ad-963a-09c21577d3b1?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 7, file: raw/web/amazon-s3-cloud-object-storage-aws.md}
  - {url: "https://substack.com/redirect/e977b834-d351-4598-8385-4302bce29292?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 7, file: raw/web/azure-data-lake-storage-introduction-azure-storage.md}
  - {url: "https://substack.com/redirect/e9173339-e305-4325-bc52-a781223f0c02?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 7, file: raw/web/cloud-storage.md}
  - {url: "https://substack.com/redirect/ac2b2e19-2dda-40fa-8670-b091366aab32?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: false, score: 2, reason: low-utility}
  - {url: "https://substack.com/redirect/e6f59acf-1645-40d7-87a8-5bcbbea1fce6?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: false, score: 2, reason: low-utility}
  - {url: "https://substack.com/redirect/aa5fa32f-464c-467c-aaac-0ba79a377b31?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: false, score: 1, reason: low-utility}
corpus_ingested: true
corpus_ingested_at: 2026-06-11
corpus_pages:
  - corpus/data-engineering/databricks.md
---

View this post on the web at https://pipeline2insights.substack.com/p/when-and-when-not-to-use-databricks

Every data engineer eventually gets asked the same question: “Should we use Databricks?” It comes up when a team is building a platform from scratch, replacing Hadoop, or quietly outgrowing a single warehouse.
The honest answer is: sometimes yes, sometimes no. And the framework for deciding rarely makes it into the room.
This post is the framework I wish more teams would run through before signing the contract.
In this post, I will cover:
When Databricks makes sense (use cases, team size, data scale).
When Databricks is overkill (simpler stack alternatives)
Common adoption mistakes engineers make
How to think about cost realistically (without specific DBU [ https://substack.com/redirect/ebe23f5b-9121-4a14-825b-13ff13b6479b?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] prices)
I’m Jakub Lasak, a Databricks Data Engineer working on production pipelines daily. Outside of work, I publish on dataengineer.wiki [ https://substack.com/redirect/ac2b2e19-2dda-40fa-8670-b091366aab32?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ], helping Databricks Data Engineers reach the next level through frameworks and cheat sheets grounded in real-world experience.
This topic is important to me because I see teams over-adopt and under-adopt Databricks every quarter. The decision rarely gets made honestly. It usually gets made on vibes: a conference talk, a vendor demo, an executive who read a Gartner report on a flight.
You can follow more of my work on LinkedIn [ https://substack.com/redirect/aa5fa32f-464c-467c-aaac-0ba79a377b31?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ], at dataengineer.wiki [ https://substack.com/redirect/ac2b2e19-2dda-40fa-8670-b091366aab32?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ], or on my Substack.
Pipeline To Insights is a reader-supported publication. To receive new posts and support my work, consider becoming a free or paid subscriber🙏💐.
When Databricks makes sense
Databricks is a lakehouse platform: a system that puts warehouse-style SQL, BI, ML, and streaming on top of low-cost object storage (S3 [ https://substack.com/redirect/501cc3b5-7f6d-41ad-963a-09c21577d3b1?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ], ADLS [ https://substack.com/redirect/e977b834-d351-4598-8385-4302bce29292?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ], GCS [ https://substack.com/redirect/e9173339-e305-4325-bc52-a781223f0c02?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]) using open table formats such as Delta or Iceberg.
It earns its keep when the alternative is stitching together a warehouse, a Spark cluster, a streaming engine, a notebook environment, a feature store, a governance layer, and a permissions model from three different vendors. If your platform has reached that level of complexity, Databricks usually wins.
Five situations where Databricks is a strong fit:
1. Multi-TB data with mixed workloads. 
BI dashboards, ad-hoc SQL, scheduled batch, streaming, and at least one ML use case all on the same data. Running them on one platform with one permission story is a leverage. Running them across five tools is an integration tax.
2. Ten or more engineers across disciplines. 
Data engineers, analytics engineers, ML engineers, and BI analysts in the same org. A shared platform with a shared catalogue stops being a luxury and starts paying back. Conventions, lineage, and governance become reusable across teams rather than being reinvented for each tool.
3. Multi-source ingestion with governance requirements. 
A dozen source systems plus a real legal obligation (financial services, healthcare, regulated public sector). Unity Catalogue [ https://substack.com/redirect/415e2669-bd20-49e4-a425-e835ff2b8995?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]  [ https://substack.com/redirect/415e2669-bd20-49e4-a425-e835ff2b8995?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ](Databricks’ governance layer for tables, files, models, and access policies), row- and column-level security, and unified audit logs make for a compelling value proposition. The alternative is reinventing controls in every tool.
4. Replatforming off Hadoop or legacy Spark. 
Teams already on Spark get the biggest immediate win: cluster management, governance, optimised storage, and serverless SQL out of the box, without having to rebuild pipelines. The learning curve is short because Spark knowledge transfers easily.
5. Streaming, ML, and BI on the same data. 
If your business genuinely needs near-real-time ingestion, model serving, and analytics in a single platform, the lakehouse is the path of least resistance.
Keep these scenarios in mind. I’ll compare where Databricks fits well versus where it becomes overkill in the matrix below.
When Databricks is overkill
This is the section that does not get written often enough. There are real, common situations where a lakehouse is the wrong tool.
Sub-500GB BI-only workloads. 
If the whole dataset fits on a single Postgres instance, BI is your only consumer, and growth is linear, then Postgres plus dbt plus a managed BI tool will quietly out-deliver a lakehouse on every dimension that matters. Cost, simplicity, hiring, and time to first dashboard. A junior analytics engineer can run that stack for years.
Small teams (1-3 engineers) who have never run Spark. 
They will spend six months fighting cluster configs, shuffle partitions, and broadcast joins before shipping anything that justifies the platform. The same team would be productive in week two on Postgres or BigQuery.
Single-cloud, single-source SQL workloads. 
If everything is “load data, transform with SQL, query with SQL”, a single cloud warehouse (BigQuery, Snowflake, Redshift, Synapse) is enough. You skip the cluster-management layer entirely.
Pure batch, daily refresh. 
Managed Airflow, plus a warehouse, plus dbt, is well understood, well-staffed, and boring. Boring is good. Boring is hireable.
Early-stage startups are still figuring out the data layer. 
A lakehouse is a premature commitment to heavy architecture. Start simple, prove the use cases, then move up.
If most of your situation lives on the right side of the matrix below, you do not have a Databricks problem. You have a “Databricks is the wrong tool” problem, which is much cheaper to fix early.
Common adoption mistakes engineers make
Most failed Databricks adoptions are not platform failures. They are failures of fit, configuration, or process. 
Seven patterns repeat often enough to name.
1. Picking Databricks for the logo. 
“Everyone uses it” and “it’ll look good on the team’s CV” are not criteria for evaluating a platform. They are cultural pressure dressed up as a decision. Write down the use cases, data scale, and team mix before you talk to a vendor.
2. Running all-purpose clusters 24/7.
All-purpose clusters are interactive clusters meant for notebooks. They are expensive, and they bill for idle time. Move scheduled jobs to job clusters or serverless. Auto-terminate aggressively on anything interactive.
3. Rolling out the Unity Catalogue before you have anything to govern. 
UC is genuine work to set up: Metastore, catalogues, external locations, storage credentials, and permissions inheritance. Teams with five tables and three users sometimes spend a quarter rolling it out and get zero value. Roll out UC when the governance pain is real, not before you need it.
4. Treating Databricks as “just managed Spark”. 
A team migrates Hadoop Spark workloads over, runs them on all-purpose clusters, and stops there. They never adopt  [ https://substack.com/redirect/85a0aa5e-5b66-4c13-bcb8-65052c58435b?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]Lakeflow Spark Declarative Pipelines [ https://substack.com/redirect/85a0aa5e-5b66-4c13-bcb8-65052c58435b?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] (the framework formerly known as DLT, where you describe tables and the platform handles orchestration and incremental processing), never use serverless SQL, never turn on Photon (Databricks’ vectorised query engine). The platform is doing one thing instead of five. Ask, on a workload-by-workload basis, which Databricks primitive is the best fit.
5. No cost guardrails on day one. Databricks bills are famously easy to lose control of. Without budgets, alerts, cluster policies, and tags, costs accumulate quietly across teams. Budgets and alerts in week one. Cluster policies that block the worst misconfigurations. Tags on every cluster.
6. Underestimating egress and storage. The DBU bill (Databricks Unit, a normalised measure of processing capacity) gets attention because it appears on the Databricks invoice. Cloud egress, ADLS or S3 storage, snapshot retention, and Unity Catalogue metadata storage live on the cloud provider’s invoice. At scale, the cloud bill can be a large share of the all-in cost. Monitor both invoices.
7. Picking Databricks without picking who owns it. A platform is not free. It needs at least one engineer who treats it as their primary domain. Without a clear owner, the platform decays and the bill grows. Name the owner before adoption, not after.
None of these is a platform fault. They are the predictable shape of adopting any heavy platform without enough thought about how you will run it.
How to think about cost realistically
Cost is the topic where this conversation usually goes wrong, in both directions. Pro-Databricks teams hand-wave it (”it pays for itself”). Anti-Databricks teams point at a DBU rate and stop thinking. Both are wrong.
DBU categories matter more than the DBU rate. Databricks does not have one price. It has several, by workload type:
All-purpose computing is the most expensive. Interactive, notebook-style work. Do not run scheduled jobs on it.
Jobs compute is cheaper than all-purpose for the same cluster spec. Scheduled work belongs here.
SQL warehouses (serverless and classic) are built for BI. Serverless is meaningfully cheaper for bursty workloads because it spins up and down quickly.
Declarative pipelines (Lakeflow) have their own SKU. The value is the orchestration, dependency management, and incremental processing logic that the platform handles for you.
Match the workload to the right SKU. A scheduled ELT job running on all-purpose compute is paying a premium for capabilities it does not use. Move it to jobs compute or declarative pipelines, and the bill drops without a code change.
Cluster lifecycle is where most of the waste lives. A few habits do disproportionate work:
Auto-terminate on every interactive cluster (defaults are too generous).
Spot instances for fault-tolerant workloads.
Right-sized drivers. A driver bigger than the workload needs is paying for idle RAM.
Cluster policies. Without them, somebody will eventually spin up a 64-node memory-optimised cluster for a one-off query.
A simple way to think about where the money goes:
The headline DBU rate is one of the five places money moves. Reasoning about cost on that one line alone will mislead you, in either direction.
A useful exercise before adoption: build a rough total cost of ownership (TCO) model for both Databricks and the simpler stack you would otherwise use, including the engineering time to operate each. Run it for one year and three years. If Databricks still wins, fine. If it does not, you have saved yourself a multi-year migration.
Conclusion
The decision to adopt Databricks comes down to four questions:
What is the data scale and growth trajectory? Multi-TB and growing? Lakehouse territory. Sub-500GB and linear? Postgres plus dbt is quietly better.
How big is the team, and what is the skill mix? A small SQL-first team will spend months learning a platform they did not need. A larger mixed-discipline team gets compounding leverage from a shared platform.
What is the workload mix? BI, ML, and streaming on the same data is where the lakehouse earns its place. BI-only or batch-SQL-only is where a single warehouse wins.
What is the realistic total cost of ownership? Not the headline DBU rate. The all-in: compute, storage, egress, governance, and the engineers required to run it well, compared honestly against the alternative.
Run these four questions every time the adoption question comes up, and the decision stops being a vibes call.
Databricks is a powerful platform. It is also a heavy one. The question is not whether it is good. It is whether it fits.
Use the wrong tool, and you will spend six months proving you did not need it. Use the right tool, and you will quietly compound for years.
If you want to go deeper on the cost question or on rolling out Unity Catalogue without setting it on fire, I publish write-ups on both at dataengineer.wiki [ https://substack.com/redirect/ac2b2e19-2dda-40fa-8670-b091366aab32?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]. Two that pair naturally with this article:  [ https://substack.com/redirect/e6f59acf-1645-40d7-87a8-5bcbbea1fce6?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]
We value your feedback
If you have any feedback, suggestions, or additional topics you’d like us to cover, please share them with us. We’d love to hear from you!

Unsubscribe https://substack.com/redirect/2/eyJlIjoiaHR0cHM6Ly9waXBlbGluZTJpbnNpZ2h0cy5zdWJzdGFjay5jb20vYWN0aW9uL2Rpc2FibGVfZW1haWw_dG9rZW49ZXlKMWMyVnlYMmxrSWpveE1EY3pPREV4TENKd2IzTjBYMmxrSWpveE9UZzFORGN4T0RNc0ltbGhkQ0k2TVRjM09UY3dOemsxTml3aVpYaHdJam94T0RFeE1qUXpPVFUyTENKcGMzTWlPaUp3ZFdJdE16QTBORGsyTmlJc0luTjFZaUk2SW1ScGMyRmliR1ZmWlcxaGFXd2lmUS5KNUYxWFN6NFBxa1Z6bFRfSjg5aVZuVjlFVmRJUDlma2t1a0NxNE1oSnVZIiwicCI6MTk4NTQ3MTgzLCJzIjozMDQ0OTY2LCJmIjp0cnVlLCJ1IjoxMDczODExLCJpYXQiOjE3Nzk3MDc5NTYsImV4cCI6MjA5NTI4Mzk1NiwiaXNzIjoicHViLTAiLCJzdWIiOiJsaW5rLXJlZGlyZWN0In0.PtBVLpNBgg3TgqM5v0g36EtjA4k4r9jbWpuZ6spNh-I?
