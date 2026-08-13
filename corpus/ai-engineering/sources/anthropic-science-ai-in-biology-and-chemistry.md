---
type: source
domain: ai-engineering
status: stub
sources:
  - path: raw/_inbox/web-paving-the-way-for-ai-agents-in-biology-e2470097.md
    channel: web
    ingested_at: 2026-08-13
  - path: raw/_inbox/web-making-claude-a-chemist-ff153605.md
    channel: web
    ingested_at: 2026-08-13
aliases:
  - Anthropic science biology agents
  - Anthropic science chemistry NMR
  - VirBench
  - gget virus
tags:
  - corpus/ai-engineering
  - source
  - anthropic
  - ai-for-science
  - biology-agents
  - chemistry
  - scientific-ai
created: 2026-08-13
updated: 2026-08-13
---

# Anthropic Science: AI Agents in Biology and Chemistry

TL;DR: Two Anthropic research posts on applying frontier AI to science. (1) Biology: biological data infrastructure is not agent-friendly; VirBench benchmark shows frontier models achieve 17–91% accuracy on NCBI Virus retrieval, but adding `gget virus` (a deterministic retrieval layer) raises accuracy to ~100% for all models. (2) Chemistry: Claude Opus 4.7 performs comparably to ChemDraw and MestReNova on NMR spectrum prediction and can uniquely do inverse structure elucidation from 1D NMR data.

## AI Agents in Biology: The Data Infrastructure Problem [^biology]

Authors: Laura Luebbert et al. (Ferdous Nasri, Sarah Gurev, Patrick Varilly, Krithik Ramesh, Nuala A. O'Leary, Jonah Cool, Bernhard Y. Renard, Pardis Sabeti, Laura Luebbert).

**Core argument**: using AI agents to navigate biological data is "like driving through an old city designed before cars — the infrastructure may be beautiful, but it's full of narrow, winding streets." The bottleneck for biological agents is not reasoning but the absence of widespread deterministic execution layers for querying biological data.

**Why coding agents advanced faster**: software provides structured digital workflows, reliable interfaces, testable outputs (a patch either passes the tests or it doesn't). Biology offers heterogeneous databases, idiosyncratic file formats, bespoke retrieval scripts, and few simple verifiable rewards.

**VirBench benchmark**: 120 realistic viral sequence queries across 40 pathogens with manually verified ground-truth counts. Tasks reflect real surveillance, diagnostic assay design, and protein model training-data workflows.

*Results without tools*: Claude Sonnet 4, Claude Opus 4.7, Biomni OSS, Edison Analysis, GPT-5.2-pro, GPT-5.5 achieved mean accuracies from **16.9% to 91.3%**. Even top models failed the effective bar of ~100% required for reliable dataset construction. The same model asked the same question three times often gave substantially different answers (e.g., Sonnet 4 returned 106, 15, and 5 sequences for the same Ebolavirus query; expected: 266).

*Consequences of errors*: Incomplete sequence retrieval shifted inferred TMRCA (time to most recent common ancestor) in a phylogenetic analysis of the 2014 Ebolavirus outbreak from January 2014 to April 2014, or pushed it to 1922 — changing conclusions about outbreak origin timing. Similar errors misrepresented antibody therapeutic epitope coverage.

**gget virus**: A deterministic retrieval tool built in collaboration with NCBI, coordinating across REST, Datasets, and E-utilities APIs to replicate the NCBI Virus web interface's filtering behavior programmatically — including filters that exist only in the browser UI but not in any single API. Handles batching for large result sets (SARS-CoV-2, Influenza A, HIV-1). Standardized, machine-readable outputs with detailed logs.

*Results with gget virus*: Accuracy rose above 90% for all agents, peaking at **99.7% for GPT-5.5**. Run-to-run variability was largely eliminated. Performance gap between models narrowed dramatically — "model choice [becomes] much less important."

**Broader lesson**: "We want models to be creative when they generate hypotheses, design experiments, or reason about mechanisms. But the layer underneath that creativity — gene identifiers, schemas, retrieval logic, coordinate systems, metadata conventions — has to be boringly reliable (deterministic)." Biological databases need to be designed with agents as first-class users.[^biology]

## Making Claude a Chemist: NMR Spectrum Analysis [^chemistry]

Author: David Kamber (Anthropic chemist), based on work with world-class synthetic, computational, and analytical chemists.

**Problem**: chemistry involves moving between multiple representations (drawn structures, instrument readouts, database query strings, patent notations). NMR spectroscopy is one of the most time-consuming steps in synthetic chemistry — every compound requires matching peaks to atoms in a proposed structure by hand.

**Assessment setup**: 20 compounds from ChemRxiv preprints (after model training cutoffs to avoid data leakage), across 4 structural families (5 compounds each), each representing a different category of NMR challenge. Compared: Claude Opus 4.7, Opus 4.6, Sonnet 4.6 vs. ChemDraw and MestReNova.

**Forward prediction results** (structure → predicted spectrum):
- Hydrogen: Opus 4.7 average error ±0.079 ppm (well under ±0.20 ppm tolerance). Highest share of peaks within tolerance.
- Carbon: Opus 4.7 (±1.37 ppm) and MestReNova (±1.48 ppm) effectively tied within ±1.0 ppm tolerance.
- Splitting patterns (peak shape): Opus 4.7 matched experimentally reported patterns more often than any other tool.
- Sub-peak spacing: all three Claude models predicted spacing within 0.5 Hz ~80% of the time vs. 26–35% for ChemDraw and MestReNova.

**Inverse prediction** (spectrum → structure elucidation — the harder task, unsupported by existing tools):
- 8 simpler targets (single-ring, two-fragment molecules): Opus 4.7 recovered all 8 on every attempt from spectra and formula alone.
- 7 harder targets (fused rings, spirocycles, with starting-material hint): correct structure on all 3 runs for 4/7; on 2/3 runs for the remaining 3.

**Significance**: "A general-purpose model without chemistry-specific fine-tuning is now as good as or better than ChemDraw and MestReNova on average" for routine NMR prediction. Claude uniquely handles 1D inverse elucidation (structure-from-spectrum) with no specialized setup or 2D NMR required — existing dedicated software requires 2D NMR, specialized training, and licenses.[^chemistry]

**Current limitations**: Assessment covers 20 compounds across 4 scaffold classes — needs broader validation (hundreds of compounds, 20–30 scaffold classes, 15/class). NH-active heteroaromatics tested only for chloropyridazines. Retrosynthesis planning is still being scoped.

## Cross-links

- [/ai-engineering/anthropic.md](/ai-engineering/anthropic.md) — Anthropic entity page
- [/ai-engineering/multimodal-models.md](/ai-engineering/multimodal-models.md) — multimodal reasoning capabilities

---

[^biology]: raw/_inbox/web-paving-the-way-for-ai-agents-in-biology-e2470097.md — anthropic.com/research/agents-in-biology
[^chemistry]: raw/_inbox/web-making-claude-a-chemist-ff153605.md — anthropic.com/research/making-claude-a-chemist
