---
type: entity
domain: data-engineering
status: draft
sources:
  - path: raw/web/redis-array-data-type-how-it-works-and-when-to-use-it.md
    channel: web
    ingested_at: 2026-06-16
aliases:
  - Redis
  - Redis array
  - Redis array data type
  - Redis 8.8
tags:
  - corpus/data-engineering
  - entity
created: 2026-06-16
updated: 2026-06-16
---

# Redis

**TL;DR** — Redis is an in-memory data store whose core types are strings, lists, hashes, sets, and sorted sets, each "purpose-built around a specific way of organizing data" [^src1]. None of those offered constant-time access to a specific *position*, so Redis 8.8 introduced the **array** type, designed by original Redis creator Salvatore Sanfilippo, for cases where the numeric index itself carries domain meaning [^src1].

## Core data types and the positional gap

The classic types each leave a hole when position is the data model: a list gives O(N) index access, a hash has no position concept, and a sorted set treats scores as metadata rather than addresses [^src1]. The array fills that gap with a specific contract: "if you know the index, you get the value, and everything in between costs nothing" [^src1]. Use it when index 47 *means* something — the 47th minute, line 4821 of a file, workflow step 3, or port 47 on a switch [^src1].

## The array type — internals

The array does not allocate memory per position. It divides the index space into **groups of 4096 slots** and allocates a slot block only when a group is written; an empty group costs 8 bytes (one null pointer) [^src1]. Consequences:

- **Gaps are free.** A 4096-position gap costs the same 8 bytes as a 40,960-position gap [^src1].
- **Scanning skips gaps.** Null group pointers are jumped in a single step, so scan cost is proportional to entries written, not index-space size [^src1].
- **Small values inline.** Small integers, floats, and short strings are encoded directly in the pointer's unused low bits, so a dense array of small values approximates a raw C array's footprint [^src1].
- **Two-step access.** A lookup finds the group, then binary-searches within it — constant-time because steps depend on structure, not data volume [^src1].
- **Self-promoting structure.** Writing an index ≥ 8,388,608 silently promotes the flat directory to a fixed three-level structure (superdir → block → slice); the upgrade is a one-time bounded cost (~16 KB pointer copies, a few microseconds) and is permanent [^src1].

## Commands

`ARGET`/`ARSET` for positional read/write; `ARGETRANGE` (full range incl. gaps) vs `ARSCAN` (occupied slots only); `ARCOUNT` returns active count in O(1) from a stored counter, while `ARLEN` returns highest set index + 1 — the two diverge under mid-array deletion [^src1]. `ARRING` is an atomic fixed-capacity ring write (single op, no read-before-write), replacing the non-atomic `LPUSH`+`LTRIM` pattern [^src1]. `ARGREP` does server-side pattern search (EXACT/MATCH/GLOB/RE, backed by the TRE regex library to avoid pathological worst cases) [^src1]. `AROP` runs server-side aggregations (SUM/MIN/MAX/AND/OR/XOR/USED/MATCH) [^src1].

## When to use array vs. existing types

The decision question is "does the numeric index carry domain meaning?" — if removing the index would change what the data means, use an array; if the index is an implementation detail for ordering or uniqueness, use an existing type [^src1].

- **vs. list** — a list is a deque (O(1) ends, O(N) positional, always dense); use a list when insertion order is the meaning, an array when position is [^src1].
- **vs. hash** — integer-keyed hashes work for point lookups but offer no server-side range query or gap detection [^src1].
- **vs. set** — sets answer membership, not position [^src1].
- **vs. sorted set** — the score is computed metadata you attach; the array index *is* the address [^src1].

For purely search-driven workloads on dense data, a dedicated index via Redis Search remains the right architecture [^src1].

## Related corpus pages

In the mondayDB architecture, Redis is used as a high-frequency write-cache WAL backend and for distributed locking / rate limiting — see [[data-engineering/mondaydb|mondayDB]].

[^src1]: [Diving deep into Redis's new array data type](../../raw/web/redis-array-data-type-how-it-works-and-when-to-use-it.md)
