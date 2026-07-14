---
type: concept
domain: ai-engineering
status: stub
sources:
  - path: raw/_inbox/pdf-the-quest-for-artificial-intelligence-a-history-of-part-01.md
    channel: pdf
    ingested_at: 2026-07-14
aliases:
  - AI history
  - history of artificial intelligence
  - quest for artificial intelligence
  - AI timeline
tags:
  - corpus/ai-engineering
  - concept
created: 2026-07-14
updated: 2026-07-14
---

# History of Artificial Intelligence

TL;DR: AI's history spans from ancient myths of automata through 1950s–60s foundational programs (Logic Theorist, Perceptron, Dartmouth Project), expert-systems boom and bust (1970s–80s), neural network revival, and today's LLM era. Nils Nilsson's 707-page history (Cambridge, 2010) is the canonical insider account, written by a 50-year participant.

## Structure of the field (per Nilsson)

Nilsson defines AI as "that activity devoted to making machines intelligent, and intelligence is that quality that enables an entity to function appropriately and with foresight in its environment." The history is organized into eight chronological parts [^src1]:

| Period | Part | Content |
|---|---|---|
| Antiquity – 1950 | I: Beginnings | Dreams, logic, neural theory, early computers |
| 1950s–60s | II: Early Explorations | Dartmouth project, perceptrons, GPS, early NLP |
| Mid-1960s–mid-1970s | III: Efflorescence | Computer vision, Shakey robot, STRIPS planning |
| 1970s–early 1980s | IV: Applications | Speech recognition, expert systems (MYCIN, PROSPECTOR) |
| 1980s | V: New Generation | Japanese 5th Gen, DARPA Strategic Computing |
| 1980s–90s | VI: Entr'acte | AI winter, controversies, alternative paradigms |
| 1980s onward | VII: Armamentarium | Bayesian networks, ML (decision trees, neural nets, RL) |
| Present | VIII: Modern AI | Chess, driverless cars, ubiquitous AI, toward HLAI |

## Key historical milestones (TOC-derived)

**Beginnings**: Ramon Llull's Ars Magna (~1300) as mechanical reasoning device. Hobbes' "artificial animal" (1651). Da Vinci's robot knight (~1495). Philosophical and biological clues to intelligence — neurons, evolution, automata, and the computer [^src1].

**Dreams and Dreamers (Ch. 1)**: Ancient automata myths — Homer's self-propelled tripods, Pygmalion's Galatea, Aristotle's conditional vision of automation enabling a slaveless society. Hobbes as "patriarch of artificial intelligence" (per George Dyson) [^src1].

**1950s–60s**: Dartmouth Summer Project (1956, coined "artificial intelligence"). Perceptrons (Rosenblatt). Logic Theorist and General Problem Solver (Newell & Simon). Game-playing programs. Semantic networks. Early NLP and machine translation.

**1970s–80s**: Expert systems (MYCIN for medical diagnosis, PROSPECTOR for geology). Shakey robot at SRI + A* search + STRIPS planner. Speech understanding (DARPA SUR program). Dendral project (chemistry). AI winter: combinatorial explosion limits, funding cuts.

**1980s–present**: Neural network revival (backprop, NETtalk, ALVINN). Reinforcement learning (TD-Gammon). Bayesian networks. Statistical NLP. Deep learning era. Driverless cars. LLMs.

## Notable systems (historical)

- **Logic Theorist (1956)**: first heuristic AI program, proved 38 theorems from Principia Mathematica
- **GPS (General Problem Solver)**: means-ends analysis; goal/subgoal decomposition
- **Shakey (SRI, ~1966–72)**: first mobile robot with planning; pioneered A* search and STRIPS
- **MYCIN (1970s)**: expert system for bacterial infections; ~600 rules; performed at specialist level
- **TD-Gammon (1992)**: first RL system to reach expert backgammon play via self-play

## AI winter (Ch. 24)

Nilsson documents the "speed bumps" — Dreyfus's "What Computers Can't Do," Lighthill report (UK), DARPA cuts — driven by: combinatorial explosion (problems scale exponentially), Minsky-Papert critique of perceptrons, and overpromising. Recovery came through specialization (expert systems), then statistical methods [^src1].

## Relation to corpus pages

- [/ai-engineering/nils-nilsson.md](/ai-engineering/nils-nilsson.md) — book author; 50-year AI participant at SRI/Stanford
- [/ai-engineering/machine-learning.md](/ai-engineering/machine-learning.md) — ML as a subdiscipline of AI
- [/ai-engineering/neural-network.md](/ai-engineering/neural-network.md) — perceptrons through deep learning; historical arc
- [/ai-engineering/ai-fundamentals.md](/ai-engineering/ai-fundamentals.md) — what AI is; the field's goals
- [/ai-engineering/README.md](/ai-engineering/README.md) — domain hub

---

[^src1]: [The Quest for Artificial Intelligence — Part 1 (TOC, Preface, Ch. 1)](../../raw/pdf/pdf-the-quest-for-artificial-intelligence-a-history-of-part-01.md), Nils Nilsson (Stanford/Cambridge, 2010)
