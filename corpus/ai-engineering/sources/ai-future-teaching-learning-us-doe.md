---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-artificial-intelligence-and-the-future-for-teachin-part-01.md
    channel: inbox
    ingested_at: 2026-07-15
  - path: raw/_inbox/pdf-artificial-intelligence-and-the-future-for-teachin-part-02.md
    channel: inbox
    ingested_at: 2026-07-15
  - path: raw/_inbox/pdf-artificial-intelligence-and-the-future-for-teachin-part-03.md
    channel: inbox
    ingested_at: 2026-07-15
  - path: raw/_inbox/pdf-artificial-intelligence-and-the-future-for-teachin-part-04.md
    channel: inbox
    ingested_at: 2026-07-15
aliases:
  - US DoE AI Report 2023
  - Department of Education AI Teaching Learning
  - AI Future Teaching Learning
tags:
  - corpus/ai-engineering
  - source
created: 2026-07-15
updated: 2026-07-15
---

# Artificial Intelligence and the Future of Teaching and Learning (US DoE, May 2023)

**Source:** U.S. Department of Education, Office of Educational Technology  
**Date:** May 2023  
**Length:** 71 pages  
**Format:** PDF policy report (4 parts ingested)

---

## Overview

A policy and research report from the U.S. Department of Education examining how AI should be integrated into K-12 and higher education. The report covers AI fundamentals, learning applications (primarily Intelligent Tutoring Systems), teaching support tools, formative assessment, and an R&D agenda — then closes with seven binding policy recommendations [^src4].

The report is unusual among AI policy documents in that it: (1) defines AI explicitly and resists hype, (2) takes equity and algorithmic bias as foundational (not afterthoughts), and (3) issues a clear, non-negotiable principle: humans must remain in the loop for all consequential educational decisions [^src1].

---

## Structure

| Part | Content |
|---|---|
| Part 1 | Introduction · Why address AI now · Policy framework · Ethical/equity principles · What is AI · Learning (intro) |
| Part 2 | Adaptive learning · ITS deep-dive · Teaching frameworks (ACE, IEO) · Educator preparation |
| Part 3 | Formative assessment · AES · R&D agenda · Context-sensitivity recommendations |
| Part 4 | Seven policy recommendations · Calls to action |

---

## Key Definitions

**AI (DoE definition):** "automation based on associations" — pattern-matching systems, not reasoning agents [^src1].

Three perspectives on AI in the report:
- Human-like reasoning simulation
- Goal-pursuing optimization
- Intelligence Augmentation (IA) — the preferred framing [^src1]

---

## Core Arguments

### 1. AI models are approximations, not truth

"AI models learn from historical data and therefore inherit whatever biases exist in that data" [^src1]. This is not a fringe concern — it is the mechanism by which any AI system works. Educational AI deployed without bias auditing will replicate existing inequities in student outcomes.

### 2. Adaptive learning via ITS is effective but narrow

Intelligent Tutoring Systems (ITS) are the most evidence-backed AI application in education. They build student knowledge models and adapt instruction in real time [^src2]. However, they optimize for the objective they are given — which is typically narrower than what educators mean by "learning" (social, emotional, creative dimensions are out-of-scope) [^src2].

### 3. ACE — Always Center Educators

Teachers must remain the instructional decision-maker. AI reduces administrative overhead and surfaces data, but cannot replace professional judgment about individual students [^src2]. The ACE principle rejects any framing where AI "teaches" independently.

### 4. IEO — Inspectable, Explainable, Overridable

Every AI tool in teaching must satisfy all three: educators can see what data it uses, understand why it made a recommendation, and reject or modify that recommendation. Black-box tools fail this standard and should not be deployed in classrooms [^src2].

### 5. AES is a useful first-pass tool, not a final arbiter

Automated Essay Scoring can process volume and flag patterns, but cannot reliably detect meaning, argumentation quality, or creativity. Deployed as a sole or final grader, it is gameable and inequitable [^src3].

### 6. R&D must address context

Current AI R&D optimizes for average conditions. The "long tail" of learner variability (neurodiverse students, English learners, students with disabilities) falls outside training distributions and is systematically under-served [^src3]. The report calls for R&D that prioritizes context-sensitivity as a design target, not an afterthought.

### 7. Seven policy recommendations

See full treatment in [AI in Education](/ai-engineering/ai-education.md). Summary [^src4]:
1. Humans in the loop — mandatory
2. Align AI to educational goals, not proxy metrics
3. Ground design in learning science
4. Prioritize trust (transparency + explainability)
5. Involve educators as co-designers
6. Focus R&D on context and safety
7. Education-specific guardrails (generic AI governance is insufficient)

---

## What This Source Adds to the Corpus

This is the primary government policy document on AI in education as of mid-2023. It pre-dates the ChatGPT/LLM hype peak but addresses LLMs explicitly. Key contributions:

- Authoritative definition of AI for an education audience (not engineering-native)
- Evidence base for ITS effectiveness (anchored to peer-reviewed literature)
- Equity framing that treats algorithmic bias as structural, not incidental
- Policy language (IEO, ACE, humans-in-the-loop) that has influenced subsequent state/district edtech procurement guidelines

**Limitations / potential staleness:** Published May 2023 — before widespread classroom adoption of generative AI tools (ChatGPT, Claude for Education). The ITS and AES evidence base is robust; the generative-AI recommendations are necessarily forward-looking and may warrant re-evaluation against 2024–2026 deployment evidence.

---

## Pages Produced

- [AI in Education](/ai-engineering/ai-education.md) — concept page covering ITS, adaptive learning, formative assessment, AI policy, risks, human-in-the-loop

---

[^src1]: [AI and the Future of Teaching and Learning — Part 1 (US DoE, 2023)](../../../raw/pdf/pdf-artificial-intelligence-and-the-future-for-teachin-part-01.md)
[^src2]: [AI and the Future of Teaching and Learning — Part 2 (US DoE, 2023)](../../../raw/pdf/pdf-artificial-intelligence-and-the-future-for-teachin-part-02.md)
[^src3]: [AI and the Future of Teaching and Learning — Part 3 (US DoE, 2023)](../../../raw/pdf/pdf-artificial-intelligence-and-the-future-for-teachin-part-03.md)
[^src4]: [AI and the Future of Teaching and Learning — Part 4 (US DoE, 2023)](../../../raw/pdf/pdf-artificial-intelligence-and-the-future-for-teachin-part-04.md)
