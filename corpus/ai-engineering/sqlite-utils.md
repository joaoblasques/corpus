---
type: entity
domain: ai-engineering
status: draft
sources:
  - path: raw/web/web-sqlite-utils-4-0rc1-adds-migrations-and-nested-transactions-5199a144.md
    channel: web
    ingested_at: 2026-07-05
  - path: raw/web/web-release-sqlite-utils-4-0rc1-4e10b289.md
    channel: web
    ingested_at: 2026-07-05
aliases:
  - sqlite-utils
  - sqlite_utils
tags:
  - corpus/ai-engineering
  - entity
created: 2026-07-05
updated: 2026-07-05
---

# sqlite-utils

**TL;DR**: `sqlite-utils` is a Python library and CLI tool for manipulating SQLite databases, developed by [Simon Willison](/ai-engineering/simon-willison.md). The 4.0 release candidate (June 2026) adds two major features: database migrations and nested transactions [^src1].

## 4.0 Release Candidate (4.0rc1)

Released June 21, 2026. Two headline features [^src1]:

### Database migrations

Ported from the `sqlite-migrate` package. Usage:

```python
from sqlite_utils import Database
from sqlite_utils.migrations import Migrations

db = Database("mydb.db")
migrations = Migrations("my_app")

@migrations()
def m001_initial(db):
    db["users"].create({"id": int, "name": str})
```

Run via Python or `sqlite-utils migrate <db_path>` CLI. Enables schema evolution across deployments.

### Nested transactions (db.atomic())

`db.atomic()` provides nested transactions using SQLite savepoints. Terminology borrowed from Django/Peewee. Wrapping calls in `db.atomic()` creates a savepoint that rolls back independently if an inner block raises, rather than aborting the full outer transaction.

### Backwards-incompatible changes in 4.0

Notable breaking changes from 3.x [^src1]:
- Upsert syntax changed
- Python 3.8 dropped
- `db.table()` only works with tables (not views)
- `FLOAT` → `REAL` type mapping
- `[square-braces]` identifiers replaced with `"double-quotes"`
- Type detection on by default for CSV/TSV import

## See also

- [Simon Willison](/ai-engineering/simon-willison.md) — creator
- [Datasette](/ai-engineering/datasette.md) — primary consumer of sqlite-utils

---

[^src1]: [sqlite-utils 4.0rc1 adds migrations and nested transactions](../../raw/web/web-sqlite-utils-4-0rc1-adds-migrations-and-nested-transactions-5199a144.md) — Simon Willison, 2026-06-21
