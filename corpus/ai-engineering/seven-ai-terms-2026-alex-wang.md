---
type: synthesis
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-03-resources-articles-neurosymbolic-ai-improving-ai-reasoning.md
    channel: notes
    ingested_at: 2026-07-14
  - path: raw/notes/notes-03-resources-articles-reflective-ai-systems-that-learn-from-their-mistakes.md
    channel: notes
    ingested_at: 2026-07-14
  - path: raw/notes/notes-03-resources-articles-physical-ai-when-ai-gets-a-body.md
    channel: notes
    ingested_at: 2026-07-14
  - path: raw/notes/notes-03-resources-articles-edge-ai-running-ai-on-device.md
    channel: notes
    ingested_at: 2026-07-14
  - path: raw/notes/notes-03-resources-articles-model-routing-choosing-the-right-model-for-the-job.md
    channel: notes
    ingested_at: 2026-07-14
  - path: raw/notes/notes-03-resources-articles-ai-observability-monitoring-ai-in-production.md
    channel: notes
    ingested_at: 2026-07-14
aliases:
  - 7 AI Terms You'll Hear a Lot This Year
  - seven AI terms 2026
  - Alex Wang AI terms
tags:
  - corpus/ai-engineering
  - synthesis
created: 2026-07-14
updated: 2026-07-14
confidence: 0.6
last_confirmed: 2026-07-14
---

# "7 AI Terms You'll Hear a Lot This Year" (Alex Wang) — One Source, Six Corpus Pages

**TL;DR** — Six corpus source pages that look like independent arrivals are all sections of a **single LinkedIn article** by Alex Wang, "7 AI Terms You'll Hear a Lot This Year" [^src1][^src2][^src3][^src4][^src5][^src6]. This page records that shared provenance so the cluster is not mistaken for corroboration from six sources. Its purpose is provenance hygiene, not new technical content.

## Why this page exists

The Obsidian vault stored each section of Wang's article as a separate note, and each note ingested into its own corpus source page. The result reads like six independent sources agreeing that neurosymbolic AI, reflective AI, physical AI, edge AI, model routing, and AI observability are the themes of the year. They are not independent. They are one author's list, split six ways.

Per §7, corroboration requires distinct sources. Anyone counting these pages as separate evidence would be **overcounting a single opinion sixfold**. That is the failure this page exists to prevent.

## The member pages and their shared origin

| Corpus page | Wang's claim |
|---|---|
| [Neurosymbolic AI](/ai-engineering/sources/neurosymbolic-ai-improving-ai-reasoning-ea.md) | Combining neural nets with symbolic reasoning targets structured reasoning, logical consistency, and explainability [^src1] |
| [Reflective AI](/ai-engineering/sources/reflective-ai-systems-that-learn-from-their-mistakes-ae.md) | Systems that evaluate and revise their own outputs; "reflection loops improve accuracy without requiring additional training data" [^src2] |
| [Physical AI](/ai-engineering/sources/physical-ai-when-ai-gets-a-body-bd.md) | AI embedded in machines that sense, move, and act; simulation is key to training it safely [^src3] |
| [Edge AI](/ai-engineering/sources/edge-ai-running-ai-on-device-dece.md) | On-device inference for lower latency, better privacy, lower infrastructure cost [^src4] |
| [Model Routing](/ai-engineering/sources/model-routing-choosing-the-right-model-for-the-job-b.md) | Dynamically select the model per task, balancing cost, speed, and performance [^src5] |
| AI Observability | Monitoring AI in production (collected in the same batch; not yet a corpus page) [^src6] |

Wang's own notes cross-link these sections to each other, confirming they were written as one connected set rather than assembled later [^src1][^src2].

## The through-line Wang argues

Read as one article rather than six, the sections share a thesis: **the 2026 frontier is not bigger models but better system architecture around them**. Each term names a way of composing or constraining models rather than scaling them — symbolic structure bolted onto neural nets [^src1], self-critique loops around generation [^src2], inference moved onto the device [^src4], traffic split across several models [^src5], and monitoring wrapped around the deployed result [^src6].

That framing is coherent and matches practice documented elsewhere in the corpus from independent sources — see [Agent Cost Management](/ai-engineering/agent-cost-management.md) on routing economics and [Agent Evaluation](/ai-engineering/agent-evaluation.md) on external checking. But the through-line above is **one author's synthesis**, and this page does not treat it as established.

## Confidence and limits

`confidence: 0.6` — the technical definitions are uncontroversial and consistent with corpus coverage from other sources, but the source is a single LinkedIn trend-list by one author, captured only as quick-intake stubs rather than full ingests. Trend lists are predictive and promotional by genre; none of the six sections carries evidence for its "you'll hear a lot about this" premise.

Treat individual definitions as usable, and the *selection* of these seven terms as one practitioner's opinion pending independent confirmation.

## Relation to corpus pages

- The six member source pages above — all *derived from* this single origin
- [Agent Cost Management](/ai-engineering/agent-cost-management.md) — independently covers the routing economics Wang asserts
- [Agent Evaluation](/ai-engineering/agent-evaluation.md) — the external-evaluation counterpart to Wang's self-reflection framing
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [Neurosymbolic AI — Improving AI Reasoning](../../raw/notes/notes-03-resources-articles-neurosymbolic-ai-improving-ai-reasoning.md) — Alex Wang, from "7 AI Terms You'll Hear a Lot This Year" (LinkedIn)
[^src2]: [Reflective AI — Systems That Learn From Their Mistakes](../../raw/notes/notes-03-resources-articles-reflective-ai-systems-that-learn-from-their-mistakes.md) — Alex Wang, same article
[^src3]: [Physical AI — When AI Gets a Body](../../raw/notes/notes-03-resources-articles-physical-ai-when-ai-gets-a-body.md) — Alex Wang, same article
[^src4]: [Edge AI — Running AI On Device](../../raw/notes/notes-03-resources-articles-edge-ai-running-ai-on-device.md) — Alex Wang, same article
[^src5]: [Model Routing — Choosing the Right Model for the Job](../../raw/notes/notes-03-resources-articles-model-routing-choosing-the-right-model-for-the-job.md) — Alex Wang, same article
[^src6]: [AI Observability — Monitoring AI in Production](../../raw/notes/notes-03-resources-articles-ai-observability-monitoring-ai-in-production.md) — Alex Wang, same article
