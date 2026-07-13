#!/usr/bin/env python3
"""Tests for blog_discover — cited-but-unscraped discovery + [x]-promote to the scrape list."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import blog_discover as bd  # noqa: E402


def _web(dir_: Path, host: str, n: int):
    dir_.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        (dir_ / f"web-{host.replace('.', '-')}-{i}.md").write_text(
            f"---\nchannel: web\nsource_url: https://{host}/post-{i}\n---\nx", encoding="utf-8")


def test_candidate_domains_counts_and_filters(tmp_path):
    web = tmp_path / "web"
    _web(web, "goodblog.dev", 4)
    _web(web, "rareblog.io", 1)                 # below min_cited
    _web(web, "youtube.com", 5)                 # ignored aggregator
    cands = dict(bd.candidate_domains(web, bd.DEFAULT_IGNORE, min_cited=3))
    assert cands.get("goodblog.dev") == 4
    assert "rareblog.io" not in cands and "youtube.com" not in cands


def test_collect_writes_review_dedups_scraped_and_ledger(tmp_path, monkeypatch, capsys):
    web = tmp_path / "web"
    _web(web, "goodblog.dev", 5)
    _web(web, "alreadyscraped.com", 4)
    monkeypatch.setattr(bd, "WEB", web)
    monkeypatch.setattr(bd, "REVIEW", tmp_path / "Blogs to review.md")
    monkeypatch.setattr(bd, "LEDGER", tmp_path / ".ledger")
    scrape = tmp_path / "blogs to scrape.md"
    scrape.write_text("https://alreadyscraped.com/\n", encoding="utf-8")   # already watched
    monkeypatch.setattr(bd, "SCRAPE_LIST", scrape)
    cfg = tmp_path / "c.yaml"
    cfg.write_text("min_cited: 3\nmax_new_per_run: 10\n", encoding="utf-8")

    bd.cmd_collect(bd._args(["collect", "--config", str(cfg)]))
    out = json.loads(capsys.readouterr().out)
    assert out["proposed"] == 1                              # goodblog only; alreadyscraped excluded
    review = (tmp_path / "Blogs to review.md").read_text()
    assert "- [ ] https://goodblog.dev/ · cited 5x" in review
    assert "alreadyscraped.com" not in review

    # second run: goodblog now in the ledger -> not re-proposed
    bd.cmd_collect(bd._args(["collect", "--config", str(cfg)]))
    assert json.loads(capsys.readouterr().out)["proposed"] == 0


def test_promote_appends_only_ticked_and_dedups(tmp_path, monkeypatch, capsys):
    review = tmp_path / "Blogs to review.md"
    review.write_text(
        "- [x] https://ticked.dev/ · cited 9x\n"
        "- [ ] https://skipme.io/ · cited 4x\n"
        "- [x] https://already.com/ · cited 5x\n", encoding="utf-8")
    scrape = tmp_path / "blogs to scrape.md"
    scrape.write_text("https://already.com/\n", encoding="utf-8")          # already in list
    monkeypatch.setattr(bd, "REVIEW", review)
    monkeypatch.setattr(bd, "SCRAPE_LIST", scrape)

    bd.cmd_promote(bd._args(["promote"]))
    out = json.loads(capsys.readouterr().out)
    assert out["promoted"] == 1                              # ticked.dev only
    text = scrape.read_text()
    assert "https://ticked.dev/" in text                     # appended
    assert "https://skipme.io/" not in text                  # unticked stays out
    assert text.count("https://already.com/") == 1           # not duplicated


def test_collect_dry_run_writes_nothing(tmp_path, monkeypatch, capsys):
    web = tmp_path / "web"; _web(web, "goodblog.dev", 5)
    monkeypatch.setattr(bd, "WEB", web)
    monkeypatch.setattr(bd, "REVIEW", tmp_path / "Blogs to review.md")
    monkeypatch.setattr(bd, "LEDGER", tmp_path / ".ledger")
    monkeypatch.setattr(bd, "SCRAPE_LIST", tmp_path / "blogs to scrape.md")
    cfg = tmp_path / "c.yaml"; cfg.write_text("min_cited: 3\n", encoding="utf-8")
    bd.cmd_collect(bd._args(["collect", "--config", str(cfg), "--dry-run"]))
    assert json.loads(capsys.readouterr().out)["proposed"] == 1
    assert not (tmp_path / "Blogs to review.md").exists()    # dry-run: no file written
