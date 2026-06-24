---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/anthropic.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/web/claude-101.md
    channel: web
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-06-03-claude-101.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-05-29-claude-opus-4-8-arrives.md
    channel: email
    ingested_at: 2026-06-12
  - path: raw/email/email-2026-05-06-certified.md
    channel: email
    ingested_at: 2026-06-17
  - path: raw/_inbox/web-claude-legal-solutions-claude-by-anthropic.md
    channel: web
    ingested_at: 2026-06-24
  - path: raw/_inbox/web-enhancing-ai-driven-defense-with-anthropics-claude-opus-4-7.md
    channel: web
    ingested_at: 2026-06-24
aliases:
  - Anthropic
  - Anthropic PBC
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-12
updated: 2026-06-24
---

# Anthropic

**TL;DR.** Anthropic PBC is the AI lab behind the Claude model family and the [[ai-engineering/claude-code|Claude Code]] / [[ai-engineering/claude-cowork|Claude Cowork]] products [^src1]. As of mid-2026 it reportedly closed a ~$65B round at a ~$965B valuation, passing OpenAI for the first time [^src4]. The Claude lineup (Haiku → Sonnet → Opus → Fable/Mythos) and per-model specifics live on [[ai-engineering/claude-models|Claude Model Lineup]]; product specifics live on the Claude Code and Cowork pages.

## Learning resources

`claude101.com` is a free collection of guides covering Claude basics, Cowork, Skills, "Claude to sound like you", certifications, and avoiding AI-speak — a recap of which guides to read and in what order [^src2][^src3].

**Anthropic Academy** hosts official, free certifications via a Skilljar LMS (`anthropic.skilljar.com`); these are the only Anthropic-issued Claude certificates — viral paid "Claude Certifications" sold elsewhere are scams Anthropic does not endorse [^src5]. Three certificates [^src5]:
- **Claude 101** (~1 hr) — what Claude is, when to use Chat vs Cowork vs Code, how Projects and Skills work, connecting Gmail/Drive/Slack.
- **AI Fluency: Framework & Foundations** (~3 hr, 13 lessons) — the **4Ds** of working with AI: *Delegation, Description, Discernment, Diligence*; effective prompting, critical thinking about outputs, and ethics. Ships a vocabulary cheat sheet.
- **Introduction to Claude Cowork** (~2 hr) — what Cowork is, Projects, Plugins, Skills, scheduling tasks, file/document handling, permissions, and picking the right model.

The framing is a low-cost career signal: a certificate shows a hiring viewer you have "actually touched the tool." The source cites the Stanford 2025 AI Index (78% of organizations used AI in 2024, up from 55% the year before) and a PwC finding that AI-skilled workers command a ~56% average wage premium (up from 25%) [^src5] — see [[ai-business/technical-career|Navigating a Technical Career]].

## Project Glasswing (April 2026)

Project Glasswing is Anthropic's AI-powered security initiative, announced April 7 2026, using Mythos Preview to find critical vulnerabilities in widely-deployed software [^src6]. Anthropic deployed Mythos Preview autonomously against real codebases and found "thousands of 0-days" in critical software that could have been exploited by malicious actors [^src6].

Key elements:
- **$100M in credits** — issued to the security research community so defenders (not just attackers) can access frontier AI for security work.
- **Major tech coalition** — participating organizations include companies across software, hardware, and cloud infrastructure.
- **Claude Security product** — an enterprise-grade vulnerability scanning tool using Opus 4.7 to analyze codebases the way a security researcher would; see [[ai-engineering/agent-security|Agent Security]].
- **Cyber Verification Program** — a vetting process for security researchers and companies to access frontier Claude models for legitimate offensive security work.

Security partners embedding Claude for their platforms: CrowdStrike (Falcon + Project QuiltWorks), SentinelOne (Wayfinder), TrendAI (AESIR), Microsoft Security, Palo Alto Networks (Unit 42 / Frontier AI Defense [^src8]), Wiz (Red Agent — 150K+ assets scanned/week, 0 false positives [^src6]) [^src6].

## Claude for Legal

A dedicated product suite for legal professionals, available on Team and Enterprise plans [^src7]:
- **Practice area plugins**: Commercial Legal, Corporate Legal, IP, Litigation, Employment, Privacy, Regulatory, AI Governance, and more
- **Connectors**: iManage, NetDocuments (document management); Docusign, Ironclad (contract lifecycle); Thomson Reuters (legal research); Box/Intralinks (deal rooms)
- **Microsoft integration**: Claude for Word (draft, redline, summarize) and Outlook (correspondence, contract review)
- **Extensible**: custom skills and connectors for firm-specific workflows

Legal professionals became the most engaged Claude Cowork user segment after the first plugin release [^src7]. See [[ai-engineering/claude-cowork|Claude Cowork]] §Legal vertical for the connector and plugin inventory.

## Interpretability initiative

Anthropic's mechanistic interpretability research aims to produce an "MRI for AI" — tools capable of auditing a model's reasoning for honesty, correctness, and alignment before deployment [^src9]. Key milestone: ~30 million distinct features discovered in Claude 3 Sonnet using sparse autoencoders. Target: working interpretability audit tools by 2027. See [[ai-engineering/interpretability|Interpretability]] for the full scientific background.

## See also

- [[ai-engineering/claude-models|Claude Model Lineup]] — the Claude model family (Haiku → Sonnet → Opus → Fable/Mythos), specs, and per-model detail
- [[ai-engineering/claude-code|Claude Code]] — Anthropic's CLI coding agent
- [[ai-engineering/claude-cowork|Claude Cowork]] — desktop product for non-developers
- [[ai-engineering/interpretability|Interpretability]] — mechanistic interpretability research program
- [[ai-engineering/agent-security|Agent Security]] — Project Glasswing, Claude Security product
- [[ai-engineering/llm|LLM]], [[ai-engineering/claude-api|Claude API]]

[^src1]: [Anthropic (YouTube footer stub)](../../raw/web/anthropic.md)
[^src2]: [Claude 101](../../raw/web/claude-101.md)
[^src3]: [Claude 101 (email)](../../raw/email/email-2026-06-03-claude-101.md)
[^src4]: [Claude Opus 4.8 arrives (The Code)](../../raw/email/email-2026-05-29-claude-opus-4-8-arrives.md)
[^src5]: [Certified. (Ruben Hassid)](../../raw/email/email-2026-05-06-certified.md)
[^src6]: [Project Glasswing: Securing Critical Software for the AI Era](../../raw/web/web-project-glasswing-securing-critical-software-for-the-ai-era.md) — Anthropic
[^src7]: [Claude Legal Solutions](../../raw/_inbox/web-claude-legal-solutions-claude-by-anthropic.md) — Anthropic
[^src8]: [Enhancing AI-Driven Defense with Anthropic's Claude Opus 4.7](../../raw/_inbox/web-enhancing-ai-driven-defense-with-anthropics-claude-opus-4-7.md) — Palo Alto Networks
[^src9]: [Dario Amodei: The Urgency of Interpretability](../../raw/web/web-dario-amodei-the-urgency-of-interpretability.md) — Dario Amodei, Anthropic
