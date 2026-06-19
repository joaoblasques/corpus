---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/web/what-is-an-etl-pipeline-examples-tools-updated-2026.md
    channel: web
    ingested_at: 2026-06-16
aliases:
  - ETL pipeline
  - ETL
  - extract transform load
  - ELT
  - extract load transform
  - ETL vs ELT
  - data pipeline
  - streaming ETL
  - batch ETL
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-16
updated: 2026-06-16
---

# ETL Pipeline

**TL;DR.** An ETL pipeline extracts data from source systems, transforms it into a usable format, and loads it into a destination such as a data warehouse, data lake, or operational tool[^src1]. ETL stands for **Extract, Transform, Load** — three sequential steps defining this category of data pipeline, the foundation of business intelligence, analytics, ML, and operational reporting[^src1]. ETL is a *subset* of data pipelines; all ETL pipelines are data pipelines, but not all data pipelines are ETL pipelines[^src1].

## The three steps

- **Extract** — ingest data from a source or multiple sources (APIs, websites, data lakes, SaaS apps, relational/transactional databases)[^src1]. Because the pipeline is a separate system from the source, it needs an integration interface; extraction can be **real-time** (as soon as data appears) or **batch** (picked up at a set interval)[^src1].
- **Transform** — convert raw extracted data into a form compatible with the destination and use case[^src1]. Common processing: filtering, aggregation, data cleaning, feature extraction, and re-shaping to conform to a schema — simple enough to automate, ensuring data arrives "clean, consistent, and won't cause errors"[^src1]. Complex exploratory analysis happens later in the lifecycle[^src1].
- **Load** — write data into the target/destination (the inverse of extraction): data warehouses, SaaS apps, operational business systems, or visualizations/dashboards[^src1]. After loading you can measure **latency** — hours, minutes, or down to the millisecond with real-time streaming[^src1].

See [[data-engineering/pipeline-layers|Pipeline Layers]] for the staging→warehouse→marts separation downstream of load, [[data-engineering/data-ingestion-patterns|Data Ingestion Patterns]] for stream-vs-batch extraction, and [[data-engineering/change-data-capture|Change Data Capture (CDC)]] for one real-time extraction mechanism.

## ETL pipeline vs data pipeline

A **data pipeline** is any system that moves data from source to destination — including ETL, ELT, streaming, CDC replication, and reverse ETL[^src1]. ETL is a sub-category serving a subset of those tasks; the terms are often used interchangeably for historical reasons (ETL was among the first pipeline architectures to gain enterprise popularity, when you had to build your own rather than buy a tool)[^src1]. Two things set ETL apart[^src1]:

- A generic data pipeline **does not by definition have a transformation step** (though it almost always should).
- **ETL pipelines explicitly end with loading** — transformation occurs *between* extract and load. In other pipelines transformation can occur after loading (ELT) or in more complex multi-step flows.

## ETL vs ELT

ETL transforms data **before** loading; **ELT** loads raw data first and transforms it **inside the destination warehouse** — the difference is the order of the last two steps[^src1].

- **ETL** dominated when on-premises warehouses had limited compute and storage was expensive[^src1].
- **ELT** became dominant once cloud warehouses (Snowflake, BigQuery, Redshift) made it cost-effective to load raw data first and transform at the destination[^src1]. (This is the model [[data-engineering/dbt|dbt]] and [[data-engineering/pipeline-layers|Pipeline Layers]] are built around.)
- **ETL is still preferred** when source data must be cleaned before storage, when destinations have limited compute, when compliance requires transformation before persistence, or when streaming transformations are required in flight[^src1].
- ELT's main advantage is **time** (no transform latency before load); its drawback is dumping disorganized/unclean — possibly corrupt — data into the store[^src1].

## 2026 trends

- **Real-time ETL becoming the standard** — low-latency pipelines delivering fresh data in milliseconds (user behavior tracking, fraud detection, supply chains)[^src1].
- **ETL automation + AI integration** — AI-driven tools automating transformations, anomaly detection, and on-the-fly schema adjustment[^src1].
- **Serverless and cloud-native ETL** — pipelines that scale on demand and eliminate infrastructure maintenance[^src1].

## Benefits and limitations

**Benefits**: centralizing data from various sources; reduced time to analysis (data arrives ready to use); deeper analytics by automating tedious transforms; easy operationalization (piping data straight to operational apps); ample tooling and support; and data-quality assurance (transforming before loading keeps corrupt data out, optionally with automated testing)[^src1].

**Main limitation**: traditional ETL relies on **batch processing**, introducing delay — unacceptable for fraud detection, fast-paced inventory, or capturing an online sale before the customer leaves[^src1]. Real-time pipelines with in-flight transformation exist but rely on streaming infrastructure and "you won't hear these kinds of pipelines called 'ETL,'" because technically they are very different processes despite the same goal[^src1]. See [[data-engineering/stream-processing|Stream Processing]] for the batch-vs-stream decision, streaming engines, and delivery guarantees.

## Tooling and use cases

The article lists eight 2026 ETL/ELT tools: **Estuary** (streaming ETL + real-time CDC), **AWS Glue** (serverless, Spark-based), **Azure Data Factory**, **Google Cloud Dataflow**, **Integrate.io**, **IBM DataStage**, **Oracle Data Integrator (ODI)**, and **Matillion** (cloud-DB push-down)[^src1]. Note: Estuary is the publishing vendor (estuary.dev), so the list is vendor-authored — treat ordering as promotional, not ranked[^src1].

Real-world use cases span online-review sentiment analysis, ride-hailing/transit analytics, aviation data, oil-and-gas sensor analytics, social-media/video platform analytics, retail/eCommerce (Walmart, Amazon), and healthcare (warehousing patient/medication data plus streaming patient-monitor alerts)[^src1].

[^src1]: [What Is An ETL Pipeline? Examples, Tools (Updated 2026)](../../raw/web/what-is-an-etl-pipeline-examples-tools-updated-2026.md)
