import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import collect_youtube as cy  # noqa: E402


def test_resolve_policy_listed():
    cfg = {"playlists": [{"id": "PL1", "policy": "collect-remove"},
                         {"id": "PL2", "policy": "collect-keep"}],
           "default_policy": "ignore"}
    assert cy.resolve_policy("PL1", cfg) == "collect-remove"
    assert cy.resolve_policy("PL2", cfg) == "collect-keep"


def test_resolve_policy_unlisted_uses_default():
    cfg = {"playlists": [], "default_policy": "ignore"}
    assert cy.resolve_policy("PLX", cfg) == "ignore"


def test_load_policy_config_missing_file(tmp_path):
    cfg = cy.load_policy_config(tmp_path / "nope.yaml")
    assert cfg == {"playlists": [], "default_policy": "ignore"}


def test_load_policy_config_parses(tmp_path):
    p = tmp_path / "pl.yaml"
    p.write_text("playlists:\n  - id: PL1\n    name: AI\n    policy: collect-remove\n"
                 "default_policy: ignore\n", encoding="utf-8")
    cfg = cy.load_policy_config(p)
    assert cfg["playlists"][0]["id"] == "PL1"
    assert cy.resolve_policy("PL1", cfg) == "collect-remove"
