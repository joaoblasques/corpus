#!/usr/bin/env python3
"""github_discover.py — the GitHub analog of book_discover / blog_discover: propose repos for review.

Searches GitHub for the most-starred repos across the corpus's technical domains (the same demand
signal the old auto-star `discover` used) and appends them to the vault review queue
`00_Inbox/Clippings/GitHubs to review.md` (phone-tickable) — WITHOUT auto-starring, so the user's
GitHub stars stay their own. `promote` reads the `[x]`-ticked ones and collects each into the ingest
inbox (README + docs digest), so the normal ingest pipeline picks them up. A seen-ledger makes each
repo proposed at most once.
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
    "Repos proposed from your technical domains (most-starred first). Tick `[x]` the ones worth\n"
    "ingesting; the nightly then collects each into the corpus (README + docs) and processes it.\n"
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


# Relevance vocabulary = the corpus's own domain topics (a repo must actually carry one of these
# to count as genuinely on-topic — GitHub's fuzzy topic search otherwise drags in tangential repos).
_RELEVANT_TOPICS = {t for topics in cg.DOMAIN_TOPICS.values() for t in topics}

# Never surface: leaked/jailbreak prompt dumps, curation lists, career/interview prep, roadmaps —
# low-signal for a knowledge corpus even when they rank high by stars.
_JUNK_RE = re.compile(
    r"(system[\s_-]?prompts?|prompt[\s_-]?leak|jailbreak|\bleaked?\b|awesome[\s_-]|"
    r"roadmap|cheat[\s_-]?sheet|interview|curated|\bawesome\b|good[\s_-]?first[\s_-]?issue)",
    re.I,
)


def _relevant(meta: dict) -> bool:
    """True if a repo is genuinely corpus-relevant: it carries at least one corpus-domain topic
    AND is not a curation / leaked-prompt / career-prep repo."""
    topics = {str(t).lower() for t in (meta.get("topics") or [])}
    haystack = f"{meta.get('full_name', '')} {meta.get('description', '')} {' '.join(topics)}"
    if _JUNK_RE.search(haystack):
        return False
    return bool(topics & _RELEVANT_TOPICS)


_SCAN_CAP = 120  # hard bound on candidates examined per run (each needs one metadata fetch)


def cmd_propose(args) -> int:
    """Search corpus-domain repos and append the freshest to the review queue (no auto-star)."""
    if not gh.gh_available():
        print(json.dumps({"status": "not configured", "proposed": 0}))
        return 0
    pushed_after = (datetime.date.today()
                    - datetime.timedelta(days=cg.DISCOVER_PUSHED_WITHIN_DAYS)).isoformat()
    candidates: dict = {}
    for topic in cg.discover_topics():
        for repo in gh.search_repos(topic, min_stars=cg.DISCOVER_MIN_STARS, pushed_after=pushed_after):
            fn = repo["full_name"]
            candidates[fn] = max(candidates.get(fn, 0), repo["stars"])
    starred = {r["full_name"] for r in gh.list_starred() if r.get("full_name")}
    fresh = cg.rank_candidates(candidates, starred, cg.already_collected)

    seen = _ledger() | _repos_in_review()
    picks = []  # (full_name, stars, meta) — meta carried so the line-builder needn't re-fetch
    for i, (fn, stars) in enumerate(fresh):
        if len(picks) >= args.max or i >= _SCAN_CAP:
            break
        if fn in seen:
            continue
        meta = repo_meta(fn)
        if not _relevant(meta):        # drop off-topic + junk (leaks, awesome-lists, roadmaps)
            continue
        seen.add(fn)
        picks.append((fn, stars, meta))

    if picks and not args.dry_run:
        REVIEW.parent.mkdir(parents=True, exist_ok=True)
        body = REVIEW.read_text(encoding="utf-8") if REVIEW.exists() else REVIEW_HEADER
        lines = []
        for fn, stars, meta in picks:
            lang = meta.get("language") or ""
            desc = (meta.get("description") or "")[:90]
            tag = f" · {lang}" if lang else ""
            lines.append(f"- [ ] {fn} · ★{_stars_h(stars)}{tag} · {desc}".rstrip(" ·"))
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
