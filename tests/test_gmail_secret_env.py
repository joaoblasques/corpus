from __future__ import annotations
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import gmail_client  # noqa: E402


def test_token_resolves_from_env(monkeypatch):
    monkeypatch.setenv("GMAIL_TOKEN_JSON", '{"refresh_token": "x"}')
    p = gmail_client._resolve_token()
    assert p.read_text(encoding="utf-8") == '{"refresh_token": "x"}'


def test_credentials_resolve_from_env(monkeypatch):
    monkeypatch.setenv("GMAIL_CREDENTIALS_JSON", '{"installed": {}}')
    p = gmail_client._resolve_credentials()
    assert p.read_text(encoding="utf-8") == '{"installed": {}}'


def test_token_falls_back_to_file_when_env_absent(tmp_path, monkeypatch):
    monkeypatch.delenv("GMAIL_TOKEN_JSON", raising=False)
    fake = tmp_path / "token.json"
    fake.write_text('{"from": "file"}', encoding="utf-8")
    monkeypatch.setattr(gmail_client, "TOKEN", fake)
    p = gmail_client._resolve_token()
    assert p == fake
    assert p.read_text(encoding="utf-8") == '{"from": "file"}'
