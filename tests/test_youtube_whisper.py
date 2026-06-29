import sys, importlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
yc = importlib.import_module("youtube_client")


def test_merge_offsets_by_chunk_index():
    chunks = [
        [{"start": 0.0, "text": "a"}, {"start": 5.0, "text": "b"}],
        [{"start": 10.0, "text": "c"}],
    ]
    out = yc._merge_chunk_segments(chunks, 2400)
    assert out == [
        {"start": 0.0, "text": "a"},
        {"start": 5.0, "text": "b"},
        {"start": 2410.0, "text": "c"},
    ]


def test_merge_single_chunk_no_offset():
    chunks = [[{"start": 3.0, "text": "x"}]]
    assert yc._merge_chunk_segments(chunks, 2400) == [{"start": 3.0, "text": "x"}]


def test_groq_key_prefers_env(monkeypatch, tmp_path):
    monkeypatch.setenv("GROQ_API_KEY", "env-key")
    assert yc._groq_key(str(tmp_path / "none.env")) == "env-key"


def test_groq_key_reads_envfile(monkeypatch, tmp_path):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    f = tmp_path / "watch.env"
    f.write_text("# comment\nGROQ_API_KEY=file-key\nOTHER=1\n")
    assert yc._groq_key(str(f)) == "file-key"


def test_groq_key_none_when_absent(monkeypatch, tmp_path):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    assert yc._groq_key(str(tmp_path / "missing.env")) is None


def test_caption_ok_does_not_invoke_whisper(monkeypatch):
    monkeypatch.setenv("CORPUS_YT_BROWSER", "0")
    monkeypatch.setattr(yc, "_caption_transcript", lambda v: ("CAPTIONS", "ok"))
    called = {"n": 0}
    monkeypatch.setattr(yc, "_whisper_transcript", lambda v: called.__setitem__("n", called["n"] + 1) or "W")
    assert yc.extract_transcript("vid") == ("CAPTIONS", "ok")
    assert called["n"] == 0


def test_none_found_uses_whisper(monkeypatch):
    monkeypatch.setattr(yc, "_caption_transcript", lambda v: ("", "none_found"))
    monkeypatch.setattr(yc, "_whisper_enabled", lambda: True)
    monkeypatch.setattr(yc, "_whisper_transcript", lambda v: "WHISPER_MD")
    assert yc.extract_transcript("vid") == ("WHISPER_MD", "ok")


def test_blocked_does_not_use_whisper(monkeypatch):
    monkeypatch.setenv("CORPUS_YT_BROWSER", "0")
    monkeypatch.setattr(yc, "_caption_transcript", lambda v: ("", "blocked"))
    monkeypatch.setattr(yc, "_whisper_enabled", lambda: True)
    monkeypatch.setattr(yc, "_whisper_transcript", lambda v: "WHISPER_MD")
    assert yc.extract_transcript("vid") == ("", "blocked")   # blocked left to retry


def test_whisper_failure_keeps_status(monkeypatch):
    monkeypatch.setattr(yc, "_caption_transcript", lambda v: ("", "disabled"))
    monkeypatch.setattr(yc, "_whisper_enabled", lambda: True)
    monkeypatch.setattr(yc, "_whisper_transcript", lambda v: "")
    assert yc.extract_transcript("vid") == ("", "disabled")


def test_blocked_with_whisper_on_blocked_flag_uses_whisper(monkeypatch):
    monkeypatch.setenv("CORPUS_YT_BROWSER", "0")
    monkeypatch.setattr(yc, "_caption_transcript", lambda v: ("", "blocked"))
    monkeypatch.setattr(yc, "_whisper_enabled", lambda: True)
    monkeypatch.setattr(yc, "_whisper_transcript", lambda v: "WHISPER_MD")
    # last-resort: a refetch-blocked re-attempt still blocked → Whisper
    assert yc.extract_transcript("vid", whisper_on_blocked=True) == ("WHISPER_MD", "ok")
    # default (normal run) still leaves blocked alone
    assert yc.extract_transcript("vid") == ("", "blocked")


def test_ytdlp_cookie_args_env(monkeypatch):
    import youtube_client as yc
    monkeypatch.setenv("CORPUS_YT_COOKIES_BROWSER", "chrome")
    assert yc._ytdlp_cookie_args() == ["--cookies-from-browser", "chrome"]
    monkeypatch.setenv("CORPUS_YT_COOKIES_BROWSER", "")
    assert yc._ytdlp_cookie_args() == []
    monkeypatch.delenv("CORPUS_YT_COOKIES_BROWSER", raising=False)
    assert yc._ytdlp_cookie_args() == ["--cookies-from-browser", "chrome"]  # default
