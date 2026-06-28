#!/usr/bin/env python3
"""scrape_blog.py — deep-scrape a blog (sitemap/RSS) or a series (index page)
into per-post raw sources.

All HTTP goes through injectable seams: `_session(url)->str` for sitemap/feed/
index GETs, `_fetch(url)->dict` for per-post content. Tests pass these and never
touch the network. Discovery is heuristic (spec §4.2): sitemap-first with an
RSS/Atom fallback for blogs; same-path `<a href>` links for series.
"""
from __future__ import annotations

import hashlib
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urljoin, urlparse

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
INBOX = ROOT / "raw" / "_inbox"
# Persistent "seen post URLs" ledger: lets shelved/pruned backfill posts stay
# deduped (never re-scraped) WITHOUT keeping their content files on disk. One
# url per line. Gitignored, local-only. Checked alongside the on-disk dedup.
SEEN_LEDGER = ROOT / "raw" / ".blog_seen_urls.txt"
sys.path.insert(0, str(BIN))
import collect_obsidian as co  # noqa: E402
import fetch_link as fl        # noqa: E402

DEFAULT_CAP = 25
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


def load_seen(path=None) -> set:
    """Load the seen-URL ledger as a set (empty if absent)."""
    p = Path(path) if path is not None else SEEN_LEDGER
    try:
        return {ln.strip() for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()}
    except OSError:
        return set()


def _post_collected(url: str, dirs=None, seen=None) -> bool:
    """A post is 'collected' if it's in the seen-ledger OR already on disk. The
    ledger lets a shelved backfill stay deduped without keeping its files."""
    if seen is None:
        seen = load_seen()
    return url in seen or co.url_already_collected(url, dirs)


def write_post(seed: str, url: str, content: dict, collected_at: str,
               *, via_vault_list: str, inbox=None) -> Path:
    """Write one per-post raw source (channel web) tagged with scrape_seed.

    Filename is web-<slug>-<8-char url hash>.md so posts with identical titles
    (or both empty-title) never collide — each source_url maps to a unique path.
    """
    base = inbox if inbox is not None else INBOX
    slug = co.slugify(content.get("title", "") or url)
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    path = base / f"web-{slug}-{digest}.md"
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
    seen = load_seen()   # load the ledger once per seed, not per post
    for u in urls:
        if _post_collected(u, dedup_dirs, seen):
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
