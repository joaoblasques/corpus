"""Resolve a JSON secret to a filesystem path.

In the cloud/CI, secrets arrive as environment variables holding the JSON
content; locally they live in on-disk token files. `materialize_secret` bridges
the two so collector code can stay file-based: env var wins (written to a 0600
temp file), else the on-disk fallback, else an error.
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path


def materialize_secret(env_var: str, fallback_path: Path) -> Path:
    value = os.environ.get(env_var)
    if value:
        fd, name = tempfile.mkstemp(prefix="corpus_secret_", suffix=".json")
        try:
            os.fchmod(fd, 0o600)
            os.write(fd, value.encode("utf-8"))
        finally:
            os.close(fd)
        return Path(name)
    if fallback_path.exists():
        return fallback_path
    raise FileNotFoundError(
        f"secret unavailable: env {env_var!r} unset and {fallback_path} missing"
    )
