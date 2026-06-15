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
