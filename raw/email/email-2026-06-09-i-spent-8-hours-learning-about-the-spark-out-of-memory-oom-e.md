---
channel: email
source: gmail
gmail_message_id: 19eaaceed6ae93dd
from: Vu Trinh <vutr@substack.com>
subject: I spent 8 hours learning about the Spark Out-Of-Memory (OOM) errors
date_received: 2026-06-09
pointer: false
collected_at: 2026-06-11
links:
  - {url: "https://substack.com/redirect/70c3aa39-8a4a-4199-9e80-0a08bc3c2989?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 8, file: raw/web/problems.md}
  - {url: "https://substack.com/redirect/c4486cb0-5f77-4679-bc63-6e26f039d05f?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 8, file: raw/web/understand-the-internals-run-the-code.md}
  - {url: "https://substack.com/redirect/dd50b6ea-35ca-440b-b900-f5e13512555d?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 7, file: raw/web/a-small-hands-on-project-to-2-your-apache-spark-learning-pro.md}
  - {url: "https://substack.com/redirect/229dd249-a1e9-4360-ae31-a086164a2069?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: false, score: 1, reason: low-utility}
corpus_ingested: true
corpus_ingested_at: 2026-06-11
corpus_pages:
  - corpus/data-engineering/apache-spark.md
---

View this post on the web at https://vutr.substack.com/p/i-spent-8-hours-learning-about-the

With only $7/month (billed annually), you can access all the materials you need to grow from junior → senior DE.
200+ deep-dive data engineering articles
practice-spark [ https://substack.com/redirect/70c3aa39-8a4a-4199-9e80-0a08bc3c2989?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]: 65 LeetCode-style problems to practice Spark SQL/DataFrame
learn-spark/dbt/airflow [ https://substack.com/redirect/c4486cb0-5f77-4679-bc63-6e26f039d05f?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]: CLI tools to master Spark/dbt/Airflow
If you’re a student with an education email, use this 50% ANNUAL DISCOUNT [ https://substack.com/redirect/229dd249-a1e9-4360-ae31-a086164a2069?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]
If you’re a Vietnamese user, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get 50% OFF the annual plan.
Intro
If you’ve ever run Spark in production, you might encounter the OOM error once.
You might simply increase the executor memory, and the problem will be fixed. However, naively allocating more resources to your Spark job won’t be sustainable in the long term. 
Instead, understanding the nature of the OOM is the better approach.
In this article, I deliver my understanding of the OOM errors so you can operate Spark more robustly in production. 
Note 1: This article assumes you have a basic understanding of Spark. I highly recommend you read this article [ https://substack.com/redirect/dd50b6ea-35ca-440b-b900-f5e13512555d?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] for that purpose.
Note 2: This article only discusses OOM on Spark executors.
How Spark works?
In brief
If you want to run Spark, you must have a cluster of machines that provide the resources for the Spark cluster.
A Spark cluster is a set of JVM processes, including a Driver and Executors. Those processes run on the cluster of machines (with communication with the Cluster Manager).
Every Spark cluster is associated with a Spark application.
Below the application is the Spark job. A job represents a series of transformations applied to data: the entire workflow from start to finish. The series of transformations (e.g, filter, map…) can be triggered only by an action (e.g., show, count,…).  We can say that a job is associated with an action. An application can have multiple jobs.
A job is split into different stages when a transformation requires shuffling data across partitions. (e.g., groupBy, join). A stage is a job segment executed without data shuffling. 
A stage has a set of tasks. A task is the smallest unit of execution within Spark. Each stage is divided into multiple tasks, each handling a partition, a portion of data from an external source or from the upstream stage. 
At a given stage, tasks can run in parallel; the parallelism depends on the executor's CPUs. You can understand that tasks are handled in parallel in an executor using the multithreading paradigm. By default, a task is handled by an executor core (controlled by the “spark.task.cpus” setting); if the executor has 4 cores, 4 tasks can run in parallel within the executor.
Why do OOM errors happen?
With only $7/month (billed annually), you can access all the materials you need to grow from junior → senior DE.
200+ deep-dive data engineering articles
practice-spark [ https://substack.com/redirect/70c3aa39-8a4a-4199-9e80-0a08bc3c2989?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]: 65 LeetCode-style problems to practice Spark SQL/DataFrame
learn-spark/dbt/airflow [ https://substack.com/redirect/c4486cb0-5f77-4679-bc63-6e26f039d05f?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]: CLI tools to master Spark/dbt/Airflow
If you’re a student with an education email, use this 50% ANNUAL DISCOUNT [ https://substack.com/redirect/229dd249-a1e9-4360-ae31-a086164a2069?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]
If you’re a Vietnamese user, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get 50% OFF the annual plan...

Unsubscribe https://substack.com/redirect/2/eyJlIjoiaHR0cHM6Ly92dXRyLnN1YnN0YWNrLmNvbS9hY3Rpb24vZGlzYWJsZV9lbWFpbD90b2tlbj1leUoxYzJWeVgybGtJam94TURjek9ERXhMQ0p3YjNOMFgybGtJam95TURBd056SXhOamdzSW1saGRDSTZNVGM0TURrNE1qRTBOeXdpWlhod0lqb3hPREV5TlRFNE1UUTNMQ0pwYzNNaU9pSndkV0l0TVRrek1EY3dOU0lzSW5OMVlpSTZJbVJwYzJGaWJHVmZaVzFoYVd3aWZRLnNzRkxXZzFaVzFQbUZvVmlXZEMwWHI0YUp5czdxdURyZHc5OUdKYzJ3SkkiLCJwIjoyMDAwNzIxNjgsInMiOjE5MzA3MDUsImYiOnRydWUsInUiOjEwNzM4MTEsImlhdCI6MTc4MDk4MjE0NywiZXhwIjoyMDk2NTU4MTQ3LCJpc3MiOiJwdWItMCIsInN1YiI6ImxpbmstcmVkaXJlY3QifQ._uNVTt9LzsId4hpLRAFOpK5tuwfHluvRuMTif5Or714?
