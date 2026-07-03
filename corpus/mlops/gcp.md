---
type: entity
domain: mlops
status: draft
sources:
  - path: raw/youtube/youtube-IUU6OR8yHCc-google-cloud-platform-full-course-gcp-tutorial-google-cloud.md
    channel: youtube
    ingested_at: 2026-06-15
aliases:
  - GCP
  - Google Cloud Platform
  - Google Cloud
  - BigQuery
  - Compute Engine
  - GKE
tags:
  - corpus/mlops
  - entity
created: 2026-06-15
updated: 2026-06-15
---

# GCP

**TL;DR**: Google Cloud Platform is the third-largest major cloud provider, running on Google's global fiber-connected data centers [^src1]. This page maps GCP's core services onto the [cloud fundamentals](/mlops/cloud-computing-fundamentals.md); GCP's standout services are **BigQuery** (serverless data warehouse) and **GKE** (the managed Kubernetes that Google originated) [^src1].

## Resource hierarchy

**Organization → Folder → Project → resources** — each **project** is the container for resources and the unit of billing [^src1]. Free tier provides a $300 credit for 90 days [^src1].

## Service map (by layer)

| Layer | Services |
|---|---|
| **Compute** | Compute Engine (IaaS VMs; general/compute/memory-optimized, GPU machine types), App Engine (PaaS), Cloud Functions (serverless), Cloud Run, **GKE** (Google Kubernetes Engine — control plane + worker nodes) [^src1] |
| **Storage** | Cloud Storage (object/blob buckets) [^src1] |
| **Databases** | Cloud SQL (managed MySQL/Postgres/SQL Server), **Bigtable** (key-value NoSQL, high-throughput), Firestore/Datastore (NoSQL), Spanner (globally-distributed relational), **BigQuery** (serverless analytics DW, SQL over petabytes) [^src1] |
| **Messaging** | Pub/Sub (streaming/messaging) [^src1] |
| **Networking** | VPC (global virtual network + subnets), Cloud Load Balancing, Cloud CDN (edge caching) [^src1] |
| **Identity** | IAM (role-based access; who can do what to which resource) [^src1] |

These map onto [cloud fundamentals](/mlops/cloud-computing-fundamentals.md): Compute Engine ↔ IaaS VMs, App Engine ↔ PaaS, Cloud Functions ↔ serverless, Cloud Load Balancing ↔ load balancing, Cloud Storage ↔ object storage, GKE ↔ container orchestration.

## Global infrastructure

Geographical **regions** contain independent **zones** (separate-infrastructure data centers); the course cites ~22–25 regions and ~67–76 zones plus ~140 points of presence and CDN edge locations [^src1]. Spreading resources across zones/regions delivers high availability and disaster recovery [^src1].

## See also

- [Cloud Computing Fundamentals](/mlops/cloud-computing-fundamentals.md) — the concepts these services implement
- [AWS](/mlops/aws.md) · [Azure](/mlops/azure.md) — peer providers (BigQuery ≈ Redshift/Synapse; GKE ≈ EKS/AKS; Cloud Storage ≈ S3/Blob)
- [Kubernetes](/software-engineering/kubernetes.md) — GKE is managed Kubernetes (software-engineering)
- [dbt](/data-engineering/dbt.md) / [Data Engineering](/data-engineering/README.md) — BigQuery is a common dbt warehouse target (data-engineering)
- [MLOps hub](/mlops/README.md)

---

[^src1]: [Google Cloud Platform Full Course (GCP Tutorial)](../../raw/youtube/youtube-IUU6OR8yHCc-google-cloud-platform-full-course-gcp-tutorial-google-cloud.md) — Cloud Functions [[10:32](../../raw/youtube/youtube-IUU6OR8yHCc-google-cloud-platform-full-course-gcp-tutorial-google-cloud.md#t=10:32)], project/resource hierarchy [[12:42](../../raw/youtube/youtube-IUU6OR8yHCc-google-cloud-platform-full-course-gcp-tutorial-google-cloud.md#t=12:42)], regions/zones [[18:50](../../raw/youtube/youtube-IUU6OR8yHCc-google-cloud-platform-full-course-gcp-tutorial-google-cloud.md#t=18:50)], Compute Engine [[23:54](../../raw/youtube/youtube-IUU6OR8yHCc-google-cloud-platform-full-course-gcp-tutorial-google-cloud.md#t=23:54)], App Engine [[31:58](../../raw/youtube/youtube-IUU6OR8yHCc-google-cloud-platform-full-course-gcp-tutorial-google-cloud.md#t=31:58)], GKE [[32:23](../../raw/youtube/youtube-IUU6OR8yHCc-google-cloud-platform-full-course-gcp-tutorial-google-cloud.md#t=32:23)], Cloud Storage [[42:48](../../raw/youtube/youtube-IUU6OR8yHCc-google-cloud-platform-full-course-gcp-tutorial-google-cloud.md#t=42:48)], IAM [[01:07:30](../../raw/youtube/youtube-IUU6OR8yHCc-google-cloud-platform-full-course-gcp-tutorial-google-cloud.md#t=01:07:30)], Bigtable [[03:12:39](../../raw/youtube/youtube-IUU6OR8yHCc-google-cloud-platform-full-course-gcp-tutorial-google-cloud.md#t=03:12:39)], BigQuery [[03:21:42](../../raw/youtube/youtube-IUU6OR8yHCc-google-cloud-platform-full-course-gcp-tutorial-google-cloud.md#t=03:21:42)]
</content>
