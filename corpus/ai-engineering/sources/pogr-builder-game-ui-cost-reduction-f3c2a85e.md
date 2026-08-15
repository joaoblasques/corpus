---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-how-pogr-cut-30k-and-a-year-of-ui-work-with-builder-f3c2a85e.md
    channel: web
    ingested_at: 2026-08-15
aliases:
  - POGR Builder case study
  - game UI cost reduction
  - Figma-to-engine pipeline
  - Blazium game studio
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-15
updated: 2026-08-15
url: https://www.builder.io/blog/how-pogr-cut-30k-and-a-year-of-ui-work
origin: obsidian-list
---

# How POGR Cut $30K and a Year of UI Work with Builder

**TL;DR** — POGR/Blazium Games (10-dev indie studio, multiple titles) eliminated $30K+ and ~1 year of UI development per game by routing Figma → Builder → game engine instead of custom-tooling the Figma → React → manual CSS/SVG → engine chain. Animation now ships with the design rather than being bolted on at the end.[^src1]

## The problem: game UI is the highest-cost surface

"Game UI is the most expensive surface in game development. It touches the interface a player interacts with every second, the environment they move through, the character art on screen, and the marketing pages that sell the game in the first place."[^src1]

Before Builder, POGR's pipeline: design in Figma → custom conversion tools → React components → engineers manually rip apart components, write CSS, extract SVGs, rebuild in engine → animation scripted from scratch on top of static screens.

Numbers on their flagship project *Depths*: $5K spent for 25% UI completion; $30K+ projected for full UI; 2.5–3 months per quarter of the UI; full year projected for complete UI.[^src1]

## The insight: Builder output is game engine feedstock

Builder's export (clean CSS, SVGs, animation logic) is the same raw material a game engine consumes. POGR now prototypes UIs in Builder, exports as React/HTML, converts to native engine formats including C# for Blazium engine. Animation logic carries through to GDScript — motion ships with the design from the start.[^src1]

## Results

| Metric | Before | With Builder |
|---|---|---|
| Full UI cost | $30K+ | ~$30K saved |
| Full UI timeline | 1 year | Weeks to months |
| Quarter UI build | 2.5–3 months | Days to weeks |
| Animation | Scripted manually post-integration | Ships with design |

"We were looking at a year and $30K to finish the UI on one project. Now it takes weeks. There's nothing else doing this for game studios."[^src1]

## Broader relevance

Savings compound across a multi-title roadmap: $30K × N titles + recovered dev time = fundamentally different operating model. Indie developers have been priced out of high-quality animated UIs; tooling that compresses Figma-to-engine is equivalent to the same structural shift generative UI brings to web product teams.

See also [Designing Generative UI in an Agent-Native World](/ai-engineering/sources/designing-generative-ui-agent-native-c57dd663.md) for the design-system-first framing that explains *why* Builder's output is pipeline-safe.

## See also

- [Agent UI](/ai-engineering/agent-ui.md)
- [Designing Generative UI (agent-native world)](/ai-engineering/sources/designing-generative-ui-agent-native-c57dd663.md)

---

[^src1]: [How POGR Cut $30K and a Year of UI Work with Builder](../../../raw/web/web-how-pogr-cut-30k-and-a-year-of-ui-work-with-builder-f3c2a85e.md) — Builder.io blog, 2026-06-29
