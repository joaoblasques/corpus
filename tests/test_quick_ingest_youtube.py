#!/usr/bin/env python3
"""Tests for bin/quick_ingest_youtube.py — OKF conformance: index.md path + root-relative links."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))


# NOTE: import the REAL modules. youtube_client's heavy deps (googleapiclient, transcript
# APIs) are all lazy inside functions, so importing offline is safe. Never inject fakes into
# sys.modules here — a fake module leaks into every later test file in the same pytest
# process (it once broke test_youtube_client.py's entire suite).
import quick_ingest_youtube as qy  # noqa: E402


# ---------------------------------------------------------------------------
# Test: INDEX constant points to OKF-conformant file name
# ---------------------------------------------------------------------------

def test_index_constant_is_index_md():
    """INDEX must point to corpus/index.md (not the old _index.md)."""
    assert qy.INDEX.name == "index.md", (
        f"INDEX filename should be 'index.md', got {qy.INDEX.name!r}"
    )


# ---------------------------------------------------------------------------
# Test: _index_append emits root-relative markdown link (no wikilinks)
# ---------------------------------------------------------------------------

def test_index_append_emits_root_relative_link(tmp_path):
    """_index_append must write a root-relative markdown link, not a [[wikilink]]."""
    # Set up a minimal index.md with a domain section
    index = tmp_path / "index.md"
    index.write_text(
        "# Corpus Index\n\n## Domains\n\n### ai-engineering\n",
        encoding="utf-8",
    )
    # Monkeypatch INDEX to point to our tmp index
    original_index = qy.INDEX
    try:
        qy.INDEX = index
        qy._index_append("ai-engineering", "my-slug-abc123", "My Video", "Short summary here")
    finally:
        qy.INDEX = original_index

    text = index.read_text(encoding="utf-8")
    # Must contain a root-relative markdown link
    assert re.search(r"- \[My Video\]\(/ai-engineering/sources/my-slug-abc123\.md\)", text), (
        f"Expected root-relative markdown link in index, got:\n{text}"
    )
    # Must NOT contain a wikilink
    assert "[[" not in text, f"Found wikilink in index output:\n{text}"


def test_index_append_no_wikilink_when_section_absent(tmp_path):
    """When the domain section is absent, _index_append creates it with a root-relative link."""
    index = tmp_path / "index.md"
    index.write_text("# Corpus Index\n\n## Domains\n\n", encoding="utf-8")
    original_index = qy.INDEX
    try:
        qy.INDEX = index
        qy._index_append("data-engineering", "slug-xyz", "Some Doc", "one line summary")
    finally:
        qy.INDEX = original_index

    text = index.read_text(encoding="utf-8")
    assert re.search(r"- \[Some Doc\]\(/data-engineering/sources/slug-xyz\.md\)", text), (
        f"Expected root-relative markdown link (absent section case):\n{text}"
    )
    assert "[[" not in text, f"Found wikilink in index output:\n{text}"


def test_index_append_link_format_matches_okf_pattern(tmp_path):
    """The bullet written by _index_append must match the OKF root-relative pattern."""
    index = tmp_path / "index.md"
    index.write_text("# Corpus Index\n\n### mlops\n", encoding="utf-8")
    original_index = qy.INDEX
    try:
        qy.INDEX = index
        qy._index_append("mlops", "cool-video-vid1", "Cool Video", "summary text")
    finally:
        qy.INDEX = original_index

    text = index.read_text(encoding="utf-8")
    # Pattern: - [Title](/domain/sources/slug.md) — source · stub · summary
    assert re.search(
        r"- \[.+\]\(/mlops/sources/.+\.md\) — source · stub",
        text,
    ), f"Bullet does not match OKF root-relative pattern:\n{text}"


def test_index_append_noop_when_index_absent(tmp_path):
    """_index_append silently does nothing when index.md doesn't exist."""
    index = tmp_path / "nonexistent_index.md"
    original_index = qy.INDEX
    try:
        qy.INDEX = index
        # Should not raise
        qy._index_append("ai-engineering", "slug", "Title", "summary")
    finally:
        qy.INDEX = original_index
    assert not index.exists()
