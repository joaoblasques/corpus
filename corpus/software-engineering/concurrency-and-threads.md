---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-threads-intro.md
    channel: pdf
    ingested_at: 2026-07-10
  - path: raw/_inbox/pdf-threads-monitors.md
    channel: pdf
    ingested_at: 2026-07-10
  - path: raw/_inbox/pdf-threads-api.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-threads-cv.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-threads-bugs.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-threads-dialogue.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-dialogue-concurrency.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-dialogue-monitors.md
    channel: pdf
    ingested_at: 2026-07-09
aliases:
  - threads
  - concurrency
  - locks
  - mutex
  - condition variables
  - deadlock
  - race condition
  - monitor
  - monitors
  - TCB
  - thread control block
  - POSIX threads
  - pthreads
  - Mesa semantics
  - Hoare semantics
tags:
  - corpus/software-engineering
  - concept
created: 2026-07-09
updated: 2026-07-10
---

# Concurrency and Threads

TL;DR: Threads are lightweight concurrent execution units within a process sharing the same address space. Concurrency is hard because threads interleave unpredictably — even trivially small code becomes nearly impossible to reason about exhaustively. The standard toolkit: **locks** (mutual exclusion over critical sections), **condition variables** (waiting for a condition to become true), and **semaphores** (a generalization). Key bugs: deadlock (circular lock dependency) and atomicity violations. Prescription: keep concurrency minimal, use simple and proven patterns, and prefer parallelism abstractions (Map-Reduce) when possible.

## What is a Thread?

A **thread** is like a separate process, but it shares the same address space as other threads in the same process [^src1]:
- **Own program counter, stack, and register state**
- **Shared**: heap, globals, code, open file descriptors

A multi-threaded process has one stack per thread (in the same address space). Thread-local data lives on each thread's stack; shared data lives on the heap.

**Why threads?**
1. Parallelism — use multiple CPUs on a single task
2. Overlapping I/O — keep the CPU busy while one thread waits on I/O
3. Avoiding the forking overhead of processes (threads share memory; processes copy it)

## Thread Fundamentals: State and Context Switching

Each thread has its own **Thread Control Block (TCB)** storing its register state (PC, general-purpose registers) [^src5]. Context switching between threads saves T1's registers to its TCB and restores T2's registers from its TCB — exactly like a process context switch except the **address space does not change** (no page-table switch needed) [^src5].

A multi-threaded address space has **one stack per thread**. These stacks share the same virtual address space, consuming space that would otherwise be free between the heap and the single stack of a single-threaded process [^src5].

The fundamental problem threading introduces: execution order is determined by the **scheduler**, not the programmer. "Two threads executing this code can result in a race condition" on even a trivially simple counter increment [^src5]:

```
mov 0x8049a1c, %eax    // load counter
add $0x1, %eax         // increment in register
mov %eax, 0x8049a1c    // store counter
```

A timer interrupt between any two of these three instructions causes an incorrect result if another thread runs the same sequence concurrently [^src5].

## POSIX Thread API (pthreads)

**Thread creation** [^src1]:
```c
pthread_t t;
int rc = pthread_create(&t, NULL, my_function, arg);
```
Returns immediately; the new thread starts executing my_function(arg) concurrently.

**Joining** (wait for thread completion) [^src1]:
```c
void *ret;
pthread_join(t, &ret);  // blocks until t finishes; ret = return value
```

**Locks** (mutexes) [^src1]:
```c
pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_lock(&m);
// critical section
pthread_mutex_unlock(&m);
```

**Condition variables** [^src1]:
```c
pthread_cond_t c = PTHREAD_COND_INITIALIZER;
pthread_cond_wait(&c, &m);    // atomically releases m and waits; re-acquires m before returning
pthread_cond_signal(&c);       // wake one waiting thread
pthread_cond_broadcast(&c);    // wake all waiting threads
```

## The Critical Section Problem

A **critical section** is a piece of code that accesses a shared resource and must not be concurrently executed by multiple threads. Without mutual exclusion, **data races** (undefined behavior from concurrent reads and writes) occur [^src1].

**Race condition**: the outcome depends on the interleaving of thread execution — a scheduling-dependent bug that may appear rarely in testing but cause catastrophic failures in production [^src1].

**Atomicity violation**: a code sequence that assumes multi-step operations appear atomic, but concurrent threads can interleave between the steps [^src2].

## Locks

A **lock** provides mutual exclusion: only one thread holds the lock at a time. All others requesting it block until it is released [^src1].

**Requirements for a good lock**:
1. **Correctness** — mutual exclusion
2. **Fairness** — threads shouldn't starve waiting for the lock
3. **Performance** — low overhead, especially under low contention

**Common lock implementations**:
- **Spinlock with test-and-set (TSL)**: busy-waits. Wastes CPU in single-CPU systems; OK when lock hold time is very short on multi-CPU.
- **Spinlock with test-and-test-and-set**: reduces bus traffic by reading the lock value before doing an atomic swap.
- **Yield-on-contention**: call yield() to give up the CPU instead of spinning.
- **OS-assisted sleep (futex/mutex_lock)**: when contended, put the thread to sleep in a wait queue and wake it when the lock is released.

**Recommendation**: always use well-tested, OS-provided mutex implementations (pthread_mutex_t). Implement locks yourself only for learning or special-case performance needs [^src1].

## Condition Variables

A **condition variable** lets a thread wait for a condition to become true without busy-waiting [^src2]:

```c
// Producer-consumer pattern
mutex_lock(&m);
while (buffer_full()) {          // always while, never if (spurious wakeups)
    cond_wait(&not_full, &m);    // releases m, sleeps; re-acquires m on wake
}
add_to_buffer(item);
cond_signal(&not_empty);
mutex_unlock(&m);
```

**Critical rule: always use `while`, not `if` around cond_wait**. Spurious wakeups (no guarantee the condition is true when woken) and the window between signal and re-acquiring the lock mean the condition must be re-checked [^src2].

**Parent-child synchronization (join)**: parent waits for child completion:
```c
// Child:
mutex_lock(&m); done = 1; cond_signal(&cv); mutex_unlock(&m);
// Parent:
mutex_lock(&m); while (!done) cond_wait(&cv, &m); mutex_unlock(&m);
```

## Common Concurrency Bugs

Researchers have studied concurrency bugs extensively. Four main categories [^src3]:

**1. Atomicity violations**: a code region assumes it runs atomically but doesn't. Example: thread A checks `if (ptr != NULL) { use(ptr); }` while thread B sets `ptr = NULL` between the check and use. Fix: lock the whole check-then-use sequence [^src3].

**2. Order violations**: thread A assumes it runs before thread B (e.g., A initializes data that B uses), but no synchronization enforces the order. Fix: use condition variables or semaphores to enforce ordering [^src3].

**3. Deadlock**: a cycle of lock dependencies where each thread holds a lock that another thread needs. Example: A holds L1 and waits for L2; B holds L2 and waits for L1. Both block forever [^src3].

Deadlock conditions (all four must hold):
- **Mutual exclusion**: a resource can only be held by one thread
- **Hold and wait**: a thread holds a resource while waiting for another
- **No preemption**: resources cannot be forcibly taken
- **Circular wait**: a cycle of waiting threads

Deadlock prevention strategies:
- **Lock ordering**: always acquire locks in the same global order (breaks circular wait)
- **trylock and backoff**: if trylock fails, release held locks and retry (breaks hold-and-wait)
- **Deadlock avoidance** (Banker's algorithm): keep system in safe states — rarely used in practice due to overhead

**4. Non-deadlock liveness bugs**: starvation, livelock (two threads keep retrying and backing off in sync).

## Concurrency Design Principles

From OSTEP's summary dialogue [^src4]:
1. **Keep it simple** — avoid complex thread interactions; use proven patterns (simple locking, producer-consumer queues)
2. **Only use concurrency when necessary** — premature thread introduction adds complexity without benefit
3. **Prefer parallelism abstractions** when available — Map-Reduce, task queues, futures — they hide the concurrency primitives behind safe interfaces

"Concurrent code can be nearly impossible to understand even for just a few lines" [^src4].

## Monitors (Deprecated Approach)

A **monitor** is a structured concurrency primitive from the early 1970s, introduced by Per Brinch Hansen and refined by Tony Hoare [^src6]. It merges synchronization into the class/object structure of object-oriented programming.

**Core idea**: declare methods of a class as monitor routines. The monitor guarantees that **only one thread can be active inside the monitor at a time** — enforced by an implicit lock on every method entry/exit [^src6].

```cpp
// pretend C++ monitor (not real syntax)
monitor class account {
    int balance = 0;
public:
    void deposit(int amount)  { balance += amount; }
    void withdraw(int amount) { balance -= amount; }
};
```

This is equivalent to a C++ class that acquires a `pthread_mutex_t` at the start of each method and releases it at the end [^src6].

Monitors also include **condition variables** for blocking/waking. The producer/consumer solution uses two CVs (`empty`, `full`) and a state variable (`fullEntries`) [^src6].

**Hoare semantics** (original, theoretical): `signal()` immediately transfers control to a waiting thread. Amenable to proofs but hard to implement in real systems [^src6].

**Mesa semantics** (Lampson and Redell at Xerox PARC, building the Mesa language): `signal()` is a **hint** only — it moves one waiting thread from blocked to runnable, but the signaling thread keeps running. The woken thread must **recheck the condition** because another thread may have changed state before the woken thread gets to run [^src6].

> "Always recheck the condition after being woken! Use while loops, not if statements, when checking conditions." [^src6]

All modern systems use Mesa semantics. The `while`-loop pattern for `cond_wait` (already in the Condition Variables section above) is precisely the consequence of Mesa semantics [^src6].

**`broadcast()`**: wakes all waiting threads, needed when a single signal might wake the wrong waiter (e.g., a memory allocator with waiters for different sizes). Carries risk of a **thundering herd** — all wake, only one proceeds, rest re-block [^src6].

**Java monitors**: Java added the `synchronized` keyword to achieve the same effect. The original Java had only a single per-object condition variable (`wait()`/`notify()`), forcing use of `notifyAll()` for producer-consumer. Java later added an explicit `Condition` class to fix this [^src6].

**Why monitors are deprecated**: they are not fundamentally more powerful than explicit `pthread_mutex_t` + `pthread_cond_t`. They fell out of fashion as C and POSIX became dominant and OOP languages adopted more explicit synchronization APIs. The conceptual contribution — the `while`-loop idiom and Mesa semantics — survived and is universal [^src6].

## Related Corpus Pages

- [/software-engineering/operating-systems.md](/software-engineering/operating-systems.md) — processes, context switches, timer interrupts underlying thread scheduling
- [/software-engineering/cpu-scheduling.md](/software-engineering/cpu-scheduling.md) — how the OS schedules threads onto CPUs
- [/software-engineering/distributed-systems-fallacies.md](/software-engineering/distributed-systems-fallacies.md) — distributed concurrency failures
- [/software-engineering/sources/ostep-operating-systems-three-easy-pieces.md](/software-engineering/sources/ostep-operating-systems-three-easy-pieces.md) — OSTEP source summary

---

[^src1]: [OSTEP Interlude: Thread API](../../raw/pdf/pdf-threads-api.md)
[^src2]: [OSTEP Condition Variables](../../raw/pdf/pdf-threads-cv.md)
[^src3]: [OSTEP Common Concurrency Problems](../../raw/pdf/pdf-threads-bugs.md)
[^src4]: [OSTEP Summary Dialogue on Concurrency](../../raw/pdf/pdf-threads-dialogue.md)
[^src5]: [OSTEP Ch. 26: Concurrency — An Introduction](../../raw/pdf/pdf-threads-intro.md)
[^src6]: [OSTEP Appendix D: Monitors (Deprecated)](../../raw/pdf/pdf-threads-monitors.md)
