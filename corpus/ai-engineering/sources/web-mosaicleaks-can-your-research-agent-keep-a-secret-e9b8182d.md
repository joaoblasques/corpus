---
type: source
domain: ai-engineering
status: stub
sources:
  - path: raw/_inbox/web-mosaicleaks-can-your-research-agent-keep-a-secret-e9b8182d.md
    channel: web
    ingested_at: 2026-07-04
aliases:
  - MosaicLeaks
  - mosaic leakage
tags:
  - corpus/ai-engineering
  - source
created: 2026-07-04
updated: 2026-07-04
---

# MosaicLeaks: Can your research agent keep a secret?

**TL;DR.** MosaicLeaks is a benchmark (1,001 multi-hop research chains) evaluating whether deep-research agents leak private enterprise information through their web query logs — the "mosaic effect." Models tested frequently leaked. PA-DR (Privacy-Aware Deep Research), an RL training method, reduces leakage from 34.0% to 9.9% while improving task success [^src1].

Three leakage types measured: intent leakage (adversary infers research goals), answer leakage (adversary can answer private questions from query log), full-information leakage (adversary discovers private facts without being given the question) [^src1].

PA-DR raises strict chain success from 48.7% to 58.7% while reducing answer/full-information leakage from 34.0% to 9.9% [^src1]. Key insight: "training only for task performance made it worse" [^src1].

[^src1]: [MosaicLeaks: Can your research agent keep a secret?](../../raw/_inbox/web-mosaicleaks-can-your-research-agent-keep-a-secret-e9b8182d.md) — Hugging Face blog, ServiceNow, 2026-06
