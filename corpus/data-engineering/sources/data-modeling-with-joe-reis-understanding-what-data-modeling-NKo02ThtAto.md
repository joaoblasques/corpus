---
type: source
domain: data-engineering
status: draft
sources:
  - path: raw/youtube/youtube-NKo02ThtAto-data-modeling-with-joe-reis-understanding-what-data-modeling.md
    channel: youtube
    ingested_at: 2026-07-02
aliases: []
tags:
  - corpus/data-engineering
  - source
  - youtube-quick-intake
  - data-modeling
  - joe-reis
created: 2026-07-02
updated: 2026-07-22
provisional: false
youtube_video_id: NKo02ThtAto
url: https://youtu.be/NKo02ThtAto
channel_name: Seattle Data Guy
playlist: Corpus_queue
published: 2023-07-15
transcript_status: ok
---

# Data Modeling With Joe Reis - Understanding What Data Modeling Is And Where It's Going

> **Source** (YouTube · Seattle Data Guy · 2023-07-15). [watch](https://youtu.be/NKo02ThtAto) · [transcript](../../../raw/youtube/youtube-NKo02ThtAto-data-modeling-with-joe-reis-understanding-what-data-modeling.md)

A live conversation between Ben (Seattle Data Guy) and Joe Reis — co-author of *Fundamentals of Data Engineering* — on what data modeling actually is, where the industry goes wrong, and the three-level modeling framework practitioners should internalize.

---

## TL;DR

Data modeling is not Kimball. Kimball is one technique. Data modeling is the broader discipline of representing business reality in data — for humans and machines across the full data lifecycle. The industry defaults to physical/query-driven modeling and skips the more valuable conceptual and logical levels. Reis argues the field has accumulated forgotten best practices (patterns, normalization theory, classic texts) that are more relevant than ever as AI raises the stakes for clean, well-understood data.

---

## Reis's definition

> "Organizing and standardizing data to facilitate believable and useful information and knowledge for humans and machines."[^1]

Key departure from historical usage: the explicit inclusion of **machines** as consumers. With LLMs now able to introspect datasets, Reis argues "the machines part was definitely necessary to future-proof the definition."[^1] Data modeled only for analysts will not serve AI pipelines.

---

## The conflation problem: tactics vs. practices

The industry conflates a specific technique — Kimball dimensional modeling — with data modeling as a whole. Reis uses the analogy: "It's like saying that martial arts is karate."[^1] Dimensional modeling (facts, dimensions, measures) is table-stakes and has been since 1996, but it is one tool in a much larger toolkit that includes normalization, entity-relationship modeling, data vault, activity schemas, and one-big-table.

Knowing a technique is not enough. "You have to know what you're doing in order to know not to apply it. To willfully ignore these things is professional recklessness."[^1]

---

## The three modeling levels

Reis frames modeling as three layers that should be worked **top-down**, not bottom-up:

| Level | Description | Technology dependency |
|---|---|---|
| Conceptual | Entities, processes, relationships — how the business works | None |
| Logical | Intermediate translation: cardinality (1:1, 1:N, M:N), data organization | None |
| Physical | Implementation in a specific database system, optimized for workload | High |

The dominant failure mode: "Starting from physical and trying to work backwards — it's not really going to work."[^1] The industry effectively skips conceptual and logical and lands directly on physical (or its extreme: query-driven modeling, where a dbt model is created to answer one specific question with no higher-level context).

---

## The process: start with business empathy

Before any SQL or schema, Reis recommends:

1. **Build business literacy** — understand how the domain (e.g., marketing) actually operates.
2. **Develop stakeholder relationships** — understand the world they live in before asking what data they need.
3. **Conceptual modeling first** — identify entities, processes, vocabulary. "Customer" is the canonical example: it means different things to different people in the same company.

"Data modeling really is about translating the business and bridging the business to the data."[^1] The technical steps follow from that, not the other way around.

Software engineers are Reis's most important audience here: "It's more important for software engineers to understand data modeling than it is for data and analytics engineers. Because they're the ones creating the data that analytics and data engineers depend upon."[^1] Bad source-side modeling forces downstream engineers to compensate with complex SQL patches indefinitely.

---

## Query-driven modeling and dbt sprawl

The dominant US-market pattern is what Reis calls **query-driven modeling** (named in his book): create a dbt model to answer a specific question, not to represent a business concept. Extreme form: 39,000 dbt models at one customer site, flagged by dbt Labs CEO Tristan Handy as a known problem.[^1]

Symptoms:
- Moving one number propagates unknown downstream effects.
- No one can explain the grain of a table.
- Update/delete strategies are undefined.
- Slowly changing dimensions are absent even where business history requires them.

The debt accumulates across three dimensions: technical debt (system complexity), data debt (concepts lose fidelity over time), and organizational debt ("a punch pass" of credibility with the business that depletes as data quality failures accumulate).[^1]

---

## US vs. Europe cultural gap

Reis observed a geographic split after spending time in Europe: European companies treat data modeling as a formal, rigorous discipline — the job title "data modeler" is common. US companies optimize for speed, leading to reactive, query-driven approaches. "We tend to gravitate towards the fast part of the pendulum."[^1]

---

## Forgotten knowledge worth recovering

Reis highlights two underappreciated resources:

- **Data model patterns** (Len Silverston & Graham Simpson, *Data Model Resource Books*): reusable conceptual patterns by industry vertical (retail, healthcare, etc.) that can cover 70–80% of a domain's modeling needs. "If you use those patterns, [they] save you so much time. Nobody talks about this stuff now."[^1]
- **Normalization as a conceptual exercise**: even if the physical model will be denormalized or one-big-table, running through a normalization exercise on the logical model surfaces relationships and update/delete side effects before they become production problems.

Classic texts Reis recommends: Kimball's *Data Warehouse Toolkit*; Ted Codd's relational paper; Peter Chen's 1970s ER paper; Inmon's original data warehouse book.

---

## AI and the future of data modeling

Reis's position (as of mid-2023): AI is more likely to **enhance** data practitioners than replace them, but only if the underlying data is coherent. "If we cannot get this right — getting our house in order with data — I think [the AI opportunity] is actually going to be lost."[^1]

Ironically, AI raises the value of business-facing skills: "In the age of AI, the needs for data practitioners to work with a business more closely will be more paramount than ever. You can't hide behind technology anymore."[^1] Someone still needs to know what the correct answer looks like to validate AI outputs.

On dimensional modeling/data vault longevity: "A lack of modeling is still modeling. It's just a really crappy model."[^1] Techniques are not made obsolete by AI — they structure how practitioners think about data at an atomic level, which AI cannot substitute for.

---

## Star schema vs. one big table

Short answer: understand both, know the trade-offs, pick what fits. Questions to answer before choosing one-big-table: What is the grain? What is the update strategy? What is the deletion strategy? "These are all trade-offs you have to deal with with one big table. It's not the savior. It's a technique."[^1]

Practical hybrid common in industry: star schema as the canonical model, pre-joined wide tables surfaced to analysts so they don't perform joins themselves. "We've done the joins. Please don't try to do it yourselves."[^1]

---

## Fundamentals of Data Engineering (v1) relevance

Asked whether the book is still relevant, Reis says yes — it was written to withstand 5–10 years by focusing on immutable concepts (the data engineering lifecycle) rather than specific tools. "If it was a really trendy book that focused on like here's how to do data engineering with Airflow and Kafka — that's going to get outdated."[^1] The technology-agnostic framing held against the generative AI wave.

---

[^1]: [Transcript](../../../raw/youtube/youtube-NKo02ThtAto-data-modeling-with-joe-reis-understanding-what-data-modeling.md) — Joe Reis in conversation with Seattle Data Guy, 2023-07-15.
