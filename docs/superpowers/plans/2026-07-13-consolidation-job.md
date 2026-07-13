# Consolidation Job Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Cluster shallow `source` pages by shared topic and synthesize each cluster into one dense, fully-cited `synthesis` page — raising the corpus's depth ratio (949 sources : 143 knowledge) without destroying provenance.

**Architecture:** Four stages mirroring the existing Gardener pattern — deterministic topic-clustering (`consolidate.py`, no LLM) → Sonnet triage → Opus synthesis writer → Sonnet fail-closed critic (reused from `gardener._critic_call`). Members are flagged `consolidated_into:` (never deleted); a synthesis that fails the critic is reverted and its cluster queued for a human. Weekly, Opus-budgeted, bounded, piloted on `ai-engineering`.

**Tech Stack:** Python 3.12 stdlib only (re, json, subprocess, pathlib) + pytest. Headless `claude` via `scheduled_run.CLAUDE_BIN`. No new dependencies.

## Global Constraints

- **Stdlib only** — no new pip dependencies (matches every other `bin/` collector).
- **Provenance is non-negotiable (§7):** the synthesis cites members' original sources via footnotes; every non-trivial claim cites a source; ≤25-word quotes; NEVER invent a claim absent from the cited members.
- **No deletion of knowledge (§7.1):** members are kept and flagged `consolidated_into: <path>`; a rejected synthesis is reverted (single new file removed, members un-flagged). Supersession of absorbed stubs is OUT of v1.
- **Fail closed:** any critic error or unparseable verdict = reject (revert + queue), never commit.
- **Main-branch only:** the runner exits `{"status":"skipped","reason":"not_on_main"}` when `scheduled_run._on_main()` is false (matches Gardener).
- **OKF stays conformant:** synthesis pages have `type: synthesis`, root-relative markdown links `[t](/domain/page.md)`, valid YAML frontmatter.
- **Models:** writer `claude-opus-4-8` (env `CONSOLIDATE_MODEL`); triage + critic `claude-sonnet-4-6` (env `CONSOLIDATE_TRIAGE_MODEL`). Weekly cadence only — never nightly.
- **Pilot domain:** `ai-engineering` (default `--domain`); v1 cluster signal is topics+tags overlap (embeddings deferred to v2).
- **Tests never hit the network or the real corpus:** every headless `claude` call goes through an injectable `_run=` seam; every filesystem test uses `tmp_path`.

---

## File Structure

| File | Responsibility |
|---|---|
| `bin/consolidate.py` | Pure: extract topics from source pages, build + rank `(domain,topic)` clusters, dedup vs existing knowledge pages. CLI `clusters` (dry-run listing). No LLM, no writes. |
| `bin/consolidate_prompts.py` | Pure prompt builders: `triage_prompt`, `synthesis_prompt`. |
| `bin/consolidate_run.py` | Orchestrator mirroring `gardener.py`: triage → synthesize → critic → stamp/revert → reject-queue. `run` CLI with `--domain/--max-clusters/--dry-run`, lock, on-main guard. Reuses `gardener._critic_call`. |
| `bin/scheduled_run.py` | Add `run_consolidation` (weekly, bounded, Opus) + `depth_ratio` in the run report. |
| `raw/_consolidation_review.md` | Runtime reject/deepen queue (gitignored). |
| `tests/test_consolidate.py` | Cluster math, topic extraction, dedup, ranking. |
| `tests/test_consolidate_prompts.py` | Prompt content invariants. |
| `tests/test_consolidate_run.py` | Triage parse, synthesis write, member stamping, critic-revert, dry-run, lock, on-main. |
| `tests/test_scheduled_run.py` | Add `run_consolidation` unit tests + fixture guard + depth-ratio. |

---

### Task 1: Topic extraction + source-page iteration (`consolidate.py` pure core)

**Files:**
- Create: `bin/consolidate.py`
- Test: `tests/test_consolidate.py`

**Interfaces:**
- Consumes: nothing (new module).
- Produces:
  - `read_topics(text: str) -> list[str]` — lowercased, de-duped topic strings from a source page's `**Key topics**` bullets and its non-generic `tags:`.
  - `page_type(text: str) -> str` — value of the `type:` frontmatter field, or `""`.
  - `iter_source_pages(corpus: Path, domain: str | None = None) -> list[Path]` — every `type: source` page (optionally restricted to one domain dir).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_consolidate.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import consolidate as co  # noqa: E402

SOURCE = """---
type: source
domain: ai-engineering
tags:
  - corpus/ai-engineering
  - source
  - youtube-quick-intake
  - Claude Code
  - RAG
---

# A Talk

Body text.

**Key topics**
- Claude Code
- context windows
- RAG
"""

def test_read_topics_merges_bullets_and_tags_drops_generic():
    topics = co.read_topics(SOURCE)
    assert "claude code" in topics
    assert "context windows" in topics
    assert "rag" in topics
    # generic tags are dropped
    assert "source" not in topics
    assert "corpus/ai-engineering" not in topics
    assert "youtube-quick-intake" not in topics
    # de-duped (Claude Code appears in both tags and bullets)
    assert topics.count("claude code") == 1

def test_page_type_reads_frontmatter():
    assert co.page_type(SOURCE) == "source"
    assert co.page_type("no frontmatter") == ""

def test_iter_source_pages_filters_type_and_domain(tmp_path):
    corpus = tmp_path / "corpus"
    (corpus / "ai-engineering" / "sources").mkdir(parents=True)
    (corpus / "data-engineering").mkdir(parents=True)
    (corpus / "ai-engineering" / "sources" / "s1.md").write_text(SOURCE, encoding="utf-8")
    (corpus / "ai-engineering" / "concept.md").write_text("---\ntype: concept\n---\n", encoding="utf-8")
    (corpus / "data-engineering" / "s2.md").write_text(SOURCE.replace("ai-engineering", "data-engineering"), encoding="utf-8")
    all_src = co.iter_source_pages(corpus)
    assert len(all_src) == 2  # both source pages, concept excluded
    ai_only = co.iter_source_pages(corpus, domain="ai-engineering")
    assert [p.name for p in ai_only] == ["s1.md"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate.py -q -p no:cacheprovider`
Expected: FAIL — `ModuleNotFoundError: No module named 'consolidate'`.

- [ ] **Step 3: Write minimal implementation**

```python
# bin/consolidate.py
#!/usr/bin/env python3
"""consolidate.py — pure topic-clustering of shallow source pages (no LLM, no writes).

Builds (domain, topic) clusters from source-page topics/tags so the consolidation runner can
synthesize each cluster into one cited page. Spec: docs/superpowers/specs/2026-07-11-consolidation-job-design.md
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
ROOT = BIN.parent
CORPUS = ROOT / "corpus"

_TYPE_RE = re.compile(r"^type:\s*(\w+)", re.M)
_TAGS_BLOCK_RE = re.compile(r"^tags:\s*$((?:\n\s+-\s+.+)+)", re.M)
_TAG_ITEM_RE = re.compile(r"^\s+-\s+(.+?)\s*$", re.M)
_TOPICS_BULLET_RE = re.compile(r"\*\*Key topics\*\*\s*((?:\n-\s+.+)+)", re.M)
_BULLET_RE = re.compile(r"^-\s+(.+?)\s*$", re.M)
# tags that carry no topical signal
_GENERIC_TAG_RE = re.compile(r"^(corpus/|source$|hub$|entity$|concept$|synthesis$|.*-quick-intake$)")


def page_type(text: str) -> str:
    m = _TYPE_RE.search(text)
    return m.group(1) if m else ""


def read_topics(text: str) -> list[str]:
    """Lowercased, de-duped topics from a source page's Key-topics bullets + non-generic tags."""
    topics: list[str] = []
    tb = _TAGS_BLOCK_RE.search(text)
    if tb:
        for t in _TAG_ITEM_RE.findall(tb.group(1)):
            t = t.strip()
            if not _GENERIC_TAG_RE.match(t):
                topics.append(t)
    kt = _TOPICS_BULLET_RE.search(text)
    if kt:
        topics += [b.strip() for b in _BULLET_RE.findall(kt.group(1))]
    seen, out = set(), []
    for t in topics:
        k = t.lower().strip()
        if k and k not in seen:
            seen.add(k)
            out.append(k)
    return out


def iter_source_pages(corpus: Path, domain: str | None = None) -> list[Path]:
    roots = [corpus / domain] if domain else [corpus]
    out = []
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("*.md"):
            if p.name == "README.md":
                continue
            if page_type(p.read_text(encoding="utf-8", errors="ignore")) == "source":
                out.append(p)
    return sorted(out)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate.py -q -p no:cacheprovider`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
cd ~/Dev/corpus
git add bin/consolidate.py tests/test_consolidate.py
git commit -m "feat(consolidate): topic extraction + source-page iteration (pure)"
```

---

### Task 2: Cluster building, ranking + existing-page dedup (`consolidate.py`)

**Files:**
- Modify: `bin/consolidate.py` (append functions)
- Test: `tests/test_consolidate.py` (append)

**Interfaces:**
- Consumes: `read_topics`, `page_type`, `iter_source_pages` (Task 1).
- Produces:
  - `existing_topic_keys(corpus: Path, domain: str) -> set[str]` — normalized titles + slugs of `concept`/`entity`/`synthesis` pages in the domain (used to flag clusters that already have a home).
  - `build_clusters(corpus: Path, domain: str, min_cluster: int = 5) -> list[dict]` — each cluster `{"topic": str, "domain": str, "members": list[str], "size": int}` where `members` are corpus-root-relative paths, sorted by member path; only clusters with `size >= min_cluster`.
  - `rank_clusters(clusters: list[dict], existing: set[str]) -> list[dict]` — returns clusters annotated with `"has_existing_page": bool`, sorted so new-topic clusters come first, then by descending size.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_consolidate.py  (append)
def _src(topics):
    tags = "\n".join(f"  - {t}" for t in topics)
    return f"---\ntype: source\ndomain: ai-engineering\ntags:\n  - source\n{tags}\n---\n# t\nbody\n"

def test_build_clusters_groups_by_topic_and_min_size(tmp_path):
    corpus = tmp_path / "corpus"
    d = corpus / "ai-engineering" / "sources"
    d.mkdir(parents=True)
    for i in range(5):
        (d / f"s{i}.md").write_text(_src(["RAG", "context"]), encoding="utf-8")
    for i in range(2):
        (d / f"o{i}.md").write_text(_src(["obscure"]), encoding="utf-8")
    clusters = co.build_clusters(corpus, "ai-engineering", min_cluster=5)
    topics = {c["topic"]: c for c in clusters}
    assert "rag" in topics and topics["rag"]["size"] == 5          # 5 sources share RAG
    assert "context" in topics                                      # also shared by 5
    assert "obscure" not in topics                                  # only 2 -> below min
    assert topics["rag"]["members"][0].startswith("ai-engineering/sources/")

def test_existing_topic_keys_and_ranking(tmp_path):
    corpus = tmp_path / "corpus"
    (corpus / "ai-engineering" / "sources").mkdir(parents=True)
    (corpus / "ai-engineering" / "rag.md").write_text(
        "---\ntype: concept\n---\n# RAG\n", encoding="utf-8")
    existing = co.existing_topic_keys(corpus, "ai-engineering")
    assert "rag" in existing
    clusters = [
        {"topic": "rag", "domain": "ai-engineering", "members": ["a", "b"], "size": 8},
        {"topic": "agents", "domain": "ai-engineering", "members": ["c"], "size": 6},
    ]
    ranked = co.rank_clusters(clusters, existing)
    # 'agents' has no existing page -> ranks before 'rag' despite smaller size
    assert ranked[0]["topic"] == "agents" and ranked[0]["has_existing_page"] is False
    assert ranked[1]["topic"] == "rag" and ranked[1]["has_existing_page"] is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate.py -q -p no:cacheprovider`
Expected: FAIL — `AttributeError: module 'consolidate' has no attribute 'build_clusters'`.

- [ ] **Step 3: Write minimal implementation**

```python
# bin/consolidate.py  (append)
_H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.M)


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def existing_topic_keys(corpus: Path, domain: str) -> set[str]:
    """Normalized titles + slugs of concept/entity/synthesis pages in the domain."""
    keys: set[str] = set()
    root = corpus / domain
    if not root.exists():
        return keys
    for p in root.rglob("*.md"):
        if p.name == "README.md":
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if page_type(text) in ("concept", "entity", "synthesis"):
            keys.add(_norm(p.stem))
            body = text.split("---", 2)[-1] if text.startswith("---") else text
            hm = _H1_RE.search(body)
            if hm:
                keys.add(_norm(hm.group(1)))
    return keys


def build_clusters(corpus: Path, domain: str, min_cluster: int = 5) -> list[dict]:
    index: dict[str, list[str]] = {}
    for p in iter_source_pages(corpus, domain):
        rel = str(p.relative_to(corpus))
        for topic in read_topics(p.read_text(encoding="utf-8", errors="ignore")):
            index.setdefault(topic, []).append(rel)
    clusters = []
    for topic, members in index.items():
        members = sorted(set(members))
        if len(members) >= min_cluster:
            clusters.append({"topic": topic, "domain": domain,
                             "members": members, "size": len(members)})
    return clusters


def rank_clusters(clusters: list[dict], existing: set[str]) -> list[dict]:
    out = []
    for c in clusters:
        c = dict(c)
        c["has_existing_page"] = _norm(c["topic"]) in existing
        out.append(c)
    out.sort(key=lambda c: (c["has_existing_page"], -c["size"], c["topic"]))
    return out
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate.py -q -p no:cacheprovider`
Expected: PASS (5 passed).

- [ ] **Step 5: Commit**

```bash
cd ~/Dev/corpus
git add bin/consolidate.py tests/test_consolidate.py
git commit -m "feat(consolidate): cluster building, ranking + existing-page dedup"
```

---

### Task 3: `clusters` CLI (dry-run listing)

**Files:**
- Modify: `bin/consolidate.py` (add `main` + argparse)
- Test: `tests/test_consolidate.py` (append)

**Interfaces:**
- Consumes: `build_clusters`, `existing_topic_keys`, `rank_clusters`.
- Produces: `main(argv=None) -> int` — subcommand `clusters --domain <d> --min <n>` prints JSON `{"domain","count","clusters":[{topic,size,has_existing_page,members(<=5)}]}`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_consolidate.py  (append)
import json

def test_clusters_cli_prints_ranked_json(tmp_path, capsys):
    corpus = tmp_path / "corpus"
    d = corpus / "ai-engineering" / "sources"
    d.mkdir(parents=True)
    for i in range(5):
        (d / f"s{i}.md").write_text(_src(["RAG"]), encoding="utf-8")
    rc = co.main(["clusters", "--corpus", str(corpus), "--domain", "ai-engineering", "--min", "5"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["domain"] == "ai-engineering"
    assert out["count"] == 1
    assert out["clusters"][0]["topic"] == "rag" and out["clusters"][0]["size"] == 5
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate.py::test_clusters_cli_prints_ranked_json -q -p no:cacheprovider`
Expected: FAIL — `AttributeError: module 'consolidate' has no attribute 'main'`.

- [ ] **Step 3: Write minimal implementation**

```python
# bin/consolidate.py  (append)
import argparse
import json


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="List consolidation clusters (dry-run, no writes).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("clusters")
    c.add_argument("--corpus", default=None)
    c.add_argument("--domain", default="ai-engineering")
    c.add_argument("--min", type=int, default=5)
    args = ap.parse_args(argv)

    corpus = Path(args.corpus) if args.corpus else CORPUS
    clusters = build_clusters(corpus, args.domain, min_cluster=args.min)
    ranked = rank_clusters(clusters, existing_topic_keys(corpus, args.domain))
    print(json.dumps({
        "domain": args.domain, "count": len(ranked),
        "clusters": [{"topic": c["topic"], "size": c["size"],
                      "has_existing_page": c["has_existing_page"],
                      "members": c["members"][:5]} for c in ranked],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run test to verify it passes + smoke on real corpus**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate.py -q -p no:cacheprovider`
Expected: PASS (6 passed).
Run: `cd ~/Dev/corpus && python3 bin/consolidate.py clusters --domain ai-engineering --min 5 | python3 -c "import sys,json;print('clusters:',json.load(sys.stdin)['count'])"`
Expected: prints a non-zero cluster count (e.g. `clusters: 30+`).

- [ ] **Step 5: Commit**

```bash
cd ~/Dev/corpus
git add bin/consolidate.py tests/test_consolidate.py
git commit -m "feat(consolidate): clusters CLI (dry-run listing)"
```

---

### Task 4: Prompt builders (`consolidate_prompts.py` pure)

**Files:**
- Create: `bin/consolidate_prompts.py`
- Test: `tests/test_consolidate_prompts.py`

**Interfaces:**
- Consumes: nothing.
- Produces:
  - `triage_prompt(topic: str, domain: str, member_titles: list[str]) -> str`
  - `synthesis_prompt(topic: str, domain: str, slug: str, member_rel_paths: list[str]) -> str`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_consolidate_prompts.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import consolidate_prompts as cp  # noqa: E402

def test_triage_prompt_asks_for_json_mode_and_lists_titles():
    p = cp.triage_prompt("rag", "ai-engineering", ["Talk A", "Post B"])
    assert "rag" in p and "ai-engineering" in p
    assert "Talk A" in p and "Post B" in p
    # must request a strict JSON verdict with the three modes
    assert "new-synthesis" in p and "deepen-existing" in p and "reject" in p
    assert "JSON" in p or "json" in p

def test_synthesis_prompt_enforces_provenance_and_paths():
    p = cp.synthesis_prompt("rag", "ai-engineering", "rag-patterns",
                            ["ai-engineering/sources/s1.md", "ai-engineering/sources/s2.md"])
    assert "corpus/ai-engineering/rag-patterns.md" in p          # exact output path
    assert "s1.md" in p and "s2.md" in p                          # member pages listed
    assert "cite" in p.lower() and "type: synthesis" in p        # provenance + type
    assert "consolidates:" in p                                   # required frontmatter field
    assert "25" in p                                              # quote length limit
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate_prompts.py -q -p no:cacheprovider`
Expected: FAIL — `ModuleNotFoundError: No module named 'consolidate_prompts'`.

- [ ] **Step 3: Write minimal implementation**

```python
# bin/consolidate_prompts.py
#!/usr/bin/env python3
"""consolidate_prompts.py — prompt builders for the consolidation runner (pure strings)."""
from __future__ import annotations


def triage_prompt(topic: str, domain: str, member_titles: list[str]) -> str:
    titles = "\n".join(f"- {t}" for t in member_titles)
    return (
        f"You are triaging a candidate knowledge cluster in the '{domain}' domain of a personal "
        f"corpus. The cluster topic is \"{topic}\". Its member source-summary pages are:\n{titles}\n\n"
        "Decide ONE mode:\n"
        "- \"new-synthesis\": the members form a COHERENT topic worth ONE synthesis page and no "
        "such concept/synthesis page exists yet.\n"
        "- \"deepen-existing\": a concept page for this topic already exists; these members should "
        "feed its expansion instead of a new page.\n"
        "- \"reject\": the members are a grab-bag / too incoherent / too thin to synthesize.\n\n"
        "Reply with STRICT JSON only, no prose: "
        '{"mode": "new-synthesis|deepen-existing|reject", '
        '"title": "<concise Title Case page title>", '
        '"slug": "<kebab-case-slug>", "reason": "<one sentence>"}'
    )


def synthesis_prompt(topic: str, domain: str, slug: str, member_rel_paths: list[str]) -> str:
    members = "\n".join(f"- corpus/{m}" for m in member_rel_paths)
    out_path = f"corpus/{domain}/{slug}.md"
    return (
        f"Write ONE dense `synthesis` page consolidating these source-summary pages on \"{topic}\" "
        f"in the '{domain}' domain. Read every member page first:\n{members}\n\n"
        f"Create EXACTLY this file: {out_path}\n\n"
        "Rules (from CLAUDE.md):\n"
        f"- Frontmatter: type: synthesis, domain: {domain}, status: draft, plus a `consolidates:` "
        "list holding EVERY member path above, `created`/`updated` today, tags [corpus/"
        f"{domain}, synthesis].\n"
        "- Structure: TL;DR first, then the mental model, then patterns/gotchas.\n"
        "- Every non-trivial claim CITES a member's original source via a footnote [^n] (reuse the "
        "members' own source citations). NEVER invent a claim not present in a member. Keep any "
        "verbatim quote to 25 words max, one per source.\n"
        "- Link each member page inline with a root-relative link [title](/"
        f"{domain}/sources/<slug>.md).\n"
        "- Impersonal, reference-dense. Do NOT edit any file other than the one synthesis page."
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate_prompts.py -q -p no:cacheprovider`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
cd ~/Dev/corpus
git add bin/consolidate_prompts.py tests/test_consolidate_prompts.py
git commit -m "feat(consolidate): triage + synthesis prompt builders"
```

---

### Task 5: Triage call + reject/deepen queue (`consolidate_run.py`)

**Files:**
- Create: `bin/consolidate_run.py`
- Test: `tests/test_consolidate_run.py`

**Interfaces:**
- Consumes: `consolidate.build_clusters/rank_clusters/existing_topic_keys`, `consolidate_prompts.triage_prompt`, `scheduled_run` (`CLAUDE_BIN`, `ROOT`, `CORPUS`).
- Produces:
  - `triage_cluster(cluster: dict, *, _run=None) -> dict` — returns `{"mode","title","slug","reason"}`; fail-closed to `{"mode":"reject","reason":...}` on any error/unparseable output.
  - `queue_reject(cluster: dict, verdict: dict, review_path: Path) -> None` — appends a line to the review file.
  - Module constants `CONSOLIDATE_MODEL`, `CONSOLIDATE_TRIAGE_MODEL`, `REVIEW`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_consolidate_run.py
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import consolidate_run as cr  # noqa: E402

def _proc(stdout="", returncode=0, stderr=""):
    class P:  # minimal CompletedProcess stand-in
        pass
    p = P(); p.stdout = stdout; p.returncode = returncode; p.stderr = stderr
    return p

def test_triage_cluster_parses_verdict():
    def fake_run(cmd, **kw):
        assert "--model" in cmd and cr.CONSOLIDATE_TRIAGE_MODEL in cmd
        inner = json.dumps({"mode": "new-synthesis", "title": "RAG Patterns",
                            "slug": "rag-patterns", "reason": "coherent"})
        return _proc(stdout=json.dumps({"result": inner}))
    v = cr.triage_cluster({"topic": "rag", "domain": "ai-engineering",
                           "members": ["ai-engineering/sources/s1.md"]}, _run=fake_run)
    assert v["mode"] == "new-synthesis" and v["slug"] == "rag-patterns"

def test_triage_cluster_fails_closed_on_garbage():
    def fake_run(cmd, **kw):
        return _proc(stdout="not json at all")
    v = cr.triage_cluster({"topic": "x", "domain": "ai-engineering", "members": []}, _run=fake_run)
    assert v["mode"] == "reject"

def test_queue_reject_appends_line(tmp_path):
    review = tmp_path / "_consolidation_review.md"
    cr.queue_reject({"topic": "grab bag", "domain": "ai-engineering", "size": 6},
                    {"mode": "reject", "reason": "incoherent"}, review)
    txt = review.read_text()
    assert "grab bag" in txt and "reject" in txt and "incoherent" in txt
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate_run.py -q -p no:cacheprovider`
Expected: FAIL — `ModuleNotFoundError: No module named 'consolidate_run'`.

- [ ] **Step 3: Write minimal implementation**

```python
# bin/consolidate_run.py
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate_run.py -q -p no:cacheprovider`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
cd ~/Dev/corpus
git add bin/consolidate_run.py tests/test_consolidate_run.py
git commit -m "feat(consolidate): triage call + reject queue (fail-closed)"
```

---

### Task 6: Synthesis writer + member stamping

**Files:**
- Modify: `bin/consolidate_run.py` (append)
- Test: `tests/test_consolidate_run.py` (append)

**Interfaces:**
- Consumes: `_headless`, `consolidate_prompts.synthesis_prompt`, `CONSOLIDATE_MODEL`.
- Produces:
  - `synthesize(cluster: dict, triage: dict, corpus: Path, *, _run=None) -> Path | None` — invokes the Opus writer with Read/Write/Edit; returns the created synthesis Path if it now exists, else None.
  - `stamp_members(cluster: dict, synthesis_rel: str, corpus: Path) -> int` — adds `consolidated_into: <synthesis_rel>` to each member's frontmatter (idempotent); returns count stamped.
  - `unstamp_members(cluster: dict, corpus: Path) -> int` — removes any `consolidated_into:` line from members (used on revert); returns count.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_consolidate_run.py  (append)
def _write_member(corpus: Path, rel: str):
    p = corpus / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("---\ntype: source\ndomain: ai-engineering\nstatus: stub\n---\n# M\nbody\n",
                 encoding="utf-8")
    return p

def test_synthesize_returns_path_when_writer_creates_file(tmp_path):
    corpus = tmp_path / "corpus"
    cluster = {"topic": "rag", "domain": "ai-engineering",
               "members": ["ai-engineering/sources/s1.md"]}
    triage = {"mode": "new-synthesis", "title": "RAG", "slug": "rag-patterns"}

    def fake_run(cmd, **kw):
        # simulate the writer creating the synthesis page
        out = corpus / "ai-engineering" / "rag-patterns.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("---\ntype: synthesis\n---\n# RAG\n", encoding="utf-8")
        p = type("P", (), {})(); p.stdout = json.dumps({"result": "done"}); p.returncode = 0
        return p

    path = cr.synthesize(cluster, triage, corpus, _run=fake_run)
    assert path is not None and path.name == "rag-patterns.md" and path.exists()

def test_stamp_and_unstamp_members(tmp_path):
    corpus = tmp_path / "corpus"
    _write_member(corpus, "ai-engineering/sources/s1.md")
    cluster = {"topic": "rag", "domain": "ai-engineering",
               "members": ["ai-engineering/sources/s1.md"]}
    n = cr.stamp_members(cluster, "ai-engineering/rag-patterns.md", corpus)
    assert n == 1
    txt = (corpus / "ai-engineering/sources/s1.md").read_text()
    assert "consolidated_into: ai-engineering/rag-patterns.md" in txt
    # idempotent: stamping again does not duplicate
    assert cr.stamp_members(cluster, "ai-engineering/rag-patterns.md", corpus) == 1
    assert txt.count("consolidated_into:") == 1 or \
        (corpus / "ai-engineering/sources/s1.md").read_text().count("consolidated_into:") == 1
    # unstamp removes it
    assert cr.unstamp_members(cluster, corpus) == 1
    assert "consolidated_into:" not in (corpus / "ai-engineering/sources/s1.md").read_text()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate_run.py -q -p no:cacheprovider`
Expected: FAIL — `AttributeError: module 'consolidate_run' has no attribute 'synthesize'`.

- [ ] **Step 3: Write minimal implementation**

```python
# bin/consolidate_run.py  (append)
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate_run.py -q -p no:cacheprovider`
Expected: PASS (5 passed).

- [ ] **Step 5: Commit**

```bash
cd ~/Dev/corpus
git add bin/consolidate_run.py tests/test_consolidate_run.py
git commit -m "feat(consolidate): synthesis writer + member stamping"
```

---

### Task 7: Fail-closed critic + revert-on-fail

**Files:**
- Modify: `bin/consolidate_run.py` (append)
- Test: `tests/test_consolidate_run.py` (append)

**Interfaces:**
- Consumes: `gardener._critic_call(page_path: Path, sources_text: str, *, _run=None) -> (bool, list)`, `synthesize`, `stamp_members`, `unstamp_members`, `queue_reject`.
- Produces:
  - `_member_sources_text(cluster: dict, corpus: Path) -> str` — concatenated member page bodies for the critic's "cited sources".
  - `process_cluster(cluster: dict, triage: dict, corpus: Path, review_path: Path, *, _run=None, _critic=None) -> dict` — for `new-synthesis`: write → critic → on pass stamp members + return `{"status":"synthesized","page":...}`; on fail delete the page, unstamp, `queue_reject`, return `{"status":"reverted",...}`. For `deepen-existing`/`reject`: `queue_reject` + return `{"status":"queued","mode":...}`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_consolidate_run.py  (append)
def test_process_cluster_commits_on_critic_pass(tmp_path):
    corpus = tmp_path / "corpus"
    _write_member(corpus, "ai-engineering/sources/s1.md")
    cluster = {"topic": "rag", "domain": "ai-engineering", "size": 5,
               "members": ["ai-engineering/sources/s1.md"]}
    triage = {"mode": "new-synthesis", "title": "RAG", "slug": "rag-patterns"}

    def fake_writer(cmd, **kw):
        (corpus / "ai-engineering" / "rag-patterns.md").write_text(
            "---\ntype: synthesis\n---\n# RAG\ncited[^1]\n", encoding="utf-8")
        p = type("P", (), {})(); p.stdout = json.dumps({"result": "ok"}); p.returncode = 0
        return p

    res = cr.process_cluster(cluster, triage, corpus, tmp_path / "rev.md",
                             _run=fake_writer, _critic=lambda page, src: (True, []))
    assert res["status"] == "synthesized"
    assert (corpus / "ai-engineering" / "rag-patterns.md").exists()
    assert "consolidated_into:" in (corpus / "ai-engineering/sources/s1.md").read_text()

def test_process_cluster_reverts_on_critic_fail(tmp_path):
    corpus = tmp_path / "corpus"
    _write_member(corpus, "ai-engineering/sources/s1.md")
    cluster = {"topic": "rag", "domain": "ai-engineering", "size": 5,
               "members": ["ai-engineering/sources/s1.md"]}
    triage = {"mode": "new-synthesis", "title": "RAG", "slug": "rag-patterns"}

    def fake_writer(cmd, **kw):
        (corpus / "ai-engineering" / "rag-patterns.md").write_text(
            "---\ntype: synthesis\n---\n# RAG\nfabricated claim\n", encoding="utf-8")
        p = type("P", (), {})(); p.stdout = json.dumps({"result": "ok"}); p.returncode = 0
        return p

    review = tmp_path / "rev.md"
    res = cr.process_cluster(cluster, triage, corpus, review,
                             _run=fake_writer, _critic=lambda page, src: (False, ["fabricated"]))
    assert res["status"] == "reverted"
    assert not (corpus / "ai-engineering" / "rag-patterns.md").exists()   # page removed
    assert "consolidated_into:" not in (corpus / "ai-engineering/sources/s1.md").read_text()
    assert "reject" in review.read_text() or "rag" in review.read_text()

def test_process_cluster_queues_deepen_and_reject(tmp_path):
    corpus = tmp_path / "corpus"
    review = tmp_path / "rev.md"
    for mode in ("deepen-existing", "reject"):
        res = cr.process_cluster(
            {"topic": "t", "domain": "ai-engineering", "size": 6, "members": []},
            {"mode": mode, "title": "", "slug": "", "reason": "r"}, corpus, review, _run=None)
        assert res["status"] == "queued" and res["mode"] == mode
    assert review.read_text().count("\n") >= 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate_run.py -q -p no:cacheprovider`
Expected: FAIL — `AttributeError: module 'consolidate_run' has no attribute 'process_cluster'`.

- [ ] **Step 3: Write minimal implementation**

```python
# bin/consolidate_run.py  (append)
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
    ok, issues = critic(str(page), _member_sources_text(cluster, corpus))
    if not ok:
        page.unlink(missing_ok=True)                       # revert the new page (only new file)
        unstamp_members(cluster, corpus)
        queue_reject(cluster, {**triage, "mode": "reject",
                               "reason": "critic: " + "; ".join(issues)[:160]}, review_path)
        return {"status": "reverted", "issues": issues}

    stamped = stamp_members(cluster, synthesis_rel, corpus)
    return {"status": "synthesized", "page": synthesis_rel, "members_stamped": stamped}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate_run.py -q -p no:cacheprovider`
Expected: PASS (8 passed).

- [ ] **Step 5: Commit**

```bash
cd ~/Dev/corpus
git add bin/consolidate_run.py tests/test_consolidate_run.py
git commit -m "feat(consolidate): fail-closed critic + revert-on-fail"
```

---

### Task 8: `run` CLI — orchestration, lock, on-main guard, dry-run

**Files:**
- Modify: `bin/consolidate_run.py` (append)
- Test: `tests/test_consolidate_run.py` (append)

**Interfaces:**
- Consumes: everything above + `scheduled_run._on_main/acquire_lock/release_lock`, `consolidate.build_clusters/rank_clusters/existing_topic_keys`.
- Produces:
  - `run_consolidation(corpus: Path, domain: str, max_clusters: int, *, dry_run: bool = False, _run=None, _critic=None, review_path: Path | None = None) -> dict` — clusters, ranks, triages + processes up to `max_clusters`; returns `{"status","synthesized","reverted","queued","clusters_seen"}`.
  - `main(argv=None) -> int` — `run --domain --max-clusters --min --dry-run`; `_on_main()` guard; lock via `acquire_lock`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_consolidate_run.py  (append)
def test_run_consolidation_dry_run_lists_without_writing(tmp_path, monkeypatch):
    corpus = tmp_path / "corpus"
    d = corpus / "ai-engineering" / "sources"; d.mkdir(parents=True)
    for i in range(5):
        (d / f"s{i}.md").write_text(
            "---\ntype: source\ndomain: ai-engineering\ntags:\n  - source\n  - RAG\n---\n# t\nx\n",
            encoding="utf-8")
    res = cr.run_consolidation(corpus, "ai-engineering", 3, dry_run=True)
    assert res["status"] == "ok" and res["clusters_seen"] >= 1
    assert res["synthesized"] == 0                          # dry-run writes nothing
    # no synthesis page created
    assert not list((corpus / "ai-engineering").glob("rag*.md"))

def test_main_skips_when_not_on_main(monkeypatch, capsys):
    monkeypatch.setattr(cr.sr, "_on_main", lambda *a, **k: False)
    rc = cr.main(["run"])
    assert rc == 0
    assert json.loads(capsys.readouterr().out)["reason"] == "not_on_main"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate_run.py -q -p no:cacheprovider`
Expected: FAIL — `AttributeError: module 'consolidate_run' has no attribute 'run_consolidation'`.

- [ ] **Step 3: Write minimal implementation**

```python
# bin/consolidate_run.py  (append)
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


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Consolidate source clusters into synthesis pages.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("run")
    pr.add_argument("--domain", default="ai-engineering")
    pr.add_argument("--max-clusters", type=int, default=3)
    pr.add_argument("--dry-run", action="store_true")
    pr.add_argument("--lock-path", default=LOCK, type=Path)
    args = ap.parse_args(argv)

    if not sr._on_main():
        print(json.dumps({"status": "skipped", "reason": "not_on_main"})); return 0
    if args.dry_run:
        print(json.dumps(run_consolidation(CORPUS, args.domain, args.max_clusters, dry_run=True)))
        return 0
    if not sr.acquire_lock(args.lock_path):
        print(json.dumps({"status": "skipped", "reason": "lock_held"})); return 0
    try:
        print(json.dumps(run_consolidation(CORPUS, args.domain, args.max_clusters)))
        return 0
    finally:
        sr.release_lock(args.lock_path)


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run test to verify it passes + full-suite regression**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_consolidate_run.py tests/test_consolidate.py tests/test_consolidate_prompts.py -q -p no:cacheprovider`
Expected: PASS (all green).
Run: `cd ~/Dev/corpus && python3 bin/consolidate_run.py run --dry-run | python3 -c "import sys,json;print('clusters_seen:',json.load(sys.stdin)['clusters_seen'])"`
Expected: prints a non-zero `clusters_seen`.

- [ ] **Step 5: Commit + gitignore the runtime files**

```bash
cd ~/Dev/corpus
grep -qF "raw/_consolidation_review.md" .gitignore || printf 'raw/_consolidation_review.md\nraw/.consolidate.lock\n' >> .gitignore
git add bin/consolidate_run.py tests/test_consolidate_run.py .gitignore
git commit -m "feat(consolidate): run CLI — orchestration, lock, on-main guard, dry-run"
```

---

### Task 9: Nightly/weekly wiring + depth-ratio metric (`scheduled_run.py`)

**Files:**
- Modify: `bin/scheduled_run.py` (add `run_consolidation` wrapper + weekly call + `depth_ratio` in report)
- Modify: `tests/test_scheduled_run.py` (add unit tests + fixture guard)

**Interfaces:**
- Consumes: `consolidate_run.py` via subprocess (like every other collector), `corpus_lint`/`consolidate` for the depth ratio.
- Produces:
  - `scheduled_run.run_consolidation(*, max_clusters: int = 3, domain: str = "ai-engineering", timeout_s: int = 3000, _subprocess_run=None) -> dict` — runs `consolidate_run.py run`, returns `{"status","synthesized","reverted","queued"}`.
  - Depth-ratio line in the run report: `* **Depth**: K knowledge · S sources · ratio 1:R`.

Note: the WEEKLY Opus job is a separate scheduled entry (the existing Tue 13:00 leftover-Opus run). This task adds the callable + report bullet + a guarded call; wiring it into the specific weekly entrypoint follows the existing `run_gardener` call site pattern. Copy that call site exactly (same try/except, same tallies key).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_scheduled_run.py  (append near the other run_* tests)
def test_run_consolidation_parses_summary():
    def fake_run(cmd, **kw):
        assert "consolidate_run.py" in cmd[1] and "run" in cmd
        return _make_proc(returncode=0, stdout=json.dumps(
            {"status": "ok", "synthesized": 2, "reverted": 1, "queued": 3, "clusters_seen": 30}))
    out = scheduled_run.run_consolidation(_subprocess_run=fake_run)
    assert out["status"] == "ok" and out["synthesized"] == 2 and out["reverted"] == 1


def test_run_consolidation_failure_recorded_not_raised():
    def fake_run(cmd, **kw):
        return _make_proc(returncode=1, stderr="boom")
    out = scheduled_run.run_consolidation(_subprocess_run=fake_run)
    assert out["status"] == "failed" and out["synthesized"] == 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_scheduled_run.py -k consolidation -q -p no:cacheprovider`
Expected: FAIL — `AttributeError: module 'scheduled_run' has no attribute 'run_consolidation'`.

- [ ] **Step 3: Write minimal implementation**

Add to `bin/scheduled_run.py` (next to `run_gardener`):

```python
def run_consolidation(*, max_clusters: int = 3, domain: str = "ai-engineering",
                      timeout_s: int = 3000, _subprocess_run=None) -> dict:
    """Weekly consolidation: cluster shallow sources -> cited synthesis pages (Opus writer +
    fail-closed Sonnet critic in consolidate_run.py). Bounded; failure recorded, never raised."""
    _run = _subprocess_run if _subprocess_run is not None else subprocess.run
    try:
        proc = _run([sys.executable, str(BIN / "consolidate_run.py"), "run",
                     "--domain", domain, "--max-clusters", str(max_clusters)],
                    capture_output=True, text=True, timeout=timeout_s)
        if proc.returncode != 0:
            return {"status": "failed", "synthesized": 0,
                    "error": (proc.stderr or "").strip()[:200]}
        try:
            d = json.loads((proc.stdout or "").strip().splitlines()[-1])
        except (json.JSONDecodeError, IndexError):
            d = {}
        return {"status": d.get("status", "ok"), "synthesized": d.get("synthesized", 0),
                "reverted": d.get("reverted", 0), "queued": d.get("queued", 0)}
    except Exception as exc:  # noqa: BLE001
        return {"status": "failed", "synthesized": 0, "error": str(exc)}
```

- [ ] **Step 4: Run the consolidation tests + add fixture guard**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_scheduled_run.py -k consolidation -q -p no:cacheprovider`
Expected: PASS (2 passed).

Then add the fixture guard so the isolation fixture stubs it (find the `guarded = [...]` table in `tests/test_scheduled_run.py` and add this line beside `run_gardener`):

```python
        ("run_consolidation", "_subprocess_run", {"status": "ok", "synthesized": 0, "reverted": 0, "queued": 0}),
```

- [ ] **Step 5: Add the depth-ratio metric to the run report**

In `bin/scheduled_run.py`, inside `write_run_report` after the `* **Heal**:` bullet, add:

```python
    # Depth ratio (fitness metric the consolidation job moves)
    try:
        import consolidate as _co
        corpus = ROOT / "corpus"
        knowledge = sources = 0
        for p in corpus.rglob("*.md"):
            if p.name in ("README.md", "index.md", "log.md", "_domains.md", "_config.md"):
                continue
            ty = _co.page_type(p.read_text(encoding="utf-8", errors="ignore"))
            if ty in ("concept", "entity", "synthesis"):
                knowledge += 1
            elif ty == "source":
                sources += 1
        if knowledge:
            ratio = round(sources / knowledge, 1)
            bullets.append(f"* **Depth**: {knowledge} knowledge · {sources} sources · ratio 1:{ratio}")
    except Exception:  # noqa: BLE001 — advisory metric, never break the report
        pass
```

Run: `cd ~/Dev/corpus && python3 -m pytest tests/test_scheduled_run.py -q -p no:cacheprovider`
Expected: PASS (all green).

- [ ] **Step 6: Commit**

```bash
cd ~/Dev/corpus
git add bin/scheduled_run.py tests/test_scheduled_run.py
git commit -m "feat(consolidate): weekly run_consolidation wrapper + depth-ratio report metric"
```

---

### Task 10: Schema note + pilot dry-run validation

**Files:**
- Modify: `CLAUDE.md` (§4 frontmatter: document `consolidates`/`consolidated_into`; §15 version bump)
- Modify: `docs/changelog.md` (new version entry)

**Interfaces:**
- Consumes: nothing (documentation).
- Produces: schema documentation for the two new optional frontmatter fields.

- [ ] **Step 1: Document the new frontmatter fields**

In `CLAUDE.md` §4, under the claim-lifecycle fields block, add:

```markdown
- `consolidates:` (optional, v2.1) — on a `synthesis` page: list of member source-page paths it consolidates.
- `consolidated_into:` (optional, v2.1) — on a `source` page: path of the synthesis that consolidated it (member is kept, not deleted).
```

- [ ] **Step 2: Bump the version + changelog**

In `CLAUDE.md` §15 change `Current: v2.0` to `Current: v2.1`. In `docs/changelog.md` add:

```markdown
## v2.1 (2026-07-13)
- Consolidation job: cluster shallow source pages into cited synthesis pages (Opus writer +
  fail-closed Sonnet critic). New optional frontmatter `consolidates`/`consolidated_into`;
  members kept, never deleted (§7.1). Weekly, bounded, piloted on ai-engineering.
```

- [ ] **Step 3: Full-suite regression + OKF check**

Run: `cd ~/Dev/corpus && python3 -m pytest tests/ -q -p no:cacheprovider`
Expected: PASS (whole suite green).
Run: `cd ~/Dev/corpus && python3 bin/okf_lint.py | python3 -c "import sys,json;print('okf violations:', json.load(sys.stdin)['violations'])"`
Expected: `okf violations: 0`.

- [ ] **Step 4: Live pilot dry-run (no writes, real corpus)**

Run: `cd ~/Dev/corpus && python3 bin/consolidate_run.py run --domain ai-engineering --dry-run`
Expected: JSON with `status: ok` and a non-zero `clusters_seen`. Inspect that the top clusters are coherent topics ("claude code", "ai engineering", …) — if they look like grab-bags, raise `MIN_CLUSTER` in `consolidate.build_clusters` before the first real run.

- [ ] **Step 5: Commit**

```bash
cd ~/Dev/corpus
git add CLAUDE.md docs/changelog.md
git commit -m "docs(consolidate): schema v2.1 — consolidates/consolidated_into frontmatter"
```

---

## First real run (after the plan is implemented + reviewed)

Do NOT wire the weekly cron until one supervised real run passes:

```bash
cd ~/Dev/corpus
# one real cluster, watched:
python3 bin/consolidate_run.py run --domain ai-engineering --max-clusters 1
# inspect the new synthesis page, its citations, and the members' consolidated_into flags;
# check raw/_consolidation_review.md for anything reverted/queued.
python3 bin/okf_lint.py    # must stay 0 violations
```

Only after the output is trustworthy, add the weekly (Tue 13:00 Opus) call site mirroring `run_gardener`, and commit that wiring separately.

---

## Self-Review

**1. Spec coverage:**
- Cluster (deterministic) → Tasks 1-3. ✅
- Triage (Sonnet) → Task 5. ✅
- Synthesize (Opus) → Task 6. ✅
- Verify (fail-closed critic) → Task 7 (reuses `gardener._critic_call`). ✅
- Provenance + `consolidated_into`, no deletion → Tasks 6-7, 10. ✅ (supersession OUT of v1 per decision 2.)
- Reject/deepen review queue → Tasks 5, 7. ✅
- Weekly, Opus, bounded → Tasks 8-9 (`--max-clusters 3`, weekly call site). ✅
- Depth-ratio metric → Task 9. ✅
- ai-engineering pilot → default `--domain`, Task 10 dry-run. ✅
- topics-overlap v1 (no embeddings) → Task 1-2. ✅
- Schema touchpoints → Task 10. ✅

**2. Placeholder scan:** No TBD/TODO; every code step has complete code; commands have expected output. ✅

**3. Type consistency:** `cluster` dict shape (`topic/domain/members/size[/has_existing_page]`) consistent across Tasks 2-8; `triage` dict (`mode/title/slug/reason`) consistent Tasks 5-8; `process_cluster` return `status` values (`synthesized/reverted/queued`) consistent Tasks 7-8; `_critic_call` signature matches `gardener.py` as read. ✅
