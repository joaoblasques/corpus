import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import collect_email as ce  # noqa: E402


def test_slugify_basic():
    assert ce.slugify("Hello World") == "hello-world"


def test_slugify_strips_punctuation_and_collapses():
    assert ce.slugify("Re: [Newsletter] AI & You!!") == "re-newsletter-ai-you"


def test_slugify_truncates_without_trailing_hyphen():
    out = ce.slugify("a" * 80, max_len=10)
    assert out == "a" * 10


def test_slugify_empty_is_untitled():
    assert ce.slugify("!!!") == "untitled"


def test_detect_pointer_true_for_bare_link():
    ok, url = ce.detect_pointer("Check this out: https://example.com/article")
    assert ok is True
    assert url == "https://example.com/article"


def test_detect_pointer_false_for_prose_newsletter():
    body = "Welcome to the weekly digest. " * 20 + "More at https://example.com"
    ok, url = ce.detect_pointer(body)
    assert ok is False
    assert url is None


def test_detect_pointer_false_when_no_url():
    ok, url = ce.detect_pointer("Just some text, no links here.")
    assert ok is False
    assert url is None


def test_already_collected_finds_existing(tmp_path):
    d = tmp_path / "inbox"
    d.mkdir()
    (d / "email-2026-06-09-x.md").write_text(
        "---\ngmail_message_id: ABC123\n---\nbody\n", encoding="utf-8"
    )
    assert ce.already_collected("ABC123", [d]) is True


def test_already_collected_absent(tmp_path):
    d = tmp_path / "inbox"
    d.mkdir()
    assert ce.already_collected("NOPE", [d]) is False


def test_already_collected_ignores_missing_dirs(tmp_path):
    assert ce.already_collected("X", [tmp_path / "does-not-exist"]) is False


def _meta(**over):
    base = {
        "gmail_message_id": "ABC123",
        "from": "Jane Doe <jane@example.com>",
        "subject": "Hello: a test",
        "date_received": "2026-06-09",
        "collected_at": "2026-06-09",
        "pointer": False,
        "url": None,
    }
    base.update(over)
    return base


def test_yaml_scalar_quotes_colon():
    assert ce.yaml_scalar("Hello: world") == '"Hello: world"'


def test_yaml_scalar_plain_passthrough():
    assert ce.yaml_scalar("just text") == "just text"


def test_build_document_has_frontmatter_and_body():
    doc = ce.build_document(_meta(), "The body text.")
    assert doc.startswith("---\n")
    assert "channel: email" in doc
    assert "gmail_message_id: ABC123" in doc
    assert 'subject: "Hello: a test"' in doc
    assert "pointer: false" in doc
    assert doc.rstrip().endswith("The body text.")


def test_build_document_includes_url_when_pointer():
    doc = ce.build_document(_meta(pointer=True, url="https://x.com"), "https://x.com")
    assert "url: https://x.com" in doc
    assert "pointer: true" in doc


def test_target_filename_collision_appends_id(tmp_path):
    first = ce.target_filename("2026-06-09", "Hello: a test", "ABC123", tmp_path)
    first.write_text("x", encoding="utf-8")
    second = ce.target_filename("2026-06-09", "Hello: a test", "ZZZ999", tmp_path)
    assert first != second
    assert "email-2026-06-09-hello-a-test" in first.name
    assert "zzz999" in second.name


def test_write_collected_writes_file(tmp_path):
    inbox = tmp_path / "_inbox"
    res = ce.write_collected(_meta(), "Newsletter body here.", inbox=inbox, dedup_dirs=[inbox])
    assert res["status"] == "written"
    p = Path(res["path"])
    assert p.exists()
    assert "gmail_message_id: ABC123" in p.read_text(encoding="utf-8")


def test_write_collected_dedup_skips(tmp_path):
    inbox = tmp_path / "_inbox"
    ce.write_collected(_meta(), "body", inbox=inbox, dedup_dirs=[inbox])
    res2 = ce.write_collected(_meta(), "body", inbox=inbox, dedup_dirs=[inbox])
    assert res2["status"] == "duplicate"
    assert len(list(inbox.glob("*.md"))) == 1


def test_write_collected_sets_pointer(tmp_path):
    inbox = tmp_path / "_inbox"
    res = ce.write_collected(
        _meta(gmail_message_id="PTR1"), "https://example.com/x", inbox=inbox, dedup_dirs=[inbox]
    )
    assert res["pointer"] is True
    assert res["url"] == "https://example.com/x"


def test_cli_writes_and_prints_json(tmp_path, monkeypatch, capsys):
    inbox = tmp_path / "_inbox"
    monkeypatch.setattr(ce, "INBOX", inbox)
    monkeypatch.setattr(ce, "DEDUP_DIRS", [inbox])
    body_file = tmp_path / "body.md"
    body_file.write_text("Hello body", encoding="utf-8")
    rc = ce.main([
        "--message-id", "CLI1", "--from", "a@b.com", "--subject", "Subj",
        "--date", "2026-06-09", "--collected-at", "2026-06-09",
        "--body-file", str(body_file),
    ])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["status"] == "written"
    assert Path(out["path"]).exists()


# Fix 1: dedup needle prefix bug — short id must not false-match a longer one
def test_already_collected_no_prefix_match(tmp_path):
    d = tmp_path / "inbox"
    d.mkdir()
    (d / "email-2026-06-09-x.md").write_text(
        "---\ngmail_message_id: ABC123\n---\nbody\n", encoding="utf-8"
    )
    # "ABC12" is a strict prefix of "ABC123" — must NOT be treated as collected
    assert ce.already_collected("ABC12", [d]) is False


# Fix 2: tabs in yaml_scalar must be normalized to spaces
def test_yaml_scalar_no_tab():
    result = ce.yaml_scalar("a\tb")
    assert "\t" not in result


# Fix 4: yaml_scalar("") returns '""'
def test_yaml_scalar_empty_returns_quoted_empty():
    assert ce.yaml_scalar("") == '""'


# Fix 3: CLI returns 1 and prints error JSON when body-file does not exist
def test_cli_error_on_missing_body_file(tmp_path, monkeypatch, capsys):
    inbox = tmp_path / "_inbox"
    monkeypatch.setattr(ce, "INBOX", inbox)
    monkeypatch.setattr(ce, "DEDUP_DIRS", [inbox])
    missing = str(tmp_path / "does_not_exist.md")
    rc = ce.main([
        "--message-id", "ERR1", "--from", "a@b.com", "--subject", "Subj",
        "--date", "2026-06-09", "--collected-at", "2026-06-09",
        "--body-file", missing,
    ])
    assert rc == 1
    out = json.loads(capsys.readouterr().out)
    assert out["status"] == "error"
    assert "error" in out


def test_select_links_extracts_url_and_description():
    body = "Agentic AI Flywheels [ https://news.example.com/flywheels ] (15 min read)\nHow evals create a flywheel."
    links = ce.select_links(body)
    assert len(links) == 1
    assert links[0]["url"] == "https://news.example.com/flywheels"
    assert "Agentic AI Flywheels" in links[0]["description"]


def test_select_links_drops_noise():
    body = ("Unsubscribe https://list.example.com/unsubscribe?id=9\n"
            "Follow us https://twitter.com/example\n"
            "Real article https://blog.example.com/post")
    urls = [l["url"] for l in ce.select_links(body)]
    assert urls == ["https://blog.example.com/post"]


def test_select_links_dedups():
    body = "A https://x.example.com/a\nB https://x.example.com/a"
    assert len(ce.select_links("https://x.example.com/a " + body)) == 1


def test_select_links_skips_images():
    assert ce.select_links("logo https://cdn.example.com/logo.png") == []


def test_heuristic_score_boosts_learning_and_github():
    s = ce.heuristic_score("https://github.com/org/rag-toolkit", "A practical RAG tutorial")
    assert s >= 8


def test_heuristic_score_penalizes_news():
    s = ce.heuristic_score("https://news.example.com/x", "NVIDIA announces new data center, raises $40M")
    assert s <= 3


def test_heuristic_score_clamped_0_10():
    assert 0 <= ce.heuristic_score("https://x.example.com", "") <= 10


def test_build_link_document_has_provenance():
    doc = ce.build_link_document(
        {"channel": "web", "source_url": "https://x.example.com/a",
         "via_email": "MSG1", "score": 9, "collected_at": "2026-06-11"},
        "Article body text.",
    )
    assert "channel: web" in doc
    assert "source_url: https://x.example.com/a" in doc
    assert "via_email: MSG1" in doc
    assert "utility_score: 9" in doc
    assert doc.rstrip().endswith("Article body text.")


def test_link_target_slugifies_title(tmp_path):
    p = ce.link_target("RAG Patterns!", tmp_path)
    assert p.name == "rag-patterns.md"


# I3: 3+ same-title links must yield distinct files even when the hint collides
# (same hint, or empty hint) — the old single-collision-level logic overwrote.
def test_link_target_three_collisions_are_distinct(tmp_path):
    hint = "https://a.example.com/rag"  # identical hint each time -> worst case
    paths = []
    for _ in range(3):
        p = ce.link_target("RAG Patterns", tmp_path, hint)
        p.write_text("x", encoding="utf-8")  # materialize so the next call collides
        paths.append(p)
    assert len(set(paths)) == 3
    assert all(p.exists() for p in paths)
    # Every distinct path is its own file — nothing was overwritten.
    assert len(list(tmp_path.glob("*.md"))) == 3


def test_add_links_frontmatter_inserts_block(tmp_path):
    f = tmp_path / "email.md"
    f.write_text("---\nchannel: email\nsubject: Hi\n---\n\nBody\n", encoding="utf-8")
    ce.add_links_frontmatter(str(f), [
        {"url": "https://x.example.com/a", "score": 9, "file": "raw/web/a.md", "reason": None},
        {"url": "https://x.example.com/b", "score": 2, "file": None, "reason": "low-utility"},
    ])
    out = f.read_text(encoding="utf-8")
    assert "links:" in out
    assert "fetched: true" in out and "file: raw/web/a.md" in out
    assert "reason: low-utility" in out
    assert out.index("links:") < out.index("\n---")  # inside frontmatter
    assert out.rstrip().endswith("Body")


# I2: a url with YAML-special chars (comma, braces, colon) must stay valid YAML.
def test_add_links_frontmatter_quotes_special_url(tmp_path):
    f = tmp_path / "email.md"
    f.write_text("---\nchannel: email\nsubject: Hi\n---\n\nBody\n", encoding="utf-8")
    url = "https://ex.com/a?x={1,2}:b,c"
    ce.add_links_frontmatter(str(f), [
        {"url": url, "score": 7, "file": url, "reason": None},
    ])
    out = f.read_text(encoding="utf-8")
    frontmatter = out.split("---", 2)[1]
    data = yaml.safe_load(frontmatter)
    assert data["links"][0]["url"] == url
    assert data["links"][0]["file"] == url


def test_build_document_emits_corpus_labels():
    doc = ce.build_document(
        {"gmail_message_id": "abc", "from": "a@b.c", "subject": "S",
         "date_received": "2026-06-18", "collected_at": "2026-06-18",
         "gmail_corpus_labels": ["Data Engineering", "MLOps"]},
        "body")
    assert "gmail_corpus_labels:\n  - Data Engineering\n  - MLOps" in doc


def test_build_document_omits_corpus_labels_when_absent():
    doc = ce.build_document(
        {"gmail_message_id": "abc", "from": "a@b.c", "subject": "S",
         "date_received": "2026-06-18", "collected_at": "2026-06-18"}, "body")
    assert "gmail_corpus_labels" not in doc


def test_labeled_reapable_selects_ingested_labeled(tmp_path):
    d = tmp_path / "raw"; d.mkdir()
    (d / "email-ingested.md").write_text(
        "---\nchannel: email\ngmail_message_id: m1\n"
        "gmail_corpus_labels:\n  - MLOps\n  - Ml\ncorpus_ingested: true\n---\nbody",
        encoding="utf-8")
    (d / "email-not-ingested.md").write_text(  # has labels but not ingested
        "---\ngmail_message_id: m2\ngmail_corpus_labels:\n  - MLOps\n---\nx", encoding="utf-8")
    (d / "email-starred.md").write_text(  # ingested but no corpus labels (starred)
        "---\ngmail_message_id: m3\ncorpus_ingested: true\n---\nx", encoding="utf-8")
    out = ce.labeled_reapable(dirs=[d])
    assert out == [{"gmail_message_id": "m1", "gmail_corpus_labels": ["MLOps", "Ml"]}]


def test_build_document_to_labeled_reapable_roundtrip(tmp_path):
    """End-to-end seam: a source produced by build_document (then ingest-stamped) is
    selected by labeled_reapable with the SAME labels — the write<->parse contract."""
    d = tmp_path / "raw"; d.mkdir()
    doc = ce.build_document(
        {"gmail_message_id": "rt1", "from": "a@b.c", "subject": "S",
         "date_received": "2026-06-18", "collected_at": "2026-06-18",
         "gmail_corpus_labels": ["Data Engineering", "MLOps"]}, "body")
    doc = doc.replace("\n---\n", "\ncorpus_ingested: true\n---\n", 1)  # simulate ingest stamp
    (d / "email-rt.md").write_text(doc, encoding="utf-8")
    assert ce.labeled_reapable(dirs=[d]) == [
        {"gmail_message_id": "rt1", "gmail_corpus_labels": ["Data Engineering", "MLOps"]}]


def test_labeled_reapable_gates_on_frontmatter_not_body(tmp_path):
    d = tmp_path / "raw"; d.mkdir()
    # labeled, NOT ingested, but the BODY quotes the stamp string -> must be EXCLUDED
    (d / "email-x.md").write_text(
        "---\ngmail_message_id: m9\ngmail_corpus_labels:\n  - MLOps\n---\n"
        "body that quotes corpus_ingested: true somewhere\n", encoding="utf-8")
    assert ce.labeled_reapable(dirs=[d]) == []
