---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/email/email-2026-05-27-how-i-use-hermes-as-a-lead-developer.md
    channel: email
    ingested_at: 2026-06-16
  - path: raw/youtube/youtube-6kGXn-j16QM-7-hermes-desktop-hacks-that-will-change-your-life.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-built-the-best-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-7-hermes-desktop-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-AQHlyGA2cZM-6-hermes-agent-use-cases-i-promise-will-change-your-life.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - Hermes
  - Hermes agent
  - Hermes coding agent
  - Hermes Desktop
  - interview-before-acting
  - pinned sessions
  - remote gateway
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-16
updated: 2026-06-25
---

# Hermes (coding agent)

**TL;DR.** Hermes is an AI coding agent that one developer runs on their own VPS and drives remotely over Telegram chat — the framing is using it as a **"lead developer" from a phone**: host it on a server so it stays available, connect it to GitHub, and message it to edit and ship code while away from your computer [^src1]. The cited source is a sponsored ZazenCodes newsletter introducing a video walkthrough of this setup [^src1].

> Not to be confused with the React Native/Expo **Hermes** JavaScript engine referenced in [[ai-engineering/agent-security|Agent Security]] — unrelated tool, same name.

## The pitch: a lead developer on your phone

The author describes a personal workflow built on three ideas [^src1]:

- **Use Hermes as a "lead developer" from a phone** — delegate coding to the agent rather than doing it directly.
- **Run Hermes on a VPS so it stays available** — keeping the agent online independent of the author's own machine.
- **Chat with it through Telegram while away from your computer** — the messaging app is the interface for issuing work.

The author says they have been using this workflow to build out their personal website [^src1].

## Workflow, stack, and architecture

The stated stack [^src1]:

- **Host Hermes in Docker on a VPS.**
- **Connect it to GitHub.**
- **Use GitHub Actions to deploy code changes.**

Operationally this is a **remote, chat-driven agent harness** — operating a coding agent through a messaging UI, the pattern discussed in [[ai-engineering/agent-ui|Agent UI]], here applied to an always-on, phone-first deployment. See also [[ai-engineering/agent-harness|Agent Harness]] and [[ai-engineering/agentic-coding|Agentic Coding]].

## Setting up Hermes on a VPS

The walkthrough's setup steps [^src1]:

- **Deploy Hermes with Hostinger's one-click flow** — Hostinger is the video's sponsor, offering a one-click deploy.[^src1]
- **Configure the model provider** — the underlying model is a configurable setup step rather than fixed.
- **Create a Telegram bot with BotFather** — the bot is how the user reaches the agent.

## Live demo and publishing from mobile

The video includes a live demo driven entirely from Telegram [^src1]:

- **Ask Hermes to edit the website** from the chat, and **watch its commands and skills run in the chat** thread.
- **Building and publishing from mobile**: get Hermes to **add a blog**, and **generate sample content and an image** for it.

## VPS, Docker, and Hermes layers

For inspecting the running system, the source walks through the deployment layers [^src1]:

- **SSH into the VPS.**
- **Inspect the Docker Compose and environment files.**
- **Enter the container and locate Hermes data.**

> [Thin first source — a sponsored newsletter outlining a video walkthrough of the VPS/Telegram setup. The seven-hack walkthrough below provides deeper Hermes Desktop usage patterns.]

## 7 Hermes Desktop hacks

A walkthrough of advanced workflows using Claude Code Desktop branded as "Hermes Desktop" — seven patterns for power users [^src2]:

**Hack 1 — Interview before acting.** Never let Hermes (Claude Code) start a task immediately. Begin every session with: "Before you start, ask me three clarifying questions about this task." This front-loads ambiguity resolution and prevents the common failure mode of "agent goes off in the wrong direction for 30 minutes" [^src2].

**Hack 2 — Pinned sessions as persistent workspaces.** Instead of opening a new session per task, create named pinned sessions per domain of work (e.g., "Newsletter," "Client Projects," "Dev"). Each pinned session accumulates context and tooling relevant to that domain and stays open indefinitely. Switching between projects means switching sessions, not re-explaining context [^src2].

**Hack 3 — Skills as SOPs.** Encode every recurring workflow as a `SKILL.md` file. The pattern: identify a workflow you explain more than once → record yourself doing it (Loom auto-generates the SOP) → convert to a skill → the next time, type the skill name instead of explaining. "The goal is to have the agent already know how to do it" [^src2]. See [[ai-engineering/agent-skills|Agent Skills]] for the full skill design discipline.

**Hack 4 — Cron jobs for scheduled intelligence.** Use Claude Code routines (or a simple launchd/cron on the server) to run scheduled tasks: daily competitor monitoring, weekly content calendar generation, nightly data pulls. The session runs headlessly; results arrive in email or Slack the next morning [^src2]. See [[ai-engineering/claude-code|Claude Code]] (Routines section) for the routing infrastructure.

**Hack 5 — Webhooks for event-triggered intelligence.** Connect external services (Zapier, n8n, Make.com) to fire a Hermes session on events: a new form submission starts a CRM entry + follow-up email draft; a calendar event ending triggers a meeting summary post [^src2]. The underlying mechanism is the API-triggered routine (see Claude Code § Routines).

**Hack 6 — Specialist agent profiles.** Create named Claude Code sessions with custom system prompts for each recurring specialist need. The documented example is "Nova" — a YouTube content research agent with tools and context scoped only for video research and scripting [^src2]. Switching to Nova means switching to a session where Claude is already a YouTube specialist, not a generalist who needs domain context re-injected. See [[ai-engineering/agent-skills|Agent Skills]] (Specialist agent profiles section).

**Hack 7 — Remote gateway connection.** Run Claude Code on an always-on server (VPS, home server, cloud instance) and connect to it from anywhere via SSH or the Desktop remote-control feature. Benefits: tasks run while the laptop is closed, no context lost when switching devices, and team members can share access to the same running session [^src2]. This is the Desktop-app complement to the VPS/Telegram pattern described above.

> **Key theme across all 7 hacks**: the goal is **removing friction at the point of action** — every hack reduces the gap between "I want this done" and "the agent is doing it." [^src2]

## See also

- [[ai-engineering/agent-ui|Agent UI]] — operating agents through chat/messaging interfaces
- [[ai-engineering/agent-harness|Agent Harness]] — the harness around a coding agent
- [[ai-engineering/agent-skills|Agent Skills]] — skills as SOPs (Hack 3); specialist profiles (Hack 6)
- [[ai-engineering/agentic-coding|Agentic Coding]] — delegating coding work to agents
- [[ai-engineering/README|AI Engineering hub]]

## Hermes use cases: /goal, kanban, research, memory wiki, Tailscale

Advanced Hermes use cases from a practitioner walkthrough [^src4]:

**Meta-prompting via /goal**: the `/goal` command requires meta-prompting to produce useful results. A plain instruction like "create a web app" gives generic output; wrapping it with a meta-prompt that asks Hermes to clarify requirements, research constraints, and draft a specification first produces high-quality task plans [^src4].

**Kanban board**: Hermes manages a kanban-style board (triage → in-progress → done) for tasks. Triage is automated — new tasks go to triage; Hermes auto-assigns priority and moves to in-progress based on urgency heuristics [^src4].

**Technical research via browser control**: Hermes can drive browser research, visiting multiple sources and synthesizing findings. The practitioner used this for competitive analysis (1 hour research time → 10 minutes with Hermes) [^src4].

**Memory wiki** (self-hosted): Hermes maintains a static site as its long-term knowledge store. Each memory is a markdown file; a semantic search index makes retrieval fast. The wiki lives on a VPS or local machine [^src4].

**Tailscale for cross-device memory**: Tailscale connects all user devices so the memory wiki is accessible from phone, laptop, and desktop without public internet exposure. The Tailscale network acts as a private VPN joining the devices into one flat network [^src4].

**Morning priority prompt**: a scheduled morning prompt pulls from the memory wiki, current kanban state, and calendar to produce a daily briefing and priority list. This is the "self-improvement" loop — each briefing session teaches Hermes what matters to the user [^src4].

---

## Hermes as memory injection (the frozen snapshot role)

In the composite memory stack analyzed by one practitioner, Hermes fills the **injection** role [^src3]:

- **Role**: inject a frozen snapshot of relevant knowledge at session start — static, pre-built, cached.
- **Mechanism**: ~1,300 cached tokens loaded at the start of every session. Token cost is negligible once cached; the snapshot doesn't change per-session.
- **Weakness**: keyword-only recall for determining which snapshot chunks to include. If the memory is tagged with keywords and the user doesn't use those keywords, relevant context is missed. Hermes has no semantic/embedding-based recall.
- **Position in the stack**: it sits *after* MemSearch (storage) and *before* GBrain (recall). The snapshot is what gets *injected*; MemSearch captures new things; GBrain re-ranks and cites when answering.

The composite: **MemSearch captures → Hermes snapshot injects → GBrain re-ranks at recall time**. Hermes handles the "what to always have in context" problem; GBrain handles the "what to surface for this specific query" problem [^src3].

This limitation (keyword-only injection) is why the composite stack pairs Hermes with GBrain — GBrain's semantic re-ranking compensates for Hermes's structural weakness at recall [^src3].

[^src1]: [How I use Hermes as a Lead Developer (ZazenCodes)](../../raw/email/email-2026-05-27-how-i-use-hermes-as-a-lead-developer.md)
[^src2]: [7 Hermes Desktop Hacks That Will Change Your Life](../../raw/youtube/youtube-6kGXn-j16QM-7-hermes-desktop-hacks-that-will-change-your-life.md) — YouTube
[^src3]: [I Built The Best Claude Memory System (YouTube)](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-built-the-best-report.md) — composite memory stack analysis
[^src4]: [Hermes use cases: /goal, kanban, memory wiki, Tailscale](../../raw/youtube/youtube-AQHlyGA2cZM-6-hermes-agent-use-cases-i-promise-will-change-your-life.md) — YouTube
