---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-a-field-guide-to-rapidly-improving-ai-products-hamels-blog-h.md
    channel: web
    ingested_at: 2026-06-26
aliases:
  - error analysis
  - AI error analysis
  - bottom-up error analysis
  - data viewer
  - data annotation tool
  - failure mode analysis
  - looking at your data
tags:
  - corpus/ai-engineering
  - concept
created: 2026-06-26
updated: 2026-06-26
---

# Error Analysis

**TL;DR**: Error analysis — systematically reading real AI outputs, annotating failures in open-ended notes, then letting a failure-mode taxonomy *emerge* from the data — is, per Hamel Husain, "the single most valuable activity in AI development and consistently the highest-ROI activity" [^src1]. It is the front end of the [evaluation](/ai-engineering/agent-evaluation.md) loop: it tells you *what* to measure before you build evals to measure it. Its enabling investment is a simple, custom **data viewer**; teams that have one "iterate 10× faster than those without them" [^src1].

## The mistake it fixes: the "tools trap"

The most common mistake in AI development is the "tools first" mindset — teams get "caught up in architecture diagrams, frameworks, and dashboards while neglecting the process of actually understanding what's working and what isn't" [^src1]. Generic metrics are "worse than useless" because they (1) create a false sense of progress (a team celebrates a +10% "helpfulness score" while users still can't finish basic tasks) and (2) fragment attention — "when everything is important, nothing is" [^src1]. The corrective is not a better metric; it is *looking at your data*.

## Bottom-up vs top-down

When identifying error types you can work in two directions [^src1]:

| Approach | Method | Weakness |
|---|---|---|
| **Top-down** | Start from common metrics ("hallucination", "toxicity") + a few task-specific ones | Convenient, but "often misses domain-specific issues" |
| **Bottom-up** (preferred) | Look at actual data first; let metrics *emerge* | More work, but surfaces the failures that actually matter |

The bottom-up process [^src1]:
1. One row per conversation/interaction in a spreadsheet (or viewer).
2. Write **open-ended notes** on any undesired behavior — no fixed schema.
3. Use an LLM to cluster the notes into a **taxonomy** of common failure modes.
4. Map each row to failure-mode labels and **count frequencies**.

**Worked example (NurtureBoss)**: annotating dozens of apartment-leasing conversations, three issues accounted for **over 60% of all problems** — conversation-flow issues, human-handoff failures, and rescheduling/date-handling [^src1]. Targeting just the date-handling failures (the AI failed 66% of the time on "two weeks from now") moved success from **33% → 95%** [^src1]. Categorizing failures and building specific tests beat reaching for new tools.

## The data viewer — the most important AI investment

"The single most impactful investment I've seen AI teams make isn't a fancy evaluation dashboard — it's building a customized interface that lets anyone examine what their AI is actually doing" [^src1]. *Customized* matters: every domain has unique context (chat history + scheduling for leasing; property details + source docs for real estate) that off-the-shelf labeling tools rarely surface, and friction — clicking between systems, copying notes into separate sheets — "actively discourages the kind of systematic analysis that catches subtle issues" [^src1].

What makes a good annotation tool [^src1]:
- **Show all context in one place** — don't make users hunt across systems.
- **Make feedback trivial** — one-click correct/incorrect beats long forms.
- **Capture open-ended feedback** — for issues that don't fit a predefined taxonomy.
- **Quick filtering/sorting** — dive into specific error types (e.g. by channel: voice/text/chat).
- **Hotkeys** — navigate and annotate without clicking.

These viewers "can be built in hours using AI-assisted development (like [Cursor](/ai-engineering/cursor.md) or Loveable)" [^src1]. Hamel's own stack is FastHTML + MonsterUI (back-end and front-end in one Python file); but "a spreadsheet is better than nothing" — the point is to start [^src1].

## Domain experts should write the prompts

"The people best positioned to improve your AI system are often the ones who know the least about AI" [^src1]. Because "prompts are just English," the friction of a domain expert (learning designer, lawyer, doctor) explaining principles in slides → engineers translating to prompts is wasted; the most effective teams give experts tools to write and iterate on prompts directly [^src1].

- **Build bridges, not gatekeepers** — playgrounds (Arize, [LangSmith](/ai-engineering/langsmith.md), Braintrust) are a start, but the next step many miss is **integrated prompt environments**: an admin version of the real UI that exposes prompt editing within the app's actual RAG/agent/business-logic context [^src1].
- **Kill the jargon** — calling everything "an agent" makes domain experts feel they can't contribute. Translate: "we're implementing RAG" → "we're making sure the model has the right context to answer"; "prevent prompt injection" → "make sure users can't trick the AI into ignoring our rules." Not dumbing down — being precise about what you're actually doing [^src1].

## Where it sits

Error analysis is the *discovery* phase that feeds the rest of the evaluation discipline: the failure modes it surfaces become the [eval](/ai-engineering/agent-evaluation.md) criteria and golden-dataset labels; [synthetic data](/ai-engineering/synthetic-data.md) generates inputs to exercise the failure modes you can't yet observe; and the experiment-based [roadmap](/ai-engineering/ai-product-management.md) prioritizes fixes by frequency. It is the antidote to the [over-trust](/ai-engineering/generator-evaluator-separation.md) failure mode — you can't grade what you haven't looked at.

## See also

- [Agent Evaluation](/ai-engineering/agent-evaluation.md) — error analysis defines what the evals measure
- [Synthetic Data](/ai-engineering/synthetic-data.md) — bootstraps data to analyze when you have no users
- [AI Product Management](/ai-engineering/ai-product-management.md) — experiment-based roadmaps built on this loop
- [Source: Hamel Husain's field guide](/ai-engineering/sources/field-guide-improving-ai-products.md)
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [A Field Guide to Rapidly Improving AI Products](../../raw/web/web-a-field-guide-to-rapidly-improving-ai-products-hamels-blog-h.md) — Hamel Husain, hamel.dev
