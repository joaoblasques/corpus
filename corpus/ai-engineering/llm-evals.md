---
type: concept
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
aliases:
  - LLM evals
  - product evals
  - AI evals
  - evaluation methodology
  - critique shadowing
  - LLM-as-judge
  - benevolent dictator
  - criteria drift
  - eval-driven development
  - binary pass/fail evals
  - trace review
  - annotation tool
  - principal domain expert
  - eval anti-patterns
  - eval maturity
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-06
updated: 2026-07-06
confidence: 0.95
last_confirmed: 2026-07-06
---

# LLM Evals (Product Evaluation Methodology)

**TL;DR**: Product-specific LLM evals measure whether *your pipeline works on your task with your data* — not general model capability. Hamel Husain's methodology, developed across 50+ company engagements, distills to: look at your data first, use binary pass/fail judgments, involve a single principal domain expert ("benevolent dictator"), validate LLM judges against human labels, and treat error analysis as the highest-ROI activity. Off-the-shelf metrics create false confidence; application-specific evals require a bottom-up, data-first approach [^src1][^src2][^src3].

## Why evals matter: iteration speed = success

"Like software engineering, success with AI hinges on how fast you can iterate. You must have processes and tools for evaluating quality, debugging issues, and changing behavior" [^src1]. Teams that focus only on prompt/model changes — without an evaluation system — plateau quickly: fixing one failure causes others (whack-a-mole), prompts bloat without measurable progress, and there is "limited visibility into AI system effectiveness beyond vibe checks" [^src1].

An eval system creates a flywheel: systematic assessment → directed improvement → regression prevention → fine-tuning and data curation come nearly for free once the eval infrastructure exists [^src1].

## The three levels of evaluation

| Level | What | When | Cost |
|---|---|---|---|
| **1 — Unit Tests** | Code assertions (regex, schema, exact-match) | Every code change | Low — fast, deterministic |
| **2 — Human & Model Eval** | Trace review, LLM-as-judge | Cadenced (e.g. 2–4 weeks) or on significant changes | Medium |
| **3 — A/B Testing** | Randomized user exposure | After stable, proven product | High — requires production traffic |

Run Level 1 on every code change; Level 2 on a cadence; Level 3 only after significant confidence [^src1]. Pass rates are product decisions — 70% may indicate a more meaningful eval than 100% [^src1].

## Anti-patterns (what most teams do wrong)

Hamel's five recurring pitfalls, framed as "missing data science fundamentals" [^src4]:

1. **Generic metrics** — teams deploy "helpfulness", "coherence", "hallucination score" without looking at data. These metrics are useless for diagnosis because they don't reveal *what is actually broken*. Application-specific failures ("Calendar Scheduling Failure", "Failure to Escalate To Human") require application-specific metrics.

2. **Unverified judges** — asking an LLM to rate outputs on a scale without validating the judge against human labels. A judge is a classifier; treat it like one. Measure precision and recall, not raw agreement rate. "Verifying classifiers has become a lost art in modern AI" [^src4].

3. **Bad experimental design** — generating synthetic test data by prompting "give me 50 test queries" produces generic, unrepresentative data. Better: look at real production data first, define dimensions, generate examples along those dimensions.

4. **Bad data and labels** — delegating labeling to non-domain-experts. Domain experts must label the data because "it is impossible to know what you want unless you look at the data" — the *labeling process itself* surfaces criteria [^src4]. Per Shankar et al., "criteria drift": users need criteria to grade outputs, but grading outputs helps them define criteria.

5. **Automating too much** — LLMs can wire up plumbing and write boilerplate for evaluations, but cannot look at data *for* you. "You don't know what you want until you see the outputs" [^src4].

## Core methodological commitments

### Binary pass/fail over Likert scales

> "If your evaluations consist of a bunch of metrics that LLMs score on a 1-5 scale, you're doing it wrong." [^src2]

Why binary wins [^src2][^src3]:
- Forces annotators to make a decision rather than hiding uncertainty in middle values (3-vs-4 debates inject noise).
- Faster during error analysis.
- Immediately legible: "a 10% increase in passing outputs is meaningful"; a +0.2 on a 1-5 scale is not.
- Sub-component tracking preserves granularity: instead of a 1-5 "factual accuracy" score, track "4 out of 5 expected facts included" as separate binary checks.

**Start with binary to understand what 'bad' looks like. Numeric labels are advanced and usually not necessary** [^src3].

### The principal domain expert ("benevolent dictator")

For most small-to-medium teams, one internal domain expert as the final decision-maker outperforms committees [^src2][^src3]:
- A psychologist for a mental health chatbot; a lawyer for legal AI; a customer service director for support automation.
- Eliminates annotation conflicts; prevents paralysis from "too many cooks."
- Captures tacit knowledge that cannot be encoded in a rubric.
- Creates ownership — the expert is more likely to accept the AI if they shaped its criteria.

"If you feel like you need five subject matter experts to judge a single interaction, it's a sign your product scope might be too broad" [^src3].

**When to use multiple annotators**: larger orgs or multi-domain products. Measure inter-annotator agreement with Cohen's Kappa; facilitate alignment sessions to reduce disagreement.

### Trace review as the core activity

A **trace** is the complete record of all actions, messages, tool calls, and data retrievals from a single initial user query through to the final response [^src3]. Looking at traces — not dashboards — is the primary diagnostic act.

Minimum viable eval setup: "spend 30 minutes manually reviewing 20-50 LLM outputs whenever you make significant changes" [^src3]. Use a notebook or a custom annotation interface. Remove all friction.

Trace sampling strategies (beyond random) [^src3]:
- **Outlier detection** — sort by response length, latency, tool-call count; review extremes.
- **User feedback signals** — prioritize traces with negative feedback or escalations.
- **Metric-based sorting** — generic metrics as *exploration signals* (not quality measures): review both high and low scores to find interesting traces.
- **Stratified sampling** — sample from each user-type/feature/query-category group.
- **Embedding clustering** — cluster queries, sample proportionally (oversample small clusters for edge cases).

## Critique Shadowing — building an LLM-as-judge

The methodology for building an aligned LLM judge [^src2]:

**Step 1: Find the principal domain expert.** This person sets the standard, captures unspoken expectations, and ensures consistency (see §above).

**Step 2: Build a diverse dataset.** Define dimensions meaningful for your use case (features, scenarios, personas for B2C). Generate realistic coverage with a mix of real and synthetic data. Ground synthetic data in real logs or traces.

**Step 3: Domain expert makes pass/fail judgments with written critiques.** The expert answers one question: "Did the AI achieve the desired outcome?" Plus a written critique explaining the reasoning. Critiques:
- Capture nuance the binary label loses.
- Serve as few-shot examples in the judge prompt.
- Force articulation of implicit criteria — "seeing how the LLM breaks down its reasoning made me realize I wasn't being consistent about how I judged certain edge cases" (Phillip Carter, Honeycomb) [^src2].

**Step 4: Fix obvious errors first.** Don't build an LLM judge for issues you can fix with a prompt change. Stabilize the system, then instrument it.

**Step 5: Build the LLM judge iteratively.** Start with a prompt using the expert's criteria + few-shot critique examples. Iterate against the expert's labels. Measure convergence (TPR/TNR on a held-out set). With Honeycomb, three iterations reached >90% agreement [^src2]. Raw agreement is misleading when classes are imbalanced — use precision/recall separately.

**Step 6: Perform error analysis.** Segment error rates by dimension (persona × feature × scenario). Classify trace errors by root cause. Prioritize fixes by frequency.

**Step 7: Create specialized judges as needed.** Only after the critique-shadowing process reveals persistent failure modes that warrant targeted investment.

> "The real value of this process is looking at your data and doing careful analysis. Creating a LLM judge is a hack I use to trick people into carefully looking at their data." [^src2]

## Evaluator tool selection

Key selection criteria (from a live panel of LangSmith, Braintrust, Arize Phoenix reviewing the same homework) [^src6]:

1. **Workflow and developer experience** — reduce friction between observing a failure and iterating on a solution. A notebook-centric workflow gives transparency and control.
2. **Human-in-the-loop support** — the tool should empower human review, not automate it away. First-class manual annotation and error analysis is non-negotiable.
3. **Transparency and control vs. "magic"** — be deeply skeptical of features that promise full automation without human validation (e.g. an AI agent that both creates a rubric and immediately scores outputs — "stacking of abstractions").
4. **Ecosystem integration** — avoid proprietary DSLs; ensure bulk data export in common formats.

Hamel's own workflow: use these tools as a backend data store, then use Jupyter notebooks and custom annotation interfaces for actual analysis [^src6].

**Specific tool notes** [^src6]:
- **LangSmith** — smooth trace-to-playground transition; intuitive for new teams; can nudge toward over-automation.
- **Braintrust** — clean UI; strong human-in-the-loop support; "Loop" AI-scorer (auto-rubric creation) is the main concern.
- **Arize Phoenix** — notebook-centric, open-source, local-first, "hackable"; limited aggregate visualization.

## Synthetic data for evals

The structured approach [^src3]:

1. **Define dimensions** — categories that describe different aspects of user queries (dietary restrictions × cuisine type × query complexity for a recipe app).
2. **Create tuples manually first** — write 20 combinations by hand to understand the problem space.
3. **Scale with two-step generation** — first generate structured tuples (LLM), then convert tuples to natural language (separate prompt). Separation avoids repetitive phrasing.
4. **Filter with error analysis** — don't generate synthetic data for issues you can fix immediately. Fix the prompt first.

**When synthetic data fails** [^src3]: complex domain-specific content (legal filings, medical records), low-resource languages, high-stakes domains where edge cases are hard to validate, underrepresented user groups.

## CI/CD vs. production monitoring

| | CI/CD evals | Production monitoring |
|---|---|---|
| Data | Small purpose-built datasets (100+ examples): core features, regression tests, known edge cases | Live traces sampled asynchronously |
| Evaluators | Assertions, deterministic checks (fast, cheap) | LLM-as-judge (reference-free, async) |
| Signal | Regression prevention | New failure mode discovery |
| Integration | Bidirectional — production patterns feed CI dataset | |

When production monitoring reveals new failure patterns, add representative examples to the CI dataset [^src3].

## Guardrails vs. evaluators

| | Guardrails | Evaluators |
|---|---|---|
| When | Inline, synchronous, in the request path | Asynchronous, after response is produced |
| Speed | Fast, deterministic (ms latency budget) | Heavier computation tolerated |
| Targets | Objective, high-impact failures (PII leaks, SQL injection, malformed JSON) | Subjective/nuanced quality (factual correctness, completeness, tone) |
| False positive cost | Very high — blocks valid responses | Lower — only affects dashboards/loops |

"Do not use LLM guardrails off the shelf blindly. Always look at the prompt." [^src3]

## Evals skills for coding agents

OpenAI's Harness Engineering demonstrates the pattern: three engineers, five months, ~1M lines of code built with Codex agents — and "improving the infrastructure around the agent mattered more than improving the model" [^src5]. Documentation tells the agent what to do; telemetry tells it whether it worked; evals tell it whether the output is good.

Skills/tools that fill eval gaps in coding agent workflows [^src5]:

| Skill | What it does |
|---|---|
| `error-analysis` | Read traces, categorize failures, build failure vocabulary |
| `generate-synthetic-data` | Create diverse test inputs when real data is sparse |
| `write-judge-prompt` | Design binary Pass/Fail LLM-as-judge evaluators |
| `validate-evaluator` | Calibrate judges against human labels using TPR/TNR and bias correction |
| `evaluate-rag` | Evaluate retrieval and generation quality separately |
| `build-review-interface` | Generate annotation interfaces for human trace review |
| `eval-audit` | Inspect an existing eval pipeline across six diagnostic areas; produces prioritized action list |

All major eval vendors (Braintrust, LangSmith, Phoenix) now ship MCP servers — agents can query traces directly. But access without methodology is not sufficient; these skills provide the "what to do with it" [^src5].

## The data science framing

Error analysis IS data science [^src4]:

| Classic data science concept | Eval equivalent |
|---|---|
| Exploratory Data Analysis | Reading traces, categorizing failures |
| Model Evaluation | Validating LLM judge against human labels |
| Experimental Design | Building representative test sets from production data |
| Data Collection | Getting domain experts to label outputs |
| Production ML | Monitoring whether the product works in production |

"Training models was never most of the job. The bulk of the work is setting up experiments to test how well the AI generalizes to unseen data, debugging stochastic systems, and designing good metrics." [^src4]

## See also

- [Agent Evaluation](/ai-engineering/agent-evaluation.md) — the broader evaluation concept page (online/offline modes, golden datasets, benchmarks)
- [Error Analysis](/ai-engineering/error-analysis.md) — the data-viewer / bottom-up methodology
- [Hamel Husain](/ai-engineering/hamel-husain.md) — practitioner who developed this methodology
- [LangSmith](/ai-engineering/langsmith.md) — primary eval platform
- [Synthetic Data](/ai-engineering/synthetic-data.md) — dimension-based synthetic data generation
- [Generator–Evaluator Separation](/ai-engineering/generator-evaluator-separation.md) — why judges must be separate from generators

---

[^src1]: [Your AI Product Needs Evals](../../raw/_inbox/web-your-ai-product-needs-evals-2b2dee98.md) — Hamel Husain, hamel.dev
[^src2]: [Using LLM-as-a-Judge For Evaluation: A Complete Guide](../../raw/_inbox/web-using-llm-as-a-judge-for-evaluation-a-complete-guide-9693f495.md) — Hamel Husain, hamel.dev
[^src3]: [LLM Evals: Everything You Need to Know](../../raw/_inbox/web-llm-evals-everything-you-need-to-know-hamels-blog-hamel-husa-5bf201ee.md) — Hamel Husain & Shreya Shankar, hamel.dev
[^src4]: [The Revenge of the Data Scientist](../../raw/_inbox/web-the-revenge-of-the-data-scientist-hamels-blog-hamel-husain-28a4d4c3.md) — Hamel Husain, hamel.dev
[^src5]: [Evals Skills for Coding Agents](../../raw/_inbox/web-evals-skills-for-coding-agents-hamels-blog-hamel-husain-f8a26550.md) — Hamel Husain, hamel.dev
[^src6]: [Selecting The Right AI Evals Tool](../../raw/_inbox/web-selecting-the-right-ai-evals-tool-hamels-blog-hamel-husain-daa87ecb.md) — Hamel Husain, hamel.dev
