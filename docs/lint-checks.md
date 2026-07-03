# Lint checks

Externalized from CLAUDE.md §8.3 (third compression pass, Thrift #8). Trigger and
approval gate stay in CLAUDE.md: "lint" (full) or "lint `<domain>`" (scoped); check
in order, output report, apply fixes only with approval.

| Check | Action |
|---|---|
| Orphan pages (0 inbound hub links) | Link or flag for archive |
| Stubs >14 days old | Flag for expansion or archive |
| Duplicate entities (alias overlap) | Propose merge |
| Contradictions between pages | Create/update synthesis page |
| Implicit concepts (3+ page references, no own page) | Propose creation |
| Stale claims (newer source contradicts) | Update with citation |
| Domain health (<3 pages, >30 days) | Propose merge into sibling |
| Provisional domains (>30 days, <3 sources) | Propose merge or removal |
| Topic-mixed pages | Propose split |
