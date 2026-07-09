---
type: concept
domain: software-engineering
status: draft
sources:
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
  - POSIX threads
  - pthreads
tags:
  - corpus/software-engineering
  - concept
created: 2026-07-09
updated: 2026-07-09
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

## Related Corpus Pages

- [/software-engineering/operating-systems.md](/software-engineering/operating-systems.md) — processes, context switches, timer interrupts underlying thread scheduling
- [/software-engineering/cpu-scheduling.md](/software-engineering/cpu-scheduling.md) — how the OS schedules threads onto CPUs
- [/software-engineering/distributed-systems-fallacies.md](/software-engineering/distributed-systems-fallacies.md) — distributed concurrency failures
- [/software-engineering/sources/ostep-operating-systems-three-easy-pieces.md](/software-engineering/sources/ostep-operating-systems-three-easy-pieces.md) — OSTEP source summary

---

[^src1]: [OSTEP Interlude: Thread API](../../raw/_inbox/pdf-threads-api.md)
[^src2]: [OSTEP Condition Variables](../../raw/_inbox/pdf-threads-cv.md)
[^src3]: [OSTEP Common Concurrency Problems](../../raw/_inbox/pdf-threads-bugs.md)
[^src4]: [OSTEP Summary Dialogue on Concurrency](../../raw/_inbox/pdf-threads-dialogue.md)
