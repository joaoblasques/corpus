---
channel: email
source: gmail
gmail_message_id: 19e316a8fcefa0eb
from: Pipeline to Insights <pipeline2insights@substack.com>
subject: Change Data Capture (CDC) Fundamentals for Data Engineers
date_received: 2026-05-16
pointer: false
collected_at: 2026-06-11
corpus_ingested: true
corpus_ingested_at: 2026-06-11
corpus_pages:
  - corpus/data-engineering/change-data-capture.md
---

View this post on the web at https://pipeline2insights.substack.com/p/change-data-capture-cdc-fundamentals-for-data-engineers

Once, at a company that provided HVAC services and maintenance for commercial buildings, a product manager came to me with a problem:
“I need to know every time a technician is reassigned to a project , and I need to know the moment it happens.”
The reason was important. Some projects involved secure, sensitive facilities that required technicians with specialised training and experience. If a technician was reassigned to one of these projects without the right background, the PM needed to know immediately so they could organise the correct training before the technician stepped onto the job.
At first, it sounded simple. The first thing I tried was querying the assignments table to check the change history. But when I looked at the database, I hit a problem.
The SQL Server table only stored the current state of assignments. No history. No timestamps. Just: Technician A is assigned to project Y.
When an assignment changed, the row was updated. There was no record of the previous value or when the change occurred.
So I started thinking through my options.
Option 1: Full load on a schedule
Take a snapshot of the entire table every hour and compare it with the previous snapshot.
This could tell me that something changed, but only between two snapshots.
If I only ran the pipeline once a day and a reassignment happened at 9 am, the PM wouldn’t know until the next morning, far too late.
And even worse, if a technician was reassigned multiple times between snapshots, I would only see the final state and completely miss the earlier changes.
Option 2: Slowly Changing Dimensions (SCD Type 2)
Another option was using SCD Type 2.
Instead of overwriting rows, SCD Type 2 preserves history by creating a new row whenever data changes and marking the old row as inactive.
This was better because it allowed me to track historical versions of assignments over time.
But there was still a problem.
SCD Type 2 only captures changes when the snapshot process runs.
So if a technician were assigned and then reassigned again between snapshots, I would still miss the intermediate change entirely.
I wouldn’t even know it happened.
Note: There are two common SCD types worth knowing:
SCD Type 1 overwrites old values and keeps only the latest state
SCD Type 2 preserves history by storing multiple versions of a row
My use case needed Type 2 because I needed historical tracking. But even Type 2 couldn’t help if changes happened between snapshots.
Both approaches had the same problem:
I was trying to detect changes after the fact by comparing snapshots, rather than capturing the exact moment the change occurred.
That’s when I started learning about Change Data Capture (CDC). CDC allows you to capture changes as they happen and send them to downstream systems in near real time, without repeatedly querying the entire database.
Note: The database I was working with already supported native CDC, and database triggers could also have solved this problem. Later in this post, we’ll look at how these approaches work and how they differ.
In this post, we’ll cover:
The decision framework
Full load
Incremental loading
Change Data Capture (CDC)
The three main CDC methods (with PostgreSQL examples)
CDC vs database replication
When to use CDC?
Important things beginners should know before using CDC.
Pipeline To Insights is a reader-supported publication. To receive new posts and support my work, consider becoming a free or paid subscriber💐.
The Decision Framework
The problem I ran into is common in data engineering. 
At a high level, there are three common approaches engineers use to move and sync data between systems:
Each approach solves different problems and comes with different trade-offs.
As systems grow and business requirements become more demanding, engineers usually move from simpler approaches toward more advanced ones.
Let’s walk through them one by one.
Step 0: Full Load
The simplest approach is to copy the entire table from the source system to the destination every time the pipeline runs.
When full load is the right choice:
The table is small (fewer than a few million rows) and quick to copy.
The data changes rarely, or you have no way to detect what changed.
You’re doing a one-time historical migration.
Freshness requirements are loose (once a day is fine).
Note: Full load is underrated. Many pipelines don’t need anything fancier. If your table has 50,000 rows and the business only needs yesterday’s data, a nightly full load is perfectly fine, don’t over-engineer it.
Where full load breaks down:
The table has tens of millions of rows, and copying it all every hour is slow and expensive.
The business needs fresher data than your batch window allows.
Deletes need to be tracked accurately.
That’s when engineers might start thinking about incremental loading.
Step 1: Incremental Loading
Instead of copying the entire table every run, incremental loading processes only the rows that have changed since the last execution.
The most common approach uses a timestamp column such as updated_at or last_modified.
Where Incremental Loading Breaks Down
Problem 1: You Only See the Latest State
Imagine your pipeline runs once every 24 hours on a bank account table.
During the day, a customer makes five withdrawals. But when the pipeline runs at midnight, it only sees the final balance. The other four changes are invisible.
You only see the latest state. not the full history of what happened.
The same problem exists with hard deletes.
If a row is physically deleted from the source database, your incremental pipeline may never know the row existed. The deleted row can remain in your warehouse even though it no longer exists in the source system.
One workaround is soft deletes; instead of deleting the row, the system marks it with a flag, such as is_deleted.
But this only works if you control the source system.
Problem 2: Latency
Even well-designed incremental pipelines still take time to run.
If downstream systems need updates within seconds, a pipeline that runs every 5 minutes may already be too slow.
Problem 3: Backfills Become Large
Imagine your incremental pipeline has been running smoothly for two months.
Then, suddenly, you need to reload historical data.
Instead of processing one hour's worth of changes, your pipeline now tries to process two months' worth of data in a single run.
At that point, it’s no longer really incremental; it’s basically a full load.
This can create major pressure on your infrastructure.
One common solution is to process data in smaller time windows rather than loading everything at once.
Note: If you start running into missing deletes, high latency, or difficult backfills, that’s usually the signal that it’s time to consider CDC.
What Is Change Data Capture?

Unsubscribe https://substack.com/redirect/2/eyJlIjoiaHR0cHM6Ly9waXBlbGluZTJpbnNpZ2h0cy5zdWJzdGFjay5jb20vYWN0aW9uL2Rpc2FibGVfZW1haWw_dG9rZW49ZXlKMWMyVnlYMmxrSWpveE1EY3pPREV4TENKd2IzTjBYMmxrSWpveE9UYzRNalV6T1RVc0ltbGhkQ0k2TVRjM09EazBOVFV5TXl3aVpYaHdJam94T0RFd05EZ3hOVEl6TENKcGMzTWlPaUp3ZFdJdE16QTBORGsyTmlJc0luTjFZaUk2SW1ScGMyRmliR1ZmWlcxaGFXd2lmUS5DWnMtTE1vb0ppSEZBUFg1SFJidTE4djBuRWRjazI3MlFjQ3ItdER6NEpFIiwicCI6MTk3ODI1Mzk1LCJzIjozMDQ0OTY2LCJmIjp0cnVlLCJ1IjoxMDczODExLCJpYXQiOjE3Nzg5NDU1MjMsImV4cCI6MjA5NDUyMTUyMywiaXNzIjoicHViLTAiLCJzdWIiOiJsaW5rLXJlZGlyZWN0In0.jzaxzn-YhoEJpYwbeDi8FPAyDvPJkxLiHn81iw923CQ?
