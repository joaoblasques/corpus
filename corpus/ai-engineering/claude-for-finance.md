---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/youtube-qLDwThdc3WQ-how-to-use-claude-for-finance-better-than-99-of-people.md
    channel: youtube
    ingested_at: 2026-06-26
aliases:
  - Claude for finance
  - Claude finance
  - FP&A with Claude
  - financial modeling with Claude
  - Claude Excel add-in finance
  - structured prompting for finance
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-26
updated: 2026-06-26
confidence: 0.7
last_confirmed: 2026-06-26
---

# Claude for Finance

**TL;DR**: An applied **structured-prompting workflow** for FP&A / financial modeling that turns "generic Claude outputs into high-level finance work" — moving "from unstructured prompts and fragile outputs to controlled, auditable and boardroom-ready financial workflows that hold up in the real FP&A world" [^src1]. The discipline is a **9-stage pipeline** run through the **Claude Excel add-in**, gated at each step, designed so that "every number you use later is verifiable" and no hidden assumption ever becomes a formula [^src1]. It is the finance-domain specialization of [[ai-engineering/prompt-engineering|prompt engineering]]: inventory-before-insight, plan-before-execute, and **model-selection-by-task-type**.

## Core principles

The workflow rests on a few cross-cutting disciplines [^src1]:

- **Inventory before insight.** "Most people upload a workbook and immediately request insights" — instead, force Claude to "do inventory before anything else," producing "a complete documented inventory of the workbook so that nothing remains implicit" [^src1]. The biggest modeling errors "come from inputs that were never properly examined or mislabeled," not from formulas [^src1].
- **Eliminate hidden assumptions at the source.** "Any assumptions must be eliminated before they become part of the projections" — structural validation up front so weaknesses surface "early," not "after the model has already been built… when fixing them is costly and your credibility is already on the line" [^src1].
- **Protected baseline.** "Establish a protected baseline by saving an untouched version of the workbook before ingestion begins" [^src1].
- **Plan-first, never execute silently.** Claude must "act like a senior FP&A lead, not like an operator" and produce an approved step-by-step work plan before any edits — "if Claude starts making fixes before you approve a plan, hidden assumptions quietly turn into formulas" [^src1]. This is the finance instance of the [[ai-engineering/prompt-engineering|plan-first prompting]] and [[ai-engineering/agentic-workflow|describe-what-not-how]] patterns.
- **Auditable / formula-driven outputs.** Three-statement models and the DCF must be "formula-driven and auditable" — "if the model is built with hard-coded numbers or hidden logic or missing links, everything downstream… becomes non-auditable" [^src1]. Every step carries explicit **acceptance checks** and a **"do not proceed if" gate** [^src1].
- **Verifiable inputs / traceability.** "You must be able to trace from source to output"; mismatches are "documented, not auto-fixed" via a mapping log [^src1].

## Model selection by task type

The workflow assigns models to task *kinds*, not uniformly — an applied case of matching model to job [^src1]:

| Task | Model | Rationale |
|---|---|---|
| Workbook ingestion / inventory | **Opus 4.5** | "Ingestion is a structural reasoning task" [^src1] |
| Persona calibration | **Opus 4.5** | "balances capability with stability, making it ideal for configuration" [^src1] |
| Plan-first work plan | **Opus 4.5** | "Planning is a reasoning task and you need stability before execution" [^src1] |
| Scope control / data filtering | **Opus 4.5** | structural-integrity reasoning [^src1] |
| Building the 3-statement model | **Opus 4.6** (Build Financial Models button) | formula construction [^src1] |
| DCF / valuation | **Opus 4.5** | auditable reasoning over the model [^src1] |
| CFO memo (executive comms) | **Sonnet 4.5** | drafting, not structural reasoning [^src1] |
| Contract-risk extraction | **Opus 4.5** | structured extraction from legal text [^src1] |

> [unsourced — note] The source predates the Opus 4.7/4.8 lineup (published 2026-03-12); the model names reflect what was current then. See [[ai-engineering/claude-models|Claude Model Lineup]] for the current family.

## The nine stages

1. **Source collection.** Build "a complete documented inventory of the workbook"; every sheet accounted for, every modeling-critical column present or flagged, missing data visible early. Save a protected baseline first [^src1].
2. **Persona configuration & calibration.** Lock Claude into "a repeatable, auditable CFO and FP&A analyst persona operating within Excel" — finance terminology, cited sheets/columns, step-by-step calculation logic, data-quality flags, trade-off-framed recommendations. Calibration only; no sheet edits yet [^src1].
3. **Plan-first prompting.** Produce "a prioritized, auditable plan, ideally between six and 12 steps" converting the workbook into "a driver-based three-statement model plus a DCF." Each step defines objective, sheets, inputs (precise columns/cells), outputs, acceptance checks, and a "do not proceed if" gate. The approved plan becomes a `stage_checklist` sheet — "your formal governance artifact" [^src1].
4. **Scope control & data filtering.** Restrict Claude to approved sheets to prevent hallucinated joins / mixed context; build `input_history` and "a transparent mapping log." All mismatches "documented, not auto-fixed" [^src1].
5. **Three-statement model (formula-driven).** Driver-based IS/BS/CF plus an audit sheet that verifies reconciliation; revenue split into price × volume where product data exists; Claude returns "a complete machine-readable list of added formulas." No hard-coded values in forecast cells; no circular references [^src1].
6. **Valuation (DCF).** Auditable DCF: FCF = CFO − CAPEX, discounted at WACC, Gordon-growth terminal value, enterprise/equity/per-share value; scenario toggle (base/upside/downside) and sensitivity matrices that link directly to the DCF output; top-5 value drivers ranked by NPV impact [^src1].
7. **Liquidity visibility.** A simple **13-week rolling cash forecast** driven by one input cell, with a line chart and a basic liquidity alert — "clarity, not complexity"; "executives don't just see risk, they see cash" [^src1].
8. **Presentation discipline.** A "one-page CFO memo under 400 words" with four labeled sections (key ask, options, drivers & sensitivity, recommendation), inline cell citations (e.g. `DCF!B28`), saved to a deliverables sheet; "Claude cannot invent or alter numbers" [^src1].
9. **Contract language → structured risk.** Extract payment terms, termination notice periods, covenant thresholds, and cash-flow impacts into a `contract_mapped` table with low/medium/high risk flags and model notes; 12-month liquidity/covenant impacts highlighted; source sheets untouched [^src1].

## Why it generalizes

The throughline — inventory the inputs before asking for insight, get a numbered plan approved before any execution, keep every output formula-traceable, and pick the model by the *type* of cognitive work — is domain-specific structured prompting: the same prompt-engineering levers ([[ai-engineering/prompt-engineering|clarity, plan-first, acceptance criteria, persona]]) hardened into a gated, auditable workflow for a high-stakes domain where "the wrong output" is the real cost [^src1].

## See also

- [[ai-engineering/prompt-engineering|Prompt Engineering]] — the general discipline this specializes (plan-first, personas, acceptance criteria, model-led elicitation)
- [[ai-engineering/claude-cowork|Claude Cowork]] — Claude in Excel/PowerPoint/Word/Outlook (the Microsoft 365 add-in surface)
- [[ai-engineering/claude-models|Claude Model Lineup]] — current Opus/Sonnet family; the source's model names predate the 4.7/4.8 lineup
- [[ai-engineering/agentic-workflow|Agentic Workflows]] — describe-what-not-how; gated multi-step orchestration
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [How to use Claude For Finance Better Than 99% of People (Luke Finance)](../../raw/youtube/youtube-qLDwThdc3WQ-how-to-use-claude-for-finance-better-than-99-of-people.md) — YouTube playlist: Claude Finance
