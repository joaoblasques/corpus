---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/How AI agents & Claude skills work (Clearly Explained).md
    channel: youtube
    ingested_at: 2026-06-09
aliases:
  - How AI agents and Claude skills work
  - Ras Mic skills episode
tags:
  - corpus/ai-engineering
  - source
created: 2026-06-09
updated: 2026-06-09
---

# Source: How AI agents & Claude skills work (Clearly Explained)

**Format**: YouTube podcast episode · Greg Isenberg (host) × Ras Mic (guest) · published 2026-04-08
**URL**: https://www.youtube.com/watch?v=S_oN3vlzpMw

**Thesis**: The models are now good enough that the bottleneck has shifted to the *harness, tools, and context* you give them. The highest-leverage move for most people is not big `AGENTS.md`/`CLAUDE.md` files but **building your own skills** through hands-on iteration. "Less is more." [^src1]

This is an opinionated practitioner talk, not a tutorial or paper. Claims below are the guest's positions; where they tension with other corpus sources, the relevant concept page flags it.

## Key claims

| Claim | Timestamp |
|---|---|
| Models are good now (Opus 4.6, GPT 5.4); context + harness now matter more than model choice | [0:33](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md#t=0:50>) |
| Context = "the model assembling information it needs to execute an action"; window = system prompt + AGENTS.md + skills + tools + codebase + conversation | [1:20](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md#t=1:20>) |
| 95% of people don't need an AGENTS.md/CLAUDE.md file; it's re-injected every turn (~7k tokens for a 1k-line file) | [1:41](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md#t=1:41>) |
| Skills use **progressive disclosure**: only name + description in context; body loads on demand | [3:39](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md#t=3:39>) |
| Build skills by walking the agent through the workflow first, then codifying the successful run | [9:17](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md#t=9:17>) |
| LLMs don't think — they predict tokens; treat agents like new employees | [10:15](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md#t=10:15>) |
| Don't download others' skills (security + missing successful-run context) | [12:34](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md#t=12:34>) |
| Scale for productivity, not for looks: start with one agent, add sub-agents only once skills exist | [14:00](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md#t=14:33>) |
| "Code itself has become context" → tech-stack instructions are mostly unnecessary; templates as context will have a renaissance | [19:26](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md#t=19:26>) |
| Recursively improve a skill from its own failures ("update the skill so this doesn't happen again"); ~5 loops for a robust report generator | [20:52](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md#t=20:52>) |
| The model "gets dumb" as the window fills; keep usage roughly between baseline (~10%) and ~70% | [29:43](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md#t=31:23>) |

## Where it routes in the corpus

- [[ai-engineering/agent-skills|Agent Skills]] — new concept page (progressive disclosure, recursive building, don't-download)
- [[ai-engineering/context-window-management|Context Window Management]] — window-fill degradation, token efficiency
- [[ai-engineering/context-engineering|Context Engineering]] — "less is more"; code-as-context; supply unique workflow not general knowledge
- [[ai-engineering/ai-agent|AI Agent]] — token-predictor mental model; agents-as-new-employees
- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] — one-agent-first → sub-agents for productivity

## See also

- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [How AI agents & Claude skills work (Clearly Explained)](<../../raw/youtube/How AI agents & Claude skills work (Clearly Explained).md>) — Greg Isenberg × Ras Mic, YouTube
