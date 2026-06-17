---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/email/email-2025-11-05-python-essentials-for-data-engineers.md
    channel: email
    ingested_at: 2026-06-15
  - path: raw/web/python-essentials-for-data-engineers-start-data-engineering.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/web/github-josephmachado-python-essentials-for-data-engineers-co.md
    channel: web
    ingested_at: 2026-06-15
  - path: raw/web/web-how-to-extract-data-from-apis-for-data-pipelines-using-pytho.md
    channel: web
    ingested_at: 2026-06-17
aliases:
  - python for data engineers
  - python essentials
  - python data engineering
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-15
updated: 2026-06-17
---

# Python for Data Engineering

**TL;DR.** "Knowing Python" for data engineering is not the whole language — it's a focused set of concepts that map to pipeline tasks (extract/load, transform, data quality, testing, scheduling, orchestration) [^src1]. The unifying mental model: **data lives on disk, is processed in memory**, and Python is mostly the *glue* controlling data flow — the heavy lifting happens in external systems (Spark, Snowflake, BigQuery) you drive *via* Python [^src1].

## The foundational idea: disk vs memory

A running script is a **process** using part of RAM. Reading from disk (CSV, etc.) means moving data from disk *into memory* to process it [^src1]. RAM is expensive, disk (HDD/SSD) cheap; often the data is larger than memory — that's when you reach for distributed systems like [[data-engineering/apache-spark|Spark]] or larger-than-memory engines like [[data-engineering/duckdb|DuckDB]] [^src1]. (See [[data-engineering/storage-fundamentals|Storage Fundamentals]] for the hierarchy.)

## Python basics that matter

Variables, operations, **data structures** (list = ordered + indexed; dict = hashed key-value, fast lookup; set = unique elements; tuple = immutable + ordered), loops + comprehensions, functions, classes/objects, libraries, and exception handling [^src1].

## Python across the pipeline (ETL)

Python is the glue: **Extract** from sources, **Transform**, **Load** into destinations [^src1].

### Extract & Load — read/write any system

| System | Python tooling |
|---|---|
| Database drivers | `psycopg2`, `sqlite3`, `duckdb` — connect, query, read [^src1] |
| Cloud SDKs | AWS `boto3`, GCP `gsutil` — extract/load from object storage [^src1] |
| APIs | `requests` for HTTPS endpoints [^src1] |
| Files | stdlib `csv`; libs for XML, xlsx, `parquet` [^src1] |
| SFTP/FTP | `paramiko`, `ftplib` [^src1] |
| Queues | `pykafka` etc. for [[data-engineering/kafka|Kafka]], Kinesis, Redpanda [^src1] |

### Transform — in Python or push to the database

- **stdlib** — work on native structures (dict/list/tuple): `csv`, `json`, `gzip` [^src1].
- **DataFrame libs** — pandas, polars, Spark; tabular data, in-memory variants are memory-bound [^src1].
- **SQL via Python** — use a DB driver to run SQL so processing happens *in the database*, not Python memory [^src1].

Key nuance: with Spark/Dask/Snowflake/BigQuery you *interact* via Python but the bulk of work runs inside those external systems [^src1].

### Data Quality — define and check expectations

Libraries: **Great Expectations** (define/run checks across DuckDB/Spark/Snowflake) and **Cuallee** (lightweight, multi-engine) [^src1]. See [[data-engineering/data-quality|Data Quality]].

### Code Testing — ensure code does what it should

Run *before* deploy (distinct from runtime data-quality checks) [^src1]. stdlib `unittest`; the popular ergonomic choice is **pytest** with broad plugin support [^src1].

### Scheduler & Orchestrator

- **Scheduler** — runs pipelines at set times (loop: check for due tasks, run, sleep) [^src1].
- **Orchestrator** — controls execution order/parallelism via a **DAG** (Directed Acyclic Graph): [[data-engineering/dbt|dbt core]] (orders SQL models), Airflow, Dagster [^src1]. See [[data-engineering/data-orchestration|Data Orchestration]].

## API extraction patterns in Python

APIs are one of the most common data sources for modern pipelines. Using `requests` as the base, the full pattern stack [^src4]:

### HTTP basics

```python
import requests
response = requests.get(url, headers={"Authorization": f"Bearer {token}"}, params={"page": 1})
data = response.json()  # parse JSON body
```

Always check `response.status_code`: `2xx` = success; `4xx` = client error (auth, bad params); `5xx` = server error (retry).

### Pagination

Most APIs paginate responses to limit result size. Three common patterns [^src4]:

| Pattern | Mechanism | Termination |
|---|---|---|
| Limit/offset | `?limit=100&offset=0` — increment offset by limit per page | `len(items) < limit` |
| Page number | `?page=1` — increment `page` | `len(items) == 0` |
| Next-page link | Response body contains `next_url` field | `next_url is None` |

```python
all_data = []
offset = 0
while True:
    response = requests.get(url, params={"limit": 100, "offset": offset})
    data = response.json()["results"]
    all_data.extend(data)
    if len(data) < 100:
        break
    offset += 100
```

### Retries with exponential backoff

Transient failures (rate limits, brief outages) require retry logic. `tenacity` is the idiomatic library [^src4]:

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def fetch_with_retry(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
```

Or simple manual backoff:
```python
import time
for attempt in range(max_retries):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        time.sleep(2 ** attempt)  # exponential backoff
```

### Rate limiting

Respect API rate limits proactively to avoid 429 errors [^src4]:
```python
import time
RATE_LIMIT_DELAY = 0.1  # 100ms between requests
# ...in loop...
time.sleep(RATE_LIMIT_DELAY)
```

### Authentication patterns

| Method | Header |
|---|---|
| API key | `"Authorization": f"Bearer {api_key}"` or `"X-API-Key": api_key` |
| OAuth2 | Exchange client credentials for a Bearer token at `/oauth/token`, then use the token |
| Basic Auth | `requests.get(url, auth=(username, password))` |

Store credentials in environment variables or a secrets manager; never hardcode [^src4].

### Production pattern (end-to-end)

```python
import requests, json
from datetime import datetime

def extract_from_api(api_key, base_url):
    headers = {"Authorization": f"Bearer {api_key}"}
    all_data, page = [], 1
    while True:
        response = requests.get(f"{base_url}/data",
                                headers=headers,
                                params={"page": page, "per_page": 100})
        response.raise_for_status()
        result = response.json()
        data = result.get("data", [])
        all_data.extend(data)
        if len(data) < 100 or not result.get("has_more"):
            break
        page += 1
    return all_data

data = extract_from_api(api_key, base_url)
with open(f"data_{datetime.now().strftime('%Y%m%d')}.json", "w") as f:
    json.dump(data, f)
```

See [[data-engineering/data-observability|Data Observability]] for monitoring pipelines that consume API data (lag detection, flow interruption patterns apply directly to API extraction failure modes).

## Takeaway

The library landscape is overwhelming, but the point is that **most DE tasks can be done with Python** — when faced with tool/vendor overload, find the Python library that fulfils the requirement [^src1]. Each concept ships with a hands-on workbook (`python_essentials_for_data_engineers`) runnable in GitHub Codespaces [^src1][^src3]. This reinforces the [[data-engineering/data-engineer-role|fundamentals-over-tools]] principle.

## Related

- [[data-engineering/storage-fundamentals|Storage Fundamentals]] — disk vs memory in depth
- [[data-engineering/data-quality|Data Quality]] · [[data-engineering/data-orchestration|Data Orchestration]]
- [[data-engineering/dbt|dbt]] · [[data-engineering/apache-spark|Apache Spark]] · [[data-engineering/duckdb|DuckDB]]
- [[data-engineering/de-portfolio-projects|DE Portfolio Projects]]
- [[data-engineering/README|Data Engineering hub]]

---

[^src1]: [Python essentials for data engineers](../../raw/web/python-essentials-for-data-engineers-start-data-engineering.md)
[^src2]: [Python essentials for data engineers (newsletter)](../../raw/email/email-2025-11-05-python-essentials-for-data-engineers.md)
[^src3]: [python_essentials_for_data_engineers (code)](../../raw/web/github-josephmachado-python-essentials-for-data-engineers-co.md)
[^src4]: [How to Extract Data from APIs for Data Pipelines Using Python](../../raw/web/web-how-to-extract-data-from-apis-for-data-pipelines-using-pytho.md)
