---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/web/building-the-data-mart.md
    channel: web
    ingested_at: 2026-06-16
aliases:
  - data mart
  - data marting
  - data marts
  - data warehouse vs data mart
  - hybrid DSS model
  - Demarest hybrid model
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-16
updated: 2026-06-16
---

# Data Mart

**TL;DR.** A data mart is a user community-specific data store focused on decision-support (DSS) end-user requirements, presenting only the data a constituency needs in a form close to its business model[^src1]. Marc Demarest (1993) argues against choosing between enterprise data warehousing and data marting, proposing instead a hybrid multitiered model: one central warehouse feeds many community-specific marts — "the corner stores of the enterprise"[^src1].

## The two conventional models

DSS architecture historically posed two "mutually exclusive" alternatives[^src1]:

- **Data warehousing** focuses on a single large server/mainframe consolidating enterprise data from diverse production systems into a unified model; it protects production data but treats end-user access as an afterthought[^src1].
- **Data marting** deals almost exclusively with servicing a distinct community of knowledge workers, ignoring the practical difficulty of protecting production systems from extraction impact[^src1].

The warehouse stores data at the lowest level of detail (individual customer names, UPC/SKU codes, sales orders, invoice line items); marts roll that detail up to each community's level of understanding[^src1]. See [Dimensional Modeling](/data-engineering/dimensional-modeling.md) for the fact/dimension modeling these marts typically use, and [Pipeline Layers](/data-engineering/pipeline-layers.md) for the modern staging→warehouse→marts ELT separation that mirrors this split.

## Four goals of data warehousing (and their flaws)

Demarest lists the warehouse's four goals and critiques each[^src1]:

1. **Protect production systems** from query drain — worthy and necessary.
2. **Improve data manageability** — has merit; DSS data is a unique enriched asset, not just a copy.
3. **Build an Enterprise Data Model (EDM)** — honorable but expensive; flawed for non-technical reasons (autonomous business units refusing data, cross-region legal constraints, constant annual revision).
4. **Separate data management from end-user access** — a shortcoming in practice, forcing expensive paper-based reporting on proprietary tech.

A key failure mode named is **schema explosion**: as each community adds views, summary tables, and aggregations, table count balloons and legibility suffers. Demarest's rule of thumb: past ~20 tables, the average knowledge worker's ability to navigate the warehouse becomes impaired[^src1].

## Why marts alone fall short

Data marts deliver legibility and ride the client/server price-performance curve, but on their own they[^src1]:

- overestimate LAN-based data-management tool capability (flat-file/small RDBMS can't sustain high-performance queries or large timely extracts);
- create a "network and extraction chaos" when many marts extract from many production systems;
- address only small companies with few knowledge workers, single markets, simple product lines;
- invite unauthorized "shadow" marts built outside IS control.

## The hybrid multitiered model

Demarest's synthesis treats **information as a product**, built by knowledge workers from data warehoused for economy of distribution and "retailed based on local need" — analogous to grocery distribution (manufacturer → warehouse → local store)[^src1]. The hybrid delivery has four processes[^src1]:

1. **Extract** relevant data from OLTP sources (copy, scrub, enrich — translating cryptic codes to readable text).
2. **Store** the result in one location, the data warehouse, schematized into an EDM.
3. **Create** a unique cut (or cuts) of the warehouse per knowledge-worker community — the data marts.
4. **Supply** decision-support tools appropriate to each community's computing style.

> "Data marts are the 'corner stores' of the enterprise, and each unique knowledge worker community has its own mart"[^src1].

Architectural division of labor[^src1]:

- **One warehouse per enterprise**, residing near major OLTP systems; corporate IS data architects own it and the enterprise's historic data.
- The warehouse is **built for bulk extracts**; marts are **built for fast response** to specific end-user questions, so a mart is organized/indexed differently and anticipates common questions by hard-coding answers rather than building them dynamically.
- **Marts are owned by the divisional/departmental IS group** closest to the end-user constituency — placing data-marting responsibility there ends the "information wars" between corporate and divisional regimes.
- A **master/slave control policy** decides whether extraction instructions live in the mart ("pump") or the warehouse — a policy choice each enterprise resolves per its data-management approach.

## Gotchas / framing

- The article is from 1993 (last updated 1997); terminology (3270 terminals, CICS, VSAM/QSAM, EISs) and the "data warehousing is dead" Forrester claim are period artifacts, but the warehouse-vs-mart tension and the hybrid resolution remain the conceptual ancestor of the modern lakehouse + marts split.
- "Information-on-demand" is framed as the basis of good DSS architecture: knowledge workers are *customers*, data is the *raw material*[^src1].

[^src1]: [Building The Data Mart](../../raw/web/building-the-data-mart.md)
