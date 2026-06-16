---
type: entity
domain: ai-engineering
status: stub
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
updated: 2026-06-16
---

# Hermes (coding agent)

**TL;DR.** Hermes is a self-hosted AI coding agent you run on your own server and drive remotely over chat — the pitch is using it as a "lead developer" from your phone: host it on a VPS so it stays available, connect it to GitHub, and message it through Telegram to edit and ship code while away from your computer [^src1].

> Not to be confused with the React Native/Expo **Hermes** JavaScript engine referenced in [[ai-engineering/agent-security|Agent Security]] — unrelated tool, same name.

## Setup and architecture

As described in a sponsored walkthrough [^src1]:

- **Runs on a VPS in Docker** (Docker Compose) so it stays online independent of your laptop; you SSH in and can enter the container to inspect Hermes data and environment files.
- **Controlled via Telegram** — create a bot with BotFather and chat with the agent; you watch its commands and skills execute in the chat thread.
- **Connected to GitHub**, using **GitHub Actions** to deploy code changes.
- The **model provider is configurable**.
- The source demonstrates a one-click deploy via Hostinger (the video's sponsor) and a live demo building a personal website from mobile — adding a blog, generating sample content and an image [^src1].

This is a **remote, chat-driven agent harness** — the same "operate a coding agent through a messaging UI" pattern discussed in [[ai-engineering/agent-ui|Agent UI]], applied to a phone-first, always-on deployment. See also [[ai-engineering/agent-harness|Agent Harness]] and [[ai-engineering/agentic-coding|Agentic Coding]].

> [Thin source — a sponsored newsletter outlining a video walkthrough; deeper Hermes capabilities are not yet captured. Expand when a primary source is ingested.]

## See also

- [[ai-engineering/agent-ui|Agent UI]] — operating agents through chat/messaging interfaces
- [[ai-engineering/agent-harness|Agent Harness]] — the harness around a coding agent
- [[ai-engineering/README|AI Engineering hub]]

---

[^src1]: [How I use Hermes as a Lead Developer (ZazenCodes)](../../raw/email/email-2026-05-27-how-i-use-hermes-as-a-lead-developer.md)
