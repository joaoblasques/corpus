---
type: entity
domain: software-engineering
status: draft
sources:
  - path: raw/github/github-kanbn-kan.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - Kan
  - kan.bn
  - open-source Trello
  - kanban board
tags:
  - corpus/software-engineering
  - entity
created: 2026-06-25
updated: 2026-07-12
---

# Kan

**TL;DR**: Open-source Trello alternative for project management (★5,049). TypeScript full-stack app using Next.js, tRPC, Drizzle ORM, Better Auth, Tailwind CSS, Zod, and Turborepo monorepo architecture. AGPLv3 licensed, self-hostable via Docker or Railway [^src1].

## What it is

Kan is a kanban-style project management tool positioned as "the open-source project management alternative to Trello" [^src1]. It runs as a SaaS web app (kan.bn) and is fully self-hostable.

Core features [^src1]:
- **Board Visibility** — control who can view and edit boards
- **Workspace Members** — invite members and collaborate
- **Trello Imports** — import existing Trello boards
- **Labels & Filters** — organise and find cards quickly
- **Comments** — discuss on cards
- **Activity Log** — track all card changes with detailed history
- **Templates** — reusable custom board templates
- **Integrations** — listed as coming soon on the roadmap

## Tech stack

Built with [^src1]:
- **Next.js** — React fullstack framework
- **tRPC** — type-safe API layer (no separate REST/GraphQL spec)
- **Drizzle ORM** — TypeScript-first ORM
- **Better Auth** — authentication
- **Tailwind CSS** — utility-first styling
- **Zod** — schema validation
- **React Email** — transactional email rendering
- **Turborepo** — monorepo build tooling

The tRPC + Drizzle + Zod + Next.js combination enforces end-to-end type safety from the database schema through API layer to the UI, without a separate API specification document.

## Self-hosting

Two supported paths [^src1]:

**Railway (one-click):** official template maintained in partnership with Railway; recommended for minimal setup.

**Docker Compose:** ships a `docker-compose.yml` with three services — `postgres` (Postgres 15), `migrate` (runs Drizzle migrations on startup), and `web` (the Next.js app). The `migrate` service must complete before `web` starts; this is enforced via `depends_on` with `condition: service_completed_successfully`. App defaults to port 3000.

Key environment variables required: `POSTGRES_URL`, `BETTER_AUTH_SECRET`, `NEXT_PUBLIC_BASE_URL` [^src1].

## Local development

Uses `pnpm` as the package manager. Standard workflow: clone → `pnpm install` → copy `.env.example` → `pnpm db:migrate` → `pnpm dev` [^src1].

## Metadata

- **Language**: TypeScript
- **License**: AGPLv3
- **Stars**: ★5,049 (collected 2026-06-22)
- **Topics**: better-auth, drizzle-orm, nextjs, open-source, tailwindcss, trpc, turborepo, typescript, zod

## See also

- [System Design Fundamentals](/software-engineering/system-design-fundamentals.md) — API design patterns (REST vs tRPC)
- [InsForge](/software-engineering/insforge.md) — another open-source backend dev tool

---

[^src1]: [kanbn/kan (GitHub)](../../raw/github/github-kanbn-kan.md)
