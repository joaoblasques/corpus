---
type: source
domain: software-engineering
status: draft
sources:
  - path: raw/pdf/pdf-burns-designing-distributed-systems-microsoft-free-edition-part-01.md
    channel: pdf
    ingested_at: 2026-07-07
  - path: raw/pdf/pdf-burns-designing-distributed-systems-microsoft-free-edition-part-02.md
    channel: pdf
    ingested_at: 2026-07-07
  - path: raw/pdf/pdf-burns-designing-distributed-systems-microsoft-free-edition-part-03.md
    channel: pdf
    ingested_at: 2026-07-07
  - path: raw/pdf/pdf-burns-designing-distributed-systems-microsoft-free-edition-part-04.md
    channel: pdf
    ingested_at: 2026-07-07
  - path: raw/pdf/pdf-burns-designing-distributed-systems-microsoft-free-edition-part-05.md
    channel: pdf
    ingested_at: 2026-07-07
  - path: raw/pdf/pdf-burns-designing-distributed-systems-microsoft-free-edition-part-06.md
    channel: pdf
    ingested_at: 2026-07-07
aliases:
  - Designing Distributed Systems
  - Burns distributed systems
tags:
  - corpus/software-engineering
  - source
created: 2026-07-07
updated: 2026-07-07
---

# Designing Distributed Systems (Brendan Burns, O'Reilly, 2018)

TL;DR: A pattern catalog for distributed systems, structured analogously to the Gang-of-Four design patterns book but applied to container-based distributed services. Argues that containers are the unit of reusable distributed system components — enabling the same pattern reuse in distributed systems that OOP enabled in single-process programming.

## Core argument

Prior to containers, distributed system architectures were bespoke: each team built their own logging, health-checking, and traffic-shaping code. Containers provide an object-and-interface for expressing reusable patterns — just as OOP did for single-process software. This enables a "buy off the rack" vs "bespoke" tradeoff: the library/container-based approach is less tailored but much faster to acquire [^src1].

## Three pattern groups

### Part I — Single-Node Patterns (containers on one machine)

These patterns decompose a single application into cooperating containers sharing resources (filesystem, network, namespace) on one node.

| Pattern | Description |
|---|---|
| **Sidecar** | A second container that augments the main container: adds logging, health monitoring, Git-sync, or proxy functionality without modifying the main app image |
| **Ambassador** | A proxy container that translates the outside world for the main container: load-balancing, sharding, protocol translation, or A/B testing |
| **Adapter** | A container that normalizes heterogeneous output from the main container into a standard interface for external consumers (e.g., transforms custom metrics into Prometheus format) |

**Sidecar principle**: the sidecar must be parameterized (env vars), have a documented API surface, and be designed for modularity/reusability across many different application containers [^src2].

### Part II — Serving Patterns (multi-node, user-facing)

| Pattern | Description |
|---|---|
| **Replicated Load-Balanced** | Stateless service replicated N≥2 times behind a load balancer; uses readiness probes to gate traffic |
| **Sharded Services** | Stateful service where requests are deterministically routed by a shard key to the owning replica; reduces hot-spot and enables state partitioning |
| **Scatter/Gather** | Root node fans out a request to all leaf nodes; leaves process in parallel; root merges partial results. Parallelizes latency-bound workloads at the cost of "straggler" amplification |

**SLA math on replication**: achieving three-nines (99.9% = 1.4 min/day downtime) with continuous delivery requires either sub-3.6-second rollouts or ≥2 replicas — replicas are the practical path [^src3].

**Scatter/Gather straggler problem**: with 100 leaf nodes each having P(2s tail latency) = 1%, the root-level P(any leaf ≥2s) approaches 100% — more parallelism creates guaranteed tail latency amplification. Solution: bound leaf count; replicate each shard for failover [^src4].

### Part III — Batch Computation Patterns

| Pattern | Description |
|---|---|
| **Work Queue** | Items placed in a queue (e.g., Kafka topic); workers pull and process; decouples producers from consumers; enables horizontal scaling of workers |
| **Event-Driven (FaaS)** | Functions triggered by events; scale-to-zero; stateless; ideal for infrequent or bursty workloads |
| **Coordinated Batch (Join/Reduce)** | Fan-out work across shards, then barrier-synchronize (join) before aggregating; the distributed MapReduce pattern |

**Join (barrier synchronization)**: unlike a merge (blend two queues), a join waits until ALL parallel work items complete before releasing output — provides completeness guarantees for aggregate computations [^src5].

## Distributed locking pattern

Distributed locks via key-value stores (etcd, Redis) use compare-and-swap (CAS) with TTL: acquire = CAS(key, "locked", "unlocked"); release = CAS(key, "unlocked", "locked"). Resource versioning prevents the ABA problem (a TTL-expired lock being "unlocked" by the wrong holder) [^src5].

## Key implementation platform

All examples use [Kubernetes](/software-engineering/kubernetes.md) (Deployments, Services, readiness probes, Kafka on k8s). The author (Brendan Burns) is co-founder of Kubernetes [^src1].

[^src1]: [Designing Distributed Systems, part 1](../../raw/pdf/pdf-burns-designing-distributed-systems-microsoft-free-edition-part-01.md), Brendan Burns, O'Reilly, 2018
[^src2]: [Designing Distributed Systems, part 2](../../raw/pdf/pdf-burns-designing-distributed-systems-microsoft-free-edition-part-02.md), Brendan Burns, O'Reilly, 2018
[^src3]: [Designing Distributed Systems, part 3](../../raw/pdf/pdf-burns-designing-distributed-systems-microsoft-free-edition-part-03.md), Brendan Burns, O'Reilly, 2018
[^src4]: [Designing Distributed Systems, part 4](../../raw/pdf/pdf-burns-designing-distributed-systems-microsoft-free-edition-part-04.md), Brendan Burns, O'Reilly, 2018
[^src5]: [Designing Distributed Systems, part 5](../../raw/pdf/pdf-burns-designing-distributed-systems-microsoft-free-edition-part-05.md), Brendan Burns, O'Reilly, 2018
