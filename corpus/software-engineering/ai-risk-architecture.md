---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/web/ai-risk-is-an-architecture-problem.md
    channel: web
    ingested_at: 2026-06-12
aliases:
  - AI risk
  - AI risk architecture
  - data output action
  - lethal trifecta
  - mechanism risk
tags:
  - corpus/software-engineering
  - concept
created: 2026-06-12
updated: 2026-06-12
---

# AI Risk Architecture

**TL;DR**: The business risk of an AI system is "a property of the system, not just the components" [^src1]. Two products using the same model with the same error rate can have wildly different risk profiles depending on what the AI is allowed to see, what its output flows into, and what it can do. The right question is not "how do we make the model more trustworthy?" but "how do we build a system that's safe enough even when the model isn't?" [^src1].

## Two layers of risk

Companies conflate two vocabularies, which stalls AI-risk conversations [^src1]:

- **Mechanism risks** (what engineers see) — how a component can fail.
- **Business risks** (what executives see) — brand, compliance, liability, operational, commercial harm.

The executive's vocabulary doesn't tell the engineer what to fix; the engineer's doesn't tell the executive what to worry about — so conversations stall on definitions or jump to vague calls for "guardrails" [^src1].

## The three mechanism risks: data, output, action

Every AI integration can fail in three ways — through **what it sees, what it says, and what it does** [^src1]:

| Mechanism | What it is | Example failure |
|---|---|---|
| **Data** | Exposure of information that shouldn't have been exposed (exfiltration or cross-tenant contamination) | A PO PDF with an SSN sent to a third-party model, crossing a boundary into infrastructure governed by *their* terms of service [^src1] |
| **Output** | Wrong/misleading assertions; "structurally-valid output whose contents do not match reality" | Model misreads "$1,250" as "$12,500" — valid JSON, correct schema, wrong number [^src1] |
| **Action** | Unintended consequences the AI causes in the world (sends email, spends money, deploys) | The misread number triggers an automated wire transfer that already happened [^src1] |

The defining feature of action risk: consequences are "usually irreversible, or expensive to reverse" [^src1]. This is the fastest-growing category as agentic systems add tools. Simon Willison's **lethal trifecta** is the canonical case where all three coexist: private data in context, influenced by untrusted content, with the ability to exfiltrate or act [^src1].

## Risk is a property of the system, not the component

The same OCR misread is an accounting headache if a human catches it, or an operational disaster if it triggers an automatic payment. "The error didn't change. The system components between the error and the world did." [^src1] Adding broad action capabilities magnifies the business impact of output errors — the core reason agentic systems demand different architectural caution than non-agentic ones [^src1].

Most AI-risk energy goes to component-level optimizations (model choice, prompting, fine-tuning, output guardrails). These "help, on the margin, but none of it is the dominant factor" [^src1]. The dominant factors are architectural: what the AI may see, what its output flows into, and what it may do unchecked [^src1].

## The mitigation pattern: probabilistic component + deterministic check

The worked example pairs an LLM extraction step with a **deterministic lookup** against a known supplier/product database before any database write; mismatches beyond tolerance are routed to a human, the rest proceed automatically [^src1].

> "A probabilistic component (the model) is paired with a deterministic check ... and harm is now only possible when both fail." [^src1]

This also fixes reviewer fatigue: humans only see records that already failed the deterministic check — "a much smaller and much more interesting set" — so the same effort catches far more errors [^src1]. No new model, vendor, or prompt was needed. The architectural toolkit: bounded capabilities, verification steps, reversibility, human checkpoints at the right places, and closed tool sets instead of arbitrary access [^src1].

## Where it fits relative to formal frameworks

The data/output/action lens is a translation layer, not a replacement, for [^src1]:

- **NIST AI RMF** — governance meta-framework (Govern, Map, Measure, Manage); tells a Chief Risk Officer how to organize a program, not an architect what to look at first.
- **EU AI Act** — compliance scoping by use-case tier; two differently-built systems can land in the same tier.
- **OWASP Top 10 for LLM Applications / for Agentic AI** — the closest neighbor; the 2025 edition split "Misinformation" from "Excessive Agency," mapping directly onto output/action.
- **MIT AI Risk Repository** — comprehensive academic taxonomy, "almost completely unusable in a Tuesday meeting" [^src1].

## See also

- [AI-Assisted Development](/software-engineering/ai-assisted-development.md) — the same probabilistic-plus-deterministic discipline applied to code review and feedback loops
- [Distributed Systems Fallacies](/software-engineering/distributed-systems-fallacies.md) — adjacent "the failure mode lives in the system, not one component" reasoning
- [Software Engineering hub](/software-engineering/README.md)

---

[^src1]: [AI Risk Is an Architecture Problem](../../raw/web/ai-risk-is-an-architecture-problem.md)
