#!/usr/bin/env python3
"""collect_obsidian.py — deterministic core for the collect-obsidian collector.

Pure functions: path policy, URL-list parsing, source-frontmatter building, dedup,
discovery, and the reaper selector. All I/O (copies, fetch, git) lives in
obsidian_client.py. Reuses helpers from collect_email (DRY).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
INBOX = ROOT / "raw" / "_inbox"
DEDUP_DIRS = [ROOT / "raw" / "_inbox", ROOT / "raw" / "notes", ROOT / "raw" / "web"]

VAULT_ROOT = Path("/Users/jonasblasques/Dev/second-brain")
INCLUDE_DIRS = [
    "Clippings",                       # top-level web clippings
    "00_Inbox/Clippings",
    "03_Resources/Books",
    "06_Metadata/Reference",           # reference prompt notes only
]
EXCLUDE_DIRS = [
    "03_Resources/llm-wiki-system",
]
EXCLUDE_FILE_RE = re.compile(r"(?i)(_processed\.md$|(^|/)README\.md$)")
URL_LIST_NAMES = {"articles to process.md", "blogs to scrape.md"}
# Per-list default scrape mode for UNTAGGED lines (an explicit [blog]/[series]
# tag on a line still overrides). "blogs to scrape" treats every line as a blog
# to deep-scrape; "articles to process" stays single-page (mode None).
URL_LIST_DEFAULT_MODE = {
    "blogs to scrape.md": "blog",
    "articles to process.md": None,
}
# Watch-mode lists are NEVER auto-struck: their blog seeds stay in the list
# permanently so each scheduled collect re-scrapes them and picks up new posts
# (dedup by source_url means only genuinely new articles are added). Consume-mode
# lists (e.g. "articles to process.md") still get their lines struck once ingested.
WATCH_LISTS = {"blogs to scrape.md"}
MAX_LINKS_PER_NOTE = 10
AUTH_WALLED_RE = re.compile(r"(?i)://(?:[^/]*\.)?(?:linkedin\.com|x\.com|twitter\.com)(?:/|$)")
ASSET_EXT_RE = re.compile(r"(?i)\.(?:png|jpe?g|gif|svg|webp|pdf|mp4|mov|zip)$")

sys.path.insert(0, str(BIN))
from collect_email import slugify, yaml_scalar, URL_RE  # noqa: E402


def is_included(rel_path: str) -> bool:
    rel = rel_path.replace("\\", "/")
    if any(rel == e or rel.startswith(e + "/") for e in EXCLUDE_DIRS):
        return False
    if not rel.endswith(".md"):
        return False
    if EXCLUDE_FILE_RE.search(rel):
        return False
    return any(rel.startswith(i + "/") for i in INCLUDE_DIRS)


def classify(rel_path: str) -> str:
    return "url-list" if rel_path.rsplit("/", 1)[-1] in URL_LIST_NAMES else "note"


def parse_url_list(text: str) -> list:
    seen, out = set(), []
    for m in URL_RE.finditer(text or ""):
        u = m.group(0).rstrip(".,)")
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


DEFAULT_BLOG_CAP = 25   # watch-list scrape depth per blog: incremental, not full-archive
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


def list_default_mode(rel_path: str):
    """Default scrape mode for untagged lines of a url-list file, keyed by its
    basename (e.g. 'blogs to scrape.md' -> 'blog'). None for unknown lists."""
    return URL_LIST_DEFAULT_MODE.get(rel_path.rsplit("/", 1)[-1])


def is_watch_list(rel_path) -> bool:
    """True if this url-list is watch-mode (re-scraped forever; seeds never struck).
    Keyed by basename so it survives the file living under any folder. A None/empty
    path (a seed with no recorded via_vault_list) is not a watch list."""
    return bool(rel_path) and rel_path.rsplit("/", 1)[-1] in WATCH_LISTS


def iter_scrape_targets(text: str, default_mode=None) -> list:
    """Per-line {url, mode, cap} for every url-list line that holds a URL,
    order-preserved and deduped by url (first occurrence's tag wins). An
    untagged line (mode None) inherits `default_mode` — so a whole list can
    default to blog-scraping without per-line [blog] tags; an explicit
    [blog]/[series] tag on a line always overrides the default."""
    seen, out = set(), []
    for line in (text or "").splitlines():
        tgt = parse_scrape_tag(line)
        if tgt["url"] and tgt["url"] not in seen:
            seen.add(tgt["url"])
            if tgt["mode"] is None:
                tgt["mode"] = default_mode
            out.append(tgt)
    return out


def extract_inline_links(body: str, source_url: str = "") -> dict:
    """External http(s) links in a note body: deduped, minus the source URL, asset
    links, and auth-walled domains; capped at MAX_LINKS_PER_NOTE."""
    seen, links, auth = set(), [], 0
    for m in URL_RE.finditer(body or ""):
        u = m.group(0).rstrip(".,)")
        if u in seen:
            continue
        seen.add(u)
        if source_url and u == source_url.rstrip(".,)"):
            continue
        if ASSET_EXT_RE.search(u.split("?", 1)[0]):
            continue
        if AUTH_WALLED_RE.search(u):
            auth += 1
            continue
        links.append(u)
    dropped = max(0, len(links) - MAX_LINKS_PER_NOTE)
    return {"links": links[:MAX_LINKS_PER_NOTE], "auth_skipped": auth, "dropped": dropped}


def read_note(abs_path: str):
    """Return (title, tags, source_url, body) — splits the note's frontmatter off the body."""
    t = Path(abs_path).read_text(encoding="utf-8", errors="replace")
    title, tags, source_url, body = "", [], "", t
    if t.startswith("---"):
        end = t.find("\n---", 3)
        if end != -1:
            fm, body = t[3:end], t[end + 4:].lstrip("\n")
            tm = re.search(r"^title:\s*(.+)$", fm, re.M)
            if tm:
                title = tm.group(1).strip().strip('"')
            sm = re.search(r"^source:\s*(.+)$", fm, re.M)
            if sm:
                source_url = sm.group(1).strip().strip('"')
            tg = re.search(r"^tags:\s*\n((?:\s*-\s*.+\n?)+)", fm, re.M)
            if tg:
                tags = [re.sub(r"^\s*-\s*", "", ln).strip() for ln in tg.group(1).splitlines() if ln.strip()]
    if not title:
        title = Path(abs_path).stem
    return title, tags, source_url, body


def note_filename(rel_path: str, base=None) -> Path:
    base = base if base is not None else INBOX
    parts = rel_path.replace("\\", "/").split("/")
    stem = parts[-1]
    if stem.endswith(".md"):
        stem = stem[:-3]
    # full parent path slug so same-titled notes in different trees never collide
    parent_slug = slugify("-".join(parts[:-1])) if len(parts) >= 2 else ""
    name = f"notes-{parent_slug}-{slugify(stem)}.md" if parent_slug else f"notes-{slugify(stem)}.md"
    return base / name


def url_filename(url: str, title: str, base=None) -> Path:
    base = base if base is not None else INBOX
    return base / f"web-{slugify(title or url)}.md"


def build_note_source(meta: dict, body: str) -> str:
    lines = [
        "---", "channel: notes", "source: obsidian",
        f"vault_origin: {meta['vault_origin']}",
        f"title: {yaml_scalar(meta.get('title', ''))}",
    ]
    tags = meta.get("tags") or []
    if tags:
        lines.append("tags:")
        lines += [f"  - {t}" for t in tags]
    lines += [f"collected_at: {meta['collected_at']}", "---", "", body.strip(), ""]
    return "\n".join(lines)


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


def _frontmatter(text: str) -> str:
    """Return only the text inside the leading `---\\n ... \\n---` block.

    Empty string if the file doesn't start with `---` or has no closing `---`.
    This prevents body content (e.g. an article quoting this system's frontmatter)
    from being mistaken for the file's own frontmatter.
    """
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    if end == -1:
        return ""
    return text[3:end].strip("\n")


def fm_field(text: str, key: str):
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", _frontmatter(text), re.M)
    return m.group(1).strip() if m else None


def is_vault_note_ingested(abs_path: str) -> bool:
    try:
        t = Path(abs_path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    return "corpus_ingested: true" in _frontmatter(t)


def _raw_sources(dirs=None):
    for d in (dirs if dirs is not None else DEDUP_DIRS):
        p = Path(d)
        if not p.exists():
            continue
        for md in p.glob("*.md"):
            try:
                yield md, md.read_text(encoding="utf-8", errors="replace")
            except (OSError, UnicodeDecodeError):
                continue


def already_collected_vault(rel_path: str, dirs=None) -> bool:
    needle = f"vault_origin: {rel_path}\n"
    return any(needle in t for _, t in _raw_sources(dirs))


def url_already_collected(url: str, dirs=None) -> bool:
    needle = f"source_url: {url}\n"
    return any(needle in t for _, t in _raw_sources(dirs))


def url_in_ledger(url: str, ledger_path) -> bool:
    """True if `url` appears in the per-list articles_processed.md ledger."""
    p = Path(ledger_path)
    try:
        return url in p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False


def discover(vault_root=None, dedup_dirs=None) -> list:
    root = Path(vault_root) if vault_root else VAULT_ROOT
    out = []
    for inc in INCLUDE_DIRS:
        base = root / inc
        if not base.exists():
            continue
        for f in sorted(base.rglob("*.md")):
            rel = str(f.relative_to(root))
            if not is_included(rel):
                continue
            if is_vault_note_ingested(str(f)):
                continue
            if already_collected_vault(rel, dedup_dirs):
                continue
            out.append({"rel_path": rel, "abs_path": str(f), "kind": classify(rel)})
    return out


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
                    if rec["count"] >= 1 and rec["all_ingested"] and rec["list"]
                    and not is_watch_list(rec["list"])]   # watch lists are never struck
    return {"vault_notes": notes, "url_strikes": url_strikes, "seed_strikes": seed_strikes}
