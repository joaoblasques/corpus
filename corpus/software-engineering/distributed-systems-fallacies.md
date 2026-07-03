---
type: concept
domain: software-engineering
status: draft
sources:
  - path: 03_Resources/Articles/Disasters in a Microservices World.md
    channel: notes
    ingested_at: 2026-05-07
  - path: 03_Resources/Study Notes/DevOps - Kubernetes Complete Course for Beginners.md
    channel: notes
    ingested_at: 2026-05-21
aliases:
  - distributed systems fallacies
  - fallacies of distributed computing
  - eight fallacies
tags:
  - corpus/software-engineering
  - concept
created: 2026-05-07
updated: 2026-05-22
---

# Distributed Systems Fallacies

**TL;DR**: Eight false assumptions developers make about distributed networks — network reliability and zero latency being the most commonly violated — that cause production failures in [microservices](/software-engineering/microservices.md) architectures when left unaddressed [^src1].

## The eight fallacies

Originally enumerated by L. Peter Deutsch and James Gosling at Sun Microsystems [unsourced — canonical list; awaits a dedicated ingested source]. Each assumption holds in local development and breaks in production:

| # | Fallacy |
|---|---|
| 1 | The network is reliable |
| 2 | Latency is zero |
| 3 | Bandwidth is infinite |
| 4 | The network is secure |
| 5 | Topology doesn't change |
| 6 | There is one administrator |
| 7 | Transport cost is zero |
| 8 | The network is homogeneous |

Sourced failure modes from ingested sources cover fallacies 1, 2, 4, and 5. Fallacies 3, 6, 7, and 8 are listed for completeness; substantive coverage awaits a dedicated source.

## Sourced failure modes and mitigations

### Fallacies 1 + 2 — Network is reliable / Latency is zero

Microservices make these assumptions visible: assumptions about network reliability and latency that don't hold in production cause failures in inter-service communication and data consistency [^src1]. Partial failures are not edge cases — distributed systems will have them, and explicit resilience strategies are required [^src1].

**Design responses (sourced):**
- Resilience planning: explicit strategies for handling partial failures; centralized observability — logging and monitoring across all services — to detect anomalies [^src1]. See [Microservices — best practices](/software-engineering/microservices.md).
- Eventual consistency: in distributed microservices systems, updates are not immediately visible everywhere; temporary inconsistencies are expected and must be designed for explicitly [^src1]. See [Microservices — eventual consistency](/software-engineering/microservices.md).
- Kubernetes auto-restart and health checks catch failed containers and route traffic away from unhealthy pods — a direct infrastructure response to the reliability assumption [^src2]. See [Kubernetes — relationship to microservices](/software-engineering/kubernetes.md).

### Fallacy 4 — The network is secure

In Kubernetes, Secrets are base64-encoded but not encrypted by default [^src2] — a concrete instance of trusting the network to provide security that it does not. Encryption must be configured explicitly: etcd encryption at rest for stored Secrets, and mutual TLS (mTLS) between pods for in-transit traffic.

### Fallacy 5 — Topology doesn't change

In Kubernetes, pod IPs are ephemeral: pods are replaced rather than restarted in place, and receive new IP addresses each time [^src2]. Any service addressing a pod directly by IP breaks on pod restart — the topology fallacy made literal.

**Kubernetes mitigation**: Service objects provide stable virtual endpoints backed by selector-matched pods, fully decoupling callers from topology churn [^src2]. This is the primary mechanism Kubernetes uses to operationalize microservices at scale. See [Kubernetes — core components (Service)](/software-engineering/kubernetes.md).

### Fallacies 3, 6, 7, 8 — Bandwidth / Administration / Transport cost / Homogeneity

Referenced as a group in [^src1] but not elaborated in ingested sources. No sourced content yet — awaits a primary source that covers the full canonical list (e.g., a distributed systems design text or the original Deutsch/Gosling paper).

## Relationship to microservices

Every microservices deployment is subject to all eight fallacies; ignoring them causes compounding failures as the service count grows [^src1]. The concrete design responses documented in the corpus are:

| Fallacy | Response | Source |
|---|---|---|
| Network reliability | Resilience planning; centralized observability | [Microservices](/software-engineering/microservices.md) [^src1] |
| Latency | Eventual consistency design; async where possible | [Microservices](/software-engineering/microservices.md) [^src1] |
| Network secure | Explicit secret encryption; mTLS | [Kubernetes](/software-engineering/kubernetes.md) [^src2] |
| Topology changes | Service objects with stable endpoints | [Kubernetes](/software-engineering/kubernetes.md) [^src2] |

## See also

- [Microservices](/software-engineering/microservices.md) — architectural context where fallacies 1+2 most commonly bite; resilience planning and eventual consistency
- [Kubernetes](/software-engineering/kubernetes.md) — infrastructure mitigations for fallacies 1 (auto-restart), 5 (Service stable endpoints), 4 (Secrets caveat)
- [Software Design Principles](/software-engineering/software-design-principles.md) — the defensibility principle (handle edge cases; fail loudly) is the code-level response to these fallacies
- [System Design Fundamentals](/software-engineering/system-design-fundamentals.md) — load balancing, database selection, horizontal scaling as practical mitigations for fallacies 1, 2, and 5
- [Software Engineering hub](/software-engineering/README.md)

---

[^src1]: [Disasters I've Seen in a Microservices World](/03_Resources/Articles/Disasters in a Microservices World.md)
[^src2]: [DevOps - Kubernetes Complete Course for Beginners](/03_Resources/Study Notes/DevOps - Kubernetes Complete Course for Beginners.md)
