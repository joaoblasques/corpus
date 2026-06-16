#!/usr/bin/env python3
"""Tests for bin/refetch_links.py — retry high-score fetch-failed email links."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import refetch_links as rfl  # noqa: E402


class FakeFetcher:
    """Injectable stand-in for fetch_link: deterministic, no network."""

    def __init__(self, *, fail_urls=None, text="real article body"):
        self.fail_urls = set(fail_urls or [])
        self.text = text
        self.fetched = []

    def resolve(self, url):
        return url

    def classify(self, url):
        return "article"

    def fetch(self, url):
        if url in self.fail_urls:
            raise RuntimeError("fetch failed again")
        self.fetched.append(url)
        return {"title": "Recovered Article", "text": self.text, "channel": "web"}


def _email(inbox: Path, name: str, links: list[str]) -> Path:
    p = inbox / name
    block = "\n".join(links)
    p.write_text(
        "---\n"
        "channel: email\nsource: gmail\ngmail_message_id: abc123\n"
        "subject: x\ndate_received: 2026-05-17\npointer: true\n"
        "collected_at: 2026-06-11\n"
        f"links:\n{block}\n"
        "---\n\nhttps://example.com/x\n",
        encoding="utf-8",
    )
    return p


# --- parse_links ----------------------------------------------------------

def test_parse_links_reads_fields():
    content = (
        "links:\n"
        '  - {url: "https://github.com/x/y.md", fetched: false, score: 9, reason: fetch-failed}\n'
        "  - {url: https://ok.com, fetched: true, score: 8, file: raw/web/ok.md}\n"
    )
    links = rfl.parse_links(content)
    assert links[0]["url"] == "https://github.com/x/y.md"
    assert links[0]["fetched"] is False
    assert links[0]["score"] == 9
    assert links[0]["reason"] == "fetch-failed"
    assert links[1]["fetched"] is True
    assert links[1]["file"] == "raw/web/ok.md"


# --- refetch_file ---------------------------------------------------------

def test_refetch_file_recovers_high_score_failed(tmp_path):
    inbox = tmp_path / "_inbox"
    inbox.mkdir()
    web = tmp_path / "web"
    yt = tmp_path / "yt"
    p = _email(inbox, "e.md", [
        '  - {url: "https://github.com/x/handbook.md", fetched: false, score: 9, reason: fetch-failed}',
    ])
    fetcher = FakeFetcher()
    res = rfl.refetch_file(p, min_score=7, web_dir=web, yt_dir=yt, root=tmp_path, fetcher=fetcher)

    assert res["refetched"] == 1
    text = p.read_text(encoding="utf-8")
    assert "fetched: true" in text
    assert "fetch-failed" not in text
    assert "file: web/" in text  # companion path recorded
    assert list(web.glob("*.md")), "companion file should be written"


def test_refetch_file_skips_low_score(tmp_path):
    inbox = tmp_path / "_inbox"; inbox.mkdir()
    p = _email(inbox, "e.md", [
        '  - {url: "https://x.com/a", fetched: false, score: 3, reason: fetch-failed}',
    ])
    fetcher = FakeFetcher()
    res = rfl.refetch_file(p, min_score=7, web_dir=tmp_path / "web", yt_dir=tmp_path / "yt",
                           root=tmp_path, fetcher=fetcher)
    assert res["refetched"] == 0
    assert fetcher.fetched == []


def test_refetch_file_skips_non_fetch_failed_reasons(tmp_path):
    inbox = tmp_path / "_inbox"; inbox.mkdir()
    p = _email(inbox, "e.md", [
        '  - {url: "https://x.com/a", fetched: false, score: 9, reason: over-cap}',
        '  - {url: "https://x.com/b", fetched: false, score: 9, reason: low-utility}',
        '  - {url: "https://x.com/c", fetched: false, score: 9, reason: duplicate}',
    ])
    fetcher = FakeFetcher()
    res = rfl.refetch_file(p, min_score=7, web_dir=tmp_path / "web", yt_dir=tmp_path / "yt",
                           root=tmp_path, fetcher=fetcher)
    assert res["refetched"] == 0, "only fetch-failed is retried; budget/utility skips are deliberate"


def test_refetch_file_failure_keeps_failed_marker(tmp_path):
    inbox = tmp_path / "_inbox"; inbox.mkdir()
    url = "https://x.com/still-broken"
    p = _email(inbox, "e.md", [
        f'  - {{url: "{url}", fetched: false, score: 9, reason: fetch-failed}}',
    ])
    fetcher = FakeFetcher(fail_urls={url})
    res = rfl.refetch_file(p, min_score=7, web_dir=tmp_path / "web", yt_dir=tmp_path / "yt",
                           root=tmp_path, fetcher=fetcher)
    assert res["refetched"] == 0
    text = p.read_text(encoding="utf-8")
    assert "fetched: false" in text
    assert "fetch-failed" in text  # marker preserved for a future retry


def test_refetch_file_respects_max(tmp_path):
    inbox = tmp_path / "_inbox"; inbox.mkdir()
    p = _email(inbox, "e.md", [
        '  - {url: "https://x.com/a", fetched: false, score: 9, reason: fetch-failed}',
        '  - {url: "https://x.com/b", fetched: false, score: 9, reason: fetch-failed}',
    ])
    fetcher = FakeFetcher()
    res = rfl.refetch_file(p, min_score=7, max_refetch=1, web_dir=tmp_path / "web",
                           yt_dir=tmp_path / "yt", root=tmp_path, fetcher=fetcher)
    assert res["refetched"] == 1


# --- refetch_inbox --------------------------------------------------------

def test_max_bounds_attempts_not_just_successes(tmp_path):
    """A dead URL consumes the attempt budget — the cap bounds network calls."""
    inbox = tmp_path / "_inbox"; inbox.mkdir()
    dead = "https://x.com/dead"
    good = "https://x.com/good"
    p = _email(inbox, "e.md", [
        f'  - {{url: "{dead}", fetched: false, score: 9, reason: fetch-failed}}',
        f'  - {{url: "{good}", fetched: false, score: 9, reason: fetch-failed}}',
    ])
    fetcher = FakeFetcher(fail_urls={dead})
    res = rfl.refetch_file(p, min_score=7, max_refetch=1, web_dir=tmp_path / "web",
                           yt_dir=tmp_path / "yt", root=tmp_path, fetcher=fetcher)
    # Only the first (dead) link is attempted; budget spent → good URL never tried.
    assert res == {"refetched": 0, "failed": 1}
    assert good not in fetcher.fetched


def test_refetch_inbox_aggregates_and_caps(tmp_path):
    inbox = tmp_path / "_inbox"; inbox.mkdir()
    _email(inbox, "e1.md", ['  - {url: "https://x.com/a", fetched: false, score: 9, reason: fetch-failed}'])
    _email(inbox, "e2.md", ['  - {url: "https://x.com/b", fetched: false, score: 9, reason: fetch-failed}'])
    fetcher = FakeFetcher()
    res = rfl.refetch_inbox(inbox, min_score=7, max_total=1, web_dir=tmp_path / "web",
                            yt_dir=tmp_path / "yt", root=tmp_path, fetcher=fetcher)
    assert res["refetched"] == 1
    assert res["files_scanned"] >= 1
