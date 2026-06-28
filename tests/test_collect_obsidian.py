import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import collect_obsidian as co  # noqa: E402


def test_is_included_resources():
    # PARA-native folders are now EXCLUDED from collect->delete (kept in place)
    assert co.is_included("03_Resources/Articles/Clean Code.md") is False
    assert co.is_included("03_Resources/Study Notes/CAP.md") is False
    # Newly collected folders
    assert co.is_included("Clippings/Introducing routines in Claude Code.md") is True
    assert co.is_included("06_Metadata/Reference/note_taking_protocol.md") is True
    # Still-collected folders
    assert co.is_included("00_Inbox/Clippings/scrape/merkle-trees-scrape.md") is True
    assert co.is_included("03_Resources/Books/cheatsheet.md") is True
    # Snippets / Prompt Templates removed from the watch-list (folders don't exist in the vault)
    assert co.is_included("03_Resources/Snippets/Enrich Notes Script.md") is False
    assert co.is_included("03_Resources/Prompt Templates/foo.md") is False


def test_is_included_excludes():
    assert co.is_included("03_Resources/llm-wiki-system/CLAUDE.md") is False
    assert co.is_included("01_Projects/foo.md") is False
    assert co.is_included("00_Inbox/Clippings/articles_processed.md") is False
    assert co.is_included("06_Metadata/Templates/Daily-Note-Template.md") is False
    assert co.is_included("06_Metadata/SETUP_COMPLETE.md") is False
    assert co.is_included("06_Metadata/Reference/README.md") is False
    assert co.is_included("03_Resources/Books/cheatsheet.pdf") is False


def test_classify():
    assert co.classify("00_Inbox/Clippings/articles to process.md") == "url-list"
    assert co.classify("00_Inbox/Clippings/blogs to scrape.md") == "url-list"
    assert co.classify("03_Resources/Articles/Clean Code.md") == "note"


def test_parse_url_list():
    text = "\nhttps://a.com/x\n\nsome prose\nhttps://b.com/y?z=1\nhttps://a.com/x\n"
    assert co.parse_url_list(text) == ["https://a.com/x", "https://b.com/y?z=1"]


def test_read_note_extracts_title_tags_body(tmp_path):
    f = tmp_path / "n.md"
    f.write_text('---\ntitle: "Hello"\nsource: "https://ex.com/a"\ntags:\n  - x\n  - y\n---\nBody here\n')
    title, tags, source_url, body = co.read_note(str(f))
    assert title == "Hello"
    assert tags == ["x", "y"]
    assert source_url == "https://ex.com/a"
    assert body.strip() == "Body here"


def test_read_note_no_frontmatter_uses_stem(tmp_path):
    f = tmp_path / "My Note.md"
    f.write_text("Just text, no frontmatter")
    title, tags, source_url, body = co.read_note(str(f))
    assert title == "My Note"
    assert tags == []
    assert source_url == ""
    assert body.strip() == "Just text, no frontmatter"


def test_note_filename(tmp_path):
    p = co.note_filename("03_Resources/Books/Clean Code!.md", tmp_path)
    assert p.name == "notes-03-resources-books-clean-code.md"
    # same title, different folder -> different raw filename (collision fixed)
    a = co.note_filename("Clippings/Routines.md", tmp_path)
    b = co.note_filename("00_Inbox/Clippings/Routines.md", tmp_path)
    assert a.name == "notes-clippings-routines.md"
    assert b.name == "notes-00-inbox-clippings-routines.md"
    assert a.name != b.name


def test_build_note_source():
    doc = co.build_note_source(
        {"vault_origin": "03_Resources/Articles/Clean Code.md", "title": "Clean: Code",
         "tags": ["python"], "collected_at": "2026-06-12"}, "Body text.")
    assert "channel: notes" in doc
    assert "source: obsidian" in doc
    assert "vault_origin: 03_Resources/Articles/Clean Code.md" in doc
    assert 'title: "Clean: Code"' in doc
    assert "  - python" in doc
    assert doc.rstrip().endswith("Body text.")


def test_build_url_source():
    doc = co.build_url_source(
        {"source_url": "https://a.com/x", "via_vault_list": "00_Inbox/Clippings/articles to process.md",
         "title": "A", "collected_at": "2026-06-12"}, "Article body")
    assert "channel: web" in doc
    assert "source_url: https://a.com/x" in doc
    assert "via_vault_list: 00_Inbox/Clippings/articles to process.md" in doc
    assert doc.rstrip().endswith("Article body")


def test_build_url_source_via_vault_note():
    doc = co.build_url_source(
        {"source_url": "https://a.com/x", "via_vault_note": "Clippings/Routines.md",
         "title": "X", "collected_at": "2026-06-17"}, "body text")
    assert "channel: web" in doc
    assert "via_vault_note: Clippings/Routines.md" in doc
    assert "via_vault_list:" not in doc


def test_fm_field():
    assert co.fm_field("---\nvault_origin: a/b.md\n---\n", "vault_origin") == "a/b.md"
    assert co.fm_field("no fm", "vault_origin") is None


def test_is_vault_note_ingested(tmp_path):
    a = tmp_path / "a.md"; a.write_text("---\ncorpus_ingested: true\n---\nx", encoding="utf-8")
    b = tmp_path / "b.md"; b.write_text("---\ntitle: x\n---\ny", encoding="utf-8")
    assert co.is_vault_note_ingested(str(a)) is True
    assert co.is_vault_note_ingested(str(b)) is False


def test_frontmatter_extracts_only_leading_block():
    assert co._frontmatter("---\na: 1\n---\nbody x\n") == "a: 1"
    assert co._frontmatter("no fm at all") == ""
    assert co._frontmatter("---\na: 1\nno closing fence") == ""


def test_is_vault_note_ingested_ignores_body(tmp_path):
    # corpus_ingested in BODY (after closing ---) must not count as ingested
    f = tmp_path / "a.md"
    f.write_text("---\ntitle: x\n---\nThis article discusses corpus_ingested: true in the system.\n",
                 encoding="utf-8")
    assert co.is_vault_note_ingested(str(f)) is False


def test_fm_field_ignores_body():
    # a body line that literally starts with `vault_origin:` (e.g. a code block in
    # an article about this very system) must NOT be picked up
    text = "---\ntitle: x\n---\nExample frontmatter:\nvault_origin: 03_Resources/Articles/WRONG.md\n"
    assert co.fm_field(text, "vault_origin") is None
    # real frontmatter value is still returned
    assert co.fm_field("---\nvault_origin: a/b.md\n---\nbody", "vault_origin") == "a/b.md"


def test_reapable_ignores_body_vault_origin(tmp_path):
    raw = tmp_path / "raw"; raw.mkdir()
    (raw / "n.md").write_text(
        "---\ncorpus_ingested: true\n---\nExample frontmatter:\nvault_origin: 03_Resources/Articles/WRONG.md\n",
        encoding="utf-8")
    r = co.reapable([raw])
    assert "03_Resources/Articles/WRONG.md" not in r["vault_notes"]


def test_already_collected_vault(tmp_path):
    d = tmp_path / "inbox"; d.mkdir()
    (d / "notes-x.md").write_text("---\nvault_origin: 03_Resources/Articles/X.md\n---\n", encoding="utf-8")
    assert co.already_collected_vault("03_Resources/Articles/X.md", [d]) is True
    assert co.already_collected_vault("03_Resources/Articles/Y.md", [d]) is False


def test_url_already_collected(tmp_path):
    d = tmp_path / "web"; d.mkdir()
    (d / "web-x.md").write_text("---\nsource_url: https://a.com/x\n---\n", encoding="utf-8")
    assert co.url_already_collected("https://a.com/x", [d]) is True
    assert co.url_already_collected("https://a.com/z", [d]) is False


def _vault(tmp_path):
    v = tmp_path / "vault"
    (v / "03_Resources/Articles").mkdir(parents=True)
    (v / "03_Resources/Books").mkdir(parents=True)
    (v / "03_Resources/llm-wiki-system").mkdir(parents=True)
    (v / "00_Inbox/Clippings").mkdir(parents=True)
    (v / "01_Projects").mkdir(parents=True)
    (v / "03_Resources/Books/New.md").write_text("---\ntitle: New\n---\nbody", encoding="utf-8")
    (v / "03_Resources/Books/Done.md").write_text("---\ncorpus_ingested: true\n---\nx", encoding="utf-8")
    (v / "03_Resources/Articles/Para.md").write_text("---\ntitle: Para\n---\nbody", encoding="utf-8")
    (v / "03_Resources/llm-wiki-system/CLAUDE.md").write_text("mirror", encoding="utf-8")
    (v / "01_Projects/task.md").write_text("task", encoding="utf-8")
    (v / "00_Inbox/Clippings/articles to process.md").write_text("https://a.com/x\n", encoding="utf-8")
    return v


def test_discover_filters(tmp_path):
    v = _vault(tmp_path)
    found = co.discover(v, dedup_dirs=[tmp_path / "none"])
    rels = {(d["rel_path"], d["kind"]) for d in found}
    assert ("03_Resources/Books/New.md", "note") in rels
    assert ("00_Inbox/Clippings/articles to process.md", "url-list") in rels
    assert "03_Resources/Books/Done.md" not in {r for r, _ in rels}              # already ingested
    assert "03_Resources/Articles/Para.md" not in {r for r, _ in rels}           # PARA-native, now excluded
    assert "03_Resources/llm-wiki-system/CLAUDE.md" not in {r for r, _ in rels}  # excluded
    assert "01_Projects/task.md" not in {r for r, _ in rels}                     # not a knowledge dir


def test_discover_skips_already_collected(tmp_path):
    v = _vault(tmp_path)
    raw = tmp_path / "raw"; raw.mkdir()
    (raw / "notes-new.md").write_text("---\nvault_origin: 03_Resources/Books/New.md\n---\n", encoding="utf-8")
    rels = {d["rel_path"] for d in co.discover(v, dedup_dirs=[raw])}
    assert "03_Resources/Books/New.md" not in rels   # already collected → skipped


def test_reapable_selects_only_ingested(tmp_path):
    raw = tmp_path / "raw"; raw.mkdir()
    (raw / "notes-a.md").write_text("---\ncorpus_ingested: true\nvault_origin: 03_Resources/Articles/A.md\n---\n", encoding="utf-8")
    (raw / "notes-b.md").write_text("---\nvault_origin: 03_Resources/Articles/B.md\n---\n", encoding="utf-8")  # NOT ingested
    (raw / "web-u.md").write_text("---\ncorpus_ingested: true\nvia_vault_list: 00_Inbox/Clippings/articles to process.md\nsource_url: https://a.com/x\n---\n", encoding="utf-8")
    r = co.reapable([raw])
    assert r["vault_notes"] == ["03_Resources/Articles/A.md"]                 # B excluded (not ingested)
    assert r["url_strikes"] == [("00_Inbox/Clippings/articles to process.md", "https://a.com/x")]


def _src(scrape_seed=None, ingested=False, via="00_Inbox/Clippings/TO SCRAPE.md",
         source_url="https://b.com/p"):
    fm = ["---", "channel: web", f"source_url: {source_url}", f"via_vault_list: {via}"]
    if scrape_seed:
        fm.append(f"scrape_seed: {scrape_seed}")
    if ingested:
        fm.append("corpus_ingested: true")
    fm += ["---", "", "body", ""]
    return "\n".join(fm)


def test_reapable_seed_strikeable_only_when_all_posts_ingested(tmp_path):
    seed = "https://b.com"
    (tmp_path / "p1.md").write_text(_src(seed, ingested=True, source_url="https://b.com/p1"), encoding="utf-8")
    (tmp_path / "p2.md").write_text(_src(seed, ingested=False, source_url="https://b.com/p2"), encoding="utf-8")
    r = co.reapable([tmp_path])
    assert (("00_Inbox/Clippings/TO SCRAPE.md", seed) not in r["seed_strikes"])   # p2 not ingested

    (tmp_path / "p2.md").write_text(_src(seed, ingested=True, source_url="https://b.com/p2"), encoding="utf-8")
    r = co.reapable([tmp_path])
    assert ("00_Inbox/Clippings/TO SCRAPE.md", seed) in r["seed_strikes"]         # all ingested


def test_is_watch_list_keyed_by_basename():
    assert co.is_watch_list("00_Inbox/Clippings/blogs to scrape.md") is True
    assert co.is_watch_list("blogs to scrape.md") is True            # any folder
    assert co.is_watch_list("00_Inbox/Clippings/articles to process.md") is False
    assert co.is_watch_list("00_Inbox/Clippings/TO SCRAPE.md") is False
    assert co.is_watch_list(None) is False and co.is_watch_list("") is False


def test_reapable_never_strikes_watch_list_seed_even_when_all_ingested(tmp_path):
    # 'blogs to scrape.md' is a watch list: its seed stays forever so the blog is
    # re-scraped for new posts. Even with every post ingested, the seed is NOT struck.
    seed = "https://watched-blog.com"
    via = "00_Inbox/Clippings/blogs to scrape.md"
    (tmp_path / "p1.md").write_text(
        _src(seed, ingested=True, via=via, source_url="https://watched-blog.com/p1"), encoding="utf-8")
    (tmp_path / "p2.md").write_text(
        _src(seed, ingested=True, via=via, source_url="https://watched-blog.com/p2"), encoding="utf-8")
    r = co.reapable([tmp_path])
    assert (via, seed) not in r["seed_strikes"]    # watch list -> never struck
    assert r["seed_strikes"] == []


def test_reapable_excludes_scrape_posts_from_url_strikes(tmp_path):
    (tmp_path / "p1.md").write_text(_src("https://b.com", ingested=True, source_url="https://b.com/p1"), encoding="utf-8")
    r = co.reapable([tmp_path])
    assert ("00_Inbox/Clippings/TO SCRAPE.md", "https://b.com/p1") not in r["url_strikes"]


def test_extract_inline_links_basic_dedup():
    body = "See https://a.com/x and again https://a.com/x and https://b.com/y."
    r = co.extract_inline_links(body)
    assert r["links"] == ["https://a.com/x", "https://b.com/y"]
    assert r["auth_skipped"] == 0
    assert r["dropped"] == 0


def test_extract_inline_links_skips_source_assets_auth():
    body = ("source repeated https://src.com/post "
            "image ![alt](https://c.com/pic.png) "
            "doc https://c.com/file.pdf "
            "social https://www.linkedin.com/in/x "
            "good https://good.com/article")
    r = co.extract_inline_links(body, source_url="https://src.com/post")
    assert r["links"] == ["https://good.com/article"]
    assert r["auth_skipped"] == 1  # linkedin


def test_extract_inline_links_respects_cap():
    body = " ".join(f"https://s{i}.com/a" for i in range(15))
    r = co.extract_inline_links(body)
    assert len(r["links"]) == co.MAX_LINKS_PER_NOTE
    assert r["dropped"] == 5


def test_parse_scrape_tag_blog_series_and_untagged():
    assert co.parse_scrape_tag("https://blog.example.com [blog]") == {
        "url": "https://blog.example.com", "mode": "blog", "cap": 25}
    assert co.parse_scrape_tag("https://blog.example.com [blog:50]") == {
        "url": "https://blog.example.com", "mode": "blog", "cap": 50}
    assert co.parse_scrape_tag("- https://site.com/the-series  [series]") == {
        "url": "https://site.com/the-series", "mode": "series", "cap": 25}
    assert co.parse_scrape_tag("https://plain.example.com/post") == {
        "url": "https://plain.example.com/post", "mode": None, "cap": 25}
    assert co.parse_scrape_tag("no url here [blog]")["url"] == ""


def test_iter_scrape_targets_dedups_and_preserves_order():
    text = ("https://a.com [blog]\n"
            "- https://b.com/series [series]\n"
            "https://c.com/post\n"
            "https://a.com [blog:5]\n")   # dup url, first tag wins
    out = co.iter_scrape_targets(text)
    assert [t["url"] for t in out] == ["https://a.com", "https://b.com/series", "https://c.com/post"]
    assert out[0] == {"url": "https://a.com", "mode": "blog", "cap": 25}
    assert out[1]["mode"] == "series"
    assert out[2]["mode"] is None


def test_build_url_source_includes_scrape_seed_when_present():
    out = co.build_url_source({
        "source_url": "https://b.com/p1", "via_vault_list": "00_Inbox/Clippings/TO SCRAPE.md",
        "scrape_seed": "https://b.com", "title": "P1", "collected_at": "2026-06-26"}, "body")
    assert "scrape_seed: https://b.com\n" in out
    assert "source_url: https://b.com/p1\n" in out
    assert "via_vault_list: 00_Inbox/Clippings/TO SCRAPE.md\n" in out


def test_build_url_source_omits_scrape_seed_when_absent():
    out = co.build_url_source({
        "source_url": "https://b.com/p1", "via_vault_list": "L", "collected_at": "2026-06-26"}, "body")
    assert "scrape_seed" not in out


# --- blogs-to-scrape default mode + filename rename (2026-06-27) ---

def test_url_list_names_renamed_to_blogs_to_scrape():
    assert "blogs to scrape.md" in co.URL_LIST_NAMES
    assert "TO SCRAPE.md" not in co.URL_LIST_NAMES
    assert "articles to process.md" in co.URL_LIST_NAMES


def test_list_default_mode_blogs_vs_articles():
    assert co.list_default_mode("00_Inbox/Clippings/blogs to scrape.md") == "blog"
    assert co.list_default_mode("00_Inbox/Clippings/articles to process.md") is None
    assert co.list_default_mode("00_Inbox/Clippings/other.md") is None


def test_iter_scrape_targets_applies_default_mode():
    text = "https://a.com\nhttps://b.com [series]\nhttps://c.com [blog:5]\n"
    out = co.iter_scrape_targets(text, default_mode="blog")
    assert out[0] == {"url": "https://a.com", "mode": "blog", "cap": 25}   # untagged -> default
    assert out[1]["mode"] == "series"                                       # explicit tag wins
    assert out[2] == {"url": "https://c.com", "mode": "blog", "cap": 5}     # explicit blog:N


def test_iter_scrape_targets_default_none_keeps_single_page():
    out = co.iter_scrape_targets("https://a.com\n")   # default None -> single-page
    assert out[0]["mode"] is None
