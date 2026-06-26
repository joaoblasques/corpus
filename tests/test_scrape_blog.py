import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import scrape_blog as sb  # noqa: E402

SITEMAP = """<?xml version="1.0"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://blog.example.com/post-one</loc></url>
  <url><loc>https://blog.example.com/post-two</loc></url>
  <url><loc>https://blog.example.com/tag/python</loc></url>
  <url><loc>https://blog.example.com/author/jane</loc></url>
  <url><loc>https://blog.example.com/</loc></url>
</urlset>"""

SITEMAP_INDEX = """<?xml version="1.0"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://blog.example.com/sitemap-posts.xml</loc></sitemap>
</sitemapindex>"""

RSS = """<?xml version="1.0"?>
<rss version="2.0"><channel>
  <item><link>https://blog.example.com/rss-post-a</link></item>
  <item><link>https://blog.example.com/rss-post-b</link></item>
</channel></rss>"""


def test_discover_blog_posts_from_sitemap_filters_nonposts():
    def session(url):
        return SITEMAP if url == "https://blog.example.com/sitemap.xml" else ""
    out = sb.discover_blog_posts("https://blog.example.com", _session=session)
    assert out == ["https://blog.example.com/post-one", "https://blog.example.com/post-two"]


def test_discover_blog_posts_follows_sitemap_index():
    pages = {
        "https://blog.example.com/sitemap.xml": SITEMAP_INDEX,
        "https://blog.example.com/sitemap-posts.xml": SITEMAP,
    }
    out = sb.discover_blog_posts("https://blog.example.com", _session=lambda u: pages.get(u, ""))
    assert "https://blog.example.com/post-one" in out and "https://blog.example.com/tag/python" not in out


def test_discover_blog_posts_caps():
    def session(url):
        return SITEMAP if url.endswith("/sitemap.xml") else ""
    assert len(sb.discover_blog_posts("https://blog.example.com", cap=1, _session=session)) == 1


def test_discover_blog_posts_rss_fallback_when_no_sitemap():
    def session(url):
        if url.endswith("/sitemap.xml"):
            return ""                       # no sitemap
        if url == "https://blog.example.com":
            return '<html><head></head><body>hi</body></html>'  # no <link> feed hint
        if url == "https://blog.example.com/feed":
            return RSS
        return ""
    out = sb.discover_blog_posts("https://blog.example.com", _session=session)
    assert out == ["https://blog.example.com/rss-post-a", "https://blog.example.com/rss-post-b"]


def test_discover_series_parts_same_path_prefix_in_order():
    index = "https://site.com/guide/intro"
    html = ('<a href="https://site.com/guide/part-1">1</a>'
            '<a href="/guide/part-2">2</a>'
            '<a href="https://other.com/guide/x">no</a>'      # different host
            '<a href="https://site.com/about">no</a>'         # outside prefix
            '<a href="https://site.com/guide/part-1#top">dup</a>')
    out = sb.discover_series_parts(index, _session=lambda u: html)
    assert out == ["https://site.com/guide/part-1", "https://site.com/guide/part-2"]


def test_scrape_seed_writes_dedups_and_counts(tmp_path):
    sitemap = ('<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
               '<url><loc>https://b.com/p1</loc></url>'
               '<url><loc>https://b.com/p2</loc></url></urlset>')
    # p1 already collected: drop a raw source with its source_url into the dedup dir
    (tmp_path / "web-existing.md").write_text(
        "---\nchannel: web\nsource_url: https://b.com/p1\n---\nold\n", encoding="utf-8")

    def session(url):
        return sitemap if url.endswith("/sitemap.xml") else ""

    def fake_fetch(url):
        return {"title": "Title " + url[-2:], "text": "body of " + url}

    res = sb.scrape_seed(
        "https://b.com", "blog", collected_at="2026-06-26",
        via_vault_list="00_Inbox/Clippings/TO SCRAPE.md",
        inbox=tmp_path, dedup_dirs=[tmp_path],
        _session=session, _fetch=fake_fetch)

    assert res == {"seed": "https://b.com", "mode": "blog", "found": 2,
                   "written": 1, "duplicate": 1, "failed": 0, "capped": False}
    written = [p for p in tmp_path.glob("web-*.md") if "existing" not in p.name]
    assert len(written) == 1
    txt = written[0].read_text(encoding="utf-8")
    assert "scrape_seed: https://b.com\n" in txt and "source_url: https://b.com/p2\n" in txt


def test_scrape_seed_counts_fetch_failures(tmp_path):
    sitemap = ('<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
               '<url><loc>https://b.com/p1</loc></url></urlset>')
    res = sb.scrape_seed(
        "https://b.com", "blog", collected_at="2026-06-26",
        via_vault_list="L", inbox=tmp_path, dedup_dirs=[tmp_path],
        _session=lambda u: sitemap if u.endswith("/sitemap.xml") else "",
        _fetch=lambda u: {})   # empty -> failed
    assert res["failed"] == 1 and res["written"] == 0


def test_write_post_same_title_different_url_no_collision(tmp_path):
    """Two posts with identical titles but different source_url must produce
    two separate files (never overwrite each other)."""
    sitemap = ('<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
               '<url><loc>https://b.com/post-a</loc></url>'
               '<url><loc>https://b.com/post-b</loc></url></urlset>')

    # Both posts return SAME title — collision scenario
    def fake_fetch(url):
        return {"title": "Same Title", "text": "body for " + url}

    res = sb.scrape_seed(
        "https://b.com", "blog", collected_at="2026-06-26",
        via_vault_list="00_Inbox/Clippings/TO SCRAPE.md",
        inbox=tmp_path, dedup_dirs=[tmp_path],
        _session=lambda u: sitemap if u.endswith("/sitemap.xml") else "",
        _fetch=fake_fetch)

    assert res["written"] == 2, f"expected 2 written, got {res}"
    written = sorted(tmp_path.glob("web-*.md"))
    assert len(written) == 2, f"expected 2 files, found: {[p.name for p in written]}"
    # Each file must contain its own source_url
    urls_found = set()
    for p in written:
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.startswith("source_url:"):
                urls_found.add(line.split("source_url:", 1)[1].strip())
    assert urls_found == {"https://b.com/post-a", "https://b.com/post-b"}
