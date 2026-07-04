---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-from-the-hugging-face-hub-to-robot-hardware-with-strands-age-c7b6e0d1.md
    channel: web
    ingested_at: 2026-07-04
aliases:
  - Strands Robots
  - Strands Agents
  - strands-robots
  - AWS Strands
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-04
updated: 2026-07-04
---

# Strands Robots

**TL;DR.** Strands Robots is an open-source SDK from AWS (Apache 2.0) that exposes robotics abstractions, simulation (MuJoCo), and the LeRobot stack as **AgentTools** composable into a single Strands agent [^src1]. Its design goal: five separate tools (record, train, simulate, deploy, coordinate) that didn't talk to each other, unified into one agent loop where the agent orchestrates all of them [^src1].

## Architecture

Two design choices that make the unification work [^src1]:

1. `Robot("so100")` returns a **simulation** by default (MuJoCo-backed, no hardware risk); `mode="real"` returns a hardware-backed robot driven by LeRobot. Agent code is **identical across both modes**.
2. The `DatasetRecorder` that writes a `LeRobotDataset` is shared between simulation and LeRobot's hardware recording — a dataset from MuJoCo and one from a physical SO-101 are in the same format.

## Five-step agent workflow (one Strands agent)

```python
from strands_robots import Robot
from strands import Agent

arm = Robot("so100")  # simulation by default
agent = Agent(tools=[arm])
agent("Pick up the red cube")
```

Internal steps [^src1]:
1. Record demonstrations as a `LeRobotDataset` (simulation or hardware)
2. Push dataset to Hugging Face Hub
3. Run a policy against the same format
4. Deploy the same agent code to physical hardware with `mode="real"`
5. Coordinate a fleet via a built-in Zenoh peer mesh

## Integration with LeRobot

LeRobot's own CLIs (`lerobot-record`, `lerobot-calibrate`) handle hardware bring-up and calibration; Strands Robots picks up from there [^src1]. Policy inference is backed by GR00T or LerobotLocal (a common interface); MolmoAct2 checkpoints run through the LerobotLocal path [^src1].

## Supported model providers

The agent's reasoning loop can use Amazon Bedrock (AWS credentials), Anthropic API, OpenAI, or Ollama locally [^src1].

## Related

- [Hugging Face](/ai-engineering/hugging-face.md) — Strands Robots uses HF Hub for dataset storage and model weights
- [AI Agent](/ai-engineering/ai-agent.md) — the agent loop driving robot operations
- [Local AI Agents](/ai-engineering/local-ai-agents.md) — local agent patterns (Ollama as local model provider)
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [From the Hugging Face Hub to robot hardware with Strands Agents and LeRobot](../../raw/_inbox/web-from-the-hugging-face-hub-to-robot-hardware-with-strands-age-c7b6e0d1.md) — Hugging Face blog, AWS, 2026-06
