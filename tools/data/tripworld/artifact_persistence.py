"""Offline artifact persistence and build-result reuse checks."""

import json
import os
from pathlib import Path

from backend.app.tripworld.artifacts import canonical_json_bytes, load_json_object
from backend.app.tripworld.hashing import sha256_file


def write_json_if_changed(path: Path, payload: object) -> bool:
    """Atomically write canonical JSON and return whether the file changed."""

    content = canonical_json_bytes(payload)
    if path.is_file() and path.read_bytes() == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".part")
    temporary.write_bytes(content)
    os.replace(temporary, path)
    return True


def write_text_if_changed(path: Path, content: str) -> bool:
    encoded = content.encode("utf-8")
    if path.is_file() and path.read_bytes() == encoded:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".part")
    temporary.write_bytes(encoded)
    os.replace(temporary, path)
    return True


def artifact_is_current(
    output_path: Path,
    metadata_path: Path,
    *,
    input_fingerprint: str,
) -> bool:
    if not output_path.is_file() or not metadata_path.is_file():
        return False
    try:
        metadata = load_json_object(metadata_path)
        return (
            metadata.get("input_fingerprint") == input_fingerprint
            and metadata.get("output_size_bytes") == output_path.stat().st_size
            and metadata.get("output_sha256") == sha256_file(output_path)
        )
    except (OSError, ValueError, json.JSONDecodeError):
        return False
