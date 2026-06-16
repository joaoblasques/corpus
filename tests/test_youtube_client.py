import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import youtube_client as yc  # noqa: E402


class _FakeReq:
    def __init__(self, resp): self._resp = resp
    def execute(self): return self._resp


def test_list_playlist_items_maps_fields():
    svc = MagicMock()
    svc.playlistItems().list.return_value = _FakeReq({
        "items": [{
            "id": "ITEM1",
            "snippet": {"title": "Vid A", "resourceId": {"videoId": "VA"},
                        "videoOwnerChannelTitle": "Chan A"},
            "contentDetails": {"videoPublishedAt": "2026-06-01T00:00:00Z"},
            "status": {"privacyStatus": "public"},
        }]})
    svc.playlistItems().list_next.return_value = None
    items = list(yc.list_playlist_items(svc, "PL1"))
    assert items[0]["playlist_item_id"] == "ITEM1"
    assert items[0]["video_id"] == "VA"
    assert items[0]["published"] == "2026-06-01"


def test_list_playlist_items_skips_malformed(monkeypatch):
    # I1: first item lacks resourceId (deleted/private) -> skipped, not a KeyError.
    svc = MagicMock()
    svc.playlistItems().list.return_value = _FakeReq({
        "items": [
            {"id": "BAD", "snippet": {"title": "Gone"}},  # no resourceId
            {"id": "ITEM2",
             "snippet": {"title": "Vid B", "resourceId": {"videoId": "VB"},
                         "videoOwnerChannelTitle": "Chan B"},
             "contentDetails": {"videoPublishedAt": "2026-06-02T00:00:00Z"},
             "status": {"privacyStatus": "public"}},
        ]})
    svc.playlistItems().list_next.return_value = None
    items = list(yc.list_playlist_items(svc, "PL1"))
    assert len(items) == 1
    assert items[0]["video_id"] == "VB"


def test_delete_playlist_item_404_is_success():
    from googleapiclient.errors import HttpError
    svc = MagicMock()
    resp = MagicMock(); resp.status = 404
    svc.playlistItems().delete.return_value.execute.side_effect = HttpError(resp, b"gone")
    assert yc.delete_playlist_item(svc, "ITEM1") is True


def test_extract_transcript_disabled(monkeypatch):
    # Force the youtube_transcript_api path to raise TranscriptsDisabled
    import youtube_transcript_api as yta
    class FakeApi:
        def fetch(self, *a, **k): raise yta._errors.TranscriptsDisabled("V")
    monkeypatch.setattr(yc, "_transcript_api", lambda: FakeApi())
    body, status = yc.extract_transcript("V")
    assert body == "" and status == "disabled"


def test_extract_transcript_ok(monkeypatch):
    class Snip:
        def __init__(self, s, t): self.start, self.text = s, t
    class FakeApi:
        def fetch(self, vid, languages=None): return [Snip(0, "hello"), Snip(30, "world")]
    monkeypatch.setattr(yc, "_transcript_api", lambda: FakeApi())
    body, status = yc.extract_transcript("VID")
    assert status == "ok"
    assert "hello" in body and "world" in body


def test_extract_transcript_inner_block_falls_through_to_ytdlp(monkeypatch):
    # M2: fetch raises NoTranscriptFound, then api.list() raises a blocked-type error.
    # The inner branch must fall through to yt-dlp rather than returning none_found.
    import youtube_transcript_api as yta

    class FakeApi:
        def fetch(self, *a, **k): raise yta._errors.NoTranscriptFound("V", [], None)
        def list(self, *a, **k): raise yta._errors.RequestBlocked("V")
    monkeypatch.setattr(yc, "_transcript_api", lambda: FakeApi())
    monkeypatch.setattr(yc, "_ytdlp_transcript", lambda vid: "[00:00](x) recovered")
    body, status = yc.extract_transcript("V")
    assert status == "ok"
    assert "recovered" in body


def test_extract_transcript_inner_block_ytdlp_empty(monkeypatch):
    # M2: blocked in inner branch and yt-dlp yields nothing -> "blocked", not "none_found".
    import youtube_transcript_api as yta

    class FakeApi:
        def fetch(self, *a, **k): raise yta._errors.NoTranscriptFound("V", [], None)
        def list(self, *a, **k): raise yta._errors.RequestBlocked("V")
    monkeypatch.setattr(yc, "_transcript_api", lambda: FakeApi())
    monkeypatch.setattr(yc, "_ytdlp_transcript", lambda vid: "")
    body, status = yc.extract_transcript("V")
    assert body == "" and status == "blocked"


def test_run_collects_and_removes_only_with_transcript(tmp_path, monkeypatch):
    # one tech playlist, two videos: one with transcript (removed), one without (kept)
    monkeypatch.setattr(yc.cy, "INBOX", tmp_path)
    monkeypatch.setattr(yc.cy, "DEDUP_DIRS", [tmp_path])
    monkeypatch.setattr(yc, "load_config", lambda: {
        "playlists": [{"id": "PL1", "name": "AI", "policy": "collect-remove"}],
        "default_policy": "ignore"})
    monkeypatch.setattr(yc, "get_service", lambda: "SVC")
    monkeypatch.setattr(yc, "list_playlist_items", lambda svc, pid: iter([
        {"playlist_item_id": "I1", "video_id": "V1", "title": "A", "channel_name": "C",
         "published": "2026-06-01", "privacy": "public"},
        {"playlist_item_id": "I2", "video_id": "V2", "title": "B", "channel_name": "C",
         "published": "2026-06-01", "privacy": "public"}]))
    monkeypatch.setattr(yc, "extract_transcript",
                        lambda vid: ("[00:00](x) hi", "ok") if vid == "V1" else ("", "disabled"))
    deleted = []
    monkeypatch.setattr(yc, "delete_playlist_item", lambda svc, iid: deleted.append(iid) or True)

    args = yc._args(["run", "--sleep", "0"])
    rc = yc.cmd_run(args)
    assert rc == 0
    assert deleted == ["I1"]                      # only the one WITH a transcript removed
    assert (tmp_path / "youtube-V1-a.md").exists()
    assert (tmp_path / "youtube-V2-b.md").exists()  # kept, recorded with disabled status


def test_run_stops_on_quota_error(tmp_path, monkeypatch):
    # I2: a 403 quota/rate-limit HttpError from delete must stop the run gracefully,
    # not get swallowed as failed+continue. Second video's delete is never attempted.
    from googleapiclient.errors import HttpError
    monkeypatch.setattr(yc.cy, "INBOX", tmp_path)
    monkeypatch.setattr(yc.cy, "DEDUP_DIRS", [tmp_path])
    monkeypatch.setattr(yc, "load_config", lambda: {
        "playlists": [{"id": "PL1", "name": "AI", "policy": "collect-remove"}],
        "default_policy": "ignore"})
    monkeypatch.setattr(yc, "get_service", lambda: "SVC")
    monkeypatch.setattr(yc, "list_playlist_items", lambda svc, pid: iter([
        {"playlist_item_id": "I1", "video_id": "V1", "title": "A", "channel_name": "C",
         "published": "2026-06-01", "privacy": "public"},
        {"playlist_item_id": "I2", "video_id": "V2", "title": "B", "channel_name": "C",
         "published": "2026-06-01", "privacy": "public"}]))
    monkeypatch.setattr(yc, "extract_transcript", lambda vid: ("[00:00](x) hi", "ok"))
    attempted = []

    def fake_delete(svc, iid):
        attempted.append(iid)
        resp = MagicMock(); resp.status = 403
        raise HttpError(resp, b"quotaExceeded")
    monkeypatch.setattr(yc, "delete_playlist_item", fake_delete)
    rc = yc.cmd_run(yc._args(["run", "--sleep", "0"]))
    assert rc == 0
    assert attempted == ["I1"]  # stopped after first; second delete never attempted


def test_run_unknown_status_duplicate_not_removed(tmp_path, monkeypatch):
    # C1: a prior file matches the dedup needle but has NO transcript_status line.
    # collected_status -> None; the delete guard must fail closed (not delete).
    monkeypatch.setattr(yc.cy, "INBOX", tmp_path)
    monkeypatch.setattr(yc.cy, "DEDUP_DIRS", [tmp_path])
    (tmp_path / "youtube-V1-a.md").write_text(
        "---\nyoutube_video_id: V1\n---\n\nbody\n", encoding="utf-8")
    monkeypatch.setattr(yc, "load_config", lambda: {
        "playlists": [{"id": "PL1", "name": "AI", "policy": "collect-remove"}],
        "default_policy": "ignore"})
    monkeypatch.setattr(yc, "get_service", lambda: "SVC")
    monkeypatch.setattr(yc, "list_playlist_items", lambda svc, pid: iter([
        {"playlist_item_id": "I1", "video_id": "V1", "title": "A", "channel_name": "C",
         "published": "2026-06-01", "privacy": "public"}]))
    deleted = []
    monkeypatch.setattr(yc, "delete_playlist_item", lambda svc, iid: deleted.append(iid) or True)
    rc = yc.cmd_run(yc._args(["run", "--sleep", "0"]))
    assert rc == 0
    assert deleted == []  # unknown-status duplicate must NOT be removed


def test_run_refetch_blocked_reextracts_and_removes(tmp_path, monkeypatch):
    # A prior 'blocked' stub for V1 exists (rate-limit artifact). With --refetch-blocked
    # the run re-extracts; the transcript now succeeds, the stub is overwritten to status
    # 'ok', and (collect-remove) the video is finally removed.
    monkeypatch.setattr(yc.cy, "INBOX", tmp_path)
    monkeypatch.setattr(yc.cy, "DEDUP_DIRS", [tmp_path])
    (tmp_path / "youtube-V1-a.md").write_text(
        "---\nyoutube_video_id: V1\ntranscript_status: blocked\n---\n\n_No transcript available._\n",
        encoding="utf-8")
    monkeypatch.setattr(yc, "load_config", lambda: {
        "playlists": [{"id": "PL1", "name": "AI", "policy": "collect-remove"}],
        "default_policy": "ignore"})
    monkeypatch.setattr(yc, "get_service", lambda: "SVC")
    monkeypatch.setattr(yc, "list_playlist_items", lambda svc, pid: iter([
        {"playlist_item_id": "I1", "video_id": "V1", "title": "A", "channel_name": "C",
         "published": "2026-06-01", "privacy": "public"}]))
    monkeypatch.setattr(yc, "extract_transcript", lambda vid: ("[00:00](x) recovered", "ok"))
    deleted = []
    monkeypatch.setattr(yc, "delete_playlist_item", lambda svc, iid: deleted.append(iid) or True)
    rc = yc.cmd_run(yc._args(["run", "--refetch-blocked", "--sleep", "0"]))
    assert rc == 0
    assert deleted == ["I1"]                                          # re-fetched -> ok -> removed
    assert "recovered" in (tmp_path / "youtube-V1-a.md").read_text()  # stub overwritten


def test_run_blocked_stub_not_refetched_by_default(tmp_path, monkeypatch):
    # Without the flag, a blocked stub stays a duplicate: not re-fetched, not removed.
    monkeypatch.setattr(yc.cy, "INBOX", tmp_path)
    monkeypatch.setattr(yc.cy, "DEDUP_DIRS", [tmp_path])
    (tmp_path / "youtube-V1-a.md").write_text(
        "---\nyoutube_video_id: V1\ntranscript_status: blocked\n---\n\n_No transcript available._\n",
        encoding="utf-8")
    monkeypatch.setattr(yc, "load_config", lambda: {
        "playlists": [{"id": "PL1", "name": "AI", "policy": "collect-remove"}],
        "default_policy": "ignore"})
    monkeypatch.setattr(yc, "get_service", lambda: "SVC")
    monkeypatch.setattr(yc, "list_playlist_items", lambda svc, pid: iter([
        {"playlist_item_id": "I1", "video_id": "V1", "title": "A", "channel_name": "C",
         "published": "2026-06-01", "privacy": "public"}]))
    called = []
    monkeypatch.setattr(yc, "extract_transcript", lambda vid: called.append(vid) or ("x", "ok"))
    deleted = []
    monkeypatch.setattr(yc, "delete_playlist_item", lambda svc, iid: deleted.append(iid) or True)
    rc = yc.cmd_run(yc._args(["run", "--sleep", "0"]))
    assert rc == 0
    assert called == [] and deleted == []   # blocked stub left untouched


def test_run_dry_run_never_deletes(tmp_path, monkeypatch):
    monkeypatch.setattr(yc.cy, "INBOX", tmp_path)
    monkeypatch.setattr(yc.cy, "DEDUP_DIRS", [tmp_path])
    monkeypatch.setattr(yc, "load_config", lambda: {
        "playlists": [{"id": "PL1", "name": "AI", "policy": "collect-remove"}], "default_policy": "ignore"})
    monkeypatch.setattr(yc, "get_service", lambda: "SVC")
    monkeypatch.setattr(yc, "list_playlist_items", lambda svc, pid: iter([
        {"playlist_item_id": "I1", "video_id": "V1", "title": "A", "channel_name": "C",
         "published": "2026-06-01", "privacy": "public"}]))
    monkeypatch.setattr(yc, "extract_transcript", lambda vid: ("[00:00](x) hi", "ok"))
    deleted = []
    monkeypatch.setattr(yc, "delete_playlist_item", lambda svc, iid: deleted.append(iid) or True)
    rc = yc.cmd_run(yc._args(["run", "--dry-run", "--sleep", "0"]))
    assert rc == 0 and deleted == []


def test_run_sleeps_after_fetch(tmp_path, monkeypatch):
    # A fresh video is fetched -> throttle (sleep) once.
    monkeypatch.setattr(yc.cy, "INBOX", tmp_path)
    monkeypatch.setattr(yc.cy, "DEDUP_DIRS", [tmp_path])
    monkeypatch.setattr(yc, "load_config", lambda: {
        "playlists": [{"id": "PL1", "name": "AI", "policy": "collect-keep"}],
        "default_policy": "ignore"})
    monkeypatch.setattr(yc, "get_service", lambda: "SVC")
    monkeypatch.setattr(yc, "list_playlist_items", lambda svc, pid: iter([
        {"playlist_item_id": "I1", "video_id": "VNEW", "title": "A", "channel_name": "C",
         "published": "2026-06-01", "privacy": "public"}]))
    monkeypatch.setattr(yc, "extract_transcript", lambda vid: ("[00:00](x) hi", "ok"))
    slept = []
    monkeypatch.setattr(yc.time, "sleep", lambda s: slept.append(s))
    rc = yc.cmd_run(yc._args(["run", "--sleep", "2"]))
    assert rc == 0
    assert slept == [2.0], "must throttle after a real fetch"


def test_run_no_sleep_on_duplicate(tmp_path, monkeypatch):
    # A previously-collected video is a duplicate -> no fetch -> no sleep (fast).
    monkeypatch.setattr(yc.cy, "INBOX", tmp_path)
    monkeypatch.setattr(yc.cy, "DEDUP_DIRS", [tmp_path])
    (tmp_path / "youtube-VDUP-x.md").write_text(
        "---\nyoutube_video_id: VDUP\ntranscript_status: ok\n---\nbody\n", encoding="utf-8")
    monkeypatch.setattr(yc, "load_config", lambda: {
        "playlists": [{"id": "PL1", "name": "AI", "policy": "collect-keep"}],
        "default_policy": "ignore"})
    monkeypatch.setattr(yc, "get_service", lambda: "SVC")
    monkeypatch.setattr(yc, "list_playlist_items", lambda svc, pid: iter([
        {"playlist_item_id": "I1", "video_id": "VDUP", "title": "A", "channel_name": "C",
         "published": "2026-06-01", "privacy": "public"}]))

    def _boom(vid):
        raise AssertionError("must not fetch a duplicate")
    monkeypatch.setattr(yc, "extract_transcript", _boom)
    slept = []
    monkeypatch.setattr(yc.time, "sleep", lambda s: slept.append(s))
    rc = yc.cmd_run(yc._args(["run", "--sleep", "2"]))
    assert rc == 0
    assert slept == [], "duplicates must not be throttled (no fetch happened)"


def _seed_blocked(tmp_path, *vids):
    for vid in vids:
        (tmp_path / f"youtube-{vid}-x.md").write_text(
            f"---\nyoutube_video_id: {vid}\ntranscript_status: blocked\n---\n"
            "_No transcript available._\n", encoding="utf-8")


def _blocked_run_setup(tmp_path, monkeypatch, vids):
    monkeypatch.setattr(yc.cy, "INBOX", tmp_path)
    monkeypatch.setattr(yc.cy, "DEDUP_DIRS", [tmp_path])
    _seed_blocked(tmp_path, *vids)
    monkeypatch.setattr(yc, "load_config", lambda: {
        "playlists": [{"id": "PL1", "name": "AI", "policy": "collect-keep"}],
        "default_policy": "ignore"})
    monkeypatch.setattr(yc, "get_service", lambda: "SVC")
    monkeypatch.setattr(yc, "list_playlist_items", lambda svc, pid: iter([
        {"playlist_item_id": f"I{i}", "video_id": v, "title": "A", "channel_name": "C",
         "published": "2026-06-01", "privacy": "public"} for i, v in enumerate(vids)]))
    monkeypatch.setattr(yc.time, "sleep", lambda s: None)
    calls = []
    monkeypatch.setattr(yc, "extract_transcript",
                        lambda vid: calls.append(vid) or ("[00:00](x) hi", "ok"))
    return calls


def test_run_refetch_max_caps_refetches(tmp_path, monkeypatch):
    calls = _blocked_run_setup(tmp_path, monkeypatch, ["VB1", "VB2", "VB3"])
    rc = yc.cmd_run(yc._args(["run", "--refetch-blocked", "--refetch-max", "1", "--sleep", "0"]))
    assert rc == 0
    assert calls == ["VB1"], "only 1 blocked stub should be refetched at cap=1"


def test_run_refetch_unlimited_without_cap(tmp_path, monkeypatch):
    calls = _blocked_run_setup(tmp_path, monkeypatch, ["VB1", "VB2", "VB3"])
    rc = yc.cmd_run(yc._args(["run", "--refetch-blocked", "--sleep", "0"]))
    assert rc == 0
    assert calls == ["VB1", "VB2", "VB3"], "no cap → all blocked stubs refetched"
