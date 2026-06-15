---
type: entity
domain: mlops
status: draft
sources:
  - path: raw/youtube/youtube-OGYEXGy8ca4-aws-explained-the-most-important-aws-services-to-know.md
    channel: youtube
    ingested_at: 2026-06-15
  - path: raw/youtube/youtube-Qz3Mjk_7D0Y-do-this-instead-of-watching-endless-tutorials-how-i-d-learn.md
    channel: youtube
    ingested_at: 2026-06-15
aliases:
  - AWS
  - Amazon Web Services
  - EC2
  - S3
  - Lambda
  - DynamoDB
tags:
  - corpus/mlops
  - entity
created: 2026-06-15
updated: 2026-06-15
---

# AWS

**TL;DR**: Amazon Web Services is the largest cloud provider (~30% of global cloud infrastructure, ahead of Azure ~25% and GCP ~13%) [^src2]. It has 300+ services, but ~50 matter and far fewer need depth [^src1]. This page maps the important services onto the [[mlops/cloud-computing-fundamentals|cloud fundamentals]], framed (per the source) by building an e-commerce app end-to-end [^src1].

## Service map (by layer)

| Layer | Services |
|---|---|
| **DNS / edge** | Route 53 (DNS, health checks, geo/latency routing), CloudFront (CDN) [^src1] |
| **Compute** | EC2 (rent VMs), Lightsail ("EC2 for dummies"), ECS + Fargate (containers, serverless variant), EKS (Kubernetes), **Lambda** (serverless functions) [^src1] |
| **Storage** | **S3** (object/blob), EBS (block, one instance), EFS (shared file system) [^src1] |
| **Databases** | RDS + Aurora (relational; Aurora has a scale-to-zero serverless tier), **DynamoDB** (key-value NoSQL), DocumentDB (Mongo), Keyspaces (Cassandra), Neptune (graph), OpenSearch [^src1] |
| **Caching** | ElastiCache (Redis/Memcached; purges on node loss), MemoryDB (durable cache) [^src1] |
| **APIs / security** | Elastic Load Balancer, **API Gateway** ("front door"), WAF, Shield (DDoS), Cognito (auth), Certificate Manager [^src1] |
| **Messaging** | **SNS** (pub/sub topics), **SQS** (queues), EventBridge (event bus + rules + scheduler), Step Functions (workflows), MWAA (managed Airflow) [^src1] |
| **Analytics** | EMR, Athena (SQL on S3), Glue (serverless ETL), Redshift (columnar DW), QuickSight (BI), Kinesis (streaming ingest) [^src1] |
| **AI** | Bedrock (foundation models, incl. Anthropic), SageMaker (build/train/deploy), Rekognition, Polly, Transcribe [^src1] |
| **Observability** | CloudWatch (logs/metrics/alarms), CloudTrail (audit), Config, X-Ray (tracing) [^src1] |
| **CI/CD + IaC** | CodeBuild/CodeDeploy/CodePipeline, **CloudFormation** (YAML/JSON templates), **CDK** (IaC in real languages) [^src1] |
| **Identity / network** | IAM (users + roles + policies), Identity Center, **VPC**, VPN, PrivateLink [^src1] |

These map directly onto [[mlops/cloud-computing-fundamentals|cloud fundamentals]]: ELB ↔ load balancing, Lambda ↔ serverless, SNS/SQS/EventBridge ↔ event-driven architecture, S3/EBS ↔ object/block storage, VPC ↔ cloud networks.

## Serverless lean

The source repeatedly favors serverless: **Lambda** (functions, scale-to-zero), **Fargate** (serverless containers), **Aurora Serverless** (scale-to-zero database), **Glue** (serverless ETL) — low maintenance, pay-for-use [^src1]. IAM **roles** ("a construction hat" — predefined permissions assumed by infrastructure) vs. **users** (people) is the core access-control distinction [^src1].

## Learning roadmap (getting hired)

A four-step path from a data/AI engineer [^src2]:

1. **Foundations** — active (hands-on) learning beats 40-hour passive videos; ~80–90% retention vs. low retention for one-way video [^src2].
2. **AWS Cloud Practitioner exam** — consolidates learning; passing one cert gives 50% off the next, so the first effectively pays for the second [^src2].
3. **Solutions Architect Associate** — recommended even for specialists: "go wide before you go deep" across networking, databases, security, compute; end-to-end system design interviews better than DE-specific knowledge [^src2].
4. **Build 2–3 real projects** with defensible architecture decisions; use the free tier and set budgets from day one ("easy to burn money in cloud") [^src2].

> The source advises **skipping professional-tier certs** (~$300, low ROI) — for professionals, actual experience outweighs the certificate; spend the money on projects instead [^src2].

## See also

- [[mlops/cloud-computing-fundamentals|Cloud Computing Fundamentals]] — the concepts these services implement
- [[mlops/azure|Azure]] · [[mlops/gcp|GCP]] — the other two major providers
- [[mlops/infrastructure-as-code|Infrastructure as Code]] — CloudFormation/CDK are AWS's IaC tools
- [[data-engineering/sources/aws-duckdb-etl-fargate|DuckDB ETL on ECS Fargate]] — a concrete AWS ETL build (data-engineering)
- [[mlops/README|MLOps hub]]

---

[^src1]: [AWS Explained: The Most Important AWS Services (Be A Better Dev)](../../raw/youtube/youtube-OGYEXGy8ca4-aws-explained-the-most-important-aws-services-to-know.md) — Route 53/CloudFront [[00:26](../../raw/youtube/youtube-OGYEXGy8ca4-aws-explained-the-most-important-aws-services-to-know.md#t=00:26)], compute [[13:26](../../raw/youtube/youtube-OGYEXGy8ca4-aws-explained-the-most-important-aws-services-to-know.md#t=13:26)], databases [[25:12](../../raw/youtube/youtube-OGYEXGy8ca4-aws-explained-the-most-important-aws-services-to-know.md#t=25:12)], messaging [[36:53](../../raw/youtube/youtube-OGYEXGy8ca4-aws-explained-the-most-important-aws-services-to-know.md#t=36:53)], IaC [[54:43](../../raw/youtube/youtube-OGYEXGy8ca4-aws-explained-the-most-important-aws-services-to-know.md#t=54:43)], IAM [[01:00:48](../../raw/youtube/youtube-OGYEXGy8ca4-aws-explained-the-most-important-aws-services-to-know.md#t=01:00:48)]
[^src2]: [How I'd Learn AWS FAST (Jash Radia)](../../raw/youtube/youtube-Qz3Mjk_7D0Y-do-this-instead-of-watching-endless-tutorials-how-i-d-learn.md) — market share [[00:52](../../raw/youtube/youtube-Qz3Mjk_7D0Y-do-this-instead-of-watching-endless-tutorials-how-i-d-learn.md#t=00:52)], active learning [[02:10](../../raw/youtube/youtube-Qz3Mjk_7D0Y-do-this-instead-of-watching-endless-tutorials-how-i-d-learn.md#t=02:10)], Cloud Practitioner [[03:28](../../raw/youtube/youtube-Qz3Mjk_7D0Y-do-this-instead-of-watching-endless-tutorials-how-i-d-learn.md#t=03:28)], Solutions Architect [[04:47](../../raw/youtube/youtube-Qz3Mjk_7D0Y-do-this-instead-of-watching-endless-tutorials-how-i-d-learn.md#t=04:47)], projects [[07:49](../../raw/youtube/youtube-Qz3Mjk_7D0Y-do-this-instead-of-watching-endless-tutorials-how-i-d-learn.md#t=07:49)]
</content>
