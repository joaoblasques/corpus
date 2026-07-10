---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-a-field-guide-to-rapidly-improving-ai-products-hamels-blog-h.md
    channel: web
    ingested_at: 2026-06-26
aliases:
  - A Field Guide to Rapidly Improving AI Products
  - Hamel Husain field guide
  - rapidly improving AI products
  - field guide AI products
tags:
  - corpus/ai-engineering
  - source
created: 2026-06-26
updated: 2026-06-26
---

# A Field Guide to Rapidly Improving AI Products (Hamel Husain)

**TL;DR**: After helping 30+ companies build AI products, Hamel Husain finds the teams that succeed "barely talk about tools at all" — instead they "obsess over measurement and iteration" [^src1]. The field guide distills six process patterns that beat tool/framework selection: (1) start with [error analysis](/ai-engineering/error-analysis.md), not architecture; (2) build a simple custom data viewer; (3) let domain experts write prompts directly; (4) bootstrap with synthetic data even at zero users; (5) maintain trust in [evals](/ai-engineering/agent-evaluation.md) against criteria drift; (6) make the [roadmap](/ai-engineering/ai-product-management.md) count experiments, not features.

## Why this source matters

It is a practitioner consensus document on the *non-glamorous* half of AI engineering — the measurement and iteration discipline that determines whether an AI product improves. The opening scene is the thesis: a tech lead proudly describes "RAG here, a router there, this new framework," and Hamel pauses him to ask "can you show me how you're measuring if any of this actually works?" — a question teams routinely can't answer after weeks of building [^src1].

## The six patterns (and where each lands in the corpus)

| # | Pattern | Corpus page |
|---|---|---|
| 1 | **Error analysis** is the single highest-ROI activity; bottom-up beats top-down | [Error Analysis](/ai-engineering/error-analysis.md) |
| 2 | **A simple custom data viewer** is the most important AI investment (teams with one iterate 10× faster) | [Error Analysis](/ai-engineering/error-analysis.md) §Data viewer |
| 3 | **Empower domain experts** to write/iterate prompts directly ("prompts are just English") | [Error Analysis](/ai-engineering/error-analysis.md) §Domain experts |
| 4 | **Synthetic data** bootstraps evaluation with zero users | [Synthetic Data](/ai-engineering/synthetic-data.md) §For evaluation |
| 5 | **Maintain trust in evals** — binary + critique, criteria drift, human↔LLM alignment | [Agent Evaluation](/ai-engineering/agent-evaluation.md) |
| 6 | **Count experiments, not features** — capability funnel, timeboxes | [AI Product Management](/ai-engineering/ai-product-management.md) |

## Notable claims and worked examples

- **NurtureBoss date-handling fix**: bottom-up error analysis on a spreadsheet of annotated conversations found the AI failed 66% of the time on relative dates ("two weeks from now"); building targeted tests took the success rate from 33% → 95% [^src1].
- **Generic metrics are "worse than useless"** — they create a false sense of progress (teams celebrate a +10% "helpfulness score" while users still can't complete basic tasks) and fragment attention across dimensions [^src1].
- **The "tools trap"**: the belief that adopting the right framework/tool will solve AI problems; the alternative is looking at actual data [^src1].
- **Criteria drift** (Shankar et al., *Who Validates the Validators?*): "the process of grading outputs helps [people] define that very criteria" — so eval criteria can't be fully fixed before judging real outputs [^src1].
- **GitHub Copilot eval infrastructure**: the team built offline evals that cloned repos at scale and ran their existing unit-test suites as automated correctness checks, enabling thousands of experiments — "this wasn't wasted time, it was the foundation that accelerated everything" [^src1].
- **Capability funnel** (Bryan Bischof, ex-Head of AI at Hex): break AI performance into progressive utility levels (responds at all → valid output → relevant → matches intent → solves the job) so you can show progress before the final goal [^src1].
- **Eugene Yan's timeboxes**: 2 weeks data feasibility → 1 month technical feasibility → 6 weeks prototype/A-B; "at any step, if it doesn't work out, we pivot" — reassures leadership while preserving room to learn [^src1].

## See also

- [Error Analysis](/ai-engineering/error-analysis.md) — the central pattern, given its own page
- [Agent Evaluation](/ai-engineering/agent-evaluation.md) — eval-trust, criteria drift, binary+critique
- [Synthetic Data](/ai-engineering/synthetic-data.md) — bootstrapping evals without users
- [AI Product Management](/ai-engineering/ai-product-management.md) — experiment-based roadmaps
- [Generator–Evaluator Separation](/ai-engineering/generator-evaluator-separation.md) — the over-trust-in-self-grading failure mode this guide warns about

---

[^src1]: [A Field Guide to Rapidly Improving AI Products](../../../raw/web/web-a-field-guide-to-rapidly-improving-ai-products-hamels-blog-h.md) — Hamel Husain, hamel.dev
