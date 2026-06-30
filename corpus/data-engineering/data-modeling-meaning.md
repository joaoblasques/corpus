---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2025-11-05-semantics-ontology-and-taxonomy-and-metadata-foundations-for.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/_inbox/web-where-data-engineering-is-heading-in-2026-5-trends-fe513e25.md
    channel: web
    ingested_at: 2026-06-29
  - path: raw/_inbox/web-the-insanity-of-data-education-c2478cdc.md
    channel: web
    ingested_at: 2026-06-29
  - path: raw/youtube/youtube-7jbcvxmj1bs.md
    channel: youtube
    ingested_at: 2026-06-17
  - path: raw/email/email-2025-08-06-data-modeling-theory-vs-reality.md
    channel: email
    ingested_at: 2026-06-19
aliases:
  - semantics
  - ontology
  - taxonomy
  - controlled vocabulary
  - meaning in data modeling
  - data modeling meaning
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-15
updated: 2026-06-19
---

# Meaning in Data Modeling: Semantics, Taxonomy, Ontology

**TL;DR.** Data modeling silently assumes data *has meaning* — but "what does it mean, for whom?" [^src1]. This is a draft chapter from Joe Reis's data-modeling book establishing four building blocks for capturing meaning: **semantics** (how we describe agreed meaning in language), **taxonomies** (hierarchical organisation), **ontologies** (formal, machine-readable meaning), and **metadata** [^src1]. AI is shifting modeling from "structure only" to "structure plus semantics," because LLMs both consume and generate data and need explicit business meaning to reason rather than guess [^src1].

## Why meaning is the missing link

Many modeling failures are really ignored semantics — integration failures, mismatched assumptions, scattered definitions [^src1]. Classic example: few companies have a single definition of "Customer" (last order? quantity? a 10-year-old free sample?) [^src1]. **Meaning is mostly subjective, sometimes objective, and depends on context** — unlike math (`2+2=4`) or chemistry (H₂O) [^src1]. Because models serve a *group*, the modeler's job is to capture **shared meaning** — the overlap of individual meanings — agreed and understood across (and between) organisations [^src1].

## Semantics — describing agreed meaning

If meaning is what we agree something is, **semantics is how we describe and preserve that agreement in language** [^src1]. A semantic model defines what a "customer" *is* (attributes, relationships to orders/products), not just a `cust_id` field — crucial for business users and, increasingly, machines [^src1]. Key tools [^src1]:
- **Controlled vocabulary** — a pre-defined authorised list of terms ensuring consistent labelling; controls synonyms (e.g. "Data Engineer" maps to "ETL Developer", "Data Platform Engineer") and disambiguates polysemous terms ("platform" → "cloud platform" / "data platform").
- **Thesaurus** — an advanced controlled vocabulary that also defines *relationships*: hierarchical broad/narrow (Data → Data Modeling), related-term (Data Modeling ↔ Data Governance), and equivalence (MLOps ↔ ML Operations).

This disambiguation gets harder moving from SQL keys (`client_id` vs `customer_id`) to **natural-language prompts** ("top clients" vs "top customers for region X") — exactly where an LLM needs correctly-mapped semantics [^src1]. See [[data-engineering/semantic-layer|Semantic Layer]] for the operational layer.

## Taxonomies — organising into hierarchies

A **taxonomy** is an organised "tree" of related concepts, broad → specific (a product catalog: All Products → Electronics → Phones/Computers/Gaming/Drones) [^src1]. Hierarchy direction matters (Electronics is a parent of Phones, not vice-versa) [^src1]. Beyond UX, taxonomies give two data-management benefits [^src1]:
1. **Standardise terms** — one "Geography" taxonomy resolves the West/Pacific/"CA,OR,WA" mismatch across sales/marketing/finance.
2. **Improve governance & quality** — enforce that a field holds only approved values (a "Sandwich" under Electronics is rejected).

## Ontologies — flexible, machine-readable structure

> "An ontology is an explicit specification of a conceptualization." — Tom Gruber [^src1]

Where semantics gives meaning and taxonomies organise it hierarchically, an **ontology captures informal meaning in a formal semantic model for human *and machine* interpretability** — defining concepts (Customer, Product, Order), their relationships (a Customer *places* an Order), and rules/constraints (every Order must have ≥1 Product) [^src1]. To make it machine-readable, ontologies use logic-based languages like **RDF** or **OWL (Web Ontology Language)**; the chapter walks an OWL example (`Class: Customer SubClassOf Person`) [^src1]. The next step beyond a taxonomy is "a formal framework that lets machines not just read the data, but reason over it" [^src1].

## Metadata

Semantics also clarifies *individual attributes* through rich **metadata** that travels with the data — tagging a field's units, or specifying `Status` as an enum with business-rule-defined allowed values — so the model carries business context, not just raw data [^src1].

## Why this matters now (AI)

With AI as both consumer and generator of data, semantics is "no longer a second-class citizen" — the difference between an agent that **reasons** and one that **guesses** [^src1]. This is the modeling foundation beneath the [[data-engineering/semantic-layer|semantic layer]] and [[data-engineering/progressive-disclosure-analytics-agents|analytics-agent]] reliability.

## The master-data layer as the locus of agreed meaning

The book's "shared meaning" abstraction has a concrete operational home in practice. Zach Wilson describes a **master-data layer** built by joining, deduping, and **conforming** production snapshots into one consistent definition — "this is the layer where truth is... where trust is" [^src2]. This is the semantic-agreement problem in physical form: without it, five analysts compute the same metric five subtly-different ways on raw snapshots [^src2]. Capturing shared meaning (this page) and materializing it as conformed master data (operational) are two faces of the same discipline. See [[data-engineering/dimensional-modeling|Dimensional Modeling]] for the OLTP→master-data→OLAP continuum, and [[data-engineering/data-quality|Data Quality]] for conformance enforcement.

## Theory vs reality: the organizational dimension

Capturing meaning is the *theory*; a separate draft chapter from the same book stresses that **most data-modeling initiatives fail on people, not technique** [^src3]. Theory imagines a sterile top-down exercise in an orderly org; reality is "a tough and unpredictable place" where the modeler's job is a mix of *practitioner, sales, and servant* [^src3]. Five recurring reality-checks [^src3]:

- **Ivory-tower modeling.** Instead of gathering clean requirements from eager stakeholders, you reverse-engineer arcane undocumented systems under deadline pressure; business rules are fuzzy, stakeholders contradict each other, requirements shift mid-project, and the data may not match the domain language (a model says "customer" but includes prospects, partners, employees). Approach each situation with an eye on *what can go wrong and when*, not on perfection.
- **Data is political.** "Every data model is a political artifact" — it reflects who had influence, what got prioritized, and what got ignored. A department may resist a more-accurate customer definition precisely because it makes their legacy metrics look worse. Expect some to support and some to sabotage.
- **Needs and expectations vary.** No single model fits everyone; the relational model is *not* universally applicable. One model typically feeds many: decision-makers need digestible data, analysts need explorable data, engineers need cost-efficiency and performance, and ML/AI needs clean features. *"You wouldn't hand a CEO a raw ML model output, and you wouldn't give a software engineer a star schema."*
- **Compromises happen.** A perfect textbook model that takes years loses to delivering value quickly under real time/budget constraints. What matters is value for the situation at hand, not textbook fidelity.
- **Don't fixate on tools and technology.** The goal is a *shared understanding* of the data; overly technical diagrams distract non-technical people. "Engaging and thoughtful conversations are more critical than diagrams — diagrams are the *result* of those conversations, not the reason to have them."

The takeaway: data modeling demands **situational and social awareness**, not only technical approaches — the same "shared meaning across a group" problem this page frames semantically, viewed through organizational dynamics [^src3]. See [[productivity/working-with-stakeholders|Working with Stakeholders]] and [[data-engineering/requirements-gathering|Requirements Gathering]] for the practitioner-and-sales side.

## The 2026 crisis: survey data

A February 2026 survey of 1,101 data practitioners and leaders (Joe Reis, Practical Data Community) quantifies the scale of the organizational dysfunction this page frames theoretically [^src4][^src5]:

- **89% report pain points** with their data modeling approach; only 11% say things are going well
- **59% cite constant time pressure** as the primary obstruction
- **51% cite lack of clear ownership**
- Only **5% are using semantic models** — suggesting the solution space (§ Semantics above) is vastly underutilized

The survey shows a concrete downstream effect: **38% of ad-hoc modelers are constantly firefighting** vs. teams with a disciplined modeling approach, who fight fewer fires [^src4]. This is the "organizational dimension" (§ Theory vs reality) expressed as measurable operational cost.

Two AI-era paths from here [^src4]:
- **Path A**: Semantic and context layers go mainstream — AI makes explicit semantics viable and necessary
- **Path B**: AI generates models on the fly, bypassing the semantic layer entirely (Joe Reis's prediction: Path A happens first, Path B eats it in 2027–2028 as models get strong enough to interpret messy schemas)

**Ownership vs. education**: Joe Reis's 2026 piece on data education argues directly that blame-the-practitioner is the wrong frame [^src5]. The 40-year echo chamber — data industry repeating the same educational mistakes and blaming practitioners for not following 40-year-old methodologies — is insanity by the literal definition: doing the same thing and expecting different results. The 51% ownership void is a leadership failure, not a skills failure [^src5].

> "If the data industry has been teaching and preaching the same way for four decades and the vast majority of practitioners are still struggling, clearly the approach hasn't worked. At this point, we cannot keep blaming the practitioners." — Joe Reis [^src5]

The prescribed reset [^src5]:
1. **Teach building blocks, not religion** — pragmatic, modular primitives; drop the dogmatic 600-page textbooks
2. **Invest in team growth** — giving people powerful tools without training is handing a teenager car keys without a driving lesson
3. **Solve the ownership void** — assign actual ownership, give top-down air cover to slow down and build things right
4. **Compete for attention** — if the material is boring, it loses to ChatGPT and Slack pings; digestible + directly applicable wins

## 2026 survey: data modeling is a people/process problem

Joe Reis's 2026 survey data reframes the modeling failure as organizational rather than technical [^src6]:

- **4.8%** of teams cite tooling as the primary data modeling problem
- **95.2%** cite training, unclear requirements, time pressure, and ownership gaps
- **19.2%** of teams have a dedicated data modeler role (majority have no one whose explicit job is data modeling)

The implication: better tooling (dbt v2, AI-assisted schema design) addresses the 4.8%, while the 95.2% is a management and organization design problem. Teams that jump to new tools without solving the ownership and requirements problem get faster data modeling failure, not better data modeling [^src6].

See also [[data-engineering/vibe-engineering|Vibe Engineering]] for the related problem of building data systems without theoretical grounding.

## Related

- [[data-engineering/requirements-gathering|Requirements Gathering]] — the practitioner/sales/servant work of pulling requirements out of stakeholders
- [[data-engineering/semantic-layer|Semantic Layer]] — the operational layer applying these foundations to AI
- [[data-engineering/dimensional-modeling|Dimensional Modeling]] — master-data layer; consumer-driven modeling
- [[data-engineering/dimensional-modeling|Dimensional Modeling]] — structural modeling (Kimball)
- [[data-engineering/data-quality|Data Quality]] — taxonomies as governance/constraint enforcement
- [[ai-engineering/rag|RAG]] — knowledge graphs / ontologies as retrieval substrate (ai-engineering)
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [Semantics, Ontology, and Taxonomy, and Metadata — Foundations for Meaning in Data Modeling](../../raw/email/email-2025-11-05-semantics-ontology-and-taxonomy-and-metadata-foundations-for.md)
[^src2]: [Dimensional Data Modeling Day 1 (Zach Wilson / DataExpert)](../../raw/youtube/youtube-7jbcvxmj1bs.md)
[^src3]: [Data Modeling - Theory vs Reality (Joe Reis, Practical Data Modeling)](../../raw/email/email-2025-08-06-data-modeling-theory-vs-reality.md)
[^src4]: [Where Data Engineering Is Heading in 2026 — 5+ Trends](../../raw/_inbox/web-where-data-engineering-is-heading-in-2026-5-trends-fe513e25.md) — Joe Reis, Practical Data Community survey (1,101 respondents, Feb 2026)
[^src5]: [The Insanity of Data Education](../../raw/_inbox/web-the-insanity-of-data-education-c2478cdc.md) — Joe Reis, Practical Data Community
[^src6]: [Why 90% of Data Teams Are Failing at Data Modeling](../../raw/_inbox/web-why-90-of-data-teams-are-failing-at-data-modeling-33d8f9be.md) — Joe Reis, Practical Data Community
