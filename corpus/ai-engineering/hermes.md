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
  - path: raw/_inbox/youtube-EmF06O4vOWI-master-hermes-agent-in-41-mins.md
    channel: youtube
    ingested_at: 2026-06-27
  - path: raw/_inbox/youtube-gb5TlGw6Uks-hermes-agent-zero-to-personal-ai-assistant-1-hour-course.md
    channel: youtube
    ingested_at: 2026-06-27
  - path: raw/_inbox/youtube-cEo95olh2j4-hermes-agent-is-blowing-me-away.md
    channel: youtube
    ingested_at: 2026-06-27
  - path: raw/_inbox/youtube-w4xOiuBQHKA-full-hermes-agent-set-up-for-beginners-in-2026-24-7-ai-agent.md
    channel: youtube
    ingested_at: 2026-06-27
  - path: raw/_inbox/youtube-QQEgIo4Juxg-you-need-to-use-hermes-right-now-goodbye-openclaw.md
    channel: youtube
    ingested_at: 2026-06-27
  - path: raw/_inbox/youtube-zHE434sBw2U-i-gave-my-hermes-agent-a-phone-number-its-crazy.md
    channel: youtube
    ingested_at: 2026-06-27
  - path: raw/_inbox/youtube-y4hiT-j5J24-how-i-use-hermes-as-a-lead-developer.md
    channel: youtube
    ingested_at: 2026-06-29
  - path: raw/_inbox/youtube-mTYxpIRK7xA-hermes-agent-full-course-setup-guide-for-complete-beginners.md
    channel: youtube
    ingested_at: 2026-06-29
  - path: raw/_inbox/youtube-u6L9aedHqZc-hermes-agent-is-crazy-180-000-github-stars.md
    channel: youtube
    ingested_at: 2026-06-29
  - path: raw/_inbox/youtube-yzlvDnxvi1I-the-hermes-agent-briefing-what-it-is-why-it-matters-and-how.md
    channel: youtube
    ingested_at: 2026-06-29
aliases:
  - Hermes
  - Hermes agent
  - Hermes coding agent
  - Hermes Desktop
  - interview-before-acting
  - pinned sessions
  - remote gateway
  - 5 pillars (Hermes)
  - soul.md
  - user.md (Hermes)
  - memory.md (Hermes)
  - Hermes loop
  - Vapi Hermes
  - Nous Research agent
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-16
updated: 2026-06-29
---

# Hermes (coding agent)

**TL;DR.** Hermes is an AI coding agent that one developer runs on their own VPS and drives remotely over Telegram chat — the framing is using it as a **"lead developer" from a phone**: host it on a server so it stays available, connect it to GitHub, and message it to edit and ship code while away from your computer [^src1]. The cited source is a sponsored ZazenCodes newsletter introducing a video walkthrough of this setup [^src1].

> Not to be confused with the React Native/Expo **Hermes** JavaScript engine referenced in [Agent Security](/ai-engineering/agent-security.md) — unrelated tool, same name.

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

Operationally this is a **remote, chat-driven agent harness** — operating a coding agent through a messaging UI, the pattern discussed in [Agent UI](/ai-engineering/agent-ui.md), here applied to an always-on, phone-first deployment. See also [Agent Harness](/ai-engineering/agent-harness.md) and [Agentic Coding](/ai-engineering/agentic-coding.md).

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

**Hack 3 — Skills as SOPs.** Encode every recurring workflow as a `SKILL.md` file. The pattern: identify a workflow you explain more than once → record yourself doing it (Loom auto-generates the SOP) → convert to a skill → the next time, type the skill name instead of explaining. "The goal is to have the agent already know how to do it" [^src2]. See [Agent Skills](/ai-engineering/agent-skills.md) for the full skill design discipline.

**Hack 4 — Cron jobs for scheduled intelligence.** Use Claude Code routines (or a simple launchd/cron on the server) to run scheduled tasks: daily competitor monitoring, weekly content calendar generation, nightly data pulls. The session runs headlessly; results arrive in email or Slack the next morning [^src2]. See [Claude Code](/ai-engineering/claude-code.md) (Routines section) for the routing infrastructure.

**Hack 5 — Webhooks for event-triggered intelligence.** Connect external services (Zapier, n8n, Make.com) to fire a Hermes session on events: a new form submission starts a CRM entry + follow-up email draft; a calendar event ending triggers a meeting summary post [^src2]. The underlying mechanism is the API-triggered routine (see Claude Code § Routines).

**Hack 6 — Specialist agent profiles.** Create named Claude Code sessions with custom system prompts for each recurring specialist need. The documented example is "Nova" — a YouTube content research agent with tools and context scoped only for video research and scripting [^src2]. Switching to Nova means switching to a session where Claude is already a YouTube specialist, not a generalist who needs domain context re-injected. See [Agent Skills](/ai-engineering/agent-skills.md) (Specialist agent profiles section).

**Hack 7 — Remote gateway connection.** Run Claude Code on an always-on server (VPS, home server, cloud instance) and connect to it from anywhere via SSH or the Desktop remote-control feature. Benefits: tasks run while the laptop is closed, no context lost when switching devices, and team members can share access to the same running session [^src2]. This is the Desktop-app complement to the VPS/Telegram pattern described above.

> **Key theme across all 7 hacks**: the goal is **removing friction at the point of action** — every hack reduces the gap between "I want this done" and "the agent is doing it." [^src2]

## See also

- [Agent UI](/ai-engineering/agent-ui.md) — operating agents through chat/messaging interfaces
- [Agent Harness](/ai-engineering/agent-harness.md) — the harness around a coding agent
- [Agent Skills](/ai-engineering/agent-skills.md) — skills as SOPs (Hack 3); specialist profiles (Hack 6)
- [Agentic Coding](/ai-engineering/agentic-coding.md) — delegating coding work to agents
- [AI Engineering hub](/ai-engineering/README.md)

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

## Origin and background

Hermes is an open-source MIT-licensed Python project from **Nous Research** — a research-oriented AI collective known for a hacker-origin-story, Discord community culture, and a dog-food mentality (the team uses Hermes as their primary agent) [^src9]. The key framing: **Hermes is a harness, not the agent itself** — the LLM running inside (Claude, GPT-4o, local models via OpenRouter) is the intelligence; Hermes provides the memory, skills, crons, and orchestration around it [^src9]. This puts it in the same category as [OpenClaw](/ai-engineering/openclaw.md) — a framework you deploy, not a product you subscribe to.

Reliability vs OpenClaw: practitioners switching from OpenClaw to Hermes cite themed releases (no breaking changes without warning), a self-improvement loop that compounds over time, and support for local models (LoRA fine-tuning, Swarms integration) [^src7][^src9].

## The 5 pillars architecture

From a comprehensive 1-hour practitioner course [^src6]:

**1. Memory** — two markdown files always loaded at session start:
- `user.md` — who you are: preferences, communication style, timezone, recurring projects, personal context about you as a person.
- `memory.md` — ongoing state: active projects, business context, tasks-in-flight. Updated immediately as Hermes learns new things (not batched).

Both files inject a frozen snapshot into every session start; the agent always "knows" the user without re-explaining. See [Agent Memory](/ai-engineering/agent-memory.md) for how this compares to RAG-based recall.

**2. Skills** — the same `SKILL.md` format as Claude Code (see [Agent Skills](/ai-engineering/agent-skills.md)). 520+ community skills are available via the Hermes skills hub; 91 are built-in. Hermes auto-creates and auto-patches skills as it learns new workflows from use — the self-improving loop.

**3. soul.md** — personality shaping. Unlike `user.md` (about the user), `soul.md` is about the *agent's* character: tone, communication style, personal identity, how it pushes back. "Honey" (NetworkChuck's wife's nickname for their Hermes instance) is partly a product of soul.md [^src9].

**4. Crons** — natural-language scheduling: "remind me every Tuesday to review my pipeline" becomes a scheduled task. Crons run in isolated sessions — Hermes cannot recursively create crons from inside a cron. They convert Hermes from reactive (waits for prompts) to proactive (acts on schedule) [^src8].

**5. Self-improving loop** — after each task, Hermes reflects and updates its skills and memory accordingly. Pattern: skill → execute → improve. This is why "it starts slow — give it 30 days to become useful" [^src8].

## The Hermes loop

The core execution loop per task [^src8]:

```
Target → Read memory → Read skills → Use tools → Result → Feedback → Improve
```

Persistent memory is written immediately on learning, not at session end. This means partial sessions build memory even if interrupted. The loop makes Hermes progressively more calibrated to the specific user's workflow — a property that neither pure RAG nor static CLAUDE.md achieves, since both are read-only from the agent's perspective [^src8].

## OpenRouter auto-routing (model selection)

Hermes integrates OpenRouter for model routing, applying three heuristics per task [^src5]:

| Task type | Model tier |
|---|---|
| Fast, lightweight (reminders, lookups) | Fast model |
| Cost-sensitive, bulk processing | Cheap model |
| Complex, intensive (research, long-horizon coding) | Expensive model |

"Opus is the best model for AI agents" — the practitioner framing is to spend Opus tokens selectively on the tasks that deserve frontier reasoning; route everything else cheaper [^src9]. This mirrors the planner-Opus / worker-Sonnet split in [Multi-Agent Systems](/ai-engineering/multi-agent-systems.md).

One-line VPS deploy via Open Router Spawn on Google Cloud, AWS, or DigitalOcean [^src5]. Apple Health, calendar, and Gmail integrations available post-setup [^src5].

## Minimax M3: running Hermes at 1/20th the cost

Minimax M3's architecture makes it the cost-optimal model for always-on Hermes deployments [^src13]:

**MSA (Minimax Sparse Attention)**: Normal transformers read every token in context on every inference. MSA checks which parts of the context are relevant and reads only those — skipping the rest. Result: **1 million token context window at 1/20th of the compute** of a normal transformer [^src13].

**Cost**: Minimax M3 at $0.60/$2.40 per 1M tokens (input/output) vs. Opus 4.8 at $5/$25 — approximately 10–20× cheaper. With the $20/month subscription plan: 1.7 billion tokens per month; the $50 plan yields 5.1 billion tokens [^src13]. (Note: video is Minimax-sponsored; treat pricing claims as approximate.)

**Capability**: On SWE-bench Pro, Minimax M3 outperforms Gemini 3.1 Pro and GPT-5.5. On Browse-Comp (directly relevant to Hermes /goal deep research), it is comparable to Opus and GPT-5.5 [^src13].

**Always-on practicality**: "Cheap enough to run 24/7, which makes always-on agents finally possible." Can run for 24+ hours doing up to 2,000 tool calls without human intervention — matching Hermes's /goal long-horizon task pattern [^src13].

Selecting Minimax M3 in Hermes's model picker (or via OpenRouter) routes all Hermes calls there. The subscription key (not API key) unlocks the token-plan pricing. This is the same routing logic as OpenRouter auto-routing (§ above) but with a cost-specific rationale [^src13].

## Vapi phone integration

Hermes can be connected to Vapi to gain phone-call capabilities [^src10]:

| Component | What it provides |
|---|---|
| **Vapi** | Phone numbers (inbound + outbound), voice agent transcription, call routing |
| **Hermes** | Goals, persistent memory, tools, crons, proactive decisions |

Install the Vapi MCP into the running Hermes instance. Hermes then acts as the "brain" — deciding what to say and do — while Vapi handles the voice/telephony layer. Documented performance: **$0.10/min average cost**, **1.15s average latency** [^src10].

[^src1]: [How I use Hermes as a Lead Developer (ZazenCodes)](../../raw/email/email-2026-05-27-how-i-use-hermes-as-a-lead-developer.md)
[^src2]: [7 Hermes Desktop Hacks That Will Change Your Life](../../raw/youtube/youtube-6kGXn-j16QM-7-hermes-desktop-hacks-that-will-change-your-life.md) — YouTube
[^src3]: [I Built The Best Claude Memory System (YouTube)](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-i-built-the-best-report.md) — composite memory stack analysis
[^src4]: [Hermes use cases: /goal, kanban, memory wiki, Tailscale](../../raw/youtube/youtube-AQHlyGA2cZM-6-hermes-agent-use-cases-i-promise-will-change-your-life.md) — YouTube
[^src5]: [Master Hermes Agent in 41 Minutes](../../raw/_inbox/youtube-EmF06O4vOWI-master-hermes-agent-in-41-mins.md) — Keith AI, YouTube
[^src6]: [Hermes Agent: Zero to Personal AI Assistant (1 Hour Course)](../../raw/_inbox/youtube-gb5TlGw6Uks-hermes-agent-zero-to-personal-ai-assistant-1-hour-course.md) — Nate Herk, YouTube
[^src7]: [Hermes Agent Is Blowing Me Away](../../raw/_inbox/youtube-cEo95olh2j4-hermes-agent-is-blowing-me-away.md) — Alex Finn, YouTube
[^src8]: [Full Hermes Agent Set Up for Beginners in 2026 — 24/7 AI Agent](../../raw/_inbox/youtube-w4xOiuBQHKA-full-hermes-agent-set-up-for-beginners-in-2026-24-7-ai-agent.md) — AI Foundations, YouTube
[^src9]: [You Need to Use Hermes RIGHT NOW — Goodbye OpenClaw](../../raw/_inbox/youtube-QQEgIo4Juxg-you-need-to-use-hermes-right-now-goodbye-openclaw.md) — NetworkChuck, YouTube
[^src10]: [I Gave My Hermes Agent a Phone Number — It's Crazy](../../raw/_inbox/youtube-zHE434sBw2U-i-gave-my-hermes-agent-a-phone-number-its-crazy.md) — David Ondrej, YouTube
[^src11]: [How I Use Hermes as a Lead Developer (YouTube)](../../raw/_inbox/youtube-y4hiT-j5J24-how-i-use-hermes-as-a-lead-developer.md) — ZazenCodes, YouTube
[^src12]: [Hermes Agent Full Course — Setup Guide for Complete Beginners](../../raw/_inbox/youtube-mTYxpIRK7xA-hermes-agent-full-course-setup-guide-for-complete-beginners.md) — Tech With Tim, YouTube
[^src13]: [Hermes Agent is Crazy — 180,000+ GitHub Stars](../../raw/_inbox/youtube-u6L9aedHqZc-hermes-agent-is-crazy-180-000-github-stars.md) — David Ondrej, YouTube (sponsored by Minimax)
[^src14]: [The Hermes Agent Briefing — What It Is, Why It Matters, and How to Get Started](../../raw/_inbox/youtube-yzlvDnxvi1I-the-hermes-agent-briefing-what-it-is-why-it-matters-and-how.md) — Dmitri Shapiro (MindStudio CEO), YouTube
