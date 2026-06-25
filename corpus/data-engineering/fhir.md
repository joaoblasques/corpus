---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/web/overview-clinical.md
    channel: web
    ingested_at: 2026-06-25
aliases:
  - FHIR
  - Fast Healthcare Interoperability Resources
  - HL7 FHIR
  - FHIR resource
  - FHIR REST API
  - FHIR Observation
  - FHIR Composition
  - healthcare interoperability
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-25
updated: 2026-06-25
---

# FHIR (Fast Healthcare Interoperability Resources)

**TL;DR.** FHIR (Fast Healthcare Interoperability Resources) is an HL7 standard for the **exchange of healthcare information** — clinical data, administrative records, public health data, and research data — between electronic systems [^src1]. It defines a set of **Resources** (discrete, typed data objects, like "forms" for allergy lists, prescriptions, referrals, etc.) and a **REST API** for querying and updating them. FHIR is the dominant modern standard for healthcare data interchange, backed by a large ecosystem of EHR vendors (Epic, Cerner), cloud platforms, and analytics tools.

## The Resource model

Think of a FHIR **Resource** as a standardized paper form for a clinical concept [^src1]:
- One resource type per concept: Allergy, Medication, Observation, Patient, Encounter, etc.
- Each resource is **highly focused** (small amount of data); multiple resources assembled form a complete clinical record.
- A Resource carries both **discrete data** (structured fields for computation) and a **human-readable narrative** (so clinicians can always read the record even if the receiving system doesn't parse discrete data) [^src1].

A FHIR **repository** can be an EHR (Epic, Cerner), pharmacy system, HIS, or a decision-support engine. Systems expose a FHIR REST API; internally they may store data in any format [^src1].

## Core design principles

**Extensibility without breaking interoperability** [^src1]: Resources include only data elements present in *most* implementations. Elements like "deceased date" are in the base resource (commonly tracked). "Hair color" is omitted and must be added as a **FHIR extension** when needed — extensions add fields without changing the wire format, so systems that don't understand an extension can still consume the base resource.

**Profiles** constrain resources for specific contexts [^src1]: a blood pressure profile constrains the `Observation` resource to require specific LOINC codes and value types. Profiles coexist — a receiver can consume an extended/profiled resource even without knowing the profile.

**Broad coverage** [^src1]: intended for inpatient, ambulatory, acute, long-term, community, and allied health; human and veterinary medicine; usable worldwide.

## Exchange paradigms

FHIR supports four exchange mechanisms [^src1]:

| Paradigm | Mechanism | Use case |
|---|---|---|
| **REST** | `GET`, `PUT`, `POST`, `DELETE` on resource instances via a FHIR server | Clinical decision support, patient portals, app integrations |
| **Documents** | A `Composition` resource (cover page) + bundled resource instances; "stapled" together as a snapshot | Discharge summaries, lab reports, referrals |
| **Messages** | A `MessageHeader` (requisition) + paper-clipped resources; event-driven | Patient admission events, lab order requests, bed transfers |
| **Services** | Lightweight: a small "sticky note" (parameters) + fragment resources; synchronous request-response | Decision support: "Is drug X safe for patient Y?" |

REST is the simplest; the server is like "a room full of filing cabinets" — one cabinet per resource type, each folder is one entity (one Patient, one Encounter), each piece of paper a version [^src1].

### REST operations

- `GET /Patient/123` — read a resource instance
- `GET /Patient?name=Smith` — search for resources
- `PUT /Patient/123` — update a resource instance
- `POST /Patient` — create a new resource instance
- `DELETE /Patient/123` — delete an instance

## Key resource types for data engineering

| Resource | Data it holds |
|---|---|
| `Patient` | Demographics: name, DOB, gender, address |
| `Observation` | Vital signs, lab results, assessments (highly reused across domains) |
| `Encounter` | A clinical visit or contact |
| `Condition` | Diagnosed conditions / problems |
| `MedicationRequest` | Prescriptions |
| `Procedure` | Procedures performed |
| `Composition` | Document cover page (links other resources into a document) |

The `Observation` resource is notably broad: it covers vital signs, lab results, psychological assessments, and other measurable data — all via the same resource type, differentiated by LOINC/SNOMED codes [^src1].

## Data engineering implications

**FHIR as a source for analytics pipelines**:
- FHIR REST APIs are the standard integration surface for extracting clinical data from EHR systems. The [Bulk FHIR API](https://hl7.org/fhir/uv/bulkdata/) (`$export`) enables large-scale async extraction of all resources for a population [^unsourced — verify].
- Raw FHIR resources are deeply nested JSON/XML — not query-friendly. Typical pipelines flatten FHIR into tabular form, often mapped to **OMOP CDM** (Observational Medical Outcomes Partnership Common Data Model) for standardized analytics [^unsourced — verify].
- Key challenges: handling resource versioning, extensions, and profile variants; managing PHI (Protected Health Information) under HIPAA; deduplicating patient matching across systems (MPI — Master Patient Index).

**FHIR and data warehousing**: raw FHIR JSON lands in a bronze/raw layer; transformations produce flattened clinical tables (silver) and OMOP or domain-specific analytical models (gold). See [[data-engineering/medallion-architecture|Medallion Architecture]].

**Tooling**: Spark's `from_json` + schema inference handles FHIR JSON in a data lake; AWS HealthLake and Google Cloud Healthcare API provide managed FHIR servers with BigQuery export.

> Note: FHIR analytics patterns (OMOP mapping, Bulk FHIR, PHI handling) are marked `[unsourced — verify]` above — these reflect standard practice but were not in the indexed source.

## Related

- [[data-engineering/medallion-architecture|Medallion Architecture]] — bronze → silver → gold fits FHIR data lakes
- [[data-engineering/bigquery|BigQuery]] / [[data-engineering/snowflake|Snowflake]] — common analytical targets for FHIR-sourced clinical data
- [[data-engineering/etl-pipeline|ETL Pipeline]] — FHIR is an API-based extraction source
- [[data-engineering/change-data-capture|Change Data Capture (CDC)]] — capturing EHR changes can use CDC alongside FHIR subscriptions
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [FHIR Clinical Overview — HL7 FHIR Specification](../../raw/web/overview-clinical.md)
