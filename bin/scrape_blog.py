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
