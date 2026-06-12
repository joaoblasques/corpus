---
channel: email
source: gmail
gmail_message_id: 19eb6300cdb21426
from: TLDR Data <dan@tldrnewsletter.com>
subject: "Fable Evals Performance ✅, Airbnb’s Evolved Data Architecture 🏘️, PostgreSQL Differential Privacy 🎭"
date_received: 2026-06-11
pointer: false
collected_at: 2026-06-11
corpus_ingested: true
corpus_ingested_at: 2026-06-12
corpus_pages:
  - corpus/ai-engineering/agent-evaluation.md
---

Claude Fable 5 is a major step up for complex data analysis, scoring
roughly 10-15% better than recent frontier models on Hex’s
evals ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌  ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ ‌ 


 Sign Up [1] |Advertise [2]|View Online [3] 

		TLDR 

		TOGETHER WITH [Transcend] [4]

TLDR DATA 2026-06-11

 WEBINAR: UNLOCKING FIRST-PARTY DATA FOR AI (SPONSOR) [4] 

 Join CEO Ben Brook on June 16 for a practical roadmap to first-party
data activation and AI governance, plus a maturity diagnostic you can
apply immediately.

> It starts with a real-time source of truth. Transcend encodes
complete data-use permissions directly into the systems that process
customer data, so every AI initiative and data product runs on a
real-time source of truth. SEE HOW [5].

> 220+ enterprise IT and business leaders on why AI initiatives fail,
and what to do about it.

GET THE REPORT → [6]

📱 

DEEP DIVES

 SCALING BEYOND ONE: HOW AIRBNB EVOLVED ITS DATA ARCHITECTURE FOR A
MULTI-PRODUCT WORLD (9 MINUTE READ) [7] 

 Airbnb evolved its offline data architecture for a multi-product
world with a flexible modeling framework that balances shared
consistency with domain-specific needs. Its three principles are no
hybrid models, consistent identifier naming, and clear namespaces so
teams can separate product-specific models from cross-cutting
monolithic ones. 

 INSIDE QUESTDB'S QUERY ENGINE: TRACING THREE QUERIES (8 MINUTE READ)
[8] 

 QuestDB's time-series query engine appears tuple-at-a-time
externally, but internally mixes vectorized execution, SIMD C++
kernels, Java batch processing, JIT filtering, and frame-based
parallelism. Small SQL changes can shift execution paths, affecting
group-by, filtering, and aggregation performance. 

 PARENTING ICEBERG AND LANCE WITH GRAVITINO: THE REALITY BEHIND
UNIFIED LAKEHOUSE ARCHITECTURES (8 MINUTE READ) [9] 

 Apache Gravitino can govern Iceberg tables and Lance multimodal
datasets through one metadata layer, RBAC model, and audit surface.
Iceberg commits through the catalog, while Lance uses a two-step
object-storage flow, with gotchas around config rewrites, jars, enum
casing, and client drift. 

🚀 

OPINIONS & ADVICE

 WE HAD TO BUILD NEW EVALS FOR FABLE (8 MINUTE READ) [10] 

 Claude Fable 5 is a major step up for complex data analysis, scoring
roughly 10-15% better than recent frontier models on Hex's evals and
excelling at messy, long-horizon tasks that require judgment, clear
assumptions, and cross-checking semantic models against raw data. 

 DAGSTER PRICE INCREASE 10X INSANE, DON'T EVER USE THEM (REDDIT
THREAD) [11] 

 Dagster's managed pricing jump has triggered backlash, pushing
smaller users toward self-hosting, Airflow, Prefect, or simpler
cron-style setups while still valuing Dagster OSS. 

 WHY METADATA HAS TO BE MUTATION-FRIENDLY (10 MINUTE READ) [12] 

 In high-update lakehouses, metadata becomes a high-mutation system.
Apache Hudi's Merge-On-Read Metadata Table handles this with
append-first writes and deferred compaction, reducing write cost and
supporting scalable indexing more efficiently than Copy-On-Write
designs. 

 WHEN EVENT TIME MEETS REALITY: LESSONS FROM BUILDING BILLING ON
APACHE FLINK (12 MINUTE READ) [13] 

 While building their usage-based billing pipeline, Gorgias
experienced overlapping windows and incorrect aggregations during
historical reprocessing due to internal repartitioning and uneven
operator behavior that broke event-time guarantees. The team mitigated
this by aligning keys across pipeline steps and applying conditional
extra delays only during replays. 

💻 

LAUNCHES & TOOLS

 POSTGRESQL ANONYMIZER 3.1: INTRODUCING LOCAL DIFFERENTIAL PRIVACY (2
MINUTE READ) [14] 

 PostgreSQL Anonymizer 3.1 adds expanded masking for PII and sensitive
data, with six masking strategies, including substitution,
randomization, pseudonymization, shuffling, noise addition, and
generalization. It now supports Local Differential Privacy via GRRM,
providing formal privacy guarantees for survey and categorical data
with privacy controlled by epsilon. 

 INTRODUCING LOON: A NEW STORAGE ENGINE FOR VECTOR DATA THAT NEVER
STOPS CHANGING (19 MINUTE READ) [15] 

 Vector datasets evolve through backfills, embedding versions, and
mixed workloads, not just vector columns. Loon, behind Milvus 3.0 beta
and Zilliz Vector Lakebase, uses hybrid file formats, row-ID
alignment, and versioned manifests so scalars, vectors, and object
references can update independently with less rewriting. 

 INTRODUCING STREAMLING: PERFORMANT AND EXTENSIBLE DATA STREAMING
RUNTIME (7 MINUTE READ) [16] 

 Streamling is an open-source Rust, Arrow, and DataFusion streaming
runtime for transactional workloads rather than heavy analytics. It
runs mostly single-node stateless pipelines with Kafka, Postgres,
ClickHouse, HTTP enrichment, TypeScript/WASM transforms, plugins,
checkpointing, and effectively-once delivery. 

🎁 

MISCELLANEOUS

 SCALING ZERO COPY FROM 1 TRILLION TO 120 TRILLION ROWS WITH FILE
FEDERATION (5 MINUTE READ) [17] 

 Zero Copy at Salesforce Data 360 evolved from Query Federation to
Iceberg File Federation to support AI workloads across distributed
enterprise data without centralizing it. The new architecture reduces
cross-system compute overhead, preserves governance through temporary
catalog-based access, and is being pushed by the need for real-time AI
across major data platforms. 

 DATAAGENTS: HOW WE TURNED 9 MONTHS OF ANALYSIS INTO 10 DAYS (6 MINUTE
READ) [18] 

 Capital One's DataAgent pattern cut cloud dormancy analysis across
about 350 AWS, Azure, and GCP resource types from 6-9 months to 10
days. It combines asset data, AI-generated Spark SQL, confidence
scoring, false-positive checks, and human validation to find
high-confidence savings opportunities. 

⚡ 

QUICK LINKS

 HNSW VS. LSH: HOW ELASTICSEARCH HITS 0.99 RECALL@10 AT 15,000 QPS —
AND WHAT IT COSTS (9 MINUTE READ) [19] 

 Exact vector search fails at scale because of high dimensionality,
making HNSW the dominant approach in Elasticsearch. 

 WHY WE SHRANK OUR TIMESCALEDB CHUNKS FROM 30 DAYS TO 7 (4 MINUTE
READ) [20] 

 Warner Music Group reduced TimescaleDB chunk intervals from 30 days
to 7 days on high-ingest hypertables after larger chunks caused
compression failures, slower recent queries, and costly backfills. 

Love TLDR? Tell your friends and get rewards!

 Share your referral link below with friends to get free TLDR swag! 

 https://refer.tldr.tech/5e134a97/11 [21] 

		 Track your referrals here. [22] 

Want to advertise in TLDR? 📰

 If your company is interested in reaching an audience of data
engineering professionals and decision makers, you may want to
ADVERTISE WITH US [23]. 

Want to work at TLDR? 💼

 APPLY HERE [24], CREATE YOUR OWN ROLE [25] or send a friend's resume
to jobs@tldr.tech and get $1k if we hire them! TLDR is one of INC.'S
BEST BOOTSTRAPPED BUSINESSES [26] of 2025. 

 If you have any comments or feedback, just respond to this email! 

Thanks for reading, 
Joel Van Veluwen [27], Tzu-Ruey Ching [28] & Remi Turpaud [29] 

 Manage your subscriptions [30] to our other newsletters on tech,
startups, and programming. Or if TLDR Data isn't for you, please
unsubscribe [31]. 

 

Links:
------
[1] https://tldr.tech/data?utm_source=tldrdata
[2] https://advertise.tldr.tech?utm_source=tldrdata&utm_medium=newsletter&utm_campaign=advertisetopnav
[3] https://a.tldrnewsletter.com/web-version?ep=1&lc=ad8a8f94-145d-11ef-9302-6303621b287c&p=b67e1254-654d-11f1-b11e-1f75079694bb&pt=campaign&t=1781173062&s=74e948d2febc3c37a54b2de9a4738f4e0d0b79588114733e3caf863c8b8ca8e1
[4] https://transcend-io.zoom.us/webinar/register/2817805140216/WN_E4EDUw8mQjaUqYusDmdaYQ?utm_source=TLDR&utm_medium=newsletter&utm_campaign=2026-06-11_Primary_Transcend&utm_content=header_webinar_i_use#/registration
[5] https://transcend.io/?utm_source=TLDR&utm_medium=newsletter&utm_campaign=2026-06-11_Primary_Transcend&utm_content=Body_how
[6] https://transcend.io/resources/state-of-customer-data-report-2026?utm_source=TLDR&utm_medium=newsletter&utm_campaign=2026-06-11_Primary_Transcend&utm_content=cta_report
[7] https://links.tldrnewsletter.com/aghsFN
[8] https://bcalza.b-cdn.net/blog/2026/06/08/inside-questdb-query-engine.html?utm_source=tldrdata
[9] https://links.tldrnewsletter.com/P2hZup
[10] https://hex.tech/blog/fable-evals/?utm_source=tldrdata
[11] https://links.tldrnewsletter.com/HQ8qjg
[12] https://hudi.apache.org/blog/2026/06/05/why-metadata-has-to-be-mutation-friendly/?utm_source=tldrdata
[13] https://links.tldrnewsletter.com/aXFWIY
[14] https://www.postgresql.org/about/news/postgresql-anonymizer-31-introducing-local-differential-privacy-3311/?utm_source=tldrdata
[15] https://links.tldrnewsletter.com/jWpP5U
[16] https://www.streamingdata.tech/p/introducing-streamling?utm_source=tldrdata
[17] https://engineering.salesforce.com/scaling-zero-copy-from-1-trillion-to-120-trillion-rows-with-file-federation/?utm_source=tldrdata
[18] https://links.tldrnewsletter.com/fCbyQU
[19] https://www.elastic.co/blog/understanding-approximate-nearest-neighbor-search?utm_source=tldrdata
[20] https://links.tldrnewsletter.com/qHJY2Z
[21] https://refer.tldr.tech/5e134a97/11
[22] https://hub.sparklp.co/sub_e2f80d4d5249/11
[23] https://advertise.tldr.tech/?utm_source=tldrdata&utm_medium=newsletter&utm_campaign=advertisecta
[24] https://jobs.ashbyhq.com/tldr.tech
[25] https://jobs.ashbyhq.com/tldr.tech/c227b917-a6a4-40ce-8950-d3e165357871
[26] https://www.linkedin.com/feed/update/urn:li:activity:7401699691039830016/
[27] https://www.linkedin.com/in/joelvanveluwen/
[28] https://www.linkedin.com/in/jennytzurueyching/
[29] https://www.linkedin.com/in/remi-turpaud/
[30] https://tldr.tech/data/manage?email=tilakapash%40gmail.com
[31] https://a.tldrnewsletter.com/unsubscribe?ep=1&l=037ede50-92cc-11ee-b0f2-b761aa2217ad&lc=ad8a8f94-145d-11ef-9302-6303621b287c&p=b67e1254-654d-11f1-b11e-1f75079694bb&pt=campaign&pv=4&spa=1781172073&t=1781173062&s=76d924bd935c76a2320fe03a16b8715526add89310f9fe4c315ed0ace3f504f8
