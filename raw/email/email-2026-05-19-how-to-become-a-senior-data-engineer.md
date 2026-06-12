---
channel: email
source: gmail
gmail_message_id: 19e3eaa178c6bb53
from: Vu Trinh <vutr@substack.com>
subject: How to become a senior data engineer?
date_received: 2026-05-19
pointer: false
collected_at: 2026-06-11
links:
  - {url: "https://substack.com/redirect/94bda382-c9b2-461e-b38f-01d57cb8ebb4?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: false, score: 8, reason: fetch-failed}
  - {url: "https://substack.com/redirect/db00bb68-da18-44c1-bd66-9ee47815ff5f?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: false, score: 8, reason: fetch-failed}
  - {url: "https://substack.com/redirect/662e156b-2c71-4cef-b824-e0cf52ff35a2?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 7, file: raw/web/fundamentals-of-data-engineering.md}
  - {url: "https://substack.com/redirect/2dfc2e7f-4738-42b4-932b-1a9de712abc5?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: false, score: 6, reason: duplicate}
  - {url: "https://substack.com/redirect/d3d61180-5e9a-4f5b-9a3d-6373430ac5fe?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: false, score: 1, reason: low-utility}
corpus_ingested: true
corpus_ingested_at: 2026-06-11
corpus_pages:
  - corpus/data-engineering/data-engineer-role.md
---

View this post on the web at https://vutr.substack.com/p/how-to-become-a-senior-data-engineer

I invite you to join my paid membership list for only 7$/month (pay annually) to get access to:
This article and 200+deep-dive data engineering articles
learn-spark: a CLI tool to master Apache Spark internals
learn-dbt: a CLI tool to master dbt from the ground up
All future learning tools → Tools Demo [ https://substack.com/redirect/2dfc2e7f-4738-42b4-932b-1a9de712abc5?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]
If you’re a student with an education email, use this 50% ANNUAL DISCOUNT [ https://substack.com/redirect/d3d61180-5e9a-4f5b-9a3d-6373430ac5fe?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]
If you’re a Vietnamese user, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get 50% OFF the annual plan.
Intro
The inconsistency in some companies’ evaluation systems often leads people to think that the title of software engineer is losing its value. This is even more common in data engineering, given that it is still a relatively new field compared to software engineering. 
Lack of best practices and the heavy dependence on a company’s business may make data engineers look very different between Company A and Company B. That’s why one might be a senior DE at Company A, yet only receive a junior offer from Company B. 
Saying that does not mean the title is meaningless. No one wants to be stuck at junior forever. It’s not only about salary; it’s also about being trusted and contributing more value.
—
In this week's article, I share my notes that will help you to become more senior. You won’t see anything like “learning tool X or Y”; instead, I want to deliver the mindsets that I distilled from my own experience and learned from “way-more-senior” colleagues than me. 
Note: It’s my note, so you might not find it comprehensive. 
Business value is 1st priority
The company hires data engineers to build a robust data foundation so business users can derive insights from it.
When we begin our journey, we rarely realize this. (If you did, congratulations.)
Any company hires an employee, assuming he is good at “X,” so he can help the company with that. For data engineers, we are hired because we’re good at “data engineering,” and the company believes we can leverage that to build the data foundation. 
That “and“ is very important. 
You’re not hired solely for your ability to debug Spark.
You’re hired because you can operate Spark at the scale the company needs to help produce business reports on time. 
Thus, every single task you do, every decision you make, must output some business value (directly or indirectly). This is even more true for data engineers, as we work in the (data) department, which is very close to the business decision-making process. (If the company is actually doing that by leveraging data)
—
Business value is the number one priority. But how would you know what value you could help create? This falls back to the question: What is the true responsibility of a data engineer? To answer this, I always suggest reading the first chapter of the book Fundamentals of Data Engineering: Plan and Build Robust Data Systems [ https://substack.com/redirect/662e156b-2c71-4cef-b824-e0cf52ff35a2?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ].
Data engineering is the development, implementation, and maintenance of systems and processes that take in raw data and produce high-quality, consistent information that supports downstream use cases, such as analysis and machine learning. Data engineering is the intersection of security, data management, DataOps, data architecture, orchestration, and software engineering. — Joe Reis [ https://substack.com/redirect/94bda382-c9b2-461e-b38f-01d57cb8ebb4?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ], Matt Housley [ https://substack.com/redirect/db00bb68-da18-44c1-bd66-9ee47815ff5f?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]
A data engineer manages the data engineering lifecycle, beginning with getting data from source systems and ending with serving data for use cases, such as analysis or machine learning — Joe Reis [ https://substack.com/redirect/94bda382-c9b2-461e-b38f-01d57cb8ebb4?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ], Matt Housley [ https://substack.com/redirect/db00bb68-da18-44c1-bd66-9ee47815ff5f?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ].
—
The more business-value-oriented you are, the more chances you have to grow and contribute. A signal that tells you you’re going the right path: you focus more on the “boring“ things: data modeling, data security, or data governance.  
I invite you to join my paid membership list for only 7$/month (pay annually) to get access to:
This article and 200+deep-dive data engineering articles
learn-spark: a CLI tool to master Apache Spark internals
learn-dbt: a CLI tool to master dbt from the ground up
All future learning tools → Tools Demo [ https://substack.com/redirect/2dfc2e7f-4738-42b4-932b-1a9de712abc5?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]
If you’re a student with an education email, use this 50% ANNUAL DISCOUNT [ https://substack.com/redirect/d3d61180-5e9a-4f5b-9a3d-6373430ac5fe?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]
If you’re a Vietnamese user, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get 50% OFF the annual plan...

Unsubscribe https://substack.com/redirect/2/eyJlIjoiaHR0cHM6Ly92dXRyLnN1YnN0YWNrLmNvbS9hY3Rpb24vZGlzYWJsZV9lbWFpbD90b2tlbj1leUoxYzJWeVgybGtJam94TURjek9ERXhMQ0p3YjNOMFgybGtJam94T1RjeE56UTBOamNzSW1saGRDSTZNVGMzT1RFMk56YzVNeXdpWlhod0lqb3hPREV3TnpBek56a3pMQ0pwYzNNaU9pSndkV0l0TVRrek1EY3dOU0lzSW5OMVlpSTZJbVJwYzJGaWJHVmZaVzFoYVd3aWZRLlZlMzBHMXlIY3BfRGVkQlV1SFlNaVFIeEhvSVdjLVhDckNISkNMN2ZzRXMiLCJwIjoxOTcxNzQ0NjcsInMiOjE5MzA3MDUsImYiOnRydWUsInUiOjEwNzM4MTEsImlhdCI6MTc3OTE2Nzc5MywiZXhwIjoyMDk0NzQzNzkzLCJpc3MiOiJwdWItMCIsInN1YiI6ImxpbmstcmVkaXJlY3QifQ.MZNV5kp6U3L8DpvL-D-X1CZ3_iZ_vET6Kj4pT-dgOg4?
