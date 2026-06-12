---
channel: email
source: gmail
gmail_message_id: 19929a9af1b6baf2
from: Joe Reis from Practical Data Modeling <practicaldatamodeling@substack.com>
subject: Medallion Architecture is NOT a Data Model
date_received: 2025-09-08
pointer: false
collected_at: 2026-06-11
links:
  - {url: "https://substack.com/redirect/2fee6bfb-8d92-4b86-ab0d-3932cf9570d6?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 7, file: raw/web/building-the-data-mart.md}
  - {url: "https://substack.com/redirect/3a63cfc5-dca8-433f-8bee-8fb15b1b3159?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 7, file: raw/web/the-pedantic-layer.md}
  - {url: "https://substack.com/redirect/15af00e4-cc69-4d98-ab36-ad9ffe850fe0?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: true, score: 6, file: raw/web/practical-data-modeling-joe-reis-substack.md}
  - {url: "https://substack.com/redirect/34cc05bc-4394-4d6a-9f0b-09c7d4554b82?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: false, score: 2, reason: low-utility}
  - {url: "https://substack.com/redirect/b13ad522-6e0c-4a8a-a116-ff21841cfa3d?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms", fetched: false, score: 1, reason: low-utility}
corpus_ingested: true
corpus_ingested_at: 2026-06-11
corpus_pages:
  - corpus/data-engineering/medallion-architecture.md
  - corpus/data-engineering/pipeline-layers.md
---

View this post on the web at https://practicaldatamodeling.substack.com/p/medallion-architecture-is-not-a-data

Ellie makes data modeling as easy as sketching on a whiteboard—so even business stakeholders can contribute effortlessly. By skipping redraws, rework, and forgotten context, and by keeping all dependencies in sync, teams report saving up to 78% of modeling time.
Bridge reality with Data! Read more here [ https://substack.com/redirect/34cc05bc-4394-4d6a-9f0b-09c7d4554b82?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ].
Thanks to Ellie.ai [ https://substack.com/redirect/b13ad522-6e0c-4a8a-a116-ff21841cfa3d?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] for sponsoring this post.
The Medallion Architecture is back in the zeitgeist. Since I’m writing a book on data modeling, I pay attention to the conversations where people conflate Medallion with data modeling. Most of these people are very confused. But I also can’t blame them because the literature is sparse for clearly delineating the boundaries of Medallion and data models.
The TL;DR is these are not the same thing. The Medallion architecture is no more a data model approach than a parking lot is a type of car.
A Medallion Architecture Refresher
Here’s a quick refresher on Medallion Architecture. “Medallion” is a term popularized by Databricks around the early 2020s to describe stages of data traverses in an analytical lifecycle. This is usually associated with ELT. If you’ve been around a while, you’ve seen variations of stages.
Landing → Curated → Serving
Staging → Data Mart
Different names, but the intent is to progressively refine data so it’s more useful for specific use cases (usually analytics).
Medallion is the same thing, but here we use the stages of bronze → silver → gold. No, these aren’t Olympic medals.
Bronze: Raw ingestion. Think append‑only files or tables, minimal transformation, schema drift tolerated, heavy lineage focus.
Silver: Cleansed and conformed. De-duplicated, typed, and standardized IDs, business keys resolved, and quality rules enforced.
Gold: Business‑ready. Here, data is modeled specifically for consumption, such as dashboards, reports, self-serve analytics, etc.
The way I like to think about this is each stage removes complexity for an increasingly broader (and less technical) audiences.
Bronze (primarily technical) → Silver (less technical) → Gold (non‑technical/business)
At no point do we prescribe how the data is modeled. Each stage is model agnostic.
As an aside, some people take issue with whether a medallion is truly an “architecture.” That’s a separate debate that I won’t get into here. The point here is far simpler: don’t conflate a staging pattern with modeling.
WTF is a Data Model?
As I’ve described in my upcoming data modeling book [ https://substack.com/redirect/15af00e4-cc69-4d98-ab36-ad9ffe850fe0?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ], “A data model organizes and standardizes data in a precise, structured representation, enabling and guiding human and machine behavior, informing decision-making, and facilitating actions.”
Data modeling also has stages, from low complexity and ease of understanding to high complexity and technicality. At a high level, data modeling consists of conceptual → logical → physical stages.
Conceptual: What domains, entities, and relationships exist? (Customers, Orders, Products; how do they relate?)
Logical: What’s the grain of each dataset? What are the keys, attributes, and cardinalities?
Physical: How do we implement the model efficiently for a specific database or storage system?
Data models answers questions like:
What is a Customer in our business, and how do we identify one?
What’s the grain of an Orders dataset? Order, order line, or shipment?
Which attributes are slowly changing, and how do we track history?
Where do we put constraints, and how do we enforce integrity?
People have asked these types of questions since the dawn of business. None of these decisions is implied by “Bronze vs Silver vs Gold.” They’re orthogonal to data modeling.
Consider the journey data's path within the Medallion Architecture. Data in Medallion becomes simpler for the end-user as it moves from Bronze to Gold. A non-technical business analyst doesn't want raw JSON, they want a clean table to query. Conversely, a data model becomes more complex and specific as it moves from a conceptual whiteboard sketch to a physically implemented DDL script. They are inverse processes serving a common goal, namely delivering value.
Orthogonal by Design: Who Owns What
Now that we’ve established what Medallion and data modeling are, how do they interact?
Medallion owns the data pipeline, including ingestion patterns, file formats, and handling schema changes between stages. There’s also orchestration, data quality checks, and more. These are the operational characteristics of the data pipeline, and the ways data is transformed between the bronze, silver, and gold stages.
Modeling owns the entities, attributes, relationships, the grain, etc. You can choose to normalize or denormalize your data. Also, modeling owns naming standards and semantic consistency across the data lifecycle. Notice I haven’t said data modeling is a particular approach (Star Schema, Data Vault, 3NF, OBT, etc). These are tactics you can deploy, depending on the needs of your end-users.
Medallion does not decide the data model, nor does the data model decide the data pipeline. These are orthogonal concerns.
“Gold = Star Schema,” Right? Not Necessarily.
I’ve seen discussions where people say, “Gold is a star schema.” Maybe, maybe not. Gold is simply business-ready data. In the “old days,” Gold was a data mart [ https://substack.com/redirect/2fee6bfb-8d92-4b86-ab0d-3932cf9570d6?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ] (1994?), and a data mart can be modeled however the consumer needs. You can model a data mart using a Star Schema, wide tables (OBT), 3NF, Data Vault, or any other way you see fit. The main goal is to provide end-users (usually non-technical) with the data they need, in a way that is easily consumable and valuable. That’s it. There’s not a single best way to model data for Gold, or any other stage in the Medallion stages.
Instead of worrying about the data model you’ll use, pick the approach that best serves the consumer. This is why you need to know the various tactics of data modeling, so you can understand what to use and when to use it.
For Bronze and Silver, it’s the same thing. We are just trying to progressively simplify the data.
Let’s walk through a simple example where we’ll use the same data pipeline for a fictitious retailer. We have the standard fare domains - Customers, Orders, Products - which we’ll thread through a Medallion flow.
First, the Bronze layer is a few change-data-capture (CDC) streams from the OLTP database, warts and all. The orders_raw dataset includes duplicates, late-arriving records, and soft deletes.
Next, the Silver stage contains the cleansed and conformed tables from orders_raw. Here, we have new tables such as orders_clean (order line grain, de‑duped), customers_clean (business keys resolved), and products_clean (typed attributes).
Finally, we have the Gold layer, where we can take our pick of modeling approaches.
Star: fact_orders (order line grain), dim_customer (SCD2), dim_product (SCD1), optimized for BI slice‑and‑dice.
OBT: orders_enriched with 69 flattened attributes for a specific dashboard with fixed questions.
Data Vault → Data Mart: Hubs/Links/Satellites in Silver for lineage and history. From these Hubs/Links/Satellites in Silver, you can then publish a star or OBT to Gold.
For ML, you can create features such as: customer_90d_order_count, avg_item_price_30d, days_since_last_order.
Can you just jump from Bronze to Gold? In practice, yes. But bear in mind that the data transformation steps (deduping, conformed attributes, etc) in the Silver stage will likely be in your workflow anyway. By the way, this is ETL. The Silver layer provides an opportunity to store your data at an intermediate stage.
Does this Matter?
I recently wrote about how I hate pedantic bikeshedding [ https://substack.com/redirect/3a63cfc5-dca8-433f-8bee-8fb15b1b3159?j=eyJ1IjoibjBrMyJ9.SQ5ZKHxJh0MocVfrsArKZFhT_ts26OEfWqtevr5N8ms ]. The confusion over Medallion and data modeling is not pedantic and represents a lack of understanding and knowledge. Too often, data engineers focus on data pipelines, moving data from point A to B. Sadly, I frequently see a lack of data modeling knowledge among data engineers. This leads to conflating things like data lifecycle stages with data modeling.
Use both, but don’t confuse them. If you do, you’ll end up debating colors when you should be agreeing on grain, keys, and definitions. Or the reverse, where you're debating column-level semantics when you’re discussing data orchestration.
Stop treating Bronze/Silver/Gold as data models. They’re lifecycle stages.

Unsubscribe https://substack.com/redirect/2/eyJlIjoiaHR0cHM6Ly9wcmFjdGljYWxkYXRhbW9kZWxpbmcuc3Vic3RhY2suY29tL2FjdGlvbi9kaXNhYmxlX2VtYWlsP3Rva2VuPWV5SjFjMlZ5WDJsa0lqb3hNRGN6T0RFeExDSndiM04wWDJsa0lqb3hOek13T1RVeE56SXNJbWxoZENJNk1UYzFOek0wTURZd09Dd2laWGh3SWpveE56ZzRPRGMyTmpBNExDSnBjM01pT2lKd2RXSXRNVFEzTXpBMk9TSXNJbk4xWWlJNkltUnBjMkZpYkdWZlpXMWhhV3dpZlEuMFR5bjQxYWlYcVMtOWtXWUNxbEplajJCV1ZEeGZtdkpvUENiRkNhSDNNUSIsInAiOjE3MzA5NTE3MiwicyI6MTQ3MzA2OSwiZiI6dHJ1ZSwidSI6MTA3MzgxMSwiaWF0IjoxNzU3MzQwNjA4LCJleHAiOjIwNzI5MTY2MDgsImlzcyI6InB1Yi0wIiwic3ViIjoibGluay1yZWRpcmVjdCJ9.UIW_sFXmqoH1rpBU_UZdat5vzKeHUFdk0PUqe9OuXaY?
