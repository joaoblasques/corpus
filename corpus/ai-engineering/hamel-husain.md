---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-your-ai-product-needs-evals-2b2dee98.md
    channel: web
    ingested_at: 2026-07-06
  - path: raw/_inbox/web-using-llm-as-a-judge-for-evaluation-a-complete-guide-9693f495.md
    channel: web
    ingested_at: 2026-07-06
  - path: raw/_inbox/web-llm-evals-everything-you-need-to-know-hamels-blog-hamel-husa-5bf201ee.md
    channel: web
    ingested_at: 2026-07-06
  - path: raw/_inbox/web-the-revenge-of-the-data-scientist-hamels-blog-hamel-husain-28a4d4c3.md
    channel: web
    ingested_at: 2026-07-06
  - path: raw/_inbox/web-evals-skills-for-coding-agents-hamels-blog-hamel-husain-f8a26550.md
    channel: web
    ingested_at: 2026-07-06
  - path: raw/_inbox/web-selecting-the-right-ai-evals-tool-hamels-blog-hamel-husain-daa87ecb.md
    channel: web
    ingested_at: 2026-07-06
  - path: raw/_inbox/web-fuck-you-show-me-the-prompt-ad95e5b5.md
    channel: web
    ingested_at: 2026-07-06
  - path: raw/_inbox/web-why-i-stopped-using-nbdev-hamels-blog-hamel-husain-1fae2588.md
    channel: web
    ingested_at: 2026-07-06
  - path: raw/_inbox/web-how-to-debug-axolotl-hamels-blog-hamel-husain-76be0ce3.md
    channel: web
    ingested_at: 2026-07-06
  - path: raw/web/web-a-field-guide-to-rapidly-improving-ai-products-hamels-blog-h.md
    channel: web
    ingested_at: 2026-06-26
aliases:
  - Hamel Husain
  - hamel.dev
  - Parlance Labs
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-06
updated: 2026-07-06
---

# Hamel Husain

**TL;DR**: Independent AI consultant and educator who has helped 50+ companies build domain-specific AI evaluation systems and taught 4,000+ engineers in AI Evals courses. Best known for the "Critique Shadowing" LLM-as-judge methodology, the field guide to rapidly improving AI products, and the evals-skills open-source plugin. Previously at GitHub (co-created CodeSearchNet, precursor to GitHub Copilot) and helped build nbdev at fast.ai.

## Background

- **GitHub** — led the team that created CodeSearchNet (2019), which became a precursor to GitHub Copilot. Worked with non-technical professionals (lawyers, accountants) on GitHub web tooling [^src1].
- **Fast.ai / nbdev** — joined the nbdev project in 2020, built fastpages (notebook blogging system), and helped lead a complete rewrite of nbdev in 2022. Eventually stopped using nbdev when AI coding tools changed the tradeoffs [^src8].
- **Parlance Labs** — independent consulting practice (hamel@parlance-labs.com); the organizational home for consulting work and the AI Evals course [^src1].
- **AI Evals course** — co-taught with Shreya Shankar; has trained 700+ engineers and PMs (as of early 2026); live cohort with hands-on exercises and office hours [^src3].

## Core methodology contributions

### Critique Shadowing

The end-to-end process for building an LLM-as-judge that is aligned with a principal domain expert [^src2]. Steps:

1. Find the principal domain expert ("benevolent dictator").
2. Build a diverse dataset of real/synthetic interactions.
3. Expert makes binary pass/fail judgments with written critiques.
4. Fix obvious errors in the underlying system.
5. Build an LLM judge iteratively using critiques as few-shot examples.
6. Perform error analysis on judge-scored interactions.
7. Create specialized judges for persistent failure modes.

The cited practical outcome with Honeycomb (Phillip Carter as domain expert): three iterations to reach >90% human-LLM agreement [^src2].

### Field Guide to Rapidly Improving AI Products

A practitioner guide covering [^src_fg]:
- Error analysis as the highest-ROI activity in AI development.
- The data viewer as the most important AI investment (10× iteration speed improvement).
- Domain experts writing prompts directly (prompts are just English).
- An experiment-based roadmap rather than a feature roadmap.
- Synthetic data grounded in real production traces.

### evals-skills (open-source plugin)

Published to help coding agents instrument evaluation pipelines correctly [^src5]. Includes skills for error analysis, synthetic data generation, judge-prompt writing, evaluator validation, RAG evaluation, annotation interface building, and an eval-audit skill that diagnoses existing pipelines across six areas. Repo: `github.com/hamelsmu/evals-skills`.

### "Fuck You, Show Me The Prompt"

Philosophy and tooling for prompt transparency [^src7]. Core argument: LLM abstractions that hide prompts add accidental complexity and prevent practitioners from making informed decisions. Recommended tool: `mitmproxy` as a framework-agnostic proxy to intercept any library's API calls to an LLM. Applied to guardrails, Guidance, LangChain SmartLLMChain, Instructor, and DSPy to reveal what each is actually sending to the model.

### "The Revenge of the Data Scientist"

Argument that LLM-era AI work is fundamentally data science [^src4]:
- The evaluation harness (the observability stack of logs, metrics, traces that bounds agent behavior) is data science work.
- Five eval pitfalls map directly to missing data science fundamentals: generic metrics → EDA; unverified judges → model evaluation; bad experimental design → experimental design; bad labels → data collection; over-automation → production ML.
- Evals = stochastic system debugging; measuring causality; designing good metrics — the classic data scientist skillset.

## Opinions and strong takes

- **Binary pass/fail over Likert scales**: "If your evaluations consist of a bunch of metrics that LLMs score on a 1-5 scale, you're doing it wrong." [^src2]
- **Don't outsource error analysis**: "Outsourcing error analysis is usually a big mistake. The core of evaluation is building product intuition that only comes from systematically analyzing your system's failures." [^src3]
- **Don't buy ready-made metrics**: "Generic evaluations waste time and create false confidence. All you get is you don't know what they actually do." [^src3]
- **Model selection is not the primary axis**: "I suggest not thinking of switching models as the main axis of how to improve your system off the bat without evidence. Does error analysis suggest that your model is the problem?" [^src3]
- **Eval-driven development generally doesn't work**: "Unlike traditional software where failure modes are predictable, LLMs have infinite surface area. You can't anticipate what will break. Write evaluators for errors you discover, not errors you imagine." [^src3]
- **Prompts are English**: "The people best positioned to improve your AI system are often the ones who know the least about AI." Domain experts should write and iterate on prompts directly [^src_fg].
- **The tool is not the solution**: On eval tools — "people focus too much on tools instead of the process, thinking the tool will be an off-the-shelf solution when it rarely is." Personally uses eval platforms as a backend data store, then notebooks and custom annotation tools for analysis [^src6].

## Tool preferences (as of 2026)

- **Development**: Amp, Cursor, Claude Code [^src8].
- **Languages**: shifted from "Python for everything" to task-appropriate stacks; TypeScript for web; notebooks only for data analysis and ML exploratory work [^src8].
- **Eval platforms**: LangSmith, Arize Phoenix, Braintrust — all used as data backends, not as primary interfaces [^src6].
- **Debugging LLMs**: mitmproxy for intercepting API calls; Axolotl for fine-tuning with VSCode debugging config [^src7][^src9].

## See also

- [LLM Evals](/ai-engineering/llm-evals.md) — the full methodology this practitioner developed
- [Agent Evaluation](/ai-engineering/agent-evaluation.md) — broader evaluation concept page
- [Error Analysis](/ai-engineering/error-analysis.md) — the data-first discovery phase
- [LangSmith](/ai-engineering/langsmith.md) — eval platform frequently referenced in his work
- [Prompt Engineering](/ai-engineering/prompt-engineering.md) — "Fuck You, Show Me The Prompt" on prompt transparency

---

[^src1]: [Your AI Product Needs Evals](../../raw/_inbox/web-your-ai-product-needs-evals-2b2dee98.md) — Hamel Husain, hamel.dev
[^src2]: [Using LLM-as-a-Judge For Evaluation: A Complete Guide](../../raw/_inbox/web-using-llm-as-a-judge-for-evaluation-a-complete-guide-9693f495.md) — Hamel Husain, hamel.dev
[^src3]: [LLM Evals: Everything You Need to Know](../../raw/_inbox/web-llm-evals-everything-you-need-to-know-hamels-blog-hamel-husa-5bf201ee.md) — Hamel Husain & Shreya Shankar, hamel.dev
[^src4]: [The Revenge of the Data Scientist](../../raw/_inbox/web-the-revenge-of-the-data-scientist-hamels-blog-hamel-husain-28a4d4c3.md) — Hamel Husain, hamel.dev
[^src5]: [Evals Skills for Coding Agents](../../raw/_inbox/web-evals-skills-for-coding-agents-hamels-blog-hamel-husain-f8a26550.md) — Hamel Husain, hamel.dev
[^src6]: [Selecting The Right AI Evals Tool](../../raw/_inbox/web-selecting-the-right-ai-evals-tool-hamels-blog-hamel-husain-daa87ecb.md) — Hamel Husain, hamel.dev
[^src7]: [Fuck You, Show Me The Prompt](../../raw/_inbox/web-fuck-you-show-me-the-prompt-ad95e5b5.md) — Hamel Husain, hamel.dev
[^src8]: [Why I Stopped Using nbdev](../../raw/_inbox/web-why-i-stopped-using-nbdev-hamels-blog-hamel-husain-1fae2588.md) — Hamel Husain, hamel.dev
[^src9]: [How To Debug Axolotl](../../raw/_inbox/web-how-to-debug-axolotl-hamels-blog-hamel-husain-76be0ce3.md) — Hamel Husain, hamel.dev
[^src_fg]: [A Field Guide to Rapidly Improving AI Products](../../raw/web/web-a-field-guide-to-rapidly-improving-ai-products-hamels-blog-h.md) — Hamel Husain, hamel.dev
