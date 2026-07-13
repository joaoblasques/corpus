---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/LangSmith - Debugging and Evaluating AI Agents.md
    channel: notes
    ingested_at: 2026-05-21
  - path: raw/web/better-experiments-with-llm-evals-a-funnel-not-a-fork-spotif.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/what-data-agent-benchmarks-do-and-don-t-tell-us.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/monitoring-cortex-agent-performance-with-trace-data.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-06-11-fable-evals-performance-airbnbs-evolved-data-architecture-po.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/web/web-swe-bench-multilingual.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/web/web-task-completion-time-horizons-of-frontier-ai-models.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/web/web-claude-swe-bench-performance.md
    channel: web
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-this-karpathy-sys-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/web/web-a-field-guide-to-rapidly-improving-ai-products-hamels-blog-h.md
    channel: web
    ingested_at: 2026-06-26
  - path: raw/_inbox/web-swe-bench-pro-results-2026-ai-coding-model-rankings-dca3b106.md
    channel: web
    ingested_at: 2026-07-06
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
  - agent evaluation
  - LLM evaluation
  - LLM evals
  - agent benchmarking
  - online evaluation
  - offline evaluation
  - evaluation funnel
  - trace monitoring
  - SWE-bench Multilingual
  - multilingual coding benchmark
  - METR time horizons
  - time horizons
  - task-completion time horizon
  - 50%-time horizon
  - 80%-time horizon
  - critique shadowing
  - LLM-as-judge
  - benevolent dictator
  - principal domain expert
  - eval anti-patterns
  - evals skills
  - eval-audit
  - SWE-Bench Pro
  - SWE-Bench Pro 2026
  - Harbor benchmark tool
  - regression-style eval
  - model overlap analysis
  - Jaccard overlap
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-21
updated: 2026-07-06
last_confirmed: 2026-07-06
---

# Agent Evaluation

**TL;DR**: Measuring agent quality through two complementary loops — *online* (production monitoring) and *offline* (pre-deployment regression testing) — anchored to curated golden datasets [^src1].

## Two evaluation modes

| Mode | When | Mechanism |
|---|---|---|
| **Online** | Live production traffic | Sample-based eval of real traces; flags quality regressions before they degrade UX |
| **Offline** | Before deploying a change | Run agent against golden dataset; compare accuracy/latency/cost vs baseline |

Configure online evals with sampling rate (e.g., 10% for cost control) + filter condition + judge LLM + scoring schema [^src1].

## Evaluator types

| Type | Use case |
|---|---|
| **LLM-as-judge** | Subjective quality: helpfulness, relevance, faithfulness to source |
| **Custom code** | Deterministic checks: regex, format validation, schema compliance |
| **Thread evaluator** | Task completion across full multi-turn conversations |

LLM-as-judge requires a scoring schema and a judge model configured independently from the agent model [^src1].

## Golden datasets

"Golden examples" are the core of reliable agent development [^src1]. Properties:
- 50–100 curated `input → reference_output` pairs
- Seeded by hand-crafted examples; grown from production failures routed through annotation queues
- Treated as the regression suite — every experiment runs against it before shipping

```python
from langsmith import Client
client = Client(api_key="...")

results = client.evaluate(
    eval_config={"evaluators": ["accuracy", "faithfulness", {"type": "code_checker"}]},
    data_set_name="my_golden_dataset",
    llm_or_chain_factory=my_agent_function
)
```
[^src1]

## Key metrics

- **Task success rate** — did the agent complete the goal?
- **Tool call accuracy** — right tool, right arguments?
- **Retrieval quality** — for RAG components
- **Latency and cost per task**
- **Context window growth** — agents degrade as context fills across turns; thread-level evaluation captures this [^src1]

## Production feedback loop

Automations auto-route failing traces (low score, thumbs-down) to annotation queues. SMEs review and edit traces → export as golden examples → dataset grows. Production failures become training data [^src1].

## Accuracy vs cost/latency trade-off

More powerful model = better quality + higher cost. Measure both before choosing a model. Use a comparison dashboard to evaluate experiments side-by-side across accuracy, latency, cost, and token count [^src1].

## Evals as a funnel, not a fork

Evals and A/B experiments measure different things, so the right relationship is a **funnel** — evals come *before* the experiment, not instead of it [^src2]. The distinction [^src2]:

| | Evals (verification) | Experiments (validation) |
|---|---|---|
| Question | Does the output conform to quality standards? | Do real users respond as predicted? |
| Role | Discard non-promising candidates; raise experiment hit rate | Confirm the change drives the business outcome and bound risk |

At Spotify only ~12% of A/B tests ship a positive result, but ~64% produce valid learning, and ~42% of *launched* experiments are rolled back to prevent regressions in secondary (guardrail) metrics no eval flagged [^src2]. LLM judges add a **second calibration layer** on top of traditional quantitative metrics; both layers can drift and must be validated against online outcomes [^src2]. When eval scores and experiment outcomes diverge, "that's diagnostic gold" — it recalibrates the judge [^src2].

> "Without offline-online signal calibration, our evals are opinions, not evidence." [^src2]

A cautionary example of eval miscalibration: when Anthropic released Opus 4.5, Qodo's coding evals showed no improvement, yet the model had improved substantially on longer tasks that a controlled experiment would have surfaced [^src2]. Long-running tasks and long-term behavior are, by construction, hard to capture with evals [^src2].

## What benchmarks do and don't tell us

Benchmark progress on data agents: ontologies outperform text-to-SQL (Sequeda et al. 2023); semantic layers increase LLM query reliability; ADE-bench is the first to benchmark agents *building* data pipelines, not just answering questions [^src3]. On well-specified tasks where the answer is present, "models are good and getting better" [^src3]. But two real-world dimensions evade today's benchmarks [^src3]:

1. **Statefulness** — most benchmarks treat learning from a past mistake as cheating, but in the real world that is "being good at your job." A 90-day business simulation with tasks that build on each other measures whether an agent learns over time — closer to real deployment than disconnected tasks [^src3].
2. **Context** — sandboxed benchmarks underestimate agents that, in production, read across dbt projects, GitHub, Slack, Notion, Jira, email. "One big pile of context" (OBPOC) is too valuable to ignore despite governance concerns [^src3].

A flagged gap: organizational context and memory improve agent output, but there are "no great mechanisms for tracking them" [^src3]. **Token efficiency** is emerging as a first-class eval axis — delivering equivalent quality while minimizing token (and warehouse) spend [^src3].

**Domain-specific eval example**: the Fable 5 model required *new* evals because existing ones did not capture its strengths; it scored roughly 10–15% better than recent frontier models on Hex's evals, excelling at messy, long-horizon data tasks requiring judgment, clear assumptions, and cross-checking semantic models against raw data [^src5]. This reinforces the funnel point — when a model's gains are on long-horizon judgment, static evals miss them [^src2][^src5].

## Maintaining trust in evals (against criteria drift)

A recurring failure pattern: teams build eval systems, then "gradually lose faith in them" — metrics stop matching production, or the evals get too complex to interpret — and revert to gut feeling, defeating the purpose [^src10]. Front-loading [error analysis](/ai-engineering/error-analysis.md) tells you *what* to measure; the practices below keep the measurement trustworthy as it scales [^src10].

**Criteria drift.** Per Shankar et al. (*Who Validates the Validators?*), "the process of grading outputs helps [people] define that very criteria" — so you cannot fully fix eval criteria before judging real outputs [^src10]. Treat criteria as living documents that evolve with understanding, and reconcile contradictory stakeholder criteria rather than imposing one [^src10]. (Honeycomb's Phillip Carter: "Seeing how the LLM breaks down its reasoning made me realize I wasn't being consistent about how I judged certain edge cases.")

**Favor binary decisions over arbitrary scales** [^src10]. A 1–5 scale forces evaluators to agonize over 3-vs-4 boundary cases, injecting noise; a pass/fail forces a clear "did this output achieve its purpose?" and makes progress legible ("a 10% increase in passing outputs is immediately meaningful"). Even teams using 1–5 inevitably ask where "good enough" is — a binary decision in disguise.

**Pair binary judgments with detailed critiques** [^src10]. The nuance isn't lost — it moves into a written critique of *why* something passed/failed. Used as few-shot examples in judge prompts, these critiques yield "15–20% higher agreement rates between human and LLM evaluations" and seed high-quality [synthetic data](/ai-engineering/synthetic-data.md).

**Measure human↔LLM alignment, don't assume it** [^src10]. People "over-rely and over-trust AI systems" (e.g. the debunked MIT-EECS-GPT-4 pre-print where the model graded itself), and LLM judges can be swayed by option order or formatting. With Honeycomb it took **three iterations to reach >90% agreement** between the LLM-judge and human labels — alignment is "an ongoing conversation," not a one-time setup (cf. Eugene Yan's AlignEval). This is the [generator–evaluator separation](/ai-engineering/generator-evaluator-separation.md) principle applied to grading.

**Scale without losing trust** [^src10]: start with high human involvement → study where automated evals align vs diverge → use strategic sampling on the weakest-alignment cases → keep calibrating. The goal is to *direct* human effort to the most informative cases, not eliminate it.

## Evaluation infrastructure as the foundation

The key enabler of an experiment-based [roadmap](/ai-engineering/ai-product-management.md) is robust eval infrastructure — "without it, you're just guessing whether your experiments are working" [^src10]. In early GitHub Copilot development the team "invested heavily in building sophisticated offline evaluation infrastructure": systems that cloned repositories at scale, set up their environments, and ran each repo's **existing unit-test suites** as an automated way to verify completion correctness across many languages and frameworks [^src10]. That foundation let them run thousands of experiments and say "this change improved quality by X%" instead of debating — "this wasn't wasted time, it was the foundation that accelerated everything" [^src10]. This mirrors the SWE-bench philosophy above: binary outcomes tied to executable criteria beat rubric scoring.

## Trace-based production monitoring

Beyond golden-dataset evals, production agents are monitored via **trace data** — a hierarchy of spans per interaction [^src4]. Snowflake's Cortex Agents log span-level traces (`GET_AI_OBSERVABILITY_EVENTS`) mapping `record_name` to agent phases [^src4]:

| Span type | Captures |
|---|---|
| `chat` | Top-level conversation turn; full input/output + `thread_id` |
| `planning` | Tool selection, query formulation, per-step token count + model name |
| `response_generation` | Final answer synthesis cost |
| `tool_call` | Search query/filters/results, or generated SQL + `question_category` |

A monitoring **maturation curve**: moment-in-time snapshots → dashboards → anomaly detection on trends → incident management for SLAs [^src4]. The three baseline metrics where abnormal behavior shows up first [^src4]:

- **Total tokens** (per span, not per conversation) — a step-change up signals a persistent config change; gradual drift signals multi-turn context accumulation (a session can climb from 5k to 40k tokens by turn 10), the case for explicit [context window management](/ai-engineering/context-window-management.md) [^src4].
- **Duration** — correlates with tokens but can spike independently on extra tool calls or retries; watch P50/P90, not just the mean, since a stable mean hides a growing slow tail [^src4].
- **Status codes** (`STATUS_CODE_OK` vs `STATUS_CODE_ERROR`) per span — distinguishes planning vs tool-call vs response-generation failures, and a span-level completion rate catches silent failures that token/duration miss [^src4].

Token and duration tell you *something changed* even when an agentic system fails gracefully rather than crashing — powerful because graceful failures are hard to detect [^src4]. Combining signals across span types localizes the problem: high planning-span tokens + low tool-call completion is a different root cause than stable metrics with declining evaluation scores [^src4].

## SWE-bench Multilingual

SWE-bench Multilingual is a benchmark for evaluating AI coding agents on real-world software engineering tasks across multiple programming languages [^src6].

**Scope** [^src6]:
- 300 tasks from 42 repositories in 9 programming languages
- Tasks are real GitHub issues requiring code changes to resolve (the same structure as SWE-bench Verified, generalized beyond Python)
- Languages: Python, JavaScript/TypeScript, Java, Go, Ruby, Rust, C/C++, C#, PHP

**Headline results (Claude 3.7 Sonnet + SWE-agent)** [^src6]:
- **43% overall** (vs 63% on SWE-bench Verified, the Python-only benchmark)
- Highest-performing language: **Rust** (58%)
- Lowest-performing language: **C/C++** (28%)
- The gap between Verified (Python) and Multilingual scores quantifies the Python bias baked into current agents and training data

**Key finding** [^src6]: the gap is not just about syntax — it's about the density of public training examples, the maturity of language-specific tooling (linters, test runners, type systems), and how well agentic scaffolding is tuned for each language's idioms. "The benchmark highlights how much of current agent capability is Python-specific rather than general software engineering ability."

**Comparison with prior art** [^src6]:
- SWE-bench Lite (Python only, 300 tasks): 43.7% Claude Sonnet 3.5 + Agentless
- SWE-bench Verified (Python only, 500 tasks): 63% Claude Sonnet 3.7 + SWE-agent
- SWE-bench Multilingual (9 languages, 300 tasks): 43% — roughly matching Lite despite including languages where models are weaker

**Implication for practitioners** [^src6]: when evaluating coding agents for non-Python work (Java backends, Go services, Rust systems code), expect performance closer to 30–50% of Verified results. Use language-specific golden datasets (per §Golden datasets above) rather than extrapolating from Python benchmark scores.

## METR time horizons — industry-wide capability measurement

METR (Model Evaluation & Threat Research) publishes the **task-completion time horizon**: the human-expert task duration at which a frontier AI agent is predicted to succeed with a given reliability level [^src7].

- **50%-time horizon**: task length where the agent succeeds half the time
- **80%-time horizon**: task length where the agent succeeds 80% of the time

Both metrics are measured using logistic regression over METR's benchmark of 100+ diverse software tasks (RE-Bench, HCAST, and novel short tasks) with automated success criteria [^src7].

**What "time horizon" measures (and doesn't)**:
- It measures *task difficulty* (calibrated by how long a human expert takes) — NOT how long the AI takes to run.
- AI agents typically finish tasks several times faster than human contractors, often writing code in one shot without iterative lookup [^src7].
- The benchmark is software/ML/cybersecurity-heavy; time horizons vary significantly across domains (same exponential trend, different absolute levels) [^src7].
- An 8-hour time horizon does NOT mean AI can automate all jobs — it means it can complete *well-specified, self-contained* 8-hour software tasks without prior context.

**Exponential growth trend**: across public frontier models, time horizons are growing roughly exponentially — a useful macro-benchmark for tracking the pace of agent capability improvement at the industry level [^src7].

**Implication for eval design**: METR's tasks are self-contained and well-specified. Real-world agentic performance draws on prior context (conversations, domain knowledge, existing codebases) — the benchmark assumes low/zero context, similar to a new hire or freelance contractor. Practitioners should design their own golden datasets (see §Golden datasets above) for tasks that require sustained context [^src7].

## SWE-bench Verified: Claude's performance and philosophy

Claude 3.5 Sonnet scored **49% on SWE-bench Verified** (GitHub issues from real repos), beating the previous SOTA of ~45% [^src8]. Key philosophical points from the Anthropic writeup:

**Minimal scaffold philosophy** [^src8]: Anthropic tested multiple levels of scaffolding complexity and found that "simple scaffolds often beat complex ones." The winning submission used standard tools (bash, file editing, code execution) without elaborate orchestration — the model's judgment was the primary driver of performance, not the harness.

**Tool description weight** [^src8]: "The single-highest-impact intervention was improving the descriptions of the tools available to the agent." Clear, precise tool descriptions (especially for file-editing tools) meaningfully improved task completion rates without changing the underlying model or scaffold.

**Context window** [^src8]: the 200K context limit was sufficient for most SWE-bench tasks; Claude rarely hit the limit. For practitioners: 200K is enough headroom for well-structured agentic coding tasks if context is managed with intent.

**Implications for eval design** [^src8]: SWE-bench measures concrete repair tasks on real GitHub issues — pass/fail via test suite. This is a high-signal, low-ambiguity eval. Most practitioners should mirror this structure: binary outcomes tied to executable criteria, not rubric-based scoring.

## Fit checklist for autonomous agent loops (autoresearch)

When evaluating whether a task is suitable for a fully autonomous overnight agent loop — with the agent scoring its own output — three conditions must hold [^src9]:

**Must-haves**:
1. **Objective score** — the quality metric can be computed programmatically without human judgment in the loop. "Come up with the funniest joke — how do you measure funny? You need that objective measure."
2. **Fast feedback loop** — each experiment completes in minutes, not hours, so the agent can run many iterations overnight.
3. **AI write access** — the agent can modify the asset being optimized.

**Nice-to-haves**: high feedback volume, cheap to fail (experiments are reversible), consistent measuring stick (scorer doesn't drift across runs).

This checklist comes from Karpathy's `autoresearch` repo practice and is directly applicable to deciding whether a custom eval can run headlessly. If all three must-haves hold, the agent loop is self-sustaining; if the score is subjective, a human must be in the loop (which breaks the overnight compounding pattern).

See also: [Compound Engineering](/ai-engineering/compound-engineering.md) §Autoresearch for the 3-file system (instructions / asset / scoring file) that implements this pattern.

## Evaluating agentic workflows

Hamel Husain's recommended two-phase approach for agent evaluation [^src11]:

**Phase 1 — End-to-end task success.** Treat the agent as a black box: "did we meet the user's goal?" Define a precise success rule per task (exact answer, correct side-effect) and measure with human or aligned LLM judges. Note the first upstream failure when conducting error analysis.

**Phase 2 — Step-level diagnostics.** Once error analysis reveals which workflows fail, score individual components: tool choice (was the selected tool appropriate?), parameter extraction (were inputs complete?), error handling (did the agent recover from empty results?), context retention (were earlier constraints preserved?), efficiency (steps, tokens, time), and goal checkpoints.

**Transition failure matrices**: "Create a matrix where rows represent the last successful state and columns represent where the first failure occurred." This transforms overwhelming agent complexity into actionable insights — immediately surfacing whether, e.g., `GenSQL → ExecSQL` transitions cause 12 failures while `DecideTool → PlanCal` causes only 2 [^src11].

## SWE-Bench Pro 2026: task specification as a hidden eval variable

A large-scale 2026 benchmarking study ($50k total compute) on SWE-Bench Pro produced two major findings about what benchmarks actually measure [^src13].

**Setup**: Zencoder ran 15 frontier models using native CLIs on SWE-Bench Pro via Harbor (an open-source tool for local SWE-Bench execution), supplemented by Fireworks inference for open-weights models. Benchmark: real GitHub issues across multiple languages.

### The $20k bug that changed the analysis

A Harbor adapter bug accidentally leaked fail-to-pass tests from the golden patch while keeping task descriptions minimal — creating a "regression-style" setup resembling real CI/CD: CI catches a failure, developer gets a short description plus a stack trace and failing tests, and must figure out both what's wrong and how to fix it — "without a detailed implementation spec" [^src13].

This unintentional fork produced two radically different tables:

**Standard results** (detailed instructions: exact class names, interface definitions, variable naming):

| Model | Standard Score |
|---|---|
| claude-opus-4-6 | 52.7% |
| openai/gpt-5.4 | 51.3% |
| claude-sonnet-4-6 | 50.7% |
| google/gemini-3.1-pro | 49.9% |

All frontier models cluster within a ~6-point band.

**Regression-style results** (minimal description + leaked failing tests — more representative of real engineering):

| Model | Regression Score | Δ vs Standard |
|---|---|---|
| claude-sonnet-4.6 | 78.90% | +28.2 |
| claude-opus-4.6 | 76.58% | +23.9 |
| gpt-5.3-codex | 63.42% | +13.8 |
| gpt-5.4 | 62.33% | +11.0 |
| gemini-3.1-pro | 52.33% | +2.4 |
| kimi-k2.5 | 43.15% | -1.7 |
| minimax-2.5 | 32.60% | -8.5 |

Spread explodes from ~6 points to ~46 points. Anthropic dominates. Some models (Minimax, Kimi) get *worse* with ambiguity [^src13].

### Key findings

**Task specification is a hidden variable** [^src13]: "When you measure performance on perfectly specified tasks, all models look the same. The real differentiation shows up exactly where benchmarks usually don't look: in the messy, ambiguous, underspecified reality of day-to-day engineering."

**Models solve different problems even at similar scores** [^src13]: cross-cutting analysis of 730 tasks showed only 68–84% pairwise Jaccard overlap between same-vendor model pairs, and as low as 68% cross-vendor. Of 730 tasks: 144 (19.7%) trivially solved by all models; 224 (30.7%) solved by none; 259 (35.5%) are the differentiating set.

**Model pairing for ensembles** [^src13]: highest-value pairs are cross-vendor (Anthropic + Google: 68% overlap); same-vendor pairs are largely redundant (OpenAI Codex ↔ GPT-5.4: 84% overlap). "If you're picking two models for an ensemble, you get far more out of pairing Anthropic + Google than pairing two OpenAI models."

**Orchestration implication** [^src13]: "Relying on a single model is leaving performance on the table. Under the hood, each model has blind spots that others cover. A well-designed orchestration layer can push your effective solve rate well beyond what any individual model achieves." This is the production case for multi-model agent review pipelines.

**The 80% ceiling and what it means** [^src13]: Sonnet 4.6 at ~79% on regression-style tasks "essentially means this benchmark has been beaten" — but "real-world tasks are far messier than any benchmark, and no single model will sustain 80% in production." The areas humans still own: system design and architecture, UX, "peripheral vision" (noticing a problem before it becomes one).

**Sonnet over Opus at high resolve rates**: at the ~80% level, Opus tends to "overthink and produce solutions that may theoretically be better, but don't pass the specific tests" — hitting the benchmark ceiling of reliable measurement, not model capability [^src13].

## Evals-skills for coding agents

OpenAI's Harness Engineering result: three engineers, five months, ~1M lines of code built with Codex agents — "improving the infrastructure around the agent mattered more than improving the model" [^src12]. Documentation tells the agent what to do; telemetry tells it whether it worked; evals tell it whether the output is good.

The `evals-skills` open-source plugin (Hamel Husain) provides Claude Code skills that guard against common eval mistakes: `eval-audit` (diagnostic sweep across six areas with prioritized action list), `error-analysis`, `write-judge-prompt`, `validate-evaluator`, `evaluate-rag`, `build-review-interface`, `generate-synthetic-data` [^src12]. All major eval vendors (Braintrust, LangSmith, Phoenix) now ship MCP servers — agents can query traces directly, but methodology is still required to know what to do with them.

## See also

- [Error Analysis](/ai-engineering/error-analysis.md) — the discovery phase that defines what these evals measure
- [LLM Evals](/ai-engineering/llm-evals.md) — full Hamel Husain evaluation methodology: critique shadowing, binary pass/fail, domain experts, anti-patterns
- [Hamel Husain](/ai-engineering/hamel-husain.md) — practitioner who developed the methodology; 50+ company engagements
- [LangSmith](/ai-engineering/langsmith.md) — platform that implements these patterns
- [AI Agent](/ai-engineering/ai-agent.md) — the systems being evaluated
- [Context Engineering](/ai-engineering/context-engineering.md) — context window growth directly affects evaluation quality (thread evaluator catches degradation)
- [Context Window Management](/ai-engineering/context-window-management.md) — token-drift monitoring surfaces multi-turn context accumulation
- [RAG](/ai-engineering/rag.md) — temporal accuracy is an eval dimension most RAG benchmarks miss
- [Agent Harness](/ai-engineering/agent-harness.md) — harness choice can swing eval scores independent of the model

---

[^src1]: [LangSmith - Debugging and Evaluating AI Agents](/03_Resources/Study Notes/LangSmith - Debugging and Evaluating AI Agents.md)
[^src2]: [Better Experiments with LLM Evals — A Funnel, Not a Fork](../../raw/web/better-experiments-with-llm-evals-a-funnel-not-a-fork-spotif.md)
[^src3]: [What Data Agent Benchmarks Do and Don't Tell Us](../../raw/web/what-data-agent-benchmarks-do-and-don-t-tell-us.md)
[^src4]: [Monitoring Cortex Agent Performance With Trace Data](../../raw/web/monitoring-cortex-agent-performance-with-trace-data.md)
[^src5]: [Fable Evals Performance / We Had to Build New Evals for Fable](../../raw/email/email-2026-06-11-fable-evals-performance-airbnbs-evolved-data-architecture-po.md)
[^src6]: [SWE-bench Multilingual — Anthropic](../../raw/web/web-swe-bench-multilingual.md)
[^src7]: [Task-Completion Time Horizons of Frontier AI Models](../../raw/web/web-task-completion-time-horizons-of-frontier-ai-models.md) — METR, metr.org
[^src8]: [Claude on SWE-bench Verified — Anthropic blog](../../raw/web/web-claude-swe-bench-performance.md) — Anthropic
[^src9]: [This "Karpathy System" could 701x your AI Workflows — autoresearch fit checklist](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-this-karpathy-sys-report.md) — YouTube (processed report)
[^src10]: [A Field Guide to Rapidly Improving AI Products](../../raw/web/web-a-field-guide-to-rapidly-improving-ai-products-hamels-blog-h.md) — Hamel Husain, hamel.dev
[^src11]: [LLM Evals: Everything You Need to Know](../../raw/web/web-llm-evals-everything-you-need-to-know-hamels-blog-hamel-husa-5bf201ee.md) — Hamel Husain & Shreya Shankar, hamel.dev
[^src12]: [Evals Skills for Coding Agents](../../raw/web/web-evals-skills-for-coding-agents-hamels-blog-hamel-husain-f8a26550.md) — Hamel Husain, hamel.dev
[^src13]: [SWE-Bench Pro Results 2026: AI Coding Model Rankings](../../raw/web/web-swe-bench-pro-results-2026-ai-coding-model-rankings-dca3b106.md) — Andrew Filev & Dmitry Krasnov, Zencoder blog, 2026

<!-- RELATED:START (generated by bin/corpus_heal.py related — do not edit inside) -->

## Related across domains

- [AI Observability as a Data Pipeline](/data-engineering/ai-observability-data-pipeline.md) · _data-engineering_

<!-- RELATED:END -->
