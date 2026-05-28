---
type: concept
domain: ai-engineering
status: draft
sources:
  - path: 03_Resources/Study Notes/LangSmith - Debugging and Evaluating AI Agents.md
    channel: notes
    ingested_at: 2026-05-21
aliases:
  - agent evaluation
  - LLM evaluation
  - agent benchmarking
  - online evaluation
  - offline evaluation
tags:
  - corpus/ai-engineering
  - concept
created: 2026-05-21
updated: 2026-05-21
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

## See also

- [[ai-engineering/langsmith|LangSmith]] — platform that implements these patterns
- [[ai-engineering/ai-agent|AI Agent]] — the systems being evaluated
- [[ai-engineering/context-engineering|Context Engineering]] — context window growth directly affects evaluation quality (thread evaluator catches degradation)

---

[^src1]: [[03_Resources/Study Notes/LangSmith - Debugging and Evaluating AI Agents|LangSmith - Debugging and Evaluating AI Agents]]
