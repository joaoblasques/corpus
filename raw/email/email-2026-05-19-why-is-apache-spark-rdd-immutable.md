---
channel: email
source: gmail
gmail_message_id: 19e405ad6923d329
from: luminousmen <luminousmen+apache-spark-under-the-hood@substack.com>
subject: Why is Apache Spark RDD Immutable?
date_received: 2026-05-19
pointer: false
collected_at: 2026-06-11
links:
  - {url: "https://substack.com/redirect/cccd7bcb-4420-4291-9b56-44467581b42a?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 9, file: raw/web/learning-spark-lightning-fast-data-analytics-damji-jules-s-w.md}
  - {url: "https://substack.com/redirect/fe421191-1699-42f9-abbd-f68237a1a446?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 9, file: raw/web/high-performance-spark-best-practices-for-scaling-and-optimi.md}
  - {url: "https://substack.com/redirect/ff61972b-28db-483a-bf34-9fc8d9a00f0d?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 9, file: raw/web/advanced-analytics-with-pyspark-patterns-for-learning-from-d.md}
  - {url: "https://substack.com/redirect/b90cf084-ea56-4426-bc75-57f746d45e94?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 8, file: raw/web/spark-caching-explained-what-really-happens-under-the-hood.md}
  - {url: "https://substack.com/redirect/35dc0f08-e38f-4cfe-85f4-d427e1746e80?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 8, file: raw/web/spark-tips-use-dataframe-api.md}
  - {url: "https://substack.com/redirect/52f73239-d9ea-4f35-b27a-faa63801ecc8?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 7, file: raw/web/the-apache-spark-optimization-checklist.md}
corpus_ingested: true
corpus_ingested_at: 2026-06-11
corpus_pages:
  - corpus/data-engineering/apache-spark.md
---

View this post on the web at https://luminousmen.substack.com/p/why-is-apache-spark-rdd-immutable

When I’m interviewing data engineers, I like to ask why Spark RDDs are immutable. It’s a simple question, but the answers tell me a lot — whether someone actually understands distributed systems or just learned the API.
What is RDD?
RDD stands for Resilient Distributed Dataset. It’s not a list, and not an array — it’s Spark’s abstraction for “a bunch of data spread across a cluster”. You do transformations on it, and Spark records what you asked for and creates a new RDD using those instructions. It doesn’t compute anything right away (aka lazy evaluation). 
So why design it this way?
Why Are RDDs Immutable?
Once you create an RDD, you can’t change it. Period.
rdd1 = sc.parallelize([1, 2, 3])
rdd2 = rdd1.map(lambda x: x * 2)
rdd1.collect()   # [1, 2, 3] — untouched
rdd2.collect()   # [2, 4, 6] — new RDD
But why? For several reasonable reasons.
Functional programming roots
Spark borrowed heavily from Functional Programming — pure functions, no side effects, and immutable data. In Spark, you don’t modify an RDD — you transform it into a new one. The original stays untouched. This makes things predictable, which matters a lot when your code runs on 200 machines simultaneously.
Concurrency without issues
Multiple nodes reading the same data at the same time? If that data is mutable, you need a complex system of locks and synchronization. If it’s immutable, then that’s not a problem. Nobody can change it, so nobody can corrupt it. There’s no race conditions, no “who wrote last” bugs. Each transformation just makes a new RDD and moves on.
In-memory computing
Spark is fast because it keeps data in memory. But in-memory data that can change right from under you? That’s a cache invalidation nightmare.
Immutable data doesn’t have this problem — once it’s cached, it’s valid forever (or until you explicitly unpersist it). No stale reads, no “did someone update this partition while I was reading it”.
Lineage and fault tolerance
This is where the “resilient” in RDD comes from. Machines fail — and in a distributed system, that’s a-okay.
Spark handles this with lineage: a graph of every transformation that produced each RDD. A node dies? Spark traces back through the lineage and replays the transformations to rebuild the lost data.
This only works because RDDs are immutable. If the input data could change between the original run and the replay, you’d get different results. The replay would be meaningless. Immutability guarantees the inputs are the same, so the outputs are the same.
Lineage in practice
Say you have this pipeline:
raw_logs → filtered_logs → enriched_logs → aggregated_metrics
Each arrow is a transformation. Each step is a new immutable RDD. Spark remembers the whole chain.
Node holding enriched_logs dies? Spark looks at the lineage:
enriched_logs = enrich(filtered_logs)
filtered_logs = filter(raw_logs)
Then, it replays from the last checkpoint or from raw_logs. Done — you might not even notice.
Now imagine RDDs were mutable. Someone modified filtered_logs in place between the original run and the recovery. Spark replays the same transformations but gets different results. The whole recovery model falls apart.
That’s why this matters. Not as a concept — as the reason your 200-node cluster survives hardware failures without you waking up.
The tradeoff
Immutability isn’t free. Every transformation = new RDD = new object in memory. Chain ten transformations and you’ve got ten RDDs sitting in your lineage.
The actual cost shows up when you start materializing data:
Memory pressure. If you cache intermediate RDDs, each one occupies memory across the cluster.
Recomputation cost. If you don’t cache them, Spark may need to replay parts of the lineage repeatedly.
GC overhead. More objects, more churn, more work for the JVM.
So the tradeoff isn’t just “more memory” — it’s memory vs recomputation.
So why bother?
Because mutable distributed state is worse. Way worse. Locking, synchronization, conflict resolution across a cluster — people have tried it. They stopped. Immutability trades memory for not losing your mind. At scale, that’s a good deal.
In practice you manage this with .persist() or .cache() on the RDDs you actually reuse [ https://substack.com/redirect/b90cf084-ea56-4426-bc75-57f746d45e94?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ], and let Spark clean up the rest.
What about DataFrames?
“But I don’t use RDDs — I use DataFrames.”
Same rules. df.filter(...), df.withColumn(...) — you get a new DataFrame back. The original doesn’t change. Same lineage, same fault tolerance, same lazy evaluation.
DataFrames just add Catalyst (query optimizer) and Tungsten (memory manager) on top [ https://substack.com/redirect/35dc0f08-e38f-4cfe-85f4-d427e1746e80?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]. They optimize how things run, but underneath it’s still immutable RDDs all the way down. You just don’t see it because the API feels like SQL instead of functional programming.
The interview answer I’m actually looking for
Back to the interview question. Here’s what I hear:
“Because that’s how Spark works”.
Cool. But I’m looking for why?
“For fault tolerance”.
Ok. Better. But that’s only one reason out of four.
“Fault tolerance through lineage replay, no synchronization headaches in concurrent execution, simpler caching, and it follows FP principles. The cost is memory, but only when you materialize — caching, or shuffles. The transformations themselves are cheap plan objects, lazy until an action. You manage it with selective caching and checkpoints.”
That answer tells me you’ve run Spark jobs that broke. You know the theory and you know what it costs. That’s who I want on my team.
Wrapping up
Immutability isn’t a design quirk — it’s the foundation that everything else in Spark stands on — fault tolerance, concurrency, caching — the whole execution model. Take it away, and the system doesn’t get “a bit worse.” It stops working entirely.
Next time someone asks you this question in an interview, don’t just list the benefits, Make sure to mention the cost as well. That’s what separates knowing Spark from having used it.
For more on the practical side, check out the Spark Optimization Checklist [ https://substack.com/redirect/52f73239-d9ea-4f35-b27a-faa63801ecc8?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ].
Additional Materials
Learning Spark: Lightning-Fast Data Analytics by Jules S. Damji, Brooke Wenig, Tathagata Das, Denny Lee [ https://substack.com/redirect/cccd7bcb-4420-4291-9b56-44467581b42a?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]
High Performance Spark by Holden Karau, Adi Polak, Rachel Warren [ https://substack.com/redirect/fe421191-1699-42f9-abbd-f68237a1a446?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]
Advanced Analytics with PySpark by Akash Tandon, Sandy Ryza, Uri Laserson, Sean Owen, Josh Wills [ https://substack.com/redirect/ff61972b-28db-483a-bf34-9fc8d9a00f0d?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]

Unsubscribe https://substack.com/redirect/2/eyJlIjoiaHR0cHM6Ly9sdW1pbm91c21lbi5zdWJzdGFjay5jb20vYWN0aW9uL2Rpc2FibGVfZW1haWw_dG9rZW49ZXlKMWMyVnlYMmxrSWpveE1EY3pPREV4TENKd2IzTjBYMmxrSWpveE9UWTVOamN5TkRjc0ltbGhkQ0k2TVRjM09URTVOakUxTUN3aVpYaHdJam94T0RFd056TXlNVFV3TENKcGMzTWlPaUp3ZFdJdE1Ua3pOall6TnlJc0luTjFZaUk2SW1ScGMyRmliR1ZmWlcxaGFXd2lmUS5Pcm1qRDVmbFBxU1JmV1lFNlQ3eWlBYWJwZUJ6SW5tR1FodDJ6eGNmWktrIiwicCI6MTk2OTY3MjQ3LCJzIjoxOTM2NjM3LCJmIjp0cnVlLCJ1IjoxMDczODExLCJpYXQiOjE3NzkxOTYxNTAsImV4cCI6MjA5NDc3MjE1MCwiaXNzIjoicHViLTAiLCJzdWIiOiJsaW5rLXJlZGlyZWN0In0.u_u7SNIMA6nKEmkMYgfETWFZOE-WnCCA4PTNl6bbopE?
