#!/usr/bin/env python3
"""consolidate_run.py — orchestrate cluster -> triage -> synthesize -> critic -> stamp/revert.

Mirrors gardener.py (headless claude via scheduled_run.CLAUDE_BIN; fail-closed Sonnet critic
reused from gardener._critic_call). Weekly, Opus writer. Spec: docs/superpowers/specs/
2026-07-11-consolidation-job-design.md
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
import scheduled_run as sr  # noqa: E402
import consolidate as co  # noqa: E402
import consolidate_prompts as cp  # noqa: E402
import gardener as gd  # noqa: E402 — reuse the fail-closed provenance critic

ROOT = sr.ROOT
CORPUS = ROOT / "corpus"
REVIEW = ROOT / "raw" / "_consolidation_review.md"
LOCK = ROOT / "raw" / ".consolidate.lock"
CONSOLIDATE_MODEL = os.environ.get("CONSOLIDATE_MODEL", "claude-opus-4-8")
CONSOLIDATE_TRIAGE_MODEL = os.environ.get("CONSOLIDATE_TRIAGE_MODEL", "claude-sonnet-4-6")


def _headless(prompt: str, model: str, tools: list[str], *, _run=None) -> str:
    """Run a headless claude call; return the JSON-mode `result` string ('' on failure)."""
    run = _run if _run is not None else subprocess.run
    cmd = [str(sr.CLAUDE_BIN), "--print", prompt, "--output-format", "json",
           "--permission-mode", "bypassPermissions", "--allowedTools", *tools,
           "--model", model]
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    try:
        proc = run(cmd, capture_output=True, text=True, timeout=600, env=env,
                   stdin=subprocess.DEVNULL)
        if proc.returncode != 0:
            return ""
        return json.loads(proc.stdout).get("result", "")
    except Exception:  # noqa: BLE001
        return ""


def triage_cluster(cluster: dict, *, _run=None) -> dict:
    titles = [Path(m).stem.replace("-", " ") for m in cluster.get("members", [])]
    prompt = cp.triage_prompt(cluster["topic"], cluster["domain"], titles)
    inner = _headless(prompt, CONSOLIDATE_TRIAGE_MODEL, ["Read"], _run=_run)
    m = re.search(r"\{.*\}", inner, re.S)
    if not m:
        return {"mode": "reject", "title": "", "slug": "", "reason": "unparseable triage"}
    try:
        data = json.loads(m.group(0))
    except json.JSONDecodeError:
        return {"mode": "reject", "title": "", "slug": "", "reason": "bad json"}
    mode = data.get("mode")
    if mode not in ("new-synthesis", "deepen-existing", "reject"):
        return {"mode": "reject", "title": "", "slug": "", "reason": "unknown mode"}
    return {"mode": mode, "title": data.get("title", ""), "slug": data.get("slug", ""),
            "reason": data.get("reason", "")}


def queue_reject(cluster: dict, verdict: dict, review_path: Path) -> None:
    review_path.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    line = (f"- [{today}] [{verdict.get('mode')}] {cluster['domain']} · \"{cluster['topic']}\" "
            f"({cluster.get('size', len(cluster.get('members', [])))} sources) — "
            f"{verdict.get('reason', '')}\n")
    with review_path.open("a", encoding="utf-8") as f:
        f.write(line)


_CONSOLIDATED_RE = re.compile(r"^consolidated_into:\s*\S+\s*\n", re.M)


def synthesize(cluster: dict, triage: dict, corpus: Path, *, _run=None) -> Path | None:
    slug = triage.get("slug") or co._norm(cluster["topic"])
    prompt = cp.synthesis_prompt(cluster["topic"], cluster["domain"], slug, cluster["members"])
    _headless(prompt, CONSOLIDATE_MODEL, ["Read", "Write", "Edit"], _run=_run)
    out = corpus / cluster["domain"] / f"{slug}.md"
    return out if out.exists() else None


def stamp_members(cluster: dict, synthesis_rel: str, corpus: Path) -> int:
    n = 0
    for rel in cluster["members"]:
        p = corpus / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if "consolidated_into:" in text:
            n += 1
            continue
        # insert the flag just before the closing '---' of the frontmatter
        if text.startswith("---"):
            end = text.find("\n---", 3)
            if end != -1:
                text = text[:end] + f"\nconsolidated_into: {synthesis_rel}" + text[end:]
                p.write_text(text, encoding="utf-8")
                n += 1
    return n


def unstamp_members(cluster: dict, corpus: Path) -> int:
    n = 0
    for rel in cluster["members"]:
        p = corpus / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        new = _CONSOLIDATED_RE.sub("", text)
        if new != text:
            p.write_text(new, encoding="utf-8")
            n += 1
    return n


def _member_sources_text(cluster: dict, corpus: Path) -> str:
    parts = []
    for rel in cluster["members"]:
        p = corpus / rel
        if p.exists():
            parts.append(f"=== {rel} ===\n{p.read_text(encoding='utf-8', errors='ignore')}")
    return "\n\n".join(parts)


def process_cluster(cluster: dict, triage: dict, corpus: Path, review_path: Path,
                    *, _run=None, _critic=None) -> dict:
    mode = triage.get("mode")
    if mode != "new-synthesis":
        queue_reject(cluster, triage, review_path)
        return {"status": "queued", "mode": mode}

    page = synthesize(cluster, triage, corpus, _run=_run)
    if page is None:
        queue_reject(cluster, {**triage, "mode": "reject", "reason": "writer produced no page"},
                     review_path)
        return {"status": "reverted", "reason": "no page written"}

    synthesis_rel = str(page.relative_to(corpus))
    critic = _critic if _critic is not None else \
        (lambda pg, src: gd._critic_call(Path(pg), src))
    try:
        ok, issues = critic(str(page), _member_sources_text(cluster, corpus))
    except Exception as exc:  # noqa: BLE001 — fail CLOSED: a critic that errors is not trusted
        ok, issues = False, [f"critic error: {exc}"]
    if not ok:
        page.unlink(missing_ok=True)                       # revert the new page (only new file)
        unstamp_members(cluster, corpus)
        queue_reject(cluster, {**triage, "mode": "reject",
                               "reason": "critic: " + "; ".join(issues)[:160]}, review_path)
        return {"status": "reverted", "issues": issues}

    stamped = stamp_members(cluster, synthesis_rel, corpus)
    return {"status": "synthesized", "page": synthesis_rel, "members_stamped": stamped}


def run_consolidation(corpus: Path, domain: str, max_clusters: int, *, dry_run: bool = False,
                      _run=None, _critic=None, review_path: Path | None = None) -> dict:
    review = review_path if review_path is not None else REVIEW
    clusters = co.build_clusters(corpus, domain)
    ranked = co.rank_clusters(clusters, co.existing_topic_keys(corpus, domain))
    t = {"status": "ok", "synthesized": 0, "reverted": 0, "queued": 0,
         "clusters_seen": len(ranked)}
    for cluster in ranked[:max_clusters]:
        if dry_run:
            continue
        triage = triage_cluster(cluster, _run=_run)
        res = process_cluster(cluster, triage, corpus, review, _run=_run, _critic=_critic)
        if res["status"] == "synthesized":
            t["synthesized"] += 1
        elif res["status"] == "reverted":
            t["reverted"] += 1
        else:
            t["queued"] += 1
    return t


def run_deepen(corpus: Path, domain: str, max_candidates: int, *, dry_run: bool = False,
               _run=None, _critic=None, review_path: Path | None = None) -> dict:
    review = review_path if review_path is not None else REVIEW
    ranked = co.rank_deepen_candidates(corpus, domain)
    t = {"status": "ok", "deepened": 0, "reverted": 0, "no_change": 0,
         "candidates_seen": len(ranked)}
    for cand in ranked[:max_candidates]:
        if dry_run:
            continue
        cluster = {"topic": cand["topic"], "domain": cand["domain"], "members": cand["members"]}
        res = deepen_page(cluster, cand["target_page"], corpus, review,
                          _run=_run, _critic=_critic)
        t[res["status"]] = t.get(res["status"], 0) + 1
    return t


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Consolidate source clusters (synthesize | deepen).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("run")
    pr.add_argument("--domain", default="ai-engineering")
    pr.add_argument("--max-clusters", type=int, default=3)
    pr.add_argument("--mode", choices=["synthesize", "deepen"], default="synthesize")
    pr.add_argument("--dry-run", action="store_true")
    pr.add_argument("--lock-path", default=LOCK, type=Path)
    args = ap.parse_args(argv)

    def _go(dry):
        if args.mode == "deepen":
            return run_deepen(CORPUS, args.domain, args.max_clusters, dry_run=dry)
        return run_consolidation(CORPUS, args.domain, args.max_clusters, dry_run=dry)

    if not sr._on_main():
        print(json.dumps({"status": "skipped", "reason": "not_on_main"})); return 0
    if args.dry_run:
        print(json.dumps(_go(True))); return 0
    if not sr.acquire_lock(args.lock_path):
        print(json.dumps({"status": "skipped", "reason": "lock_held"})); return 0
    try:
        print(json.dumps(_go(False))); return 0
    finally:
        sr.release_lock(args.lock_path)


_FOOTNOTE_DEF_RE = re.compile(r"^\[\^([^\]]+)\]:", re.M)


def _footnote_targets(text: str) -> set:
    """The set of footnote-definition ids (`[^id]:`) declared in a page."""
    return set(_FOOTNOTE_DEF_RE.findall(text))


def deepen_page(cluster: dict, target_rel: str, corpus: Path, review_path: Path,
                *, _run=None, _critic=None) -> dict:
    target = corpus / target_rel
    if not target.exists():
        return {"status": "no_change", "reason": "target missing"}
    pre = target.read_text(encoding="utf-8", errors="ignore")   # saved pre-image for revert

    prompt = cp.deepen_prompt(target_rel, cluster["topic"], cluster["members"])
    _headless(prompt, CONSOLIDATE_MODEL, ["Read", "Write", "Edit"], _run=_run)
    post = target.read_text(encoding="utf-8", errors="ignore")

    if post == pre:                                             # writer did nothing
        return {"status": "no_change", "page": target_rel}

    def _restore(reason):
        target.write_text(pre, encoding="utf-8")               # byte-for-byte restore
        unstamp_members(cluster, corpus)
        queue_reject({**cluster, "size": len(cluster["members"])},
                     {"mode": "deepen-existing", "reason": reason}, review_path)
        return {"status": "reverted", "reason": reason}

    # deterministic guard: the deepened page must keep every original footnote
    dropped = _footnote_targets(pre) - _footnote_targets(post)
    if dropped:
        return _restore("dropped citations: " + ", ".join(sorted(dropped))[:120])

    critic = _critic if _critic is not None else (lambda pg, src: gd._critic_call(Path(pg), src))
    try:
        ok, issues = critic(str(target), _member_sources_text(cluster, corpus))
    except Exception as exc:  # noqa: BLE001 — fail CLOSED
        ok, issues = False, [f"critic error: {exc}"]
    if not ok:
        return _restore("critic: " + "; ".join(issues)[:140])

    stamped = stamp_members(cluster, target_rel, corpus)
    return {"status": "deepened", "page": target_rel, "members_stamped": stamped,
            "added_words": len(post.split()) - len(pre.split())}


if __name__ == "__main__":
    raise SystemExit(main())
