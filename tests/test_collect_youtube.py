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


def test_target_filename(tmp_path):
    p = cy.target_filename("VID123", "My Talk!", tmp_path)
    assert p.name == "youtube-VID123-my-talk.md"


def test_build_document_frontmatter():
    doc = cy.build_document({
        "video_id": "VID123", "title": "My: Talk", "channel_name": "Chan",
        "published": "2026-06-01", "playlist": "AI", "transcript_status": "ok",
        "collected_at": "2026-06-12",
    }, "[00:00](https://youtu.be/VID123?t=0) hi")
    assert "channel: youtube" in doc
    assert "youtube_video_id: VID123" in doc
    assert "url: https://youtu.be/VID123" in doc
    assert 'title: "My: Talk"' in doc
    assert "transcript_status: ok" in doc
    assert doc.rstrip().endswith("hi")


def test_build_document_no_transcript_note():
    doc = cy.build_document({
        "video_id": "V", "title": "T", "channel_name": "", "published": "",
        "playlist": "AI", "transcript_status": "disabled", "collected_at": "2026-06-12",
    }, "")
    assert "_No transcript available._" in doc


def test_already_collected_and_status(tmp_path):
    d = tmp_path / "inbox"; d.mkdir()
    (d / "youtube-VID9-x.md").write_text(
        "---\nyoutube_video_id: VID9\ntranscript_status: ok\n---\nbody\n", encoding="utf-8")
    assert cy.already_collected("VID9", [d]) is True
    assert cy.already_collected("NOPE", [d]) is False
    assert cy.collected_status("VID9", [d]) == "ok"
    assert cy.collected_status("NOPE", [d]) is None


def _seed(dirs_parent, video_id, status):
    d = dirs_parent / "inbox"
    d.mkdir(exist_ok=True)
    (d / f"youtube-{video_id}-x.md").write_text(
        f"---\nyoutube_video_id: {video_id}\ntranscript_status: {status}\n---\nbody\n",
        encoding="utf-8")
    return d


def test_should_collect_never_collected(tmp_path):
    d = _seed(tmp_path, "VID1", "ok")
    assert cy.should_collect("NEW", refetch_blocked=False, dirs=[d]) is True
    assert cy.should_collect("NEW", refetch_blocked=True, dirs=[d]) is True


def test_should_collect_ok_is_skipped(tmp_path):
    d = _seed(tmp_path, "OKV", "ok")
    assert cy.should_collect("OKV", refetch_blocked=False, dirs=[d]) is False
    assert cy.should_collect("OKV", refetch_blocked=True, dirs=[d]) is False


def test_should_collect_blocked_only_refetched_with_flag(tmp_path):
    d = _seed(tmp_path, "BLK", "blocked")
    # default: a blocked stub still counts as collected (current behavior preserved)
    assert cy.should_collect("BLK", refetch_blocked=False, dirs=[d]) is False
    # with the flag: a blocked stub is re-fetched
    assert cy.should_collect("BLK", refetch_blocked=True, dirs=[d]) is True


def test_should_collect_disabled_never_refetched(tmp_path):
    # 'disabled' = genuinely no captions; never worth retrying even with the flag
    d = _seed(tmp_path, "DIS", "disabled")
    assert cy.should_collect("DIS", refetch_blocked=True, dirs=[d]) is False
