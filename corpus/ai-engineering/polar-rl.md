---
type: concept
domain: ai-engineering
status: stub
sources:
  - path: raw/_inbox/web-polar-agentic-rl-on-any-harness-at-scale.md
    channel: web
    ingested_at: 2026-08-19
aliases:
  - Polar
  - Polar RL
  - agentic RL framework
  - Prorl Agent
confidence: 0.9
last_confirmed: 2026-08-19
tags:
  - ai-engineering
  - reinforcement-learning
  - agent-harness
  - training
created: 2026-08-19
updated: 2026-08-19
---

# Polar: Agentic RL on Any Harness at Scale

**TL;DR**: Polar is a rollout framework for scalable asynchronous RL over arbitrary agent harnesses. It treats the harness as a black box, proxying LLM API calls and recording token-level interactions for trajectory reconstruction. Validated on SWE-Bench Verified across four coding harnesses (Codex, Claude Code, Qwen Code, Pi).

## Problem it solves

Reinforcement learning for language agents increasingly depends on custom harnesses managing long-running context, multi-turn tool use, and multi-agent orchestration. Porting these harnesses into RL environment interfaces is difficult and often loses training signals. Polar bridges this gap.[^polar]

## Design

- Treats the agent harness as a **black box**: proxies LLM API calls, records token-level model interactions, reconstructs token-faithful trajectories for training
- Each rollout node manages runtime prewarming, agent execution, trajectory reconstruction, and evaluation in parallel
- Exposes asynchronous service endpoints consumable by independent trainers
- Decoupled from specific harnesses, training infrastructure, and RL algorithms
- Also supports offline data generation over custom harnesses[^polar]

## Results

Using simple GRPO, Polar improved Qwen3.5-4B on SWE-Bench Verified:
- Codex harness: +22.6 points
- Claude Code harness: +4.8 points
- Qwen Code harness: +0.6 points
- Pi harness: +6.2 points[^polar]

## Lineage

Polar rewrites its preceding work, **Prorl Agent**, and has been registered as one of NeMo Gym environments.[^polar]

## Related

- [/ai-engineering/agent-harness.md](/ai-engineering/agent-harness.md)
- [/ai-engineering/pi-agent.md](/ai-engineering/pi-agent.md)
- [/ai-engineering/agentic-coding.md](/ai-engineering/agentic-coding.md)

[^polar]: Polar paper, arxiv.org/abs/2605.24220, submitted 2026-05-22. `raw/_inbox/web-polar-agentic-rl-on-any-harness-at-scale.md`
