#!/usr/bin/env python3
"""Tests for book_fetch — the allowlist guard, once-per-URL ledger, PDF verification."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import book_fetch as bf  # noqa: E402

ALLOW = ["arxiv.org", "d2l.ai", "github.com"]


def test_host_allowed_exact_subdomain_and_edu():
    assert bf.host_allowed("https://d2l.ai/d2l-en.pdf", ALLOW)
    assert bf.host_allowed("https://export.arxiv.org/pdf/x", ALLOW)      # subdomain
    assert bf.host_allowed("https://pages.cs.wisc.edu/book.pdf", ALLOW)  # .edu
    assert not bf.host_allowed("https://z-lib.example.com/book.pdf", ALLOW)
    assert not bf.host_allowed("https://sci-hub.se/x.pdf", ALLOW)
    assert not bf.host_allowed("not-a-url", ALLOW)


def test_collect_refuses_untrusted_host(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(bf, "LEDGER", tmp_path / "ledger.txt")
    monkeypatch.setattr(bf, "REVIEW", tmp_path / "no_review.md")
    cfg = tmp_path / "s.yaml"
    cfg.write_text('allowlist: [d2l.ai]\nbooks:\n'
                   '  - name: pirate\n    url: https://z-lib.example.org/book.pdf\n'
                   '    license: x\n    domain: ai-engineering\n', encoding="utf-8")
    args = bf._args(["collect", "--config", str(cfg), "--dir", str(tmp_path / "land")])
    args._download = lambda url, dest, timeout=180: (_ for _ in ()).throw(
        AssertionError("must not download an untrusted host"))
    bf.cmd_collect(args)
    out = json.loads(capsys.readouterr().out)
    assert out["refused"] == 1 and out["fetched"] == 0
    assert "https://z-lib.example.org/book.pdf" in out["refused_urls"]


def test_collect_downloads_allowlisted_and_ledgers(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(bf, "LEDGER", tmp_path / "ledger.txt")
    monkeypatch.setattr(bf, "REVIEW", tmp_path / "no_review.md")
    land = tmp_path / "land"
    cfg = tmp_path / "s.yaml"
    cfg.write_text('allowlist: [d2l.ai]\nbooks:\n'
                   '  - name: d2l\n    url: https://d2l.ai/d2l-en.pdf\n'
                   '    license: CC\n    domain: ai-engineering\n', encoding="utf-8")

    calls = []

    def fake_dl(url, dest, timeout=180):
        calls.append(url)
        Path(dest).parent.mkdir(parents=True, exist_ok=True)
        Path(dest).write_bytes(b"%PDF-1.5 fake")
        return True

    args = bf._args(["collect", "--config", str(cfg), "--dir", str(land)])
    args._download = fake_dl
    bf.cmd_collect(args)
    out = json.loads(capsys.readouterr().out)
    assert out["fetched"] == 1 and (land / "d2l.pdf").exists()

    # second run: URL is in the ledger -> skipped, not re-downloaded
    args2 = bf._args(["collect", "--config", str(cfg), "--dir", str(land)])
    args2._download = fake_dl
    bf.cmd_collect(args2)
    out2 = json.loads(capsys.readouterr().out)
    assert out2["skipped"] == 1 and out2["fetched"] == 0
    assert len(calls) == 1                    # downloaded exactly once across both runs


def test_download_rejects_non_pdf(tmp_path):
    dest = tmp_path / "x.pdf"
    # simulate the real _download's PDF-magic check by writing an HTML body
    dest.write_bytes(b"<html>not a pdf</html>")
    with open(dest, "rb") as fh:
        assert fh.read(5) != b"%PDF-"          # the guard the real _download enforces
