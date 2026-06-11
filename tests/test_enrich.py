import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import gmail_client as gc  # noqa: E402
import rank_links as rl  # noqa: E402


# C1: enrich_email must never raise — a ranking error must not abort the run loop.
def test_enrich_email_returns_dict_when_ranking_raises(tmp_path, monkeypatch):
    email = tmp_path / "email.md"
    email.write_text(
        "---\nchannel: email\nsubject: Hi\n---\n\n"
        "A great read https://blog.example.com/post\n",
        encoding="utf-8",
    )

    def boom(_candidates):
        raise RuntimeError("malformed .env / ranking blew up")

    monkeypatch.setattr(rl, "score_candidates", boom)

    result = gc.enrich_email(
        str(email), "MSG1", email.read_text(encoding="utf-8"),
        "2026-06-11", max_links=5,
    )
    assert isinstance(result, dict)
    assert result == {"captured": 0, "skipped": 0}


# C1: rank_links.load_env must not raise on an unreadable/malformed .env path.
def test_load_env_swallows_read_errors(tmp_path, monkeypatch):
    # Point load_env at a directory (read_text raises OSError) — must return, not raise.
    bad = tmp_path / "envdir"
    bad.mkdir()
    rl.load_env(str(bad))  # should not raise
