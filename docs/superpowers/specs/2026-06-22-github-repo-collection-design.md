# GitHub Repo Collection — Design Spec

> Date: 2026-06-22
> Status: **design approved**; ready for implementation plan
> A new collection channel mirroring the email/youtube/pdf/obsidian collectors.

## 1. Problem

GitHub repos currently reach the corpus only as incidental **web-clips** — a one-page HTML
snapshot of a repo's README captured when a link appears in an email/clip (109 such sources
exist). There's no first-class way to collect a repo the user actually cares about. The user
**stars** repos on GitHub as a curated signal; those should become proper corpus sources:
the README + docs + a metadata overview, ingested like everything else.

## 2. Decisions (confirmed with user)

- **Trigger:** the user's **starred** repos (mirrors the starred-email flow).
- **Depth:** **README + markdown docs + an overview** (description, topics, primary language,
  star count, latest release). **No raw source code.**
- **Lifecycle:** **leave the star in place** (it's a bookmark, not a queue). Dedup by repo
  full-name prevents re-collection.
- **Granularity:** **one source document per repo** (a "repo digest" — README + docs +
  overview together), filed to a new `github` channel.
- **Snapshot once** for v1. (Re-collect-on-update is a noted future add-on, not built now.)
- **Auth:** the `gh` CLI (already authenticated). No token handling.

## 3. Scope

In: `bin/collect_github.py` (pure logic), `bin/github_client.py` (CLI driver using `gh`),
wiring into `bin/scheduled_run.py` (a new collector leg + `github` → `raw/github` channel
dir), `corpus/_config.md` docs, tests.
Out: un-starring; re-collect-on-update; collecting source code; private-repo-only modes
(works on whatever the authed `gh` user can see); a per-repo routing-to-domain scheme
(routing stays with the normal ingest).

## 4. Design

### 4.1 `bin/github_client.py` — CLI driver (network via `gh`)
All GitHub I/O is `gh` subprocess calls (injectable `_run` seam), so tests need no network.

- `gh_available(_run) -> bool` — `gh auth status` succeeds; else the collector reports
  `not configured` and is skipped (like the youtube token check).
- `list_starred(max_n=None, _run) -> list[dict]` — `gh api user/starred --paginate`
  (JSON array). Each item → `{full_name, html_url, description, language, stargazers_count,
  topics, default_branch}`. Honors `max_n`.
- `fetch_repo(full_name, *, max_docs=8, _run) -> dict` — gather, with per-piece failures
  tolerated (a missing piece is omitted, never fatal):
  - **README:** `gh api repos/{full_name}/readme` → base64 `content`, decode. Truncate to
    ~40 KB.
  - **Metadata:** from the starred-list item (already have description/language/topics/stars)
    + **latest release:** `gh api repos/{full_name}/releases/latest` → `tag_name` (404 → none).
  - **Docs:** `gh api repos/{full_name}/contents` (root) → top-level `*.md` except the README
    (CONTRIBUTING, ARCHITECTURE, ROADMAP, etc.); plus `gh api repos/{full_name}/contents/docs`
    (404 → none) → its `*.md`. Take up to `max_docs`, fetch each via its `content`/`download_url`,
    truncate each to ~15 KB.
  - Returns `{full_name, html_url, description, language, stars, topics, latest_release,
    readme, docs:[{path, text}]}`.
- `cmd_run(args)` — `gh_available` gate → `list_starred(args.max)` → for each repo NOT
  `cg.already_collected(full_name)` (cg = the collect_github module): `fetch_repo` → `cg.write_collected(...)` (writes to
  `raw/_inbox`). **No un-star.** Prints a JSON summary `{found, written, duplicate, failed,
  skipped_unavailable}`. `--dry-run` lists candidate new repos without fetching/writing.
- subparsers: `auth` (print `gh auth status`), `list-starred`, `run` (`--max`, `--dry-run`,
  `--max-docs`, `--collected-at`).

### 4.2 `bin/collect_github.py` — pure logic
- `DEDUP_DIRS = [raw/_inbox, raw/github]`.
- `slugify(full_name) -> str` — `owner/name` → `github-owner-name`.
- `already_collected(full_name, dirs=None) -> bool` — grep `^repo:\s*<full_name>$` in the
  frontmatter of `DEDUP_DIRS/*.md`. (Reuse the established dedup pattern.)
- `build_document(repo: dict, *, collected_at) -> str` — one markdown source:
  ```
  ---
  channel: github
  source: github
  repo: owner/name
  repo_url: https://github.com/owner/name
  description: <desc>
  language: <lang>
  stars: <int>
  topics: [a, b, c]
  latest_release: <tag or "">
  collected_at: YYYY-MM-DD
  ---

  # owner/name
  > <description> · <language> · ★<stars> · latest <tag> · topics: a, b, c

  ## README
  <readme text>

  ## Docs
  ### <path>
  <text>
  ...
  ```
- `write_collected(repo, collected_at, inbox=None, dedup_dirs=None) -> dict` — dedup via
  `already_collected(repo["full_name"])`; if new, write `slugify(full_name).md` to `raw/_inbox`
  via `build_document`; returns `{status: "written"|"duplicate"|..., path}`.

### 4.3 Scheduled wiring — `bin/scheduled_run.py`
- Add a **github leg** to `run_collectors` (after pdf/youtube): `github_client.py run`,
  per-channel isolation like the others (failure recorded, never aborts the run). Counts
  surface in the run summary + commit message (`github=N`).
- Add `"github": "github"` to `_CHANNEL_DIR` so ingested github sources move `raw/_inbox` →
  `raw/github`.

### 4.4 Ingest
Drains via the normal nightly ingest (Branch-A `/ingest-auto`): each repo digest → a corpus
entity page (or enriches an existing one), §7-cited to the README/docs. The repo's
topics/description guide routing. No collector-side ingest logic.

## 5. Testing
- `gh_available`: success/failure of `gh auth status` (mock `_run`).
- `list_starred`: parses the `gh api user/starred` JSON; honors `max_n`.
- `fetch_repo`: assembles readme+docs+metadata; a 404 on release/docs is omitted not fatal;
  README base64 decoded; truncation caps applied (mock `_run` per endpoint).
- `build_document`: emits the frontmatter (incl. `repo:` dedup key) + README/Docs sections.
- `already_collected` / `write_collected`: dedup by `repo:` full-name; writes new, skips dup.
- `cmd_run`: skips when `gh` unavailable; collects only NOT-already-collected repos; never
  un-stars (no `PUT user/starred` / `DELETE` call); `--dry-run` writes nothing.
- `scheduled_run`: the github leg is invoked in `run_collectors`; `_CHANNEL_DIR["github"]` set.
- All `gh`/subprocess effects injected — no network, no git, no real `gh`.

## 6. Risks & mitigations
| Risk | Mitigation |
|---|---|
| `gh` not authed on the unattended run | `gh_available` gate → leg reports `not configured`, run continues |
| GitHub API rate limit | Authed `gh` = 5000/hr; `--max` caps repos/run; few new stars/night |
| Huge README/docs bloat a source | Truncate README ~40 KB, each doc ~15 KB, `max_docs` cap |
| Re-collecting an already-collected repo | `already_collected` dedup by `repo:` full-name (leave-starred is safe) |
| A repo piece missing (no docs/release) | Per-piece try/except → omit, never fail the whole repo |
| Private/secret repo content leaking to a public corpus remote | The corpus repo is the user's own; collects only what the authed `gh` user chose to star |

## 7. Decisions locked
1. Trigger = starred repos; leave starred; dedup by `repo:` full-name.
2. Depth = README + markdown docs + metadata overview; no source code.
3. One source doc per repo (`github` channel → `raw/github`).
4. `gh` CLI auth; injectable subprocess seam; snapshot-once.
