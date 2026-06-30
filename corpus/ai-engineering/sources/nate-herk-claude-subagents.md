---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/_inbox/youtube-e18sdZLwP7o-how-to-build-claude-subagents-better-than-99-of-people.md
    channel: youtube
    ingested_at: 2026-06-30
tags:
  - corpus/ai-engineering
  - source
created: 2026-06-30
updated: 2026-06-30
---

# How to Build Claude Subagents (Nate Herk)

**Source**: [How to Build Claude Subagents — Better Than 99% of People](../../raw/_inbox/youtube-e18sdZLwP7o-how-to-build-claude-subagents-better-than-99-of-people.md) — Nate Herk, YouTube, 2026.

**Summary**: Practitioner deep-dive on Claude Code custom sub-agents — file format, YAML front matter fields, progressive disclosure mechanics, sub-agents vs skills distinction, model routing, dynamic workflows, and security hardening. Primary source for [[ai-engineering/claude-subagents|Claude Sub-Agents]].

## Key claims

- Sub-agents = `.claude/agents/<name>.md` files; same markdown format as skills but execution is isolated (clean context, separate model possible, parallel) [^src1]
- The `description:` YAML field is the routing trigger; Claude reads only front matter to decide if a sub-agent applies (progressive disclosure) [^src1]
- Model routing: assign `model: claude-haiku-4-5-20251001` to workers to reduce cost; Opus orchestrates, Haiku executes [^src1]
- `ultracode` trigger on Opus 4.8: spawns 40–210 parallel sub-agents for large-scale tasks [^src1]
- Security: `tools:` whitelist > prompting — a sub-agent with only `[read, grep]` literally cannot write files regardless of prompt injection [^src1]
- Sub-agents cannot talk to each other (orchestrator ↔ sub-agent is one-to-one) [^src1]
- Community repo: "Awesome-Claude-Code-Subagents" on GitHub [^src1]

## Pages populated

- [[ai-engineering/claude-subagents|Claude Sub-Agents]] — primary: full concept page
- [[ai-engineering/agent-skills|Agent Skills]] — updated with sub-agents vs skills distinction

---

[^src1]: [How to Build Claude Subagents — Better Than 99% of People](../../raw/_inbox/youtube-e18sdZLwP7o-how-to-build-claude-subagents-better-than-99-of-people.md) — Nate Herk, YouTube, 2026
