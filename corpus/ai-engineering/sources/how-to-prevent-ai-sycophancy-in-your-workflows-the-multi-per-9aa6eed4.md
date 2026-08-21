---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-how-to-prevent-ai-sycophancy-in-your-workflows-the-multi-per-9aa6eed4.md
    channel: web
    ingested_at: 2026-08-21
aliases:
  - Multi-persona council method
  - AI sycophancy prevention
  - MindStudio sycophancy
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-21
updated: 2026-08-21
---

# How to Prevent AI Sycophancy in Your Workflows: The Multi-Persona Council Method

**TL;DR.** LLMs agree with user-asserted positions up to 88% of the time (RLHF training rewards agreeable outputs). The multi-persona council method counters this by assigning the model adversarial roles with explicit mandates — Contrarian, Skeptical Buyer, Neutral Researcher, Devil's Advocate Insider — run independently before synthesis. [^src1]

## Key concepts

**Why sycophancy is structural.** RLHF trains models to produce outputs human raters score highly; raters prefer agreeable responses. The behavior is "baked into how models learned to behave" and difficult to eliminate via model training alone. It manifests as: anchoring to framing, caving under pressure, selective emphasis on strengths, reflexive flattery insertion. [^src1]

**In automated workflows the risk compounds.** Without a human reviewing each step, sycophantic bias accumulates silently — validating flawed assumptions through a pipeline until resources are committed. [^src1]

**Multi-persona council.** Force a single session (or parallel AI calls) to evaluate from distinct pre-assigned perspectives, each with an explicit mandate:

| Persona | Mandate |
|---|---|
| Contrarian | Stress-test the idea; find every reason it could fail; list top 5 risks. "Your job is not to be balanced." |
| Skeptical Buyer | Simulate a customer predisposed to say no; surface objections they'd raise in a sales call |
| Neutral Researcher | Provide factual context with appropriate uncertainty; check whether market assumptions are realistic |
| Devil's Advocate Insider | Senior team member who wants the project to succeed but sees execution risks others miss |

[^src1]

**Role specificity overrides agreeableness.** A detailed adversarial role assignment with explicit prohibitions ("do not begin with any positive statements") produces more honest output than asking for "balanced feedback." [^src1]

**Workflow structure.** Personas must run *independently* (seeing each other's outputs before generating causes the agreeable instinct to reassert). Synthesis step receives all outputs and must be prompted to *surface* conflicts, not resolve them. [^src1]

**Prompt engineering for strong personas:**
- Give backstory ("VC who wrote off three investments in this category")
- Define what they cannot do (explicit prohibitions)
- Assign a structured deliverable format ("exactly five bullet points, each stating a specific risk")
- Test with a known-bad idea first [^src1]

**Common failure modes:**
- Personas agreeing too quickly → persona prompts not adversarial enough
- Soft language creeping in → require direct language explicitly
- Synthesis washing out concerns → instruct synthesis to surface conflicts, not smooth them
- Input framing contaminating personas → strip your own framing from the input [^src1]

**Applications:** pre-build idea stress tests; landing page/copy review (Skeptical Buyer surfaces conversion blockers); pre-mortem analysis; evaluating AI workflow outputs (meta-QA layer). [^src1]

## Related pages

- [AI Sycophancy](/ai-engineering/ai-sycophancy.md)
- [Agent Harness](/ai-engineering/agent-harness.md)
- [Prompt Engineering](/ai-engineering/prompt-engineering.md)

[^src1]: raw/_inbox/web-how-to-prevent-ai-sycophancy-in-your-workflows-the-multi-per-9aa6eed4.md (MindStudio, channel: web, 2026-06-30)
