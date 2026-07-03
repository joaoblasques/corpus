# Batch ingest (N>10) — cluster pipeline

Externalized from CLAUDE.md §8.1 (third compression pass, Thrift #8). The always-on
invariant stays in CLAUDE.md: **only the Coordinator writes shared files**
(`index.md`, `log.md`, `_domains.md`, `_config.md`); Workers own disjoint domains.

Coordinator + parallel Workers:

| Phase | Owner | What |
|---|---|---|
| 0 Pre-flight | Coordinator | Re-read CLAUDE.md + index/domains/config. Check stamps/collisions → skip/force/append list. |
| 1 Survey & cluster | Coordinator | Title+tags+¶1 per source (no full reads). Cluster thematically → route to existing domains (default); ≥3 distinct sources with no fit → propose new domain (confirm first); 1–2 sources → provisional; <3 no fit → fold as pages. Surface cluster→domain map for confirmation. |
| 2 Entity registry | Coordinator | Extract 3–10 candidates/source. Dedup against `index.md` + across clusters by name/alias. Build `{slug → aliases, domain, path}` registry before any writes. |
| 3 Per-cluster ingest | Workers (one/domain, parallel) | Read full bodies. Create/update pages via registry (no dupes). Citation gate every claim (§7). Target 10–15 page cascade. Link new pages from domain hub — no orphans. Workers return deltas; never write shared files. |
| 4 Integrate | Coordinator | Stamps, `index.md` update, `log.md` append, inbox moves — all serialized. |
| 5 Verify | Coordinator | Lint scoped to touched domains (orphans, dupes, contradictions, stubs, domain health). Apply safe fixes; surface rest. |
