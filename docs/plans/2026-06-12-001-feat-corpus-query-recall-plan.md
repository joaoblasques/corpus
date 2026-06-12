---
type: plan
status: active
feature: corpus /query — factual recall
origin: docs/brainstorms/2026-06-12-corpus-query-recall-requirements.md
created: 2026-06-12
sequence: 001
depth: standard
---

# Corpus `/query` (Factual Recall) — Implementation Plan

> **For agentic workers:** this is a decisions-and-scope plan (ce-plan output). Each implementation unit lists exact repo-relative file paths, a test file path, and enumerated test scenarios. Execute with `superpowers:subagent-driven-development` (one unit per subagent, spec-then-quality review between units), consistent with how `collect-email`/`collect-youtube`/`collect-obsidian` were built.

**Goal:** Add a `/query` operation that answers a factual-recall question from cited corpus pages, fills thin coverage with labeled web top-up (WebSearch → `fetch_link.fetch`), auto-queues fetched web sources to `raw/_inbox/`, logs gaps to `corpus/_log.md`, and offers to file a non-trivial answer back as a synthesis page.

**Architecture:** A Claude-driven skill (`.claude/skills/query/SKILL.md`) owns judgment — page selection across `corpus/_index.md`, synthesis, citations, the file-back decision. A thin deterministic helper (`bin/query.py`, pytest-covered) owns mechanical I/O — dedup-checked inbox queueing of fetched web sources and append-only gap logging. This is the same skill-owns-judgment / Python-owns-I/O split used by the three existing collectors.

**Tech stack:** Python 3 stdlib + `PyYAML` (already present), reuse of `bin/fetch_link.py` (httpx + trafilatura) and `bin/collect_email.py` helpers (`slugify`, `yaml_scalar`, `link_target`, needle-based dedup). URL discovery via the session **WebSearch** tool (skill-level, not Python). No new dependencies, no OAuth, no new tokens.

---

## Problem frame & scope

Three of four strategy tracks (Collection, Ingestion/Synthesis, Schema/Integrity) are built; the corpus holds ~96 cited pages across 6 domains but cannot yet be *used* as a trustworthy second brain. `CLAUDE.md` §8.2 Query exists but is thin (exercised once, producing `corpus/ai-engineering/optimizing-claude.md`). This feature operationalizes §8.2 into a repeatable, gap-honest, self-feeding `/query`.

**In scope (v1):** factual recall ("what did I learn about X?") — a synthesized, cited answer; labeled web top-up on thin coverage; auto-queue of fetched web sources; gap logging; approval-gated synthesis file-back.

**Out of scope (carried from origin, unchanged):** cross-source synthesis mode, decision-support mode, proactive rediscovery/push, semantic/vector retrieval, headless/scheduled querying.

---

## Requirements traceability

| Req (origin) | Where satisfied |
|---|---|
| **R1** answer from `_index.md` + page reads | Skill §"Retrieve & answer" (Unit 4) — LLM index-selection |
| **R2** every corpus claim inline-cited to pages | Skill answer-format rules (Unit 4); enforces §7 |
| **R3** covered → no web fetch, no inbox write | Skill coverage gate (Unit 4) — branch before any fetch |
| **R4** thin → fetch web, mark `[fresh — not yet in corpus]` | Skill gap branch (Unit 4) + `fetch-and-queue` CLI (Unit 2/3) |
| **R5** auto-queue fetched web to `raw/_inbox/` (channel web), dedup by `source_url`, no per-query confirm | `already_queued` (Unit 1) + `build_web_document` (Unit 2) + `fetch-and-queue` CLI (Unit 3) |
| **R6** every gap query appends a `query` entry to `_log.md` | `log_gap` + `log-gap` CLI (Unit 3) |
| **R7** offer synthesis file-back when non-trivial; write only on approval; update `_index.md`/`_log.md` | Skill §"File-back" (Unit 4) — Claude authors page per §3/§4 |
| **R8** never present model knowledge as a corpus claim; label general/web | Skill answer-format rules (Unit 4) |
| **R9** web-fetch failure handled gracefully; gap still logged; nothing fabricated/queued for that source | `fetch-and-queue` returns structured error (Unit 3); skill failure branch (Unit 4) |
| **R10** interactive Claude-Code-session op, not headless | Skill framing (Unit 4); helper is callable but the operation is session-driven |

---

## Key decisions (resolved at planning; see origin "Outstanding questions → Deferred to planning")

1. **Retrieval = LLM selection over `corpus/_index.md`** (not a deterministic keyword matcher). The index is one line per page (path · type · status · one-line summary) and is loaded at session start per `CLAUDE.md`. Claude selects candidate pages by topic and `aliases`, then reads them. Rationale: the index is small and purpose-built; a Python matcher would duplicate judgment the agent does better, and the single prior filed-back query worked exactly this way. *Consequence:* recall quality rides on index freshness — the plan does not add a vector index (explicitly deferred); if recall degrades at scale, that is the named follow-up.
2. **Web-fetch cap = 3 per query, configurable** (`--max-fetch`, default 3). URL **discovery** is the session **WebSearch** tool (skill step); **extraction** is `fetch_link.fetch(url)`. Rationale: a v1 factual-recall gap is one topic, not a survey; 3 bounds cost. (collect-email's cap of 10 covers a whole newsletter — a wider surface.) This also resolves the origin's unstated question of *where gap URLs come from*: WebSearch feeds fetch_link.
3. **File-back offered when the answer drew on 2+ corpus pages OR incorporated kept web top-up.** A single-page restatement is trivial → no offer. Documented as a guideline in the skill (Claude's judgment), not a hard numeric gate. Rationale: "non-trivial/derived" means synthesized-across-sources or introduced-fresh-material-worth-keeping.

Additional decisions:
- **Helper writes only to `raw/_inbox/`; Claude writes corpus pages.** `bin/query.py` never touches `corpus/` except appending to `corpus/_log.md` (an explicitly Claude-owned file the helper is permitted to append to under §2/§12, mirroring how ingest logs). Synthesis pages are authored by Claude per §3/§4 with citations/wikilinks — no Python scaffolding of corpus content (judgment-heavy, schema-bound).
- **`via_query` provenance field** on queued web sources (parallel to `via_email`/`via_vault_list`) records that the source entered through a query gap — supports the "query is a third intake channel" tracking noted in the origin's Consequence.
- **Dedup needle = `source_url: <url>\n`** across `raw/_inbox` + `raw/web` + `raw/youtube`, reusing the `already_collected` needle pattern (which keys on `gmail_message_id:`). YouTube gap links dedup against `raw/youtube` too.

---

## File structure

| File | Action | Responsibility | Network | Tested |
|---|---|---|---|---|
| `bin/query.py` | create | Deterministic core + CLI: `already_queued`, `build_web_document`, `queue_source`, `log_gap`; subcommands `fetch-and-queue`, `log-gap`. Reuses `collect_email` helpers + `fetch_link.fetch`. | only via `fetch_link` in `fetch-and-queue` | pytest |
| `tests/test_query.py` | create | Pure + mocked tests for `bin/query.py`. | no (mock fetch) | — |
| `.claude/skills/query/SKILL.md` | create | Drives the operation: retrieve → coverage-gate → answer (cited) / gap (web top-up, labeled) → queue → log → offer file-back. Safety + trust rules. | — (skill) | — |
| `CLAUDE.md` | modify → v0.8 | Replace thin §8.2 with the operationalized `/query` flow; add `query`-channel/`via_query` note; bump §15 + log entry. | — | — |
| `corpus/_config.md` | modify | Add `via_query` to channel/provenance reference; note `/query` as a `web`-channel intake path. | — | — |
| `tests/` | (existing) | All existing tests (113 after collect-obsidian) stay green — regression gate. | — | — |

> Confirm the existing test directory name/location during Unit 1 (repo uses `pytest`; place `test_query.py` alongside the existing collector tests, whatever their directory).

---

## Implementation units

### Unit 1 — `already_queued` dedup (pure)

**Files:** Create `bin/query.py`; Test `tests/test_query.py`.

Mirror `collect_email.already_collected`, but key on `source_url: <url>\n` and search `raw/_inbox` + `raw/web` + `raw/youtube`. Signature: `already_queued(source_url: str, search_dirs: list[Path] | None = None) -> bool`. Default dirs constant `DEDUP_DIRS` at module top.

**Test scenarios (`tests/test_query.py`):**
- Returns `True` when a file under a search dir contains the exact `source_url: <url>` line.
- Returns `False` when no file contains it.
- Substring/partial-URL safety: `source_url: https://a.com/x` does **not** match a query for `https://a.com/` (needle is line-anchored with trailing `\n`).
- Skips unreadable/binary files without raising (OSError/UnicodeDecodeError swallowed, like `already_collected`).
- Empty/missing search dir is skipped silently.

### Unit 2 — `build_web_document` (pure)

**Files:** Modify `bin/query.py`; Test `tests/test_query.py`.

Build a normalized markdown source mirroring `collect_email.build_link_document`. Frontmatter: `channel: web`, `source_url:` (via `yaml_scalar`), `via_query:` (the question text, via `yaml_scalar`), `fetched_at:`, then blank line + body. Signature: `build_web_document(meta: dict, text: str) -> str`.

**Test scenarios:**
- Output starts with `---\n`, contains `channel: web`, `source_url: <url>`, `via_query: <question>`, `fetched_at: <date>`, closes frontmatter, then the stripped body.
- A question containing a colon/quote is quoted correctly (delegates to `yaml_scalar`).
- Body is `.strip()`-ed and trailing newline present (round-trips with a YAML frontmatter parser).

### Unit 3 — `queue_source` + `log_gap` + CLI

**Files:** Modify `bin/query.py`; Test `tests/test_query.py`.

- `queue_source(question, fetch_result, inbox=None, dedup_dirs=None) -> dict`: if `already_queued(source_url)` → `{"status":"duplicate", ...}`; else build doc, write to `raw/_inbox/` via `collect_email.link_target(title, base_dir, message_hint=source_url)` for collision-safe naming, return `{"status":"written","path":...}`.
- `log_gap(question, uncovered_note, log_path=None) -> None`: append a `## [YYYY-MM-DD HH:MM] query | <question>` block (§12 format) with a `- gap:` line describing what the corpus did not cover and a `- queued:` line listing queued source paths (or `none`). Append-only; never rewrite existing content. Date/time passed in by caller (CLI supplies it) so the function stays deterministic/testable.
- **CLI** (`main`): subcommand `fetch-and-queue --question Q --url U [--inbox DIR]` → calls `fetch_link.fetch(U)`; on success `queue_source`; on `fetch_link` failure (paywall/blocked/unsupported) return `{"status":"error","error":...,"url":U}` (R9 — never fabricate, never queue). Subcommand `log-gap --question Q --note N --at "YYYY-MM-DD HH:MM"`. Both print a JSON result line and return 0/1 like `collect_email.main`.

**Test scenarios:**
- `queue_source` writes a file under a `tmp_path` inbox and returns `status: written` with the path; the file contains `via_query` and `source_url`.
- `queue_source` on an already-queued `source_url` returns `status: duplicate` and writes nothing.
- Filename collision (same title) produces a distinct path via `link_target` (hash suffix from `source_url`).
- `log_gap` appends a well-formed `query` block to a `tmp_path` log; a second call appends again without disturbing the first (append-only).
- `fetch-and-queue` CLI with `fetch_link.fetch` **mocked** to return an article dict → writes inbox file, prints `status: written`, exit 0.
- `fetch-and-queue` CLI with `fetch_link.fetch` **mocked to raise** (e.g. `ValueError("unsupported url")`) → prints `status: error`, writes nothing, exit 1 (R9).
- `fetch-and-queue` CLI with `already_queued` true → `status: duplicate`, no write.
- No live network or live `_log.md` writes in any test (mock fetch; use `tmp_path` for inbox + log).

### Unit 4 — `.claude/skills/query/SKILL.md`

**Files:** Create `.claude/skills/query/SKILL.md`.

Frontmatter `name: query`, `description:` (factual recall against the corpus; cited answer; labeled web top-up on gaps; offers synthesis file-back; interactive). Body sections:

1. **Operation framing** — interactive session op (R10); read `CLAUDE.md` §8.2, `corpus/_index.md` first.
2. **Retrieve** — select candidate pages from `corpus/_index.md` by topic + `aliases` (LLM selection, Decision 1); read them.
3. **Coverage gate (R3)** — if the corpus fully covers the question → answer from pages only; **no WebSearch, no `fetch-and-queue`, no `log_gap`**. State which pages answered it.
4. **Answer format (R2, R8)** — every non-trivial corpus claim carries an inline citation to the corpus page(s); never present model/general knowledge as a corpus claim. Use the `[[domain/page|Title]]` wikilink style.
5. **Gap branch (R4, R5, R9)** — if thin: run **WebSearch** to find ≤`--max-fetch` (default 3) candidate URLs; for each, `python3 bin/query.py fetch-and-queue --question … --url …`. Read each `written` file to ground the answer; mark those claims **`[fresh — not yet in corpus]`**, visually distinct from cited corpus claims. On `error` results, state the gap couldn't be auto-filled for that source — fabricate nothing.
6. **Log the gap (R6)** — `python3 bin/query.py log-gap --question … --note … --at "<now>"` with queued paths.
7. **File-back (R7)** — if the answer drew on 2+ corpus pages OR kept web top-up (Decision 3), **offer** to save a `synthesis` page. On approval: Claude authors `corpus/<domain>/<topic>.md` per §3/§4 (type `synthesis`, full frontmatter, citations, wikilinks), updates `corpus/_index.md` and appends to `corpus/_log.md`. On decline: persist nothing beyond the gap log.
8. **Safety rules** — helper writes only to `raw/_inbox/`; corpus pages are written by Claude only on explicit approval; covered queries never write anything; never fabricate on fetch failure.

> No automated test (skill prose). Validate by walking AE1–AE4 (below) manually during review.

### Unit 5 — Schema + config (`CLAUDE.md` v0.8, `corpus/_config.md`)

**Files:** Modify `CLAUDE.md`; Modify `corpus/_config.md`.

- `CLAUDE.md` §8.2: replace the thin Query description with the operationalized flow (retrieve → coverage gate → cited answer / labeled web top-up → auto-queue → gap log → offer file-back), citing R1–R10 behavior. Note `/query` as a third `web`-channel intake into `raw/_inbox/` and the `via_query` provenance field. Bump §15 to **v0.8** with a one-line rationale; append a `## [YYYY-MM-DD HH:MM] schema | v0.8 — operationalized §8.2 /query` entry to `corpus/_log.md`.
- `corpus/_config.md`: add `via_query` to the channel/provenance reference and a one-line note that `/query` queues gap-filling web sources into `raw/_inbox/` (channel `web`).

**Test scenarios:** none (docs). Review check: §8.2 internally consistent with R1–R10; version bumped; log entry present.

---

## Dependencies & sequencing

1. **Unit 1 → Unit 2 → Unit 3** (Python core, strict order — Unit 3 depends on 1 & 2). TDD; pure functions first, CLI + mocked-fetch last. Existing test suite is the regression gate.
2. **Unit 4** (skill) after the helper exists, so the skill's CLI calls are real.
3. **Unit 5** (schema/config) last — documents the shipped behavior; v0.8 bump + log entry.
4. Branch: a fresh `feat/corpus-query` branch off `main`. Finish via `superpowers:finishing-a-development-branch`.

**Reuses (no reimplementation):** `bin/fetch_link.py::fetch`; `bin/collect_email.py::{slugify, yaml_scalar, link_target}` and its `already_collected` needle pattern; the §12 log format; the v0.6 ingest pipeline downstream (queued web sources drain on the next ingest wave — not part of this feature).

---

## Acceptance examples (validate before finishing)

- **AE1 (covered)** — "Spark OOM tuning" (covered by `data-engineering/apache-spark`): cited answer from corpus pages only; no WebSearch; no `raw/_inbox/` write; no gap log.
- **AE2 (gap → web)** — an uncovered topic: answer notes the gap, WebSearch + `fetch-and-queue` (≤3), `[fresh]`-labeled claims, queued web source(s) in `raw/_inbox/`, `query` entry in `_log.md`.
- **AE3 (web fails)** — uncovered topic where every fetch errors (e.g. only LinkedIn/x.com URLs): answer states the gap couldn't be auto-filled; gap logged; nothing fabricated or queued.
- **AE4 (file-back)** — a 2+-page derived answer: user offered a synthesis page; "yes" → page written + `_index.md`/`_log.md` updated; "no" → nothing written beyond the gap log.

---

## Risks & mitigations

- **Index-selection misses a relevant page (recall).** Mitigation: select generously (topic + `aliases`), read borderline candidates; recall-at-scale upgrade (vector index) is the named deferred follow-up, not silently assumed solved.
- **Query-driven intake grows the backlog** (origin Consequence). Mitigation: `via_query` tags queued sources so backlog-drain tracking can attribute query-channel intake; cap (3) bounds per-query growth.
- **Over-eager file-back clutters the corpus.** Mitigation: Decision-3 threshold + approval gate (R7); covered single-page lookups never offer.
- **Helper writing outside `raw/_inbox/` / corpus pages written without approval** — a §13 failure mode. Mitigation: helper's only corpus-side write is the append-only `_log.md`; all corpus *pages* are Claude-authored under the R7 approval gate; covered queries are write-free (R3).
- **Fabrication on fetch failure** (trust boundary). Mitigation: `fetch-and-queue` returns structured `error` and the skill's failure branch states the gap plainly (R8/R9); explicit AE3 test.

---

## Success criteria (from origin)

- A covered factual-recall question → answer with **zero uncited corpus claims** and no spurious web fetch.
- A gap question → **either** a logged gap + queued web source, **or** a clean "couldn't auto-fill" on fetch failure — never a fabricated answer.
- **Corpus-answered query rate** becomes measurable from `_log.md` `query` entries (covered vs. gap).
