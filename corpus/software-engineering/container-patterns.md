---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/pdf/pdf-burns-designing-distributed-systems-microsoft-free-edition-part-01.md
    channel: pdf
    ingested_at: 2026-07-07
  - path: raw/pdf/pdf-burns-designing-distributed-systems-microsoft-free-edition-part-02.md
    channel: pdf
    ingested_at: 2026-07-07
aliases:
  - sidecar pattern
  - ambassador pattern
  - adapter pattern
  - single-node container patterns
tags:
  - corpus/software-engineering
  - concept
created: 2026-07-07
updated: 2026-07-07
---

# Container Patterns (Single-Node)

TL;DR: Three reusable patterns for splitting an application into cooperating containers on a single Kubernetes node. Containers share a filesystem, network namespace, and process namespace — enabling modular augmentation of any application without modifying its image.

## Why containers enable pattern reuse

The OOP analogy: just as objects provide a clean interface for reusable code components, containers provide a clean interface (filesystem, HTTP port, env vars) for reusable distributed system components. A sidecar that adds HTTP monitoring works alongside any application that exposes a /health endpoint, regardless of language [^src1].

## The Sidecar Pattern

A second container co-scheduled with the main application container that augments it — without the main container being aware of the sidecar.

**What it adds** (examples from Burns):
- **Monitoring/observability**: `topz` sidecar reads the main container's `/proc` via shared PID namespace; exposes resource usage on HTTP
- **Git synchronization**: sidecar runs `git pull` loop; shares filesystem with Node.js app; implements a PaaS that auto-redeploys on git push
- **SSL termination**: nginx sidecar handles HTTPS; main container only speaks HTTP
- **Log forwarding**: sidecar tails log files; ships to central log aggregator

**Design principles for reusable sidecars**:
1. Parameterize via environment variables (not hardcoded config)
2. Document the API surface (which filesystem paths, ports, env vars are used)
3. Document the operational model (restart behavior, failure modes)
[^src1]

## The Ambassador Pattern

A proxy container that acts as an intermediary between the main container and the outside world. The main application always connects to `localhost`; the ambassador translates and routes.

**Examples**:
- **Request splitting**: ambassador routes 1% of traffic to an experimental service (A/B testing)
- **Service discovery**: ambassador handles sharding; main app doesn't need to know which shard to contact
- **Protocol translation**: ambassador speaks gRPC externally; main container speaks HTTP/1.1 internally

The ambassador pattern decouples service discovery and routing logic from business logic [^src1].

## The Adapter Pattern

The inverse of Ambassador: the adapter normalizes the **output** of the main container for external consumers.

**Example**: application emits custom metrics format; adapter container transforms them to Prometheus exposition format. The monitoring system only needs to speak one protocol; each application gets its own adapter [^src1].

## Comparison

| Pattern | Transforms | Direction |
|---|---|---|
| Sidecar | Adds capability to main container | Internal augmentation |
| Ambassador | Routes/adapts requests inbound | External → internal |
| Adapter | Normalizes output | Internal → external |

[^src1]: [Designing Distributed Systems, parts 1–2](../../raw/pdf/pdf-burns-designing-distributed-systems-microsoft-free-edition-part-01.md), Brendan Burns, O'Reilly, 2018
