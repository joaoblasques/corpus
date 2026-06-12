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


def test_hms():
    assert cy.hms(65) == "01:05"
    assert cy.hms(3725) == "01:02:05"


def test_ts_anchor():
    assert cy.ts_anchor(90, "abc123") == "[01:30](https://youtu.be/abc123?t=90)"


def test_clean_snippets_drops_empty_dups_and_noise():
    snips = [{"start": 0, "text": "Hello"}, {"start": 2, "text": "Hello"},
             {"start": 4, "text": "[Music]"}, {"start": 6, "text": " World \n"}]
    out = cy.clean_snippets(snips)
    assert [s["text"] for s in out] == ["Hello", "World"]


def test_group_snippets_windows():
    snips = [{"start": 0, "text": "a"}, {"start": 10, "text": "b"}, {"start": 30, "text": "c"}]
    groups = cy.group_snippets(snips, window=25)
    assert [g["texts"] for g in groups] == [["a", "b"], ["c"]]
    assert groups[1]["start"] == 30


def test_transcript_to_markdown():
    snips = [{"start": 0, "text": "intro"}, {"start": 30, "text": "next"}]
    md = cy.transcript_to_markdown(snips, "vid", window=25)
    assert "[00:00](https://youtu.be/vid?t=0) intro" in md
    assert "[00:30](https://youtu.be/vid?t=30) next" in md


def test_dedup_vtt_strips_tags_and_rolling_dups():
    vtt = (
        "WEBVTT\n\n"
        "00:00:00.000 --> 00:00:02.000\n"
        "<c>hello</c> there\n\n"
        "00:00:02.000 --> 00:00:04.000\n"
        "hello there\n\n"                # rolling duplicate of previous cue
        "00:00:04.000 --> 00:00:06.000\n"
        "next line\n"
    )
    snips = cy.dedup_vtt(vtt)
    assert [s["text"] for s in snips] == ["hello there", "next line"]
    assert snips[0]["start"] == 0 and snips[1]["start"] == 4
