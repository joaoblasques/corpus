#!/usr/bin/env python3
"""github_discover.py — the GitHub analog of book_discover / blog_discover: propose repos for review.

Searches GitHub for the most-starred repos across the corpus's technical domains (the same demand
signal the old auto-star `discover` used) and appends them, pre-ticked, to the vault log
`00_Inbox/Clippings/GitHubs to review.md` — WITHOUT auto-starring, so the user's GitHub stars stay
their own. Entries are pre-approved because `_topic_admits`/`_is_junk`/star+recency thresholds
already do the admission judgment call before a repo is written; the user no longer needs to tick
each one by hand. `promote` reads the `[x]` lines and collects each into the ingest inbox (README +
docs digest), so the normal ingest pipeline picks them up. A seen-ledger makes each repo proposed at
most once; untick a line (`[ ]`) to skip a specific repo before the same nightly run's `promote` step.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
sys.path.insert(0, str(BIN))
import github_client as gh  # noqa: E402
import collect_github as cg  # noqa: E402

LEDGER = ROOT / "raw" / ".github_proposed.txt"
_CLIP = Path.home() / "Dev" / "second-brain" / "00_Inbox" / "Clippings"
REVIEW = Path(os.environ.get("CORPUS_GITHUB_REVIEW", str(_CLIP / "GitHubs to review.md")))

# `- [ ] owner/repo · …` — a review-queue entry; the checked variant is `[x]`.
_REVIEW_REPO_RE = re.compile(r"^- \[[ xX]\]\s+([\w.-]+/[\w.-]+)", re.M)
_REVIEW_CHECKED_RE = re.compile(r"^- \[[xX]\]\s+([\w.-]+/[\w.-]+)", re.M)

REVIEW_HEADER = (
    "# GitHubs to review\n\n"
    "Repos proposed from your technical domains (most-starred first), pre-approved and auto-ingested\n"
    "the same night. Untick a line (`[ ] owner/repo`) before the nightly run to skip it instead.\n"
)


def _ledger() -> set:
    if not LEDGER.exists():
        return set()
    return {ln.strip() for ln in LEDGER.read_text(encoding="utf-8").splitlines() if ln.strip()}


def _mark(fn: str) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(fn + "\n")


def _repos_in_review() -> set:
    if not REVIEW.exists():
        return set()
    return set(_REVIEW_REPO_RE.findall(REVIEW.read_text(encoding="utf-8", errors="ignore")))


def repo_meta(full_name, *, _run=None) -> dict:
    """Full metadata for a repo full_name (description/language/stars/topics); minimal dict on error."""
    p = gh._gh(["api", f"repos/{full_name}"], _run=_run)
    if not p or getattr(p, "returncode", 1) != 0:
        return {"full_name": full_name, "stars": 0}
    try:
        d = json.loads(p.stdout)
    except (json.JSONDecodeError, TypeError):
        return {"full_name": full_name, "stars": 0}
    return {"full_name": d.get("full_name", full_name), "html_url": d.get("html_url"),
            "description": d.get("description") or "", "language": d.get("language") or "",
            "stars": d.get("stargazers_count") or 0, "topics": d.get("topics") or []}


def _stars_h(n: int) -> str:
    return f"{n / 1000:.1f}k" if n >= 1000 else str(n)


# Precise vs broad domain topics. A lone BROAD-only match admits off-domain mega-starred repos
# (apache/dubbo via distributed-systems, files-community/Files via developer-tools, siyuan/GitHubDaily
# too), so a candidate is admitted only if its matched search-topics include ≥1 PRECISE topic OR ≥2
# topics total. Relevance belongs to the generator, not the reviewer (Jonas ticks everything).
_BROAD_TOPICS = {"distributed-systems", "developer-tools", "observability"}
_PRECISE_TOPICS = {t for tt in cg.DOMAIN_TOPICS.values() for t in tt} - _BROAD_TOPICS

# Hard-block only the clearest non-recommendations (leaked/jailbreak prompt dumps). Everything else is
# governed by the topic-admission rule, so a genuine in-domain resource list is NOT blanket-dropped
# just for being an "awesome-*" list.
_JUNK_RE = re.compile(r"(system[\s_-]?prompts?|prompt[\s_-]?leak|jailbreak|\bleaked?\b)", re.I)


def _topic_admits(hit_topics) -> bool:
    """Admit only if the candidate's matched search-topics include ≥1 precise domain topic OR ≥2
    topics total — a single broad-topic match (distributed-systems / developer-tools) is dropped."""
    hit = {str(t).lower() for t in hit_topics}
    return len(hit & _PRECISE_TOPICS) >= 1 or len(hit) >= 2


def _is_junk(meta: dict) -> bool:
    topics = {str(t).lower() for t in (meta.get("topics") or [])}
    hay = f"{meta.get('full_name', '')} {meta.get('description', '')} {' '.join(topics)}"
    return bool(_JUNK_RE.search(hay))


_SCAN_CAP = 120  # hard bound on candidates examined per run (each needs one metadata fetch)


def cmd_propose(args) -> int:
    """Search corpus-domain repos and append the freshest to the review queue (no auto-star)."""
    if not gh.gh_available():
        print(json.dumps({"status": "not configured", "proposed": 0}))
        return 0
    pushed_after = (datetime.date.today()
                    - datetime.timedelta(days=cg.DISCOVER_PUSHED_WITHIN_DAYS)).isoformat()
    candidates: dict = {}   # fn -> {"stars": int, "topics": set}  (which of OUR topics it matched)
    for topic in cg.discover_topics():
        for repo in gh.search_repos(topic, min_stars=cg.DISCOVER_MIN_STARS, pushed_after=pushed_after):
            fn = repo["full_name"]
            c = candidates.setdefault(fn, {"stars": 0, "topics": set()})
            c["stars"] = max(c["stars"], repo["stars"])
            c["topics"].add(topic)
    starred = {r["full_name"] for r in gh.list_starred() if r.get("full_name")}
    fresh = sorted(((fn, c) for fn, c in candidates.items()
                    if fn not in starred and not cg.already_collected(fn)),
                   key=lambda kv: -kv[1]["stars"])

    seen = _ledger() | _repos_in_review()
    picks = []  # (full_name, stars, meta) — meta carried so the line-builder needn't re-fetch
    for i, (fn, c) in enumerate(fresh):
        if len(picks) >= args.max or i >= _SCAN_CAP:
            break
        if fn in seen or not _topic_admits(c["topics"]):   # drop lone-broad-topic off-domain repos
            continue
        meta = repo_meta(fn)
        if _is_junk(meta):                                 # drop the clearest non-recs (leaks/jailbreak)
            continue
        seen.add(fn)
        picks.append((fn, c["stars"], meta))

    if picks and not args.dry_run:
        REVIEW.parent.mkdir(parents=True, exist_ok=True)
        body = REVIEW.read_text(encoding="utf-8") if REVIEW.exists() else REVIEW_HEADER
        lines = []
        for fn, stars, meta in picks:
            lang = meta.get("language") or ""
            desc = (meta.get("description") or "")[:90]
            tag = f" · {lang}" if lang else ""
            lines.append(f"- [x] {fn} · ★{_stars_h(stars)}{tag} · {desc}".rstrip(" ·"))
        REVIEW.write_text(body.rstrip() + "\n" + "\n".join(lines) + "\n", encoding="utf-8")
        for fn, _, _ in picks:
            _mark(fn)
    print(json.dumps({"proposed": len(picks), "top": [fn for fn, _, _ in picks[:8]],
                      "dry_run": bool(args.dry_run)}, indent=2))
    return 0


def cmd_promote(args) -> int:
    """Collect each `[x]`-ticked review repo into the ingest inbox (README + docs digest)."""
    if not REVIEW.exists():
        print(json.dumps({"promoted": 0, "note": "no review file"}))
        return 0
    if not gh.gh_available():
        print(json.dumps({"status": "not configured", "promoted": 0}))
        return 0
    checked = _REVIEW_CHECKED_RE.findall(REVIEW.read_text(encoding="utf-8", errors="ignore"))
    at = datetime.date.today().isoformat()
    written = dup = 0
    done = []
    for fn in checked:
        if cg.already_collected(fn):
            dup += 1
            continue
        if args.dry_run:
            written += 1
            done.append(fn)
            continue
        try:
            res = cg.write_collected(gh.fetch_repo(repo_meta(fn), max_docs=args.max_docs),
                                     collected_at=at)
        except Exception:  # noqa: BLE001 — one bad repo must not sink the batch
            continue
        if res.get("status") == "written":
            written += 1
            done.append(fn)
        else:
            dup += 1
    print(json.dumps({"promoted": written, "duplicate": dup, "repos": done[:8],
                      "dry_run": bool(args.dry_run)}, indent=2))
    return 0


def _args(argv):
    p = argparse.ArgumentParser(description="Discover + promote GitHub repos for corpus ingestion.")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("propose", help="Propose top corpus-domain repos into the review queue.")
    c.add_argument("--max", type=int, default=15)
    c.add_argument("--dry-run", action="store_true")
    c.set_defaults(func=cmd_propose)
    pr = sub.add_parser("promote", help="Collect [x]-ticked review repos into the ingest inbox.")
    pr.add_argument("--max-docs", type=int, default=8)
    pr.add_argument("--dry-run", action="store_true")
    pr.set_defaults(func=cmd_promote)
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = _args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
