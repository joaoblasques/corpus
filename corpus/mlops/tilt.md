---
type: entity
domain: mlops
status: draft
sources:
  - path: raw/github/github-tilt-dev-tilt.md
    channel: github
    ingested_at: 2026-06-25
aliases:
  - tilt-dev/tilt
  - Tilt dev tool
  - Kubernetes dev environment
tags:
  - corpus/mlops
  - entity
created: 2026-06-25
updated: 2026-07-14
---

# Tilt

**TL;DR** — Tilt is a developer experience tool that automates the inner dev loop for **microservice apps on Kubernetes**: watch files → build container images → apply to the cluster — replacing the manual `docker build && kubectl apply` / `docker-compose up` cycle. Tagline: "Kubernetes for Prod, Tilt for Dev" [^src1].

## Key facts

- **Repo**: github.com/tilt-dev/tilt
- **Stars**: ~9,883
- **Language**: Go
- **Topics**: `development-environment`, `kubernetes`
- **Latest release**: v0.37.4
- **License**: Apache 2.0, Copyright 2022 Docker, Inc. [^src1]

## Installation

One-step binary install [^src1]:

```bash
# macOS/Linux
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash

# Windows (PowerShell)
iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.ps1'))
```

Also available via Homebrew, Scoop, Conda, and asdf package managers [^src1].

## Core workflow

```bash
tilt up   # start the dev environment defined in Tiltfile
```

Tilt "automates all the steps from a code change to a new process: watching files, building container images, and bringing your environment up-to-date" [^src1]. On file change it:

1. Rebuilds only the affected container image(s).
2. Applies updated manifests to your local/remote Kubernetes cluster.
3. Streams logs from all services in a dashboard UI.

The `Tiltfile` (Python-like DSL) describes your services, images, and deployment configs and is shared across the team so every developer has the same dev environment [^src1].

## Language support

Official best-practice guides exist for HTML, NodeJS, Python, Go, Java, and C# [^src1].

## Extensibility

Tilt supports community-contributed extensions via the [tilt-extensions](https://github.com/tilt-dev/tilt-extensions) repo — "code snippets of Tiltfile functionality shared by the Tilt community" [^src1]. Custom extensions can be built and published following the Extensions docs.

## Community

- Kubernetes Slack: `#tilt` channel [^src1]
- GitHub Issues for bug reports
- Tilt sends anonymized usage telemetry by default to improve cross-platform quality [^src1]
- Code of Conduct covers users, contributors, followers, and employees [^src1]

## Security

Security issues should be reported privately to security@docker.com — not filed as public GitHub issues [^src1].

## Positioning

Complementary to production GitOps tools (Argo CD, Flux). Tilt owns the *development* side of Kubernetes; production deployment is handled separately. Analogous to how `docker-compose` accelerates single-machine multi-service dev but doesn't replace K8s in production [^src1].

## See also

- [CI/CD for ML](/mlops/ci-cd-for-ml.md) — CI/CD in the broader pipeline
- [Infrastructure as Code](/mlops/infrastructure-as-code.md) — Terraform for the cluster itself
- [MLOps hub](/mlops/README.md)

---

[^src1]: [tilt-dev/tilt (GitHub)](../../raw/github/github-tilt-dev-tilt.md)
