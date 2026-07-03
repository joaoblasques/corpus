---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-announcing-vime-a-simple-stable-and-efficient-rl-framework-f-9a392163.md
    channel: web
    ingested_at: 2026-07-02
aliases:
  - vime
  - slime
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-02
updated: 2026-07-02
---

# vime

**TL;DR.** vime is an LLM post-training (RL) framework within the [vLLM](/ai-engineering/vllm.md) ecosystem. It ports **slime**'s training-stack and data-generation design onto [vLLM](/ai-engineering/vllm.md) as the rollout/inference backend, connecting Megatron (training) and vLLM (inference) into one RL pipeline, aiming for stable train-inference alignment across Dense and MoE models [^src1].

## Architecture

Three-stage decoupled train-inference design (inherited from slime, with vLLM replacing the rollout backend) [^src1]:

- **Training (Megatron)** — the main training loop; parameter updates, synchronizes weights to the rollout side.
- **Rollout (vLLM + Router)** — inference sampling that produces training samples with reward/verifier signals.
- **Data Buffer** — connects training and rollout; manages prompt injection and custom rollout logic.

## Key capabilities

- vLLM-side arguments passed through via `--vllm-prefix`; default rollout entry point `vime.rollout.vllm_rollout`.
- **Stable train-inference alignment**: `train_rollout_logprob_abs_diff` (the divergence between the logprobs computed during training vs. during rollout) stays in a controllable range over long runs.
- For MoE models specifically, **R3 (routing replay)** further reduces train-inference mismatch by replaying the same expert-routing decisions between train and rollout passes.
- Algorithm coverage: GRPO, PPO; model coverage: Qwen3 Dense/MoE, GLM-4.5, with CI-verified end-to-end examples.

## Validation benchmarks

| Setup | Result |
|---|---|
| Qwen3-30B-A3B, 8-GPU colocate, GRPO, dapo-math-17k | GB200 ~147s/step, H200 ~252s/step (GB200 ~1.72× H200) |
| Qwen3-4B on A100, GRPO, 4 train + 4 inference non-colocate, gsm8k | `train_rollout_logprob_abs_diff` stable ~0.011 vs. baseline drifting to ~0.77 |
| Qwen3-30B-A3B MoE on A100, EP=4, R3 enabled | logprob diff reduced from ~0.019 to ~0.013 |
| Qwen3-30B-A3B MoE on GB200, 8-GPU colocate | logprob diff stable ~0.018, no baseline drift |
| GLM-4.5-Air on GB200, GRPO, 8-GPU colocate | raw_reward trending up over 100 steps (mean ~0.56); logprob diff mean ~0.028 |

The consistent finding across these runs: vime's train-inference logprob divergence stays low and stable, whereas an unnamed baseline framework drifts substantially over the course of training [^src1].

## Positioning

vLLM's community already supports several post-training frameworks (NeMo RL, OpenRLHF, verl, others); vime specifically targets bringing slime's proven training paradigm into the vLLM ecosystem as a production-ready bridge, not replacing the other options [^src1]. Open-sourced under Apache 2.0.

## Related

- [vLLM](/ai-engineering/vllm.md) — the inference/rollout backend vime pairs with Megatron
- [Mixture of Experts](/ai-engineering/mixture-of-experts.md) — R3 routing-replay specifically targets MoE train-inference mismatch
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [Announcing vime: A Simple, Stable, and Efficient RL Framework for LLMs](../../raw/web/web-announcing-vime-a-simple-stable-and-efficient-rl-framework-f-9a392163.md) — vLLM blog, 2026-06-09
