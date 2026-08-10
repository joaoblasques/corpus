---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/notes/notes-03-resources-articles-physical-ai-when-ai-gets-a-body.md
    channel: notes
    ingested_at: 2026-07-14
aliases:
  - physical AI
  - embodied AI
tags:
  - corpus/ai-engineering
  - source
  - physical-ai
  - robotics
  - simulation
  - reinforcement-learning
created: 2026-07-14
updated: 2026-08-10
provisional: false
url: https://www.linkedin.com/pulse/7-ai-terms-youll-hear-lot-this-year-alex-wang
origin: obsidian
---

# Physical AI — When AI Gets a Body

**TL;DR:** Physical AI is the convergence of AI models, robotics, and sensors into systems that can sense, move, and act in the real world. Simulation environments are central to training these systems safely before real-world deployment.

*Source: Alex Wang, "7 AI Terms You'll Hear a Lot This Year" (LinkedIn)[^1]. Shared provenance with sibling pages — see §Corpus relations.*

---

## Definition

Physical AI refers to "AI systems embedded in machines that can sense, move, and interact with the real world."[^1] Unlike purely software-based AI, physical AI must perceive its environment, actuate physical systems, and handle unpredictable real-world conditions.

The convergence enabling this shift is three-way: **AI models + robotics + sensors**.[^1]

---

## Why it matters

Most AI systems today exist purely in software.[^1] Moving into the physical world introduces a qualitatively different set of challenges:

- **Perception** — understanding the environment through sensors.[^1]
- **Movement** — controlling actuators and limbs.[^1]
- **Safety** — avoiding harm to people and objects.[^1]
- **Real-world unpredictability** — handling situations never seen in training.[^1]

Advances across models, sensors, and robotics are making this shift viable now.[^1]

---

## Where it's showing up

Wang identifies four prominent examples[^1]:

| Player | Focus |
|---|---|
| Figure AI | Humanoid robots with AI-powered reasoning |
| Agility Robotics | Robots for logistics and warehouse work |
| Boston Dynamics | Legged robots with advanced mobility |
| NVIDIA Isaac | Simulation environments for training physical AI |

---

## Role of simulation

Simulation is key to training physical AI safely.[^1] Robots cannot be trained purely in the real world without risk of damage or harm. Simulation environments (such as NVIDIA Isaac) allow iterative training at scale before physical deployment. This links to synthetic data generation and deep reinforcement learning as the underlying learning paradigm.

---

## Corpus relations

- [Edge AI — Running AI On Device](/ai-engineering/sources/edge-ai-running-ai-on-device-dece.md) — sibling section of the same Alex Wang article; embodied AI *depends on* on-device inference since a robot cannot round-trip to the cloud for every action.
- [Strands Robots](/ai-engineering/strands-robots.md) — a concrete robotics instance of this embodied AI pattern.
- [Reinforcement Learning](/ai-engineering/reinforcement-learning.md) — the learning paradigm behind simulation-trained physical control.
- ["7 AI Terms You'll Hear a Lot This Year" (Alex Wang)](/ai-engineering/seven-ai-terms-2026-alex-wang.md) — shared-provenance synthesis: this page and its siblings all derive from that single article and do not corroborate each other.
- [AI Engineering hub](/ai-engineering/README.md)

---

[^1]: Alex Wang, "7 AI Terms You'll Hear a Lot This Year," LinkedIn, 2026. `raw/notes/notes-03-resources-articles-physical-ai-when-ai-gets-a-body.md`
