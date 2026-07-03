---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/youtube-IiZ5HRaeX4s-stop-watching-tutorials-build-these-4-claude-projects-to-10x.md
    channel: youtube
    ingested_at: 2026-06-15
aliases:
  - internal operating system
  - board of advisers
  - niche command center
  - 4 Claude projects
  - improve-system skill
tags:
  - corpus/ai-engineering
  - source
created: 2026-06-15
updated: 2026-06-15
---

# Source: Build These 4 Claude Projects (Internal Operating System)

**What it is**: A hands-on pattern (Austin Marchese) for building a personal "internal operating system" on Claude Code through four projects, whether technical or not [^src1]. The standout is project four — a self-improving file system — which maps directly onto the LLM-Wiki / corpus pattern this repo implements.

## The four projects

1. **Board of advisers** — clone experts by ingesting their public content (e.g. YouTube), then an `ask-the-board` **skill** loops every board member for one combined answer [^src1].
2. **Niche command center** — build a personal tool for a problem you actually have today; "you'll actually use it, you skip the hardest part (finding the right problem), zero audience pressure" [^src1].
3. **AI-optimized public profile** — a personal site with an "ask AI about me" block, on the thesis that people increasingly go to AI first to learn about a person [^src1].
4. **Internal operating system** — the unifying file system (below).

## The internal operating system (project 4)

Three folders + a root `CLAUDE.md` "brain" that tells Claude how to use them [^src1]:
- **Knowledge** — everything Claude should know (notes, voice samples, frameworks, saved articles).
- **Skills** — repeatable processes (e.g. `ask-the-board`).
- **Projects** — what you're actively working on.

Two maintenance skills make it compound [^src1]:
- **`/improve-system`** — captures feedback into the system so the next output is better (e.g. after editing a verbose email draft, run it and future drafts come out concise). "The most important part of the whole process."
- **`ingest-resource`** — systematically brings in articles/transcripts/videos and files them in the right place ("a librarian for the AI brain").

Put it on **GitHub** to version and share it [^src1]. The author notes this builds on Andrej Karpathy's own version of the pattern.

## Why it's filed

This is the most direct external articulation of the **LLM-Wiki / compounding-knowledge-base** pattern that this corpus itself implements — knowledge + skills + an ingest loop + an improve loop, all in version control. It corroborates [Agent Skills](/ai-engineering/agent-skills.md) (skills as reusable processes), [CLAUDE.md Conventions](/ai-engineering/claude-md-conventions.md) (the root brain file), and [Agent Harness](/ai-engineering/agent-harness.md) (the self-improvement ratchet).

## See also

- [Agent Skills](/ai-engineering/agent-skills.md) · [CLAUDE.md Conventions](/ai-engineering/claude-md-conventions.md) · [Agent Harness](/ai-engineering/agent-harness.md)
- [Vibe Coding](/ai-engineering/vibe-coding.md) — the build-MVP-then-iterate loop
- [AI Engineering hub](/ai-engineering/README.md)

---

[^src1]: [Stop Watching Tutorials — Build These 4 Claude Projects to 10x Output](../../../raw/youtube/youtube-IiZ5HRaeX4s-stop-watching-tutorials-build-these-4-claude-projects-to-10x.md) — Austin Marchese
