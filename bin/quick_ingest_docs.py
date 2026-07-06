#!/usr/bin/env python3
"""quick_ingest_docs.py — fast "quick intake" of already-fetched web/notes stubs.

The raw/_inbox backlog is dominated by content-bearing stubs (vault clippings, blog/
article scrapes, first-party notes) that the slow ~6/night headless-claude ingest can't
keep up with. This drains them the same way quick_ingest_youtube drains videos: each
content stub -> ONE lightweight `source` page (LLM summary: domain + 2-3 sentence
what-it-covers + topics + pointer-back URL), skipping the full §8.1 cascade.

Backends: OpenRouter FREE models (default, so bulk drain costs nothing) with a Groq
fallback. Thin/URL-only stubs (no fetched body yet) are skipped — they need a fetch pass
first. Resumable (skips corpus_ingested). Excludes nothing by channel here; caller scopes
via --channel.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import time
from pathlib import Path

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
sys.path.insert(0, str(BIN))
import quick_ingest_youtube as qy  # reuse DOMAINS, _slug, _one_line, _index_append, _fallback_domain  # noqa: E402

INBOX = ROOT / "raw" / "_inbox"
WEB_CHANNEL = ROOT / "raw" / "web"
NOTES_CHANNEL = ROOT / "raw" / "notes"
CORPUS = ROOT / "corpus"

DOMAINS = qy.DOMAINS
MIN_WORDS = 120           # below this a stub is treated as thin/URL-only -> skip

# Free OpenRouter models (bulk drain costs nothing). First that the account can use wins;
# override with --model. These rotate over time — --model lets you pin a current one.
OPENROUTER_FREE_DEFAULT = "meta-llama/llama-3.3-70b-instruct:free"


def _openrouter_key(env_file="~/.config/watch/.env") -> str | None:
    k = os.environ.get("OPENROUTER_API_KEY")
    if k:
        return k
    for p in (ROOT / ".env", Path(os.path.expanduser(env_file))):
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("OPENROUTER_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'") or None
    return None


def _front(text: str, key: str) -> str | None:
    m = re.search(rf"^{re.escape(key)}:[^\S\n]*(.+)$", text, re.M)
    return m.group(1).strip() if m else None


def _body(text: str) -> str:
    parts = text.split("---", 2)
    return parts[2] if len(parts) == 3 else text


def _plain(body: str, max_words: int = 2500) -> str:
    return " ".join(re.sub(r"\s+", " ", body).strip().split()[:max_words])


def _prompt(title: str, source: str, content: str) -> str:
    return (
        "You are indexing a document into a personal knowledge corpus. "
        f"Available domains: {', '.join(DOMAINS)}.\n"
        f"Title: {title}\nSource: {source}\n"
        f"Content (may be truncated):\n{content}\n\n"
        "Return STRICT JSON with keys: "
        '"domain" (exactly one of the available domains, best fit), '
        '"summary" (2-3 plain sentences on what the document covers and its key takeaway), '
        '"topics" (3-6 short topic/entity strings). No prose outside the JSON.'
    )


def _parse(data: dict, fallback_domain: str) -> dict:
    dom = data.get("domain") if data.get("domain") in DOMAINS else fallback_domain
    topics = [str(t).strip() for t in (data.get("topics") or []) if str(t).strip()][:6]
    return {"domain": dom, "summary": str(data.get("summary") or "").strip(), "topics": topics}


def _llm_summary(title: str, source: str, content: str, *, backend: str, model: str,
                 fallback_domain: str, attempts: int = 4) -> dict:
    """One cheap LLM call -> {domain, summary, topics}. backend: openrouter|groq.
    Retries on 429/transient errors with backoff. Raises after `attempts`."""
    import requests
    if backend == "openrouter":
        url = "https://openrouter.ai/api/v1/chat/completions"
        key = _openrouter_key()
        if not key:
            raise RuntimeError("OPENROUTER_API_KEY not set")
        headers = {"Authorization": f"Bearer {key}",
                   "HTTP-Referer": "https://github.com/joaoblasques/corpus",
                   "X-Title": "corpus-quick-intake"}
    else:  # groq
        url = "https://api.groq.com/openai/v1/chat/completions"
        key = qy.yc._groq_key()
        headers = {"Authorization": f"Bearer {key}"}

    payload = {"model": model, "temperature": 0.2, "max_tokens": 400,
               "response_format": {"type": "json_object"},
               "messages": [{"role": "user", "content": _prompt(title, source, content)}]}
    last = None
    for i in range(attempts):
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=90)
            if r.status_code == 429:
                time.sleep(min(float(r.headers.get("retry-after", 0)) or 3.0 * (i + 1), 30))
                continue
            r.raise_for_status()
            content_out = r.json()["choices"][0]["message"]["content"]
            data = json.loads(content_out)
            info = _parse(data, fallback_domain)
            if info["summary"]:
                return info
            last = ValueError("empty summary")
        except Exception as e:  # noqa: BLE001
            last = e
        time.sleep(1.5 * (i + 1))
    raise last or RuntimeError("llm failed")


def _source_page(meta: dict, info: dict, today: str) -> str:
    topics = "\n".join(f"- {t}" for t in info["topics"]) or "- (none extracted)"
    url = meta.get("url") or ""
    link = f"[open source]({url})" if url else f"raw stub: `{meta['stub_name']}`"
    origin = meta.get("origin", meta.get("channel", "web"))
    return f"""---
type: source
domain: {info['domain']}
status: stub
sources:
  - path: raw/{meta['channel_dir']}/{meta['stub_name']}
    channel: {meta['channel']}
    ingested_at: {today}
aliases: []
tags:
  - corpus/{info['domain']}
  - source
  - doc-quick-intake
created: {today}
updated: {today}
provisional: false
url: {url}
origin: {origin}
---

# {meta['title']}

> **Quick intake** ({origin}). {link}

{info['summary']}

**Key topics**
{topics}
"""


def iter_stubs(channels: set[str], sources: set[str] | None):
    for f in sorted(INBOX.glob("*.md")):
        if f.name.startswith("youtube-"):
            continue
        text = f.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"^corpus_ingested:\s*true", text, re.M):
            continue
        ch = _front(text, "channel")
        if channels and ch not in channels:
            continue
        if sources is not None and (_front(text, "source") or "") not in sources:
            continue
        yield f, text, ch


def _stamp(text: str, today: str, page: str) -> str:
    stamp = f"corpus_ingested: true\ncorpus_ingested_at: {today}\ncorpus_pages:\n  - {page}\n"
    m = re.match(r"^(---\n.*?\n)(---\n)(.*)$", text, re.S)
    return m.group(1) + stamp + m.group(2) + m.group(3) if m else text


def process(f: Path, text: str, ch: str, *, backend: str, model: str, today: str,
            dry_run: bool) -> str:
    body = _body(text)
    if len(body.split()) < MIN_WORDS:
        return "skipped_thin"
    title = _front(text, "title") or f.stem
    url = _front(text, "source_url") or _front(text, "url") or ""
    origin = _front(text, "source") or ch or "web"
    fb = qy._fallback_domain(title + " " + origin)
    info = None
    # Try the requested backend; if OpenRouter's free model is rate-limited (frequent),
    # fall back to Groq's free tier so the drain stays reliable AND free.
    # (backend, model, attempts): try OpenRouter free briefly (fail fast on 429),
    # then fall back to Groq free with more retries for reliability.
    plan = [(backend, model, 2)]
    if backend == "openrouter":
        plan.append(("groq", "llama-3.1-8b-instant", 4))
    for bk, md, att in plan:
        try:
            info = _llm_summary(title, origin, _plain(body), backend=bk, model=md,
                                fallback_domain=fb, attempts=att)
            break
        except Exception:
            continue
    if info is None:
        return "llm_fail"
    slug = qy._slug(title, re.sub(r"[^a-f0-9]", "", f.stem.split("-")[-1])[:8] or "doc")
    channel_dir = "web" if ch == "web" else ("notes" if ch == "notes" else (ch or "web"))
    meta = {"title": title, "url": url, "origin": origin, "channel": ch or "web",
            "channel_dir": channel_dir, "stub_name": f.name}
    if dry_run:
        return f"DRY {info['domain']}/{slug}"
    dest = CORPUS / info["domain"] / "sources" / f"{slug}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(_source_page(meta, info, today), encoding="utf-8")
    qy._index_append(info["domain"], slug, title, qy._one_line(info["summary"]))
    dest_channel = ROOT / "raw" / channel_dir
    dest_channel.mkdir(parents=True, exist_ok=True)
    (dest_channel / f.name).write_text(_stamp(text, today, f"corpus/{info['domain']}/sources/{slug}.md"),
                                       encoding="utf-8")
    f.unlink(missing_ok=True)
    return f"ok:{info['domain']}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Quick-intake web/notes stubs into source pages.")
    ap.add_argument("--max", type=int, default=None)
    ap.add_argument("--channel", default="web,notes", help="comma-separated channels to process")
    ap.add_argument("--source", default=None, help="comma-separated `source:` values to restrict to")
    ap.add_argument("--backend", choices=["openrouter", "groq"], default="openrouter")
    ap.add_argument("--model", default=None, help="model id (default: free OpenRouter / groq 8b-instant)")
    ap.add_argument("--sleep", type=float, default=0.5)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    model = args.model or (OPENROUTER_FREE_DEFAULT if args.backend == "openrouter"
                           else "llama-3.1-8b-instant")
    channels = {c.strip() for c in args.channel.split(",") if c.strip()}
    sources = ({s.strip() for s in args.source.split(",")} if args.source else None)
    today = datetime.date.today().isoformat()
    tally = {"ok": 0, "skipped_thin": 0, "llm_fail": 0}
    processed = 0
    for f, text, ch in iter_stubs(channels, sources):
        if args.max and processed >= args.max:
            break
        res = process(f, text, ch, backend=args.backend, model=model, today=today,
                      dry_run=args.dry_run)
        processed += 1
        key = "ok" if res.startswith(("ok:", "DRY")) else res
        tally[key] = tally.get(key, 0) + 1
        print(json.dumps({"stub": f.name, "result": res}), flush=True)
        if not args.dry_run and args.sleep and res.startswith("ok:"):
            time.sleep(args.sleep)
    print(json.dumps({"tally": tally, "processed": processed, "backend": args.backend, "model": model}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
