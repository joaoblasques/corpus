---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-03-resources-articles-edge-ai-running-ai-on-device.md
    channel: notes
    ingested_at: 2026-07-14
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - doc-quick-intake
created: 2026-07-14
updated: 2026-07-15
provisional: false
url: 
origin: obsidian
---

# Edge AI — Running AI On Device

**TL;DR:** Edge AI runs AI models directly on local devices rather than the cloud, trading compute power for speed, privacy, and resilience. Hybrid cloud + edge architectures are projected to become the default deployment pattern as models shrink [^src1].

---

## Definition

Edge AI refers to running AI models on local devices — phones, laptops, cameras, or industrial machines — rather than sending data to a remote server [^src1].

---

## Why It Matters

Four properties distinguish edge from cloud inference [^src1]:

- **Reduced latency** — no round-trip to a server.
- **Improved privacy** — data never leaves the device.
- **Lower infrastructure costs** — less cloud compute required.
- **Offline capability** — works without constant internet access.

The source frames the core trade-off as: edge AI "trades cloud power for **speed, privacy, and resilience**" [^src1].

Model compression and efficiency gains are making on-device inference increasingly viable as models become smaller [^src1].

---

## Where It Is Showing Up

Three hardware vendors are cited as active players [^src1]:

- **Apple** — local AI models on iPhones and Macs (Apple Intelligence).
- **Qualcomm** — on-device AI chipsets for mobile and IoT.
- **NVIDIA** — edge AI hardware for industrial and automotive use.

---

## Hybrid Architectures

The source projects that many AI systems will run in hybrid configurations — partly in the cloud, partly on the device — rather than pure cloud or pure edge [^src1].

---

## Relation to corpus pages

- [Quantization](/ai-engineering/quantization.md) — the model-compression technique edge deployment depends on to fit models on-device
- [RunLocal](/ai-engineering/runlocal.md) · [LocalAI](/ai-engineering/localai.md) — tooling that runs models locally rather than in the cloud
- [Local AI Agents](/ai-engineering/local-ai-agents.md) — agents built on the on-device execution this source argues for
- ["7 AI Terms You'll Hear a Lot This Year" (Alex Wang)](/ai-engineering/seven-ai-terms-2026-alex-wang.md) — shared-provenance synthesis: this page and four siblings all derive from that single article, so they do not corroborate each other
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [Edge AI — Running AI On Device](../../../raw/notes/notes-03-resources-articles-edge-ai-running-ai-on-device.md)
