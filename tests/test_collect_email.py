import json
import sys
from pathlib import Path

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
