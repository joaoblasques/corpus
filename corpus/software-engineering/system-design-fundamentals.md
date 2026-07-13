---
type: concept
domain: software-engineering
status: draft
sources:
  - path: raw/youtube/youtube-C842vFY5kRo-system-design-course-apis-databases-caching-cdns-load-balanc.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-oYxTTirKY8M-system-design-explained-apis-databases-caching-cdns-load-bal.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-system-design-cou-report.md
    channel: notes
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-KuClyhvSzXk-every-frontend-system-design-pattern-w-senior-engineer-micro.md
    channel: youtube
    ingested_at: 2026-06-25
aliases:
  - system design
  - scalability
  - load balancing
  - horizontal scaling
  - vertical scaling
  - single point of failure
  - API design
  - REST
  - GraphQL
  - gRPC
  - DNS
  - round robin
  - consistent hashing
  - health checks
  - ephemeral environments
  - microfrontend
  - micro-frontend
  - BFF
  - backend for frontend
  - CDN
  - design system
  - API gateway
  - container systems
  - Conway's law
  - vertical slicing
tags:
  - corpus/software-engineering
  - concept
created: 2026-06-25
updated: 2026-06-25
---

# System Design Fundamentals

**TL;DR**: System design is the skill that separates mid-level from senior engineers — the ability to design from scratch, make trade-offs, and articulate architectural decisions [^src1][^src2]. Core building blocks: single-server → horizontal scaling → load balancer → database separation → caching → CDNs. API style (REST / GraphQL / gRPC) is chosen by use case. Vertical scaling hits a ceiling; horizontal scaling adds fault tolerance but requires a load balancer [^src1].

## The single-server starting point

Every system starts simple: one server runs the web app, database, and cache together [^src1]. Users reach it via DNS resolution (domain → IP) then HTTP requests. The server returns HTML/CSS/JS for browsers or JSON for mobile apps [^src1].

Insight: "starting small allows us to understand each core component before adding more complexity" [^src1].

## Scaling strategies

### Vertical scaling (scale up)

Add RAM/CPU to the existing server [^src1]. Simple, works for low-to-moderate traffic. Hard limits: there's a cap on how much one machine can hold, and a single server is a **single point of failure** [^src1].

### Horizontal scaling (scale out)

Replicate the server and distribute load [^src1]. Benefits:
- **Fault tolerance**: if one server goes down, others continue serving
- **Elasticity**: add/remove servers as traffic demands

Requires a **load balancer** to route requests across the server pool.

## Load balancing

Load balancers distribute incoming traffic, ensure no single server is overloaded, and detect failures via health checks [^src1].

### Load balancing algorithms

| Algorithm | How it works | Best for |
|---|---|---|
| **Round robin** | Each server gets a request in rotation | Uniform server specs |
| **Least connections** | Route to server with fewest active connections | Variable-length sessions |
| **Least response time** | Route to fastest-responding server with fewest connections | Heterogeneous server capacities |
| **IP hash** | Hash client IP → consistent server assignment | Session-sticky requirements |
| **Weighted** | Assign weights by server capacity; distribute proportionally | Mixed server specs |
| **Geo/location** | Route to geographically closest server | Global services, latency reduction |
| **Consistent hashing** | Hash ring maps clients to servers; minimizes remapping on server changes | Cache-affinity, distributed systems |

### Health checks

Load balancers continuously send health-check requests to all servers; if a server fails, it is removed from rotation until it recovers [^src1]. Same technique applies to load balancers themselves (multiple load balancers with health monitoring).

### Load balancer implementations

- **Software**: Nginx (also a web server), HAProxy (open-source)
- **Hardware**: F5, Citrix (high performance, high cost)
- **Cloud-managed**: AWS Elastic Load Balancing, Azure Load Balancer, Google Cloud Load Balancing (auto-scaling, monitoring included) [^src1]

## Single points of failure

Any component whose failure takes down the whole system [^src1]. Database is the canonical example — all API servers depend on it. Mitigations: **redundancy** (multiple load balancers, DB replicas), **health checks**, **self-healing** (auto-replace failed instances).

## Database selection

### Relational (SQL)

Structured tables with rows/columns; SQL query language [^src1]. ACID transactions:
- **Atomic**: entire transaction succeeds or fails as a unit
- **Consistent**: DB transitions between valid states only
- **Isolated**: concurrent transactions don't interfere
- **Durable**: committed data survives crashes

Use SQL when: data is well-structured with clear relationships; strong consistency is required (e-commerce orders, financial/banking) [^src1]. Examples: PostgreSQL, MySQL, SQLite.

### Non-relational (NoSQL)

Four subtypes [^src1]:

| Type | Example | Strength |
|---|---|---|
| **Document store** | MongoDB | Flexible nested JSON-like documents; denormalized single records |
| **Wide-column store** | Cassandra, Cosmos DB | Massive scale; high write throughput |
| **Graph store** | Neo4j, Amazon Neptune | Entity relationships; recommendation engines |
| **Key-value store** | Redis, Memcached | Primary RAM storage; extreme read/write speed |

Use NoSQL when: low latency is critical; data is unstructured/semi-structured; schema flexibility needed; massive volume with horizontal scale-out [^src1].

**Decision heuristic** [^src1]:

| Need | Choice |
|---|---|
| Well-structured data, complex joins | SQL |
| Strong ACID transactions (finance, banking) | SQL |
| Super low latency | NoSQL (key-value/document) |
| Flexible, dynamic schemas | NoSQL |
| Massive unstructured data volumes | NoSQL |

## API design styles

An API is "a contract that defines what requests can be made and what responses can be expected" [^src1]. It is an **abstraction mechanism** — callers don't need to know implementation details.

### REST (Representational State Transfer)

Stateless; each request is self-contained [^src1]. Standard HTTP verbs:
- `GET` — retrieve
- `POST` — create
- `PUT` / `PATCH` — update
- `DELETE` — remove

Most common for web and mobile applications.

### GraphQL

Single endpoint; client specifies exactly what fields it needs [^src1]. Operations: `query` (read), `mutation` (write), `subscription` (real-time). Key benefit: avoids over-fetching and multiple round-trips when complex UIs need data from several resources. Best for complex UIs with varied data requirements.

### gRPC

High-performance RPC framework using Protocol Buffers (binary serialization) [^src1]. Methods defined in `.proto` files; supports streaming and bidirectional communication. Least common of the three; favored for inter-service communication at high scale where performance is critical.

## System design as a career differentiator

> "Transitioning from a mid-level developer to a senior engineer requires shifting your focus from simply writing code to mastering high-level architectural design." [^src1]

Seniors are paid for architectural decisions, performance engineering, and trade-off articulation — not just executing clear requirements [^src1][^src2]. System design interviews now appear at nearly every senior/staff interview because companies can assess this thinking directly [^src2].

## Frontend system design patterns

Frontend engineers increasingly need system design fluency. "As AI is getting better at writing front-end code, your only choice to stay relevant and competitive as a front-end engineer is to level up your system design and architecture skills." [^src4]

### Micro-frontends

Analogy of microservices applied to the frontend. A **frontend monolith** is split into independent frontend applications, each deployable by its own team [^src4]. A **shell** application handles global state (auth, routing, language) and loads the micro-frontends inside it [^src4].

Benefits for AI-accelerated teams [^src4]:
- **Smaller surface area** → lower verification time per PR
- **Reduced blast radius** of a production bug
- Less context for the coding agent → more consistent output

**Conway's Law** predicts the architecture [^src4]: if you want smaller independent teams, you need small independent vertical slices.

### API gateway

Sits between the client and backend microservices. The client implements cross-cutting concerns (HTTPS, auth, rate limiting, caching) once at the gateway; backend services only handle their own logic [^src4]. Internal communication between services can be HTTP (not HTTPS) for performance, since it's inside a VPC [^src4].

### Backend for Frontend (BFF)

A dedicated backend owned by the frontend team, sitting between the API gateway and the microservices [^src4]. It allows frontend engineers to act as full-stack developers — modifying the API layer without needing another team's backlog. Multiple clients (desktop, mobile) each get their own BFF with an appropriate API shape; desktop may fetch more data at once, mobile needs smaller payloads [^src4].

GraphQL is frequently used to implement BFFs [^src4].

### CDN (Content Delivery Network)

A globally distributed edge cache. The server pushes static assets (JS/CSS/HTML) to edge nodes; clients are routed to the closest node, cutting round-trip latency — "data only travels as fast as the speed of light" [^src4]. CDNs also compress assets and manage cache policy. Cache hit = asset served from edge; cache invalidation = server pushes new version; **cache busting** = file-name hashing so clients get the new asset, not the stale cached one [^src4].

Node.js servers typically handle 2,000–10,000 concurrent requests; beyond that, horizontal scaling + load balancing is required [^src4].

### Design systems

A shared UI component library that prevents **visual divergence** across micro-frontend teams [^src4]. Components: **design tokens** (CSS custom properties for primary color, fonts, borders) → reusable inputs, buttons, layouts. Consistent design systems also increase AI coding agent output quality: "if you don't do that, the agent will make things up, and your UI would just look different" [^src4].

### OSI model and protocol selection

The application layer sits above TCP/UDP and chooses protocol based on use case [^src3]:

| Protocol | Transport | Best for |
|---|---|---|
| HTTP/HTTPS | TCP | Standard request/response web APIs |
| WebSockets | TCP | Bidirectional real-time (chat, live feeds) |
| gRPC | TCP (HTTP/2) | Inter-service, high-performance streaming |
| MQTT | TCP | IoT messaging (low bandwidth) |
| AMQP | TCP | Message queues |

TCP = reliable, ordered, connection-oriented. UDP = lightweight, low-latency, best-effort. [^src3]

### Authentication vs. authorization

Authentication answers *who* the user is (login → identity confirmed). Authorization answers *what they can do* (permissions, access control) — "auth is just the 1st step" [^src3].

## System design as a career differentiator

> "Transitioning from a mid-level developer to a senior engineer requires shifting your focus from simply writing code to mastering high-level architectural design." [^src3]

Seniors are paid for architectural decisions, performance engineering, and trade-off articulation — not just executing clear requirements [^src1][^src2]. System design interviews now appear at nearly every senior/staff interview because companies can assess this thinking directly [^src2].

## See also

- [Distributed Systems Fallacies](/software-engineering/distributed-systems-fallacies.md) — the eight assumptions that break in distributed systems
- [CAP Theorem](/software-engineering/cap-theorem.md) — consistency vs availability under network partition — the core distributed systems trade-off
- [Microservices](/software-engineering/microservices.md) — decomposed service architecture
- [Kubernetes](/software-engineering/kubernetes.md) — container orchestration for horizontal scaling
- [CI/CD and Progressive Delivery](/software-engineering/ci-cd.md) — deploying into this infrastructure

---

[^src1]: [System Design Course – APIs, Databases, Caching, CDNs, Load Balancing (freeCodeCamp / Alex Simonyan)](../../raw/youtube/youtube-C842vFY5kRo-system-design-course-apis-databases-caching-cdns-load-balanc.md)
[^src2]: [System Design Explained – APIs, Databases, Caching, CDNs (Hayk Simonyan)](../../raw/youtube/youtube-oYxTTirKY8M-system-design-explained-apis-databases-caching-cdns-load-bal.md)
[^src3]: [Report: System Design Course – APIs, Databases, Caching, CDNs (Obsidian analysis)](../../raw/notes/notes-00-inbox-clippings-youtube-raw-raw-watched-system-design-cou-report.md)
[^src4]: [Every Frontend System Design Pattern w/ Senior Engineer (theSeniorDev)](../../raw/youtube/youtube-KuClyhvSzXk-every-frontend-system-design-pattern-w-senior-engineer-micro.md)

<!-- RELATED:START (generated by bin/corpus_heal.py related — do not edit inside) -->

## Related across domains

- [Cloud Computing Fundamentals](/mlops/cloud-computing-fundamentals.md) · _mlops_
- [Networking Fundamentals (for DevOps/MLOps)](/mlops/networking-fundamentals.md) · _mlops_
- [Scaling Data Pipelines](/data-engineering/scaling-data-pipelines.md) · _data-engineering_
- [Stream Processing (and Batch vs Stream)](/data-engineering/stream-processing.md) · _data-engineering_

<!-- RELATED:END -->
