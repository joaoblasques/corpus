---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/web/standardized-data-the-omop-common-data-model.md
    channel: web
    ingested_at: 2026-06-25
aliases:
  - OMOP CDM
  - OMOP Common Data Model
  - Observational Medical Outcomes Partnership CDM
  - OHDSI
  - CDM
  - observational database
  - healthcare common data model
  - clinical data model
  - observational health data
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-25
updated: 2026-06-25
---

# OMOP Common Data Model (CDM)

**TL;DR.** The OMOP CDM (Observational Medical Outcomes Partnership Common Data Model), developed and maintained by **OHDSI** (Observational Health Data Sciences and Informatics), is a standardized schema for converting heterogeneous observational health databases into a common format. Once converted, a library of standard analytic tools can run against any OMOP-conformant database, enabling collaborative research across institutions and countries [^src1]. It is the dominant interoperability standard for real-world observational health data — distinct from [FHIR](/data-engineering/fhir.md) (a real-time data exchange standard) in that OMOP targets analytics over accumulated records rather than point-of-care data exchange.

## Why it exists

Healthcare data varies enormously between organizations [^src1]:
- **Different purposes** — clinical practice (EMR), insurance reimbursement (claims), clinical research
- **Different formats** — different database systems and information models
- **Different terminologies** — the same concept (e.g. blood glucose) may be represented in dozens of ways across institutions (ICD-10, SNOMED CT, LOINC, NDC, custom codes)

These differences make multi-site studies slow and expensive: each collaboration requires bespoke data transformation work. The CDM solves this by transforming data into a **common format** and a **common representation** (standardized terminologies and vocabularies) once, so that any compliant analytic tool works everywhere [^src1].

## What OMOP CDM provides

The OMOP CDM defines [^src1]:

1. **A data model** — a shared schema into which clinical tables from EMRs and administrative claims are mapped. Tables include: `person`, `visit_occurrence`, `condition_occurrence`, `drug_exposure`, `measurement`, `procedure_occurrence`, `observation`, and others.
2. **Standardized terminologies** — a set of vocabulary mappings (SNOMED CT, LOINC, RxNorm, etc.) that normalize source codes into CDM-standard concept IDs. Source codes are preserved alongside the standard concept for traceability.
3. **A library of standard analytic routines** — tools written against the CDM that can run on any conformant database: characterization, patient-level prediction, comparative effectiveness, safety surveillance, quality of care.

## OHDSI tools ecosystem

OHDSI (pronounced "odyssey") develops open-source tooling on top of the CDM [^src1]:

- **ACHILLES** — data quality and characterization (counts, distributions, data quality checks across the CDM tables)
- **ATLAS** — browser-based cohort definition and study design tool
- **HADES** (Health Analytics Data-to-Evidence Suite) — R packages for population-level effect estimation, patient-level prediction, and characterization
- **WhiteRabbit / RabbitInAHat** — source data profiling and ETL mapping tools

Commercial tools also exist alongside the OSS ecosystem.

## CDM source types

The CDM accommodates both major real-world data types [^src1]:
- **Electronic Medical Records (EMR)** — clinical data from point-of-care systems; rich clinical detail but bounded to a specific institution
- **Administrative claims** — insurance reimbursement data; broader population coverage but less clinical granularity

## Relationship to FHIR

| | OMOP CDM | FHIR |
|---|---|---|
| **Primary purpose** | Analytics over accumulated observational records | Real-time data exchange between clinical systems |
| **Paradigm** | Retrospective bulk conversion (ETL) | Event-driven API calls (REST) |
| **Standardization** | Schema + vocabulary | Resource types + terminology bindings |
| **Temporal** | Accumulated longitudinal history | Current + point-in-time |
| **Audience** | Researchers, epidemiologists, clinical analysts | EHR vendors, HIE, clinical workflows |

Both standards increasingly interact: FHIR-to-OMOP pipelines (e.g. `fhir2omop`) convert FHIR resources into CDM tables to enable OHDSI analytics on FHIR-native systems. See [FHIR](/data-engineering/fhir.md) for the exchange-standard detail.

## ETL to OMOP

Converting a source database to OMOP CDM is called an **ETL** in the OHDSI community — typically a major project. OHDSI provides:
- The **ETL Design Process** and community tutorials
- **WhiteRabbit** for source data profiling (frequency distributions, value sets)
- **RabbitInAHat** for graphically mapping source fields to CDM fields
- A large community of members who have done prior conversions and can provide guidance [^src1]

> [unsourced — verify] Typical OMOP ETL projects take weeks to months and require both clinical domain knowledge (understanding what source codes mean) and data engineering skills (building scalable, reproducible ETL pipelines). dbt is increasingly used for OMOP ETL in modern data stacks.

## Use cases supported post-conversion

After ETL to OMOP CDM, evidence can be generated for [^src1]:
- **Safety surveillance** — detecting adverse drug reactions across large populations
- **Comparative effectiveness research** — comparing treatment outcomes
- **Quality of care** — benchmarking clinical quality metrics
- **Patient-level prediction** — building ML models for readmission, progression, etc.
- **Characterization** — describing population demographics and disease burden

## Related

- [FHIR](/data-engineering/fhir.md) — the complementary HL7 standard for real-time healthcare data exchange
- [ETL Pipeline](/data-engineering/etl-pipeline.md) — OMOP conversion is one of the most standardized ETL use cases in healthcare
- [dbt](/data-engineering/dbt.md) — increasingly used for OMOP ETL pipelines
- [Data Quality](/data-engineering/data-quality.md) — ACHILLES is essentially a data-quality framework for the CDM
- [Data Engineering hub](/data-engineering/README.md)

---

[^src1]: [Data Standardization: The OMOP Common Data Model (OHDSI)](../../raw/web/standardized-data-the-omop-common-data-model.md)
