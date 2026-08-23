---
type: source
domain: software-engineering
status: draft
aliases: []
tags:
  - corpus/software-engineering
  - open-source
  - compliance
  - github
  - supply-chain
sources:
  - path: raw/_inbox/web-how-github-maintains-compliance-for-open-source-dependencies-99e81580.md
    channel: web
    title: "How GitHub maintains compliance for open source dependencies"
    url: https://github.blog/enterprise-software/governance-and-compliance/how-github-maintains-compliance-for-open-source-dependencies/
confidence: 0.85
last_confirmed: 2026-08-23
created: 2026-08-23
updated: 2026-08-23
---

# Source: How GitHub Maintains Compliance for Open Source Dependencies

**URL**: https://github.blog/enterprise-software/governance-and-compliance/how-github-maintains-compliance-for-open-source-dependencies/
**Authors**: Jeff (GitHub OSPO), Eric (GitHub PM, supply chain security)
**Collected**: 2026-07-01

## Summary

GitHub blog post describing how GitHub's own OSPO uses the GitHub License Compliance feature (part of GitHub Advanced Security) to manage open source license compliance across thousands of dependencies. Covers rollout strategy, workflow, and policy mechanics.

## Key claims

- Non-compliance risk: "costly litigation and reputational damage."[^src]
- Seed policy with common permissive licenses: MIT, Apache 2.0, BSD-3-Clause.[^src]
- Rollout: use Evaluate mode first (annotations only, no blocking) → switch to Active mode after developers are trained.[^src]
- Two decision dimensions at approval time: permit the license OR the package; enterprise scope OR repository scope.[^src]
- Wildcard package exceptions supported (e.g., `@github-ui/*` namespace approved in bulk).[^src]
- Emergency break-glass override: toggle a custom property to disable enforcement temporarily. Used once in practice.[^src]
- Policy team covers multiple time zones; triages most requests within hours.[^src]
- Feature is GA for GitHub Enterprise Cloud customers with an active GHAS Code Security license.[^src]

## Corpus pages produced

- [/software-engineering/open-source-license-compliance.md](/software-engineering/open-source-license-compliance.md) — concept page

---

[^src]: raw/_inbox/web-how-github-maintains-compliance-for-open-source-dependencies-99e81580.md
