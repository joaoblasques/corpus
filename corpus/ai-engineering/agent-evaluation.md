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
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-21
updated: 2026-06-25
last_confirmed: 2026-06-25
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

## Trace-based production monitoring

Beyond golden-dataset evals, production agents are monitored via **trace data** — a hierarchy of spans per interaction [^src4]. Snowflake's Cortex Agents log span-level traces (`GET_AI_OBSERVABILITY_EVENTS`) mapping `record_name` to agent phases [^src4]:

| Span type | Captures |
|---|---|
| `chat` | Top-level conversation turn; full input/output + `thread_id` |
| `planning` | Tool selection, query formulation, per-step token count + model name |
| `response_generation` | Final answer synthesis cost |
| `tool_call` | Search query/filters/results, or generated SQL + `question_category` |

A monitoring **maturation curve**: moment-in-time snapshots → dashboards → anomaly detection on trends → incident management for SLAs [^src4]. The three baseline metrics where abnormal behavior shows up first [^src4]:

- **Total tokens** (per span, not per conversation) — a step-change up signals a persistent config change; gradual drift signals multi-turn context accumulation (a session can climb from 5k to 40k tokens by turn 10), the case for explicit [[ai-engineering/context-window-management|context window management]] [^src4].
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

See also: [[ai-engineering/compound-engineering|Compound Engineering]] §Autoresearch for the 3-file system (instructions / asset / scoring file) that implements this pattern.

## See also

- [[ai-engineering/langsmith|LangSmith]] — platform that implements these patterns
- [[ai-engineering/ai-agent|AI Agent]] — the systems being evaluated
- [[ai-engineering/context-engineering|Context Engineering]] — context window growth directly affects evaluation quality (thread evaluator catches degradation)
- [[ai-engineering/context-window-management|Context Window Management]] — token-drift monitoring surfaces multi-turn context accumulation
- [[ai-engineering/rag|RAG]] — temporal accuracy is an eval dimension most RAG benchmarks miss
- [[ai-engineering/agent-harness|Agent Harness]] — harness choice can swing eval scores independent of the model

---

[^src1]: [[03_Resources/Study Notes/LangSmith - Debugging and Evaluating AI Agents|LangSmith - Debugging and Evaluating AI Agents]]
[^src2]: [Better Experiments with LLM Evals — A Funnel, Not a Fork](../../raw/web/better-experiments-with-llm-evals-a-funnel-not-a-fork-spotif.md)
[^src3]: [What Data Agent Benchmarks Do and Don't Tell Us](../../raw/web/what-data-agent-benchmarks-do-and-don-t-tell-us.md)
[^src4]: [Monitoring Cortex Agent Performance With Trace Data](../../raw/web/monitoring-cortex-agent-performance-with-trace-data.md)
[^src5]: [Fable Evals Performance / We Had to Build New Evals for Fable](../../raw/email/email-2026-06-11-fable-evals-performance-airbnbs-evolved-data-architecture-po.md)
[^src6]: [SWE-bench Multilingual — Anthropic](../../raw/web/web-swe-bench-multilingual.md)
[^src7]: [Task-Completion Time Horizons of Frontier AI Models](../../raw/web/web-task-completion-time-horizons-of-frontier-ai-models.md) — METR, metr.org
[^src8]: [Claude on SWE-bench Verified — Anthropic blog](../../raw/web/web-claude-swe-bench-performance.md) — Anthropic
[^src9]: [This "Karpathy System" could 701x your AI Workflows — autoresearch fit checklist](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-this-karpathy-sys-report.md) — YouTube (processed report)
