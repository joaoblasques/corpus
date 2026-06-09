#!/usr/bin/env python3
"""collect_email.py — deterministic core for the collect-email skill.

The skill fetches starred Gmail messages via MCP and, for each one, invokes
this script to idempotently write a normalized markdown file into raw/_inbox/.
Gmail mutation (de-star/archive) is performed by the skill only after this
script reports a successful write.
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "raw" / "_inbox"
DEDUP_DIRS = [ROOT / "raw" / "_inbox", ROOT / "raw" / "email"]

URL_RE = re.compile(r"https?://[^\s)>\]]+")
POINTER_MAX_PROSE = 200  # non-URL chars below which a body is "just a link"


def slugify(text: str, max_len: int = 60) -> str:
    text = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if len(text) > max_len:
        text = text[:max_len].rstrip("-")
    return text or "untitled"
