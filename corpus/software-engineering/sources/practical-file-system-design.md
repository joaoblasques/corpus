---
type: source
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-practical-file-system-design-the-be-file-system-part-01.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-practical-file-system-design-the-be-file-system-part-02.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-practical-file-system-design-the-be-file-system-part-03.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-practical-file-system-design-the-be-file-system-part-04.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-practical-file-system-design-the-be-file-system-part-05.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-practical-file-system-design-the-be-file-system-part-06.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-practical-file-system-design-the-be-file-system-part-07.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-practical-file-system-design-the-be-file-system-part-08.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-practical-file-system-design-the-be-file-system-part-09.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-practical-file-system-design-the-be-file-system-part-10.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-practical-file-system-design-the-be-file-system-part-11.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-practical-file-system-design-the-be-file-system-part-12.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-practical-file-system-design-the-be-file-system-part-13.md
    channel: pdf
    ingested_at: 2026-07-23
  - path: raw/_inbox/pdf-practical-file-system-design-the-be-file-system-part-14.md
    channel: pdf
    ingested_at: 2026-07-23
aliases:
  - Practical File System Design
  - Be File System
  - BFS
  - BeFS
  - Dominic Giampaolo
  - BFS filesystem
  - Be filesystem
confidence: 0.97
last_confirmed: 2026-07-23
tags:
  - corpus/software-engineering
  - source
created: 2026-07-23
updated: 2026-07-23
---

# Practical File System Design: The Be File System (Giampaolo, 1999)

TL;DR: 247-page practitioner's guide to designing and implementing a production journaled file system from scratch. Giampaolo (sole implementor, 2-person team, 9-month schedule) walks through every component of the Be File System (BFS) — the 64-bit journaled FS of BeOS — from disk layout and B+tree indexing to query evaluation, vnode layer integration, and testing methodology. One of very few books that exposes real implementation decisions and the tradeoffs behind them rather than textbook-level theory.

## Book structure

| Chapter | Topic |
|---|---|
| 1 | Introduction to BeOS and BFS: history, design goals, constraints |
| 2 | What Is a File System? — terminology, inode/block map/extent concepts |
| 3 | Other File Systems — BSD FFS, Linux ext2, HFS, XFS, NTFS |
| 4 | Data Structures of BFS — superblock, block_run, inode, data_stream |
| 5 | Attributes, Indexing, Queries — small_data, B+trees, query language, live queries |
| 6 | Allocation Policies — disk geometry, allocation groups, preallocation |
| 7 | Journaling — write-ahead logging, group commit, atomic operations |
| 8 | Disk Block Cache — LRU+hash dual structure, journaling integration |
| 9 | File System Performance — benchmarks (IOZone, lat_fs, PostMark), tuning |
| 10 | The Vnode Layer — 57-function interface, node monitor, live query wiring |
| 11 | User-Level API — POSIX extensions, C++ Storage Kit class hierarchy |
| 12 | Testing — data structure verification, synthetic/real-world/end-user tests |
| Appendix A | File System Construction Kit — user-level FS sandbox for experimentation |

## Design goals and constraints

BFS was designed in 1996 by a 2-person team over 9 months.[^bfs-p01] The goals were: support for extended file attributes with typed values; attribute indexing and a query interface; 64-bit disk addressing for large files; journaling for crash consistency; and good performance for media workloads.[^bfs-p01] Design was constrained by BeOS's non-unified VM and buffer cache (a constant performance handicap throughout the book) and the need to run on commodity Pentium hardware.

## Filesystem comparisons (Chapter 3)

BSD FFS used cylinder groups for locality and synchronous metadata writes (safe but slow).[^bfs-p02] Linux ext2 wrote nothing synchronously, achieving very high throughput but offering no consistency guarantees.[^bfs-p02] HFS stored all metadata in B*trees (catalog file + extent overflow file), limited volumes to 65,536 blocks per extent, and used resource/data forks.[^bfs-p02] XFS (SGI IRIX) used B+trees for everything — free-space management, inode allocation, and directories — with parallel I/O across allocation groups.[^bfs-p03] NTFS stored all metadata as typed-attribute "file records" in the Master File Table and implemented write-ahead logging via the Log File Service.[^bfs-p03]

## BFS data structures (Chapter 4)

**Disk layout**: the disk is a linear array of fixed-size blocks. BFS defaults to 1024-byte blocks. A flat bitmap tracks free blocks. No per-group bitmaps — one bitmap for the entire volume.[^bfs-p03]

**block_run**: the fundamental addressing unit.[^bfs-p03]
```c
typedef struct block_run {
    int32  allocation_group;
    uint16 start;
    uint16 len;
} block_run;
```
A single block_run can address up to 65,536 contiguous blocks within an allocation group.

**Allocation groups**: logical disk divisions (~8192 blocks at 1K block size). Every 8th allocation group holds directory and inode data; interleaved groups hold user file data. This separation improves locality without requiring complex per-group accounting.[^bfs-p06]

**Superblock** key fields: `magic`, `block_size`, `block_shift`, `num_blocks`, `used_blocks`, `inode_size`, `log_blocks`, `log_start`, `log_end`, `root_dir` (inode address), `indices` (inode address), `flags` (BFS_CLEAN / BFS_DIRTY).[^bfs-p04]

**inode** structure (condensed):[^bfs-p04]
```c
typedef struct bfs_inode {
    int32       magic1;
    inode_addr  inode_num;       /* disk address of this inode */
    int32       uid, gid, mode, flags;
    bigtime_t   create_time, last_modified_time;
    inode_addr  parent, attributes;
    uint32      type;
    int32       inode_size;
    data_stream data;            /* 12 direct + indirect + double-indirect */
    int32       small_data[1];   /* inline attribute store */
} bfs_inode;
```
One inode per disk block. The `small_data` area uses the spare space in the inode block (~760 bytes after fixed fields) to store small attributes inline, avoiding extra seeks for common GUI attributes like icon position.[^bfs-p04]

**data_stream**: `NUM_DIRECT_BLOCKS = 12` direct block_runs plus `indirect` and `double_indirect` block_run fields. Variable-length extents mean a single block_run can cover a large contiguous region; at 1K blocks, max file size is ~34 GB in the best case.[^bfs-p04]

## Attributes, indexing, queries (Chapter 5)

**Attributes** are name/value pairs attached to any file. Small attributes (total ≤ ~760 bytes) live in the `small_data` area of the inode's disk block; larger attributes are stored in a separate inode-based attribute directory.[^bfs-p05] Attribute types: int32, int64, float, double, string, or raw bytes.

**B+trees**: BFS uses B+trees (derivative of Folk & Zoellick) with 1024-byte nodes for all indexing and directories. Interior nodes hold separator keys; leaf nodes are linked for in-order traversal.[^bfs-p05] Duplicate key handling uses "fragment" nodes (shared 1024-byte block split into 8 slots) for ≤8 duplicates, and full duplicate nodes for more — a critical optimization discovered after profiling directory duplication performance.[^bfs-p10]

**Automatic indices**: BFS automatically maintains three indices on every volume: `name` (updated on create/delete/rename), `size` (updated on close), and `last_modified_time` (updated on close, 64-bit timestamp with random component to avoid collisions).[^bfs-p05]

**Query language**: C-like syntax with AND/OR/NOT, comparison operators, and regex for strings (`*`, `?`, `[...]`, `[^...]`). Parsed by a recursive descent parser into a tree.[^bfs-p06] Query evaluation uses heuristics to select the tightest available index.[^bfs-p06]

**Live queries**: when a query is opened with the live flag, BFS tags the relevant indices with callbacks. On any index modification, the callback checks the modified entry against the query parse tree and sends filesystem event notifications if the file enters or leaves the result set.[^bfs-p11] "Live queries are an extremely powerful mechanism used by the find mechanism of the file manager."[^bfs-p11]

## Allocation policies (Chapter 6)

Sequential I/O is 50–100x faster than random I/O on spinning disks.[^bfs-p06] BFS allocation policy: allocate file data in the user-data AGs near the file's inode; preallocate 64K chunks to amortize journaling cost; trim preallocated space on `close()`.[^bfs-p06] Directory inodes and data go in the metadata AGs. The preallocation trimming fix — discovered by examining I/O access patterns — eliminated gaps between successively created files.[^bfs-p09]

## Journaling (Chapter 7)

**Problem**: writing to multiple on-disk structures (inode + directory + bitmap) non-atomically leaves inconsistencies after power loss.[^bfs-p07]

**BFS approach** — new-value-only write-ahead logging (simpler than old-value/new-value but no abort capability):[^bfs-p07]
1. `start_transaction()` — claim log space; lock affected blocks in cache.
2. `log_write_blocks()` — copy modified blocks to the on-disk log.
3. `end_transaction()` — mark log entry complete; unlock blocks.

The journaling implementation is under 1000 lines of code.[^bfs-p07] **Group commit**: multiple outstanding transactions are batched into one log flush — the same technique as ext2 but with consistency guarantees.[^bfs-p07] Only metadata is journaled (directories, bitmap, inodes, indices); user file data is not.

Atomic BFS operations include: create file/directory, delete, rename, change file size (touches at most 2057 blocks), attribute/index operations.[^bfs-p07]

Log size matters: increasing the log from 512K to 2048K "saw a considerable increase in performance" because a larger log allows more transactions to complete in memory before forcing a flush.[^bfs-p10]

## Disk block cache (Chapter 8)

Dual structure: a hash table (keyed on block number) for O(1) lookup, and an LRU doubly-linked list for eviction ordering.[^bfs-p08] Key optimizations: sort+coalesce writes before flushing (5–10x throughput improvement); 32K read-ahead on cache miss; hit-under-miss (cache not locked during I/O, allowing other threads to access cached data).[^bfs-p08]

Cache bypass: I/O ≥ 64K bypasses the cache entirely via DMA directly from/to the user buffer — the mechanism that allows BFS to achieve 99% of raw disk bandwidth for streaming workloads.[^bfs-p09]

Journaling constraints on the cache: the cache must support locking blocks (to prevent flushing mid-transaction), callbacks when blocks are flushed (so the journal knows when a transaction is truly complete on disk), and block cloning (to snapshot a block's state at transaction commit time, since BFS uses pointers directly into cached data).[^bfs-p09]

## Performance (Chapter 9)

Benchmark results on a dual Pentium Pro, 32MB RAM, IBM 3.2GB disk (raw bandwidth ≈ 5.92 MB/s write, 5.94 MB/s read):[^bfs-p09]

| File system | Sequential write | Sequential read |
|---|---|---|
| BFS | 5.88 MB/s (99%) | 5.91 MB/s (99%) |
| Linux ext2 | 4.59 MB/s (78%) | 4.97 MB/s (84%) |
| NTFS | 3.77 MB/s (64%) | 3.12 MB/s (52%) |

BFS achieves 99% of raw disk bandwidth for streaming I/O via cache bypass.[^bfs-p09] For metadata-intensive workloads (PostMark at 20k files/20k transactions), all file systems fall to 6–18 transactions/sec; BFS with indexing is the worst (6 tx/sec) because indexing costs ~50% overhead on metadata operations.[^bfs-p09] BFS-noindex performs roughly 2x better than BFS in metadata benchmarks.[^bfs-p09]

Key performance tuning discoveries:[^bfs-p09][^bfs-p10]
- Multiple transactions per log buffer (group commit) was the first major fix.
- Cache write coalescing (sort + merge contiguous blocks before flush).
- Log-dedup: write each block only once per log buffer even if modified multiple times.
- Preallocation trimming on `close()` to eliminate inter-file gaps.
- Fragment nodes for B+tree duplicates — reduced I/O by ~30% for directory duplication.

## Vnode layer (Chapter 10)

The vnode layer is the kernel's file-system-independent abstraction. Every file system exports a `vnode_ops` structure of 57 function pointers; BFS implements 53 of them (skips `rename_index`, `rename_attr`, `secure_vnode`, `link`).[^bfs-p10]

Key concepts: a **vnode** is an abstract file/directory with a 64-bit vnid; the vnode layer manages reference-counted pools of active vnodes; **cookies** hold per-file-descriptor state opaque to the vnode layer.[^bfs-p10] The `walk()` routine is the crux of the API — it converts a path component to a vnid by calling into the file system.[^bfs-p10]

**Node monitor**: `notify_listener()` is called by a file system on create/delete/rename/close/write_attr; the vnode layer routes notifications to any thread that has registered interest in a vnid.[^bfs-p11] "The node monitor system of the BeOS requires very little extra work on the part of a file system."[^bfs-p11]

Attributes and indices at the vnode layer expose the same open/read/rewind/close cookie pattern as directories — a consistent iterator interface throughout the API.[^bfs-p11]

## User-level API (Chapter 11)

Two APIs: POSIX C extensions (`fs_read_attr`, `fs_write_attr`, `fs_open_query`, `fs_create_index`, etc.) and the C++ Storage Kit.[^bfs-p11][^bfs-p12]

**C++ Storage Kit class hierarchy**: `BNode` (attributes + locking), `BEntry` (file-as-a-name), `BDirectory` (directory iteration), `BFile` (read/write), `BQuery` (query iteration + live query port), `BPath` (path string management), `BStatable` (stat information).[^bfs-p12] The `entry_ref` struct (directory inode + leaf name) is the compromise between path names (fragile) and raw inode numbers (security risk).[^bfs-p12]

Live queries at the C++ level: set a message port on a `BQuery` object before calling `Fetch()`; the file system sends update messages as files enter/leave the result set.[^bfs-p12]

## Testing (Chapter 12)

BFS used three test categories:[^bfs-p12][^bfs-p13]

**Runtime data structure checks** (never disabled in production): `CHECK_INODE()` macro validates magic number, size, inode_size, and in-memory pointer on every entry. Impossible-condition checks (e.g., block_run pointing to block zero) catch cross-module bugs before disk writes.[^bfs-p12]

**Synthetic tests**: disk fragmenter, muck files (multi-threaded create/rename/delete), big file test (exercises double-indirect blocks), news test (simulates INN news server), rename test (stress notification system), random I/O test (non-aligned reads, verifiable patterns).[^bfs-p13]

**Real-world tests**: archiving/unarchiving large hierarchies, compiling source trees, video capture, multi-track audio playback. "The most stressful by far is handling an Internet news feed" (~2 GB/day, hundreds of thousands of files).[^bfs-p13]

Methodology: develop at user level first (easier to debug); graduate to kernel; tight cycle of feature→test→fix→feature. Testing low-disk-space conditions required "running heavy stress tests while very low on disk space for many hours."[^bfs-p13] "Perhaps the best indicator of the quality of a file system is when the author(s) … are willing to store their own data on their file system."[^bfs-p13]

## File System Construction Kit (Appendix A)

A user-level sandboxed FS framework that runs within a file on disk (or on a raw device).[^bfs-p13] Components: superblock, block allocation, inode management, journaling (optional), data streams, directories, file operations. Each component has create/init/shutdown/allocate/free hooks modeled after the vnode layer API. Available at `http://www.mkp.com/giampaolo/fskit.tar.gz` (as of 1999).[^bfs-p13]

## Related corpus pages

- [/software-engineering/file-systems.md](/software-engineering/file-systems.md) — inode layout, crash consistency, journaling (WAL), FFS, LFS, SSD, RAID
- [/software-engineering/data-structures.md](/software-engineering/data-structures.md) — B+tree fundamentals

---

[^bfs-p01]: [BFS Part 1](../../../raw/pdf/pdf-practical-file-system-design-the-be-file-system-part-01.md) — title pages, TOC, Preface, Ch 1 (BeOS history, design goals), Ch 2 begins
[^bfs-p02]: [BFS Part 2](../../../raw/pdf/pdf-practical-file-system-design-the-be-file-system-part-02.md) — Ch 2 continues (directory ops, extended ops); Ch 3 begins (FFS, ext2, HFS)
[^bfs-p03]: [BFS Part 3](../../../raw/pdf/pdf-practical-file-system-design-the-be-file-system-part-03.md) — XFS, NTFS; Ch 4 begins (disk as block array, block_run struct)
[^bfs-p04]: [BFS Part 4](../../../raw/pdf/pdf-practical-file-system-design-the-be-file-system-part-04.md) — superblock fields, inode structure, data_stream, small_data area
[^bfs-p05]: [BFS Part 5](../../../raw/pdf/pdf-practical-file-system-design-the-be-file-system-part-05.md) — attribute API, small_data struct, B+tree theory and implementation, automatic indices
[^bfs-p06]: [BFS Part 6](../../../raw/pdf/pdf-practical-file-system-design-the-be-file-system-part-06.md) — query language, live queries, Ch 6 allocation policies, disk geometry
[^bfs-p07]: [BFS Part 7](../../../raw/pdf/pdf-practical-file-system-design-the-be-file-system-part-07.md) — Ch 7 journaling: write-ahead log, BFS 3-function API, group commit, atomic operations
[^bfs-p08]: [BFS Part 8](../../../raw/pdf/pdf-practical-file-system-design-the-be-file-system-part-08.md) — Ch 8 disk block cache: LRU+hash, hit-under-miss, read-ahead, journal interaction
[^bfs-p09]: [BFS Part 9](../../../raw/pdf/pdf-practical-file-system-design-the-be-file-system-part-09.md) — cache bypass policy; Ch 9 performance: IOZone/lat_fs/PostMark benchmarks, tuning discoveries
[^bfs-p10]: [BFS Part 10](../../../raw/pdf/pdf-practical-file-system-design-the-be-file-system-part-10.md) — B+tree duplicate fix, log size tuning; Ch 10 vnode layer: vnode_ops (57 functions), walk(), cookies
[^bfs-p11]: [BFS Part 11](../../../raw/pdf/pdf-practical-file-system-design-the-be-file-system-part-11.md) — node monitor API, live queries at vnode layer; Ch 11 begins: POSIX C extensions, C++ Storage Kit
[^bfs-p12]: [BFS Part 12](../../../raw/pdf/pdf-practical-file-system-design-the-be-file-system-part-12.md) — C++ class hierarchy (BNode/BEntry/BDirectory/BFile/BQuery), Ch 12 testing begins
[^bfs-p13]: [BFS Part 13](../../../raw/pdf/pdf-practical-file-system-design-the-be-file-system-part-13.md) — synthetic/real-world/end-user tests, testing methodology, Appendix A (FS Construction Kit), bibliography
[^bfs-p14]: [BFS Part 14](../../../raw/pdf/pdf-practical-file-system-design-the-be-file-system-part-14.md) — index (cross-reference of all topics, pages 225–237)
