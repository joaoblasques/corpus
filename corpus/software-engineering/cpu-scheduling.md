---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-cpu-sched.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-cpu-sched-mlfq.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-cpu-sched-lottery.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-cpu-sched-multi.md
    channel: pdf
    ingested_at: 2026-07-09
aliases:
  - CPU scheduling
  - OS scheduler
  - FIFO scheduling
  - SJF scheduling
  - STCF
  - round robin
  - MLFQ
  - multi-level feedback queue
  - lottery scheduling
  - proportional share
  - multiprocessor scheduling
tags:
  - corpus/software-engineering
  - concept
created: 2026-07-09
updated: 2026-07-09
---

# CPU Scheduling

TL;DR: The OS scheduler decides which ready process runs next on the CPU. Policies evolved from simple FIFO (optimal only with equal-length jobs) through SJF (optimal turnaround but requires future knowledge) to MLFQ (learns job behavior from history to approximate SJF without foreknowledge) and lottery scheduling (proportional fairness via random ticket draws). Multi-CPU scheduling adds cache affinity and load balancing to the challenge.

## Scheduling Metrics

**Turnaround time** = T_completion − T_arrival. Minimizing this favors short jobs [^src1].

**Response time** = T_first_run − T_arrival. Critical for interactive/time-sharing workloads [^src1].

**Tradeoff**: policies that minimize turnaround (run short jobs first) often hurt response time, and vice versa.

## Simple Policies

**FIFO (First In, First Out)**: run jobs in arrival order. Optimal when all jobs have equal length. Catastrophically bad when a long job arrives before many short ones (**convoy effect**: a 100s job blocking ten 10s jobs produces avg turnaround ≈ 100s instead of 10s) [^src1].

**SJF (Shortest Job First)**: run the shortest available job next. Provably optimal for average turnaround when all jobs arrive simultaneously. Breaks down when jobs arrive at different times (a long job that started first blocks later-arriving short jobs) [^src1].

**STCF (Shortest Time-to-Completion First)**: preemptive SJF. When a new job arrives, preempt the current job if the newcomer is shorter. Optimal for turnaround with varying arrival times. Still requires knowing job lengths — impractical for general use [^src1].

**Round Robin (RR)**: run each job for a fixed **time slice** (quantum), then switch to the next in the queue. Excellent response time (bounded by time_slice * n_jobs). Terrible turnaround (stretches each job over its full waiting time). "The worst policy for turnaround time if turnaround is what you care about" [^src1].

**Key insight**: no single metric — scheduling involves a tradeoff between turnaround and response time.

## Multi-Level Feedback Queue (MLFQ)

MLFQ addresses the practical problem of optimizing both turnaround and response time **without knowing job lengths** [^src2].

**Structure**: multiple queues, each with a different priority. At a given time, the highest-priority non-empty queue runs. Within a queue, round robin.

**Basic rules**:
- Rule 1: If Priority(A) > Priority(B), A runs.
- Rule 2: If Priority(A) = Priority(B), A and B run RR.
- Rule 3: A new job enters at the highest priority.
- Rule 4 (original): If a job uses its entire time slice, reduce its priority.
- Rule 4 (refined): If a job uses its allotted time *across* multiple yields (to prevent gaming via frequent voluntary yields), reduce its priority.
- Rule 5: Periodically boost all jobs to the top priority (starvation prevention) [^src2].

**Intuition**: short jobs stay at high priority (they finish before exhausting their slice and don't get demoted); long CPU-bound jobs drift to low priority. I/O-intensive interactive jobs stay at high priority because they voluntarily yield the CPU before exhausting their slice.

**Problems with naive MLFQ**:
- **Starvation**: high-priority interactive load can starve low-priority CPU-bound jobs forever. Fixed by Rule 5 (priority boost).
- **Gaming**: a program that issues a dummy I/O near the end of each time slice keeps high priority. Fixed by tracking total CPU usage across slices.

MLFQ was first described by Corbato et al. in 1962 (CTSS) — work that eventually led to Corbato's ACM Turing Award [^src2].

## Lottery Scheduling (Proportional Share)

**Goal**: each job receives a guaranteed proportion of CPU time, not just best-effort fairness [^src3].

**Mechanism**: assign each process a number of **tickets** proportional to its desired CPU share. Each time slice, hold a lottery: pick a random winning ticket. The process holding that ticket runs [^src3].

**Example**: A has 75 tickets (0–74), B has 25 (75–99). A winning ticket in 0–74 → A runs; 75–99 → B runs. Over time, A gets ~75% of CPU.

**Advantages of randomness**:
1. No weird corner-case behaviors (unlike LRU which has worst-case O(n) for cyclic sequences).
2. Lightweight — only need to track ticket counts, not per-process CPU history.
3. Fast — just pick a random number.

**Ticket mechanisms**: ticket currency (per-job denomination), ticket transfer (temporarily give tickets to a blocked process you're waiting on), ticket inflation (boost your share without coordination if you trust other processes).

**Stride scheduling**: a deterministic alternative to lottery scheduling. Each process has a stride = large_constant / tickets. A counter (pass) advances by stride each time the process runs. Always run the process with the smallest pass. Achieves exact proportional share, not just probabilistic [^src3].

## Multi-CPU Scheduling

Multiple CPUs introduce complications beyond single-CPU scheduling [^src4]:

**Cache coherence**: modern CPUs cache memory. If process A runs on CPU1 with data in CPU1's cache, then migrates to CPU2, it must reload data from main memory — **cache cold**. Keeping a process on the same CPU (**cache affinity**) improves performance [^src4].

**Single global queue (SQMS)**: one scheduler queue for all CPUs. Simple but requires locking (performance bottleneck) and makes cache affinity hard to maintain [^src4].

**Multi-queue (MQMS)**: one queue per CPU. Each CPU has its own scheduler. Scales well; natural cache affinity. Problem: load imbalance (one CPU may become idle while another is overloaded). Solution: **work stealing** — an idle CPU occasionally steals jobs from an overloaded CPU's queue [^src4].

## Related Corpus Pages

- [/software-engineering/operating-systems.md](/software-engineering/operating-systems.md) — mechanisms (context switch, limited direct execution) that scheduling policies sit on top of
- [/software-engineering/concurrency-and-threads.md](/software-engineering/concurrency-and-threads.md) — concurrency issues arise when scheduling interleaves multiple threads
- [/software-engineering/sources/ostep-operating-systems-three-easy-pieces.md](/software-engineering/sources/ostep-operating-systems-three-easy-pieces.md) — OSTEP source summary

---

[^src1]: [OSTEP Scheduling: Introduction](../../raw/_inbox/pdf-cpu-sched.md)
[^src2]: [OSTEP Scheduling: Multi-Level Feedback Queue](../../raw/_inbox/pdf-cpu-sched-mlfq.md)
[^src3]: [OSTEP Scheduling: Proportional Share (Lottery)](../../raw/_inbox/pdf-cpu-sched-lottery.md)
[^src4]: [OSTEP Scheduling: Multi-CPU](../../raw/_inbox/pdf-cpu-sched-multi.md)
