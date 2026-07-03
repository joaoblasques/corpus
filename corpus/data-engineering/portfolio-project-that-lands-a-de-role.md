---
type: synthesis
domain: data-engineering
status: draft
sources:
  - path: raw/web/data-engineering-projects-start-data-engineering.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/web/data-engineering-best-practices-1-data-flow-code-start-data.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/web/how-to-become-a-valuable-data-engineer-start-data-engineerin.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/email/email-2026-05-25-when-and-when-not-to-use-databricks.md
    channel: email
    ingested_at: 2026-06-11
  - path: raw/email/email-2025-09-08-medallion-architecture-is-not-a-data-model.md
    channel: inbox
    ingested_at: 2026-06-11
  - path: raw/web/6-steps-to-avoid-messy-data-in-your-warehouse-start-data-eng.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/email/email-2025-11-04-scd-2-considered-harmful-part-2.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/how-to-set-up-ci-cd-for-data-infrastructure-start-data-engin.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/web/complete-end-to-end-build-of-etl-pipeline-in-aws.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/how-ruthless-prioritization-got-me-a-40-raise-and-a-head-of.md
    channel: web
    ingested_at: 2026-06-12
aliases:
  - DE portfolio project
  - data engineering portfolio
  - portfolio project that lands a job
  - Databricks AWS portfolio project
  - end-to-end DE showcase
  - impressive data engineering project
  - self-taught data engineer project
  - what makes a DE project look senior
  - junior project mistakes
tags:
  - corpus/data-engineering
  - synthesis
created: 2026-06-18
updated: 2026-06-18
provisional: false
---

# The Portfolio Project That Lands a DE Role

**TL;DR.** For a self-taught switcher targeting **data-engineering roles**, ONE end-to-end Databricks+AWS project beats a grab-bag — *if* it reads as a **solved business problem** wrapped in production rigor, not a tutorial re-skin. Hiring managers do not score the tool list; they score two things the corpus keeps returning to: **business impact** (you knew *what* and *why* to build) and **technical fundamentals** done correctly (medallion staging, data quality at ingestion, idempotent reruns, tests, metadata in version control, IaC, and cost awareness) [^role][^be]. The single highest-leverage move is **framing**: name a stakeholder, a metric, and a refresh cadence, and make the repo legible in seconds [^career][^role]. The single biggest junior tell is the inverse: a pretty notebook that ingests a CSV once, has no tests, no reruns, no cost story, and answers no one's question [^career][^be]. Honest caveat up front: the corpus's own Databricks decision framework says a solo, sub-500GB, BI-shaped project is *exactly* the "Databricks is overkill" case [^db] — so a Databricks+AWS choice must be defended as a **deliberate learning/signal decision**, paired with day-one cost guardrails, not pretended to be the cheapest right answer.

## 1. Start from the business problem, not the stack

The corpus is emphatic and consistent: a DE's value is **business impact first, fundamentals second — and a long tool list is neither** [^role]. Translate that into the project:

- **Pick a problem a real consumer would pay for.** Every data project should either *make/save money* or *save time* [^role]. A portfolio piece that "solved a real business problem" outranks "a side project nobody asked for" [^career]. Choose a domain with an obvious decision attached — e.g. *"daily marketing-spend-vs-revenue by channel so a growth lead can cut low-ROI campaigns,"* not *"I loaded the NYC taxi dataset."*
- **Work backward from the output.** List the output steps first, then derive the technology from the requirements — do **not** choose tools first [^role]. This is also what keeps you from bolting Databricks onto a problem that a warehouse + dbt would solve.
- **Frame it with STAR and a stakeholder triad.** Before building, state Situation/Task/Action/Result, and answer: *who asks this question, what do they do with the answer, how often is it needed* [^role]. Put that triad in the README's first paragraph.
- **Make the repo legible in seconds.** Recruiters skim for signal. Avoid the four portfolio failure modes: no wow factor, ambiguous names/descriptions, no role targeting, amateur presentation [^career]. "E-commerce sales dashboard for real-time order tracking" reads instantly; "Databricks project" does not [^career]. Scope to DE only — one focused, polished pipeline beats a versatility grab-bag [^career].

> The same instinct that gets a DE promoted is the one that makes a portfolio land: *"your proximity to the business is what makes you irreplaceable, not just your skill with SQL or Airflow"* [^career]. Demonstrate proximity, not just plumbing.

## 2. The rigor checklist — what makes it read as *senior*

The corpus's [six best practices](/data-engineering/data-engineering-best-practices.md) are the backbone of a credible project; map every one into the build and call it out in the README so a reviewer can find it [^be]. The meta-rule: **analyze requirements, fix high-priority gaps first — don't implement best practices for their own sake** [^be].

| # | Practice | What "senior" looks like in the project | Corpus anchor |
|---|---|---|---|
| 1 | **Layered / medallion staging** | Bronze (raw, append-only, schema drift tolerated) → Silver (deduped, typed, business keys resolved) → Gold (modeled for the consumer). A metric is defined in exactly one place. | [^be][^med] |
| 2 | **Data quality at ingestion** | Validate *before* downstream use; check **source and final consumption data** (skip intermediates); expectations as config, not buried in code. | [^be][^dq] |
| 3 | **Idempotency** | Reruns/backfills don't duplicate: fixed date windows (`BETWEEN`, not `> X`), run-id partition overwrites or natural-key merges, `depends_on_past` only where truly cumulative. | [^be][^idem] |
| 4 | **DRY + I/O separated from transformation** | Shared logic in one place; a `StandardETL`-style blueprint; pure transform functions you can unit-test without touching storage. | [^be] |
| 5 | **Metadata in version control** | Track per-run inputs/outputs/timings/retries; keep dataset metadata (keys, location, table format, partition/cluster keys, schema) in git. | [^be] |
| 6 | **Tests that check behavior** | Unit + integration (+ sparing e2e); share one Spark session via `conftest.py`; don't over-test (it slows velocity). | [^be] |

Two of these deserve emphasis because they are where juniors most visibly fall short:

**Medallion is a *lifecycle*, not a *data model*.** Bronze/silver/gold says nothing about grain, keys, or whether gold is a star schema [^med]. A senior project shows an explicit **data model** at gold (Kimball star with an [SCD2](/data-engineering/scd2.md) dimension, or a documented OBT) and can say *why* — *"Medallion owns the pipeline; modeling owns the entities, grain, and keys"* [^med]. Debating layer colors while ignoring grain is the tell of *"a genuine gap in data-modeling knowledge among data engineers who over-focus on pipelines"* [^med].

**Idempotency is the real test of pipeline maturity.** Non-idempotent pipelines create *"tests that pass but prod fails"* bugs that surface on backfill [^idem]. The clearest proof you can put in a README: a backfill that reruns a date range and produces consistent output, ideally **parallelized** because each partition reads/writes only its own `ds` [^idem]. That single demonstration signals functional-data-engineering literacy more than any tool badge.

Beyond the six, two more belong on a 2026 checklist:

- **IaC + CI/CD.** Provision with [Terraform](/mlops/terraform.md); wire the standard skeleton — **CI runs fmt/validate/plan and posts the plan to the PR; CD applies to dev on merge, then a human-gated apply to prod** [^cicd]. Even a solo project benefits: it proves you understand *"deploying infra changes as easily as a code change"* and the dev→gate→prod flow employers actually run [^cicd].
- **Cost awareness as a first-class artifact.** See §5; this is the dimension juniors omit entirely.

## 3. Realism and ops — the difference between a demo and a system

A demo runs once on your laptop; a system runs on a schedule, fails loudly, and can be debugged by someone else. Bake in the operational layer the corpus repeatedly flags as the one teams neglect *"until they get yelled at by the business"* [^aws]:

- **Scheduling + orchestration**, not a manual run. Show the trigger (EventBridge, a Databricks Job, or Airflow) and idempotent reruns [^aws][^idem].
- **Observability**: structured logs (CloudWatch), run metadata, and an alert path. The reference AWS build posts green/red/blue **Slack notifications** with the webhook secured in Secrets Manager and pulled at runtime — a small touch that reads as production-minded [^aws]. Instrument the three high-value early signals: **data freshness, volume checks, schema validation** [^dq].
- **Failure handling**: a QA step that *errors and alerts* on bad data rather than silently writing it — the AWS reference runs row-count, null, and business-rule checks and refuses to publish on failure [^aws].
- **Serving design that fits the consumer.** Don't build one pre-joined wide table for everyone — *"you will never have a single-serving approach that satisfies every use case"* [^be]. Show you matched the gold layout (pre-aggregated for a dashboard vs. lower grain for analysis) to the stated stakeholder [^be].
- **Secrets, IAM, least privilege.** Real roles and a secrets manager, not credentials in code [^aws].

## 4. Defensible Databricks + AWS stack choices

Scope: DE roles, one showcase. The stack must be **defensible**, which means you can articulate the tradeoff — exactly the "taste" signal employers probe [^career].

**Be honest about the headline tension.** The corpus's Databricks decision framework says the platform is *overkill* for **sub-500GB, BI-only, 1–3-engineer, single-source** workloads, where *"Postgres + dbt + a managed BI tool quietly out-delivers on cost, simplicity, hiring, time-to-dashboard"* and *"boring is hireable"* [^db]. A solo portfolio project is, on paper, that case. So the defense is explicit: **you are choosing Databricks+AWS as a learning and market-signal decision** — many target JDs list it, and demonstrating Unity Catalog governance, a Lakeflow declarative pipeline, and Spark literacy is itself the portfolio payload — *while acknowledging* you'd reach for the simpler stack if the only goal were shipping this one dashboard cheaply [^db]. Naming that tradeoff out loud is the senior move; pretending Databricks is automatically "the professional choice" is the junior one [^db].

**A defensible Databricks-on-AWS shape:**

- **Storage:** raw data in **S3**; tables as **Delta** (or Iceberg) under an open table format so the lake isn't vendor-trapped [^db].
- **Governance:** **Unity Catalog** for catalogs/schemas, lineage, and row/column-level security — but deploy it because you're *demonstrating* governance, and keep the setup proportionate (UC is real setup work; rolling it out "before there is anything to govern" is a listed adoption mistake) [^db].
- **Pipelines:** **Lakeflow (Spark Declarative Pipelines)** for ingestion + incremental transforms — you describe tables, the platform handles orchestration/incremental processing [^db]. This shows the native, current-era Databricks pattern.
- **Layout:** **Liquid Clustering** over Hive-style partitioning — and be able to explain *why* (cardinality isn't a constraint, keys can change, avoids the small-file/over-partitioning trap Databricks reports in >75% of cases) [^db].
- **Compute discipline:** scheduled work on **jobs/serverless compute**, never interactive all-purpose clusters; auto-terminate; spot for fault-tolerant work [^db].
- **dbt vs. native:** a legitimately defensible fork. **Native Lakeflow SDP** keeps lineage inside Unity Catalog and avoids the DAB "complexity tax"; **dbt** buys platform-agnostic portability and a richer transformation ecosystem [^db]. Pick one and state the reason — the *reasoning* is the signal.

**A cheaper, equally defensible AWS-native counterpoint** (worth knowing, and worth a sentence in the README to show you considered it): single-node **DuckDB on ECS Fargate**, Terraform-provisioned, EventBridge-scheduled, Slack-monitored — the full demo cost *under 50 cents* and Fargate avoids Glue's Spark-cluster overhead for single-node work [^aws]. Mentioning this proves you didn't reach for Spark reflexively.

## 5. The cost story juniors skip

Cost is the dimension that most cleanly separates a learner who has *operated* a platform from one who has only followed a tutorial. Put a short **cost section** in the README:

- **Right-size by SKU.** Databricks has *several* prices by workload — all-purpose (most expensive) vs. jobs vs. serverless SQL vs. Lakeflow — and *"matching the workload to the right SKU drops the bill with no code change"* [^db]. The **DBU** is the normalized unit of processing capacity [^db].
- **Most waste is cluster lifecycle.** Auto-terminate interactive clusters, use spot instances, right-size drivers, enforce cluster policies [^db].
- **Watch both invoices.** DBUs are on the Databricks bill; **egress, S3 storage, snapshot retention, and UC metadata are on the AWS bill** — monitor both [^db].
- **Set guardrails on day one.** Budgets, alerts, cluster policies, and tags in week one is a listed best practice; *"no cost guardrails on day one"* is a listed mistake [^db].
- **Quantify your demo run.** A concrete number (the Fargate reference: ~$0.50 for the run, <$0.10/month ECR storage, assets destroyed afterward) reads as cost-conscious and reproducible [^aws].

## 6. The mistakes that make a project look junior

A consolidated checklist of anti-signals, each traceable to a corpus claim:

1. **No business framing.** No stakeholder, no metric, no "why" — just data moving A→B [^role][^career]. The corpus calls over-focus on moving data *the* gap [^med].
2. **Tool-first, not problem-first.** Choosing the stack before the requirements; reaching for Spark/Databricks reflexively when a warehouse fits [^role][^db].
3. **Treating medallion as a data model.** Bronze/silver/gold with no explicit grain, keys, or modeling decision at gold [^med].
4. **Runs once, can't rerun.** `INSERT INTO` without truncate, open-ended date filters, reliance on `_LATEST_` — duplicates on backfill; *"tests that pass but prod fails"* [^idem].
5. **No data quality at ingestion.** Trusting input; a null in a key silently breaking half the joins downstream [^dq]. (Opposite failure: over-testing every intermediate, tanking run time and cost [^be].)
6. **No tests / no version control / no metadata.** No unit or integration tests; dataset metadata not in git [^be].
7. **Click-ops, no IaC/CI/CD.** Console-provisioned infra, manual deploys, no plan→gate→apply flow [^cicd].
8. **No ops layer.** No scheduling, no monitoring/alerting, silent failures — the layer teams ignore "until the business yells" [^aws].
9. **No cost awareness.** 24/7 all-purpose clusters, no guardrails, no idea what a run costs [^db].
10. **One wide table for everyone.** A single pre-joined serving table assumed to satisfy every consumer [^be].
11. **Grab-bag / poor presentation.** Unfocused project mix, vague names, amateur README — *"with AI design help there is no real excuse for a poor-looking portfolio"* [^career].
12. **AI-slop without judgment.** Generated code/docs nobody understands; the corpus warns amplified bad judgment *"gets made faster, but looks more polished"* [^career]. Think first, then let AI assist the prose and the for-loops.

## Bottom line

Build **one** project that a hiring manager can describe in a sentence — *a real consumer's decision, served on a schedule, with trustworthy data*. Wrap it in the rigor checklist (section 2), run it like a system (section 3), choose Databricks+AWS *deliberately and defend the choice* (section 4), and put a cost story in the README (section 5). Avoid the twelve anti-signals (section 6). The corpus's throughline: **fundamentals + business proximity beat tool count** — the project is just the most legible proof you have both [^role][^career][^be].

## See also

- [DE Portfolio Projects](/data-engineering/de-portfolio-projects.md) — runnable batch/stream/event-driven templates and a stack-comparison matrix
- [Data Engineering Best Practices](/data-engineering/data-engineering-best-practices.md) — the six-practice backbone (3-hop, DQ, idempotency, DRY, metadata, tests)
- [The Data Engineer Role](/data-engineering/data-engineer-role.md) — business impact + fundamentals; the DA→DE transition playbook
- [Medallion Architecture](/data-engineering/medallion-architecture.md) — lifecycle vs. data model; where modeling actually lives
- [Idempotent Pipelines](/data-engineering/idempotent-pipelines.md) — backfill as the real maturity test
- [Data Quality](/data-engineering/data-quality.md) — validate at ingestion; contracts and schema-aware checks
- [CI/CD for Data Infrastructure](/data-engineering/cicd-for-data-infrastructure.md) — plan→gate→apply with Terraform + GitHub Actions
- [Databricks](/data-engineering/databricks.md) — when (and when not) to use it; Unity Catalog, Lakeflow, Liquid Clustering, cost model
- [DuckDB ETL on ECS Fargate](/data-engineering/sources/aws-duckdb-etl-fargate.md) — a sub-$1 end-to-end AWS reference build (Terraform/EventBridge/Slack)
- [Navigating a Technical Career](/ai-business/technical-career.md) — portfolio signal, role targeting, taste vs. AI-slop
- [Dimensional Modeling](/data-engineering/dimensional-modeling.md) / [SCD2](/data-engineering/scd2.md) — the gold-layer modeling fundamentals
- [Terraform](/mlops/terraform.md) / [AWS](/mlops/aws.md) — the IaC and cloud substrate
- [Data Engineering hub](/data-engineering/README.md)

---

[^role]: [The Data Engineer Role](/data-engineering/data-engineer-role.md) (corpus) — business impact + fundamentals over tool lists; work-backward-from-output; STAR + stakeholder triad
[^be]: [Data Engineering Best Practices](/data-engineering/data-engineering-best-practices.md) (corpus) — the six practices; one-wide-table anti-pattern; don't-over-test
[^career]: [Navigating a Technical Career](/ai-business/technical-career.md) (corpus) — portfolio signal, role targeting, solved-business-problem, taste vs. AI-slop, business proximity
[^med]: [Medallion Architecture](/data-engineering/medallion-architecture.md) (corpus) — lifecycle stages not a data model; grain/keys live in modeling
[^dq]: [Data Quality](/data-engineering/data-quality.md) (corpus) — validate at ingestion; contracts; freshness/volume/schema signals; silent-null join failure
[^idem]: [Idempotent Pipelines](/data-engineering/idempotent-pipelines.md) (corpus) — fixed windows, run-id/merge, parallel backfill as the proof
[^cicd]: [CI/CD for Data Infrastructure](/data-engineering/cicd-for-data-infrastructure.md) (corpus) — CI plan-to-PR, CD apply-dev→human-gate→prod with Terraform
[^db]: [Databricks](/data-engineering/databricks.md) (corpus) — when/when-not, "boring is hireable," Unity Catalog, Lakeflow, Liquid Clustering, DBU cost model, adoption mistakes
[^aws]: [DuckDB ETL on ECS Fargate](/data-engineering/sources/aws-duckdb-etl-fargate.md) (corpus) — end-to-end AWS build; EventBridge/Slack/Secrets Manager ops; sub-$1 cost realism
