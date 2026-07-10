#!/usr/bin/env python3
"""Tests for corpus_heal — deterministic citation repointing (unique match only)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import corpus_heal as ch  # noqa: E402


def _mk(root: Path):
    """A tiny corpus + raw tree: one moved file, one ambiguous, one truly missing."""
    corpus = root / "corpus"
    (corpus / "ai-engineering" / "sources").mkdir(parents=True)
    (corpus / "ai-engineering" / "README.md").write_text("# hub\n", encoding="utf-8")
    raw = root / "raw"
    (raw / "web").mkdir(parents=True)
    (raw / "notes").mkdir(parents=True)
    (raw / "_inbox").mkdir(parents=True)
    # moved.md now lives in raw/web (page cites the old _inbox path)
    (raw / "web" / "moved.md").write_text("moved source", encoding="utf-8")
    # dup.md exists in two places -> ambiguous, must NOT be touched
    (raw / "web" / "dup.md").write_text("a", encoding="utf-8")
    (raw / "notes" / "dup.md").write_text("b", encoding="utf-8")
    return corpus, raw


def test_repoints_unique_leaves_ambiguous_and_missing(tmp_path):
    corpus, raw = _mk(tmp_path)
    page = corpus / "ai-engineering" / "concept.md"
    page.write_text(
        "---\ntype: concept\n---\n"
        "Claim one.[^1] Claim two.[^2] Claim three.[^3]\n\n"
        "[^1]: [t](../../raw/_inbox/moved.md)\n"      # moved -> should repoint to raw/web/moved.md
        "[^2]: [t](../../raw/_inbox/dup.md)\n"        # ambiguous -> leave
        "[^3]: [t](../../raw/_inbox/gone.md)\n",      # missing -> leave + report
        encoding="utf-8")

    t = ch.repair_citations(corpus, raw, apply=True)
    assert t["repaired"] == 1 and t["ambiguous"] == 1 and t["missing"] == 1
    assert t["pages_changed"] == 1

    out = page.read_text()
    assert "](../../raw/web/moved.md)" in out          # repointed to the real location
    assert "](../../raw/_inbox/dup.md)" in out         # ambiguous untouched
    assert "](../../raw/_inbox/gone.md)" in out        # missing untouched
    assert any("gone.md" in m for m in t["missing_list"])


def test_dry_run_does_not_write(tmp_path):
    corpus, raw = _mk(tmp_path)
    page = corpus / "ai-engineering" / "c.md"
    original = ("---\ntype: concept\n---\nx[^1]\n\n[^1]: [t](../../raw/_inbox/moved.md)\n")
    page.write_text(original, encoding="utf-8")

    t = ch.repair_citations(corpus, raw, apply=False)
    assert t["repaired"] == 1 and t["pages_changed"] == 1
    assert page.read_text() == original                # dry-run: unchanged on disk


def test_valid_citation_is_left_alone(tmp_path):
    corpus, raw = _mk(tmp_path)
    page = corpus / "ai-engineering" / "sources" / "s.md"
    # a correct citation from a sources/ page (../../../ depth) to an existing file
    page.write_text("---\ntype: source\n---\nx[^1]\n\n[^1]: [t](../../../raw/web/moved.md)\n",
                    encoding="utf-8")
    t = ch.repair_citations(corpus, raw, apply=True)
    assert t["repaired"] == 0 and t["pages_changed"] == 0
