---
type: source
domain: data-engineering
status: draft
sources:
  - path: raw/web/web-tristan-handy-dbt-summit-58ecab01.md
    channel: web
    ingested_at: 2026-06-30
  - path: raw/web/web-quigley-malcolm-dbt-summit-56f0d5c7.md
    channel: web
    ingested_at: 2026-06-30
  - path: raw/web/web-stefanos-nikolaou-dbt-summit-1b8b1886.md
    channel: web
    ingested_at: 2026-06-30
  - path: raw/web/web-thomas-antonakis-dbt-summit-9e1a8fe2.md
    channel: web
    ingested_at: 2026-06-30
  - path: raw/web/web-sarah-levy-dbt-summit-077eab41.md
    channel: web
    ingested_at: 2026-06-30
  - path: raw/web/web-training-and-certification-dbt-summit-50f698b5.md
    channel: web
    ingested_at: 2026-06-30
  - path: raw/web/web-thiago-baldim-dbt-summit-f3ed1a76.md
    channel: web
    ingested_at: 2026-07-01
  - path: raw/web/web-tobias-mao-dbt-summit-c440861b.md
    channel: web
    ingested_at: 2026-07-01
  - path: raw/web/web-tyson-doberneck-dbt-summit-22ef1bf7.md
    channel: web
    ingested_at: 2026-07-01
  - path: raw/web/web-vijay-singh-dbt-summit-6ce0c589.md
    channel: web
    ingested_at: 2026-07-01
  - path: raw/web/web-william-guicheney-dbt-summit-1f6f240a.md
    channel: web
    ingested_at: 2026-07-01
  - path: raw/web/web-william-tsu-dbt-summit-b8e50c79.md
    channel: web
    ingested_at: 2026-07-01
  - path: raw/web/web-xiaohan-li-dbt-summit-a45c0d64.md
    channel: web
    ingested_at: 2026-07-01
  - path: raw/web/web-yuna-yunnan-tang-dbt-summit-14ca8371.md
    channel: web
    ingested_at: 2026-07-01
  - path: raw/web/web-zhen-xing-dbt-summit-0552c755.md
    channel: web
    ingested_at: 2026-07-01
tags:
  - corpus/data-engineering
  - source
created: 2026-06-30
updated: 2026-07-01
---

# dbt Summit 2026 — Speakers & Training

**Sources**: Individual speaker bio pages + training page from `https://www.getdbt.com/dbt-summit/` (20 speaker bios, 1 training page). Collected 2026-06-28.

**Summary**: Speaker bios from dbt Summit 2026 and the training/certification catalog. Thin individually; collectively identify the key people and products in the dbt / analytics engineering ecosystem as of mid-2026.

## Notable speakers

**Tristan Handy** — Co-founder and President of Fivetran + dbt Labs. dbt used by 100,000+ teams (JetBlue, HubSpot, Dunelm, SunRun). 20+ years as data practitioner. Active newsletter and podcast on analytics engineering [^src1].

Note: Tristan Handy's role appears as both "Founder and CEO of dbt Labs" (bio text) and "Co-founder and President, Fivetran + dbt Labs" (speaker listing) — the Fivetran acquisition of dbt Labs appears to have occurred [^src1].

**Quigley Malcolm** — Senior Software Engineer at dbt Labs. Led the MetricFlow acquisition (2023). Maintains `dbt-core` OSS. On the Open Semantic Interchange (OSI) steering committee for cross-tool metric layer standardization [^src2].

**Stefanos Nikolaou** — Principal Analytics Engineer at Kaizen Gaming. Co-founder of the Athens dbt Meetup [^src3].

**Thomas Antonakis** — Principal Analytics Engineer at Kaizen Gaming. Leads AE organization of 50 engineers. Co-organizer of Athens dbt Meetup. Background: Statistics → BI → analytics engineering via ORFIUM in 2021 [^src4].

**Sarah Levy** — Co-Founder & CEO of Euno, described as "AI context platform for enterprise data." Positioned at the intersection of data governance and AI context [^src5].

**Benn Stancil** — Listed without title (notable industry figure in BI/data analytics commentary).

**Thiago Baldim** — Senior Manager, Data, SafetyCulture. Responsible for implementing SafetyCulture data infrastructure end-to-end; ensures right data access at the right time with quality and confidence [^src7].

**Tobias (Toby) Mao** — Director of Engineering, Fivetran (via acquisition of Tobiko Data, where he was Co-Founder & CTO, Sep 2022–Aug 2025). Previously Senior Staff SE at Airbnb and Architect at Netflix Experimentation Infrastructure. Background: BA Mathematics, Northwestern [^src8].

**Tyson Doberneck** — Senior Data Engineer, Obie Insurance. Designs scalable data architectures using Apache Iceberg, Snowflake, and dbt. Known for cutting warehouse costs and building AI analytics layers; previously at Toggle Insurance and USAA [^src9].

**Vijay Singh** — Lead, Data Science and Business Intelligence, Verisk Analytics (10+ years). Analytics-first mindset; designs modular pipelines for P&C insurance using Snowflake and dbt. Background: SAS-based modeling → cloud analytics engineering [^src10].

**William Guicheney** — Principal Analytics Engineer, Aimpoint Digital. 9+ years in analytics. Focuses on modern data platforms with dbt, Snowflake, Airbyte, and Sigma [^src11].

**William Tsu** — Staff Analytics Engineer, WHOOP. Scales analytics through strong data foundations and developer-friendly dbt workflows. Emphasizes analyst self-service + data quality governance. Previously Analytics Engineer at Blend (Revenue Operations) [^src12].

**XiaoHan Li** — Analytics Engineer & Consultant, Xebia. Expertise in ELT-driven Medallion Architecture, data modelling, and dbt architecture design [^src13].

**Yuna (Yunnan) Tang** — Senior Analytics Engineer, SafetyCulture. Career path: Commercial Finance Manager → Portfolio Analyst → Analytics Engineer (AMP Capital → SafetyCulture). Believes business domain understanding makes better engineers; focuses on getting engineer + analyst structure right for successful dbt projects [^src14].

**Zhen Xing** — Data Architect / Data Engineer, 74software (Axway). Full-stack expertise across cloud infrastructure, data engineering, and AI product management. Track record at TotalEnergies, Ubisoft; built enterprise Feature Stores and MLOps pipelines [^src15].

## Training catalog (dbt Summit 2026)

Six training sessions offered alongside the summit [^src6]:

| Course | Focus |
|---|---|
| Becoming a dbt Architect | Scaling dbt across teams; environments, permissions, secure project structures |
| Mastering Data Quality with dbt | Testing strategy, maintainable tests, CI quality gates |
| Operationalize Cost Visibility in dbt | Cost drivers, hotspots, team standards, cost-aware development |
| Getting Started with dbt | Foundational course: modeling, sources, testing, documentation, deployment |
| Governed & Scalable AI-Assisted Analytics with dbt | AI-assisted workflows in dbt with guardrails; what to govern, how to audit |
| Upgrade to dbt v2 | dbt v2.0 migration: SQL comprehension, column-level lineage |

The AI-assisted analytics course and the architect track reflect 2026 priorities: AI tooling integrated into the dbt workflow, and platform-scale governance.

## Pages populated

- [[data-engineering/dbt|dbt]] — updated: Tristan Handy role, 100K+ teams stat, Fivetran acquisition, v2 training
- [[data-engineering/semantic-layer|Semantic Layer]] — OSI (Open Semantic Interchange) cross-tool metric standardization mentioned

---

[^src1]: [Tristan Handy — dbt Summit Speaker Bio](../../../raw/web/web-tristan-handy-dbt-summit-58ecab01.md)
[^src2]: [Quigley Malcolm — dbt Summit Speaker Bio](../../../raw/web/web-quigley-malcolm-dbt-summit-56f0d5c7.md)
[^src3]: [Stefanos Nikolaou — dbt Summit Speaker Bio](../../../raw/web/web-stefanos-nikolaou-dbt-summit-1b8b1886.md)
[^src4]: [Thomas Antonakis — dbt Summit Speaker Bio](../../../raw/web/web-thomas-antonakis-dbt-summit-9e1a8fe2.md)
[^src5]: [Sarah Levy — dbt Summit Speaker Bio](../../../raw/web/web-sarah-levy-dbt-summit-077eab41.md)
[^src6]: [Training and Certification — dbt Summit](../../../raw/web/web-training-and-certification-dbt-summit-50f698b5.md)
[^src7]: [Thiago Baldim — dbt Summit Speaker Bio](../../../raw/web/web-thiago-baldim-dbt-summit-f3ed1a76.md)
[^src8]: [Tobias Mao — dbt Summit Speaker Bio](../../../raw/web/web-tobias-mao-dbt-summit-c440861b.md)
[^src9]: [Tyson Doberneck — dbt Summit Speaker Bio](../../../raw/web/web-tyson-doberneck-dbt-summit-22ef1bf7.md)
[^src10]: [Vijay Singh — dbt Summit Speaker Bio](../../../raw/web/web-vijay-singh-dbt-summit-6ce0c589.md)
[^src11]: [William Guicheney — dbt Summit Speaker Bio](../../../raw/web/web-william-guicheney-dbt-summit-1f6f240a.md)
[^src12]: [William Tsu — dbt Summit Speaker Bio](../../../raw/web/web-william-tsu-dbt-summit-b8e50c79.md)
[^src13]: [XiaoHan Li — dbt Summit Speaker Bio](../../../raw/web/web-xiaohan-li-dbt-summit-a45c0d64.md)
[^src14]: [Yuna (Yunnan) Tang — dbt Summit Speaker Bio](../../../raw/web/web-yuna-yunnan-tang-dbt-summit-14ca8371.md)
[^src15]: [Zhen Xing — dbt Summit Speaker Bio](../../../raw/web/web-zhen-xing-dbt-summit-0552c755.md)
