---
type: source
domain: ai-engineering
status: draft
sources:
  - path: raw/youtube/youtube-omU3zR3K7-U-the-best-ai-automation-stack-to-learn-in-2026.md
    channel: youtube
    ingested_at: 2026-07-02
aliases: []
tags:
  - corpus/ai-engineering
  - source
  - youtube-quick-intake
created: 2026-07-02
updated: 2026-08-19
provisional: false
youtube_video_id: omU3zR3K7-U
url: https://youtu.be/omU3zR3K7-U
channel_name: Dave Ebbelaar
playlist: AI Engineering
published: 2026-06-19
transcript_status: ok
---

# The Best AI Automation Stack to Learn in 2026

> **Source** (YouTube · Dave Ebbelaar · playlist _AI Engineering_). [watch on YouTube](https://youtu.be/omU3zR3K7-U) · [transcript](../../../raw/youtube/youtube-omU3zR3K7-U-the-best-ai-automation-stack-to-learn-in-2026.md)

## TL;DR

A five-layer stack for production AI automation: Python + FastAPI + Celery (backend), PostgreSQL via Supabase (database), React + Vite + shadcn/ui (frontend), direct LLM API calls (AI layer), Docker + Railway or Hetzner VPS (infrastructure). Framed as a career-oriented roadmap, arguing that jobs require the underlying engineering disciplines, not no-code tool familiarity.

---

## Author context

Dave Ebbelaar holds a bachelor's and master's degree in AI and claims to have "delivered 50 plus custom B2B AI solutions starting as a freelancer then later under an AI agency called Data Luminina."[^transcript-intro] He presents this stack as opinionated, developed over several years of client work across many companies.[^transcript-intro]

[^transcript-intro]: raw/youtube/youtube-omU3zR3K7-U-the-best-ai-automation-stack-to-learn-in-2026.md [01:17–01:43]

---

## Core argument: skills over tools

No-code AI tools (n8n, Zapier, etc.) are not what employers hire for. "Almost no job will list one of these tools as a requirement or prerequisite. They will list actually what's underneath that."[^transcript-jobs] The five-layer stack below represents what's underneath.[^transcript-jobs]

[^transcript-jobs]: raw/youtube/youtube-omU3zR3K7-U-the-best-ai-automation-stack-to-learn-in-2026.md [00:26]

---

## Layer 1 — Backend: Python + FastAPI + Celery

**Python** is the core language. Ebbelaar treats it as the prerequisite for everything else in this stack.[^transcript-python]

**FastAPI** serves as the API layer and entry point for automations — handling webhooks from external triggers and requests from the frontend, exposing GET/POST/PUT/DELETE endpoints.[^transcript-fastapi]

**Celery** handles background workers and scheduled jobs (cron). The described pattern: FastAPI receives trigger-based webhooks; Celery manages all scheduled tasks as Celery tasks. Ebbelaar states it "is really the core engine of my own AI automation system that I use to run my company."[^transcript-celery]

[^transcript-python]: raw/youtube/youtube-omU3zR3K7-U-the-best-ai-automation-stack-to-learn-in-2026.md [01:43–03:01]
[^transcript-fastapi]: raw/youtube/youtube-omU3zR3K7-U-the-best-ai-automation-stack-to-learn-in-2026.md [03:01–03:27]
[^transcript-celery]: raw/youtube/youtube-omU3zR3K7-U-the-best-ai-automation-stack-to-learn-in-2026.md [03:53–04:21]

---

## Layer 2 — Database: PostgreSQL via Supabase

PostgreSQL is presented as sufficient for virtually all scales. Ebbelaar cites Instagram scaling to hundreds of millions of users on Postgres as evidence that most projects will never outgrow it.[^transcript-postgres]

**Supabase** is recommended as a managed wrapper: it adds authentication, an admin GUI, and hosted infrastructure on top of Postgres. Vectors can also be stored in Postgres (pgvector), removing the need for a separate vector database to get started.[^transcript-supabase]

[^transcript-postgres]: raw/youtube/youtube-omU3zR3K7-U-the-best-ai-automation-stack-to-learn-in-2026.md [04:46–05:13]
[^transcript-supabase]: raw/youtube/youtube-omU3zR3K7-U-the-best-ai-automation-stack-to-learn-in-2026.md [05:13–05:39]

---

## Layer 3 — Frontend: React + Vite + shadcn/ui

Not all automations need a frontend, but for dashboards and admin panels the recommended combination is:

- **React** — industry-standard JavaScript component library for UIs.[^transcript-react]
- **Vite** — build tool that runs the dev server and packages the app for deployment.[^transcript-vite]
- **shadcn/ui** — component library where components are copied directly into the project (not kept as a node_modules dependency), making them editable by AI coding agents. Includes graphs, auth forms, menus, and full chat interfaces.[^transcript-shadcn]

Ebbelaar explicitly states that pure frontend development has diminished value: "Just being a front-end developer, like you're cooked. There's no value in that anymore" given AI's ability to generate frontend code — though UX design remains a human concern.[^transcript-frontend-value]

[^transcript-react]: raw/youtube/youtube-omU3zR3K7-U-the-best-ai-automation-stack-to-learn-in-2026.md [07:49]
[^transcript-vite]: raw/youtube/youtube-omU3zR3K7-U-the-best-ai-automation-stack-to-learn-in-2026.md [08:15]
[^transcript-shadcn]: raw/youtube/youtube-omU3zR3K7-U-the-best-ai-automation-stack-to-learn-in-2026.md [08:42–09:07]
[^transcript-frontend-value]: raw/youtube/youtube-omU3zR3K7-U-the-best-ai-automation-stack-to-learn-in-2026.md [09:33]

---

## Layer 4 — AI layer: direct LLM API calls

The AI layer is described as the simplest of the five. LLM capabilities (language models, embedding models, vision, speech-to-text, image generation) are "just one API call away."[^transcript-ai-layer] Ebbelaar argues that no new frameworks or tools are needed — the decades-old engineering layers (API, DB, frontend) are sufficient to integrate LLM calls.

For production/enterprise use, cloud provider endpoints (AWS Bedrock, Azure OpenAI, Google Vertex) are preferred over direct OpenAI/Anthropic calls for centralized billing, data privacy controls, and scale management. The API surface is compatible, so skills transfer directly.[^transcript-enterprise]

[^transcript-ai-layer]: raw/youtube/youtube-omU3zR3K7-U-the-best-ai-automation-stack-to-learn-in-2026.md [10:50–11:16]
[^transcript-enterprise]: raw/youtube/youtube-omU3zR3K7-U-the-best-ai-automation-stack-to-learn-in-2026.md [11:42–12:34]

---

## Layer 5 — Infrastructure: Docker + Railway / Hetzner VPS

Deployment follows a standard containerization approach:

- **Docker / Docker Compose** packages the backend (FastAPI + Celery) and frontend (Vite) as separate services. Supabase cloud is already hosted, so only these two need deployment.[^transcript-docker]
- **Railway** is the recommended beginner path: accepts a Docker Compose repository, has an MCP server for agent-assisted deployment, handles both backend and frontend deployments with minimal configuration.[^transcript-railway]
- **Hetzner VPS** is cited as the agency's three-year production choice for more advanced deployments — a German provider for renting a plain VPS and deploying containers directly.[^transcript-hetzner]
- Large cloud providers (AWS, Azure, GCP) offer managed container services as the enterprise alternative.[^transcript-cloud]

[^transcript-docker]: raw/youtube/youtube-omU3zR3K7-U-the-best-ai-automation-stack-to-learn-in-2026.md [13:27–13:53]
[^transcript-railway]: raw/youtube/youtube-omU3zR3K7-U-the-best-ai-automation-stack-to-learn-in-2026.md [13:53–14:18]
[^transcript-hetzner]: raw/youtube/youtube-omU3zR3K7-U-the-best-ai-automation-stack-to-learn-in-2026.md [14:44–15:11]
[^transcript-cloud]: raw/youtube/youtube-omU3zR3K7-U-the-best-ai-automation-stack-to-learn-in-2026.md [14:44]

---

## Stack summary table

| Layer | Technology | Role |
|---|---|---|
| Backend | Python + FastAPI + Celery | Engine, API entry point, scheduled jobs |
| Database | PostgreSQL (Supabase) | Storage, auth, vectors |
| Frontend | React + Vite + shadcn/ui | Dashboards, admin panels (optional) |
| AI | OpenAI / Anthropic / cloud provider SDKs | LLM/embedding/vision calls |
| Infrastructure | Docker Compose + Railway or Hetzner VPS | Deployment and hosting |

---

## Related corpus pages

- [/ai-engineering/README.md](/ai-engineering/README.md)
