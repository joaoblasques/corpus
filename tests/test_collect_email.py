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
