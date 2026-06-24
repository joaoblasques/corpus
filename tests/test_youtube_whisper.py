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
