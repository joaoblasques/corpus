---
type: entity
domain: software-engineering
status: stub
sources:
  - path: raw/github/github-usertour-usertour.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - Usertour
  - user onboarding
  - product tours
  - in-app tours
  - Appcues alternative
  - Userflow alternative
  - user onboarding platform
tags:
  - corpus/software-engineering
  - entity
created: 2026-06-25
updated: 2026-06-25
---

# Usertour

**TL;DR**: Usertour (★2,054) is an open-source user onboarding platform built with TypeScript. It lets teams create in-app product tours, checklists, and surveys in minutes. Positioned as an open-source alternative to Appcues, Userflow, Userpilot, and Chameleon — self-hostable via Docker Compose [^src1].

## Key capabilities

- **Product tours**: step-by-step in-app walkthroughs with tooltips and overlays
- **Checklists**: onboarding task lists with completion tracking
- **Surveys and NPS**: in-app survey collection
- **Announcements**: banner/modal style in-app messaging [^src1]

## Self-hosting

Deploy with Docker Compose [^src1]:

```bash
cp .env.example .env   # configure required env vars
docker compose up -d
```

Available at `http://localhost:8011`. Full docs: docs.usertour.io [^src1].

Latest release: v0.8.5. Topics: appcues, chameleon, checklist, in-app, nps, onboarding, pendo, surveys, tooltips, tour, userflow, userpilot, walkme [^src1].

## Positioning

Commercial alternatives (Appcues, Userflow, Intercom Tours) are expensive SaaS. Usertour offers full control with self-hosting and no per-seat pricing. Trade-off: requires infrastructure management [^src1].

## See also

- [[software-engineering/kan|Kan]] — another open-source alternative to a commercial SaaS product (Trello replacement)
- [[software-engineering/insforge|InsForge]] — open-source backend toolkit for similar self-hosted infrastructure stacks

---

[^src1]: [usertour (usertour/usertour)](../../raw/github/github-usertour-usertour.md)
