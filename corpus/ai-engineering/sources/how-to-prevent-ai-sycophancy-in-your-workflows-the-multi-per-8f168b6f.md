---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/web-how-to-prevent-ai-sycophancy-in-your-workflows-the-multi-per-8f168b6f.md
    channel: web
    ingested_at: 2026-08-22
aliases:
  - AI sycophancy prevention v2
  - multi-persona council MindStudio
tags:
  - corpus/ai-engineering
  - source
  - sycophancy
  - prompt-engineering
  - multi-persona
created: 2026-08-22
updated: 2026-08-22
---

# How to Prevent AI Sycophancy: The Multi-Persona Council Method (v2)

**TL;DR.** Second MindStudio source corroborating the [AI Sycophancy](/ai-engineering/ai-sycophancy.md) concept page. Adds detail on the four failure patterns and a systematic multi-persona council prompt engineering approach. [^msp1]

## Four sycophancy patterns (named taxonomy)

1. **Position reversal** — model shifts analysis to match a user's stated opinion
2. **Hollow validation** — model highlights positives and glosses over problems
3. **Confidence inflation** — model sounds more certain than warranted, mirrors user's apparent confidence
4. **False balance** — model backs down from factual claims when user pushes back, conflates disagreement with error

"None of these are obvious failures. That's what makes them dangerous." [^msp1]

## Multi-persona council prompt engineering

Assign distinct adversarial roles that explicitly override agreeableness bias:

- **Contrarian**: challenges every assumption
- **Skeptical Buyer**: finds reasons not to believe/buy
- **Neutral Researcher**: evidence only, no opinion
- **Devil's Advocate**: steelmans the opposing view

Key technique: personas need explicit *permission to disagree* in the prompt. Weak persona: "You are a critical thinker." Strong persona: "You are a Devil's Advocate. Your job is to find flaws in every argument presented to you. Do not agree with the user, even if they are right." [^msp1]

## Why personas must override RLHF defaults

Without explicit disagreement permission, even a "critical" persona defaults to the trained agreeableness behavior. The persona prompt must create a higher-weight instruction that overrides RLHF default. [^msp1]

> **See also:** [/ai-engineering/ai-sycophancy.md](/ai-engineering/ai-sycophancy.md) for the full concept page. This source corroborates and adds the named four-pattern taxonomy.

[^msp1]: MindStudio Blog, "How to Prevent AI Sycophancy in Your Workflows: The Multi-Persona Council Method," mindstudio.ai, 2026-06-30. `raw/_inbox/web-how-to-prevent-ai-sycophancy-in-your-workflows-the-multi-per-8f168b6f.md`
