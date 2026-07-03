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
  - path: raw/email/email-2025-06-26-if-you-re-learning-apache-spark-this-article-is-for-you.md
    channel: email
    ingested_at: 2026-06-19
  - path: raw/pdf/pdf-1-fundamentals-of-big-data.md
    channel: pdf
    ingested_at: 2026-06-25
  - path: raw/pdf/pdf-4-pyspark-mllib.md
    channel: pdf
    ingested_at: 2026-06-25
  - path: raw/pdf/pdf-chapter1.md
    channel: pdf
    ingested_at: 2026-06-25
  - path: raw/pdf/pdf-chapter2.md
    channel: pdf
    ingested_at: 2026-06-25
  - path: raw/pdf/pdf-chapter3.md
    channel: pdf
    ingested_at: 2026-06-25
  - path: raw/youtube/youtube-761SQ9Hxbic-databricks-tutorial-databricks-free-edition-tutorial-with-en.md
    channel: youtube
    ingested_at: 2026-06-25
  - path: raw/pdf/pdf-2-intro-to-pyspark-rdd.md
    channel: pdf
    ingested_at: 2026-06-25
  - path: raw/github/github-stabrise-spark-pdf.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/pdf/pdf-3-intro-to-pyspark-dataframes-and-sql.md
    channel: pdf
    ingested_at: 2026-06-25
  - path: raw/github/github-josephmachado-efficient-data-processing-spark.md
    channel: github
    ingested_at: 2026-06-25
  - path: raw/web/web-apache-datafusion-comet-spark-accelerator-092a8375.md
    channel: web
    ingested_at: 2026-07-01
aliases:
  - Spark
  - Apache Spark
  - PySpark
  - RDD
  - Resilient Distributed Dataset
  - Pair RDD
  - spark-pdf
  - SparkPDF
  - MapReduce
  - narrow dependencies
  - wide dependencies
  - shuffle
  - Sort Merge Join
  - SMJ
  - Spark JOIN
  - Big Data fundamentals
  - PySpark MLlib
  - Catalyst optimizer
  - Photon query engine
  - SparkSession
  - lazy evaluation
  - PySpark DataFrame
  - PySpark SQL
  - DataFrame API
  - createOrReplaceTempView
  - toPandas
  - HandySpark
  - efficient data processing spark
tags:
  - corpus/data-engineering
  - entity
created: 2026-06-11
updated: 2026-07-01
last_confirmed: 2026-07-01
---

# Apache Spark

**TL;DR.** Apache Spark is a distributed data-processing engine built on **immutable RDDs** (Resilient Distributed Datasets) and a **lazy execution model**: transformations build a plan (DAG), and only an **action** triggers actual computation [^src3]. Higher-level **DataFrames** compile down to RDDs but add the **Catalyst** query optimizer and **Tungsten** memory/execution engine, making them the recommended API over raw RDDs [^src1][^src5]. Immutability is the foundation enabling fault tolerance (lineage replay), lock-free concurrency, and safe caching [^src1]. The dominant operational failure is the **OOM error**, rooted in how Spark partitions data and divides executor memory among parallel tasks [^src2].

## Origins: from MapReduce to Spark

In **2004 Google published the MapReduce paper**, introducing a programming paradigm to distribute data processing across hundreds or thousands of machines [^src9]. Users explicitly define two functions [^src9]:

- **Map** — takes key/value inputs, processes them, and outputs intermediate key/value pairs; all values of the same key are then grouped and passed to Reduce.
- **Reduce** — receives the intermediate values for a key and merges them with defined logic (Count, Sum, …).

To guarantee fault tolerance (e.g. a worker dies mid-process), MapReduce relies on **disk to exchange intermediate data** between tasks [^src9]. Yahoo released the open-source implementation (Hadoop MapReduce), which became the go-to for distributed processing — but it "wouldn't last long" [^src9]. The strict Map/Reduce paradigm limits flexibility, and disk-based exchange is poorly suited to **machine learning or interactive queries** [^src9].

UC Berkeley's **AMPLab** saw the inefficiency and built **Apache Spark**: a **functional-programming-based API** simplifying multistep applications, plus a new engine for efficient **in-memory data sharing** across computation steps [^src9]. At time of the source's writing Spark was on its **fourth major version**, but its core and fundamentals are stable [^src9].

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

An RDD is the central abstraction even when you never touch it directly: "No matter the abstraction you use, from dataset to dataframe, they are compiled into RDDs behind the scenes." [^src9] It represents an immutable, partitioned collection of records operable in parallel, with data kept in memory for as long as possible [^src9]. The Spark creators give three reasons immutability is required — **concurrent processing** (consistency across nodes/threads without complex synchronization or race conditions), **lineage and fault tolerance** (each transformation creates a new RDD, preserving lineage and allowing reliable recomputation — mutable RDDs would make this much harder), and **functional programming** principles (easier failure handling, maintained data integrity) [^src9] — corroborating the four reasons above.

### The five RDD properties

Each RDD has five key properties [^src9]:

1. **List of partitions** — an RDD is divided into partitions, Spark's units of parallelism; each is a logical subset processed independently on different executors.
2. **Computation function** — a function determining how to compute the data for each partition.
3. **Dependencies** — the RDD tracks its dependencies on other RDDs, describing how it was created (this is the lineage).
4. **Partitioner (optional)** — for key-value RDDs, specifies how data is partitioned (e.g. a hash partitioner).
5. **Preferred locations (optional)** — lists preferred locations for computing each partition (e.g. data-block locations in HDFS) for data-locality scheduling.

### Lazy transformations vs actions

When you define an RDD, its data is not transformed immediately — nothing happens until an **action** triggers execution, which lets Spark determine the most efficient way to run the transformations [^src9]:

- **Transformations** (`map`, `filter`) define *how* data should be transformed but don't execute until an action forces computation; because RDDs are immutable, each transformation produces a *new* RDD [^src9].
- **Actions** are the commands that produce output or store data, driving the actual execution [^src9].

### Fault tolerance via lineage

Spark RDDs achieve fault tolerance through **lineage** — the recorded series of transformations that created each RDD [^src9]. If any partition is lost to a node failure, Spark **reconstructs** it by reapplying the transformations to the original dataset described by the lineage, **eliminating the need to replicate data across nodes or write to disk** (unlike MapReduce) [^src9].

## Architecture: Driver, Cluster Manager, Executors

A Spark application consists of three roles [^src9]:

- **Driver** — the JVM process managing the entire application, from handling user input to distributing tasks to executors.
- **Cluster Manager** — manages the cluster of machines running the application; Spark works with **YARN, Apache Mesos, or its own standalone manager** [^src9].
- **Executors** — processes that run the tasks the driver assigns and report status/results; each application has its own set of executors.

The Spark driver-executor cluster is distinct from the cluster hosting the application: there must be a cluster of machines (or processes, if running locally) providing resources, and the cluster manager manages those machines — called **workers** — that can host driver and executor processes [^src9].

### Execution modes

Distinguished mainly by **where the driver process runs** [^src9]:

- **Cluster mode** — the driver launches on a worker node alongside executors; the cluster manager handles all application processes.
- **Client mode** — the driver stays on the client machine that submitted the application, which must maintain the driver throughout execution.
- **Local mode** — the entire application runs on a single machine, achieving parallelism via multiple threads; commonly used for learning or testing.

## Anatomy: Job → Stage → Task and the DAG

Spark organizes a workload as a hierarchy [^src9] (matching the execution hierarchy above [^src2]):

- **Job** — a series of transformations on data; the whole workflow from start to finish.
- **Stage** — a job segment executed *without* data shuffling; a job is split into stages wherever a transformation requires shuffling data across partitions.
- **DAG** — RDD dependencies are used to build a **Directed Acyclic Graph** of stages, ensuring stages are scheduled in topological order [^src9].
- **Task** — the smallest unit of execution; each stage is divided into multiple tasks executing in parallel across partitions.

### Narrow vs wide dependencies (and why shuffle = stage boundaries)

The "data shuffling" that splits jobs into stages comes from the dependency type [^src9]:

- **Narrow dependencies** — each child-RDD partition depends on a limited, known set of parent partitions: a single parent (e.g. `map`) or a specific known subset (e.g. `coalesce`). No shuffle needed.
- **Wide dependencies** — data must be repartitioned in a specific way, so a single parent partition contributes to *multiple* child partitions. This occurs with operations like **`groupByKey`, `reduceByKey`, or `join`**, which involve **shuffling** data. Consequently, wide dependencies result in **stage boundaries** in Spark's execution plan [^src9].

This is the mechanism behind the stage-split rule noted in the execution hierarchy: shuffles (wide deps) are exactly where one stage ends and the next begins [^src2][^src9].

## DataFrame API, Catalyst, and Tungsten

DataFrames (introduced Spark 1.3) follow the same immutability and lazy rules as RDDs — `df.filter(...)` returns a new DataFrame — but add two engines on top [^src1][^src5]:

- **Catalyst** — the query optimizer. RDDs are a "black box" Spark cannot see inside, so it cannot optimize them; DataFrames carry column-level metadata that Catalyst uses [^src5]. It applies **rule-based optimization** (predicate pushdown, constant folding, projection pruning, null propagation, Boolean simplification) and **cost-based optimization** (CBO costs alternative plans and picks the cheaper), with the two working together [^src5]. Example: a filter written *after* a join gets pushed down before the join — and even pushed into the JDBC source (`PushedFilters`) — automatically [^src5].
- **Tungsten** — the execution engine (Project Tungsten, Spark 1.6). It stores data **off-heap in binary format** and generates **encoder code on the fly**, avoiding the expensive double serialization PySpark otherwise pays (Java/Scala ↔ Python via cloudpickle). Off-heap storage also reduces GC pauses since the data is out of the garbage collector's scope [^src5].

For PySpark especially, the DataFrame API is critical: serialization, not computation, is often the dominant cost, and DataFrames let you write Python while keeping data and processing in the efficient JVM/off-heap format [^src5]. The RDD-based MLlib API has been in maintenance mode since Spark 2.0; `spark.ml` (DataFrame-based) is the primary ML API [^src4][^src5]. See [Parquet](/data-engineering/parquet.md) for the recommended analytical file format that pairs with Catalyst column pruning and predicate pushdown [^src4].

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
- **Pick the right file format** — [Parquet](/data-engineering/parquet.md) for analytics; a table format ([Iceberg](/data-engineering/apache-iceberg.md) or Delta) for anything read repeatedly, for ACID, time travel, and planner stats. Always specify schema explicitly for CSV/JSON to avoid full-scan inference [^src4].
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

## Big Data fundamentals: the 3 Vs and processing paradigms

"Big data" refers to datasets "too complex for traditional data-processing software" [^src10]. The classic framing — **Volume** (size), **Variety** (formats and sources), **Velocity** (speed) — defines what makes data "big" [^src10]. Key processing paradigms [^src10]:

| Paradigm | Meaning |
|---|---|
| **Clustered computing** | Collection of resources from multiple machines |
| **Parallel computing** | Simultaneous computation on a single machine |
| **Distributed computing** | Collection of networked nodes running in parallel |
| **Batch processing** | Break job into small pieces, run on individual machines |
| **Real-time processing** | Immediate processing of data as it arrives |

Hadoop/MapReduce was the first dominant distributed framework — scalable and fault-tolerant, but slow (disk-heavy) and inflexible (strict Map+Reduce paradigm, poorly suited to ML or interactive queries) [^src10]. Spark replaced it as the preferred framework — "open source, general purpose and lightning fast" with both batch and real-time support [^src10]. Nowadays single-node engines (DuckDB, Polars) challenge whether distributed processing is needed at all for medium-scale data [^src13]. See [DuckDB](/data-engineering/duckdb.md).

## PySpark: the Python API for Spark

Spark is written in Scala; **PySpark** is the Python interface, offering similar computation speed and APIs familiar to Pandas/scikit-learn users [^src10]. When to use PySpark [^src11]:

- Big data analytics and distributed data processing across clusters
- Real-time data streaming at scale
- Machine learning on large datasets (via MLlib)
- ETL/ELT pipelines across diverse data sources (CSV, JSON, Parquet, …)

### SparkSession

The entry point to all Spark functionality. In plain Python [^src11]:

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("MySparkApp").getOrCreate()
```

In **Databricks**, the `spark` object is pre-initialized — you do not need to create it [^src13]. See [Databricks](/data-engineering/databricks.md).

### Spark shells

Three interactive shells for prototyping [^src10]:

- `spark-shell` — Scala
- `pyspark-shell` — Python
- `SparkR` — R

### DataFrame operations (quick reference)

The DataFrame API is the recommended interface (over raw RDDs). Common operations [^src12]:

| Operation | Method | Example |
|---|---|---|
| Drop nulls | `.na.drop()` | `df.na.drop()` |
| Fill nulls | `.na.fill({col: val})` | `df.na.fill({"age": 0})` |
| Add column | `.withColumn(name, expr)` | `df.withColumn("profit", col("revenue") - col("budget"))` |
| Rename column | `.withColumnRenamed(old, new)` | `df.withColumnRenamed("age", "years")` |
| Drop column | `.drop(name)` | `df.drop("department")` |
| Filter rows | `.filter(condition)` | `df.filter(df["salary"] > 50000)` |
| Group & aggregate | `.groupBy(...).agg(...)` | `df.groupBy("dept").avg("salary")` |
| Select columns | `.select([cols])` | `df.select("title", "studio")` |
| Row count | `.count()` | `df.count()` |
| Distinct values | `.distinct()` | `df.select("industry").distinct()` |
| Describe stats | `.describe()` | count, mean, min, max per column |
| Schema | `.printSchema()` | prints column names and data types |

**Two filter syntaxes** (both equivalent) [^src13]:

```python
# syntax 1 — bracket notation
df.filter(df["release_year"].between(2000, 2010))
# syntax 2 — col() function from pyspark.sql.functions
from pyspark.sql.functions import col
df.filter((col("release_year") >= 2000) & (col("release_year") <= 2010))
```

### RDD vs DataFrame

| | **DataFrame** | **RDD** |
|---|---|---|
| Level | High-level, optimized | Low-level, flexible |
| Operations | SQL-like (select, filter, groupBy) | map(), filter(), collect() |
| Schema | Columns with data types (like SQL) | No schema — harder with structured data |
| Optimization | Catalyst + Tungsten | Black box — Spark can't optimize |
| Verbosity | Concise | Very verbose for complex ops |
| Recommendation | Always prefer for analytics | Use only when DataFrame can't do it |

> "No matter the abstraction you use, from dataset to dataframe, they are compiled into RDDs behind the scenes." [^src9]

Creating an RDD from a DataFrame [^src11b]:

```python
census_rdd = census_df.rdd
census_rdd.collect()   # pulls all data to driver — use carefully!
```

Key RDD methods [^src11b]:
- `rdd.map(fn)` — apply a function (including lambdas) to every element
- `rdd.filter(fn)` — keep only elements where fn returns True
- `rdd.collect()` — retrieve all data from the cluster to the driver
- `sc.parallelize(list)` — create an RDD from a Python list

### Reading and writing files

```python
# Read CSV with header + inferred schema
df = spark.read.option("header", True).option("inferSchema", True).csv("/path/file.csv")

# Specify schema explicitly (preferred for production)
from pyspark.sql import types as t
schema = [t.StructField("order_date", t.DateType()), ...]
df = spark.read.schema(schema).csv("/path/file.csv")

# Write as Parquet
df.write.mode("overwrite").parquet("/path/output.parquet")
```

**Volumes in Databricks**: upload raw files to a Volume (not a table); the path is then `/Volumes/catalog/schema/volume/file.csv` [^src13].

### SQL in PySpark: two styles

```python
# Style 1: Python API
result = spark.sql("SELECT studio, COUNT(*) FROM workspace.default.movies GROUP BY studio")

# Style 2: magic SQL in notebooks (Databricks)
# %sql
# SELECT studio, COUNT(*) FROM workspace.default.movies GROUP BY studio

# Create a temp view from a DataFrame to run SQL against it
df.createOrReplaceTempView("weather")   # session-scoped
df.createGlobalTempView("weather")      # cluster-scoped (accessible from other notebooks)
```

[^src13]

### Spark plan internals (`.explain()`)

When you call `.explain("extended")` on a DataFrame, Spark prints four plan stages [^src13]:

1. **Parsed logical plan** (unresolved) — the raw query tree
2. **Analyzed logical plan** (resolved) — catalog validates tables/columns exist; assigns column IDs
3. **Optimized logical plan** — Catalyst applies optimizations (filter pushdown, null propagation, combined predicates); optimizations happen *before* execution
4. **Physical plan** — how to execute on the cluster (scan, filter, project, column→row conversion for output)

Key insight: **Catalyst pushes filters before selects** in the optimized plan, even if your code writes `select` first then `filter` — so writing "natural" code is fine [^src13]. The Photon executor (C++, vectorized) handles actual execution; it operates on the physical plan and scans only the columns needed (projection pushdown automatic) [^src13]. See [Databricks](/data-engineering/databricks.md) for Photon details.

## PySpark MLlib

MLlib is the **machine learning component** of Apache Spark [^src10b]. It provides distributed ML algorithms designed for parallel processing on a cluster — unlike scikit-learn, which only works on a single machine [^src10b].

### Three algorithm categories ("the three Cs")

1. **Collaborative filtering** — recommender systems; finds users/items with common interests; implemented via **ALS (Alternating Least Squares)** [^src10b]
2. **Classification** — identifying category membership (Binary and Multiclass: Linear SVMs, logistic regression, decision trees, random forests, gradient-boosted trees, naïve Bayes); also **Regression** (linear least squares, Lasso, ridge, isotonic) [^src10b]
3. **Clustering** — grouping data by similar characteristics (K-means, Gaussian mixture, Bisecting K-means, Streaming K-means) [^src10b]

Additional MLlib capabilities: featurization (feature extraction, transformation, dimensionality reduction), ML Pipelines (constructing, evaluating, tuning workflows) [^src10b].

### ALS collaborative filtering example

```python
from pyspark.mllib.recommendation import ALS, Rating

# Create Rating tuples (user, product, rating)
r1 = Rating(user=1, product=1, rating=1.0)
ratings = sc.parallelize([r1, r2, r3])

# Train model
model = ALS.train(ratings, rank=10, iterations=10)

# Predict
unrated = sc.parallelize([(1, 2), (1, 1)])
predictions = model.predictAll(unrated)

# Evaluate: MSE = mean of (actual - predicted)^2
```

**Train/test split**: use `data.randomSplit([0.6, 0.4])` to split an RDD into training (60%) and test (40%) sets [^src10b].

> Note: the RDD-based MLlib API has been in maintenance mode since Spark 2.0; `spark.ml` (DataFrame-based) is the recommended ML API for new code.

## Databricks Free Edition (entry point for Spark learners)

Databricks offers a **free edition** for learning — the only compute available is **serverless compute** (analogous to AWS Lambda: servers exist but are fully managed/hidden) [^src13]. Useful for:

- Learning Spark and the lakehouse pattern without managing clusters
- Unity Catalog exploration (catalog → schema → tables/volumes hierarchy)
- **Genie** — natural-language-to-SQL chatbot embedded in the Databricks UI [^src13]
- SQL Editor with serverless compute attached for ad-hoc queries
- Notebook-based development with the pre-initialized `spark` object

The **catalog → schema → tables/volumes** hierarchy: a workspace has catalogs, each catalog has schemas (databases), each schema has tables (registered data) and volumes (raw file storage) [^src13]. See [Databricks](/data-engineering/databricks.md) for the full platform overview.

## Pair RDDs (key-value RDDs)

Real-world datasets are usually key-value pairs. A **Pair RDD** is an RDD of `(key, value)` tuples — a special data structure enabling key-aware transformations [^src14].

**Creating Pair RDDs** (two approaches) [^src14]:

```python
# From a list of tuples
my_tuple = [('Sam', 23), ('Mary', 34), ('Peter', 25)]
pairRDD = sc.parallelize(my_tuple)

# From a regular RDD via map
my_list = ['Sam 23', 'Mary 34', 'Peter 25']
regularRDD = sc.parallelize(my_list)
pairRDD = regularRDD.map(lambda s: (s.split(' ')[0], s.split(' ')[1]))
```

**Pair RDD transformations** [^src14]:

| Transformation | Behavior |
|---|---|
| `reduceByKey(func)` | Combines values with the same key (parallel, commutative + associative required) |
| `groupByKey()` | Groups all values with the same key |
| `sortByKey()` | Returns an RDD sorted by key (ascending or descending) |
| `join()` | Joins two Pair RDDs on their key (inner join) |

Example: `reduceByKey` sums values per key [^src14]:
```python
rdd = sc.parallelize([("Messi", 23), ("Ronaldo", 34), ("Messi", 24)])
rdd.reduceByKey(lambda x, y: x + y).collect()
# [('Ronaldo', 34), ('Messi', 47)]
```

**Pair RDD actions** [^src14]:

| Action | Returns |
|---|---|
| `countByKey()` | Dict of key → count |
| `collectAsMap()` | Dict of key → value (last value wins if duplicate keys) |

**`saveAsTextFile()`** saves an RDD as a text file; `coalesce(1)` before it consolidates to one file [^src14]:
```python
RDD.coalesce(1).saveAsTextFile("output/")
```

## PySpark DataFrame and SQL (Big Data Fundamentals, ch.3)

**PySpark SQL** is the Spark library for structured data — it provides schema information and computation context (unlike low-level RDDs) [^src16]. A **PySpark DataFrame** is an **immutable distributed collection of data with named columns**, designed for both structured (relational DB) and semi-structured (JSON) data. The DataFrame API is available in Python, R, Scala, and Java [^src16].

### SparkSession vs SparkContext

- `SparkContext` — main entry point for creating **RDDs**
- `SparkSession` — entry point for **DataFrames**; used to create DataFrames, register them as temp views, and execute SQL queries; available in PySpark shell as `spark` [^src16]

### Creating DataFrames

```python
# From an existing RDD
names = ['Model', 'Year', 'Height', 'Width', 'Weight']
iphones_df = spark.createDataFrame(iphones_RDD, schema=names)

# From CSV / JSON / TXT (SparkSession.read)
df_csv  = spark.read.csv("people.csv", header=True, inferSchema=True)
df_json = spark.read.json("people.json")
df_txt  = spark.read.txt("people.txt")
```
`header=True` promotes the first row to column names; `inferSchema=True` auto-detects data types [^src16].

### Key DataFrame transformations and actions

| Method | Type | Description |
|---|---|---|
| `select('col')` | Transformation | Subset columns |
| `filter(df.Age > 21)` | Transformation | Filter rows by condition |
| `groupby('col')` | Transformation | Group for aggregation |
| `orderBy('col')` | Transformation | Sort by columns |
| `dropDuplicates()` | Transformation | Remove duplicate rows |
| `withColumnRenamed('old','new')` | Transformation | Rename a column |
| `printSchema()` | Method | Print column types (not a Spark action) |
| `show(n)` | Action | Print first n rows (default 20) |
| `count()` | Action | Row count |
| `columns` | Attribute | List column names |
| `describe()` | Action | Summary statistics for numeric columns |

[^src16]

### DataFrame API vs SQL queries

Both styles produce identical results — choose by preference [^src16]:

```python
# API style
result_df = df.groupby('Age').count().orderBy('Age')

# SQL style
df.createOrReplaceTempView("test_table")
result_df = spark.sql("SELECT Age, max(Purchase) FROM test_table GROUP BY Age")
```

The `sql()` method takes a SQL statement as a string and returns a DataFrame [^src16].

### Pandas vs PySpark DataFrame

| | Pandas | PySpark |
|---|---|---|
| Location | In-memory, single-server | Distributed across cluster |
| Evaluation | Eager (result on operation) | Lazy (builds DAG, executes on action) |
| Mutability | Mutable | Immutable |
| API coverage | More operations | Less, but sufficient for most DE tasks |

`df.toPandas()` converts a PySpark DataFrame to Pandas — **avoid on large data** (pulls all data to the driver node) [^src16].

### Visualization with PySpark DataFrames

Three methods for visualizing in notebooks [^src16]:
- **pyspark_dist_explore** — `hist()`, `distplot()`, `pandas_histogram()` directly on Spark columns
- **toPandas() + Pandas plotting** — simple but dangerous on large datasets
- **HandySpark** — `df.toHandy()` then `hdf.cols["Age"].hist()` — keeps distributed computation, easy fetching

## Efficient Data Processing in Spark (course reference)

The `josephmachado/efficient_data_processing_spark` GitHub repo (★385) is the code companion to an **"Efficient Data Processing in Spark" course** [^src17]. Key setup details:

- Uses **Docker** + **Docker Compose v2** for local Spark environment; Mac M1/later requires replacing `FROM deltaio/delta-docker:latest` with `FROM deltaio/delta-docker:latest_arm64` in the Spark Dockerfile [^src17].
- **Makefile** for command aliases: `make restart` (stop+start containers), `make setup` (create data for exercises).
- Includes a capstone project under `capstone/rainforest/`, a real-world data-processing scenario.
- Also covers **MinIO** (S3-compatible object storage) alongside PySpark — a popular local alternative to cloud storage when developing Spark pipelines locally.

Topics: `apache-spark`, `data-engineering`, `data-pipeline`, `minio`, `pyspark`, `pyspark-notebook`.

## Reading PDFs into Spark DataFrames (spark-pdf)

**spark-pdf** (StabRise, ★82) is a PDF DataSource for Apache Spark that lets you read PDF files directly into DataFrames and perform OCR on them using **Tesseract** [^src15]:

```python
# Read a directory of PDFs as a Spark DataFrame
df = spark.read.format("pdf").load("/path/to/pdfs/")
df.show()  # rows contain extracted text per page
```

Key features: Tesseract-backed OCR, Spark-native DataSource API (Scala, published to Maven Central), supports large-scale batch PDF processing on a cluster. Topics: data-extraction, PDF document processing, big-data, OCR [^src15].

Use case in data engineering: extracting structured data from document stores (contracts, reports, medical records) at scale, feeding downstream NLP pipelines or search indexes.

## Apache DataFusion Comet (Spark native accelerator)

Apache DataFusion Comet is a Rust/Arrow-based native execution plugin for Spark, replacing Spark's JVM-based executor for supported operations [^src18]. It slots in via JAR + config, requiring no SQL changes; when an operator is unsupported Comet falls back to Spark transparently (`spark.comet.explainFallback.enabled=true` logs the fallback reason) [^src18].

**Installation path (Databricks)** [^src18]:
1. Download pre-built JAR from Maven for the target Spark version (e.g. `comet-common-spark4.0_2.13-0.16.0.jar` for Spark 4.0/DBR 17.3)
2. Upload JAR to a Databricks Volume; write an `init.sh` that copies it to `/databricks/jars/`
3. Add Spark configs to the cluster: `spark.plugins=org.apache.spark.CometPlugin`, `spark.shuffle.manager=org.apache.spark.sql.comet.execution.shuffle.CometShuffleManager`
4. Attach the init script to an All-Purpose cluster

**Practical notes** [^src18]:
- Pre-built JARs now available on Maven (previously required building from source — an earlier pain point)
- A large `compatibility.json` details which operators fall back to Spark; reading it is required to assess how much an actual workload will benefit
- Configuration surface is large (1000+ config keys); no "most important ones" guide exists yet — a UX gap
- The author's recommendation for Spark in 2026: "if someone is using Spark, they better be using Databricks" — Comet is one more reason (runs directly on DBR clusters)

**Maturity signal**: the primary criticism of Comet (and similar OSS accelerators) is developer-experience gaps — poor discoverability of JARs, complex config, missing conceptual overview — vs tools like DuckDB or Databricks that prioritize DX first [^src18].

## Related pages

- [Parquet](/data-engineering/parquet.md) — recommended columnar format for Spark analytics
- [Apache Iceberg](/data-engineering/apache-iceberg.md) — table format enabling SPJ and planner stats
- [dbt](/data-engineering/dbt.md), [Dimensional Modeling](/data-engineering/dimensional-modeling.md) — adjacent transformation/modeling tooling
- [Databricks](/data-engineering/databricks.md) — managed Spark platform; Lakeflow SDP for declarative pipelines
- [DuckDB](/data-engineering/duckdb.md) — single-node alternative for medium-scale analytics

---

[^src1]: [Why is Apache Spark RDD Immutable?](../../raw/email/email-2026-05-19-why-is-apache-spark-rdd-immutable.md)
[^src2]: [I spent 8 hours learning about the Spark Out-Of-Memory (OOM) errors](../../raw/email/email-2026-06-09-i-spent-8-hours-learning-about-the-spark-out-of-memory-oom-e.md)
[^src3]: [The Basic Spark Concept Beginners Don't Know](../../raw/web/the-basic-spark-concept-beginners-don-t-know.md)
[^src4]: [The Apache Spark Optimization Checklist](../../raw/web/the-apache-spark-optimization-checklist.md)
[^src5]: [Spark Tips: Use DataFrame API](../../raw/web/spark-tips-use-dataframe-api.md)
[^src6]: [Spark Caching Explained: What Really Happens Under the Hood](../../raw/web/spark-caching-explained-what-really-happens-under-the-hood.md)
[^src7]: [A small hands-on project to 2× your Apache Spark learning process](../../raw/web/a-small-hands-on-project-to-2-your-apache-spark-learning-pro.md)
[^src8]: [10 Minutes to Learn Apache Spark JOINs with a Hands-On Project](../../raw/web/web-10-minutes-to-learn-apache-spark-joins-with-a-hands-on-proje.md)
[^src9]: [If you're learning Apache Spark, this article is for you (Vu Trinh)](../../raw/email/email-2025-06-26-if-you-re-learning-apache-spark-this-article-is-for-you.md)
[^src10]: [Fundamentals of Big Data (Big Data Fundamentals with PySpark, DataCamp)](../../raw/pdf/pdf-1-fundamentals-of-big-data.md)
[^src10b]: [PySpark MLlib (Big Data Fundamentals with PySpark, DataCamp)](../../raw/pdf/pdf-4-pyspark-mllib.md)
[^src11]: [Introduction to PySpark — Chapter 1 (DataCamp)](../../raw/pdf/pdf-chapter1.md)
[^src11b]: [Resilient Distributed Datasets in PySpark — Chapter 3 (DataCamp)](../../raw/pdf/pdf-chapter3.md)
[^src12]: [Data Manipulation with DataFrames — Chapter 2 (DataCamp)](../../raw/pdf/pdf-chapter2.md)
[^src13]: [Databricks Tutorial | Databricks Free Edition End-to-End (codebasics)](../../raw/youtube/youtube-761SQ9Hxbic-databricks-tutorial-databricks-free-edition-tutorial-with-en.md)
[^src14]: [Intro to PySpark RDD — Big Data Fundamentals with PySpark (DataCamp)](../../raw/pdf/pdf-2-intro-to-pyspark-rdd.md)
[^src15]: [StabRise/spark-pdf — PDF DataSource for Apache Spark](../../raw/github/github-stabrise-spark-pdf.md)
[^src16]: [Intro to PySpark DataFrames and SQL — Big Data Fundamentals with PySpark, ch.3 (DataCamp)](../../raw/pdf/pdf-3-intro-to-pyspark-dataframes-and-sql.md)
[^src17]: [josephmachado/efficient_data_processing_spark — Efficient Data Processing in Spark course repo](../../raw/github/github-josephmachado-efficient-data-processing-spark.md)
[^src18]: [Apache Datafusion Comet (Spark Accelerator) — hands-on review on Databricks (Data Engineering Central)](../../raw/web/web-apache-datafusion-comet-spark-accelerator-092a8375.md)
