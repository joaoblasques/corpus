---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2026-06-24-how-i-made-my-data-platform-s-failures-public-and-earned-my.md
    channel: email
    ingested_at: 2026-06-26
aliases:
  - data status page
  - data platform status page
  - data product status page
  - incident communication for data teams
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-26
updated: 2026-06-26
---

# Data Platform Status Page

**TL;DR.** A **status page for your data platform** — the same operational artifact every SaaS product (Stripe, GitHub) maintains — applied to data. When a pipeline breaks, stakeholders go to one page that shows which **data products and reports** are affected, the current status, and a timeline of updates, instead of flooding Slack with "is *my* dashboard affected?" questions [^src1]. The author reports **zero questions per incident** since launching it [^src1]. The deeper claim: data teams talk endlessly about "data as a product" but don't give their products the basic operational practice — public incident communication — that software product teams figured out long ago [^src1].

## The problem it solves

Every incident announcement in Slack triggers the same panicked, repetitive questions from different people about different downstream assets [^src1]:

> *"Is the Bookings dashboard affected? What about the ML report? Are the product usage numbers going to be wrong?"* [^src1]

Two root issues [^src1]:
1. An announcement can say *what* broke but **can't enumerate everything that's still fine**, so stakeholders ask.
2. A failure at the ingestion layer doesn't obviously map to a broken dashboard — **the lineage from broken pipeline to broken report isn't visible** without the right tooling.

## What you need to build it

If you run a modern data stack you likely already have the pieces [^src1]:

- An **ELT** process landing raw data in the warehouse (works with ETL too, slightly easier with ELT).
- A **data observability / catalog tool with column-level lineage** — the author uses SYNQ; **Elementary** (open-source) or **OpenLineage** (build-from-scratch) work too. *"Without column-level lineage, the question 'what downstream assets does this failure affect?' has no reliable answer."* [^src1] See [[data-engineering/data-observability|Data Observability]].
- A **BI tool that exposes an API** (the author uses Omni; the specific tool matters less than API access).

## The mapping problem (the part AI solved)

Lineage tools know a column flows from `accounts.plan_id` through a `bookings` model — but **not which dashboard tile queries that model** [^src1]. Without that last hop, the status page can only say "a dbt model failed," not "your report is affected." The bridge is a script that [^src1]:

1. pulls a selected set of official dashboards from the BI tool's API,
2. extracts every **tile** in those dashboards,
3. retrieves the **query each tile executes**.

That yields a map between BI tiles and underlying dbt models. Combined with the lineage graph, a failure at ingestion can be traced **all the way to the specific reports affected** — closing the same "last mile" of lineage that dbt [[data-engineering/dbt|exposures]] target.

## How an incident flows

When a test fails or a pipeline breaks, the team triages: real incident affecting stakeholders, or a transient failure resolved silently? If real, they **declare an incident** in the observability tool [^src1]:

- The declaration triggers a Slack notification **with a link to the status page**.
- Updates are added as comments in the observability tool; each comment triggers another Slack notification — stakeholders get a running update **without anyone writing a separate message or copying info across threads**.
- The page has **no database** — it makes API calls to the observability tool at request time and renders current state. Less infrastructure, nothing to keep in sync [^src1].

## What the page shows

Structured around **data products, not incidents** — because that's how stakeholders think (they have no idea about tables or pipelines) [^src1]:

- Selected **data products** (groups of dashboards).
- **Reports** per product.
- **Current status**, pulled in real time.
- **Status history** — the track record over time.
- Individual incident detail pages with affected reports and a full update timeline.

Scoping the page to the products stakeholders care about is what makes it useful — *"everything else would be noise."* [^src1]

## Why transparency builds more trust than hiding failures

The instinct is to fix quietly and say as little as possible, because every incident announcement feels like an admission [^src1]. That instinct is backwards [^src1]:

- Stakeholders lose trust when a team **goes quiet during an incident**. A team that declares incidents publicly, posts running updates, keeps a visible history, and publishes **postmortems** earns a different reputation.
- With **twelve months of visible history**, a vague "the data is always broken" complaint becomes a documented conversation about incident count, average resolution time, and trend — *"the documented fact works in your favor."* [^src1]
- When stakeholders know they'll be **told** when something breaks, they stop checking — *"they stop asking 'is this dashboard up to date?' as a routine question."* That baseline confidence is worth more than any SLA document [^src1].

This connects directly to [[productivity/working-with-stakeholders|stakeholder trust]] and the postmortem/memory layer in [[data-engineering/data-engineering-team-os|Data Engineering Team OS]].

## The meta-lesson: the skill was identifying the gap

The author wrote none of the code: read the API docs for both tools, described what was needed, handed it to an AI coding tool, and had the status page + mapping script + integration done in days [^src1]. *"You don't need to be a strong engineer to build this. You need to recognize the problem, read some documentation, and spend a couple of days on it."* [^src1] The leverage came from noticing what software product teams do that data teams don't — an instance of [[data-engineering/data-engineer-role|business-impact-over-technical-execution]] thinking, and of [[data-engineering/claude-code-for-data-engineering|AI-assisted DE]] collapsing build time.

## Related

- [[data-engineering/data-observability|Data Observability]] — column-level lineage + incident detection this page surfaces; MTTD/MTTR are the metrics the status history exposes
- [[data-engineering/dbt|dbt]] — exposures close the model→dashboard lineage hop the mapping script reconstructs
- [[data-engineering/data-engineering-team-os|Data Engineering Team OS]] — postmortems and the memory layer
- [[productivity/working-with-stakeholders|Working with Stakeholders]] — the trust mechanism this operationalizes
- [[data-engineering/data-quality|Data Quality]] — the goal incidents are declared against
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [How I Made My Data Platform's Failures Public and Earned My Stakeholders' Trust (Yordan Ivanov, Data Gibberish)](../../raw/email/email-2026-06-24-how-i-made-my-data-platform-s-failures-public-and-earned-my.md)
