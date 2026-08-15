---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-how-to-make-ai-agents-follow-your-design-system-d7698d8e.md
    channel: web
    ingested_at: 2026-08-15
aliases:
  - AI agent design system compliance
  - prose loses to code
  - ESLint for agents
  - agent codebase drift
  - agent lint rules
tags:
  - corpus/ai-engineering
  - source
created: 2026-08-15
updated: 2026-08-15
url: https://www.builder.io/blog/how-to-make-ai-agents-follow-your-design-system
origin: obsidian-list
---

# How to Make AI Agents Follow Your Design System

**TL;DR** — Agents don't violate design systems out of negligence — they infer rules from the codebase, and brownfield codebases contain more legacy patterns than canonical ones. Prose rules files lose to code examples. The fix: make wrong paths mechanically impossible (compile errors, linter rules) rather than instructionally discouraged.[^src1]

## Why agents drift

"The agent looked at my repo and correctly inferred what I do. What I do, unfortunately, is far from what I say I do."[^src1]

- Long rules files degrade: "Models pay less attention to instructions buried in the middle of a large context window."[^src1]
- Models weight examples over instructions: "When an agent writes a new component, it searches the workspace for similar components and patterns on what it finds. If your rules file says 'always use semantic tokens' and the three nearest files use inline hex values, the hex values win."[^src1]
- **"Your codebase is your prompt."** If five ways to write a form exist in the repo, the agent has five design systems to pick from.[^src1]

## The solution: make wrong paths fail mechanically

"Rules stay as slim as possible and point to code. Code teaches the agent best practices. Deterministic checks constrain code outputs and let the agent iterate until it's right."[^src1]

**Import restrictions via ESLint**: Make `components/legacy/` an import error, not a prose warning. Agents run linters in a loop — lint errors land in stderr, which becomes a repair instruction. "A lint error is, in effect, the only kind of rule the model cannot skim past."[^src1]

The error message field doubles as a prompt — "they get read more often by models than by people now."[^src1]

**Brownfield compromise**: Run strict rules only on files changed in the current branch (`lint-staged` or pre-commit hook), or keep a second config (`.eslintrc.agent.json`) with warnings escalated to errors as a required step in the agent's verification loop. "Yes, that second option means agents are held to stricter rules than humans. That asymmetry bothered me at first."[^src1]

**Typed component interfaces**: Loose interfaces invite hallucination. Tight discriminated unions (TypeScript) force the agent to select a valid variant rather than invent one.[^src1]

## Key takeaway

"Each individual fix on a PR like this is small, which is what makes the cost easy to miss... But agents generate PRs faster than humans do, so the overhead scales with their output, not yours."[^src1]

The governance gap compounds: once a reviewer approves a legacy import, that approval sets a precedent for the next reviewer. Design systems erode without an explicit decision to abandon them — tooling simply stopped enforcing them.[^src1]

## See also

- [Agent UI](/ai-engineering/agent-ui.md)
- [Agentic Coding](/ai-engineering/agentic-coding.md)
- [AI Governance source](/ai-engineering/sources/ai-governance-rate-do-you-know-7dcfcc93.md)

---

[^src1]: [How to Make AI Agents Follow Your Design System](../../../raw/web/web-how-to-make-ai-agents-follow-your-design-system-d7698d8e.md) — Builder.io blog, 2026-06-29
