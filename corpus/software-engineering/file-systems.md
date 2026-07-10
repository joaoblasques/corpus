---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-file-intro.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-file-implementation.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-file-journaling.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-file-ffs.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-file-lfs.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-file-ssd.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-file-raid.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-file-disks.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-file-devices.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-file-integrity.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-file-dialogue.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-dialogue-persistence.md
    channel: pdf
    ingested_at: 2026-07-09
aliases:
  - file system
  - file systems
  - inode
  - journaling
  - crash consistency
  - FFS
  - LFS
  - log-structured file system
  - RAID
  - SSD
  - FSCK
  - write-ahead log
  - ext2
  - ext3
  - ext4
tags:
  - corpus/software-engineering
  - concept
created: 2026-07-09
updated: 2026-07-09
---

# File Systems

TL;DR: A file system is the OS subsystem that virtualizes persistent storage — spinning disks or SSDs — into the familiar file/directory abstraction. The central challenge is **crash consistency**: how to update on-disk structures atomically when any power loss leaves them partially written. The dominant solution is **journaling** (write-ahead logging): record intended changes in a log before applying them, so recovery can replay or discard incomplete operations. FFS laid down the locality-aware disk layout; LFS turns the entire disk into an append-only log; modern SSDs require FTL-aware write patterns to avoid write amplification.

## The File/Directory Abstraction

The OS presents persistent storage via two key abstractions [^src1]:

**File**: a linear array of bytes, identified by an **inode number** (low-level name). The file name is a human-readable alias stored in a directory.

**Directory**: maps human-readable names to inode numbers. Itself stored as a special file. Directories can contain other directories, forming a tree rooted at `/`.

**Paths**: a chain of directory lookups. `/foo/bar` = look up `foo` in root directory → get inode → look up `bar` in that directory → get inode for `bar`.

**Key Unix file operations**: open(), read(), write(), close(), lseek(), stat(), unlink(), mkdir(), link(), rename(), symlink() [^src1].

## Inode-Based File System Implementation

**Disk layout** (simplified ext2/vsfs): the disk is divided into fixed-size blocks. A typical layout [^src2]:
- **Superblock**: file system metadata (block size, number of inodes, etc.)
- **Inode bitmap**: which inodes are allocated
- **Data bitmap**: which data blocks are allocated
- **Inode table**: array of inodes (one per file or directory)
- **Data blocks**: actual file/directory content

**Inode**: a fixed-size data structure storing:
- File size, permissions, owner, timestamps
- **Block pointers**: direct (e.g., 12 pointers), single indirect (pointer to a block of pointers), double indirect, triple indirect. Enables large files without wasting space on small files.

**Directory entry**: maps filename → inode number. A directory is just a file containing (name, inode_number) pairs [^src2].

**Reading a file** (e.g., reading `/foo/bar`): read root inode → read root data blocks (find `foo`) → read `foo` inode → read `foo` data blocks (find `bar`) → read `bar` inode → read `bar` data blocks. Many reads before getting actual data — disk locality matters enormously [^src2].

## Crash Consistency: FSCK and Journaling

**The problem**: updating a file requires writing to multiple on-disk structures (e.g., inode + data block + data bitmap). A power loss between writes leaves the disk in an inconsistent state — the inode points to a block that the bitmap doesn't know is allocated, or vice versa [^src3].

**fsck (file system check)**: scan the entire file system at boot after an unclean shutdown to detect and repair inconsistencies. Works but is **extremely slow** (proportional to disk size — O(hours) for large disks). Unacceptable for modern systems [^src3].

**Journaling (write-ahead log)**: before updating any on-disk structure, write the intended update to a **log** (journal) first. On crash, the journal allows recovery to determine whether to apply or discard incomplete operations [^src3].

**Journal entry structure** (ordered journaling, ext3 default):
1. **TxBegin**: marks start of transaction
2. **Data blocks**: the actual data to write (optional in ordered mode)
3. **Metadata journal blocks**: the inode, bitmap updates
4. **TxEnd**: marks journal entry as complete

**Recovery**: if TxEnd is present → replay the journal entry to disk. If TxBegin but no TxEnd → the transaction was incomplete; skip it (safe because data was not yet written to its final location) [^src3].

**Checkpointing**: once a journal entry is committed to its final disk location, its journal entry can be freed (circular journal buffer) [^src3].

**Data journaling vs metadata journaling**: journaling both data and metadata (data journaling) is safe but doubles writes. Most systems journal only metadata (ordered journaling) — data is written to disk before the journal entry, ensuring consistency [^src3].

## FFS: Fast File System

**Problem with early Unix FS**: random placement of inodes and data blocks caused excessive seeks — the file system became fragmented over time, turning random-access patterns even for sequential reads [^src4].

**FFS solution** (Berkeley Fast File System, 1984): organize the disk into **cylinder groups** (contiguous disk regions). Place a file's inode and data blocks in the same cylinder group. Place related files (same directory) in the same group [^src4].

**Key ideas**:
- Large blocks (4KB) for better throughput
- Block groups for spatial locality
- Reserved space (~10%) to allow flexible block placement and avoid pathological fragmentation

FFS forms the basis for ext2/ext3/ext4 and most modern Unix file systems [^src4].

## LFS: Log-Structured File System

**Observation**: disks are fast for sequential writes but slow for random writes. DRAM is large — most reads are cache hits. Therefore, write performance is the bottleneck, not read performance [^src5].

**LFS approach**: treat the entire disk as an append-only log. Never overwrite data in place. All writes (data + metadata) are buffered in memory and periodically written as a large sequential **segment** to the end of the log [^src5].

**Challenges**:
- **Finding inodes**: since inodes move when updated, LFS uses an **inode map (imap)** that maps inode numbers to their current disk location. The imap is also written to the log.
- **Checkpoint region (CR)**: a fixed location on disk pointing to the latest imap. Read CR at mount time to find the current state.
- **Garbage collection**: old versions of blocks accumulate in the log. LFS must periodically clean segments by reading live data and rewriting it to a new segment, reclaiming space [^src5].

**Advantage**: all writes are sequential → near-peak disk throughput for writes. Reads are similarly fast due to locality.

**Flash/SSD applicability**: LFS ideas directly influence SSD Flash Translation Layers (FTL) — SSDs cannot overwrite data in place and require erase-before-write, making append-only writes natural [^src5].

## SSDs

**NAND flash characteristics** [^src6]:
- Read by page (4KB), write by page (only to erased pages), erase by block (128–256 pages)
- Cannot overwrite in place — must erase the entire block first
- Wear leveling: blocks have a limited number of erase cycles (~10K–100K)

**Flash Translation Layer (FTL)**: the SSD's internal software that presents a block-device interface to the OS while managing flash internals. FTL responsibilities:
- Maps logical block addresses (LBA) to physical page addresses (PPA)
- Implements garbage collection (collect dead/invalid pages from blocks, compact to free full blocks for erasure)
- Wear leveling (distribute writes evenly across flash blocks)

**Write amplification**: garbage collection causes more writes than the host requested. A major SSD performance concern for write-heavy workloads [^src6].

## RAID

**RAID** (Redundant Array of Inexpensive Disks): combines multiple disks to achieve capacity, performance, and/or reliability goals that a single disk cannot [^src7].

| RAID Level | Approach | Capacity | Reliability | Performance |
|---|---|---|---|---|
| RAID-0 (Striping) | Distribute data across disks in blocks | Full N disks | None — any disk failure = data loss | Best read/write throughput |
| RAID-1 (Mirroring) | Write each block to 2 disks | N/2 effective | Tolerates 1 disk failure per mirrored pair | Read: N/2 disks; write: bandwidth limited by 1 disk |
| RAID-4 (Parity) | N-1 data disks + 1 parity disk | N-1 disks | Tolerates 1 disk failure | Write bottleneck: every write updates parity disk |
| RAID-5 (Rotating parity) | Rotate parity across all N disks | N-1 disks | Tolerates 1 disk failure | Write bottleneck spread across disks |

**Stripe**: one row of data blocks across all disks. Parity = XOR of all data blocks in the stripe — allows reconstruction of any single lost disk [^src7].

**RAID-5 small write problem**: a 4-drive RAID-5 write requires: read old data, read old parity, write new data, write new parity — 4 I/Os per logical write [^src7].

## Related Corpus Pages

- [/software-engineering/operating-systems.md](/software-engineering/operating-systems.md) — OS abstractions; persistence as the third "easy piece"
- [/software-engineering/distributed-file-systems.md](/software-engineering/distributed-file-systems.md) — NFS and AFS: file systems over the network
- [/software-engineering/distributed-systems-fallacies.md](/software-engineering/distributed-systems-fallacies.md) — storage in distributed context
- [/software-engineering/sources/ostep-operating-systems-three-easy-pieces.md](/software-engineering/sources/ostep-operating-systems-three-easy-pieces.md) — OSTEP source summary

---

[^src1]: [OSTEP Interlude: Files and Directories](../../raw/pdf/pdf-file-intro.md)
[^src2]: [OSTEP File System Implementation](../../raw/pdf/pdf-file-implementation.md)
[^src3]: [OSTEP Crash Consistency: FSCK and Journaling](../../raw/pdf/pdf-file-journaling.md)
[^src4]: [OSTEP FFS: Fast File System](../../raw/pdf/pdf-file-ffs.md)
[^src5]: [OSTEP LFS: Log-Structured File System](../../raw/pdf/pdf-file-lfs.md)
[^src6]: [OSTEP Solid-State Drives](../../raw/pdf/pdf-file-ssd.md)
[^src7]: [OSTEP RAID](../../raw/pdf/pdf-file-raid.md)
