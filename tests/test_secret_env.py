from __future__ import annotations
import stat
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import secret_env  # noqa: E402

import pytest


def test_env_var_materialized_to_0600_temp_file(tmp_path, monkeypatch):
    monkeypatch.setenv("MYSECRET", '{"token": "abc"}')
    fallback = tmp_path / "nope.json"
    out = secret_env.materialize_secret("MYSECRET", fallback)
    assert out != fallback
    assert out.read_text(encoding="utf-8") == '{"token": "abc"}'
    mode = stat.S_IMODE(out.stat().st_mode)
    assert mode == 0o600, f"expected 0600, got {oct(mode)}"


def test_falls_back_to_existing_file_when_env_absent(tmp_path, monkeypatch):
    monkeypatch.delenv("MYSECRET", raising=False)
    fallback = tmp_path / "token.json"
    fallback.write_text("{}", encoding="utf-8")
    out = secret_env.materialize_secret("MYSECRET", fallback)
    assert out == fallback


def test_empty_env_var_treated_as_absent(tmp_path, monkeypatch):
    monkeypatch.setenv("MYSECRET", "")
    fallback = tmp_path / "token.json"
    fallback.write_text("{}", encoding="utf-8")
    assert secret_env.materialize_secret("MYSECRET", fallback) == fallback


def test_raises_when_neither_env_nor_file(tmp_path, monkeypatch):
    monkeypatch.delenv("MYSECRET", raising=False)
    with pytest.raises(FileNotFoundError):
        secret_env.materialize_secret("MYSECRET", tmp_path / "missing.json")
