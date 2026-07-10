---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-intro.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-preface.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-cpu-intro.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-cpu-api.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-cpu-mechanisms.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-cpu-dialogue.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-dialogue-virtualization.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-dialogue-threeeasy.md
    channel: pdf
    ingested_at: 2026-07-09
aliases:
  - operating system
  - OS
  - process
  - virtualization
  - context switch
  - system call
  - fork exec wait
  - limited direct execution
tags:
  - corpus/software-engineering
  - concept
created: 2026-07-09
updated: 2026-07-09
---

# Operating Systems Fundamentals

TL;DR: An OS is the layer of software that virtualizes physical resources (CPU, memory, storage) into abstractions (processes, address spaces, files) that are easy to use. Three fundamental problems — virtualization, concurrency, and persistence — organize everything the OS does. The central technique for CPU virtualization is **time sharing** with **limited direct execution**: run user code directly on hardware for performance, but regain control via trap mechanisms and timer interrupts.

## What an OS Does

A running program fetches, decodes, and executes instructions one at a time — the Von Neumann model. The OS makes this useful by [^src1]:

- Running many programs simultaneously (virtualizing the CPU)
- Allowing programs to share memory (virtualizing memory)
- Managing persistent storage (managing files/devices)
- Providing security and protection between programs

**The OS as a resource manager**: the OS must fairly and efficiently manage CPU time, memory, and I/O among competing processes.

**Three easy pieces** (organizing framework) [^src2]:
1. **Virtualization** — turning physical resources into abstract, easy-to-use virtual resources
2. **Concurrency** — managing multiple things happening at once
3. **Persistence** — ensuring data survives across power loss

## The Process Abstraction

A **process** is a running program — the OS's abstraction for a CPU [^src3].

**Machine state** of a process includes:
- **Memory** (address space): instructions + data the process can address
- **Registers**: PC (program counter), stack pointer, general purpose registers
- **I/O information**: open files, connections

**Process states**:
- **Running**: executing on a CPU
- **Ready**: ready to run, but OS has scheduled another process
- **Blocked**: waiting for some event (I/O completion, lock release)

**Process list (PCB)**: the OS maintains a **process control block** for each process: registers, state, PID, memory info, I/O state. Context switching saves/restores these [^src3].

## Process API: fork(), exec(), wait()

Unix presents process creation through a distinctive pair of system calls [^src4]:

**fork()**: creates an exact copy of the calling process. Both parent and child continue execution from the point after the fork. fork() returns:
- 0 to the child
- The child's PID to the parent
- -1 on error

"Strangest routine you will ever call" — a single call, two returns in two processes.

**exec()**: replaces the current process's address space and code with a new program. Does not create a new process — transforms the calling process. Never returns on success.

**wait()**: blocks the parent until a child process completes (and its zombie entry is reaped).

**Why fork-then-exec?** The separation allows the shell to manipulate the child's environment (file descriptors, env vars) between fork() and exec() — enabling I/O redirection, pipes, and background processes cleanly [^src4].

## Limited Direct Execution

The OS's challenge: run programs efficiently (direct on hardware) while maintaining control [^src5].

**Problem 1: restricted operations**. User programs must not be able to directly access hardware, issue I/O, or harm other processes. Solution: **two CPU modes**:
- **User mode**: restricted; cannot issue privileged instructions
- **Kernel mode**: unrestricted; OS runs here

**Trap mechanism**: user code transitions to kernel mode via a **system call** (a trap instruction). The hardware:
1. Saves the calling process's state (PC, registers, flags) onto a kernel stack
2. Jumps to the OS's **trap handler** (set at boot time via a **trap table**)
3. OS executes privileged operation
4. Returns via a **return-from-trap** instruction, restoring user state

Trap table entries are set at boot; user code cannot change what operations are available — this is the "limited" in limited direct execution [^src5].

**Problem 2: regaining control**. A running process occupies the CPU — how does the OS get it back?

**Timer interrupt**: the OS programs a hardware timer (set at boot) to interrupt the CPU every N milliseconds. On interrupt:
1. Hardware saves the process's state onto the kernel stack
2. Jumps to the OS's interrupt handler
3. OS runs its **scheduler** to decide which process runs next

**Context switch**: when the scheduler decides to switch from process A to process B:
1. Save A's register state to A's PCB (kernel stack)
2. Restore B's register state from B's PCB
3. Switch to B's kernel stack and return from the interrupt into B

Critical discipline: the OS must save/restore state precisely — missing any register corrupts the process [^src5].

## Mechanism vs Policy

A key OS design principle [^src3]:
- **Mechanisms**: low-level methods that implement a piece of functionality (e.g., context switch)
- **Policies**: high-level decisions about how to use the mechanisms (e.g., scheduling: which process to run next?)

Separating them allows changing policy without changing mechanism — an important modularity principle.

## Related Corpus Pages

- [/software-engineering/cpu-scheduling.md](/software-engineering/cpu-scheduling.md) — scheduling policies: FIFO, SJF, MLFQ, lottery
- [/software-engineering/concurrency-and-threads.md](/software-engineering/concurrency-and-threads.md) — threads, locks, condition variables
- [/software-engineering/file-systems.md](/software-engineering/file-systems.md) — persistence: files, inodes, journaling
- [/software-engineering/system-design-fundamentals.md](/software-engineering/system-design-fundamentals.md) — scaling, distributed systems at application layer
- [/software-engineering/sources/ostep-operating-systems-three-easy-pieces.md](/software-engineering/sources/ostep-operating-systems-three-easy-pieces.md) — full OSTEP source summary

---

[^src1]: [OSTEP Introduction](../../raw/pdf/pdf-intro.md)
[^src2]: [OSTEP Preface](../../raw/pdf/pdf-preface.md)
[^src3]: [OSTEP CPU Introduction: The Abstraction: The Process](../../raw/pdf/pdf-cpu-intro.md)
[^src4]: [OSTEP CPU API: Interlude: Process API](../../raw/pdf/pdf-cpu-api.md)
[^src5]: [OSTEP CPU Mechanisms: Limited Direct Execution](../../raw/pdf/pdf-cpu-mechanisms.md)
