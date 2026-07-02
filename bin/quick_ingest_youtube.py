#!/usr/bin/env python3
"""quick_ingest_youtube.py — fast, low-ceremony "quick intake" of YouTube stubs.

Turns each *tech* stub in raw/_inbox/ (playlist in the collect-remove set) into ONE
lightweight `source` page: domain + 2-3 sentence summary + key topics (via Groq, cheap),
the transcript link, and the video URL. Queryable via _index.md, points back via URL.

This deliberately SKIPS the full §8.1 entity/concept cascade — it trades depth for
throughput to drain a large backlog (user directive 2026-07-02: "quick intake of what the
video is, so a query can point back to the video"). Excluded playlists (music/skate/
exercise = collect-keep/ignore) are never touched.

Blocked stubs get their transcript rescued first (captions, paced for the ~44-pull
rate-limit via --rescue-max). No captions -> a metadata-only page still lands (title +
playlist + URL = pointer-back). Resumable: stubs already stamped corpus_ingested are skipped.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
sys.path.insert(0, str(BIN))
import youtube_client as yc  # noqa: E402
import collect_youtube as cy  # noqa: E402

INBOX = ROOT / "raw" / "_inbox"
YT_CHANNEL = ROOT / "raw" / "youtube"
CORPUS = ROOT / "corpus"
INDEX = CORPUS / "_index.md"
PLAYLISTS_CFG = BIN / "youtube_playlists.yaml"

# The corpus's real domains (keep in sync with corpus/_domains.md + the corpus/ folders).
DOMAINS = ["ai-engineering", "data-engineering", "software-engineering", "mlops",
           "ai-business", "productivity", "blockchain", "trading"]

# Keyword fallback routing (used when there is no transcript to send to the LLM).
_KW_DOMAIN = [
    ("ai-business", ["business", "marketing", "sales", "startup", "freelanc", "agency",
                     "affiliate", "revenue", "passive income", "side hustle", "money",
                     "saas", "appsumo", "customers", "growth"]),
    ("productivity", ["productivity", "workflow", "habit", "note-taking", "second brain",
                      "2nd brain", "obsidian", "getting things done", "focus", "tutorial phase"]),
    ("ai-engineering", ["ai ", "agent", "claude", "llm", "prompt", "machine learning",
                        "notebooklm", "agentic", "wiki"]),
    ("data-engineering", ["data analy", "data engineering", "databricks", "data "]),
    ("mlops", ["aws", "azure", "gcp", "cloud", "devops", "linux", "mac ", "dev setup", "docker"]),
    ("trading", ["trading", "btc", "invest", "finance", "game theory"]),
    ("software-engineering", ["python", "javascript", "go", "git", "vim", "api",
                              "system design", "software", "tui", "maths", "math"]),
]


def tech_playlists() -> set[str]:
    import yaml
    d = yaml.safe_load(PLAYLISTS_CFG.read_text(encoding="utf-8"))
    return {p["name"] for p in d.get("playlists", []) if p.get("policy") == "collect-remove"}


def _front(text: str, key: str) -> str | None:
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else None


def _plain_transcript(body: str, max_words: int = 1200) -> str:
    """Strip the timestamp-link markdown to plain prose and cap length for the LLM."""
    # drop the provenance marker line and the [mm:ss](url) anchors, keep the words
    body = re.sub(r"^>\s*_Transcript source.*$", "", body, flags=re.M)
    body = re.sub(r"\[\d{1,2}:\d{2}(?::\d{2})?\]\(https?://[^)]+\)", "", body)
    words = re.sub(r"\s+", " ", body).strip().split()
    return " ".join(words[:max_words])


def _fallback_domain(playlist: str) -> str:
    p = (playlist or "").lower()
    for dom, kws in _KW_DOMAIN:
        if any(k in p for k in kws):
            return dom
    return "ai-engineering"


def _groq_summary(title: str, playlist: str, transcript: str, model: str,
                  attempts: int = 4) -> dict:
    """One cheap Groq call -> {domain, summary, topics}. Retries on 429/transient errors
    with backoff (the free tier has a tokens-per-minute cap). Raises after `attempts`."""
    import time
    import requests
    key = yc._groq_key()
    prompt = (
        "You are indexing a YouTube video into a personal knowledge corpus. "
        f"Available domains: {', '.join(DOMAINS)}.\n"
        f"Video title: {title}\nPlaylist: {playlist}\n"
        f"Transcript (may be partial):\n{transcript}\n\n"
        "Return STRICT JSON with keys: "
        '"domain" (exactly one of the available domains, best fit), '
        '"summary" (2-3 plain sentences on what the video covers and its key takeaway), '
        '"topics" (3-6 short topic/entity strings). No prose outside the JSON.'
    )
    last = None
    for i in range(attempts):
        try:
            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json={"model": model, "messages": [{"role": "user", "content": prompt}],
                      "temperature": 0.2, "response_format": {"type": "json_object"},
                      "max_tokens": 400},
                timeout=60,
            )
            if r.status_code == 429:
                wait = float(r.headers.get("retry-after", 0)) or (2.0 * (i + 1))
                time.sleep(min(wait, 30))
                continue
            r.raise_for_status()
            data = json.loads(r.json()["choices"][0]["message"]["content"])
            dom = data.get("domain") if data.get("domain") in DOMAINS else _fallback_domain(playlist)
            topics = [str(t).strip() for t in (data.get("topics") or []) if str(t).strip()][:6]
            summary = str(data.get("summary") or "").strip()
            if summary:
                return {"domain": dom, "summary": summary, "topics": topics}
            last = ValueError("empty summary")
        except Exception as e:  # noqa: BLE001
            last = e
        time.sleep(1.5 * (i + 1))
    raise last or RuntimeError("groq failed")


def _slug(title: str, vid: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (title or "").lower()).strip("-")[:60]
    return f"{s or 'video'}-{vid}"


def _source_page(meta: dict, info: dict, has_transcript: bool, today: str) -> str:
    topics = "\n".join(f"- {t}" for t in info["topics"]) or "- (none extracted)"
    tstatus = meta["transcript_status"]
    src_line = (f"  - path: raw/youtube/{meta['stub_name']}\n"
                f"    channel: youtube\n    ingested_at: {today}\n")
    body_summary = info["summary"] or f"[quick intake — no transcript] {meta['title']}"
    link = (f"[watch on YouTube]({meta['url']})"
            if not has_transcript else
            f"[watch on YouTube]({meta['url']}) · [transcript](../../../raw/youtube/{meta['stub_name']})")
    return f"""---
type: source
domain: {info['domain']}
status: stub
sources:
{src_line}aliases: []
tags:
  - corpus/{info['domain']}
  - source
  - youtube-quick-intake
created: {today}
updated: {today}
provisional: false
youtube_video_id: {meta['video_id']}
url: {meta['url']}
channel_name: {meta['channel_name']}
playlist: {meta['playlist']}
published: {meta['published']}
transcript_status: {tstatus}
---

# {meta['title']}

> **Quick intake** (YouTube · {meta['channel_name']} · playlist _{meta['playlist']}_). {link}

{body_summary}

**Key topics**
{topics}
"""


def _index_append(domain: str, slug: str, title: str, one_line: str) -> None:
    """Append a source entry under the domain section of _index.md (best-effort)."""
    if not INDEX.exists():
        return
    text = INDEX.read_text(encoding="utf-8")
    bullet = f"- [[{domain}/sources/{slug}|{title}]] — source · stub · {one_line}"
    header = f"### {domain}"
    lines = text.splitlines()
    out, inserted = [], False
    for i, ln in enumerate(lines):
        out.append(ln)
        if ln.strip() == header and not inserted:
            out.append(bullet)
            inserted = True
    if not inserted:
        # domain section absent: add it under "## Domains" (or at end)
        out.append("")
        out.append(header)
        out.append(bullet)
    INDEX.write_text("\n".join(out) + ("\n" if not text.endswith("\n") else ""), encoding="utf-8")


def _one_line(summary: str) -> str:
    s = re.sub(r"\s+", " ", summary).strip()
    return (s[:100] + "…") if len(s) > 100 else (s or "quick intake")


def iter_tech_stubs(tech: set[str], ready_only: bool = False):
    for f in sorted(INBOX.glob("youtube-*.md")):
        text = f.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"^corpus_ingested:\s*true", text, re.M):
            continue
        pl = _front(text, "playlist")
        if pl not in tech:
            continue
        if ready_only and (_front(text, "transcript_status") or "") != "ok":
            continue
        yield f, text, pl


def process_stub(f: Path, text: str, playlist: str, *, model: str, rescue: bool,
                 today: str, dry_run: bool, whisper: bool = False) -> str:
    vid = _front(text, "youtube_video_id") or ""
    if not vid:
        return "no_id"
    tstatus = _front(text, "transcript_status") or "none"
    body = text.split("---", 2)[-1]
    has_transcript = tstatus == "ok" and "_No transcript available._" not in body

    # Acquire a transcript for any stub that lacks one. Captions first (fast, free);
    # if they miss for ANY reason, Whisper (audio->Groq) is a different, uncapped surface
    # that transcribes the audio regardless of caption availability. Never write a
    # permanent metadata-only page for a rate-limited stub on a guess:
    #   - no rescue budget           -> skip (leave in inbox for a rescue window)
    #   - captions ok                -> fold transcript in, summarize
    #   - captions miss + whisper on -> Whisper the audio (or skipped_whisperfail)
    #   - captions `blocked` no whisper -> rate-limited: skip (retry a future window)
    #   - captions none_found/disabled, no whisper -> caption-less: metadata-only page
    if not has_transcript:
        if not rescue:
            return "skipped_norescue"
        tbody, tst = yc._caption_transcript(vid)
        if tst == "ok" and tbody:
            body = "\n\n" + tbody
            has_transcript, tstatus = True, "ok"
        elif whisper:
            wbody = yc._whisper_transcript(vid)
            if wbody:
                body = "\n\n" + wbody
                has_transcript, tstatus = True, "ok"
            else:
                return "skipped_whisperfail"
        elif tst == "blocked":
            return "skipped_ratelimit"

    meta = {
        "video_id": vid, "url": _front(text, "url") or f"https://youtu.be/{vid}",
        "title": _front(text, "title") or vid,
        "channel_name": _front(text, "channel_name") or "",
        "playlist": playlist, "published": _front(text, "published") or "",
        "transcript_status": tstatus, "stub_name": f.name,
    }

    if has_transcript:
        try:
            info = _groq_summary(meta["title"], playlist, _plain_transcript(body), model)
        except Exception:
            info = {"domain": _fallback_domain(playlist), "summary": "", "topics": []}
    else:
        info = {"domain": _fallback_domain(playlist), "summary": "", "topics": []}

    slug = _slug(meta["title"], vid)
    page = _source_page(meta, info, has_transcript, today)
    if dry_run:
        return f"DRY {info['domain']}/{slug} (transcript={has_transcript})"

    dest = CORPUS / info["domain"] / "sources" / f"{slug}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page, encoding="utf-8")
    _index_append(info["domain"], slug, meta["title"], _one_line(info["summary"]))

    # stamp + move stub out of the inbox
    stamped = _stamp(text, today, f"corpus/{info['domain']}/sources/{slug}.md",
                     new_transcript=body if has_transcript and tstatus == "ok" else None)
    YT_CHANNEL.mkdir(parents=True, exist_ok=True)
    (YT_CHANNEL / f.name).write_text(stamped, encoding="utf-8")
    f.unlink()
    return f"ok:{info['domain']}" + ("+transcript" if has_transcript else "+metaonly")


def _stamp(text: str, today: str, page: str, new_transcript: str | None) -> str:
    """Add corpus_ingested stamp fields; optionally fold a freshly-rescued transcript in."""
    if new_transcript is not None:
        # swap the "_No transcript available._" placeholder body for the transcript, and
        # mark the frontmatter transcript_status: ok so the moved stub reads accurately.
        parts = text.split("---", 2)
        if len(parts) == 3:
            fm = re.sub(r"^transcript_status:\s*\S+", "transcript_status: ok", parts[1], flags=re.M)
            text = f"---{fm}---\n{new_transcript.strip()}\n"
    stamp = (f"corpus_ingested: true\ncorpus_ingested_at: {today}\n"
             f"corpus_pages:\n  - {page}\n")
    # insert stamp before the closing frontmatter delimiter
    m = re.match(r"^(---\n.*?\n)(---\n)(.*)$", text, re.S)
    if m:
        return m.group(1) + stamp + m.group(2) + m.group(3)
    return text


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Quick-intake YouTube tech stubs into source pages.")
    ap.add_argument("--max", type=int, default=None, help="cap stubs processed this run")
    ap.add_argument("--model", default="llama-3.1-8b-instant", help="Groq model for summaries")
    ap.add_argument("--rescue", action="store_true",
                    help="rescue blocked-stub transcripts via captions (paced by --rescue-max)")
    ap.add_argument("--whisper", action="store_true",
                    help="when captions are rate-limited, fall back to Whisper (audio->Groq, "
                         "uncapped but ~80s/video + Groq cost). Implies unlimited rescue.")
    ap.add_argument("--rescue-max", type=int, default=30,
                    help="cap caption rescues this run (rate-limit budget)")
    ap.add_argument("--sleep", type=float, default=1.0,
                    help="seconds between videos (stay under Groq tokens-per-minute)")
    ap.add_argument("--ready-only", action="store_true",
                    help="only process stubs that already have transcript_status: ok (no rescue, no rate-limit)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    import time

    tech = tech_playlists()
    today = datetime.date.today().isoformat()
    tally = {"ok_transcript": 0, "ok_metaonly": 0, "no_id": 0, "rescued": 0,
             "skipped_ratelimit": 0, "skipped_norescue": 0, "skipped_whisperfail": 0}
    # --whisper implies rescue is on and uncapped (Whisper bypasses the caption cap).
    rescue_on = args.rescue or args.whisper
    rescue_cap = 10**9 if args.whisper else args.rescue_max
    rescued = 0
    processed = 0
    consec_ratelimit = 0
    for f, text, pl in iter_tech_stubs(tech, ready_only=args.ready_only):
        if args.max and processed >= args.max:
            break
        allow_rescue = rescue_on and rescued < rescue_cap
        was_blocked = (_front(text, "transcript_status") or "") == "blocked"
        res = process_stub(f, text, pl, model=args.model, rescue=allow_rescue,
                           today=today, dry_run=args.dry_run, whisper=args.whisper)
        processed += 1
        if res.startswith("ok:"):
            consec_ratelimit = 0
            if "+transcript" in res:
                tally["ok_transcript"] += 1
                if was_blocked and allow_rescue:
                    rescued += 1
            else:
                tally["ok_metaonly"] += 1
        elif res in tally:
            tally[res] += 1
        elif res == "no_id":
            tally["no_id"] += 1
        if res == "skipped_ratelimit":
            consec_ratelimit += 1
        else:
            consec_ratelimit = 0
        print(json.dumps({"stub": f.name, "result": res}), flush=True)
        # captions are IP-rate-limited; without a Whisper fallback, once blocking starts
        # every further caption rescue fails too — stop churning after 3 in a row.
        if consec_ratelimit >= 3 and not args.whisper:
            print(json.dumps({"note": "caption rate-limit hit — stopping (retry next window)"}),
                  flush=True)
            break
        if not args.dry_run and args.sleep and res.startswith("ok:"):
            time.sleep(args.sleep)
    tally["rescued"] = rescued
    print(json.dumps({"tally": tally, "processed": processed}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
