---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/youtube-M-NTwkM3VwM-local-ai-agents-in-26-minutes.md
    channel: youtube
    ingested_at: 2026-06-26
  - path: raw/youtube/youtube-iRew6HOY0ho-paperclip-agent-collab-made-easy.md
    channel: youtube
    ingested_at: 2026-06-26
  - path: raw/youtube/youtube-S_oN3vlzpMw-how-ai-agents-claude-skills-work-clearly-explained.md
    channel: youtube
    ingested_at: 2026-06-26
  - path: raw/youtube/youtube-fgr6Sm-dmmM-i-replaced-openclaw-with-perplexity-computer.md
    channel: youtube
    ingested_at: 2026-06-27
aliases:
  - OpenClaw
  - open claw
  - OpenCloud
  - NemoClaw
  - Cloud Hub
  - cloud hub
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-26
updated: 2026-06-26
---

# OpenClaw

**TL;DR**: OpenClaw is an open-source [[ai-engineering/local-ai-agents|local AI agent]] framework — software you run on your own machine to stand up one or more always-on agents that take actions, hold persistent memory, use tools/skills, and run on a schedule [^src1]. It is the open, maximally-customizable end of the local-agent spectrum; Anthropic's [[ai-engineering/claude-cowork|Claude Cowork]] is the safer, no-code counterpart [^src1]. A separate project, [[ai-engineering/paperclip|Paperclip]], exists specifically to *manage* a fleet of OpenClaw agents through a project-management UI [^src2].

## What it is

OpenClaw runs locally and gives each agent the standard local-agent anatomy: a communication channel (Telegram, Discord, etc.), a model "brain," a file-based memory layer, tools/skills, and a heartbeat/cron for scheduled runs [^src1] [05:28](../../raw/youtube/youtube-M-NTwkM3VwM-local-ai-agents-in-26-minutes.md#t=5:28). Because it is open source, practitioners fork it and build their own features on top [^src2] [08:18](../../raw/youtube/youtube-iRew6HOY0ho-paperclip-agent-collab-made-easy.md#t=8:18). See [[ai-engineering/local-ai-agents|Local AI Agents]] for the full anatomy this page instantiates.

## Multi-model routing (cost optimization)

A key OpenClaw pattern is assigning a *different model per agent* to control cost [^src1]. In one production setup [^src1] [15:01](../../raw/youtube/youtube-M-NTwkM3VwM-local-ai-agents-in-26-minutes.md#t=15:01):

| Agent role | Model | Why |
|---|---|---|
| Chief of staff (central brain) | Claude Sonnet 4.6 | Balanced reasoning for coordination |
| Builder/coder | Claude Opus 4.6 **+** Qwen Coder 2.5 (local) | Opus for planning/architecture; route *mechanical* coding to the free local model |
| System monitor | Ministral 3B (local) | Tiny free local model for twice-daily health checks |

Routing the "more mechanical coding tasks" to a locally-hosted open-source model is "a way to optimize cost, because Claude Opus is really expensive to be running all the time" [^src1]. This mirrors the planner-Opus / worker-Sonnet specialization in [[ai-engineering/multi-agent-systems|Multi-Agent Systems]].

## Cloud Hub (skill marketplace) and its security risk

OpenClaw has **Cloud Hub**, a marketplace where users share downloadable skills [^src1] [17:51](../../raw/youtube/youtube-M-NTwkM3VwM-local-ai-agents-in-26-minutes.md#t=17:51). The documented practitioner stance is *not* to download skills directly from it — "there was this whole like security risk and scam situation through Cloud Hub previously" — except from highly trusted developers (the example given is founder Pete Steinberger) [^src1]. The safer pattern: take a skill you like, hand it to Claude, and have Claude **scan it and rewrite it itself** before giving it to your local agent [^src1] [13:09](../../raw/youtube/youtube-M-NTwkM3VwM-local-ai-agents-in-26-minutes.md#t=13:09). This is the same "don't install third-party skills wholesale" discipline covered in [[ai-engineering/agent-skills|Agent Skills]] and [[ai-engineering/agent-security|Agent Security]].

## Mission Control (visual monitoring)

A custom **Mission Control** tool gives a visual "agent office" — a live view of every agent and what it is working on, plus tabs for tasks, scheduled jobs, an activity log, and current projects [^src1] [14:05](../../raw/youtube/youtube-M-NTwkM3VwM-local-ai-agents-in-26-minutes.md#t=14:05). The monitoring problem it solves — *seeing why an agent is stuck or spinning its wheels* — is the same gap that motivated [[ai-engineering/paperclip|Paperclip]] [^src2].

## Running it: hardware and isolation

OpenClaw is run on a dedicated machine rather than a primary work laptop, both for 24/7 uptime and for security isolation — e.g. a wiped old MacBook Pro (16 GB RAM, Cloud models only) or a Mac Mini/Mac Studio with enough RAM to host larger open-source models locally [^src1] [04:05](../../raw/youtube/youtube-M-NTwkM3VwM-local-ai-agents-in-26-minutes.md#t=4:05). See [[ai-engineering/local-ai-agents|Local AI Agents]] (§ where it lives) and [[mlops/vps-for-agents|VPS for Agents]] for the hosting trade-offs.

## OpenClaw in practice (sponsor-vetting agent)

A second practitioner (Ras Mic) corroborates the framework and adds an isolation pattern: he runs an OpenClaw agent with **its own email**, deliberately *not* connected to his real inbox "because there's like attack vectors and I've been hacked before"; he forwards sponsor emails to it for it to check every 15 minutes [^src3] [07:17](../../raw/youtube/youtube-S_oN3vlzpMw-how-ai-agents-claude-skills-work-clearly-explained.md#t=7:17). This is the same scoped-email isolation [[ai-engineering/local-ai-agents|Local AI Agents]] and [[ai-engineering/agent-security|Agent Security]] recommend.

The first version — told only to "research the sponsor and tell me if they're worth it" — rubber-stamped every email ("legit, legit, perfect") with no real research, because the agent had no step-by-step workflow to mimic [^src3] [07:45](../../raw/youtube/youtube-S_oN3vlzpMw-how-ai-agents-claude-skills-work-clearly-explained.md#t=7:45). The fix is the **recursive skill-from-failure loop**: when the agent fails, ask it what error it hit, feed that failure back, then "update the skill so this doesn't happen again" — ~5 iterations produced a flawless 8-data-source report generator [^src3] [22:08](../../raw/youtube/youtube-S_oN3vlzpMw-how-ai-agents-claude-skills-work-clearly-explained.md#t=22:08). The general discipline is in [[ai-engineering/agent-skills|Agent Skills]].

OpenClaw exposes a **memory layer** the agent uses to "do the right thing" given proper context [^src3] [13:09](../../raw/youtube/youtube-S_oN3vlzpMw-how-ai-agents-claude-skills-work-clearly-explained.md#t=13:09). The sub-agent advice mirrors Paperclip's *scale-for-productivity-not-for-looks*: start with **one main agent**, add sub-agents only once you have working skills/workflows — this practitioner ended with sub-agents for marketing, business, and personal, each with its own skills and context [^src3] [25:50](../../raw/youtube/youtube-S_oN3vlzpMw-how-ai-agents-claude-skills-work-clearly-explained.md#t=25:50).

## OpenClaw vs Perplexity Computer

A practitioner comparison identified a clear use-case boundary between OpenClaw and [[ai-engineering/perplexity-computer|Perplexity Computer]] (a cloud-native AI agent product) [^src4]:

| Dimension | OpenClaw | Perplexity Computer |
|---|---|---|
| Setup | Self-hosted, requires VPS + Docker | Zero setup, cloud-native |
| Customization | Maximally customizable (any model, any skill) | Constrained to Perplexity's connector set |
| Best for | Repeatable business automations | One-off complex research tasks |
| Cost model | API costs only, no platform fee | $200/month Max plan (10K credits) |

The use-case split: OpenClaw for automation workflows you run repeatedly; Perplexity Computer for ad hoc, complex multi-angle research that benefits from parallel sub-agents and zero-setup convenience [^src4].

## Reliability and community positioning

Practitioners who switched from OpenClaw to [[ai-engineering/hermes|Hermes]] (a competing harness) cite OpenClaw's historically unstable releases as the main reason — "breaking updates" without warning [^src9 via hermes comparison]. The OpenClaw creator counter is that the project's open-source nature allows community forks and customization that closed-source alternatives can't match.

> Note: Hermes-vs-OpenClaw comparisons are from Hermes practitioners, not OpenClaw maintainers.

## Relationship to other tools

- **[[ai-engineering/paperclip|Paperclip]]** — a project-management layer that connects and orchestrates existing OpenClaw agents (and can create new ones) [^src2].
- **[[ai-engineering/claude-cowork|Claude Cowork]]** — Anthropic's local-agent product; "a lot safer and a lot easier to use," no-code, but you "get locked into Anthropic's system" with less customization [^src1] [20:09](../../raw/youtube/youtube-M-NTwkM3VwM-local-ai-agents-in-26-minutes.md#t=20:09). Many practitioners run OpenClaw and Cowork side by side for different use cases [^src1].
- **[[ai-engineering/perplexity-computer|Perplexity Computer]]** — cloud-native alternative; better for one-off complex tasks; see comparison above [^src4].

## See also

- [[ai-engineering/local-ai-agents|Local AI Agents]] — the category and anatomy
- [[ai-engineering/paperclip|Paperclip]] — fleet management for OpenClaw agents
- [[ai-engineering/multi-agent-systems|Multi-Agent Systems]] — agent teams and per-agent model routing
- [[ai-engineering/agent-security|Agent Security]] — skill-marketplace attack surface, isolation
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [Local AI Agents In 26 Minutes](../../raw/youtube/youtube-M-NTwkM3VwM-local-ai-agents-in-26-minutes.md) — Tina Huang, YouTube
[^src2]: [Paperclip: Agent Collab Made Easy](../../raw/youtube/youtube-iRew6HOY0ho-paperclip-agent-collab-made-easy.md) — The Next New Thing, YouTube
[^src3]: [How AI agents & Claude skills work (Clearly Explained)](../../raw/youtube/youtube-S_oN3vlzpMw-how-ai-agents-claude-skills-work-clearly-explained.md) — Greg Isenberg × Ras Mic, YouTube
[^src4]: [I Replaced OpenClaw with Perplexity Computer](../../raw/youtube/youtube-fgr6Sm-dmmM-i-replaced-openclaw-with-perplexity-computer.md) — Tech With Tim, YouTube
