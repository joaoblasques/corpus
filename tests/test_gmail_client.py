import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
import gmail_client as gc  # noqa: E402


def _b64url(text: str) -> str:
    return base64.urlsafe_b64encode(text.encode("utf-8")).decode("ascii")


def test_header_case_insensitive():
    headers = [{"name": "From", "value": "a@b.com"}, {"name": "Subject", "value": "Hi"}]
    assert gc.header(headers, "from") == "a@b.com"
    assert gc.header(headers, "SUBJECT") == "Hi"
    assert gc.header(headers, "missing") == ""


def test_extract_body_prefers_plain():
    payload = {
        "mimeType": "multipart/alternative",
        "parts": [
            {"mimeType": "text/plain", "body": {"data": _b64url("plain wins")}},
            {"mimeType": "text/html", "body": {"data": _b64url("<p>html loses</p>")}},
        ],
    }
    assert gc.extract_body(payload) == "plain wins"


def test_extract_body_falls_back_to_html():
    payload = {
        "mimeType": "text/html",
        "body": {"data": _b64url("<p>Hello</p><p>World</p>")},
    }
    out = gc.extract_body(payload)
    assert "Hello" in out and "World" in out
    assert "<p>" not in out


def test_extract_body_nested_multipart():
    payload = {
        "mimeType": "multipart/mixed",
        "parts": [
            {"mimeType": "multipart/alternative", "parts": [
                {"mimeType": "text/plain", "body": {"data": _b64url("deep body")}},
            ]},
            {"mimeType": "application/pdf", "body": {"attachmentId": "x"}},
        ],
    }
    assert gc.extract_body(payload) == "deep body"


def test_extract_body_empty_when_no_text():
    assert gc.extract_body({"mimeType": "image/png", "body": {}}) == ""


def test_html_to_text_strips_and_unescapes():
    assert gc.html_to_text("<p>Tom &amp; Jerry<br>line2</p>") == "Tom & Jerry\nline2"


def test_message_date_from_header():
    msg = {"payload": {"headers": [{"name": "Date", "value": "Mon, 09 Jun 2026 14:30:00 +0000"}]}}
    assert gc.message_date(msg) == "2026-06-09"


def test_message_date_falls_back_to_internaldate():
    # 2026-06-09T00:00:00Z in ms
    ms = int(1781000000)  # arbitrary epoch seconds
    msg = {"payload": {"headers": []}, "internalDate": str(ms * 1000)}
    assert gc.message_date(msg).count("-") == 2  # well-formed YYYY-MM-DD


def test_parse_message_full():
    msg = {
        "id": "MSG123",
        "internalDate": "1717939800000",
        "payload": {
            "headers": [
                {"name": "From", "value": "Jane <jane@example.com>"},
                {"name": "Subject", "value": "Weekly digest"},
                {"name": "Date", "value": "Mon, 09 Jun 2026 14:30:00 +0000"},
            ],
            "mimeType": "text/plain",
            "body": {"data": _b64url("The newsletter body.")},
        },
    }
    info = gc.parse_message(msg)
    assert info["message_id"] == "MSG123"
    assert info["from"] == "Jane <jane@example.com>"
    assert info["subject"] == "Weekly digest"
    assert info["date_received"] == "2026-06-09"
    assert info["body"] == "The newsletter body."
