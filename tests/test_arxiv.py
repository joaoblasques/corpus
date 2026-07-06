#!/usr/bin/env python3
"""Tests for the arXiv feed pipeline — Atom parse, stub building, dedup, bounded collect."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import collect_arxiv as ca  # noqa: E402
import arxiv_client as ac  # noqa: E402

ATOM = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2607.02383v1</id>
    <published>2026-07-02T00:00:00Z</published>
    <title>Retrieval-Augmented Agents: A Study</title>
    <summary>  We study retrieval-augmented generation for agents.
    It works well.  </summary>
    <author><name>Ada Lovelace</name></author>
    <author><name>Alan Turing</name></author>
    <category term="cs.CL"/>
    <category term="cs.AI"/>
    <link title="pdf" href="https://arxiv.org/pdf/2607.02383v1"/>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2606.11111v2</id>
    <published>2026-06-15T00:00:00Z</published>
    <title>Long Context Windows</title>
    <summary>A method for long context.</summary>
    <author><name>Grace Hopper</name></author>
    <category term="cs.CL"/>
    <link title="pdf" href="https://arxiv.org/pdf/2606.11111v2"/>
  </entry>
</feed>"""


def test_parse_feed_extracts_fields_and_strips_version():
    papers = ca.parse_feed(ATOM)
    assert len(papers) == 2
    p = papers[0]
    assert p["arxiv_id"] == "2607.02383"                     # version suffix stripped
    assert p["title"] == "Retrieval-Augmented Agents: A Study"
    assert p["authors"] == ["Ada Lovelace", "Alan Turing"]
    assert p["categories"] == ["cs.CL", "cs.AI"]
    assert p["published"] == "2026-07-02"
    assert p["abstract"] == "We study retrieval-augmented generation for agents. It works well."
    assert p["pdf_url"] == "https://arxiv.org/pdf/2607.02383v1"


def test_parse_feed_malformed_returns_empty():
    assert ca.parse_feed("<not xml") == []


def test_build_stub_has_channel_and_pointer_and_safe_yaml():
    p = ca.parse_feed(ATOM)[0]
    stub = ca.build_arxiv_stub(p, "ai-engineering", "2026-07-06")
    assert "channel: arxiv" in stub and "arxiv_id: 2607.02383" in stub
    assert "domain_hint: ai-engineering" in stub
    assert 'title: "Retrieval-Augmented Agents: A Study"' in stub   # colon -> quoted scalar
    assert "[pdf](https://arxiv.org/pdf/2607.02383v1)" in stub
    assert "## Abstract" in stub


def test_stub_filename_slug():
    p = ca.parse_feed(ATOM)[0]
    assert ca.stub_filename(p) == "arxiv-2607-02383-retrieval-augmented-agents-a-study.md"


def test_collect_writes_stubs_dedups_and_bounds(tmp_path, monkeypatch, capsys):
    inbox = tmp_path / "_inbox"
    monkeypatch.setattr(ca, "INBOX", inbox)
    monkeypatch.setattr(ca, "DEDUP_DIRS", [inbox])
    cfg = tmp_path / "feeds.yaml"
    cfg.write_text('feeds:\n  - name: t\n    query: cat:cs.CL\n    domain: ai-engineering\n'
                   '    max_results: 5\n', encoding="utf-8")

    args = ac._args(["collect", "--config", str(cfg)])
    args._fetch = lambda url, timeout=40: ATOM
    ac.cmd_collect(args)
    out = json.loads(capsys.readouterr().out)
    assert out["papers"] == 2
    names = sorted(p.name for p in inbox.glob("arxiv-*.md"))
    assert names[0].startswith("arxiv-2606-11111") and names[1].startswith("arxiv-2607-02383")

    # second run: same ids -> all skipped
    args2 = ac._args(["collect", "--config", str(cfg)])
    args2._fetch = lambda url, timeout=40: ATOM
    ac.cmd_collect(args2)
    out2 = json.loads(capsys.readouterr().out)
    assert out2["papers"] == 0 and out2["skipped"] == 2


def test_collect_max_bounds_total(tmp_path, monkeypatch, capsys):
    inbox = tmp_path / "_inbox"
    monkeypatch.setattr(ca, "INBOX", inbox)
    monkeypatch.setattr(ca, "DEDUP_DIRS", [inbox])
    cfg = tmp_path / "feeds.yaml"
    cfg.write_text('feeds:\n  - name: t\n    query: cat:cs.CL\n    domain: ai-engineering\n', encoding="utf-8")
    args = ac._args(["collect", "--config", str(cfg), "--max", "1"])
    args._fetch = lambda url, timeout=40: ATOM
    ac.cmd_collect(args)
    out = json.loads(capsys.readouterr().out)
    assert out["papers"] == 1                                 # capped at --max
