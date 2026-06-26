from __future__ import annotations
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import x_client  # noqa: E402


def test_load_token_prefers_env(monkeypatch):
    monkeypatch.setenv("X_TOKEN_JSON", '{"access_token": "live", "refresh_token": "r"}')
    tok = x_client._load_token()
    assert tok["access_token"] == "live"


def test_load_token_falls_back_to_file(tmp_path, monkeypatch):
    monkeypatch.delenv("X_TOKEN_JSON", raising=False)
    fake = tmp_path / "x_token.json"
    fake.write_text('{"access_token": "fromfile"}', encoding="utf-8")
    monkeypatch.setattr(x_client, "TOKEN", fake)
    tok = x_client._load_token()
    assert tok["access_token"] == "fromfile"


def test_load_token_none_when_neither(tmp_path, monkeypatch):
    monkeypatch.delenv("X_TOKEN_JSON", raising=False)
    monkeypatch.setattr(x_client, "TOKEN", tmp_path / "missing.json")
    assert x_client._load_token() is None
