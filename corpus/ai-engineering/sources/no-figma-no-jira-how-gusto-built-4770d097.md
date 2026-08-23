---
type: source
domain: ai-engineering
status: complete
sources:
  - path: raw/_inbox/web-no-figma-no-jira-no-docs-how-gusto-built-a-new-product-line-4770d097.md
    channel: web
    ingested_at: 2026-08-23
aliases:
  - Gusto Cofounder build story
  - Eddie Kim Lenny's Newsletter
  - No Figma No Jira Gusto
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-23
updated: 2026-08-23
---

# No Figma. No Jira. No Docs. How Gusto Built a New Product Line (Lenny's Newsletter, 2026-06-30)

**Source**: lennysnewsletter.com — `raw/_inbox/web-no-figma-no-jira-no-docs-how-gusto-built-a-new-product-line-4770d097.md`

## Summary

Eddie Kim (Gusto CTO) describes building Gusto Cofounder — a net-new AI product for small businesses — in 10 weeks with 3 engineers and 1 designer, using a radically stripped-down process. [^1]

## Team and timeline

- 5 people total: Eddie Kim (CTO, coding), 3 engineers, 1 designer
- 10 weeks from zero code to tier-one launch
- No PM, no Jira, no Figma
- "Perma-Zoom" replaced standups, retros, and Slack for 10 weeks [^1]

## Key methods

**Trash-can method**: Write a full PR, review it together as a product decision, then delete it. The act of building is the planning document. Replaces design docs and planning meetings. [^1]

**Eval-first workflow**: Fix real customer bugs with Claude Code as the primary way to validate that the system works correctly. Evals drive iteration, not hand-written acceptance criteria. [^1]

**Ship to production from day one**: No staging gates, no separate release cycles. [^1]

## Two-tool agent stack

The complete technical stack behind Gusto Cofounder: [^1]
1. **Claude Code** (Anthropic)
2. **Cloudflare Workers** + **Vercel AI SDK**

No additional orchestration framework. Claude Code is the agent layer; Cloudflare Workers is the execution runtime; Vercel AI SDK provides streaming/structured output primitives. [^1]

## Designer becoming a top engineer

The designer on the team (no prior engineering background) reached the 94th percentile for code shipping using Claude Code. Key enabler: Claude Code handled the mechanical translation of design intent to code. [^1]

## Significance

Demonstrates that a minimal two-tool stack (Claude Code + Cloudflare Workers / Vercel AI SDK) can support a production-quality product launch with a very small, cross-functional team. The process innovations (trash-can method, perma-Zoom, eval-first) may be as significant as the tooling choices.

## Related pages

- [/ai-engineering/agent-harness.md](/ai-engineering/agent-harness.md) — harness patterns; Gusto's two-tool stack is a minimal real-world harness
- [/ai-engineering/claude-code.md](/ai-engineering/claude-code.md)
- [/ai-engineering/vibe-coding.md](/ai-engineering/vibe-coding.md)

[^1]: raw/_inbox/web-no-figma-no-jira-no-docs-how-gusto-built-a-new-product-line-4770d097.md
