---
type: concept
domain: mlops
status: draft
aliases:
  - data provenance
  - AI reproducibility
  - reproducible AI
  - data lineage for AI
  - data versioning for ML
  - ML reproducibility
tags:
  - corpus/mlops
  - concept
  - data-governance
  - reproducibility
sources:
  - path: raw/web/web-reproducible-ai-a-practical-guide-to-data-provenance-16cdecef.md
    channel: web
    ingested_at: 2026-08-20
created: 2026-08-20
updated: 2026-08-20
---

# Data Provenance and AI Reproducibility

**TL;DR**: Reproducible AI requires tracing every input (data, prompt, retrieved context), every transformation, and every environment configuration so failures can be debugged and results re-created. The central challenge: data is not versioned by default the way code is, creating invisible failure modes.[^src1]

## The core problem

When AI systems produce bad outputs, the root cause is almost always upstream in the data, not the model. "Bad outputs can be traced back to bad inputs: flawed data, unclear lineage, or uncontrolled environments." Smarter models don't fix this; provenance infrastructure does.[^src1]

An AI system is: `input → function → output`. We control the input most, yet data remains the least-versioned component of the stack.[^src1]

## Why traditional Git isn't enough for data

Git works for code but was not designed for massive data lakes. Enterprise data environments can reach petabyte or exabyte scale, requiring data-native tools that bring the same lifecycle discipline to data at volume.[^src1]

## What provenance requires (data layer)

Track for every dataset:

- Who last modified it and when
- What was added or changed (commit-like diff)
- Where it came from (source URLs, upstream system)
- What code/pipeline produced it (linked commit IDs)
- Ownership and ingestion frequency[^src1]

## Guardrails: staging before production

Ingest data into an isolated branch or staging area first. Automated checks validate before promotion — analogous to a pull request:

- **Privacy / compliance**: no PII in dataset
- **Format**: lands in expected format (Parquet, Iceberg)
- **Content quality**: prohibited patterns / unsafe content
- **Statistical drift**: column distributions vs. previous version
- **Schema compatibility**: backward-compatible changes
- **Organization-specific rules**: any custom quality gate[^src1]

If the data fails any gate, it doesn't reach production. The failing snapshot is preserved for inspection without impacting production.[^src1]

## Reproducibility of the compute layer

Data provenance alone isn't enough. Also make the function (model + runtime) reproducible:

- Make randomness explicit: set seeds so processes are repeatable even if random
- Lower temperature where appropriate: reduces creativity, improves stability
- Measure similarity, not exact equality: outputs can differ run-to-run but should remain within bounds
- Connect data to code: link datasets to the exact code that generated them
- Make infrastructure reproducible: infrastructure-as-code, pinned dependencies[^src1]

## Agentic systems need more provenance

For agents making decisions and taking actions, capture:

- Plans and specs (how the agent decided to approach a task)
- Decision records (what did it do and why)
- Inputs and supporting artifacts: documents, retrieved context, web search results, tool calls and outputs
- Model version, execution environment, and system configuration[^src1]

"This data is usually cheap to store and extremely valuable when something goes wrong."[^src1]

## Tooling

[lakeFS](/data-engineering/lakefs.md) is the reference implementation mentioned — a control plane for AI-ready data that provides isolated branches for ingestion, quality gates before promotion, and commit-level provenance linking data to code, on top of object storage.[^src1]

[^src1]: raw/web/web-reproducible-ai-a-practical-guide-to-data-provenance-16cdecef.md — lakeFS blog, "Reproducible AI: A Practical Guide to Data Provenance"
