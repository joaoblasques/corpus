---
type: entity
domain: mlops
status: draft
sources:
  - path: raw/youtube/youtube-5abffC-K40c-microsoft-azure-fundamentals-certification-course-az-900-upd.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/youtube/youtube--pX5PjIYTJs-az-900-azure-fundamentals-full-course-2025-azure-complete-tu.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/youtube/youtube-0bNFkI_0jhc-azure-training-azure-tutorial-intellipaat.md
    channel: youtube
    ingested_at: 2026-06-15
aliases:
  - Azure
  - Microsoft Azure
  - AZ-900
  - Azure Fundamentals
  - Entra ID
  - Azure AD
  - Blob Storage
  - Cosmos DB
tags:
  - corpus/mlops
  - entity
created: 2026-06-15
updated: 2026-06-15
---

# Azure

**TL;DR**: Microsoft Azure is the **second-largest cloud provider** behind AWS, growing fast; strongest fit for .NET / PowerShell / Windows shops via native Visual Studio integration [^src3]. This page maps Azure's core services onto the [[mlops/cloud-computing-fundamentals|cloud fundamentals]] and covers the **AZ-900 (Azure Fundamentals)** certification scope — the entry-level exam these courses target [^src1][^src2].

## Resource organization hierarchy

Azure nests governance scopes top-down, with policies/permissions inherited downward [^src1][^src2]:

**Management Group → Subscription → Resource Group → Resource**

- **Subscription** — billing + access boundary; isolate workloads/departments [^src1][^src2].
- **Resource Group** — logical container; a resource belongs to exactly one RG; deleting the RG deletes its resources [^src1][^src2]. (The Intellipaat course's "apples vs. oranges in separate bags" analogy [^src3].)
- **Management Group** — container for subscriptions for enterprise governance [^src2].

## Service map (by layer)

| Layer | Services |
|---|---|
| **Compute** | Virtual Machines (IaaS), VM Scale Sets (auto-scale identical VMs), Availability Sets (fault/update domains), App Service (PaaS web apps), Azure Functions (serverless), Container Instances, AKS (Kubernetes), Azure Virtual Desktop [^src1][^src2] |
| **Storage** | Blob (object), Files (SMB/NFS share), Queue (async messages), Table (NoSQL); all live in a globally-unique **Storage Account** [^src1][^src2] |
| **Databases** | Azure SQL (relational), Cosmos DB (NoSQL) [^src1] |
| **Networking** | VNet (+ subnets/CIDR), NSG (firewall rules), VNet Peering, VPN Gateway, ExpressRoute (dedicated private link), Azure DNS, Load Balancer, Traffic Manager [^src1][^src2] |
| **Identity** | **Azure AD / Entra ID** (SSO, MFA), AD Connect (hybrid sync), RBAC (Reader/Contributor/Owner), Conditional Access [^src1][^src2] |
| **Management / governance** | ARM templates (IaC), Azure Arc (hybrid/multi-cloud), Blueprints, Azure Policy, Resource Locks, Advisor, Service Health, Monitor [^src2] |

## Storage tiers & redundancy

- **Access tiers**: Hot (frequent, fastest, costliest) → Cool (infrequent, 30-day min) → Archive (rare, 180-day min, slow rehydrate) [^src1][^src2].
- **Redundancy**: LRS (3 copies, one data center) → ZRS (across 3 AZs) → GRS (secondary region) → RA-GRS (read-access secondary) [^src2].

## AZ-900 fundamentals emphasis

Both AZ-900 courses agree on the conceptual core [^src1][^src2]: IaaS/PaaS/SaaS, public/private/hybrid cloud, **CapEx→OpEx**, high availability / fault tolerance, vertical vs. horizontal scaling and elasticity, **regions / availability zones / region pairs**, and cost tooling (pay-as-you-go, reserved capacity, pricing calculator, TCO). File2 is more hands-on (portal demos of VMs, Functions, networking, storage); File1 leans conceptual/exam-domain [^src1][^src2]. See [[mlops/cloud-computing-fundamentals|Cloud Computing Fundamentals]] for the provider-agnostic versions.

> The Intellipaat source [^src3] is largely a *why-Azure* pitch (security investment, free-tier credits, 54 regions / 140 countries, regional expansion) plus a VM-launch portal demo; its substantive points (resource groups, virtual networks as isolated clouds, pay-per-use VMs) are subsumed by the two AZ-900 courses above and corroborate them.

## See also

- [[mlops/cloud-computing-fundamentals|Cloud Computing Fundamentals]] — the concepts these services implement
- [[mlops/aws|AWS]] · [[mlops/gcp|GCP]] — peer providers (Azure VNet ≈ AWS VPC; Blob ≈ S3; Cosmos DB ≈ DynamoDB)
- [[mlops/infrastructure-as-code|Infrastructure as Code]] — ARM templates are Azure's native IaC
- [[mlops/README|MLOps hub]]

---

[^src1]: [Microsoft Azure Fundamentals AZ-900 (File1)](../../raw/youtube/youtube-5abffC-K40c-microsoft-azure-fundamentals-certification-course-az-900-upd.md) — IaaS/PaaS/SaaS [[03:04](../../raw/youtube/youtube-5abffC-K40c-microsoft-azure-fundamentals-certification-course-az-900-upd.md#t=03:04)], VMs [[59:46](../../raw/youtube/youtube-5abffC-K40c-microsoft-azure-fundamentals-certification-course-az-900-upd.md#t=59:46)], resource groups [[29:56](../../raw/youtube/youtube-5abffC-K40c-microsoft-azure-fundamentals-certification-course-az-900-upd.md#t=29:56)], regions/AZs [[01:03:44](../../raw/youtube/youtube-5abffC-K40c-microsoft-azure-fundamentals-certification-course-az-900-upd.md#t=01:03:44)]
[^src2]: [AZ-900 Azure Fundamentals Full Course (File2)](../../raw/youtube/youtube--pX5PjIYTJs-az-900-azure-fundamentals-full-course-2025-azure-complete-tu.md) — RBAC/hierarchy [[06:37](../../raw/youtube/youtube--pX5PjIYTJs-az-900-azure-fundamentals-full-course-2025-azure-complete-tu.md#t=06:37)], VNet/NSG [[32:31](../../raw/youtube/youtube--pX5PjIYTJs-az-900-azure-fundamentals-full-course-2025-azure-complete-tu.md#t=32:31)], storage tiers/redundancy [[51:39](../../raw/youtube/youtube--pX5PjIYTJs-az-900-azure-fundamentals-full-course-2025-azure-complete-tu.md#t=51:39)], App Service/Functions [[08:41](../../raw/youtube/youtube--pX5PjIYTJs-az-900-azure-fundamentals-full-course-2025-azure-complete-tu.md#t=08:41)]
[^src3]: [Azure Training Tutorial (Intellipaat)](../../raw/youtube/youtube-0bNFkI_0jhc-azure-training-azure-tutorial-intellipaat.md) — why Azure / .NET fit [[12:30](../../raw/youtube/youtube-0bNFkI_0jhc-azure-training-azure-tutorial-intellipaat.md#t=12:30)], regions [[16:09](../../raw/youtube/youtube-0bNFkI_0jhc-azure-training-azure-tutorial-intellipaat.md#t=16:09)], resource groups / virtual networks [[28:23](../../raw/youtube/youtube-0bNFkI_0jhc-azure-training-azure-tutorial-intellipaat.md#t=28:23)]
</content>
