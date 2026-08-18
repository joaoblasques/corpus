---
type: source
domain: ai-engineering
status: draft
aliases:
  - VPS coding Claude Code
  - Pieter Levels VPS workflow
  - cloud coding workflow
  - coding on remote server
sources:
  - path: raw/web/web-i-ve-been-coding-almost-solely-on-my-vps-with-claude-code-fo-19bb6cbf.md
    channel: web
    source_url: https://levels.io/coding-on-vps-with-claude-code-for-a-year
    ingested_at: 2026-08-18
tags:
  - agentic-coding
  - claude-code
  - vps
  - remote-development
created: 2026-08-18
updated: 2026-08-18
---

# Coding on VPS with Claude Code (Pieter Levels)

**TL;DR:** Pieter Levels (@levelsio) has coded almost exclusively on a VPS using Claude Code for ~1 year. Key advantages: no local setup, continuous overnight runs, instant deploy-to-production, device-agnostic.

## Workflow

- Claude Code runs directly on production VPS (live edits to production server)
- No local Nginx/dev environment needed
- Deploy time: ~3 seconds (vs ~1 minute with local → GitHub → pull cycle)
- Works while sleeping — agent continues running overnight
- Device-agnostic: switch from laptop to phone seamlessly

## Trade-offs and caveats

Levels acknowledges this is "crazy" by conventional standards:
- "Only twice in 12 months messed up which meant my site didn't load for 10 seconds"
- Solo workflow caveat: at a company, would recommend staging server instead of production[^1]
- Requires robust backups (3-2-1 backup strategy explicitly mentioned)

## Broader trend

Levels cites @theo and Karpathy moving to cloud/Slack-based AI coding as confirmation this is the direction. Prediction: "AI agents and AI coding will operate on servers / from the cloud first."[^1]

Cross-reference: [Agentic Coding](/ai-engineering/agentic-coding.md) for the broader agentic workflow context; [Claude Code](/ai-engineering/claude-code.md) for Claude Code feature detail.

[^1]: raw/web/web-i-ve-been-coding-almost-solely-on-my-vps-with-claude-code-fo-19bb6cbf.md
