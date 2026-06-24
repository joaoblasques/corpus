# X (Twitter) Bookmarks Collector — Design Spec

> Date: 2026-06-24
> Status: **design approved**; ready for implementation plan
> A new collection channel mirroring the youtube/github collectors. Substack is a separate,
> queued follow-up (its saved-list endpoint needs a user-side reverse-engineering spike).

## 1. Problem

The user bookmarks posts/articles on **X (Twitter)** as a save-for-later queue. Bring each
bookmark into the corpus, then **un-bookmark it once it is durably ingested** (`corpus_ingested`),
so the bookmark list stays a clean "still-to-process" queue.

## 2. Decisions (confirmed with user)

- **Source:** the user's **X bookmarks**.
- **Access:** official **X API v2**, OAuth2 user-context, pay-per-use (~$0.001/owned-read). Scopes:
  `bookmark.read` **+** `bookmark.write` (+ `tweet.read`, `users.read`, `offline.access`).
- **Lifecycle:** **remove-after-ingest** — `DELETE` the bookmark only after its source is
  `corpus_ingested: true` (gated, like the email un-label + Obsidian reaper). A bookmark leaves the
  list only once it is safely in the corpus.
- **Dedup:** by post id (frontmatter `tweet_id`).
- **Granularity:** one source doc per bookmarked post (text + long-form `note_tweet` + any linked
  external article), channel `x` → `raw/x`.
- **Files:** `bin/x_client.py` (API transport + CLI) + `bin/collect_x.py` (pure logic). Wired into
  the 2 AM job (collect leg + reap leg).

## 3. Scope

In: the collector, OAuth2 auth flow, collect, reap (un-bookmark), scheduled wiring, `_config.md`
docs, tests. Out: the X dev-app creation + first OAuth authorization (the **user** does this once);
thread/reply expansion beyond the bookmarked post; media file download (capture URLs only);
deleting/posting tweets; Substack (separate spec).

## 4. Design

### 4.1 Auth — `bin/x_client.py` (OAuth2 PKCE user-context)
The user one-time: creates an X developer app, enables OAuth2 (Native/public client), sets redirect
`http://127.0.0.1:8723/callback`, copies the **client_id** into `bin/x_app.json`
(`{"client_id": "...", "redirect_uri": "http://127.0.0.1:8723/callback"}` — no secret for a public
PKCE client). Then `python3 bin/x_client.py auth`:
- Generate `code_verifier` + `code_challenge` (S256); open
  `https://twitter.com/i/oauth2/authorize?response_type=code&client_id=…&redirect_uri=…&scope=tweet.read users.read bookmark.read bookmark.write offline.access&state=…&code_challenge=…&code_challenge_method=S256`.
- A short-lived local `http.server` on :8723 captures the `code`; exchange it at
  `https://api.twitter.com/2/oauth2/token` (grant_type=authorization_code, code_verifier, client_id,
  redirect_uri) → `access_token` + `refresh_token`; store in `bin/x_token.json` (gitignored).
- `_access_token()`: load `x_token.json`; if expired, refresh via
  `grant_type=refresh_token` (offline.access) and re-store. Returns `None` if no token.
- `x_available() -> bool`: `bin/x_token.json` exists and a token can be obtained.
- Mockable seam: all HTTP through an injectable `_session` (default `requests.Session()`).

### 4.2 `bin/x_client.py` — API
- `me(_session) -> str` — `GET /2/users/me` → the authed user id.
- `list_bookmarks(max_n=None, *, _session) -> list[dict]` —
  `GET /2/users/{id}/bookmarks?max_results=100&pagination_token=…` with
  `tweet.fields=created_at,note_tweet,entities,author_id`, `expansions=author_id`,
  `user.fields=username`. Each → `{id, url ("https://x.com/{username}/status/{id}"), text
  (note_tweet.text if present else text), author (username), created_at, links (entities.urls
  expanded_url, external only)}`. Honors `max_n`; paginates.
- `delete_bookmark(tweet_id, *, _session) -> bool` — `DELETE /2/users/{id}/bookmarks/{tweet_id}`,
  returns `data.bookmarked == false`.
- subparsers: `auth`, `me`, `list` (`--max`), `run` (collect), `reap` (`--dry-run`).

### 4.3 `bin/collect_x.py` — pure logic
- `DEDUP_DIRS = [raw/_inbox, raw/x]`; `slugify(tweet_id) -> "x-<id>"`.
- `already_collected(tweet_id, dirs=None) -> bool` — frontmatter `tweet_id: <id>` match.
- `build_document(post, *, collected_at) -> str` — frontmatter (`channel: x`, `source: x`,
  `tweet_id`, `url`, `author`, `created_at`, `links: [...]`, `collected_at`) + body (the post text /
  long-form, then each linked external article fetched via `fetch_link` — cap `MAX_LINKS=3`).
- `write_collected(post, *, collected_at, inbox=None, dedup_dirs=None) -> dict` — dedup → write
  `x-<id>.md` to `raw/_inbox`.
- `reapable(dedup_dirs=None) -> list[str]` — `tweet_id`s of channel-`x` raw sources with
  `corpus_ingested: true` (gates the un-bookmark on durable ingest).

### 4.4 `cmd_run` / `cmd_reap`
- `cmd_run`: `x_available` gate → `list_bookmarks(max)` → for each NOT `already_collected` →
  `fetch` links → `write_collected`. **No un-bookmark here.** JSON summary `{found, written,
  duplicate, failed}`.
- `cmd_reap`: `x_available` gate → for each `reapable()` tweet_id → `delete_bookmark` (un-bookmark);
  `--dry-run` counts only. JSON `{unbookmarked, dry_run}`. This is the only step that removes.

### 4.5 Scheduled wiring — `bin/scheduled_run.py`
- Add an **x collect leg** to `run_collectors` (`x_client.py run`); `_CHANNEL_DIR["x"] = "x"`.
- Add an **x reap step** after ingest (mirrors `run_email_relabel`): `x_client.py reap` —
  un-bookmarks the now-`corpus_ingested` posts. Counts surface in the summary (`x=N`, `x_reaped=N`).

### 4.6 Ingest
Drains via the normal nightly ingest (Branch-A): each X source → an entity/concept/source page,
§7-cited to the post + its linked article. No collector-side ingest logic.

## 5. Testing
- `collect_x`: `slugify`, `already_collected`/`write_collected` dedup by `tweet_id`, `build_document`
  frontmatter + body (mock `fetch_link`), `reapable` gates on `corpus_ingested` + channel `x`.
- `x_client`: `list_bookmarks` parses the API JSON (note_tweet vs text, username join, link extract,
  pagination), `delete_bookmark`, `me`, `x_available`, token refresh-on-expiry — all via mocked
  `_session`. `cmd_run` skips when unavailable, collects only new, never deletes; `cmd_reap`
  un-bookmarks only `reapable` ids; `--dry-run` writes/deletes nothing.
- `scheduled_run`: the x collect leg + reap step invoked; `_CHANNEL_DIR["x"]` set.
- All HTTP injected — no real X calls, no network in tests.

## 6. Risks & mitigations
| Risk | Mitigation |
|---|---|
| OAuth token expiry | `offline.access` refresh token; `_access_token` refreshes + re-stores; `auth` re-runs if refresh fails |
| Pay-per-use cost | Owned-reads ~$0.001 each; `--max` caps bookmarks/run; few new bookmarks/day |
| Un-bookmark is irreversible | Gated on `corpus_ingested: true` (durably in corpus first); `--dry-run`; reap is a separate step, never in collect |
| No X auth yet (user sets up) | `x_available` gate → leg reports `not configured`, run continues; unit tests mock all HTTP |
| Rate limits (429) | Honor `x-rate-limit-reset`; `--max`; back off, recorded not fatal |
| Bookmarked media-only post | Capture text (may be empty) + URL; ingest can defer low-content posts |

## 7. Decisions locked
1. Source = X bookmarks; access = X API v2 OAuth2 (bookmark.read+write); remove-after-ingest.
2. Dedup by `tweet_id`; channel `x` → `raw/x`; one doc per post (+ linked article via fetch_link).
3. Un-bookmark gated on `corpus_ingested`, as a separate reap step (collect never deletes).
4. `bin/x_client.py` + `bin/collect_x.py`; injectable `_session`; wired into the 2 AM job.
5. User does the one-time X dev-app + OAuth authorization; the collector handles refresh.
