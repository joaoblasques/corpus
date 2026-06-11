# Email Link-Following Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend `collect-email` so each collected email also follows the useful links inside it and captures their content as `raw/web` / `raw/youtube` source files — strictly bounded (depth-1, noise-filtered, LLM utility-ranked, quality-floored, capped at 10).

**Architecture:** A pipeline runs *after* an email is written and archived: pure-Python `select_links` (extract + noise filter + description) → `rank_links.rank` (Anthropic Haiku scores learning-utility, heuristic fallback, applies floor + cap) → `fetch_link.fetch` (httpx+trafilatura for articles, youtube_transcript_api for video) → write one raw file per link + patch the parent email's `links:` frontmatter. Determinism lives in pure functions with pytest; network/LLM code is mocked or fixture-tested.

**Tech Stack:** Python 3.12, httpx, trafilatura, youtube_transcript_api, anthropic SDK, pytest.

**Spec:** `docs/superpowers/specs/2026-06-11-email-link-following-design.md`

---

## File Structure

| File | Responsibility |
|---|---|
| `bin/collect_email.py` *(modify)* | + `select_links` (pure), `heuristic_score` (pure), `build_link_document`, `link_target`, `add_links_frontmatter`. |
| `bin/rank_links.py` *(new)* | `.env` loader, `score_candidates` (Anthropic Haiku + heuristic fallback), `rank` (floor + cap → dispositions). |
| `bin/fetch_link.py` *(new)* | `youtube_id`, `classify`, `resolve`, `fetch_article`, `fetch_youtube`, `fetch`. |
| `bin/gmail_client.py` *(modify)* | `enrich_email` orchestration in `cmd_run`; `--no-links`, `--max-links` flags; tally fields. |
| `tests/test_collect_email.py` *(modify)* | pure-logic tests for new functions. |
| `tests/test_rank_links.py` *(new)* | rank/floor/cap + fallback (mock Anthropic). |
| `tests/test_fetch_link.py` *(new)* | classify/youtube_id (pure) + extraction (HTML fixture). |

---

## Task 1: Install dependencies

**Files:** none (environment).

- [ ] **Step 1: Install the two new libraries**

Run:
```bash
python3 -m pip install trafilatura youtube_transcript_api
```
Expected: ends with `Successfully installed ... trafilatura-... youtube-transcript-api-...`

- [ ] **Step 2: Verify imports and confirm the transcript API shape**

Run:
```bash
python3 -c "import trafilatura, httpx, anthropic; print('core ok')"
python3 -c "from youtube_transcript_api import YouTubeTranscriptApi; print([m for m in dir(YouTubeTranscriptApi) if not m.startswith('_')])"
```
Expected: `core ok`, then a method list. **Note which transcript method exists:** modern (1.x) exposes instance `fetch`; legacy exposes `get_transcript`. Task 6 uses `fetch` (1.x); if only `get_transcript` is present, adapt `fetch_youtube` to the legacy call noted there.

- [ ] **Step 3: Commit nothing yet** — deps aren't tracked (no requirements file in repo). Proceed.

---

## Task 2: `select_links` — pure extraction + noise filter

**Files:**
- Modify: `bin/collect_email.py`
- Test: `tests/test_collect_email.py`

- [ ] **Step 1: Write failing tests**

Add to `tests/test_collect_email.py`:
```python
def test_select_links_extracts_url_and_description():
    body = "Agentic AI Flywheels [ https://news.example.com/flywheels ] (15 min read)\nHow evals create a flywheel."
    links = ce.select_links(body)
    assert len(links) == 1
    assert links[0]["url"] == "https://news.example.com/flywheels"
    assert "Agentic AI Flywheels" in links[0]["description"]


def test_select_links_drops_noise():
    body = ("Unsubscribe https://list.example.com/unsubscribe?id=9\n"
            "Follow us https://twitter.com/example\n"
            "Real article https://blog.example.com/post")
    urls = [l["url"] for l in ce.select_links(body)]
    assert urls == ["https://blog.example.com/post"]


def test_select_links_dedups():
    body = "A https://x.example.com/a\nB https://x.example.com/a"
    assert len(ce.select_links("https://x.example.com/a " + body)) == 1


def test_select_links_skips_images():
    assert ce.select_links("logo https://cdn.example.com/logo.png") == []
```

- [ ] **Step 2: Run to verify they fail**

Run: `python3 -m pytest tests/test_collect_email.py -k select_links -q`
Expected: FAIL (`module 'collect_email' has no attribute 'select_links'`).

- [ ] **Step 3: Implement `select_links`**

Add to `bin/collect_email.py` (after `detect_pointer`):
```python
NOISE_URL_RE = re.compile(
    r"(?i)(unsubscribe|list-manage|mailchi\.mp|/sub/|/profile|update.*profile|"
    r"twitter\.com|x\.com|facebook\.com|linkedin\.com|instagram\.com|t\.me|"
    r"mailto:)"
)
NOISE_TEXT_RE = re.compile(
    r"(?i)(unsubscribe|view (this )?(post|email) (on|in) the web|view in browser|"
    r"manage (your )?subscription|update your profile)"
)
IMG_EXT_RE = re.compile(r"(?i)\.(png|jpe?g|gif|svg|webp|ico)(\?|$)")


def select_links(body: str) -> list[dict]:
    """Pure: extract content links with a nearby description, drop noise, dedup.

    Resolution of redirect wrappers and a second-pass filter happen later in the
    fetch stage (they require the network); this stays deterministic and testable.
    """
    lines = (body or "").splitlines()
    seen: set[str] = set()
    out: list[dict] = []
    for i, line in enumerate(lines):
        for m in URL_RE.finditer(line):
            url = m.group(0).rstrip(").,]>”\"'")
            if url in seen or NOISE_URL_RE.search(url) or IMG_EXT_RE.search(url):
                continue
            desc = re.sub(r"[\[\]]", " ", URL_RE.sub("", line))
            desc = re.sub(r"\s+", " ", desc).strip()
            if len(desc) < 8:
                for j in range(i + 1, min(i + 3, len(lines))):
                    nxt = lines[j].strip()
                    if nxt and not URL_RE.search(nxt):
                        desc = nxt
                        break
            if NOISE_TEXT_RE.search(desc):
                continue
            seen.add(url)
            out.append({"url": url, "description": desc[:300]})
    return out
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_collect_email.py -k select_links -q`
Expected: 4 passed.

- [ ] **Step 5: Commit**
```bash
git add bin/collect_email.py tests/test_collect_email.py
git commit -m "feat(collect-email): select_links pure extraction + noise filter"
```

---

## Task 3: `heuristic_score` — deterministic fallback ranker

**Files:**
- Modify: `bin/collect_email.py`
- Test: `tests/test_collect_email.py`

- [ ] **Step 1: Write failing tests**
```python
def test_heuristic_score_boosts_learning_and_github():
    s = ce.heuristic_score("https://github.com/org/rag-toolkit", "A practical RAG tutorial")
    assert s >= 8


def test_heuristic_score_penalizes_news():
    s = ce.heuristic_score("https://news.example.com/x", "NVIDIA announces new data center, raises $40M")
    assert s <= 3


def test_heuristic_score_clamped_0_10():
    assert 0 <= ce.heuristic_score("https://x.example.com", "") <= 10
```

- [ ] **Step 2: Run to verify they fail**

Run: `python3 -m pytest tests/test_collect_email.py -k heuristic -q`
Expected: FAIL (no attribute `heuristic_score`).

- [ ] **Step 3: Implement `heuristic_score`**

Add to `bin/collect_email.py`:
```python
LEARN_RE = re.compile(
    r"(?i)\b(guide|tutorial|how[\s-]?to|explained?|introduction|deep[\s-]?dive|"
    r"fundamentals|concept|primer|walkthrough|learn|course|patterns?|reference|"
    r"cheat[\s-]?sheet|build(ing)?)\b"
)
NEWS_RE = re.compile(
    r"(?i)(\bannounce[ds]?\b|\blaunch(es|ed)?\b|\braises?\b|\braised\b|\bfunding\b|"
    r"\bseries [a-d]\b|\bacqui(re|res|red|sition)\b|\bvaluation\b|\bhires?\b|"
    r"\bappoints?\b|\$\d+\s?(m|b|million|billion)\b)"
)


def heuristic_score(url: str, description: str) -> int:
    """Pure 0-10 learning-utility score; fallback when LLM ranking is unavailable."""
    text = f"{url} {description}".lower()
    score = 5
    if "github.com" in text:
        score += 3
    if re.search(r"(docs?\.|/docs/|readthedocs|\.dev/)", text):
        score += 1
    if LEARN_RE.search(text):
        score += 2
    if NEWS_RE.search(text):
        score -= 3
    return max(0, min(10, score))
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_collect_email.py -k heuristic -q`
Expected: 3 passed.

- [ ] **Step 5: Commit**
```bash
git add bin/collect_email.py tests/test_collect_email.py
git commit -m "feat(collect-email): heuristic_score fallback ranker"
```

---

## Task 4: `rank_links.py` — ranking with floor + cap

**Files:**
- Create: `bin/rank_links.py`
- Test: `tests/test_rank_links.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_rank_links.py`:
```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import rank_links as rl  # noqa: E402


def _cands(n):
    return [{"url": f"https://x.example.com/{i}", "description": f"item {i}"} for i in range(n)]


def test_rank_applies_floor(monkeypatch):
    monkeypatch.setattr(rl, "score_candidates", lambda c: [9, 2, 7])
    out = rl.rank(_cands(3), max_links=10, floor=4)
    by_url = {d["url"]: d for d in out}
    assert by_url["https://x.example.com/1"]["fetch"] is False
    assert by_url["https://x.example.com/1"]["reason"] == "low-utility"
    assert by_url["https://x.example.com/0"]["fetch"] is True


def test_rank_caps_top_n(monkeypatch):
    monkeypatch.setattr(rl, "score_candidates", lambda c: [8] * 12)
    out = rl.rank(_cands(12), max_links=10, floor=4)
    assert sum(1 for d in out if d["fetch"]) == 10
    assert sum(1 for d in out if d["reason"] == "over-cap") == 2


def test_rank_fallback_used_without_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(rl, "load_env", lambda *a, **k: None)
    scores = rl.score_candidates([{"url": "https://github.com/x/y", "description": "tutorial"}])
    assert scores[0] >= 8  # heuristic path


def test_rank_sorts_by_score_desc(monkeypatch):
    monkeypatch.setattr(rl, "score_candidates", lambda c: [3, 9, 6])
    out = rl.rank(_cands(3), max_links=10, floor=0)
    assert [d["score"] for d in out] == [9, 6, 3]
```

- [ ] **Step 2: Run to verify they fail**

Run: `python3 -m pytest tests/test_rank_links.py -q`
Expected: FAIL (`No module named 'rank_links'`).

- [ ] **Step 3: Implement `bin/rank_links.py`**
```python
#!/usr/bin/env python3
"""rank_links.py — score candidate links by learning utility, apply floor + cap.

Primary path: one Anthropic Haiku call ranks links by knowledge/learning utility.
Fallback (no ANTHROPIC_API_KEY or API error): collect_email.heuristic_score.
"""
from __future__ import annotations

import json
import os
import pathlib
import sys

BIN = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
import collect_email as ce  # noqa: E402

RANK_MODEL = "claude-haiku-4-5-20251001"


def load_env(path: str | None = None) -> None:
    """Load KEY=VALUE lines from a gitignored .env into os.environ (no overwrite)."""
    p = pathlib.Path(path) if path else (BIN.parent / ".env")
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _llm_scores(candidates: list[dict]) -> list[int]:
    import anthropic

    listing = "\n".join(
        f"{i}. {c['url']} — {c['description']}" for i, c in enumerate(candidates)
    )
    prompt = (
        "Score each link 0-10 for LEARNING/KNOWLEDGE utility to a practitioner "
        "building AI and data systems. High (7-10): concepts, how-tos, tutorials, "
        "GitHub repos, tools, deep technical explainers. Low (0-3): ephemeral news, "
        "product launches, funding/acquisitions, company announcements.\n\n"
        f"{listing}\n\n"
        'Respond with ONLY JSON: {"scores":[{"index":0,"score":7}, ...]}'
    )
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=RANK_MODEL, max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
    data = json.loads(text[text.index("{"): text.rindex("}") + 1])
    scores = {int(s["index"]): int(s["score"]) for s in data["scores"]}
    return [max(0, min(10, scores.get(i, 0))) for i in range(len(candidates))]


def score_candidates(candidates: list[dict]) -> list[int]:
    load_env()
    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            return _llm_scores(candidates)
        except Exception:
            pass
    return [ce.heuristic_score(c["url"], c["description"]) for c in candidates]


def rank(candidates: list[dict], max_links: int = 10, floor: int = 4) -> list[dict]:
    """Score, sort by score desc (stable), then apply quality floor and cap.

    Returns one disposition per candidate:
      {url, description, score, fetch: bool, reason: 'low-utility'|'over-cap'|None}
    """
    if not candidates:
        return []
    scores = score_candidates(candidates)
    ranked = sorted(
        zip(range(len(candidates)), candidates, scores),
        key=lambda t: (-t[2], t[0]),
    )
    out, kept = [], 0
    for _, c, s in ranked:
        d = {"url": c["url"], "description": c["description"], "score": s}
        if s < floor:
            d.update(fetch=False, reason="low-utility")
        elif kept >= max_links:
            d.update(fetch=False, reason="over-cap")
        else:
            d.update(fetch=True, reason=None)
            kept += 1
        out.append(d)
    return out
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_rank_links.py -q`
Expected: 4 passed.

- [ ] **Step 5: Commit**
```bash
git add bin/rank_links.py tests/test_rank_links.py
git commit -m "feat(collect-email): rank_links (Haiku ranking + floor/cap + fallback)"
```

---

## Task 5: `fetch_link.py` — classify + fetch content

**Files:**
- Create: `bin/fetch_link.py`
- Test: `tests/test_fetch_link.py`

- [ ] **Step 1: Write failing tests** (pure functions + article extraction via fixture HTML)

Create `tests/test_fetch_link.py`:
```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import fetch_link as fl  # noqa: E402


def test_youtube_id_variants():
    assert fl.youtube_id("https://www.youtube.com/watch?v=abc123XYZ_-") == "abc123XYZ_-"
    assert fl.youtube_id("https://youtu.be/abc123XYZ_-") == "abc123XYZ_-"
    assert fl.youtube_id("https://example.com/article") is None


def test_classify():
    assert fl.classify("https://youtu.be/abc123XYZ_-") == "youtube"
    assert fl.classify("https://example.com/whitepaper.pdf") == "unsupported"
    assert fl.classify("https://blog.example.com/post") == "article"
    assert fl.classify("ftp://x") == "unsupported"


def test_extract_article_from_html():
    html = (
        "<html><head><title>RAG Patterns</title></head><body>"
        "<article><h1>RAG Patterns</h1>"
        "<p>" + ("Retrieval augmented generation explained in depth. " * 20) + "</p>"
        "</article></body></html>"
    )
    out = fl.extract_article(html, "https://blog.example.com/rag")
    assert out["channel"] == "web"
    assert "Retrieval augmented generation" in out["text"]
    assert out["title"]
```

- [ ] **Step 2: Run to verify they fail**

Run: `python3 -m pytest tests/test_fetch_link.py -q`
Expected: FAIL (`No module named 'fetch_link'`).

- [ ] **Step 3: Implement `bin/fetch_link.py`**

> Transcript API note: written for youtube_transcript_api **1.x** (`YouTubeTranscriptApi().fetch(id)` returning snippet objects with `.text`/`.start`). If Task 1 Step 2 showed only legacy `get_transcript`, replace the body of `fetch_youtube` with: `chunks = YouTubeTranscriptApi.get_transcript(vid)` and iterate dicts `c["text"]` / `c["start"]`.

```python
#!/usr/bin/env python3
"""fetch_link.py — classify a link and fetch its content (article or YouTube)."""
from __future__ import annotations

import re

UA = "corpus-collector/1.0 (+personal archival)"
TIMEOUT = 10.0
MAX_BYTES = 2_000_000

YT_RE = re.compile(
    r"(?i)(?:youtube\.com/watch\?[^ ]*v=|youtu\.be/|youtube\.com/shorts/)"
    r"([A-Za-z0-9_-]{6,})"
)
PDF_RE = re.compile(r"(?i)\.pdf(\?|$)")


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
        return fetch_article(url)
    raise ValueError(f"unsupported url: {url}")
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_fetch_link.py -q`
Expected: 3 passed.

- [ ] **Step 5: Commit**
```bash
git add bin/fetch_link.py tests/test_fetch_link.py
git commit -m "feat(collect-email): fetch_link (classify + article/youtube fetch)"
```

---

## Task 6: Link-file writer + frontmatter patch (in `collect_email.py`)

**Files:**
- Modify: `bin/collect_email.py`
- Test: `tests/test_collect_email.py`

- [ ] **Step 1: Write failing tests**
```python
def test_build_link_document_has_provenance():
    doc = ce.build_link_document(
        {"channel": "web", "source_url": "https://x.example.com/a",
         "via_email": "MSG1", "score": 9, "collected_at": "2026-06-11"},
        "Article body text.",
    )
    assert "channel: web" in doc
    assert "source_url: https://x.example.com/a" in doc
    assert "via_email: MSG1" in doc
    assert "utility_score: 9" in doc
    assert doc.rstrip().endswith("Article body text.")


def test_link_target_slugifies_title(tmp_path):
    p = ce.link_target("RAG Patterns!", tmp_path)
    assert p.name == "rag-patterns.md"


def test_add_links_frontmatter_inserts_block(tmp_path):
    f = tmp_path / "email.md"
    f.write_text("---\nchannel: email\nsubject: Hi\n---\n\nBody\n", encoding="utf-8")
    ce.add_links_frontmatter(str(f), [
        {"url": "https://x.example.com/a", "score": 9, "file": "raw/web/a.md", "reason": None},
        {"url": "https://x.example.com/b", "score": 2, "file": None, "reason": "low-utility"},
    ])
    out = f.read_text(encoding="utf-8")
    assert "links:" in out
    assert "fetched: true" in out and "file: raw/web/a.md" in out
    assert "reason: low-utility" in out
    assert out.index("links:") < out.index("\n---")  # inside frontmatter
    assert out.rstrip().endswith("Body")
```

- [ ] **Step 2: Run to verify they fail**

Run: `python3 -m pytest tests/test_collect_email.py -k "link_document or link_target or links_frontmatter" -q`
Expected: FAIL (attributes not defined).

- [ ] **Step 3: Implement the three functions**

Add to `bin/collect_email.py`:
```python
def build_link_document(meta: dict, text: str) -> str:
    lines = [
        "---",
        f"channel: {meta['channel']}",
        f"source_url: {meta['source_url']}",
        f"via_email: {meta['via_email']}",
        f"utility_score: {meta['score']}",
        f"collected_at: {meta['collected_at']}",
        "---",
        "",
        text.strip(),
        "",
    ]
    return "\n".join(lines)


def link_target(title: str, base_dir: Path, message_hint: str = "") -> Path:
    slug = slugify(title)
    candidate = base_dir / f"{slug}.md"
    if candidate.exists():
        suffix = re.sub(r"[^a-z0-9]+", "", message_hint.lower())[:8] or "x"
        candidate = base_dir / f"{slug}-{suffix}.md"
    return candidate


def add_links_frontmatter(path: str, links: list[dict]) -> None:
    """Insert a `links:` block before the closing `---` of an existing file's
    frontmatter. Each entry is a one-line flow mapping for compactness."""
    p = Path(path)
    content = p.read_text(encoding="utf-8")
    block = ["links:"]
    for d in links:
        parts = [
            f"url: {d['url']}",
            f"fetched: {'true' if d.get('file') else 'false'}",
            f"score: {d.get('score', 0)}",
        ]
        if d.get("file"):
            parts.append(f"file: {d['file']}")
        if d.get("reason"):
            parts.append(f"reason: {d['reason']}")
        block.append("  - {" + ", ".join(parts) + "}")
    closing = content.index("\n---", content.index("---") + 3)
    p.write_text(content[:closing] + "\n" + "\n".join(block) + content[closing:],
                 encoding="utf-8")
```

- [ ] **Step 4: Run to verify pass**

Run: `python3 -m pytest tests/test_collect_email.py -k "link_document or link_target or links_frontmatter" -q`
Expected: 3 passed.

- [ ] **Step 5: Run the FULL suite (regression gate)**

Run: `python3 -m pytest -q`
Expected: all pass (existing 39 + new).

- [ ] **Step 6: Commit**
```bash
git add bin/collect_email.py tests/test_collect_email.py
git commit -m "feat(collect-email): link-file writer + links frontmatter patch"
```

---

## Task 7: Orchestrate enrichment in `gmail_client.py`

**Files:**
- Modify: `bin/gmail_client.py`

- [ ] **Step 1: Add imports + the `enrich_email` helper**

Near the top of `bin/gmail_client.py`, after `import collect_email as ce`:
```python
import rank_links as rl  # noqa: E402
import fetch_link as fl  # noqa: E402

WEB_DIR = ROOT / "raw" / "web"
YT_DIR = ROOT / "raw" / "youtube"
```

Add this function (above `cmd_run`):
```python
def enrich_email(email_path: str, message_id: str, body: str,
                 collected_at: str, max_links: int) -> dict:
    """Follow useful links in one email: select -> rank -> fetch -> write +
    patch the parent email's links: frontmatter. Best-effort; never raises."""
    candidates = ce.select_links(body)
    if not candidates:
        return {"captured": 0, "skipped": 0}
    dispositions = rl.rank(candidates, max_links=max_links, floor=4)
    captured = skipped = 0
    for d in dispositions:
        if not d["fetch"]:
            skipped += 1
            continue
        try:
            resolved = fl.resolve(d["url"])
            kind = fl.classify(resolved)
            if kind == "unsupported":
                d.update(fetch=False, reason="unsupported")
                skipped += 1
                continue
            base = WEB_DIR if kind == "article" else YT_DIR
            base.mkdir(parents=True, exist_ok=True)
            if _url_seen(resolved):
                d.update(fetch=False, reason="duplicate")
                skipped += 1
                continue
            content = fl.fetch(resolved)
            target = ce.link_target(content["title"], base, message_id)
            doc = ce.build_link_document(
                {"channel": content["channel"], "source_url": resolved,
                 "via_email": message_id, "score": d["score"],
                 "collected_at": collected_at},
                content["text"],
            )
            target.write_text(doc, encoding="utf-8")
            d["file"] = str(target.relative_to(ROOT))
            captured += 1
        except Exception:
            d.update(fetch=False, reason="fetch-failed")
            skipped += 1
    try:
        ce.add_links_frontmatter(email_path, dispositions)
    except Exception:
        pass
    return {"captured": captured, "skipped": skipped}


def _url_seen(resolved: str) -> bool:
    """Dedup against source_url already written in any raw/web or raw/youtube file."""
    needle = f"source_url: {resolved}\n"
    for d in (WEB_DIR, YT_DIR):
        if not d.exists():
            continue
        for md in d.glob("*.md"):
            try:
                if needle in md.read_text(encoding="utf-8"):
                    return True
            except (OSError, UnicodeDecodeError):
                continue
    return False
```

> Note: `ce.already_collected` checks the `gmail_message_id` needle, not `source_url`; `_url_seen` is the URL-level dedup. Both are cheap glob scans consistent with the existing dedup style.

- [ ] **Step 2: Wire `enrich_email` into `cmd_run`**

In `cmd_run`, after the block that sets `written`/`dup` and BEFORE the archive step, the body text is `info["body"]` and the written path is `res["path"]`. Replace the archive section so enrichment runs after a confirmed write, then archive. Find:
```python
        # Safety rule: mutate Gmail ONLY after a confirmed write/duplicate.
        if not args.dry_run:
            try:
                archive_message(service, info["message_id"])
                archived += 1
            except Exception:
                pass
```
Replace with (archive first, then enrich — matches the spec's "enrichment runs after archive"):
```python
        # Safety rule: mutate Gmail ONLY after a confirmed write/duplicate.
        if not args.dry_run:
            try:
                archive_message(service, info["message_id"])
                archived += 1
            except Exception:
                pass
        # Enrich with linked content AFTER archive (best-effort; also runs in dry-run).
        if not args.no_links and status == "written":
            e = enrich_email(res["path"], info["message_id"], info["body"],
                             collected_at, args.max_links)
            links_captured += e["captured"]
            links_skipped += e["skipped"]
```

Initialize the two counters with the others at the top of the loop (where `written = dup = failed = archived = 0` is):
```python
    written = dup = failed = archived = 0
    links_captured = links_skipped = 0
```

Add the counters to the final `print(json.dumps({...}))` payload:
```python
        "links_captured": links_captured, "links_skipped": links_skipped,
```

- [ ] **Step 3: Add the `--no-links` and `--max-links` flags**

In `main`, on the `run` subparser (`pr`), add:
```python
    pr.add_argument("--no-links", action="store_true", help="Skip link-following enrichment.")
    pr.add_argument("--max-links", type=int, default=10, help="Max links fetched per email.")
```

- [ ] **Step 4: Smoke-test the CLI wiring (no network)**

Run:
```bash
python3 bin/gmail_client.py run --help
python3 -c "import sys; sys.path.insert(0,'bin'); import gmail_client; print('imports ok')"
```
Expected: help shows `--no-links` and `--max-links`; `imports ok`.

- [ ] **Step 5: Run the full suite**

Run: `python3 -m pytest -q`
Expected: all pass.

- [ ] **Step 6: Commit**
```bash
git add bin/gmail_client.py
git commit -m "feat(collect-email): orchestrate bounded link-following in run"
```

---

## Task 8: Update the skill doc + live verification

**Files:**
- Modify: `.claude/skills/collect-email/SKILL.md`

- [ ] **Step 1: Document link-following in SKILL.md**

In the `## Notes` section, replace the line that begins "This skill does NOT follow links inside emails…" with:
```markdown
- Link-following is ON by default: useful links inside an email are ranked by
  learning-utility (Haiku, heuristic fallback), quality-floored, capped at 10, and
  captured into raw/web / raw/youtube with `via_email` provenance. Disable with
  `--no-links`; change the cap with `--max-links N`. Depth-1 only (links inside
  fetched pages are never followed).
```

- [ ] **Step 2: Live single-email verification (one starred email, dry-run so Gmail is untouched)**

Run:
```bash
python3 bin/gmail_client.py run --dry-run --max 1
```
Expected JSON includes `links_captured` ≥ 0 and `links_skipped` ≥ 0. Inspect any new files under `raw/web/` or `raw/youtube/` for clean extraction + correct `source_url`/`via_email`, and confirm the parent email file in `raw/_inbox/` gained a `links:` block.

- [ ] **Step 3: Commit**
```bash
git add .claude/skills/collect-email/SKILL.md
git commit -m "docs(collect-email): document bounded link-following in skill"
```

---

## Definition of Done

- [ ] `python3 -m pytest -q` green (existing 39 + new ~17).
- [ ] `run --dry-run --max 1` produces a `links:` block on the email and ≥0 link files with correct provenance.
- [ ] News/announcement links are scored low and recorded `low-utility`; links past 10 recorded `over-cap`; PDFs `unsupported`; failures `fetch-failed`.
- [ ] No link discovered inside a fetched page is ever followed (depth-1 holds — there is no recursion in the code).
- [ ] `.env` / OAuth secrets remain gitignored.
