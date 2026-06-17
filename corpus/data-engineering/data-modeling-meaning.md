---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2025-11-05-semantics-ontology-and-taxonomy-and-metadata-foundations-for.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/youtube/youtube-7jbcvxmj1bs.md
    channel: youtube
    ingested_at: 2026-06-17
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
updated: 2026-06-15
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

## Related

- [[data-engineering/semantic-layer|Semantic Layer]] — the operational layer applying these foundations to AI
- [[data-engineering/dimensional-modeling|Dimensional Modeling]] — master-data layer; consumer-driven modeling
- [[data-engineering/dimensional-modeling|Dimensional Modeling]] — structural modeling (Kimball)
- [[data-engineering/data-quality|Data Quality]] — taxonomies as governance/constraint enforcement
- [[ai-engineering/rag|RAG]] — knowledge graphs / ontologies as retrieval substrate (ai-engineering)
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [Semantics, Ontology, and Taxonomy, and Metadata — Foundations for Meaning in Data Modeling](../../raw/email/email-2025-11-05-semantics-ontology-and-taxonomy-and-metadata-foundations-for.md)
[^src2]: [Dimensional Data Modeling Day 1 (Zach Wilson / DataExpert)](../../raw/youtube/youtube-7jbcvxmj1bs.md)
