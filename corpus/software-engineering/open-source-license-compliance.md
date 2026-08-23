---
type: concept
domain: software-engineering
status: draft
aliases:
  - open source license compliance
  - license compliance
  - OSPO license review
  - GitHub License Compliance
  - software license policy
tags:
  - corpus/software-engineering
  - open-source
  - compliance
  - licensing
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

# Open Source License Compliance

**TL;DR**: Open source license compliance is the practice of ensuring that third-party dependencies used in a project conform to the organization's license policy. Non-compliance risk includes litigation and reputational damage. GitHub's Advanced Security product offers automated PR-level license checks; GitHub's own OSPO team uses this to manage thousands of dependencies.

## Why it matters

Nearly all software carries a license agreement. The obligations range from attribution-only (MIT, BSD) to copyleft requirements that mandate distributing source code (GPL variants) or restrict commercial use. An organization's acceptable-license policy depends on its business model, distribution strategy, and software ecosystem.[^gh]

Business risk of non-compliance: "costly litigation and reputational damage."[^gh]

Removing a non-compliant dependency after the fact requires engineering effort — catching violations at PR time is substantially cheaper.[^gh]

## GitHub License Compliance (product)

A GitHub Advanced Security (GHAS) feature that runs license checks on pull requests. Works via **rulesets**:[^gh]

- **Evaluate mode**: annotates PRs with license alerts but does not block merges. Used for rollout/training.
- **Active mode**: blocks merges when new dependencies violate policy.

A custom property on repositories determines which mode is active (can be toggled per-repo). Checks scan both direct and transitive dependencies.[^gh]

## Policy setup

Common permissive licenses (MIT, Apache 2.0, BSD-3-Clause) are a good starting list to seed a policy.[^gh] From there, two expansion mechanisms:

1. **Permit a license type**: allows that license across the entire enterprise (e.g., an MIT-variant that hasn't appeared before).
2. **Permit a specific package**: scoped to a repository when the license can't be blanket-permitted (e.g., a commercial license for which one team has paid). Supports wildcard matches (e.g., `@github-ui/*`).[^gh]

## Developer workflow

1. PR modifies dependencies → scan runs automatically.
2. If a dependency's license is already permitted or has a package exception → check passes.
3. If not: tool comments on PR with alerts per problematic package (direct and transitive).[^gh]
4. Developer either removes the dependency or **raises an exception request** → notifies the license policy team (OSPO).
5. OSPO reviews and decides: permit the license (enterprise scope) or permit the package (repo scope).[^gh]
6. Emergency **"break glass" override**: toggle the ruleset's custom property to temporarily disable enforcement for critically time-sensitive PRs. Should be rare.[^gh]

## GitHub's OSPO experience (rollout notes)

GitHub ran Evaluate mode for ~1 month before switching to Active. Running the old internal tool in parallel let them verify behavioral consistency.[^gh]

Policy team spans time zones for timely review; in practice most requests are triaged within a few hours.[^gh]

The team has only used the emergency break-glass override once.[^gh]

## See also

- [/software-engineering/github-advisory-database.md](/software-engineering/github-advisory-database.md) — related supply chain security feature
- [/software-engineering/ci-cd.md](/software-engineering/ci-cd.md) — automated checks in the PR pipeline

---

[^gh]: raw/_inbox/web-how-github-maintains-compliance-for-open-source-dependencies-99e81580.md — GitHub Blog, GitHub OSPO
