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
