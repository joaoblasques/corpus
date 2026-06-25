---
type: entity
domain: mlops
status: stub
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
updated: 2026-06-25
---

# Tilt

**TL;DR** — Tilt is a developer experience tool that automates the inner dev loop for **microservice apps on Kubernetes**: watch files → build container images → apply to the cluster — replacing the manual `docker build && kubectl apply` / `docker-compose up` cycle. Tagline: "Kubernetes for Prod, Tilt for Dev" [^src1].

## Key facts

- **Repo**: [github.com/tilt-dev/tilt](https://github.com/tilt-dev/tilt)
- **Stars**: ~9,883
- **Language**: Go
- **Topics**: `development-environment`, `kubernetes`
- **Latest release**: v0.37.4

## Core workflow

```bash
tilt up   # start the dev environment defined in Tiltfile
```

Tilt reads a `Tiltfile` (Python-like DSL) that describes your services, images, and deployment configs. On file change it:
1. Rebuilds only the affected container image(s).
2. Applies updated manifests to your local/remote Kubernetes cluster.
3. Streams logs from all services in a dashboard UI.

## Value proposition

- Replaces the manual `docker build → push → kubectl apply` cycle on every code change.
- Works with any Kubernetes cluster (local: kind, minikube; remote: EKS, GKE).
- Team-wide: share a `Tiltfile` so every developer has the same dev environment.
- Faster than rebuilding from scratch — uses image layer caching and live-update where possible [^src1].

## Positioning

Complementary to production GitOps tools (Argo CD, Flux). Tilt owns the *development* side of Kubernetes; production deployment is handled separately. Analogous to how `docker-compose` accelerates single-machine multi-service dev but doesn't replace K8s in production [^src1].

## See also

- [[mlops/dev-environment-stack|Dev Environment Stack]] — the environment Tilt runs within
- [[mlops/ci-cd-for-ml|CI/CD for ML]] — CI/CD in the broader pipeline
- [[mlops/infrastructure-as-code|Infrastructure as Code]] — Terraform for the cluster itself
- [[mlops/README|MLOps hub]]

---

[^src1]: [tilt-dev/tilt (GitHub)](../../raw/github/github-tilt-dev-tilt.md) — README: description, install commands, core workflow overview
