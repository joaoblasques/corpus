---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-i-didn-t-become-a-developer-to-review-ai-slop-3177eebf.md
    channel: web
    ingested_at: 2026-08-15
aliases:
  - AI PR review debt
  - AI slop review
  - developer review bottleneck
  - trust questions
  - AI coding velocity
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-15
updated: 2026-08-15
url: https://www.builder.io/blog/developers-drowning-in-ai-prs
origin: obsidian-list
---

# I Didn't Become a Developer to Review AI Slop

**TL;DR** — AI code generation creates a trust gap: generation outpaces review capacity, AI PRs sit longer in queues, and the developer's role shifts from builder to validator — using high-value judgment on low-value "is this correct?" checks. The issue is structural, not behavioral.[^src1]

## The trust gap

"AI made it effortless for anyone on my team (and yours) to create code, but it didn't make that code trustworthy."[^src1]

Stack Overflow 2025 Developer Survey: most common AI frustration = output that's "almost right, but not quite." Sonar 2026 State of Code: 96% of developers don't fully trust AI-generated code; 38% say reviewing it takes more effort than reviewing human-written code.[^src1]

LinearB 2026: AI PRs sit waiting 4.6× longer for review and get rejected more than human-written ones. METR study: early-2025 AI tools made experienced open-source developers 19% *slower*, partly because "real work includes style, tests, docs, and review — not just typing."[^src1]

## The role shift

"Everyone else gets to accomplish more than they've ever done before... You as a developer just experience the hype as incoming review debt."[^src1]

"The workflow is spending your judgment terribly. It's taking the scarcest resource in the system — experienced engineering attention — and aiming it at mystery diffs, bloated patches, missing context, and generated code that only looks correct."[^src1]

## Trust questions vs. syntax questions

The questions that still land on developers are trust questions, not syntax questions:[^src1]
- Did this code actually fix the stated problem?
- Did the author understand the system, or is this creating tech debt?
- Is the diff bigger than it needs to be?
- Does this fix silently break another flow?
- Does the UI work in real browsers for real users?
- Will this fix survive past a demo?
- Is this a fix to the root problem or a bandaid?
- Is this security tradeoff acceptable?

These require judgment, context, and accountability — none of which the generating agent has.

## Expanded authorship compounds the problem

"PMs will prototype the feature they've been trying to explain for three sprints... Designers will tweak UX flows and fix layouts... Marketers will update landing pages." The PR queue includes non-engineers generating production code without the institutional knowledge to know what's safe.[^src1]

## See also

- [AI Governance Gap source](/ai-engineering/sources/ai-governance-rate-do-you-know-7dcfcc93.md)
- [Agent Evaluation](/ai-engineering/agent-evaluation.md)
- [Agentic Coding](/ai-engineering/agentic-coding.md)

---

[^src1]: [I Didn't Become a Developer to Review AI Slop](../../../raw/web/web-i-didn-t-become-a-developer-to-review-ai-slop-3177eebf.md) — Builder.io blog, 2026-06-29
