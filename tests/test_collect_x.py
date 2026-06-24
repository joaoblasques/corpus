import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import collect_x as cx  # noqa: E402

POST = {"id": "1810", "url": "https://x.com/jack/status/1810", "author": "jack",
        "created_at": "2026-06-20T10:00:00Z", "text": "A thread about agents.",
        "links": ["https://example.com/a"], "articles": [{"url": "https://example.com/a", "text": "Article body"}]}


def test_slugify():
    assert cx.slugify("1810") == "x-1810"


def test_build_document_frontmatter_and_body():
    d = cx.build_document(POST, collected_at="2026-06-24")
    assert "channel: x" in d and "tweet_id: 1810" in d and "author: jack" in d
    assert "links: [https://example.com/a]" in d
    assert "A thread about agents." in d and "## Linked articles" in d and "Article body" in d


def test_write_then_dedup(tmp_path):
    d = tmp_path / "_inbox"
    r1 = cx.write_collected(POST, collected_at="2026-06-24", inbox=d, dedup_dirs=[d])
    assert r1["status"] == "written" and Path(r1["path"]).name == "x-1810.md"
    r2 = cx.write_collected(POST, collected_at="2026-06-24", inbox=d, dedup_dirs=[d])
    assert r2["status"] == "duplicate"


def test_reapable_gates_on_ingested_and_channel(tmp_path):
    d = tmp_path / "x"; d.mkdir()
    (d / "x-1.md").write_text("---\nchannel: x\ntweet_id: 1\ncorpus_ingested: true\n---\n", encoding="utf-8")
    (d / "x-2.md").write_text("---\nchannel: x\ntweet_id: 2\n---\n", encoding="utf-8")          # not ingested
    (d / "n-3.md").write_text("---\nchannel: notes\ntweet_id: 3\ncorpus_ingested: true\n---\n", encoding="utf-8")  # wrong channel
    assert cx.reapable(dirs=[d]) == ["1"]
