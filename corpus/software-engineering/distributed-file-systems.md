---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/_inbox/pdf-dist-intro.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-dist-nfs.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-dist-afs.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-dist-dialogue.md
    channel: pdf
    ingested_at: 2026-07-09
  - path: raw/_inbox/pdf-dialogue-distribution.md
    channel: pdf
    ingested_at: 2026-07-09
aliases:
  - distributed systems
  - distributed file systems
  - NFS
  - AFS
  - client-server
  - stateless protocol
  - idempotent
  - cache consistency
  - callback promise
tags:
  - corpus/software-engineering
  - concept
created: 2026-07-09
updated: 2026-07-09
---

# Distributed File Systems

TL;DR: Distributed systems add **failure** as a central concern — machines, disks, and networks all fail unpredictably. NFS (Sun, 1985) solved the distributed file system problem via a **stateless server protocol** (each request is self-contained; idempotent operations allow retry on any failure) and client-side caching with periodic revalidation. AFS (Carnegie Mellon, 1983) improved scalability via **client-side whole-file caching** and **callback promises** (server notifies clients of changes instead of clients polling), dramatically reducing server load.

## Why Distributed Systems

A single machine providing shared persistent storage fails if that machine fails. Distributing across multiple machines provides:
- **Availability**: if one machine fails, others continue
- **Scalability**: many machines can serve many more clients than one
- **Shared access**: users on different machines see the same data [^src1]

**Central challenge: failure**. In a distributed system, individual components fail while others continue. The goal is to make the system appear to clients as if it never fails — even though individual components fail regularly [^src1].

**Two problems**:
1. **Communication failure**: messages may be lost or delayed. Cannot distinguish a slow response from a dead server.
2. **Partial failure**: some machines fail while others keep running, leaving shared state inconsistent [^src1].

**Fundamental communication primitive**: RPC (Remote Procedure Call). Hides network communication behind a function call interface. Challenges: what happens when the RPC fails mid-execution? Must design each RPC to be **idempotent** (safe to re-execute multiple times with the same effect) to enable retry on failure [^src1].

## NFS: Sun Network File System

**Design goal (1985)**: allow a client machine to access files stored on a server, transparently — the same file system API works whether the file is local or remote [^src2].

**Key design choice: stateless server**. The server keeps no state between client requests. Every request from the client includes all information the server needs to process it — file handle, offset, byte count — without relying on server-maintained open-file state [^src2].

**Why stateless?** Crash recovery is trivial: the server can reboot, and clients simply retry their requests with no lost state. A stateful server would need complex crash recovery to restore all client connection state [^src2].

**Idempotent operations**: because clients retry failed requests, server operations must be idempotent — sending the same request multiple times must produce the same result as sending it once. `READ(file, offset, count)` is idempotent; `WRITE(file, offset, data)` is idempotent (overwrites same bytes). `APPEND` would not be — NFS avoids it [^src2].

**File handle**: a server-side opaque identifier for a file (volume ID + inode number + generation number). Clients pass file handles back on each request — the server does not track who has what open [^src2].

**Client-side caching**: NFS clients cache file blocks locally to reduce server load and latency. **Cache consistency problem**: if client A caches a block that client B then modifies on the server, A's cache is stale [^src2].

**NFS cache consistency solution**: on open(), check with the server if the cached version is still fresh (compare client modification time with server modification time). If stale, re-fetch. This **close-to-open consistency** is weaker than full coherence — two clients may see different versions of a file temporarily — but is practical [^src2].

**NFS write semantics**: NFS commits writes to the server synchronously (before returning to client) to ensure durability. This limits write performance but guarantees that a server crash doesn't lose acknowledged writes [^src2].

## AFS: Andrew File System

**Design goal (Carnegie Mellon, 1983)**: scale to thousands of clients per server — NFS's polling-based cache consistency doesn't scale to large deployments [^src3].

**Key insight**: most files are read much more than they are written, and most opens of a file are by the same user across sessions. Aggressive client-side caching + server callbacks exploit this pattern [^src3].

**Whole-file caching**: on open(), AFS fetches the **entire file** to the client's local disk. Subsequent reads/writes go to the local disk copy, not the server. On close(), if modified, the updated file is sent back to the server [^src3].

**Callback promises**: instead of clients polling the server to check for updates, the server maintains state about which clients have cached each file. When a file is modified, the server sends a **callback** to all clients with cached copies, invalidating their caches [^src3].

**Scalability win**: a client that has a file cached and receives no callback can read that file indefinitely without contacting the server — entirely server-load-free. Server load is proportional to file modifications, not reads [^src3].

**AFS vs NFS consistency**:
- NFS: client checks freshness on each open (periodic revalidation). Server is stateless.
- AFS: server tracks cache holders; sends callback on modification. Server is stateful.
- AFS provides stronger consistency guarantees within a session but is stateful — server crashes require rebuilding callback state [^src3].

**AFS namespace**: a global shared namespace (`/afs/...`) accessible from any AFS client anywhere — not tied to one server's hostname. Files can migrate between servers without changing their path [^src3].

## Related Corpus Pages

- [/software-engineering/file-systems.md](/software-engineering/file-systems.md) — local file systems: inode layout, journaling, FFS, LFS, RAID
- [/software-engineering/distributed-systems-fallacies.md](/software-engineering/distributed-systems-fallacies.md) — eight fallacies; network reliability and latency assumptions that fail in production
- [/software-engineering/microservices.md](/software-engineering/microservices.md) — distributed systems at the application service layer
- [/software-engineering/sources/ostep-operating-systems-three-easy-pieces.md](/software-engineering/sources/ostep-operating-systems-three-easy-pieces.md) — OSTEP source summary

---

[^src1]: [OSTEP Distributed Systems Introduction](../../raw/_inbox/pdf-dist-intro.md)
[^src2]: [OSTEP NFS: Sun's Network File System](../../raw/_inbox/pdf-dist-nfs.md)
[^src3]: [OSTEP AFS: Andrew File System](../../raw/_inbox/pdf-dist-afs.md)
