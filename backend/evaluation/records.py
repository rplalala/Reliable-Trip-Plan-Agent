"""Immutable preparation results and stable, source-derived identifiers."""

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

PROJECTION_VERSION = "rtpeval_projection_1"


def canonical_digest(value):
    """Shared compact JSON digest for independent preparation/replay policy records."""
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def freeze(value):
    if isinstance(value, dict):
        return MappingProxyType({key: freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(freeze(item) for item in value)
    return value


def thaw(value):
    if isinstance(value, Mapping):
        return {key: thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [thaw(item) for item in value]
    return value


@dataclass(frozen=True)
class IntakeResult:
    """Immutable snapshot; callers can serialize an independent mutable copy."""

    status: str
    data: Mapping

    def to_dict(self):
        return {"status": self.status, **thaw(self.data)}


def source(context, pointer):
    record = {**context, "pointer": pointer, "projection_version": PROJECTION_VERSION}
    record["record_id"] = hashlib.sha256(
        json.dumps(record, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    return record


class MaterialError(ValueError):
    """Invalid delivery material, distinct from itinerary quality."""

    def __init__(self, reason, pointer, explanation):
        super().__init__(explanation)
        self.diagnostic = {"reason": reason, "pointer": pointer, "explanation": explanation}


def require(condition, pointer, explanation, reason="artifact_integrity_error"):
    if not condition:
        raise MaterialError(reason, pointer, explanation)


def text(value):
    return isinstance(value, str) and bool(value.strip())
