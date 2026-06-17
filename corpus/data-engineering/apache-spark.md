---
type: entity
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2026-05-19-why-is-apache-spark-rdd-immutable.md
    channel: email
    ingested_at: 2026-06-11
  - path: raw/email/email-2026-06-09-i-spent-8-hours-learning-about-the-spark-out-of-memory-oom-e.md
    channel: email
    ingested_at: 2026-06-11
  - path: raw/web/the-basic-spark-concept-beginners-don-t-know.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/the-apache-spark-optimization-checklist.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/spark-tips-use-dataframe-api.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/spark-caching-explained-what-really-happens-under-the-hood.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/a-small-hands-on-project-to-2-your-apache-spark-learning-pro.md
    channel: web
    ingested_at: 2026-06-11
  - path: raw/web/web-10-minutes-to-learn-apache-spark-joins-with-a-hands-on-proje.md
    channel: web
    ingested_at: 2026-06-17
aliases:
  - Spark
  - Apache Spark
  - PySpark
  - RDD
  - Sort Merge Join
  - SMJ
  - Spark JOIN
tags:
  - corpus/data-engineering
  - entity
created: 2026-06-11
updated: 2026-06-17
---

# Apache Spark

**TL;DR.** Apache Spark is a distributed data-processing engine built on **immutable RDDs** (Resilient Distributed Datasets) and a **lazy execution model**: transformations build a plan (DAG), and only an **action** triggers actual computation [^src3]. Higher-level **DataFrames** compile down to RDDs but add the **Catalyst** query optimizer and **Tungsten** memory/execution engine, making them the recommended API over raw RDDs [^src1][^src5]. Immutability is the foundation enabling fault tolerance (lineage replay), lock-free concurrency, and safe caching [^src1]. The dominant operational failure is the **OOM error**, rooted in how Spark partitions data and divides executor memory among parallel tasks [^src2].

## Execution model: transformations, actions, lazy evaluation

Everything in Spark is either a **transformation** (describes what should happen — `select`, `filter`, `join`, `groupBy`) or an **action** (tells Spark to actually run — `count`, `show`, `collect`, `write`) [^src3]. Transformations are **lazy**: Spark builds a logical plan (a DAG) and waits, which lets it optimize the whole chain at once — combining steps, pushing filters down, and deciding how to split work across the cluster [^src3]. Nothing executes until an action appears; the driver then sends tasks to executors, which process data in parallel [^src3].

> "Transformations are planning. Actions are execution. That's the whole system." [^src3]

After an action completes, Spark **throws away intermediate results** — a later action on the same logic re-runs the entire DAG from source unless you cache [^src6].

### Execution hierarchy

The runtime is a set of JVM processes — a **Driver** and **Executors** — running on a cluster of machines, coordinated by a Cluster Manager (YARN, Kubernetes, or Standalone) [^src2][^src7]. The work hierarchy [^src2]:

- **Application** → has multiple **jobs** (one job per action).
- **Job** → split into **stages** at each shuffle boundary (`groupBy`, `join`). A stage is a segment executed without shuffling.
- **Stage** → a set of **tasks**, the smallest unit of execution; each task handles one **partition**.
- Tasks run in parallel within an executor via multithreading; parallelism is bounded by executor cores (one core per task by default, set via `spark.task.cpus`) [^src2][^src7].

## RDD immutability and lineage

An RDD is Spark's abstraction for data spread across a cluster. Once created, **it cannot be changed** — a transformation produces a *new* RDD recording the instructions, computed lazily [^src1]. Four reasons immutability is foundational [^src1]:

1. **Functional-programming roots** — pure functions, no side effects; predictable behavior when code runs on hundreds of machines.
2. **Concurrency without locks** — immutable data means no race conditions, no synchronization, no "who wrote last" corruption.
3. **In-memory computing** — once cached, an immutable block is valid until explicitly unpersisted; no cache-invalidation problem.
4. **Lineage and fault tolerance** — the "resilient" in RDD. Spark records a **lineage** graph of every transformation. When a node dies, it traces back and **replays** the transformations to rebuild lost data.

Lineage replay only works *because* RDDs are immutable: if inputs could change between the original run and the replay, the recovery would produce different results and the model collapses [^src1].

> "Immutability isn't a design quirk — it's the foundation that everything else in Spark stands on" [^src1].

**The tradeoff:** every transformation is a new object in memory. The real cost appears at materialization — memory pressure (caching), recomputation cost (no cache), and GC overhead. So the choice is **memory vs recomputation**, managed with selective `.persist()`/`.cache()` and checkpoints [^src1].

## DataFrame API, Catalyst, and Tungsten

DataFrames (introduced Spark 1.3) follow the same immutability and lazy rules as RDDs — `df.filter(...)` returns a new DataFrame — but add two engines on top [^src1][^src5]:

- **Catalyst** — the query optimizer. RDDs are a "black box" Spark cannot see inside, so it cannot optimize them; DataFrames carry column-level metadata that Catalyst uses [^src5]. It applies **rule-based optimization** (predicate pushdown, constant folding, projection pruning, null propagation, Boolean simplification) and **cost-based optimization** (CBO costs alternative plans and picks the cheaper), with the two working together [^src5]. Example: a filter written *after* a join gets pushed down before the join — and even pushed into the JDBC source (`PushedFilters`) — automatically [^src5].
- **Tungsten** — the execution engine (Project Tungsten, Spark 1.6). It stores data **off-heap in binary format** and generates **encoder code on the fly**, avoiding the expensive double serialization PySpark otherwise pays (Java/Scala ↔ Python via cloudpickle). Off-heap storage also reduces GC pauses since the data is out of the garbage collector's scope [^src5].

For PySpark especially, the DataFrame API is critical: serialization, not computation, is often the dominant cost, and DataFrames let you write Python while keeping data and processing in the efficient JVM/off-heap format [^src5]. The RDD-based MLlib API has been in maintenance mode since Spark 2.0; `spark.ml` (DataFrame-based) is the primary ML API [^src4][^src5]. See [[data-engineering/parquet|Parquet]] for the recommended analytical file format that pairs with Catalyst column pruning and predicate pushdown [^src4].

## Caching and persist mechanics

`.cache()` is shorthand for `.persist(StorageLevel.MEMORY_AND_DISK)`; `.persist()` lets you choose a **StorageLevel**: `MEMORY_ONLY` (fast, evicted silently when full), `MEMORY_AND_DISK` (spills instead of recomputing), `_SER` serialized variants (less memory, more CPU), `DISK_ONLY` and `OFF_HEAP` (always serialized), and a `_2` suffix for replication [^src6]. `MEMORY_AND_DISK` is the recommended default; treat cache as for speed, not correctness, since blocks can be evicted [^src4][^src6].

Critical gotchas under the hood [^src6]:

- **Caching is lazy.** `.cache()` only marks the plan (wrapping it in an `InMemoryRelation` logical operator). Always follow with a full action like `.count()` to force materialization — otherwise the next job recomputes everything.
- **Partial caching.** Caching is **block-level** (one block per partition) and **local + incremental** — each executor caches only the blocks it computes, only when computed. An action that touches a subset (`.take(10)`, `limit`) caches only those blocks; the rest silently recompute.
- **Plan-match sensitivity.** The cache is tied to the **analyzed** logical plan (before optimization). Two semantically identical queries with different analyzed plans won't match — Spark skips the cache and recomputes.
- **LRU eviction with no warning.** Cache competes with execution memory; Spark steals from the cache mid-job when tasks need execution memory. With `MEMORY_ONLY`, evicted blocks are gone and recomputed from source. Design jobs assuming eviction will happen.

## OOM errors and memory tuning

Executor memory is divided, not unlimited. Usable processing/storage memory is roughly `(spark.executor.memory − reserved 300MB) × spark.memory.fraction (0.6 default)`, with that pool split 50/50 between execution and storage via `spark.memory.storageFraction`; the remaining ~40% is user memory [^src7][^src4]. The Spark UI's Storage and Executors tabs show what's cached and what's in use [^src4].

Key tuning relationships from hands-on experiment [^src7]:

- More executor cores → more parallelism, but with fixed executor memory, **each task gets a smaller memory slice** (more tasks share the pool) → higher spill risk.
- More executor memory → larger per-task slice → fewer disk spills, better performance.
- **Partition size** sets per-task workload: larger partitions mean fewer tasks, longer per-task time, higher spill chance; smaller partitions mean more tasks but lower spill risk.
- Data type affects aggregation strategy — aggregating Strings forces the slower `SortAggregate` over `HashAggregate`.

Memory-specific checklist items [^src4]:

- For **PySpark, bump `memoryOverhead` to 20–25%** (default 10% / 384MB) — Arrow and pandas UDFs allocate native memory invisible to JVM metrics, causing YARN/K8s to kill executors mysteriously.
- **Don't `collect()` on the driver** — it pulls the whole dataset to one machine. Use `.take()`, `.takeSample()`, `.show()`. Past `spark.driver.maxResultSize` (1GB default) it errors out. The same applies to driver-side actions like `count`/`show` on huge results — an "architecture misunderstanding," not a Spark bug [^src3].
- **Watch for disk spills** (Spark UI Stages tab): "Spill (Memory)"/"Spill (Disk)" means data didn't fit — add partitions or memory. Spills are 10–100x slower than in-memory.
- **Off-heap memory** (`spark.memory.offHeap.enabled`) for heavy shuffles/joins bypasses GC pressure at the cost of a fixed allocation.

## Optimization checklist

Distilled production guidance [^src4]:

- **Use the DataFrame/Dataset API, not RDDs** — everything else depends on it (Catalyst, predicate pushdown, AQE, cost-based join reordering) [^src4][^src5].
- **Pick the right file format** — [[data-engineering/parquet|Parquet]] for analytics; a table format ([[data-engineering/apache-iceberg|Iceberg]] or Delta) for anything read repeatedly, for ACID, time travel, and planner stats. Always specify schema explicitly for CSV/JSON to avoid full-scan inference [^src4].
- **Splittable compression** — Snappy/LZ4/ZSTD, never GZIP (a single node must decompress the whole file). ZSTD runs parallel for shuffle as of Spark 4.x [^src4].
- **Partitioning** — tune `spark.sql.files.maxPartitionBytes` (128MB default) to file layout; target 2–4 partitions per core; coalesce after heavy filtering; repartition on join keys before multiple joins; use low-cardinality columns for `.partitionBy()` writes [^src4].
- **Filter early** — partition pruning and Dynamic Partition Pruning (default-on, multi-key in 4.x) avoid touching irrelevant data [^src4].
- **Joins** — broadcast small tables (<10MB default threshold); diagnose **skew** first (one task 10x longer than others is the problem ~80% of the time); use Storage Partition Join for co-partitioned DSv2 sources to skip shuffles [^src4].
- **Spark 4.x defaults** — AQE, DPP, and Prometheus metrics are default-on; stop double-configuring them; switch shuffle codec to ZSTD; consider Kryo serializer over default Java (2–10x faster) [^src4].
- **Read the Spark UI** — DAG, stage timeline, task distribution. Uneven task bars = skew; many stages = unnecessary shuffles; red bars = spills [^src4].
- **Break lineage** with `.localCheckpoint()` on long transformation chains to prevent deeply nested DAGs / stack overflows [^src4].

## JOIN strategies: Sort Merge Join (SMJ)

For large datasets, Spark defaults to **Sort Merge Join** (SMJ), observable in the Spark UI's SQL/DataFrame tab under the physical execution plan [^src8]. SMJ is not a Spark-exclusive technique — it has long existed in the database field.

The execution proceeds as: both datasets are (1) partitioned and sorted on the join key, then (2) merged by walking both sorted sequences in parallel. This requires a shuffle (the stage boundary in the DAG) when the two datasets are not already co-partitioned on the join key.

**Hands-on validation approach**: with 2 executor instances (2 cores, 4GB RAM each), submitting a join of the TPC-H `lineitem` (~2.6GB) and `orders` (~600MB) datasets on `o_orderkey` on a Dockerized Spark 4.0.0 Standalone cluster. `spark.sql.files.maxPartitionBytes=256MB` controls partition size at read time — larger value = larger partitions, fewer tasks, higher per-task memory pressure [^src8].

**Broadcast vs. SMJ**: Spark automatically broadcasts small tables (<10MB default threshold) — the optimization checklist item above. SMJ is the fallback when neither side qualifies for broadcast. For large-to-large joins, SMJ is correct; for large-to-small, ensure broadcast thresholds are tuned or explicitly use broadcast hints [^src4][^src8].

## Related pages

- [[data-engineering/parquet|Parquet]] — recommended columnar format for Spark analytics
- [[data-engineering/apache-iceberg|Apache Iceberg]] — table format enabling SPJ and planner stats
- [[data-engineering/dbt|dbt]], [[data-engineering/dimensional-modeling|Dimensional Modeling]] — adjacent transformation/modeling tooling
- [[data-engineering/databricks|Databricks]] — managed Spark platform; Lakeflow SDP for declarative pipelines

---

[^src1]: [Why is Apache Spark RDD Immutable?](../../raw/email/email-2026-05-19-why-is-apache-spark-rdd-immutable.md)
[^src2]: [I spent 8 hours learning about the Spark Out-Of-Memory (OOM) errors](../../raw/email/email-2026-06-09-i-spent-8-hours-learning-about-the-spark-out-of-memory-oom-e.md)
[^src3]: [The Basic Spark Concept Beginners Don't Know](../../raw/web/the-basic-spark-concept-beginners-don-t-know.md)
[^src4]: [The Apache Spark Optimization Checklist](../../raw/web/the-apache-spark-optimization-checklist.md)
[^src5]: [Spark Tips: Use DataFrame API](../../raw/web/spark-tips-use-dataframe-api.md)
[^src6]: [Spark Caching Explained: What Really Happens Under the Hood](../../raw/web/spark-caching-explained-what-really-happens-under-the-hood.md)
[^src7]: [A small hands-on project to 2× your Apache Spark learning process](../../raw/web/a-small-hands-on-project-to-2-your-apache-spark-learning-pro.md)
[^src8]: [10 Minutes to Learn Apache Spark JOINs with a Hands-On Project](../../raw/web/web-10-minutes-to-learn-apache-spark-joins-with-a-hands-on-proje.md)
