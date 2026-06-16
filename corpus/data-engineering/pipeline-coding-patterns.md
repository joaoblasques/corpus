---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/web/data-pipeline-design-patterns-2-coding-patterns-in-python-st.md
    channel: web
    ingested_at: 2026-06-16
aliases:
  - code design patterns for data pipelines
  - data pipeline code patterns
  - python design patterns for data pipelines
  - factory pattern
  - strategy pattern
  - singleton pattern
  - object pool pattern
  - context managers
  - functional data pipelines
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-16
updated: 2026-06-16
---

# Pipeline Coding Patterns (Python)

**TL;DR.** The common code design patterns for building data pipelines in Python: **functional design**, **Factory**, **Strategy**, **Singleton / Object pool**, plus Python helpers (typing, dataclasses, context managers, pytest, decorators). Patterns are suggestions, not requirements — apply one only if it keeps code clean now and later; otherwise it is premature optimization [^src1]. This is part 2 (coding patterns) of a data-pipeline-design-pattern series; part 1 covers data-flow patterns [^src1]. Demonstrated by refactoring a Reddit→sqlite3 ETL script step by step [^src1].

## Functional design

"Functional code" in a DE context means three properties [^src1]:

- **Atomicity** — a function should only do one task [^src1].
- **Idempotency** — same input run multiple times yields the same output; stored output should not be duplicated [^src1]. (See [[data-engineering/idempotent-pipelines|Idempotent Pipelines]].)
- **No side effects** — a function should not affect external data beyond its output [^src1].

> "Atomicity: A function should only do one task." [^src1]

Worked fixes from the example `load` function: split DB-connection management out of `load` via **dependency injection** (accept the connection as a parameter) to restore atomicity; replace a plain `INSERT` with an `UPSERT` / `INSERT OR REPLACE` to restore idempotency [^src1]. A subtlety: once `load` accepts an injected connection, it must *not* close it, since that would mutate state external to the function [^src1]. Related FP concepts: higher-order functions, functional composition, referential transparency [^src1].

## Factory pattern

Use a Factory when **multiple pipelines follow a similar pattern** (e.g. adding ETL for Twitter, Mastodon, LinkedIn alongside Reddit) [^src1]. A factory creates the appropriate ETL object; calling code uses it unaware of the internal implementation, avoiding complex `if..else` chains [^src1]. Define a standard method set via an **abstract interface** (Python `ABC` + `@abstractmethod`) — the **abstract interface** names methods and signatures, the **concrete implementation** supplies the bodies (e.g. `SocialETL` abstract, `RedditETL`/`TwitterETL` concrete) [^src1].

- **Pros** — improves consistency across similar ETLs and eases evolution; factories over external-system connections enable testing (e.g. sqlite3 in dev, Postgres in prod; smaller Spark executors in dev) [^src1].
- **Cons** — forcing dissimilar pipelines (ETL vs ELT, API pull vs S3→S3) behind one factory makes code brittle; using a factory for only one or two pipelines is premature optimization that can slow development [^src1].

## Strategy pattern

Lets code **choose one transformation among several at runtime** [^src1]. Example: select among `standard_deviation_outlier_filter`, `random_choice_filter`, and `no_transformation`, resolved by a `transformation_factory` and injected into the pipeline's `run` [^src1]. The key constraint: all strategy functions must share the same input/output signature so they are interchangeable; proper logging is needed to know which ran [^src1].

## Singleton & Object pool

- **Singleton** — ensures only one object of a class for the program's lifetime; common for DB connections and logs. It makes testing very hard (all tests share one object) and, without guardrails, Python can still create multiple instances — generally considered an **anti-pattern** [^src1].
- **Object pool** — builds on Singleton: draw from a *pool* of objects (pool size per use case) instead of a single one [^src1]. Common where many requests need fast DB access (backend apps, stream processing) — e.g. a Psycopg2 connection pool — so requests neither create a new connection nor wait on a singleton [^src1]. Pooled connections must be reset to their initial state before return [^src1].

For **batch** data pipelines, a Factory method for DB connections is usually preferable to a pool: it allows per-environment config and avoids pool cleanup overhead [^src1].

## Python helpers

- **Typing** — type hints + a static checker (mypy) catch type-incompatibility at "compile" time rather than runtime; `Callable[[List[X]], List[X]]` types a higher-order function (first param = input types, second = output type) [^src1].
- **Dataclasses** — represent data as objects: type hints + IDE completion, default values, `__post_init__` custom processing, frozen (immutability emulation), inheritance. Cons: slight creation overhead; overkill for simple dict data [^src1].
- **Context managers** — clean up external connections on success or error without duplicating `try/except/finally`; build with the `@contextmanager` decorator and a `yield`, consumed via a `with` block (the post-`yield` code runs on exit to commit and close) [^src1]. This is the proper home for the cursor creation that functional `load` should not own [^src1].
- **Testing with pytest** — one test file per pipeline (`test_reddit.py`); set up / tear down tables per run at session / class / function **scope** for straightforward assertions; **fixtures** supply static data so tests avoid hitting external APIs; **mocking** (`mocker` / `session_mocker`) overrides behavior — mock at the location a function is *used*, not where it is defined; `conftest.py` holds directory-wide fixtures [^src1].
- **Decorators** — add functionality to other functions; the project's `log_metadata` decorator logs function name, input args, and run time into a metadata table for **data lineage** / debugging, using the `inspect` module [^src1].

## Misc engineering hygiene

Consistent project structure and naming (Google style guide); automated formatting/lint/type checks (`black`, `isort`, `flake8`, `mypy`) run via a `Makefile` and enforced with a **pre-commit git hook**; `dotenv` for per-environment config from `.env`; `venv` (or Docker) for reproducible environments [^src1].

## Guiding principle

The design patterns are presented as suggestions, not requirements [^src1]. Ask whether a pattern keeps code clean now and in the future; if the answer is "no" or "maybe," defer it. E.g. with only two pipelines and no growth expected, skip the Factory [^src1].

## Related pages

- [[data-engineering/idempotent-pipelines|Idempotent Pipelines]] — the idempotency property of functional design, in depth
- [[data-engineering/python-for-data-engineering|Python for Data Engineering]] — Python as glue across ETL/DQ/test/orchestrate; disk vs memory
- [[data-engineering/data-engineering-best-practices|Data Engineering Best Practices]] — pipeline-level best practices (3-hop, DQ, idempotency, DRY, metadata, tests)
- [[data-engineering/etl-pipeline|ETL Pipeline]] — Extract/Transform/Load; the structure these patterns refactor

[^src1]: [Data Pipeline Design Patterns - #2. Coding patterns in Python](../../raw/web/data-pipeline-design-patterns-2-coding-patterns-in-python-st.md)
