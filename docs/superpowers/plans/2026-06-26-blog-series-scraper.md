# Blog / Series Deep-Scraper Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deep-scrape tagged blog/series URLs in the vault's `TO SCRAPE.md` — all posts of a blog (sitemap/RSS) or all parts of a series (index page) — into per-post corpus sources, striking the seed only once every post is ingested.

**Architecture:** Extend the existing Obsidian url-list flow. A per-line tag (`[blog]`/`[blog:N]`/`[series]`) routes to a new `bin/scrape_blog.py` (post discovery + per-post fetch/write, all HTTP injected); untagged lines keep today's single-page fetch. Per-post raw sources carry `scrape_seed: <seed>`; the seed is struck only when all its posts are `corpus_ingested`. The Obsidian reaper (which performs the strike) is wired into the nightly run for the first time.

**Tech Stack:** Python 3.12, stdlib `xml.etree.ElementTree` + `urllib.parse`, `httpx` (via `fetch_link._client`), `pytest`. No new dependencies.

## Global Constraints

- All HTTP in `scrape_blog.py` goes through an injectable seam (`_session` for sitemap/feed/index GETs, `_fetch` for per-post content) — **tests never hit the network.** (spec §4.2, §5)
- Per-post raw source: channel `web`, written to `raw/_inbox/`, frontmatter carries `source_url: <post>` and `scrape_seed: <seed>`. **Dedup by `source_url`** (reuse `collect_obsidian.url_already_collected`). (spec §2, §4.2)
- `[blog]` cap default **200**, raisable via `[blog:N]`; scraping pages over runs when more posts than the cap remain. (spec §2)
- Strike the seed URL from `TO SCRAPE.md` **only when every `scrape_seed: <seed>` source is `corpus_ingested: true` AND the seed produced ≥1 source.** (spec §2, §4.3)
- Untagged URL behaviour is **unchanged** (existing single-page path). (spec §2, §4.1)
- Out of scope: JS-only blogs with no sitemap/RSS (log `scraped: 0`, keep seed); media download; perfect series detection. (spec §3)
- Reuse established helpers — do not duplicate: `collect_email.slugify`, `collect_email.yaml_scalar`, `collect_email.URL_RE`, `collect_obsidian.url_already_collected`, `collect_obsidian.url_filename`, `collect_obsidian.build_url_source`, `fetch_link.fetch`, `fetch_link._client`. (DRY)

**Repo facts the implementer needs:**
- `bin/collect_obsidian.py` — pure functions (parsing, dedup, `discover`, `reapable`). Imports `from collect_email import slugify, yaml_scalar, URL_RE`. `INBOX = ROOT/"raw"/"_inbox"`. `DEDUP_DIRS = [raw/_inbox, raw/notes, raw/web]`.
- `bin/obsidian_client.py` — I/O + CLI (`collect`, `reap`). `fetch_url(url)` wraps `fetch_link.fetch` returning `{}` on failure. `cmd_collect` writes sources; `cmd_reap` calls `co.reapable()` then `_strike_url`.
- `fetch_link.fetch(url) -> {"title","text","channel"}` (raises on unsupported/failed). `fetch_link._client()` returns a configured `httpx.Client`.
- `collect_obsidian.url_already_collected(url, dirs=None)` → True if any raw source has `source_url: <url>\n`.
- `collect_obsidian.url_filename(url, title, base=None)` → `<base>/web-<slug>.md` (base defaults to `INBOX`).
- `collect_obsidian.build_url_source(meta, body)` builds the channel-`web` frontmatter; today it requires `source_url` + one of `via_vault_note`/`via_vault_list`.
- `bin/scheduled_run.py` post-ingest reap phase (~line 960-972) calls `run_email_relabel()` then `run_x_reap()`; `build_summary` (~line 495) surfaces their tallies. **No obsidian reap is called there.**
- Test files: `tests/test_collect_obsidian.py`, `tests/test_obsidian_client.py`, `tests/test_scheduled_run.py` (mirror their existing styles).

Run tests with `python3 -m pytest <path> -o addopts="" -q` (the repo's default addopts can slow collection; `-o addopts=""` keeps it fast). **Do not** run the whole suite per task — `tests/test_scheduled_run.py` has slow lock-integration tests; run only the files you touch.

---

## File Structure

- **`bin/collect_obsidian.py`** (modify) — add `parse_scrape_tag`, `iter_scrape_targets`; extend `build_url_source` (optional `scrape_seed`); extend `reapable` (emit `seed_strikes`).
- **`bin/scrape_blog.py`** (create) — `discover_blog_posts`, `discover_series_parts`, `scrape_seed`, `write_post`, `_post_collected`, `_http_get`, helpers.
- **`bin/obsidian_client.py`** (modify) — route tagged url-list lines to `scrape_blog.scrape_seed`; emit `scraped` count; strike `seed_strikes` in `cmd_reap`.
- **`bin/scheduled_run.py`** (modify) — `run_obsidian_reap()` + call it post-ingest + surface in `build_summary`.
- **`docs/solutions/`** (create one note) — document the `[blog]`/`[blog:N]`/`[series]` TO-SCRAPE syntax (NOT `corpus/_config.md`; see Task 6 note).
- Tests in `tests/test_collect_obsidian.py`, `tests/test_scrape_blog.py` (new), `tests/test_obsidian_client.py`, `tests/test_scheduled_run.py`.

---

## Task 1: Tag parsing — `parse_scrape_tag` + `iter_scrape_targets`

**Files:**
- Modify: `bin/collect_obsidian.py` (add after `parse_url_list`, ~line 61)
- Test: `tests/test_collect_obsidian.py`

**Interfaces:**
- Produces: `parse_scrape_tag(line: str) -> {"url": str, "mode": None|"blog"|"series", "cap": int}`; `iter_scrape_targets(text: str) -> list[dict]` (one dict per line that has a URL, order-preserved, deduped by url, first occurrence wins). `DEFAULT_BLOG_CAP = 200`.

- [ ] **Step 1: Write the failing tests**

In `tests/test_collect_obsidian.py` (it already does `import collect_obsidian as co` via the `bin` path shim — match the file's existing import style):

```python
def test_parse_scrape_tag_blog_series_and_untagged():
    assert co.parse_scrape_tag("https://blog.example.com [blog]") == {
        "url": "https://blog.example.com", "mode": "blog", "cap": 200}
    assert co.parse_scrape_tag("https://blog.example.com [blog:50]") == {
        "url": "https://blog.example.com", "mode": "blog", "cap": 50}
    assert co.parse_scrape_tag("- https://site.com/the-series  [series]") == {
        "url": "https://site.com/the-series", "mode": "series", "cap": 200}
    assert co.parse_scrape_tag("https://plain.example.com/post") == {
        "url": "https://plain.example.com/post", "mode": None, "cap": 200}
    assert co.parse_scrape_tag("no url here [blog]")["url"] == ""

def test_iter_scrape_targets_dedups_and_preserves_order():
    text = ("https://a.com [blog]\n"
            "- https://b.com/series [series]\n"
            "https://c.com/post\n"
            "https://a.com [blog:5]\n")   # dup url, first tag wins
    out = co.iter_scrape_targets(text)
    assert [t["url"] for t in out] == ["https://a.com", "https://b.com/series", "https://c.com/post"]
    assert out[0] == {"url": "https://a.com", "mode": "blog", "cap": 200}
    assert out[1]["mode"] == "series"
    assert out[2]["mode"] is None
```

- [ ] **Step 2: Run to verify they fail**

Run: `python3 -m pytest tests/test_collect_obsidian.py -k "scrape_tag or scrape_targets" -o addopts="" -q`
Expected: FAIL with `AttributeError: module 'collect_obsidian' has no attribute 'parse_scrape_tag'`.

- [ ] **Step 3: Implement**

In `bin/collect_obsidian.py`, after `parse_url_list` (line 61), add:

```python
DEFAULT_BLOG_CAP = 200
SCRAPE_TAG_RE = re.compile(r"\[(blog|series)(?::(\d+))?\]\s*$")


def parse_scrape_tag(line: str) -> dict:
    """Parse a url-list line's optional trailing scrape tag.

    `<url> [blog]` / `<url> [blog:N]` / `<url> [series]`. Returns
    {url, mode, cap}: mode in {None, 'blog', 'series'} (None = untagged, the
    existing single-page path); cap is the [blog:N] number or DEFAULT_BLOG_CAP.
    url is '' when the line has no http(s) URL.
    """
    s = (line or "").strip()
    mode, cap = None, DEFAULT_BLOG_CAP
    m = SCRAPE_TAG_RE.search(s)
    if m:
        mode = m.group(1)
        if m.group(2):
            cap = int(m.group(2))
        s = s[:m.start()].strip()
    um = URL_RE.search(s)
    url = um.group(0).rstrip(".,)") if um else ""
    return {"url": url, "mode": mode, "cap": cap}


def iter_scrape_targets(text: str) -> list:
    """Per-line {url, mode, cap} for every url-list line that holds a URL,
    order-preserved and deduped by url (first occurrence's tag wins)."""
    seen, out = set(), []
    for line in (text or "").splitlines():
        tgt = parse_scrape_tag(line)
        if tgt["url"] and tgt["url"] not in seen:
            seen.add(tgt["url"])
            out.append(tgt)
    return out
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_collect_obsidian.py -k "scrape_tag or scrape_targets" -o addopts="" -q`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
git add bin/collect_obsidian.py tests/test_collect_obsidian.py
git commit -m "feat(obsidian): parse [blog]/[blog:N]/[series] tags in TO SCRAPE lines"
```

---

## Task 2: Blog & series discovery — `bin/scrape_blog.py`

**Files:**
- Create: `bin/scrape_blog.py`
- Test: `tests/test_scrape_blog.py` (new)

**Interfaces:**
- Consumes: nothing from earlier tasks (pure discovery).
- Produces:
  - `_http_get(url, _session=None) -> str` (response text or `""`; `_session` is a `url->str` callable seam).
  - `discover_blog_posts(seed_url, cap=200, *, _session=None) -> list[str]` (post URLs; sitemap-first, sitemap-index aware, RSS/Atom fallback; filters non-posts; deduped; truncated to `cap`).
  - `discover_series_parts(index_url, *, _session=None) -> list[str]` (same-path-prefix `<a href>` links, absolute, order-preserved, deduped, excludes the index itself).
  - `DEFAULT_CAP = 200`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_scrape_blog.py`:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import scrape_blog as sb  # noqa: E402

SITEMAP = """<?xml version="1.0"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://blog.example.com/post-one</loc></url>
  <url><loc>https://blog.example.com/post-two</loc></url>
  <url><loc>https://blog.example.com/tag/python</loc></url>
  <url><loc>https://blog.example.com/author/jane</loc></url>
  <url><loc>https://blog.example.com/</loc></url>
</urlset>"""

SITEMAP_INDEX = """<?xml version="1.0"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://blog.example.com/sitemap-posts.xml</loc></sitemap>
</sitemapindex>"""

RSS = """<?xml version="1.0"?>
<rss version="2.0"><channel>
  <item><link>https://blog.example.com/rss-post-a</link></item>
  <item><link>https://blog.example.com/rss-post-b</link></item>
</channel></rss>"""


def test_discover_blog_posts_from_sitemap_filters_nonposts():
    def session(url):
        return SITEMAP if url == "https://blog.example.com/sitemap.xml" else ""
    out = sb.discover_blog_posts("https://blog.example.com", _session=session)
    assert out == ["https://blog.example.com/post-one", "https://blog.example.com/post-two"]


def test_discover_blog_posts_follows_sitemap_index():
    pages = {
        "https://blog.example.com/sitemap.xml": SITEMAP_INDEX,
        "https://blog.example.com/sitemap-posts.xml": SITEMAP,
    }
    out = sb.discover_blog_posts("https://blog.example.com", _session=lambda u: pages.get(u, ""))
    assert "https://blog.example.com/post-one" in out and "https://blog.example.com/tag/python" not in out


def test_discover_blog_posts_caps():
    def session(url):
        return SITEMAP if url.endswith("/sitemap.xml") else ""
    assert len(sb.discover_blog_posts("https://blog.example.com", cap=1, _session=session)) == 1


def test_discover_blog_posts_rss_fallback_when_no_sitemap():
    def session(url):
        if url.endswith("/sitemap.xml"):
            return ""                       # no sitemap
        if url == "https://blog.example.com":
            return '<html><head></head><body>hi</body></html>'  # no <link> feed hint
        if url == "https://blog.example.com/feed":
            return RSS
        return ""
    out = sb.discover_blog_posts("https://blog.example.com", _session=session)
    assert out == ["https://blog.example.com/rss-post-a", "https://blog.example.com/rss-post-b"]


def test_discover_series_parts_same_path_prefix_in_order():
    index = "https://site.com/guide/intro"
    html = ('<a href="https://site.com/guide/part-1">1</a>'
            '<a href="/guide/part-2">2</a>'
            '<a href="https://other.com/guide/x">no</a>'      # different host
            '<a href="https://site.com/about">no</a>'         # outside prefix
            '<a href="https://site.com/guide/part-1#top">dup</a>')
    out = sb.discover_series_parts(index, _session=lambda u: html)
    assert out == ["https://site.com/guide/part-1", "https://site.com/guide/part-2"]
```

- [ ] **Step 2: Run to verify they fail**

Run: `python3 -m pytest tests/test_scrape_blog.py -o addopts="" -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'scrape_blog'`.

- [ ] **Step 3: Implement `bin/scrape_blog.py` (discovery half)**

Create `bin/scrape_blog.py`:

```python
#!/usr/bin/env python3
"""scrape_blog.py — deep-scrape a blog (sitemap/RSS) or a series (index page)
into per-post raw sources.

All HTTP goes through injectable seams: `_session(url)->str` for sitemap/feed/
index GETs, `_fetch(url)->dict` for per-post content. Tests pass these and never
touch the network. Discovery is heuristic (spec §4.2): sitemap-first with an
RSS/Atom fallback for blogs; same-path `<a href>` links for series.
"""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urljoin, urlparse

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
INBOX = ROOT / "raw" / "_inbox"
sys.path.insert(0, str(BIN))
import collect_obsidian as co  # noqa: E402
import fetch_link as fl        # noqa: E402

DEFAULT_CAP = 200
HTTP_MAX_BYTES = 5_000_000
NON_POST_RE = re.compile(r"(?i)/(tag|tags|category|categories|author|authors|page|about|search|feed)(/|$|\?)")
FEED_PATHS = ("/feed", "/rss.xml", "/atom.xml", "/index.xml")


def _http_get(url: str, _session=None) -> str:
    """GET `url`, return body text (capped) or '' on any failure.
    `_session` (a url->str callable) overrides the real client in tests."""
    if _session is not None:
        try:
            return _session(url) or ""
        except Exception:  # noqa: BLE001
            return ""
    try:
        c = fl._client()
        try:
            r = c.get(url)
            r.raise_for_status()
            return r.text[:HTTP_MAX_BYTES]
        finally:
            c.close()
    except Exception:  # noqa: BLE001
        return ""


def _origin(url: str) -> str:
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc}"


def _is_post_url(u: str) -> bool:
    if not u or NON_POST_RE.search(u):
        return False
    p = urlparse(u)
    return p.scheme.startswith("http") and p.path not in ("", "/")


def _sitemap_locs(xml_text: str) -> list:
    """All <loc> texts in a sitemap/sitemap-index; [] on parse failure."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []
    out = []
    for el in root.iter():
        if el.tag.split("}")[-1] == "loc" and el.text:
            out.append(el.text.strip())
    return out


def _feed_links(xml_text: str) -> list:
    """Post URLs from an RSS (<item><link>text</link>) or Atom
    (<entry><link href=...>) feed; [] on parse failure."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []
    out = []
    for el in root.iter():
        if el.tag.split("}")[-1].lower() != "link":
            continue
        href = el.get("href")
        if href:
            out.append(href.strip())
        elif el.text and el.text.strip().lower().startswith("http"):
            out.append(el.text.strip())
    return out


def discover_blog_posts(seed_url: str, cap: int = DEFAULT_CAP, *, _session=None) -> list:
    origin = _origin(seed_url)
    posts, seen = [], set()

    def _add(urls):
        for u in urls:
            if _is_post_url(u) and u not in seen:
                seen.add(u)
                posts.append(u)
                if len(posts) >= cap:
                    return True
        return False

    sm = _http_get(urljoin(origin, "/sitemap.xml"), _session)
    if sm:
        if "<sitemapindex" in sm.lower():
            for child in _sitemap_locs(sm)[:50]:
                if _add(_sitemap_locs(_http_get(child, _session))):
                    return posts
        else:
            if _add(_sitemap_locs(sm)):
                return posts
    if posts:
        return posts

    # RSS/Atom fallback: feed hint in the seed page, then well-known paths.
    page = _http_get(seed_url, _session)
    m = re.search(
        r'<link[^>]+type=["\']application/(?:rss|atom)\+xml["\'][^>]*href=["\']([^"\']+)["\']',
        page or "", re.I)
    candidates = ([urljoin(seed_url, m.group(1))] if m else []) + [urljoin(origin, p) for p in FEED_PATHS]
    for fu in candidates:
        feed = _http_get(fu, _session)
        if feed and ("<rss" in feed.lower() or "<feed" in feed.lower()):
            _add(_feed_links(feed))
            break
    return posts


def discover_series_parts(index_url: str, *, _session=None) -> list:
    page = _http_get(index_url, _session)
    if not page:
        return []
    base = urlparse(index_url)
    prefix = base.path.rsplit("/", 1)[0] + "/"
    out, seen = [], set()
    for m in re.finditer(r'<a[^>]+href=["\']([^"\']+)["\']', page, re.I):
        absu = urljoin(index_url, m.group(1)).split("#", 1)[0]
        p = urlparse(absu)
        if p.netloc != base.netloc or not p.path.startswith(prefix):
            continue
        if absu == index_url or absu in seen:
            continue
        seen.add(absu)
        out.append(absu)
    return out
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_scrape_blog.py -o addopts="" -q`
Expected: PASS (5 passed).

- [ ] **Step 5: Commit**

```bash
git add bin/scrape_blog.py tests/test_scrape_blog.py
git commit -m "feat(scrape-blog): sitemap/RSS blog enumeration + series-index discovery"
```

---

## Task 3: Per-post fetch + write + dedup — `scrape_seed`

**Files:**
- Modify: `bin/collect_obsidian.py` (extend `build_url_source`, ~line 138)
- Modify: `bin/scrape_blog.py` (add `_post_collected`, `write_post`, `scrape_seed`)
- Test: `tests/test_scrape_blog.py`, `tests/test_collect_obsidian.py`

**Interfaces:**
- Consumes: `discover_blog_posts`, `discover_series_parts` (Task 2); `collect_obsidian.url_already_collected`, `collect_obsidian.url_filename`, `collect_obsidian.build_url_source` (now accepts optional `scrape_seed`).
- Produces: `scrape_seed(seed, mode, cap=200, *, collected_at, via_vault_list, inbox=None, dedup_dirs=None, _session=None, _fetch=None) -> {"seed","mode","found","written","duplicate","failed","capped"}`; `write_post(seed, url, content, collected_at, *, via_vault_list, inbox=None) -> Path`; `_post_collected(url, dirs=None) -> bool`.

- [ ] **Step 1: Write the failing tests**

In `tests/test_collect_obsidian.py`:

```python
def test_build_url_source_includes_scrape_seed_when_present():
    out = co.build_url_source({
        "source_url": "https://b.com/p1", "via_vault_list": "00_Inbox/Clippings/TO SCRAPE.md",
        "scrape_seed": "https://b.com", "title": "P1", "collected_at": "2026-06-26"}, "body")
    assert "scrape_seed: https://b.com\n" in out
    assert "source_url: https://b.com/p1\n" in out
    assert "via_vault_list: 00_Inbox/Clippings/TO SCRAPE.md\n" in out

def test_build_url_source_omits_scrape_seed_when_absent():
    out = co.build_url_source({
        "source_url": "https://b.com/p1", "via_vault_list": "L", "collected_at": "2026-06-26"}, "body")
    assert "scrape_seed" not in out
```

In `tests/test_scrape_blog.py`:

```python
def test_scrape_seed_writes_one_source_per_new_post(tmp_path):
    posts = ["https://b.com/p1", "https://b.com/p2"]
    seen = {"https://b.com/p1"}   # p1 already collected -> dedup
    monkey = {"posts": posts}
    def fake_fetch(url):
        return {"title": "T-" + url[-2:], "text": "content of " + url}
    res = sb.scrape_seed(
        "https://b.com", "blog", collected_at="2026-06-26",
        via_vault_list="00_Inbox/Clippings/TO SCRAPE.md", inbox=tmp_path,
        _session=lambda u: "", _fetch=fake_fetch,
        # discovery is stubbed via _session returning the sitemap below
    )
    # see Step 3 note: this test drives discovery through _session; simpler form below
```

Replace the sketch above with this concrete, self-contained test (discovery stubbed by a sitemap through `_session`, dedup by writing a pre-existing source into `inbox`, fetch stubbed):

```python
def test_scrape_seed_writes_dedups_and_counts(tmp_path):
    sitemap = ('<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
               '<url><loc>https://b.com/p1</loc></url>'
               '<url><loc>https://b.com/p2</loc></url></urlset>')
    # p1 already collected: drop a raw source with its source_url into the dedup dir
    (tmp_path / "web-existing.md").write_text(
        "---\nchannel: web\nsource_url: https://b.com/p1\n---\nold\n", encoding="utf-8")

    def session(url):
        return sitemap if url.endswith("/sitemap.xml") else ""

    def fake_fetch(url):
        return {"title": "Title " + url[-2:], "text": "body of " + url}

    res = sb.scrape_seed(
        "https://b.com", "blog", collected_at="2026-06-26",
        via_vault_list="00_Inbox/Clippings/TO SCRAPE.md",
        inbox=tmp_path, dedup_dirs=[tmp_path],
        _session=session, _fetch=fake_fetch)

    assert res == {"seed": "https://b.com", "mode": "blog", "found": 2,
                   "written": 1, "duplicate": 1, "failed": 0, "capped": False}
    written = [p for p in tmp_path.glob("web-*.md") if "existing" not in p.name]
    assert len(written) == 1
    txt = written[0].read_text(encoding="utf-8")
    assert "scrape_seed: https://b.com\n" in txt and "source_url: https://b.com/p2\n" in txt


def test_scrape_seed_counts_fetch_failures(tmp_path):
    sitemap = ('<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
               '<url><loc>https://b.com/p1</loc></url></urlset>')
    res = sb.scrape_seed(
        "https://b.com", "blog", collected_at="2026-06-26",
        via_vault_list="L", inbox=tmp_path, dedup_dirs=[tmp_path],
        _session=lambda u: sitemap if u.endswith("/sitemap.xml") else "",
        _fetch=lambda u: {})   # empty -> failed
    assert res["failed"] == 1 and res["written"] == 0
```

- [ ] **Step 2: Run to verify they fail**

Run: `python3 -m pytest tests/test_scrape_blog.py tests/test_collect_obsidian.py -k "scrape_seed or build_url_source" -o addopts="" -q`
Expected: FAIL (`AttributeError: ... 'scrape_seed'` / scrape_seed assertion on `build_url_source`).

- [ ] **Step 3: Implement**

First, extend `build_url_source` in `bin/collect_obsidian.py`. Replace the current body (lines 138-151) with:

```python
def build_url_source(meta: dict, body: str) -> str:
    lines = [
        "---", "channel: web", "source: obsidian-list",
        f"source_url: {meta['source_url']}",
    ]
    if meta.get("via_vault_note"):
        lines.append(f"via_vault_note: {meta['via_vault_note']}")
    else:
        lines.append(f"via_vault_list: {meta['via_vault_list']}")
    if meta.get("scrape_seed"):
        lines.append(f"scrape_seed: {meta['scrape_seed']}")
    lines += [
        f"title: {yaml_scalar(meta.get('title', ''))}",
        f"collected_at: {meta['collected_at']}", "---", "", body.strip(), "",
    ]
    return "\n".join(lines)
```

Then add to `bin/scrape_blog.py` (after `discover_series_parts`):

```python
def _post_collected(url: str, dirs=None) -> bool:
    return co.url_already_collected(url, dirs)


def write_post(seed: str, url: str, content: dict, collected_at: str,
               *, via_vault_list: str, inbox=None) -> Path:
    """Write one per-post raw source (channel web) tagged with scrape_seed."""
    base = inbox if inbox is not None else INBOX
    path = co.url_filename(url, content.get("title", ""), base=base)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(co.build_url_source(
        {"source_url": url, "via_vault_list": via_vault_list, "scrape_seed": seed,
         "title": content.get("title", ""), "collected_at": collected_at},
        content["text"]), encoding="utf-8")
    return path


def scrape_seed(seed: str, mode: str, cap: int = DEFAULT_CAP, *, collected_at: str,
                via_vault_list: str, inbox=None, dedup_dirs=None,
                _session=None, _fetch=None) -> dict:
    """Discover a seed's posts (blog or series), fetch+write each new one.

    Dedup by source_url (skip already-collected). Returns counts. `capped` is
    True when discovery hit `cap` (more posts page over on a later run)."""
    fetch = _fetch if _fetch is not None else fl.fetch
    if mode == "series":
        urls = discover_series_parts(seed, _session=_session)
    else:
        urls = discover_blog_posts(seed, cap, _session=_session)
    found = len(urls)
    written = duplicate = failed = 0
    for u in urls:
        if _post_collected(u, dedup_dirs):
            duplicate += 1
            continue
        try:
            content = fetch(u)
        except Exception:  # noqa: BLE001
            content = {}
        if not content or not content.get("text"):
            failed += 1
            continue
        write_post(seed, u, content, collected_at, via_vault_list=via_vault_list, inbox=inbox)
        written += 1
    return {"seed": seed, "mode": mode, "found": found, "written": written,
            "duplicate": duplicate, "failed": failed, "capped": found >= cap}
```

Delete the throwaway sketch test (`test_scrape_seed_writes_one_source_per_new_post`) if it was pasted — only the two concrete tests from Step 1 stay.

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_scrape_blog.py tests/test_collect_obsidian.py -k "scrape_seed or build_url_source" -o addopts="" -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add bin/scrape_blog.py bin/collect_obsidian.py tests/test_scrape_blog.py tests/test_collect_obsidian.py
git commit -m "feat(scrape-blog): scrape_seed per-post fetch/write with source_url dedup + scrape_seed frontmatter"
```

---

## Task 4: Routing hook in `obsidian_client.cmd_collect`

**Files:**
- Modify: `bin/obsidian_client.py` (import `scrape_blog`; rewrite the url-list branch of `cmd_collect`, lines 72-93; add `"scraped": 0` to the tally `t`, line 34-35)
- Test: `tests/test_obsidian_client.py`

**Interfaces:**
- Consumes: `collect_obsidian.iter_scrape_targets` (Task 1), `scrape_blog.scrape_seed` (Task 3).
- Produces: tagged TO-SCRAPE lines route to `scrape_blog.scrape_seed`; untagged lines keep the single-page path; `cmd_collect` JSON gains `"scraped": N` (sum of posts written across seeds; counts seeds on `--dry-run`).

- [ ] **Step 1: Write the failing test**

In `tests/test_obsidian_client.py` (mirror its existing style — it builds a fake vault dir and runs `cmd_collect` via `_args`/`main` or calls `cmd_collect` with a namespace; match whatever the file already does). Add:

```python
def test_cmd_collect_routes_blog_tag_to_scrape_seed(tmp_path, monkeypatch):
    import obsidian_client as oc
    import collect_obsidian as co
    # a vault with a TO SCRAPE.md holding one [blog] seed + one untagged URL
    listdir = tmp_path / "00_Inbox" / "Clippings"
    listdir.mkdir(parents=True)
    (listdir / "TO SCRAPE.md").write_text(
        "https://blog.example.com [blog]\nhttps://plain.example.com/post\n", encoding="utf-8")

    calls = {"scrape": [], "fetch": []}
    monkeypatch.setattr(oc.sb, "scrape_seed",
                        lambda seed, mode, cap, **k: calls["scrape"].append((seed, mode)) or
                        {"seed": seed, "mode": mode, "found": 3, "written": 3,
                         "duplicate": 0, "failed": 0, "capped": False})
    # untagged still goes through fetch_url -> stub it to avoid network + writes
    monkeypatch.setattr(oc, "fetch_url", lambda u: calls["fetch"].append(u) or {"title": "x", "text": "y"})
    # keep writes inside tmp: point INBOX at tmp
    monkeypatch.setattr(co, "INBOX", tmp_path / "inbox")
    # nothing previously collected
    monkeypatch.setattr(co, "url_already_collected", lambda u, dirs=None: False)
    monkeypatch.setattr(co, "url_in_ledger", lambda u, ledger: False)

    rc = oc.main(["collect", "--vault", str(tmp_path)])
    assert rc == 0
    assert calls["scrape"] == [("https://blog.example.com", "blog")]   # seed routed
    assert calls["fetch"] == ["https://plain.example.com/post"]        # untagged single-page
```

(If `test_obsidian_client.py` already has a vault-fixture helper, use it instead of hand-building the dir — match the file's conventions. The behavioural assertions stay the same.)

- [ ] **Step 2: Run to verify it fails**

Run: `python3 -m pytest tests/test_obsidian_client.py -k "routes_blog_tag" -o addopts="" -q`
Expected: FAIL (`AttributeError: module 'obsidian_client' has no attribute 'sb'`, or scrape_seed never called).

- [ ] **Step 3: Implement**

In `bin/obsidian_client.py`:

1. Add the import near the top imports (after `import fetch_link as fl`):
```python
import scrape_blog as sb  # noqa: E402
```

2. Add `"scraped": 0` to the tally dict `t` in `cmd_collect` (the dict at lines 34-35):
```python
    t = {"notes": 0, "urls": 0, "url_failed": 0, "skipped": 0, "scraped": 0,
         "inline_urls": 0, "inline_failed": 0, "inline_skipped_auth": 0, "inline_dropped": 0}
```

3. Replace the `else:  # url-list` branch (lines 72-93) with:
```python
            else:  # url-list
                text = Path(d["abs_path"]).read_text(encoding="utf-8", errors="replace")
                ledger = Path(d["abs_path"]).parent / "articles_processed.md"
                for tgt in co.iter_scrape_targets(text):
                    url, mode, cap = tgt["url"], tgt["mode"], tgt["cap"]
                    if mode in ("blog", "series"):
                        if args.dry_run:
                            t["scraped"] += 1      # count the seed; no network on dry run
                            continue
                        res = sb.scrape_seed(url, mode, cap, collected_at=collected_at,
                                             via_vault_list=d["rel_path"])
                        t["scraped"] += res["written"]
                        continue
                    # untagged -> existing single-page fetch
                    if co.url_already_collected(url) or co.url_in_ledger(url, ledger):
                        t["skipped"] += 1
                        continue
                    if args.dry_run:
                        t["urls"] += 1
                        continue
                    content = fetch_url(url)
                    if not content or not content.get("text"):
                        t["url_failed"] += 1
                        continue
                    path = co.url_filename(url, content.get("title", ""))
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(co.build_url_source(
                        {"source_url": url, "via_vault_list": d["rel_path"],
                         "title": content.get("title", ""), "collected_at": collected_at},
                        content["text"]), encoding="utf-8")
                    t["urls"] += 1
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_obsidian_client.py -o addopts="" -q`
Expected: PASS (the new test + all existing obsidian_client tests still green — the untagged path is byte-for-byte the old behaviour).

- [ ] **Step 5: Commit**

```bash
git add bin/obsidian_client.py tests/test_obsidian_client.py
git commit -m "feat(obsidian): route [blog]/[series] TO SCRAPE lines to scrape_blog; untagged unchanged"
```

---

## Task 5: Strike gating — `reapable` seed_strikes + `cmd_reap`

**Files:**
- Modify: `bin/collect_obsidian.py` (`reapable`, lines 232-243)
- Modify: `bin/obsidian_client.py` (`cmd_reap`, lines 164-198)
- Test: `tests/test_collect_obsidian.py`, `tests/test_obsidian_client.py`

**Interfaces:**
- Consumes: raw sources carrying `scrape_seed:` + `via_vault_list:` + (maybe) `corpus_ingested: true`.
- Produces: `reapable()` returns an added key `"seed_strikes": list[(via_vault_list, seed_url)]` — a seed appears **only** when it has ≥1 `scrape_seed` source and **all** of them are `corpus_ingested`. `scrape_seed` posts are excluded from `url_strikes`. `cmd_reap` strikes each `seed_strikes` entry via `_strike_url` and reports `"seeds_struck": N`.

- [ ] **Step 1: Write the failing tests**

In `tests/test_collect_obsidian.py` (the file's `_raw_sources` iterates `*.md` in `DEDUP_DIRS`; write sources into a tmp dir and pass it as `dedup_dirs`):

```python
def _src(scrape_seed=None, ingested=False, via="00_Inbox/Clippings/TO SCRAPE.md",
         source_url="https://b.com/p"):
    fm = ["---", "channel: web", f"source_url: {source_url}", f"via_vault_list: {via}"]
    if scrape_seed:
        fm.append(f"scrape_seed: {scrape_seed}")
    if ingested:
        fm.append("corpus_ingested: true")
    fm += ["---", "", "body", ""]
    return "\n".join(fm)

def test_reapable_seed_strikeable_only_when_all_posts_ingested(tmp_path):
    seed = "https://b.com"
    (tmp_path / "p1.md").write_text(_src(seed, ingested=True, source_url="https://b.com/p1"), encoding="utf-8")
    (tmp_path / "p2.md").write_text(_src(seed, ingested=False, source_url="https://b.com/p2"), encoding="utf-8")
    r = co.reapable([tmp_path])
    assert (("00_Inbox/Clippings/TO SCRAPE.md", seed) not in r["seed_strikes"])   # p2 not ingested

    (tmp_path / "p2.md").write_text(_src(seed, ingested=True, source_url="https://b.com/p2"), encoding="utf-8")
    r = co.reapable([tmp_path])
    assert ("00_Inbox/Clippings/TO SCRAPE.md", seed) in r["seed_strikes"]         # all ingested

def test_reapable_excludes_scrape_posts_from_url_strikes(tmp_path):
    (tmp_path / "p1.md").write_text(_src("https://b.com", ingested=True, source_url="https://b.com/p1"), encoding="utf-8")
    r = co.reapable([tmp_path])
    assert ("00_Inbox/Clippings/TO SCRAPE.md", "https://b.com/p1") not in r["url_strikes"]
```

In `tests/test_obsidian_client.py`:

```python
def test_cmd_reap_strikes_seeds(tmp_path, monkeypatch):
    import obsidian_client as oc, collect_obsidian as co
    monkeypatch.setattr(co, "reapable",
                        lambda dirs=None: {"vault_notes": [], "url_strikes": [],
                                           "seed_strikes": [("00_Inbox/Clippings/TO SCRAPE.md", "https://b.com")]})
    struck = []
    monkeypatch.setattr(oc, "_strike_url", lambda vault, lr, u: struck.append((lr, u)))
    monkeypatch.setattr(oc, "_under_vault", lambda v, r: True)
    rc = oc.main(["reap", "--vault", str(tmp_path)])
    assert rc == 0 and struck == [("00_Inbox/Clippings/TO SCRAPE.md", "https://b.com")]
```

- [ ] **Step 2: Run to verify they fail**

Run: `python3 -m pytest tests/test_collect_obsidian.py tests/test_obsidian_client.py -k "seed" -o addopts="" -q`
Expected: FAIL (`KeyError: 'seed_strikes'` / strike not called).

- [ ] **Step 3: Implement**

Replace `reapable` in `bin/collect_obsidian.py` (lines 232-243) with:

```python
def reapable(dedup_dirs=None) -> dict:
    notes, url_strikes = [], []
    seeds = {}   # seed -> {"list": via_vault_list|None, "count": int, "all_ingested": bool}
    for _, t in _raw_sources(dedup_dirs):
        ss = fm_field(t, "scrape_seed")
        if ss:   # a deep-scrape post: gates its SEED, never an ordinary url_strike
            vl = fm_field(t, "via_vault_list")
            rec = seeds.setdefault(ss, {"list": None, "count": 0, "all_ingested": True})
            rec["count"] += 1
            if vl and not rec["list"]:
                rec["list"] = vl
            if "corpus_ingested: true" not in t:
                rec["all_ingested"] = False
            continue
        if "corpus_ingested: true" not in t:
            continue
        vo = fm_field(t, "vault_origin")
        if vo:
            notes.append(vo)
        vl, su = fm_field(t, "via_vault_list"), fm_field(t, "source_url")
        if vl and su:
            url_strikes.append((vl, su))
    seed_strikes = [(rec["list"], seed) for seed, rec in seeds.items()
                    if rec["count"] >= 1 and rec["all_ingested"] and rec["list"]]
    return {"vault_notes": notes, "url_strikes": url_strikes, "seed_strikes": seed_strikes}
```

In `bin/obsidian_client.py` `cmd_reap`: add `"seeds_struck": 0` to the tally `t` (line 167), and after the `url_strikes` loop (after line 190) add:

```python
    for list_rel, seed in r.get("seed_strikes", []):
        if not _under_vault(vault, list_rel):
            continue
        if not args.dry_run:
            _strike_url(vault, list_rel, seed)
        t["seeds_struck"] += 1
```

(The `t` dict at line 167 becomes:
```python
    t = {"notes_removed": 0, "frames_removed": 0, "urls_struck": 0,
         "seeds_struck": 0, "not_removed": []}
```
)

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_collect_obsidian.py tests/test_obsidian_client.py -o addopts="" -q`
Expected: PASS (new seed tests + all existing obsidian tests green).

- [ ] **Step 5: Commit**

```bash
git add bin/collect_obsidian.py bin/obsidian_client.py tests/test_collect_obsidian.py tests/test_obsidian_client.py
git commit -m "feat(obsidian): strike a scrape seed only when all its posts are corpus_ingested"
```

---

## Task 6: Wire the Obsidian reaper into the nightly + document the syntax

**Files:**
- Modify: `bin/scheduled_run.py` (add `run_obsidian_reap()` near `run_x_reap`, ~line 492; call it in the post-ingest phase, ~line 972; surface in `build_summary`, ~line 495)
- Create: `docs/solutions/2026-06-26-blog-series-scraper.md` (engineering note: the TO-SCRAPE tag syntax + how reaping now runs nightly)
- Test: `tests/test_scheduled_run.py`

**Interfaces:**
- Consumes: `obsidian_client.py reap` CLI (Task 5).
- Produces: `run_obsidian_reap(*, _subprocess_run=None) -> dict`; called post-ingest after `run_x_reap`; `build_summary` gains `"obsidian_reap"`.

> **Why this task exists (discovery):** the Obsidian reaper is currently NOT invoked by `scheduled_run.py` — only gmail/x/pdf reaps are. Without it, the seed-strike from Task 5 (and the *existing* single-page strike) never runs in the nightly. Wiring it activates striking. Note the reaper also stages ingested vault-note deletions via `git rm` (the established §2 vault-removal exception — staged, never committed; recoverable from vault git). That is the intended collect→ingest→reap model; this task turns it on for the unattended run.

> **Doc-location deviation from spec §4.4:** the spec said document the syntax in `corpus/_config.md`. Per the repo's hard rule the `corpus/` tree is owned by the corpus's own operations; user-facing tooling docs live in `docs/`. Document the tag syntax in `docs/solutions/` instead. (If the maintainer later wants it in `corpus/_config.md`, that's a corpus-op edit done separately.)

- [ ] **Step 1: Write the failing tests**

In `tests/test_scheduled_run.py` (mirror `test_run_pdf_reap_invokes_pdf_file` / `TestBuildSummary`):

```python
    def test_run_obsidian_reap_invokes_reap(self):
        called = []
        def fake_run(cmd, **kwargs):
            called.append(" ".join(cmd))
            import types
            return types.SimpleNamespace(returncode=0, stdout='{"urls_struck": 1, "seeds_struck": 2}', stderr="")
        result = scheduled_run.run_obsidian_reap(_subprocess_run=fake_run)
        assert any("obsidian_client.py" in s and s.endswith("reap") for s in called), called
        assert result.get("seeds_struck") == 2

    def test_run_obsidian_reap_records_failure_without_raising(self):
        def fake_run(cmd, **kwargs):
            import types
            return types.SimpleNamespace(returncode=1, stdout="", stderr="vault missing")
        result = scheduled_run.run_obsidian_reap(_subprocess_run=fake_run)
        assert result["status"] == "failed" and "vault missing" in result["error"]
```

And in `TestBuildSummary`:

```python
    def test_includes_obsidian_reap(self):
        s = scheduled_run.build_summary({"obsidian_reap": {"seeds_struck": 2}}, dry_run=False)
        assert s["obsidian_reap"] == {"seeds_struck": 2}

    def test_obsidian_reap_defaults_empty_when_absent(self):
        s = scheduled_run.build_summary({}, dry_run=False)
        assert s["obsidian_reap"] == {}
```

- [ ] **Step 2: Run to verify they fail**

Run: `python3 -m pytest tests/test_scheduled_run.py -k "obsidian_reap" -o addopts="" -q`
Expected: FAIL (`AttributeError: ... 'run_obsidian_reap'` / `KeyError: 'obsidian_reap'`).

- [ ] **Step 3: Implement**

In `bin/scheduled_run.py`, after `run_x_reap` (ends ~line 492), add:

```python
def run_obsidian_reap(*, _subprocess_run=None) -> dict:
    """Post-ingest: invoke `obsidian_client.py reap` to strike now-ingested URLs
    (single-page AND deep-scrape seeds whose posts are all corpus_ingested) from
    TO SCRAPE.md and stage ingested vault-note deletions (git rm, never committed
    — §2 vault-removal exception). Gated on corpus_ingested inside the subcommand.
    Failure recorded, never raised."""
    _run = _subprocess_run if _subprocess_run is not None else subprocess.run
    try:
        proc = _run([sys.executable, str(BIN / "obsidian_client.py"), "reap"],
                    capture_output=True, text=True)
        if proc.returncode != 0:
            return {"status": "failed", "error": proc.stderr.strip() or f"exit {proc.returncode}"}
        try:
            return json.loads(proc.stdout)
        except (json.JSONDecodeError, AttributeError):
            return {"status": "ok"}
    except Exception as exc:  # noqa: BLE001
        return {"status": "failed", "error": str(exc)}
```

In `build_summary`, add the key (after `"x_reap"`):
```python
        "obsidian_reap": tallies.get("obsidian_reap", {}),
```

In the post-ingest phase, after the `x_reap` try/except block (~line 972), add:
```python
                # Post-ingest: strike now-ingested obsidian URLs/seeds + stage
                # ingested vault-note deletions (gated on corpus_ingested).
                # Failure must NOT abort the run.
                try:
                    tallies["obsidian_reap"] = run_obsidian_reap()
                except Exception as exc:  # noqa: BLE001
                    tallies["obsidian_reap"] = {"status": "failed", "error": str(exc)}
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_scheduled_run.py -k "obsidian_reap or build_summary" -o addopts="" -q`
Expected: PASS.

- [ ] **Step 5: Write the engineering note**

Create `docs/solutions/2026-06-26-blog-series-scraper.md`:

```markdown
---
module: collectors
tags: [obsidian, blog, scraping, reaping]
problem_type: feature
---

# Blog / series deep-scraper (TO SCRAPE tags)

Lines in the vault's `00_Inbox/Clippings/TO SCRAPE.md` accept an optional trailing tag:

- `https://blog.example.com [blog]` — scrape ALL posts (sitemap.xml first; RSS/Atom
  fallback). Default cap 200 posts; raise with `[blog:500]`. Posts over the cap page in
  over later runs.
- `https://site.com/the-guide [series]` — scrape the parts linked under the index's path.
- `https://one-article.com/post` — untagged: single-page fetch (unchanged).

Each post becomes a `raw/_inbox/web-*.md` source tagged `scrape_seed: <seed>`. The seed
line is struck from `TO SCRAPE.md` only once EVERY one of its posts is `corpus_ingested`
(so multi-run / paged scrapes are safe). Dedup is by `source_url` — re-tagging a blog
later only adds new posts.

Reaping (the strike, plus staging ingested vault-note deletions) runs nightly via
`scheduled_run.py` → `obsidian_client.py reap`. JS-only blogs with no sitemap/RSS scrape 0
posts and keep their seed (logged), pending browser-automation support.
```

- [ ] **Step 6: Commit**

```bash
git add bin/scheduled_run.py docs/solutions/2026-06-26-blog-series-scraper.md tests/test_scheduled_run.py
git commit -m "feat(scheduled-run): wire obsidian reaper into nightly (activates URL/seed strikes) + docs"
```

---

## Notes for the executor

- **Branch/commit isolation (two-writer hazard):** the Mac scheduled run writes `raw/` + may leave the working tree dirty. Work on a feature branch; when staging, **stage only the exact files each step lists** — never `git add -A`. `raw/` is gitignored so collector output won't be staged anyway.
- **Per-task test scope:** run only the test file(s) you touched with `-o addopts=""`. Avoid the full suite (the `test_scheduled_run.py` lock-integration tests are slow/flaky and unrelated).
- **Final whole-branch review** should confirm: untagged TO-SCRAPE behaviour is byte-for-byte unchanged (Task 4); no network in any test (all `_session`/`_fetch`/`fetch_url`/subprocess injected); the seed-strike gate truly requires ALL posts ingested (Task 5); reaper wiring failure can't abort the nightly (Task 6).
```
