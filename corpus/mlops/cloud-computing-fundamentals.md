---
type: concept
domain: mlops
status: draft
sources:
  - path: raw/youtube/youtube-ZaA0kNm18pE-cloud-computing-explained-the-most-important-concepts-to-kno.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/youtube/youtube-5abffC-K40c-microsoft-azure-fundamentals-certification-course-az-900-upd.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/youtube/youtube--pX5PjIYTJs-az-900-azure-fundamentals-full-course-2025-azure-complete-tu.md
    channel: youtube
    ingested_at: 2026-06-15
aliases:
  - cloud computing
  - cloud fundamentals
  - IaaS
  - PaaS
  - SaaS
  - scaling
  - load balancing
  - high availability
  - serverless
  - availability zones
tags:
  - corpus/mlops
  - concept
created: 2026-06-15
updated: 2026-06-15
---

# Cloud Computing Fundamentals

**TL;DR**: The provider-agnostic concepts that recur across AWS, Azure, and GCP — **scaling, load balancing, autoscaling, serverless, storage classes, availability vs. durability, event-driven architecture, the IaaS/PaaS/SaaS spectrum, and the CapEx→OpEx shift**. Cloud computing is using someone else's servers over the internet, paying only for what you use for the time you use it [^src2][^src3]. These fundamentals make the per-provider entity pages ([[mlops/aws|AWS]], [[mlops/azure|Azure]], [[mlops/gcp|GCP]]) mostly a matter of mapping names onto the same ideas.

## Service models: IaaS / PaaS / SaaS

| Model | You manage | Provider manages | Example |
|---|---|---|---|
| **IaaS** | OS, runtime, app, patching | hardware, virtualization | VMs (EC2 / Azure VM / Compute Engine) [^src2] |
| **PaaS** | your app only | OS, runtime, patching | App Service, App Engine [^src2] |
| **SaaS** | nothing (consume as end-user) | everything | hosted apps [^src2] |

**"Lift and shift"** = migrating an on-prem app to cloud IaaS without modification [^src3]. Deployment types: **public** (shared, pay-per-use), **private** (dedicated, more control), and **hybrid** (mix; choose what stays private) [^src2][^src3].

## Scaling

- **Vertical scaling** — make one machine bigger (more CPU/RAM). Pre-cloud default; suffers **diminishing cost returns** (a 64 GB stick costs more than 4× a 16 GB one) and is a single point of failure [^src1][^src3].
- **Horizontal scaling** — clone the app across many smaller, cheaper machines; survives a node failure and is the cloud-preferred model [^src1][^src3].
- **Autoscaling / elasticity** — automatically add/remove instances in response to traffic or resource thresholds (e.g. scale out at 75% CPU, in at 25%) [^src1][^src3].

## Load balancing & availability

- **Load balancer** — a layer in front of horizontally-scaled instances that distributes traffic (round-robin, least-connections, lowest-utilization) and routes only to healthy hosts [^src1].
- **Availability** — percent uptime (e.g. "99.99…%"); increased via horizontal scaling + load balancing + spreading instances across **availability zones** (physically separate data centers within a region, with independent power/network) [^src1][^src2].
- **Durability** — protection of *stored data* from loss: the provider keeps multiple copies across machines/data centers and re-replicates after a failure [^src1].
- **Region pairs** (Azure framing) — each region paired with another 300+ miles away for disaster-recovery failover [^src2].

## Serverless

Originated with AWS Lambda: write code as a **function**, deploy it, and the provider runs/scales the underlying machines invisibly; you don't provision instances [^src1]. **Caveat**: the term has drifted — some "serverless" services (e.g. provisioned OpenSearch) still bill per underlying instance rather than per execution, which one source argues isn't true serverless [^src1].

## Event-driven architecture (EDA)

Contrast with the synchronous **request-response** model, where an orchestrator must know every downstream service (tight coupling) [^src1]. In EDA a **publisher** emits an event to a notification layer (SNS / EventBridge), which **fans out** copies to any number of **subscribers** — the producer no longer needs to know its consumers (**decoupling**) [^src1]. Pub/sub is the shorthand. Trade-off: distributed-state problems (e.g. compensating/cancel messages when one consumer fails) [^src1].

## Storage taxonomy

- **Object storage** — general blob store for media, JSON, CSV, byte streams (S3 / Blob Storage / Cloud Storage) [^src1].
- **Block storage** — attachable volumes/disks, autoscalable, can be shared across instances [^src1].
- **Databases** — relational (Postgres/MySQL/SQL Server), NoSQL (document/key-value/graph), plus in-memory **cache** [^src1].

## Cost model (CapEx → OpEx)

Cloud shifts spend from **capital expenditure** (upfront servers/hardware) to **operational expenditure** (recurring, usage-based) [^src3]. Pricing levers: **pay-as-you-go**, **reserved capacity** (1–3 year commitment for a discount), pricing calculators, and TCO estimators [^src3].

## See also

- [[mlops/aws|AWS]] · [[mlops/azure|Azure]] · [[mlops/gcp|GCP]] — the three providers these concepts map onto
- [[mlops/infrastructure-as-code|Infrastructure as Code]] — provisioning the resources above declaratively
- [[software-engineering/kubernetes|Kubernetes]] — container orchestration, the runtime layer above (software-engineering)
- [[software-engineering/cap-theorem|CAP Theorem]] / [[software-engineering/distributed-systems-fallacies|Distributed Systems Fallacies]] — the theory behind availability/partition trade-offs (software-engineering)
- [[mlops/README|MLOps hub]]

---

[^src1]: [Cloud Computing Explained (Be A Better Dev)](../../raw/youtube/youtube-ZaA0kNm18pE-cloud-computing-explained-the-most-important-concepts-to-kno.md) — scaling [[01:19](../../raw/youtube/youtube-ZaA0kNm18pE-cloud-computing-explained-the-most-important-concepts-to-kno.md#t=01:19)], load balancing [[05:40](../../raw/youtube/youtube-ZaA0kNm18pE-cloud-computing-explained-the-most-important-concepts-to-kno.md#t=05:40)], autoscaling [[08:20](../../raw/youtube/youtube-ZaA0kNm18pE-cloud-computing-explained-the-most-important-concepts-to-kno.md#t=08:20)], serverless [[10:32](../../raw/youtube/youtube-ZaA0kNm18pE-cloud-computing-explained-the-most-important-concepts-to-kno.md#t=10:32)], EDA [[16:37](../../raw/youtube/youtube-ZaA0kNm18pE-cloud-computing-explained-the-most-important-concepts-to-kno.md#t=16:37)], storage [[27:02](../../raw/youtube/youtube-ZaA0kNm18pE-cloud-computing-explained-the-most-important-concepts-to-kno.md#t=27:02)], availability/durability [[31:52](../../raw/youtube/youtube-ZaA0kNm18pE-cloud-computing-explained-the-most-important-concepts-to-kno.md#t=31:52)]
[^src2]: [Microsoft Azure Fundamentals AZ-900 (File1)](../../raw/youtube/youtube-5abffC-K40c-microsoft-azure-fundamentals-certification-course-az-900-upd.md) — IaaS/PaaS/SaaS [[03:04](../../raw/youtube/youtube-5abffC-K40c-microsoft-azure-fundamentals-certification-course-az-900-upd.md#t=03:04)], regions/AZs [[01:11:54](../../raw/youtube/youtube-5abffC-K40c-microsoft-azure-fundamentals-certification-course-az-900-upd.md#t=01:11:54)]
[^src3]: [AZ-900 Azure Fundamentals Full Course (File2)](../../raw/youtube/youtube--pX5PjIYTJs-az-900-azure-fundamentals-full-course-2025-azure-complete-tu.md) — CapEx/OpEx [[01:18](../../raw/youtube/youtube--pX5PjIYTJs-az-900-azure-fundamentals-full-course-2025-azure-complete-tu.md#t=01:18)], scaling/elasticity [[16:17](../../raw/youtube/youtube--pX5PjIYTJs-az-900-azure-fundamentals-full-course-2025-azure-complete-tu.md#t=16:17)], cloud models [[09:43](../../raw/youtube/youtube--pX5PjIYTJs-az-900-azure-fundamentals-full-course-2025-azure-complete-tu.md#t=09:43)]
</content>
