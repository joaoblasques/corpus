# Open-source migration runbook — make `corpus` public, serve at `joaoblasques.com/corpus/`

> Prepared 2026-07-14. **Do NOT execute until the repo is quiet** (concurrent website-redesign
> session finished, cloud nightly paused, no other sessions writing `main`). A history rewrite +
> force-push invalidates every existing clone. Read fully before running.

## Goal

Open-source the private `joaoblasques/corpus` repo (code + `corpus/` knowledge) and serve the docs
site from it directly at `joaoblasques.com/corpus/`, retiring the separate public `corpus-docs`
deploy repo. Eliminates the repo-name conflict (the URL path *is* the Pages repo name).

## Why a history scrub is required first

`raw/` is gitignored today, but **73 `raw/email/*.md` files were committed early in history** (later
removed from the tree). Flipping the repo public exposes all history, so those must be purged first.
Confirmed scope (2026-07-14): only `raw/email` (73) is personal; `raw/proposals` (10, test fixtures)
must be KEPT. Deep secret sweep of history: **0 hits** (no keys/tokens/PEM ever committed).

## Preconditions (all must hold before Step 1)

- [ ] Concurrent website-redesign session finished; its `extra.css`/`graph.js` work committed.
- [ ] Cloud nightly + local launchd jobs (`com.corpus.daily`, `com.corpus.weekly-synthesis`) paused
      or timed to not fire during the migration (they clone/pull `main`).
- [ ] No other Claude session writing this repo.
- [ ] You accept the 1,461 `corpus/` knowledge pages becoming public (this is the intent of an open
      LLM-wiki, but confirm — it's your curated reading/synthesis).

## Step 1 — Full backup (safety net)

```bash
git clone --mirror https://github.com/joaoblasques/corpus.git ~/corpus-backup-premigration.git
```
Keep this until the migration is verified good. It is the only rollback for the history rewrite.

## Step 2 — Scrub `raw/email` from all history (surgical)

Run on a FRESH clone (filter-repo strips the remote by design):
```bash
git clone https://github.com/joaoblasques/corpus.git ~/corpus-scrub && cd ~/corpus-scrub
git filter-repo --invert-paths --path-glob 'raw/email/*.md'
# verify the 73 files are gone from history and nothing else changed:
git log --all --diff-filter=A --name-only --pretty=format: -- 'raw/email/*.md' | grep -v '^$' | wc -l   # expect 0
git log --all --diff-filter=A --name-only --pretty=format: -- 'raw/proposals/*' | grep -v '^$' | wc -l  # expect 10 (kept)
```

## Step 3 — Force-push the rewritten history

```bash
cd ~/corpus-scrub
git remote add origin https://github.com/joaoblasques/corpus.git
git push --force --all origin
git push --force --tags origin
```
**After this, every other clone is invalid.** Re-clone on the Mac working copy, and re-provision the
cloud nightly environment + any launchd job checkouts (they must re-clone, not pull).

## Step 4 — (YOU) Flip the repo to public

GitHub → `joaoblasques/corpus` → Settings → General → Danger Zone → **Change visibility → Public**.
(Claude cannot change repo sharing settings — this is yours to do.)

## Step 5 — (YOU) Enable GitHub Pages on `corpus`

Settings → Pages → Build and deployment. Either:
- **Source: GitHub Actions** (preferred — the deploy workflow can publish directly), or
- **Source: Deploy from branch → `gh-pages` / `/`** (if keeping the branch-push model).
Then set the custom domain to reuse your apex (`joaoblasques.com`) so the project serves at
`joaoblasques.com/corpus/`.

## Step 6 — (CLAUDE) Rewire the deploy + site URL

Once the repo is public and Pages is on, these one-line edits land (I'll do them then):
- `.github/workflows/docs.yml` line 42 → push `gh-pages` to **origin** (`joaoblasques/corpus`) instead
  of `corpus-docs`; the in-repo `GITHUB_TOKEN` suffices (no more cross-repo `DOCS_DEPLOY_TOKEN`).
- `website/mkdocs.yml` `site_url` → `https://joaoblasques.com/corpus/`.
- Workflow notice line → the new URL.

## Step 7 — Retire `corpus-docs`

Archive the `joaoblasques/corpus-docs` repo (or leave it as a redirect stub). Update any external
links pointing at `/corpus-docs/`.

## Rollback

Before Step 4 (visibility flip): `git push --force --all` from `~/corpus-backup-premigration.git`
restores the original history; the repo is still private, no exposure occurred. After Step 4, the
scrub already guarantees no sensitive content is public, so rollback is only about history shape.
