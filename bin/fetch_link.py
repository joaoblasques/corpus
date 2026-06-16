#!/usr/bin/env python3
"""fetch_link.py — classify a link and fetch its content (article or YouTube)."""
from __future__ import annotations

import re

UA = "corpus-collector/1.0 (+personal archival)"
TIMEOUT = 10.0
MAX_BYTES = 2_000_000

YT_RE = re.compile(
    r"(?i)(?:youtube\.com/watch\?[^ ]*v=|youtu\.be/|youtube\.com/shorts/)"
    r"([A-Za-z0-9_-]{11})"
)
PDF_RE = re.compile(r"(?i)\.pdf(\?|$)")
# github.com/<owner>/<repo>/blob/<branch>/<path> → raw.githubusercontent.com/...
GITHUB_BLOB_RE = re.compile(r"(?i)^https?://github\.com/([^/]+)/([^/]+)/blob/(.+)$")


_RAW_HOST_RE = re.compile(r"(?i)^https?://(?:raw\.githubusercontent\.com|gist\.githubusercontent\.com)/")


def github_raw(url: str) -> str | None:
    """Rewrite a GitHub blob URL to its raw.githubusercontent.com form.

    The blob page is a JS-heavy HTML shell trafilatura extracts nothing from
    (→ fetch-failed); the raw URL serves the plain markdown/code directly.
    Returns None for non-blob / non-GitHub URLs.
    """
    m = GITHUB_BLOB_RE.match(url or "")
    if not m:
        return None
    owner, repo, rest = m.groups()
    rest = rest.split("#", 1)[0].split("?", 1)[0]
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{rest}"


def raw_text_url(url: str) -> str | None:
    """The plain-text URL to fetch for source-text hosts, or None.

    Routes GitHub blob pages (rewritten) and already-raw hosts
    (raw/gist.githubusercontent.com) to `fetch_text` so trafilatura — which
    extracts nothing from raw markdown/code — is bypassed.
    """
    rewritten = github_raw(url)
    if rewritten:
        return rewritten
    if _RAW_HOST_RE.match(url or ""):
        return url
    return None


def youtube_id(url: str) -> str | None:
    m = YT_RE.search(url or "")
    return m.group(1) if m else None


def classify(url: str) -> str:
    if youtube_id(url):
        return "youtube"
    if not re.match(r"(?i)^https?://", url or ""):
        return "unsupported"
    if PDF_RE.search(url):
        return "unsupported"
    return "article"


def _client(client=None):
    import httpx
    return client or httpx.Client(
        follow_redirects=True, timeout=TIMEOUT, headers={"User-Agent": UA}
    )


def resolve(url: str, client=None) -> str:
    """Follow redirects to the canonical destination (unwraps Substack wrappers)."""
    c = _client(client)
    try:
        r = c.get(url)
        return str(r.url)
    except Exception:
        return url
    finally:
        if client is None:
            c.close()


def extract_article(html: str, url: str) -> dict:
    import trafilatura
    text = trafilatura.extract(html, include_links=False, include_comments=False) or ""
    if not text.strip():
        raise ValueError("empty extraction")
    meta = trafilatura.extract_metadata(html)
    title = (meta.title if meta and meta.title else "") or url
    return {"title": title, "text": text, "channel": "web"}


def fetch_article(url: str, client=None) -> dict:
    c = _client(client)
    try:
        r = c.get(url)
        r.raise_for_status()
        html = r.text[:MAX_BYTES]
    finally:
        if client is None:
            c.close()
    return extract_article(html, url)


def fetch_text(url: str, orig: str | None = None, client=None) -> dict:
    """Fetch a plain-text/markdown/code resource (e.g. a raw GitHub file) directly.

    Skips trafilatura — the content is already clean source text, not HTML to
    extract an article from. Title is the file basename.
    """
    c = _client(client)
    try:
        r = c.get(url)
        r.raise_for_status()
        text = r.text[:MAX_BYTES]
    finally:
        if client is None:
            c.close()
    if not text.strip():
        raise ValueError("empty fetch")
    title = url.rstrip("/").split("/")[-1] or (orig or url)
    return {"title": title, "text": text, "channel": "web"}


def fetch_youtube(url: str) -> dict:
    from youtube_transcript_api import YouTubeTranscriptApi
    vid = youtube_id(url)
    fetched = YouTubeTranscriptApi().fetch(vid)
    lines = [
        f"[{int(s.start) // 60:02d}:{int(s.start) % 60:02d}] {s.text}"
        for s in fetched
    ]
    return {"title": f"YouTube {vid}", "text": "\n".join(lines), "channel": "youtube"}


def fetch(url: str) -> dict:
    kind = classify(url)
    if kind == "youtube":
        return fetch_youtube(url)
    if kind == "article":
        rt = raw_text_url(url)
        if rt:
            return fetch_text(rt, url)
        return fetch_article(url)
    raise ValueError(f"unsupported url: {url}")
