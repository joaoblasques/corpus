#!/usr/bin/env python3
"""Tests for book_discover (index parse, trust partition, ledger) + book_fetch review promotion."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import book_discover as bd  # noqa: E402
import book_fetch as bf  # noqa: E402

INDEX = """# Free Programming Books

### Machine Learning
* [Trusted ML Book](https://d2l.ai/some-book.pdf) - Author (PDF)
* [Untrusted ML Book](https://random-host.example.org/ml.pdf) - Author (PDF)
* [HTML Only](https://random-host.example.org/read-online) - Author (HTML)

### Cooking
* [Not Relevant](https://d2l.ai/cooking.pdf) - Author (PDF)
"""


def test_parse_index_filters_section_and_pdf(tmp_path):
    cands = bd.parse_index(INDEX, ["machine learning", "cloud"])
    urls = [c["url"] for c in cands]
    assert "https://d2l.ai/some-book.pdf" in urls
    assert "https://random-host.example.org/ml.pdf" in urls
    assert "https://random-host.example.org/read-online" not in urls   # not PDF-ish
    assert "https://d2l.ai/cooking.pdf" not in urls                     # wrong section


def test_collect_partitions_trusted_vs_review_and_prechecks(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(bd, "REVIEW", tmp_path / "_book_review.md")
    monkeypatch.setattr(bd, "LEDGER", tmp_path / ".disc.txt")
    monkeypatch.setattr(bd.bf, "load_config", lambda path=None: {"allowlist": ["d2l.ai", "raw.githubusercontent.com"], "books": []})
    cfg = tmp_path / "d.yaml"
    cfg.write_text("index_urls: [https://raw.githubusercontent.com/x/y/main/f.md]\n"
                   "relevant_sections: [machine learning]\nmax_new_per_run: 10\n", encoding="utf-8")
    args = bd._args(["collect", "--config", str(cfg), "--today", "2026-07-06"])
    args._fetch = lambda url, timeout=40: INDEX
    bd.cmd_collect(args)
    out = json.loads(capsys.readouterr().out)
    assert out["proposed"] == 2 and out["auto_trusted"] == 1 and out["needs_review"] == 1

    review = (tmp_path / "_book_review.md").read_text()
    assert "- [x] [Trusted ML Book](https://d2l.ai/some-book.pdf)" in review      # pre-approved
    assert "- [ ] [Untrusted ML Book](https://random-host.example.org/ml.pdf)" in review  # needs tick

    # second run: all in the ledger -> nothing re-proposed
    args2 = bd._args(["collect", "--config", str(cfg), "--today", "2026-07-06"])
    args2._fetch = lambda url, timeout=40: INDEX
    bd.cmd_collect(args2)
    assert json.loads(capsys.readouterr().out)["proposed"] == 0


def test_collect_refuses_untrusted_index(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(bd, "REVIEW", tmp_path / "r.md")
    monkeypatch.setattr(bd, "LEDGER", tmp_path / "l.txt")
    monkeypatch.setattr(bd.bf, "load_config", lambda path=None: {"allowlist": ["d2l.ai"], "books": []})
    cfg = tmp_path / "d.yaml"
    cfg.write_text("index_urls: [https://evil.example.org/index.md]\n"
                   "relevant_sections: [machine learning]\n", encoding="utf-8")
    args = bd._args(["collect", "--config", str(cfg)])
    args._fetch = lambda url, timeout=40: (_ for _ in ()).throw(AssertionError("must not fetch untrusted index"))
    bd.cmd_collect(args)
    assert json.loads(capsys.readouterr().out)["proposed"] == 0


def test_book_fetch_review_approved_parses_checked_only(tmp_path, monkeypatch):
    review = tmp_path / "_book_review.md"
    review.write_text(
        "## Discovered 2026-07-06\n"
        "- [x] [Approved Book](https://d2l.ai/a.pdf) · d2l.ai · trusted\n"
        "- [ ] [Pending Book](https://x.org/b.pdf) · x.org · review\n"
        "- [X] [Also Approved](https://y.org/c.pdf) · y.org · review\n", encoding="utf-8")
    approved = bf.review_approved(review)
    urls = [a["url"] for a in approved]
    assert urls == ["https://d2l.ai/a.pdf", "https://y.org/c.pdf"]     # only [x]/[X], not [ ]
    assert approved[0]["name"] == "approved-book"


def test_book_fetch_downloads_approved_review_entry_bypassing_allowlist(tmp_path, monkeypatch, capsys):
    """A human-ticked entry on an UNtrusted host still downloads — approval is the gate."""
    monkeypatch.setattr(bf, "LEDGER", tmp_path / "ledger.txt")
    monkeypatch.setattr(bf, "REVIEW", tmp_path / "_book_review.md")
    bf.REVIEW.write_text("- [x] [Ticked Book](https://untrusted.example.org/x.pdf) · h · review\n",
                         encoding="utf-8")
    cfg = tmp_path / "s.yaml"
    cfg.write_text("allowlist: [d2l.ai]\nbooks: []\n", encoding="utf-8")
    got = []

    def fake_dl(url, dest, timeout=180):
        got.append(url); Path(dest).parent.mkdir(parents=True, exist_ok=True)
        Path(dest).write_bytes(b"%PDF-1.5"); return True

    args = bf._args(["collect", "--config", str(cfg), "--dir", str(tmp_path / "land")])
    args._download = fake_dl
    bf.cmd_collect(args)
    out = json.loads(capsys.readouterr().out)
    assert out["fetched"] == 1 and got == ["https://untrusted.example.org/x.pdf"]
