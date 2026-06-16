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
