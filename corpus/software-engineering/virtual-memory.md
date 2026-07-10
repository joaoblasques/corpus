---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-vm-mechanism.md
    channel: pdf
    ingested_at: 2026-07-10
  - path: raw/_inbox/pdf-vm-segmentation.md
    channel: pdf
    ingested_at: 2026-07-10
  - path: raw/_inbox/pdf-vm-freespace.md
    channel: pdf
    ingested_at: 2026-07-10
  - path: raw/_inbox/pdf-vm-paging.md
    channel: pdf
    ingested_at: 2026-07-10
  - path: raw/_inbox/pdf-vm-tlbs.md
    channel: pdf
    ingested_at: 2026-07-10
  - path: raw/_inbox/pdf-vm-smalltables.md
    channel: pdf
    ingested_at: 2026-07-10
  - path: raw/_inbox/pdf-vm-beyondphys.md
    channel: pdf
    ingested_at: 2026-07-10
  - path: raw/_inbox/pdf-vm-beyondphys-policy.md
    channel: pdf
    ingested_at: 2026-07-10
  - path: raw/_inbox/pdf-vm-complete.md
    channel: pdf
    ingested_at: 2026-07-10
  - path: raw/_inbox/pdf-vm-dialogue.md
    channel: pdf
    ingested_at: 2026-07-10
  - path: raw/_inbox/pdf-dialogue-vm.md
    channel: pdf
    ingested_at: 2026-07-10
  - path: raw/_inbox/pdf-toc.md
    channel: pdf
    ingested_at: 2026-07-10
aliases:
  - address space
  - address translation
  - virtual address
  - physical address
  - base and bounds
  - segmentation
  - paging
  - page table
  - TLB
  - translation lookaside buffer
  - free-space management
  - swap space
  - page replacement
  - demand paging
tags:
  - corpus/software-engineering
  - concept
created: 2026-07-10
updated: 2026-07-10
---

# Virtual Memory

TL;DR: Virtual memory gives each process the illusion of a large, private address space while the OS and hardware secretly share physical memory. The evolution goes: base+bounds (simple but wasteful) → segmentation (per-segment relocation, external fragmentation) → paging (fixed-size units, no external fragmentation). TLBs make paging fast. Multi-level page tables keep the page-table structure itself small. When physical memory is full, the OS swaps pages to disk and uses a replacement policy (LRU, clock algorithm) to decide what to evict.

## Address Spaces and Address Translation

The OS provides the **address space** abstraction: each process sees memory as a private array starting at address 0, even though many processes share the physical memory simultaneously [^src1].

The core technique is **hardware-based address translation**: on every memory reference, the hardware MMU (Memory Management Unit) transforms the **virtual address** issued by the process into the **physical address** where the data actually resides [^src1]. The process has no idea its references are being translated — **transparency** is a central goal.

The OS controls the hardware (sets registers, manages page tables) but lets the program run directly on the CPU for speed — the same **limited direct execution** approach used for CPU virtualization [^src1].

## Base and Bounds (Dynamic Relocation)

The simplest mechanism: two registers per CPU in the MMU — **base** and **bounds** (limit) [^src1].

```
physical address = virtual address + base
```

The hardware checks `virtual address < bounds` on every access; if not, it raises an exception (likely terminating the process). The OS sets these registers on each context switch.

**Advantages**: simple hardware; fast translation (one add, one compare).

**Limitation — internal fragmentation**: the space between the stack and heap inside the fixed slot is wasted physical memory. A 16 KB slot allocated to a process using only 4 KB wastes 12 KB [^src1].

## Segmentation

**Segmentation** generalizes base+bounds: instead of one pair for the whole address space, the MMU has one base+bounds pair per logical **segment** — typically code, heap, and stack [^src2].

Each segment can be placed independently in physical memory, avoiding the waste of the unused gap between stack and heap ("sparse address spaces") [^src2].

**Address translation**: the hardware uses the top bits of the virtual address (the **segment selector**) to choose which segment register pair to use, then adds the offset [^src2]:

```
segment  = (VirtualAddress & SEG_MASK) >> SEG_SHIFT
offset   = VirtualAddress & OFFSET_MASK
if offset >= Bounds[segment]: raise PROTECTION_FAULT
PhysAddr = Base[segment] + offset
```

The stack grows in the negative direction; the hardware needs a **grows-positive** bit per segment to handle this correctly [^src2].

Segments can carry **protection bits** (read, write, execute). A code segment marked read-execute can be shared across processes without risk [^src2].

**Problem — external fragmentation**: physical memory fills with variable-sized holes that are hard to satisfy. Algorithms like best-fit, worst-fit, and first-fit reduce but never eliminate it. The only real solution is to avoid variable-sized allocation [^src2].

> "The fact that so many different algorithms exist to try to minimize external fragmentation is indicative of a stronger underlying truth: there is no one 'best' way to solve the problem." [^src2]

## Free-Space Management

When managing variable-sized regions (as with segmentation or a `malloc` heap), the OS or allocator tracks free space with a **free list** [^src3].

Key algorithms:
- **Best-fit**: find the free chunk closest in size to the request. Low waste but slow (full scan) and leaves many small fragments.
- **Worst-fit**: find the largest free chunk. Leaves large remainders but tends to fragment them away quickly.
- **First-fit**: return the first free chunk that fits. Fast; fragmentation depends on allocation patterns.
- **Buddy algorithm**: powers-of-two splitting/coalescing; fast to find a free block, fast to coalesce adjacent free blocks.

**Splitting**: when a request is smaller than a free chunk, split it; return the requested portion, keep the remainder on the free list [^src3].

**Coalescing**: when a block is freed, merge it with adjacent free blocks to rebuild larger contiguous regions [^src3].

**External fragmentation** is an inherent problem with variable-sized allocation. Paging (fixed-size pages) sidesteps external fragmentation entirely [^src3].

## Paging

**Paging** chops the address space into fixed-size units called **pages** (typically 4 KB), and physical memory into same-size **page frames** [^src4]. Pages map to frames in arbitrary order, tracked by a per-process **page table**.

**Address translation**:
- Split the virtual address into a **Virtual Page Number (VPN)** and an **offset**.
- Index the page table with the VPN to get the **Physical Frame Number (PFN)**.
- Physical address = PFN concatenated with the offset.

```
VPN    = VirtualAddress >> PAGE_BITS
offset = VirtualAddress & OFFSET_MASK
PFN    = PageTable[VPN]
PhysAddr = (PFN << PAGE_BITS) | offset
```

**Advantages over segmentation**:
- No external fragmentation (all free frames are the same size).
- Sparse address spaces work naturally: unused virtual pages simply have invalid PTEs.

**Page Table Entry (PTE) bits** [^src4]:
- **Valid bit**: is this mapping in use? Invalid pages trap to the OS.
- **Present bit**: is the page in physical memory, or swapped to disk?
- **Protection bits**: read, write, execute permissions.
- **Dirty bit**: has the page been modified since it was brought in?
- **Reference/accessed bit**: has the page been accessed recently? Used by page replacement algorithms.

**Cost**: every memory access requires first fetching the PTE from memory — doubling memory traffic. This is why TLBs exist [^src4].

**Page table size problem**: a 32-bit address space with 4 KB pages needs 2^20 ≈ 1 million PTEs × 4 bytes = **4 MB per process**. With 100 processes, that's 400 MB just for page tables [^src4].

## TLBs (Translation-Lookaside Buffers)

A **TLB** is a small, fast, fully-associative hardware cache of recent virtual-to-physical translations, residing in the MMU [^src5].

**TLB hit path** (common case): extract VPN → look up TLB → get PFN → form physical address. No memory access for translation.

**TLB miss path**: hardware or OS walks the page table, installs the translation in the TLB, retries the instruction.

**Hardware-managed TLB** (x86): the hardware walks the page table on a miss, using a page-table base register (CR3). The OS only handles exceptions [^src5].

**Software-managed TLB** (MIPS, SPARC): a TLB miss raises an exception; the OS trap handler looks up the page table and installs the translation with privileged instructions. Flexible — the OS can use any page table format [^src5].

**Locality makes TLBs work**: spatial locality (array accesses hit the same page repeatedly) and temporal locality (recently-accessed pages reused) keep the TLB hit rate high. Typical hit rates approach 99% [^src5].

**Context switch problem**: TLB entries from a previous process are invalid for the new one. Two solutions:
1. **Flush the TLB** on every context switch (simple but costly — cold TLB after every switch).
2. **Address Space Identifiers (ASIDs)**: tag each TLB entry with an 8-bit process ID; entries from different processes coexist safely [^src5].

> "TLBs in a real sense make virtual memory possible." [^src5]

## Smaller Page Tables: Multi-Level Page Tables

A **linear page table** of 4 MB per process is impractical. Solutions [^src6]:

**Multi-level page tables**: break the page table itself into pages. Only allocate a second-level page-table page when the corresponding region of the address space is actually in use. Unused regions cost only one entry in the top-level **page directory** (marked invalid) instead of a full page of PTEs.

For a 32-bit address space with 4 KB pages:
- Split the 20-bit VPN into a 10-bit page-directory index and a 10-bit page-table index.
- The page directory has 1024 entries; each points to a 4 KB page of PTEs (also 1024 entries).
- A sparse address space (code + stack, nothing in between) uses only a handful of page-table pages rather than the full 4 MB.

**Inverted page tables**: one global page table indexed by physical frame number rather than virtual page number. Very compact for large physical memories, but VPN lookup requires searching the entire table (mitigated by hashing) [unsourced — from general OS knowledge, not directly cited in sources].

## Swapping: Beyond Physical Memory

When physical memory is full, the OS extends it using **swap space** on disk [^src7].

**Mechanism**:
- Each PTE has a **present bit**. When 0, the page is on disk.
- A memory access to a non-present page triggers a **page fault** trap.
- The OS **page fault handler** locates the page on disk, finds a free (or evicted) physical frame, reads the page from disk, updates the PTE, and retries the instruction.
- If no free frame exists, the OS must **evict** a page first (writing it to disk if dirty).

**Swap space** is a dedicated area on disk (or a file) holding pages that have been evicted from physical memory [^src7].

**Demand paging**: pages are only loaded from disk when actually accessed (on fault), not at process startup. This allows large address spaces without requiring all pages to fit in RAM simultaneously [^src7].

**Memory pressure** (when free frames are scarce) triggers the replacement policy. The OS may use a **high watermark / low watermark** policy: run a background daemon to keep at least LW free pages available; if free pages drop below LW, evict until HW is reached [^src7].

## Page Replacement Policies

The OS must choose which page to evict when it needs a free frame [^src8].

**Optimal (MIN/Belady)**: evict the page that will be accessed furthest in the future. Provably optimal but requires future knowledge — only useful as a theoretical baseline [^src8].

**FIFO**: evict the oldest page in memory. Simple; can evict frequently-used pages. Susceptible to Belady's Anomaly (larger cache can yield fewer hits) [^src8].

**LRU (Least Recently Used)**: evict the page not used for the longest time. Based on the **principle of locality** — recently used pages are likely to be used again soon. Performs well in practice but expensive to implement exactly (requires updating a time-stamp on every memory access) [^src8].

**LFU (Least Frequently Used)**: evict the page accessed least often. Variant of LRU using frequency rather than recency [^src8].

**Clock algorithm (approximating LRU)**: all pages are in a circular list; a clock hand sweeps through. Each PTE has a **use bit** (reference bit) set by hardware on access [^src8]:
1. If the page at the hand has use bit = 1: clear it to 0, advance the hand.
2. If use bit = 0: evict this page.

The clock algorithm avoids scanning all pages on every eviction while approximating LRU behavior. Dirty-page consideration: prefer evicting clean pages (no disk write needed) over dirty ones [^src8].

**Workload sensitivity**:
- **No-locality workload**: all policies perform equally — hit rate is purely a function of cache size.
- **80-20 workload**: LRU beats FIFO and Random; holds hot pages better.
- **Looping-sequential workload**: LRU performs as badly as FIFO (it evicts the pages it will need next). Random does better [^src8].

**Thrashing**: when the working set of active processes exceeds physical memory, the OS spends more time paging than doing useful work. Mitigations: admission control (don't run all processes simultaneously), out-of-memory (OOM) killer [^src8].

## Related Corpus Pages

- [/software-engineering/operating-systems.md](/software-engineering/operating-systems.md) — limited direct execution; process abstraction; context switches
- [/software-engineering/concurrency-and-threads.md](/software-engineering/concurrency-and-threads.md) — threads share a virtual address space; page tables are per-process not per-thread
- [/software-engineering/sources/ostep-operating-systems-three-easy-pieces.md](/software-engineering/sources/ostep-operating-systems-three-easy-pieces.md) — OSTEP source summary

---

[^src1]: [OSTEP Ch. 15: Mechanism: Address Translation](../../raw/_inbox/pdf-vm-mechanism.md)
[^src2]: [OSTEP Ch. 16: Segmentation](../../raw/_inbox/pdf-vm-segmentation.md)
[^src3]: [OSTEP Ch. 17: Free-Space Management](../../raw/_inbox/pdf-vm-freespace.md)
[^src4]: [OSTEP Ch. 18: Paging: Introduction](../../raw/_inbox/pdf-vm-paging.md)
[^src5]: [OSTEP Ch. 19: Paging: Faster Translations (TLBs)](../../raw/_inbox/pdf-vm-tlbs.md)
[^src6]: [OSTEP Ch. 20: Paging: Smaller Tables](../../raw/_inbox/pdf-vm-smalltables.md)
[^src7]: [OSTEP Ch. 21: Beyond Physical Memory: Mechanisms](../../raw/_inbox/pdf-vm-beyondphys.md)
[^src8]: [OSTEP Ch. 22: Beyond Physical Memory: Policies](../../raw/_inbox/pdf-vm-beyondphys-policy.md)
