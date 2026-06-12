---
channel: email
source: gmail
gmail_message_id: 19e86c2c2f4aae7e
from: Vu Trinh <vutr@substack.com>
subject: I spent 8 hours learning the CAP theorem. Here’s what I found.
date_received: 2026-06-02
pointer: false
collected_at: 2026-06-11
links:
  - {url: "https://substack.com/redirect/270c2930-88a1-43bb-8df8-55ba2d4056f6?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: false, score: 8, reason: duplicate}
  - {url: "https://substack.com/redirect/ddfa070c-0992-42c6-80a0-86823b5a0202?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: false, score: 8, reason: fetch-failed}
  - {url: "https://substack.com/redirect/6bf49ca4-7100-4d4a-97ef-2e11fc02b2f2?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: false, score: 8, reason: fetch-failed}
  - {url: "https://substack.com/redirect/96ea4df0-0e6c-485f-880d-538251279101?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 5, file: raw/web/understand-the-internals-run-the-code-716b4174.md}
  - {url: "https://substack.com/redirect/f92b9e06-e7f1-4e09-9c95-49eeb6b79377?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: false, score: 1, reason: low-utility}
corpus_ingested: true
corpus_ingested_at: 2026-06-12
corpus_pages:
  - corpus/software-engineering/cap-theorem.md
---

View this post on the web at https://vutr.substack.com/p/i-spent-8-hours-learning-the-cap

I invite you to join my paid membership list for only 7$/month (pay annually) to get access to:
This article and 200+deep-dive data engineering articles
practice-spark [ https://substack.com/redirect/270c2930-88a1-43bb-8df8-55ba2d4056f6?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]: 65 LeetCode-style problems to practice Spark SQL/DataFrame
learn-spark: a CLI tool to master Apache Spark internals
learn-dbt: a CLI tool to master dbt from the ground up
learn_airflow: a CLI tool that equips you with all the Airflow fundamentals
All future learning tools → Tools Demo [ https://substack.com/redirect/96ea4df0-0e6c-485f-880d-538251279101?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]
If you’re a student with an education email, use this 50% ANNUAL DISCOUNT [ https://substack.com/redirect/f92b9e06-e7f1-4e09-9c95-49eeb6b79377?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]
If you’re a Vietnamese user, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get 50% OFF the annual plan.
Intro
I intend to write about CAP for a long time, in the early days of this newsletter. I hesitated because I thought it was too technical and barely brought value to data engineers.
Thus, I put it aside until last weekend.
I revisited my “idea” repository, scrolled a bit, and don’t know why I stopped at CAP. This time, I did more research and gained insights into data engineering, especially the Lambda and Kappa Architectures. Thus, I believe I can deliver my understanding of CAP in a more useful way to you guys.
That’s why this article was written.
What is CAP?
Let’s start with a single machine: one database node, a client writes a value, and another client reads it back. The machine either works or it doesn’t.
Simple, right?
Now, let’s add a node to make things fun. 
We want both nodes to serve reads for availability and throughput. To do that, both must stay in sync. And you want the system to keep working even when the network between them drops.
That's where the CAP exists.
The C, A, and P
The C, the Consistency, means all nodes see the same data at the same time. If a change is made, clients querying any node will get the most recent write. The moment a write is acknowledged, every node in the system reflects it.
Note: this is not the same as the C in ACID. ACID consistency means your transactions don’t violate constraints: referential integrity, unique keys, that kind of thing. CAP consistency means linearizability across nodes. Two different things that somehow share a name and confuse us.
Availability means every request gets a response.  If a node is up, it answers back.
Partition Tolerance means the system keeps operating even when the network between nodes breaks, and messages get lost. Some nodes can’t “talk” to others.
The computer scientist Eric Brewer [ https://substack.com/redirect/ddfa070c-0992-42c6-80a0-86823b5a0202?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ], who proposed CAP, states that any distributed data store [ https://substack.com/redirect/6bf49ca4-7100-4d4a-97ef-2e11fc02b2f2?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] can provide at most two of the C, A, and P.
Pick twos
In the three, partition tolerance isn’t a knob you can tune.
You can’t predict network failures, cables get unplugged, and cloud availability zones lose connectivity, or a heavy garbage collection pause on one node can look exactly like a network partition to its neighbors.
This fact, plus Eric Brewer’s statement about “can provide at most two”, we can say that in any distributed data store, we can only pick between CP and AP.
In a two-node setup, if partition tolerance happens (Node A and B can’t talk to each other), and you:
Choose consistency: Node A refuses the write/read until it can confirm with Node B. This is to ensure that all nodes see the same data at the same time and that the query gets the most recent write. The system becomes partially unavailable during the partition, which means you can’t have the “availability“.
Choose availability: Node A still answers the query and accepts the write. Node B will also do the same. However, they’re not kept in sync; B is not aware of A’s write and vice versa, which means you can’t have the “consistency“. 
Imagine you insist on having both. The partition tolerance happens. Node A and Node B cannot talk.
A client writes x = 1 to Node A.
Another client reads x from Node B.
For availability to hold, Node B must respond; it can’t say “try again later.”
For consistency to hold, Node B must return x = 1, the value that was just written to Node A. But Node B hasn’t received that write because it can communicate with Node A. 
So Node B either responds with a stale value: violating consistency, or refuses to respond: violating availability.
There is no world where Node B answers correctly and immediately. This means, in CAP, you can choose either Consistency-Partition or Availability-Partition.
I invite you to join my paid membership list for only 7$/month (pay annually) to get access to:
This article and 200+deep-dive data engineering articles
practice-spark [ https://substack.com/redirect/270c2930-88a1-43bb-8df8-55ba2d4056f6?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]: 65 LeetCode-style problems to practice Spark SQL/DataFrame
learn-spark: a CLI tool to master Apache Spark internals
learn-dbt: a CLI tool to master dbt from the ground up
learn_airflow: a CLI tool that equips you with all the Airflow fundamentals
All future learning tools → Tools Demo [ https://substack.com/redirect/96ea4df0-0e6c-485f-880d-538251279101?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]
If you’re a student with an education email, use this 50% ANNUAL DISCOUNT [ https://substack.com/redirect/f92b9e06-e7f1-4e09-9c95-49eeb6b79377?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]
If you’re a Vietnamese user, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get 50% OFF the annual plan...

Unsubscribe https://substack.com/redirect/2/eyJlIjoiaHR0cHM6Ly92dXRyLnN1YnN0YWNrLmNvbS9hY3Rpb24vZGlzYWJsZV9lbWFpbD90b2tlbj1leUoxYzJWeVgybGtJam94TURjek9ERXhMQ0p3YjNOMFgybGtJam94T1Rrd016QXlOakVzSW1saGRDSTZNVGM0TURNM056TTJPU3dpWlhod0lqb3hPREV4T1RFek16WTVMQ0pwYzNNaU9pSndkV0l0TVRrek1EY3dOU0lzSW5OMVlpSTZJbVJwYzJGaWJHVmZaVzFoYVd3aWZRLlExZ2hLN1o3STlLNVg1LXFicDF3dTY4UDl6b2l2bkphTkgwVzVBZ3lXZzAiLCJwIjoxOTkwMzAyNjEsInMiOjE5MzA3MDUsImYiOnRydWUsInUiOjEwNzM4MTEsImlhdCI6MTc4MDM3NzM2OSwiZXhwIjoyMDk1OTUzMzY5LCJpc3MiOiJwdWItMCIsInN1YiI6ImxpbmstcmVkaXJlY3QifQ.G6__kSa3rxquO6S4J1Gvgp2kEdUBQ9D6JWE7p7kwPDc?
