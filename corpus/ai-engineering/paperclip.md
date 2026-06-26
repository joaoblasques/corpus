---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/youtube-iRew6HOY0ho-paperclip-agent-collab-made-easy.md
    channel: youtube
    ingested_at: 2026-06-26
aliases:
  - Paperclip
  - Paperclip agent
  - Proof
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-26
updated: 2026-06-26
---

# Paperclip

**TL;DR**: Paperclip is an open-source, project-management-style control plane for running a team of AI agents — it lets you manage existing [[ai-engineering/openclaw|OpenClaw]] agents (or create new ones) and supervise the whole system the way you'd manage a human team, while only being pulled in when an agent is genuinely stuck [^src1]. Its design goal is software that is *both* agent- and human-friendly, so a human team can see what the agents are doing without the operator having to babysit every run [^src1].

## The problem it solves

When agents are run through ad-hoc threads (e.g. Slack), "it's hard for you to tell why they're failing" — an agent hits a rate limit or an API error and simply stops responding, pulling the human back in to diagnose [^src1] [02:19](../../raw/youtube/youtube-iRew6HOY0ho-paperclip-agent-collab-made-easy.md#t=2:19). Paperclip makes agent work *visible* in a shared backend so blockers surface explicitly instead of as silent stalls [^src1] [00:00](../../raw/youtube/youtube-iRew6HOY0ho-paperclip-agent-collab-made-easy.md#t=0:00). This is the same observability gap [[ai-engineering/openclaw|OpenClaw]]'s Mission Control addresses.

## How it works

**Goal → issues decomposition.** When you set up a company you give it a top-level goal (e.g. "grow Amazon to 250k a month"); Paperclip breaks the goal into projects and concrete **issues** (tasks) that agents pick up [^src1] [02:47](../../raw/youtube/youtube-iRew6HOY0ho-paperclip-agent-collab-made-easy.md#t=2:47). You can also feed it raw inputs — e.g. an Ahrefs SEO CSV — and it generates the issues from that file, then routes technical fixes to an engineer agent and content edits to a writer agent [^src1] [04:12](../../raw/youtube/youtube-iRew6HOY0ho-paperclip-agent-collab-made-easy.md#t=4:12).

**Org chart of agents.** Agents are organized like an org chart with named roles (engineer, writer, etc.). A practitioner deliberately **fired half the agents** after realizing fewer, better-structured agents avoided rate limiting — "if you were just more efficient... you don't need like 10, so I'm starting with less and then I'll see what breaks" [^src1] [07:23](../../raw/youtube/youtube-iRew6HOY0ho-paperclip-agent-collab-made-easy.md#t=7:23). This echoes the *scale-for-productivity-not-for-looks* principle in [[ai-engineering/multi-agent-systems|Multi-Agent Systems]].

**Chief-of-staff agent.** A dedicated manager agent ("Knox") runs at the start and end of each day to check for blockers, so the human "doesn't want to manage the agents" directly [^src1] [06:30](../../raw/youtube/youtube-iRew6HOY0ho-paperclip-agent-collab-made-easy.md#t=6:30). This is the [[ai-engineering/multi-agent-systems|supervisor/coordinator]] pattern made into a standing role.

**Blocked status + autonomy log.** Agents surface a **blocked** status when they lack access to a tool (e.g. "needs OpenAI image generation and I need to give her the API," or missing Cloudflare DNS access); the chief-of-staff records these in an **autonomy log**, and the operator either grants increased API access or does the step manually [^src1] [06:55](../../raw/youtube/youtube-iRew6HOY0ho-paperclip-agent-collab-made-easy.md#t=6:55). Granting "always allow"-style increased access for trusted actions trades supervision for autonomy — see [[ai-engineering/agent-security|Agent Security]].

## Open source and extensible

Paperclip is **open source**, so it keeps shipping new features and can be forked and customized to a company's needs — "I've forked it and now been building some stuff of my own on it... that's what's different from any of the other [PM tools]" [^src1] [08:18](../../raw/youtube/youtube-iRew6HOY0ho-paperclip-agent-collab-made-easy.md#t=8:18). The framing for a fully-automated business: it's built for "zero human companies" where you are the board rather than the CEO, and the CEO is itself an agent [^src1] [10:10](../../raw/youtube/youtube-iRew6HOY0ho-paperclip-agent-collab-made-easy.md#t=10:10).

## Why not Notion?

The source contrasts Paperclip with general PM tools (Notion, "mission control"): agents struggled with Notion's commenting system (it needed API access *and* a real email address for the agent to read comments — "kludgy"), whereas Paperclip is built for human-and-agent collaboration from the start and, being open source, stays adaptable [^src1] [08:18](../../raw/youtube/youtube-iRew6HOY0ho-paperclip-agent-collab-made-easy.md#t=8:18). A related tool, **Proof**, is positioned as "Google Docs for people *and* agents" — a document surface agents can collaborate on directly [^src1] [01:46](../../raw/youtube/youtube-iRew6HOY0ho-paperclip-agent-collab-made-easy.md#t=1:46).

## See also

- [[ai-engineering/openclaw|OpenClaw]] — the local-agent framework Paperclip manages
- [[ai-engineering/local-ai-agents|Local AI Agents]] — the broader category
- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] — org-chart/supervisor patterns; scale-for-productivity
- [[ai-engineering/agent-ui|Agent UI]] — shells for supervising agent work
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [Paperclip: Agent Collab Made Easy](../../raw/youtube/youtube-iRew6HOY0ho-paperclip-agent-collab-made-easy.md) — The Next New Thing, YouTube (presented by Zapier)
