---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/pdf/pdf-burns-designing-distributed-systems-microsoft-free-edition-part-04.md
    channel: pdf
    ingested_at: 2026-07-07
aliases:
  - scatter/gather
  - scatter gather pattern
  - fan-out pattern
tags:
  - corpus/software-engineering
  - concept
created: 2026-07-07
updated: 2026-07-07
---

# Scatter/Gather Pattern

TL;DR: A root node fans out (scatters) a user request to all leaf nodes in parallel; each leaf processes the partial request using its local data; the root waits for all responses and merges (gathers) them into a single user-facing response. Parallelizes latency-bound workloads but amplifies tail latency.

## Structure

```
User Request
     ↓
   [Root]
  /  |  \
[L1][L2][L3]  (all in parallel)
  \  |  /
   [Root]
     ↓
Merged Response
```

Two variants [^src1]:

| Variant | When | Example |
|---|---|---|
| Replicated data | All leaves hold the same data; root distributes term queries to parallelize computation | Full-text index search on identical replicas |
| Sharded data | Each leaf holds a distinct data shard; root must query all shards; union of partial results | Patent search across 1M+ documents that won't fit in one machine's memory |

## The straggler problem

The total latency of a scatter/gather request = latency of the **slowest** leaf. With N leaves:

- If each leaf has P(tail latency) = p per request
- The probability that at least one leaf hits tail latency = 1 − (1−p)^N

Example: p = 1% (99th percentile = 2s), N = 100 leaves → P(any leaf ≥ 2s) ≈ 63%. Every user request takes ≥ 2s with 63% probability — what was a 99th-percentile becomes a 37th-percentile [^src1].

**Practical implication**: scatter/gather systems have asymptotic gains from parallelization — overhead per node + straggler amplification means there's an optimal leaf count beyond which performance degrades.

## Reliability

Single-replica leaf failure = user request failure (all leaves required). Solution: replicate each shard, load-balance within each shard. The full pattern becomes: replicated sharded scatter/gather — leaf "nodes" are replicated services, not single instances [^src1].

## Contrast with other multi-node patterns

| Pattern | All leaves required? | Data sharded? |
|---|---|---|
| Scatter/Gather | Yes (root waits for all) | Optional |
| Sharded Service | No (request goes to one shard) | Yes |
| Replicated Load-Balanced | No (request goes to any replica) | No |

[^src1]: [Designing Distributed Systems, part 4](../../raw/pdf/pdf-burns-designing-distributed-systems-microsoft-free-edition-part-04.md), Brendan Burns, O'Reilly, 2018
