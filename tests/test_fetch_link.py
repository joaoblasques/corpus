import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import fetch_link as fl  # noqa: E402


def test_youtube_id_variants():
    assert fl.youtube_id("https://www.youtube.com/watch?v=abc123XYZ_-") == "abc123XYZ_-"
    assert fl.youtube_id("https://youtu.be/abc123XYZ_-") == "abc123XYZ_-"
    assert fl.youtube_id("https://example.com/article") is None


def test_classify():
    assert fl.classify("https://youtu.be/abc123XYZ_-") == "youtube"
    assert fl.classify("https://example.com/whitepaper.pdf") == "unsupported"
    assert fl.classify("https://blog.example.com/post") == "article"
    assert fl.classify("ftp://x") == "unsupported"


def test_extract_article_from_html():
    html = (
        "<html><head><title>RAG Patterns</title></head><body>"
        "<article><h1>RAG Patterns</h1>"
        "<p>" + ("Retrieval augmented generation explained in depth. " * 20) + "</p>"
        "</article></body></html>"
    )
    out = fl.extract_article(html, "https://blog.example.com/rag")
    assert out["channel"] == "web"
    assert "Retrieval augmented generation" in out["text"]
    assert out["title"]


# --- GitHub blob → raw rewrite (fetch markdown/code as plain text) --------

class _Resp:
    def __init__(self, text, url):
        self.text = text
        self.url = url

    def raise_for_status(self):
        pass


class _Client:
    def __init__(self, text):
        self._text = text
        self.got = []

    def get(self, url):
        self.got.append(url)
        return _Resp(self._text, url)

    def close(self):
        pass


def test_github_raw_rewrite():
    assert (fl.github_raw("https://github.com/o/r/blob/main/docs/intro.md")
            == "https://raw.githubusercontent.com/o/r/main/docs/intro.md")
    # fragment and query stripped
    assert (fl.github_raw("https://github.com/o/r/blob/main/a.md#L5")
            == "https://raw.githubusercontent.com/o/r/main/a.md")
    assert fl.github_raw("https://github.com/o/r") is None  # not a blob
    assert fl.github_raw("https://example.com/x/blob/y") is None  # not github


def test_raw_text_url_routes_blob_and_raw_hosts():
    assert (fl.raw_text_url("https://github.com/o/r/blob/main/a.md")
            == "https://raw.githubusercontent.com/o/r/main/a.md")
    raw = "https://raw.githubusercontent.com/o/r/main/a.md"
    assert fl.raw_text_url(raw) == raw  # already raw → fetched as text directly
    assert fl.raw_text_url("https://gist.githubusercontent.com/o/abc/raw/x.py").endswith("x.py")
    assert fl.raw_text_url("https://blog.example.com/post") is None  # normal article


def test_fetch_text_returns_markdown_body():
    client = _Client("# Handbook\n\n" + ("real bootcamp markdown content. " * 10))
    out = fl.fetch_text("https://raw.githubusercontent.com/o/r/main/intro.md", client=client)
    assert out["channel"] == "web"
    assert "bootcamp markdown content" in out["text"]
    assert out["title"] == "intro.md"


def test_fetch_text_empty_raises():
    import pytest
    with pytest.raises(ValueError):
        fl.fetch_text("https://raw.githubusercontent.com/o/r/main/x.md", client=_Client("   \n"))


def test_fetch_routes_github_blob_through_raw(monkeypatch):
    seen = {}

    def fake_fetch_text(url, orig=None, client=None):
        seen["url"] = url
        return {"title": "x", "text": "body", "channel": "web"}

    monkeypatch.setattr(fl, "fetch_text", fake_fetch_text)
    out = fl.fetch("https://github.com/DataExpert-io/data-engineer-handbook/blob/main/bootcamp/introduction.md")
    assert seen["url"] == "https://raw.githubusercontent.com/DataExpert-io/data-engineer-handbook/main/bootcamp/introduction.md"
    assert out["channel"] == "web"
