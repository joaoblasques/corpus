#!/usr/bin/env python3
"""Tests for the GitHub-hosted CC book pipeline — AsciiDoc cleanup, chapters, stubs, dedup."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import collect_github_book as gb  # noqa: E402
import github_book_client as gbc  # noqa: E402
import collect_books as cb  # noqa: E402

CH1 = """[role="pagenumrestart"]
[[ch01_intro]]
== Introduction

Bitcoin((("Bitcoin", "operational overview"))) is a collection of concepts. See <<ch02,the overview>>.

[TIP]
====
The unit is "bitcoin" with a small _b_.
====

More prose here that should absolutely survive the cleanup pass intact and readable.
"""


def _repo(tmp_path, **files):
    d = tmp_path / "repo"
    d.mkdir()
    for name, content in files.items():
        (d / name).write_text(content, encoding="utf-8")
    return d


def test_clean_asciidoc_strips_markup_keeps_prose():
    out = gb._clean_asciidoc(CH1)
    assert "## Introduction" in out                 # == heading -> markdown
    assert "(((" not in out                          # index-term macro stripped
    assert "[role=" not in out and "[[ch01" not in out
    assert "====" not in out                         # block delimiters gone
    assert "the overview" in out                     # <<anchor,text>> -> text
    assert "Bitcoin is a collection of concepts" in out
    assert "unit is \"bitcoin\"" in out               # admonition body preserved


def test_chapter_title_reads_first_heading():
    assert gb.chapter_title(CH1) == "Introduction"
    assert gb.chapter_title("# Markdown Title\n\nbody") == "Markdown Title"
    assert gb.chapter_title("no heading here") is None


def test_extract_chapters_spine_order_and_min_words(tmp_path):
    ch1 = "== Introduction\n\n" + " ".join(["alpha"] * 300)   # long enough to keep
    ch2 = "== Real Chapter\n\n" + " ".join(["beta"] * 300)
    repo = _repo(tmp_path, **{"ch01_intro.adoc": ch1,
                              "ch02_big.adoc": ch2,
                              "ch03_stub.adoc": "== Tiny\n\ntoo short"})
    chapters = gb.extract_chapters(repo, "ch*.adoc")
    assert [c["index"] for c in chapters] == [1, 2]       # ch03 skipped (below min words)
    assert chapters[0]["title"] == "Introduction"
    assert chapters[0]["src_file"] == "ch01_intro.adoc"


def test_build_gh_stub_has_github_provenance():
    book = {"title": "Mastering Bitcoin", "author": "A. Antonopoulos",
            "repo": "https://github.com/bitcoinbook/bitcoinbook", "ref": "develop",
            "license": "CC BY-SA 4.0"}
    ch = {"index": 1, "title": "Introduction", "text": "body", "src_file": "ch01_intro.adoc"}
    stub = gb.build_gh_stub(book, ch, sha="abc123", collected_at="2026-07-06")
    assert "channel: book" in stub and "source: github-book" in stub
    assert "license: CC BY-SA 4.0" in stub
    assert "source_path: https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch01_intro.adoc" in stub
    assert "content_sha: abc123" in stub


def test_collect_no_clone_writes_stubs_and_dedups(tmp_path, monkeypatch, capsys):
    """--no-clone extracts from a pre-staged repo; a second run dedups by sha."""
    # stage a fake repo where the client expects the clone (<tmp>/repo). Patch tempfile so we
    # control the location, and INBOX/DEDUP so nothing touches the real corpus.
    work = tmp_path / "work"; work.mkdir()
    monkeypatch.setattr(gbc.tempfile, "mkdtemp", lambda prefix="": str(work))
    repo = work / "repo"; repo.mkdir()
    (repo / "ch01.adoc").write_text("== Intro\n\n" + " ".join(["alpha"] * 300), encoding="utf-8")
    (repo / "ch02.adoc").write_text("== Deep\n\n" + " ".join(["beta"] * 300), encoding="utf-8")
    inbox = tmp_path / "inbox"
    monkeypatch.setattr(cb, "INBOX", inbox)
    monkeypatch.setattr(cb, "DEDUP_DIRS", [inbox])

    cfg = tmp_path / "gh.yaml"
    cfg.write_text('books:\n  - name: t\n    title: "Test Book"\n    author: "X"\n'
                   '    repo: https://github.com/x/y\n    ref: main\n    chapter_glob: "ch*.adoc"\n'
                   '    license: "CC BY-SA 4.0"\n', encoding="utf-8")

    # rmtree would delete our staged repo mid-run; make it a no-op so --no-clone can read it
    monkeypatch.setattr(gbc.shutil, "rmtree", lambda *a, **k: None)
    gbc.cmd_collect(gbc._args(["collect", "--config", str(cfg), "--no-clone"]))
    out = json.loads(capsys.readouterr().out)
    assert out["books"] == 1 and out["chapters"] == 2
    names = sorted(p.name for p in inbox.glob("book-*.md"))
    assert names == ["book-test-book-01-intro.md", "book-test-book-02-deep.md"]
    assert "source: github-book" in (inbox / names[0]).read_text()

    # second run: identical sha -> all skipped
    gbc.cmd_collect(gbc._args(["collect", "--config", str(cfg), "--no-clone"]))
    out2 = json.loads(capsys.readouterr().out)
    assert out2["chapters"] == 0 and out2["skipped"] == 2
