"""Shared artifact identity and pure JSON reading helpers."""


import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_json_bytes(payload: object) -> bytes:
    return (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def payload_fingerprint(payload: object) -> str:
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def load_json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value
