---
type: entity
domain: software-engineering
status: stub
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
updated: 2026-06-25
---

# Kan

**TL;DR**: Open-source Trello alternative for project management (★5,049). TypeScript full-stack app using Next.js, tRPC, Drizzle ORM, Better Auth, Tailwind CSS, Zod, and Turborepo monorepo architecture [^src1].

## What it is

A kanban board SaaS app with board visibility controls, workspace collaboration, Trello import, labels/filters, card comments, activity log, and templates [^src1]. AGPLv3 licensed. Live at kan.bn.

## Tech stack

Built with [^src1]:
- **Next.js** — React fullstack framework
- **tRPC** — type-safe API layer (no separate REST/GraphQL spec)
- **Drizzle ORM** — TypeScript-first ORM
- **Better Auth** — authentication
- **Tailwind CSS** — utility-first styling
- **Zod** — schema validation
- **Turborepo** — monorepo build tooling

This stack (tRPC + Drizzle + Zod + Next.js) is a common modern TypeScript fullstack pattern — type safety all the way from DB schema to UI.

## See also

- [[software-engineering/system-design-fundamentals|System Design Fundamentals]] — API design patterns (REST vs tRPC)
- [[software-engineering/insforge|InsForge]] — another open-source backend dev tool

---

[^src1]: [kanbn/kan (GitHub)](../../raw/github/github-kanbn-kan.md)
