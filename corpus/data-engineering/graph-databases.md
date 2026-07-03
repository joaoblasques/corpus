---
type: concept
domain: data-engineering
status: draft
sources:
  - path: raw/web/choosing-the-right-graph.md
    channel: web
    ingested_at: 2026-06-16
aliases:
  - graph database
  - graph databases
  - knowledge graph
  - RDF
  - RDF knowledge graph
  - labeled property graph
  - LPG
  - property graph
  - RDF vs LPG
tags:
  - corpus/data-engineering
  - concept
created: 2026-06-16
updated: 2026-06-16
---

# Graph Databases (RDF vs Labeled Property Graph)

**TL;DR** — "Knowledge graph" collapsed two distinct traditions into one marketing category: **RDF/OWL** (descends from formal logic, knowledge representation, and the Semantic Web) and the **labeled property graph (LPG)** used by Neo4j, TinkerPop/Gremlin, etc. (descends from graph theory and connected-data applications) [^src1]. Both are graphs, but their data models, semantics, query languages, and governance differ enough that "picking the wrong one is a costly architectural mistake" [^src1].

## The two models

**RDF** — the atomic unit is the *triple* (subject, predicate, object); an RDF graph is a *set* of triples [^src1]. Predicates are globally dereferenceable IRIs, so RDF supports global identification by design and follows an **open-world assumption** (absence of a statement ≠ false) [^src1]. It carries a formal stack: RDF Schema, OWL (description-logic ontologies with decidable EL/QL/RL profiles), SPARQL (declarative, federated via `SERVICE`), SHACL (closed-world validation), PROV-O (provenance), and named graphs [^src1].

**LPG** — both nodes and relationships are first-class entities, each with an identifier, label(s), and arbitrary key–value properties; identifiers are local to the instance and the usual assumption is closed-world with no native logical/entailment layer [^src1]. Its defining engineering claim is **index-free adjacency**: relationships are stored as direct physical pointers, so a one-hop traversal is O(1) and multi-hop cost depends on the traversed subgraph rather than total graph size [^src1].

## Edge properties and the RDF 1.2 shift

Classic RDF triples can't natively carry edge metadata; practitioners used reification (four extra triples per fact), an n-ary intermediate node, or named graphs as a side channel [^src1]. **RDF 1.2** (reached W3C Candidate Recommendation 7 April 2026, earliest possible Recommendation 5 May 2026) closes this with a *triple term* (a triple used as the object of another triple, object-position-only, non-asserting, referentially transparent) and the `rdf:reifies` mechanism [^src1]. This "removes the edge-property objection that previously pushed such projects toward LPGs," weakening a historical reason to reach for an LPG [^src1]. RDF 1.2 is still at CR — feature set "stable in intent but not frozen" — and SPARQL 1.2, required to query the new constructs, was still a Working Draft, so production reliance is premature [^src1].

## Standardization

RDF is governed by a coherent W3C Recommendation suite; the LPG world was historically fragmented across vendor languages until **ISO/IEC 39075:2024 — GQL** was published 12 April 2024, "the first new ISO database query language standard since SQL in 1987" [^src1]. GQL is defined against the property-graph model (not RDF) and fuses openCypher, GSQL, and Oracle's PGQL; vendor conformance is still uneven, so Cypher / openCypher remain the practical lingua franca [^src1].

## Performance — workload-dependent, not paradigm-dependent

The source debunks the index-free-adjacency performance narrative. The famous *Neo4j in Action* benchmark (1,135× over MySQL at depth four) compared Neo4j against a MySQL schema with **no index on the join column** — an anti-pattern; with a sensible index, MySQL beat Neo4j at the same depths [^src1]. The GRADES'17 / LDBC studies found Postgres and Virtuoso competitive with or faster than Neo4j on most queries, Neo4j winning decisively only on single-pair shortest-path [^src1]. Modern SPARQL engines (e.g. QLever) execute complex queries over multi-billion-triple graphs in seconds [^src1]. Net: "performance is workload-dependent... both modern LPGs and modern triple stores deliver sub-second response on graphs of billions of edges" [^src1].

## Decision framework

- **Use RDF/OWL** when the dominant axis is meaning, cross-organizational integration, formal reasoning/entailment, FAIR/linked-open-data publishing, or long-term governance — life sciences, healthcare, cultural heritage, libraries, government [^src1].
- **Use an LPG** when the binding constraint is operational multi-hop traversal performance, rich intrinsic edge attributes, and developer velocity within a controlled boundary — fraud detection, recommendations, network topology, supply-chain graphs [^src1].
- **Use a hybrid store** (Amazon Neptune, Stardog, Ontotext GraphDB) when both axes are co-equal, budgeting for two query surfaces [^src1].

A pragmatic caveat relevant to this corpus's other pages: "if your traversal bottleneck disappears under a modern columnar SQL engine (DuckDB, ClickHouse) with well-designed materialized views, the LPG performance advantage may not justify standing up a new storage tier" [^src1].

## Related corpus pages

See [DuckDB](/data-engineering/duckdb.md) and [Materialized Views](/data-engineering/materialized-views.md) (the columnar-SQL alternative to a dedicated graph tier) and [PostgreSQL](/data-engineering/postgres.md) (competitive on bounded multi-hop workloads per the benchmarks).

[^src1]: [Choosing the Right Graph](../../raw/web/choosing-the-right-graph.md)
