---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/youtube/youtube-2x0eq5oDOJY-ci-cd-with-robert-erez.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube--hVG9z0fCac-e1-github-actions-write-your-first-workflow-with-github-apis.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - CI/CD
  - continuous integration
  - continuous delivery
  - continuous deployment
  - GitOps
  - progressive delivery
  - canary deployment
  - blue-green deployment
  - feature flags
  - feature toggles
  - ephemeral environments
  - platform teams
  - rollback
  - roll forward
  - Octopus Deploy
tags:
  - corpus/software-engineering
  - concept
created: 2026-06-25
updated: 2026-06-25
---

# CI/CD, Progressive Delivery, and GitOps

**TL;DR**: CI/CD is a maturity ladder from manual deploys to fully automated production delivery. Progressive delivery (canary, blue/green, feature flags) de-risks releases by decoupling deployment from release. GitOps extends Kubernetes' declarative model to Git as the desired-state source. Feature toggles are the most granular and reversible progressive delivery tool — preferred over canary for application logic [^src1].

## The CI/CD maturity ladder

Four stages, in order [^src1]:

| Stage | What happens |
|---|---|
| **Yolo** | SSH directly to prod, manual copy |
| **CI — Continuous Integration** | Merge frequently to a single branch; tests run continuously |
| **CD — Continuous Delivery** | Pipeline always ready to deploy; click-to-deploy to production |
| **CD — Continuous Deployment** | Every passing commit automatically reaches production |

The difference between Continuous Delivery and Continuous Deployment: "do your changes go out to production automated?" [^src1]. Continuous Deployment "doesn't really suit every company" — regulated industries often retain manual approval gates, and this is a legitimate design choice [^src1].

## Progressive delivery

Progressive delivery is "the next evolution beyond continuous delivery" — releasing changes in a controlled, incremental way to catch failures before they reach the full user base [^src1].

### Canary deployments

Route a small percentage of traffic to the new version alongside the old, observe, then graduate [^src1]. "New Zealand was always our canary" — chosen because it's large enough to be meaningful, small enough that bugs cause limited damage [^src1]. The term comes from the coal-mine canary: early warning before the hazard reaches everyone.

**Unit of change**: the entire app version. A canary testing 20 commits tests all 20 at once, making attribution hard [^src1].

### Blue/green deployments

Run old and new versions side by side; validate the new version directly before flipping 100% of traffic [^src1]. Useful when you need to avoid cold-start delays — the new version initializes fully before traffic shifts.

### Feature toggles (feature flags)

> "In my view, probably the more useful progressive delivery strategy is feature toggles." [^src1]

A toggle is a named boolean in the codebase linked to an external service; flipping it activates or deactivates a code path in seconds [^src1].

**Advantages over canary** [^src1]:

| Dimension | Canary | Feature flag |
|---|---|---|
| Unit of change | Entire app version | Single code path |
| Targeting | Network traffic rules (coarse) | Complex user-segment rules (fine) |
| Rollback speed | Minutes (redeploy old version) | Seconds (flip the toggle) |
| Timing | Tied to deployment window | Independent of deployment (ship Monday, release Tuesday) |

Feature flags decouple deployment from release — "you ship the code as fast as you want, but manage the rollout of the actual feature set independent of the deployment" [^src1].

**Schema changes still require care**: a feature flag can wrap even DB schema migration code paths, but the flag and the schema must be mutually consistent in both paths [^src1].

**Flag hygiene — the staleness problem**: flags accumulate and become forgotten. Mitigation at Octopus Deploy: each toggle carries an expiry and owner; the CI pipeline notifies the team when a toggle passes its expiry [^src1]. > "When we use that gardening metaphor in code — this is weeding." [^src1]

## Rollbacks vs. roll-forward

Rollback is "always a spicy one" [^src1]. The preferred strategy is **roll-forward**: fix the bug in a new version and push it, rather than reverting to the previous version.

Why rollback is hard:
- For stateless systems, reverting a Git commit and re-deploying works [^src1].
- For stateful systems (databases), rolling back code that ran a schema migration leaves code and schema out of sync — customers report success with rollback until the day they hit a schema change, then "it's just sheer luck that they've never run into that" [^src1].

Rule of thumb: "if the failure is just from the deployment process itself, your recovery is quick; if it involves schema or data, roll forward" [^src1].

## GitOps

Coined by Weaveworks ~2017, GitOps formalizes four pillars [^src1]:

1. **Declarative** — desired infrastructure state is described, not scripted
2. **Versioned and immutable** — state is stored in a versioned, tamper-evident store (tags, commit SHAs; not mutable tag pointers)
3. **Pull** — a GitOps agent pulls desired state from the repo and applies it to the cluster (not push)
4. **Continuous reconciliation** — the agent continuously corrects drift between desired and actual state

The name is somewhat misleading: "nothing in any of these pillars actually talks about Git" [^src1]. Secrets are the canonical example of what should *not* go into Git — sealed-secrets (encrypting secrets into Git) is noted as "a terrible idea" by the host [^src1]. As long as versioning and immutability guarantees are met, other stores are valid.

**GitOps is not for all teams**: process steps like smoke tests, notifications, and database migrations don't fit the declarative model well [^src1]. Absolutism about "everything must be in Git" often leads to overuse of tools like Argo Workflows to force non-declarative steps into the GitOps model.

## Platform teams

Evolution of the DevOps → DevOps-team → platform-team pattern [^src1]:

- **Old model**: Ops team receives code "thrown over the wall"
- **DevOps model**: Dev teams own operational aspects; fast feedback loops
- **Problem at scale**: DevOps teams form anyway, bifurcating processes; application teams carry CI/CD config as a tax on their time
- **Platform team model**: Provides self-service IDP (Internal Developer Portal) with standardized templates; application teams consume them and retain ownership of their own running services

Platform teams are justified when "you've got lots and lots of teams and each one is kind of owning that process end-to-end" — the cost is context overload on dev teams [^src1].

## Ephemeral environments

Per-feature temporary environments spun up from a branch, torn down on merge [^src1]. Benefits: each feature gets its own deployment to share/validate; testers are unblocked. Complications: multi-service dependencies, state seeding. AI agents coding and validating their own changes still need ephemeral environments — "it spins up, you've got some sort of provisioning process, and then once the job's done, you tear it down" [^src1].

## AI's effect on CI/CD

Current assessment (2026): still early. More AI-generated code → more velocity → possible de-emphasis on pipeline speed (agents don't context-switch) → increased emphasis on risk reduction [^src1]. Feature toggles emerge as the key tool for managing agentic code releases because they decouple deploy from release, allowing fast shipping while controlling feature exposure [^src1].

## Real-world scale: Kubernetes + CI/CD

Kubernetes originated at Google (Borg), released partly to level the playing field between cloud vendors [^src1]. It has become the dominant container orchestration platform — used on-prem (financial services, point-of-sale systems with hundreds of stores, research vessels) not just hyperscale cloud [^src1]. The declarative desired-state model is what made Kubernetes win over competitors like Nomad, Docker Swarm, CoreOS Fleet [^src1].

## GitHub Actions — anatomy and workflow

GitHub Actions is an automation platform for CI/CD and general workflows — "you can use them to automate your own coffee machine" [^src2].

### Core components

| Concept | Definition |
|---|---|
| **Event** | Trigger: push, pull_request, issue, `workflow_dispatch`, schedule, etc. |
| **Workflow** | YAML file in `.github/workflows/`; triggered by events |
| **Job** | Unit of work within a workflow; runs on a runner; composed of steps |
| **Step** | Atomic action or shell command; steps within a job run sequentially top-to-bottom |
| **Action** | Reusable code abstraction — `uses: actions/checkout@v2` references a public repo |
| **Runner** | Machine that executes steps; long-polls GitHub for work |

**Key rule**: Steps must run sequentially; jobs can run in parallel by default (each on an independent runner) [^src2].

### Runner types

- **GitHub-hosted**: Ubuntu, Windows, macOS — managed by GitHub [^src2]
- **Self-hosted**: provisioned and managed by you; full control over OS and tools; required for specialized hardware or environments [^src2]

### Workflow structure

```yaml
name: Hello World Workflow
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:  # adds manual "Run" button in UI

jobs:
  hello:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Hello World
        run: echo "hello world"
        shell: bash

  goodbye:
    runs-on: ubuntu-latest
    steps:
      - name: Goodbye World
        run: echo "goodbye world"
```

Action versioning uses a Git reference after `@`: `@v2`, `@main`, `@<commit-sha>` [^src2]. Pinning to a commit SHA gives the most reproducible builds.

### Community actions

The Actions marketplace hosts reusable actions with the `owner/repo@version` syntax (`actions/checkout`, `actions/setup-node`, etc.). The action's source code lives in a public repo; calling it clones it into the runner and executes it [^src2].

### Workflow series scope

The linked series covers (9–12 videos): CI pipelines → CD/delivery → Terraform Cloud (IaC) → GitOps with Argo CD and Flux → self-hosted runners → GitHub Advanced Security + CodeQL → writing custom actions (JavaScript or Docker-based) → OIDC, secrets management, hardening [^src2].

## See also

- [[software-engineering/kubernetes|Kubernetes]] — declarative orchestration platform that GitOps builds on
- [[software-engineering/microservices|Microservices]] — architectural context driving platform team formation
- [[software-engineering/distributed-systems-fallacies|Distributed Systems Fallacies]] — reliability assumptions that CI/CD is designed to surface and contain
- [[software-engineering/git-basics|Git Basics]] — underlying VCS that GitHub Actions workflows target

---

[^src1]: [CI/CD with Robert Erez (The Pragmatic Engineer)](../../raw/youtube/youtube-2x0eq5oDOJY-ci-cd-with-robert-erez.md)
[^src2]: [GitHub Actions: Write your first workflow (glich.stream)](../../raw/youtube/youtube--hVG9z0fCac-e1-github-actions-write-your-first-workflow-with-github-apis.md)
