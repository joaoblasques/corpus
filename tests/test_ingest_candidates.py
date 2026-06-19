#!/usr/bin/env python3
"""Tests for bin/ingest_candidates.py — deterministic ingest candidate selection."""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import ingest_candidates as ic  # noqa: E402


def _write(inbox: Path, name: str, *, frontmatter: str, body: str = "content", mtime=None):
    p = inbox / name
    p.write_text(f"---\n{frontmatter}\n---\n\n{body}\n", encoding="utf-8")
    if mtime is not None:
        os.utime(p, (mtime, mtime))
    return p


def test_skips_already_ingested(tmp_path):
    _write(tmp_path, "email-a.md", frontmatter="channel: email\ncorpus_ingested: true")
    assert ic.select_candidates(tmp_path, limit=10) == []


def test_skips_non_ok_transcript_stubs(tmp_path):
    _write(tmp_path, "youtube-blk.md", frontmatter="channel: youtube\ntranscript_status: blocked",
           body="_No transcript available._")
    _write(tmp_path, "youtube-dis.md", frontmatter="channel: youtube\ntranscript_status: disabled",
           body="_No transcript available._")
    assert ic.select_candidates(tmp_path, limit=10) == []


def test_keeps_ok_transcripts_and_emails(tmp_path):
    ok = _write(tmp_path, "youtube-ok.md", frontmatter="channel: youtube\ntranscript_status: ok",
                body="[00:00] real transcript")
    em = _write(tmp_path, "email-x.md", frontmatter="channel: email")
    got = set(ic.select_candidates(tmp_path, limit=10))
    assert got == {ok, em}


def test_caps_at_limit(tmp_path):
    for i in range(5):
        _write(tmp_path, f"email-{i}.md", frontmatter="channel: email")
    assert len(ic.select_candidates(tmp_path, limit=3)) == 3


def test_orders_oldest_first(tmp_path):
    old = _write(tmp_path, "email-old.md", frontmatter="channel: email", mtime=1_000)
    mid = _write(tmp_path, "email-mid.md", frontmatter="channel: email", mtime=2_000)
    new = _write(tmp_path, "email-new.md", frontmatter="channel: email", mtime=3_000)
    assert ic.select_candidates(tmp_path, limit=10) == [old, mid, new]


def test_empty_inbox(tmp_path):
    assert ic.select_candidates(tmp_path, limit=10) == []


def test_excludes_deferred_sources(tmp_path):
    _write(tmp_path, "email-keep.md", frontmatter="channel: email")
    _write(tmp_path, "email-deferred.md", frontmatter="channel: email")
    (tmp_path / "_REVIEW.md").write_text(
        "# Review queue\n- DEFER UNCERTAIN: email-deferred.md — newsletter blurb, no body\n",
        encoding="utf-8")
    got = {p.name for p in ic.select_candidates(tmp_path, limit=10)}
    assert got == {"email-keep.md"}, "already-deferred sources must not be re-selected"


def test_never_selects_the_review_file_itself(tmp_path):
    (tmp_path / "_REVIEW.md").write_text("# Review queue\n", encoding="utf-8")
    _write(tmp_path, "email-a.md", frontmatter="channel: email")
    got = {p.name for p in ic.select_candidates(tmp_path, limit=10)}
    assert got == {"email-a.md"}, "_REVIEW.md must never be an ingest candidate"


def test_no_review_file_excludes_nothing(tmp_path):
    _write(tmp_path, "email-a.md", frontmatter="channel: email")
    assert [p.name for p in ic.select_candidates(tmp_path, limit=10)] == ["email-a.md"]


# --- pointer → fetched-companion resolution -------------------------------

def test_is_pointer_true_and_false(tmp_path):
    ptr = _write(tmp_path, "p.md", frontmatter="channel: email\npointer: true")
    plain = _write(tmp_path, "q.md", frontmatter="channel: email\npointer: false")
    assert ic.is_pointer(ptr) is True
    assert ic.is_pointer(plain) is False
    assert ic.is_pointer(_write(tmp_path, "r.md", frontmatter="channel: email")) is False


def test_fetched_companions_returns_existing_web_file(tmp_path):
    web = tmp_path / "raw" / "web"
    web.mkdir(parents=True)
    (web / "article.md").write_text("real content\n", encoding="utf-8")
    fm = ('channel: email\npointer: true\nlinks:\n'
          '  - {url: "http://x", fetched: true, score: 8, file: raw/web/article.md}')
    ptr = _write(tmp_path, "p.md", frontmatter=fm)
    got = ic.fetched_companions(ptr, root=tmp_path)
    assert [p.name for p in got] == ["article.md"]


def test_fetched_companions_skips_unfetched_and_missing(tmp_path):
    (tmp_path / "raw" / "web").mkdir(parents=True)
    fm = ('channel: email\npointer: true\nlinks:\n'
          '  - {url: "http://x", fetched: false, score: 7, reason: over-cap}\n'
          '  - {url: "http://y", fetched: true, score: 8, file: raw/web/missing.md}')
    ptr = _write(tmp_path, "p.md", frontmatter=fm)
    # fetched:false excluded; fetched:true but file absent on disk excluded
    assert ic.fetched_companions(ptr, root=tmp_path) == []


def test_fetched_companions_empty_for_non_pointer(tmp_path):
    web = tmp_path / "raw" / "web"
    web.mkdir(parents=True)
    (web / "article.md").write_text("x\n", encoding="utf-8")
    fm = ('channel: email\nlinks:\n'
          '  - {url: "http://x", fetched: true, file: raw/web/article.md}')
    plain = _write(tmp_path, "q.md", frontmatter=fm)
    assert ic.fetched_companions(plain, root=tmp_path) == []


def test_select_candidates_prioritizes_labeled(tmp_path):
    """Label-collected sources sort first even when their mtime is newer (marking
    rewrites mtime); within groups, oldest first."""
    import os
    old_plain = tmp_path / "a-old-plain.md"
    old_plain.write_text("---\nchannel: email\n---\nbody\n", encoding="utf-8")
    new_labeled = tmp_path / "b-new-labeled.md"
    new_labeled.write_text("---\nchannel: email\ngmail_corpus_labels:\n  - MLOps\n---\nbody\n",
                           encoding="utf-8")
    older_labeled = tmp_path / "c-older-labeled.md"
    older_labeled.write_text("---\nchannel: email\ngmail_corpus_labels:\n  - Ml\n---\nbody\n",
                             encoding="utf-8")
    os.utime(old_plain, (100, 100))       # oldest mtime, but unlabeled
    os.utime(older_labeled, (200, 200))   # labeled, older of the two labeled
    os.utime(new_labeled, (300, 300))     # labeled, newest
    out = [p.name for p in ic.select_candidates(inbox_dir=tmp_path, limit=10)]
    assert out[:2] == ["c-older-labeled.md", "b-new-labeled.md"]  # both labeled, oldest-first
    assert out[2] == "a-old-plain.md"                              # unlabeled last
