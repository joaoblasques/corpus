---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/email/email-2026-05-27-how-i-use-hermes-as-a-lead-developer.md
    channel: email
    ingested_at: 2026-06-16
aliases:
  - Hermes
  - Hermes agent
  - Hermes coding agent
tags:
  - corpus/ai-engineering
  - entity
created: 2026-06-16
updated: 2026-06-21
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

> [Thin source — a sponsored newsletter outlining a video walkthrough; deeper Hermes capabilities are not yet captured. Expand when a primary source is ingested.]

## See also

- [[ai-engineering/agent-ui|Agent UI]] — operating agents through chat/messaging interfaces
- [[ai-engineering/agent-harness|Agent Harness]] — the harness around a coding agent
- [[ai-engineering/agentic-coding|Agentic Coding]] — delegating coding work to agents
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [How I use Hermes as a Lead Developer (ZazenCodes)](../../raw/email/email-2026-05-27-how-i-use-hermes-as-a-lead-developer.md)
