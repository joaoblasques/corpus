---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/web/how-to-gather-requirements-for-your-data-project-start-data.md
    channel: web
    ingested_at: 2026-06-19
  - path: raw/email/email-2025-07-30-requirements-gathering-doesn-t-have-to-be-terrible.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/email/email-2025-07-24-how-to-build-data-architectures-faster.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - requirements gathering
  - data pipeline requirements
  - gathering requirements
  - scope creep
  - output led engineering
  - output-led engineering
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-19
updated: 2026-06-23
---

# Requirements Gathering for Data Projects

**TL;DR.** Data engineers are routinely caught off guard by undefined end-user assumptions: scope creep kills on-time delivery, end-users rarely specify exactly what they want, and ad-hoc change requests throw off timelines [^src1]. The fix is a repeatable five-step process — **identify the end-users, help them define the requirements (with a fixed question set), validate with sample data, deliver iteratively, and gate changes behind a process** — plus a posture of working *backward from the business output* rather than forward from the data [^src1][^src2]. A useful distinction: **end-users** are the people who consume the output; **stakeholders** are the PMs/BAs/managers who sign off [^src1].

## Why it's hard

The recurring frustrations: requirements gathering feels terrible, scope creep prevents on-time delivery, you're disappointed not to get specific requirements, end-users don't understand pipeline complexity, and changing requirements interrupt you constantly [^src1]. The premise of the process is that **you can't get 100% of the requirements right the first time** — assume end-users don't fully know (or won't clearly articulate) what they want [^src1].

## The five steps

### 1. Identify the end-users
The request usually surfaces in a meeting; identify who will actually use the output, because their capabilities and preferences shape the solution. Typical end-users and their preferred access [^src1]:

| End-user | Preferred output |
|---|---|
| Data analysts / scientists | SQL, files |
| Business users | Dashboard, report, Excel |
| Software engineers | SQL, APIs |
| External clients | Cloud storage, SFTP/FTP, APIs |

### 2. Help end-users define the requirements
When the end-user says *"we want X data,"* drive out the real requirements with a fixed question set [^src1]:

- **Business impact** — how does this data move the bottom line / an OKR? (Decides whether the project is worth doing.)
- **Semantic understanding** — what does the data represent, and which business process generates it? (Informs modeling — see [[data-engineering/data-modeling-meaning|Meaning in Data Modeling]].)
- **Data source** — where does it originate (app DB, vendor SFTP/cloud dump, API, manual upload)?
- **Frequency** — how fresh must it be (minutes/hourly/daily/weekly)? What is the highest acceptable load frequency?
- **Historical data** — must history be stored? (For a warehouse, usually yes.)
- **Data caveats** — seasonality, skew, late-arriving or missing upstream data, inability to join?
- **Access pattern** — SQL / dashboard / API / cloud storage? Common filter columns? Expected latency?
- **Business-rule checks (QA)** — which DQ metrics matter; which numeric fields can't diverge by more than *x%* across loads? (Feeds [[data-engineering/data-quality|data contracts]].)
- **Data output requirements** — the exact output schema (column/API field names, file names/sizes).

Then make end-users feel **invested** — thank them, update them on progress, incorporate feedback, recommend solutions to their pain, and credit them publicly — so they evangelize the project and help with resource allocation [^src1]. Record the requirements (e.g. JIRA) and get **stakeholder sign-off** [^src1].

### 3. End-user validation
Give end-users **sample data** (ideally in the expected output format) and a timeline to validate it — they know the data distribution and business rules. Validation often surfaces new requirements and business-rule checks. **Do not start transformation logic until stakeholders sign off** [^src1].

### 4. Deliver iteratively
Break a large project into small parts with their own acceptance criteria (e.g. an API→dashboard ELT splits into model the data, pull from the API, load to raw, build the dashboard). Small chunks create a short feedback cycle that makes changing requirements easy to absorb [^src1].

### 5. Handle changing requirements with a process
**Do not accept ad-hoc change/feature requests** (barring emergencies). Instead create a process to (a) let end-users request changes, (b) prioritize with stakeholders, and (c) communicate delivery timelines. Educating end-users on the process is what prevents scope creep and protects on-time delivery [^src1].

## Output-led engineering: design backward from the business

A complementary framing for *greenfield or upgrade* architecture work: start from the **outputs the business needs and work backward**, rather than forward from all the available data sources [^src2]. The pitch is that "Output Led Engineering" both sets sound foundations from the start *and* **narrows scope** so the project doesn't become overwhelming — while still delivering results to the business fast [^src2]. This is the same instinct as step 2's *business-impact* question and the [[data-engineering/data-engineer-role|data-engineer value]] pillar of "know how the company makes money" — requirements are derived from the desired output, not the other way around.

## Related

- [[data-engineering/data-engineer-role|The Data Engineer Role]] — business impact as the first pillar of DE value; prioritization-as-leverage
- [[data-engineering/data-quality|Data Quality]] — the business-rule (QA) questions become data contracts validated before use
- [[data-engineering/data-modeling-meaning|Meaning in Data Modeling]] — the semantic-understanding question feeds modeling
- [[data-engineering/de-portfolio-projects|DE Portfolio Projects]] — "think backward from what the business needs" is the recommended starting exercise
- [[data-engineering/small-scale-pipeline-design|Small-Scale Pipeline Design]] — applies this "understand the problem scope" discipline to the everyday small pipeline (its five-question scoping step is a lighter version of these five steps)
- [[productivity/working-with-stakeholders|Working with Stakeholders]] — the relationship side of sign-off and buy-in (productivity)
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [How to gather requirements for your data project (Start Data Engineering)](../../raw/web/how-to-gather-requirements-for-your-data-project-start-data.md)
[^src2]: [How to Build Data Architectures Faster — Output Led Engineering (Kahan Data Solutions)](../../raw/email/email-2025-07-24-how-to-build-data-architectures-faster.md)
