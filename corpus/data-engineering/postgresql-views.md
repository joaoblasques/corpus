---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/web/strong-views-on-postgresql-views.md
    channel: web
    ingested_at: 2026-06-16
aliases:
  - PostgreSQL views
  - Postgres views
  - SQL views
  - VIEW
  - CREATE VIEW
  - writable views
  - auto-updatable views
  - security_invoker
  - nested view spiral
  - pg_rewrite
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-16
updated: 2026-06-16
---

# PostgreSQL Views

**TL;DR.** A PostgreSQL VIEW is not a stored object the executor consults — it is a stored parse tree (a macro) that the *rewriter* pastes into your query before planning[^src1]. This makes simple views free (the planner inlines them) but rigid: columns are pinned to attribute numbers, types and `SELECT *` are frozen at `CREATE VIEW` time, and any structural change to an underlying column is blocked or cascades. "Rigidity is the feature, not a bug"[^src1].

This page is a focused deep-dive on view mechanics and schema-evolution pain. For PostgreSQL as a general data platform see [PostgreSQL](/data-engineering/postgres.md); for materialized views across engines see [Materialized Views](/data-engineering/materialized-views.md).

## The appeal

Views promise decoupling logical intent from physical storage[^src1]. Define "active customer" once and reuse it everywhere — every query, report, and dashboard shares one definition, so a rule change is one line in one place[^src1]. They can also be a real security boundary: one definition means one result set rather than a forgotten predicate in three hand-written queries[^src1]. For simple views there is no performance penalty — Postgres inlines them so the planner sees through to the underlying SQL[^src1].

## Views are rewrite rules

> "A view is a macro. When you reference one, Postgres pastes its body into your query before the planner runs."[^src1]

- The `pg_class` row (`relkind = 'v'`) is an empty shell — name, column list, grants, but no definition. The actual `SELECT` lives in **`pg_rewrite`** as the `_RETURN` rule (`ev_type = 1` = SELECT, `is_instead = t`)[^src1].
- Between parser and planner, the **rewriter** walks the parse tree, finds relations with rules, and substitutes the rule body in place[^src1].
- After rewrite the planner can usually **flatten** the subquery via *subquery pull-up*, leaving outer predicates next to inner ones so indexes stay reachable — this is what makes simple views free. It **bails out** when the body has `LIMIT`, `DISTINCT`, an aggregate, or a set operation, leaving the subquery as a barrier that predicates cannot move past[^src1].
- `CREATE RULE` historically exposed this same machinery as a general feature; it is effectively deprecated outside views (triggers do the same jobs without the surprises)[^src1].

Two consequences drive everything else[^src1]:

- **Columns are referenced by attribute number, not name.** The tree remembers "attribute 2 of relation 16385", so a rename keeps working but dropping a column in the middle is refused upfront.
- **The body is expanded once per reference.** A volatile expression like `random()` evaluates separately in each copy — joining a view to itself can yield different values per row.

A useful side effect: views are **immune to search-path attacks** that bite `SECURITY DEFINER` functions, because identifiers resolve to OIDs at `CREATE VIEW` time[^src1].

## The nested view spiral

A three-layer chain (`customer_summary` on `customer_orders` on `active_customers`) gives a new engineer no signal that `SELECT * FROM customer_summary WHERE id = $1` expands into a three-layer rewrite, a `LEFT JOIN` against twelve months of orders, and a `GROUP BY` the planner can't push the `id` predicate through[^src1].

> "You cannot reason about the performance of a query against a view without reading the view, the views it depends on, and the tables underneath."[^src1]

## Writable views — the half-kept promise

Postgres makes views over a *single* base table (no joins, aggregates, or `DISTINCT`) **auto-updatable**: `INSERT`/`UPDATE`/`DELETE` are rewritten against the underlying table[^src1]. Add a join, aggregate, or `GROUP BY` and the write path goes silent — `SELECT` still works but `INSERT` errors and you must wire up `INSTEAD OF` triggers by hand. The rules for what qualifies aren't visible in the view definition; you find out at write time, in production[^src1]. `WITH CHECK OPTION` rejects writes that would produce a row the view can't see (`LOCAL` checks only this view, `CASCADED` — the default — checks every underlying view)[^src1].

## Views and row-level security

RLS policies live on tables, not views[^src1]:

- A view runs **as its owner** by default; table owners bypass RLS unless `FORCE ROW LEVEL SECURITY` is set. A view owned by a privileged role is therefore a silent hole in any RLS scheme[^src1].
- Since **PostgreSQL 15**, `CREATE VIEW ... WITH (security_invoker = true)` runs the view as the *calling* user so RLS evaluates against the actual caller[^src1].
- **Materialized views are structurally incompatible with RLS**: `REFRESH` runs as the owner, the rows are physically stored, and `security_invoker` has nothing to attach to — enforce access at the layer that reads the matview, never below it[^src1].

## Schema evolution — where it hurts

While the schema holds still, everything is invisible. The moment you change a referenced column, all the mechanics surface at once[^src1]:

- **Drop / rename / type change** on a referenced column is blocked: `ERROR: cannot drop column ... because other objects depend on it`. Even widening `VARCHAR(255)` to `TEXT` — lossless — is forbidden, because the stored definition references the old type OID[^src1].
- **`CASCADE` drops the dependent views** (along with their grants, RLS policies, and downstream dependencies) — it does not modify them, and there is no undo[^src1].
- The manual path is: save every definition, drop in reverse dependency order, alter the table, recreate in forward order, reapply all grants — a full migration project for thirty views[^src1].

### The `SELECT *` trap

`SELECT *` does not save you — it makes things worse. Postgres **expands `*` to explicit columns at creation time and freezes it**, so new base-table columns never appear, and a dropped original column blocks the migration the same way — except the dependency is now hidden in the catalog instead of visible in the body[^src1].

> "Always use explicit column lists in views. At least then the dependency is visible and the breakage is predictable."[^src1]

## The architect's stigma — and why it's outdated

Senior engineers historically warned against views ("views are slow", "views hide the real query")[^src1]. The warning had specific roots in Oracle shops, whose era cost-based optimiser struggled to merge predicates through non-trivial views, pushing teams to materialized views or PL/SQL packages; Postgres carried the baggage by association[^src1]. The optimiser has improved but the reputation hasn't caught up — "reach for a view in a code review today and someone will still object on principle"[^src1].

## How other databases differ (the trade-off is real everywhere)

- **Oracle** marks dependent views `INVALID` and recompiles on next access — moving breakage from migration time (where you're paying attention) to runtime (where you may not be)[^src1].
- **SQL Server** has `sp_refreshview`, but one view at a time, with no dependency-chain ordering, and it fails on dropped-column references[^src1].
- **PostgreSQL** chose **compile-time safety**: no surprise `INVALID` views, no silently wrong results — at the cost of manual dependency management on every schema change[^src1].

## Survival kit

- **Transactional DDL** is the saving grace: wrap the whole drop-alter-recreate-regrant sequence in `BEGIN/COMMIT` so a typo or missed grant rolls back cleanly — something Oracle and SQL Server cannot do for most DDL[^src1]. It does not solve locking: `DROP`/`CREATE VIEW` and `ALTER TABLE` take `AccessExclusiveLock`, so keep the transaction tight and off peak[^src1].
- **Map the dependency graph first**: `pg_depend` joined through `pg_rewrite` to `pg_class` (views depend on tables via their rewrite rule, not directly), walked with a recursive CTE — run it *before* the migration, not after the incident[^src1].
- **Versioning**: create `active_customers_v2` alongside v1 and migrate consumers one at a time; schema-based versioning (`CREATE SCHEMA api_v2`) is cleaner than name suffixes for public-facing APIs[^src1].
- **Prior art in `pg_dump`**: the placeholder-view trick (emit a stub with the right column list, then `CREATE OR REPLACE VIEW` once dependencies exist) already rewrites a view body while preserving identity and grants — but it isn't exposed as user-facing DDL[^src1].

## The missing primitive

The pain traces to one gap: there is no structural `ALTER VIEW`[^src1]. `ALTER VIEW` handles renames/owner/schema/defaults but nothing structural; `CREATE OR REPLACE VIEW` can only **append** columns at the end[^src1]. A real `ALTER VIEW DROP COLUMN / ADD COLUMN / ALTER COLUMN TYPE` is what would make views safe to evolve — the catalog mechanism exists (as `pg_dump` proves); the DDL is what's missing[^src1].

> "Even without it, views are still worth using. Just don't pretend they're tables."[^src1]

## See also

- [Storing Intermediate Results in SQL](/data-engineering/sql-intermediate-results.md) — when to use a view vs CTE vs temp table vs materialized view
- [Materialized Views](/data-engineering/materialized-views.md) — the materialized counterpart
- [PostgreSQL](/data-engineering/postgres.md) — Postgres as a general data platform
- [Data Engineering hub](/data-engineering/README.md)

[^src1]: [Strong Views on PostgreSQL Views](../../raw/web/strong-views-on-postgresql-views.md)
