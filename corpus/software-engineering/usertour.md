---
type: entity
domain: software-engineering
status: draft
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
updated: 2026-07-19
---

# Usertour

**TL;DR**: Usertour (★2,054) is an open-source user onboarding platform built with TypeScript. It lets teams "create in-app product tours, checklists, and surveys in minutes—effortlessly and with full control" [^src1]. Positioned as a self-hostable alternative to Appcues, Userflow, Userpilot, Userguiding, Chameleon, and WalkMe.

## Key capabilities

### Onboarding flows
- **Product tours**: step-by-step in-app walkthroughs with tooltips, overlays, and multi-page support [^src1]
- **Checklists**: onboarding task lists with completion tracking [^src1]
- **Launchers**: entry points to trigger flows on demand [^src1]
- **Surveys and NPS**: in-app survey collection [^src1]
- **Announcements**: banner/modal-style in-app messaging [^src1]

### Targeting and integration
- **Framework-agnostic**: "if your app runs in a browser, it seamlessly integrates with Usertour" [^src1]
- **Multi-page app support**: works across single-page and multi-page applications [^src1]
- **Advanced user targeting**: define custom user attributes and track events to segment audiences [^src1]

### Professional workflow features
- **Multiple environments**: manage Production, Staging, and other environments within one account [^src1]
- **Version tracking**: monitors every flow change — who made adjustments and when [^src1]
- **Fully customizable appearance**: adjust text, button colors, font family, and size; supports multiple themes per flow [^src1]

### Analytics
- **Performance metrics**: track views and completion rates per flow [^src1]
- **Drop-off identification**: pinpoint steps causing user confusion or abandonment [^src1]

## Self-hosting

Deploy with Docker Compose [^src1]:

```bash
cp .env.example .env   # configure required env vars
docker compose up -d
```

Available at `http://localhost:8011`. One-click Railway deployment also available [^src1]. Full docs: docs.usertour.io [^src1].

Latest release: v0.8.5.

## Positioning

Usertour positions itself against the full spectrum of commercial onboarding SaaS tools: Appcues, Userpilot, Userflow, Userguiding, Chameleon, Pendo, and WalkMe [^src1]. The self-hosted model provides full control without per-seat SaaS pricing; the trade-off is infrastructure management. The free pricing tier is advertised on the project badge [^src1].

## See also

- [Kan](/software-engineering/kan.md) — another open-source alternative to a commercial SaaS product (Trello replacement)
- [InsForge](/software-engineering/insforge.md) — open-source backend toolkit for similar self-hosted infrastructure stacks

---

[^src1]: [usertour (usertour/usertour)](../../raw/github/github-usertour-usertour.md)
