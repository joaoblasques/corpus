---
type: concept
domain: ai-engineering
status: draft
aliases:
  - sampling
  - temperature
  - top-k
  - top-p
  - nucleus sampling
  - test-time compute
  - generation parameters
tags:
  - corpus/ai-engineering
  - llm-internals
  - inference
  - sampling
sources:
  - path: raw/web/web-generation-configurations-temperature-top-k-top-p-and-test-t-1ccdc7f1.md
    channel: web
    title: "Generation configurations: temperature, top-k, top-p, and test time compute"
confidence: 0.95
last_confirmed: 2026-08-12
created: 2026-08-12
updated: 2026-08-12
---

# Generation Configurations: Sampling and Test-Time Compute

**TL;DR**: LLMs are probabilistic. Sampling strategies (temperature, top-k, top-p) control how tokens are drawn from the probability distribution. Test-time compute (sampling multiple outputs and selecting the best) trades cost for accuracy. Structured outputs constrain generation at three layers: prompting, sampling, or fine-tuning.

## Why LLMs are probabilistic

A language model computes a probability distribution over all vocabulary tokens for the next position. Rather than always picking the highest-probability token (greedy sampling, which produces boring outputs), models sample from the distribution. This enables creativity but causes inconsistency and hallucinations.[^src]

## Temperature

Temperature T adjusts logits before the softmax: each logit x_i is divided by T, then softmax is applied to the adjusted logits.[^src]

`p_i = softmax(x_i / T) = e^(x_i/T) / Σ_j e^(x_j/T)`

Effect:
- **T < 1**: sharpens the distribution (common tokens become more likely, rare ones less so) → more deterministic, more boring
- **T = 1**: no adjustment (default softmax)
- **T > 1**: flattens the distribution (rare tokens get a boost) → more diverse, more creative
- **T → 0**: argmax — picks the highest-logit token deterministically (T=0 is a special case; can't divide by 0, so in practice the model just does argmax)

Typical values: 0 for consistency/factual tasks; 0.7 for creative tasks (balances creativity and coherence); max usually 2.[^src]

## Top-k

Compute softmax over only the k highest logits, ignoring all others. Saves computation (avoids full vocabulary softmax) and reduces the chance of sampling unlikely tokens. k = 50–500 depending on desired diversity.[^src]

Limitation: fixed k doesn't adapt to context. Some contexts warrant 2 options (yes/no); others warrant 500+.

## Top-p (nucleus sampling)

Sort tokens by probability descending; sum until cumulative probability ≥ p; sample from that set only. More context-sensitive than top-k because the vocabulary size adapts per context.[^src]

Common range: top-p = 0.9–0.95. At p=0.9, considers the minimal set whose cumulative probability exceeds 90%.

Top-p doesn't always reduce softmax computation (still computes over full vocabulary to sort), but produces more contextually appropriate outputs in practice.[^src]

## Logprobs

Log probabilities (logprobs) are preferred over raw probabilities in practice because the tiny per-token probabilities cause numeric underflow at large vocabulary sizes. The logprob of a sequence is the sum of the logprobs of each token; for picking the "best" output, use average logprob (normalized by length) to avoid bias toward short outputs.[^src]

## Test-time compute

Sampling N outputs and selecting the best one. Three selection approaches:[^src]
1. **Highest average logprob** — pick the output whose tokens are most probable on average
2. **Reward model scoring** — use a trained verifier to score each candidate
3. **Majority vote / most frequent answer** — useful for classification or exact-answer tasks (e.g. math problems)

Performance gain plateaus and can reverse: OpenAI's verifier experiments found gains stopped around 400 sampled outputs. Beyond this, adversarial outputs that fool the verifier become more likely.[^src]

Cost: generating N outputs costs ~N × single-output cost. At scale, only justified for high-value or hard-answer queries.

Heuristic: "The more fickle a model is, the more we can benefit from sampling multiple outputs. The optimal thing to do with a fickle model, however, is to swap it out for another."[^src]

## Structured outputs

Three layers for constraining output format:[^src]

| Method | Reliability | Cost |
|---|---|---|
| Prompting (instruct model to output JSON) | Lowest — not guaranteed | No extra cost |
| Constraint sampling (reject non-conforming tokens at sampling time) | High — mathematically enforced | Moderate overhead |
| Fine-tuning + architecture modification (e.g. classifier head) | Highest — deterministic | Training cost |

JSON mode (OpenAI): guarantees valid JSON syntax, not specific schema. Also doesn't guarantee non-truncation if max tokens is too low.

"As models become more powerful, we can expect them to get better at following instructions … these techniques will become less important."[^src]

## Cross-links

- [/ai-engineering/chip-huyen.md](/ai-engineering/chip-huyen.md) — Chip Huyen authored this material
- [/ai-engineering/agent-cost-management.md](/ai-engineering/agent-cost-management.md) — test-time compute tradeoff is directly a cost management question

---

[^src]: raw/web/web-generation-configurations-temperature-top-k-top-p-and-test-t-1ccdc7f1.md

<!-- RELATED:START (generated by bin/corpus_heal.py related — do not edit inside) -->

## Related across domains

- [Model Serving (Real-Time API + Batch Inference)](/mlops/model-serving.md) · _mlops_

<!-- RELATED:END -->
