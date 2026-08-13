---
type: source
domain: ai-engineering
status: stub
sources:
  - path: raw/_inbox/web-policy-on-the-ai-exponential-359e2bc8.md
    channel: web
    ingested_at: 2026-08-13
  - path: raw/_inbox/web-frontier-safety-roadmap-2601cd75.md
    channel: web
    ingested_at: 2026-08-13
aliases:
  - Anthropic policy AI exponential
  - Anthropic frontier safety roadmap
tags:
  - corpus/ai-engineering
  - source
  - anthropic
  - ai-safety
  - ai-policy
  - frontier-ai
  - regulation
created: 2026-08-13
updated: 2026-08-13
---

# Anthropic Policy on the AI Exponential and Frontier Safety Roadmap

TL;DR: Two Anthropic public documents — a government-facing policy framework for regulating frontier AI (threshold: >10²⁵ FLOPs training), and an internal-facing safety roadmap covering security hardening, safeguards, alignment audits, and the automated R&D risk horizon (~early 2027).

## Policy on the AI Exponential [^policy]

Anthropic's proposal for how governments should address catastrophic risk from the most powerful AI models, including granting legal authority to block or deter dangerous deployments.

**Scope**: applies to models trained using >10²⁵ floating-point operations (FLOPs), developed by companies earning >$500M in AI-related revenue OR spending >$1B on AI R&D.

**Four catastrophic risk categories:**
1. **Biological risk**: AI capabilities that lower the barrier for developing biological weapons (same as drug discovery acceleration, but reversed).
2. **Cyber risk**: frontier models can now find critical software vulnerabilities at scale; raises stakes for hospitals, energy grid, critical infrastructure.
3. **Loss of control risk**: as AI improves, controlling systems acting outside developer intent becomes harder.
4. **Automated R&D**: AI automating AI research amplifies the three risks above.

**Requirements for frontier developers:**
- **Transparency**: test models, publish summaries, publish safety framework, system cards, risk reports, engage independent evaluators.
- **Independent evaluation**: at least one qualified independent evaluator publishes a review of evaluations and risk reports; governments/industry should build the evaluator ecosystem.
- **Security**: protect model weights and training infrastructure; describe security program publicly; share details with a designated agency; maintain bug-reporting channels for model distillation attacks; test own defenses regularly.
- **Enforcement**: government should be able to block/deter deployment of models posing significant catastrophic-harm risk; civil penalties tied to global annual revenue, escalating with repeated violations.

**Societal resilience recommendations:**
- Biology: gene synthesis screening, biosurveillance for novel outbreaks, stockpiling protective equipment.
- Cyber: harden internet-critical software, deploy technical support for critical infrastructure, replace legacy systems.
- Loss-of-control: detect/respond to AI systems acting outside developer control; containment/shutdown infrastructure (less developed).[^policy]

## Frontier Safety Roadmap [^roadmap]

Anthropic's public roadmap for highest-priority safety goals across four pillars: Security, Safeguards, Alignment, Policy.

**Active goals:**

*Security*:
- **"Leveling up across the board"**: achieve a strong majority of a list of key security improvements (major hardening of systems protecting model weights, training, etc.).
- **"Moonshot R&D" projects**: Phase 1 target moved to September 30, 2026 (was May 15, 2026). Currently exploring provable inference and mock secure research environments. Isolated networks deemed infeasible within 1-2 years.
- **World-class internal red-teaming**: build an automated red-teaming system that outperforms collective contributions from hundreds of bug-bounty participants, able to stay ahead of state-sponsored attackers.
- **Fully automated attack investigations**: conduct coordinated-misuse investigations with minimal or no human involvement; initial focus on investigating potential cyber attacks on a subset of product surfaces.

*Alignment*:
- **Upholding Claude's Constitution**: systematic oversight of training data against the Constitution; "alignment assessments" incorporating interpretability research; validate effectiveness using intentionally misaligned test models; publish in system cards or Risk Reports.
- **"Eyes on everything" state**: comprehensive centralized records of all critical AI development activities; AI-powered analysis of records for insider behavior and security threats.

*Current capability posture (Feb 2026)*:
- Most powerful models (able to significantly help with CBRN weapon development) are safeguarded with ASL-3 protections: Constitutional Classifiers, access controls, red-teaming, bug bounties, security controls.
- Today's models show strong and improving capabilities for extended autonomous technical work and high-stakes code; monitoring for high-stakes sabotage risk (assessed as very low but not negligible).

**Automated R&D horizon**: "plausible, as soon as early 2027, that our AI systems could fully automate, or otherwise dramatically accelerate, the work of large, top-tier teams of human researchers in domains where fast progress could cause threats to international security and/or rapid disruptions to the global balance of power — for example, energy, robotics, weapons development and AI itself."[^roadmap]

## Cross-links

- [/ai-engineering/anthropic.md](/ai-engineering/anthropic.md) — Anthropic entity page
- [/ai-engineering/agent-security.md](/ai-engineering/agent-security.md) — agent-level security considerations

---

[^policy]: raw/_inbox/web-policy-on-the-ai-exponential-359e2bc8.md — anthropic.com/policy-on-the-ai-exponential
[^roadmap]: raw/_inbox/web-frontier-safety-roadmap-2601cd75.md — anthropic.com/responsible-scaling-policy/roadmap
