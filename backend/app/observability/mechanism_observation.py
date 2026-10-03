"""Opt-in normalized observations at existing application submission/selection seams."""

import asyncio
import hashlib
import json
from contextlib import contextmanager
from contextvars import ContextVar

from pydantic_core import to_jsonable_python

from .run_trace import redact_secrets

current_mechanism = ContextVar("current_mechanism", default=None)
_current_projection = ContextVar("mechanism_model_projection", default=None)


def digest(value):
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False
        ).encode("utf-8")
    ).hexdigest()


def source_refs(value):
    """Read explicit structured references; do not infer facts from prose."""
    refs = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key in ("source_refs", "evidence_refs", "unresolved_conflict_source_refs"):
                refs.update(r for r in item if isinstance(r, str) and r.startswith("official_web:"))
            else:
                refs.update(source_refs(item))
    elif isinstance(value, (list, tuple)):
        for item in value:
            refs.update(source_refs(item))
    return sorted(refs)


class MechanismRecorder:
    def __init__(self, max_bytes):
        self.max_bytes = max_bytes
        self.bytes = 0
        self.catalog = []
        self.active_claims = {}
        self.prepared_calls = []
        self.occurrences = []
        self.diagnostics = []
        self.catalog_observed = False
        self.rules_observed = False
        self.call_index = 0
        self.rule_index = 0

    def append(self, target, value):
        # A detached JSON copy prevents later mutations of planner objects.
        normalized = to_jsonable_python(value)
        if redact_secrets(normalized) != normalized:
            self.issue("redacted_observation_unavailable")
            return False
        raw = json.dumps(normalized, ensure_ascii=False, allow_nan=False)
        size = len(raw.encode("utf-8"))
        if self.bytes + size > self.max_bytes:
            self.issue("capacity_truncated")
            return False
        target.append(json.loads(raw))
        self.bytes += size
        return True

    def issue(self, reason, **detail):
        row = {"reason": reason, **detail}
        if row not in self.diagnostics and len(self.diagnostics) < 32:
            self.diagnostics.append(row)


def _observe(action):
    recorder = current_mechanism.get()
    if recorder is None:
        return None
    try:
        return action(recorder)
    except Exception as exc:
        recorder.issue("observation_failed", error_type=type(exc).__name__)
        return None


def accepted_catalog(claims):
    def record(recorder):
        recorder.catalog_observed = True
        for claim in claims:
            value = claim.model_dump(mode="json")
            sha = digest(value)
            if recorder.append(recorder.catalog, {"claim": value, "claim_sha256": sha}):
                recorder.active_claims[value["source_ref"]] = sha

    _observe(record)


@contextmanager
def model_projection(stage, representation, *, round_index=None):
    """Stage exact structured input; only the adapter can establish submission."""

    def prepare(recorder):
        recorder.call_index += 1
        value = representation() if callable(representation) else representation
        row = {
            "call_id": f"call:{recorder.call_index}",
            "stage": stage,
            "round_index": round_index,
            "representation": value,
            "submitted": False,
        }
        if recorder.append(recorder.prepared_calls, row):
            return recorder.prepared_calls[-1]
        return None

    row = _observe(prepare)
    token = _current_projection.set(row)
    try:
        yield
    except BaseException as exc:
        if row is not None:
            row["outcome"] = "cancelled" if isinstance(exc, asyncio.CancelledError) else "failed"
            row["error_type"] = type(exc).__name__
        raise
    else:
        if row is not None:
            row["outcome"] = "returned"
    finally:
        _current_projection.reset(token)


def repair_representation(user):
    """The existing Repair serializer emits JSON; retain only its official fact sections."""
    value = json.loads(user)
    return {
        key: value[key] for key in ("effective_evidence", "selected_opening_evidence", "findings")
    }


def model_submitted():
    def record(recorder):
        row = _current_projection.get()
        if row is None or row["submitted"]:
            return
        row["submitted"] = True
        refs = source_refs(row["representation"])
        if any(ref not in recorder.active_claims for ref in refs):
            recorder.issue("unlinked_official_refs")
        recorder.append(
            recorder.occurrences,
            {
                "occurrence_id": row["call_id"],
                "reason": "model_input_submission",
                "stage": row["stage"],
                "round_index": row["round_index"],
                "source_refs": refs,
                "claim_links": [
                    {"source_ref": ref, "claim_sha256": recorder.active_claims[ref]}
                    for ref in refs
                    if ref in recorder.active_claims
                ],
                "representation": row["representation"],
            },
        )

    _observe(record)


def rule_selections(report):
    def record(recorder):
        recorder.rules_observed = True
        for finding in report.findings:
            if finding.check != "opening":
                continue
            for selected in finding.adopted_evidence.get("selected_hours", []):
                refs = source_refs(selected)
                if not refs:
                    continue
                if any(ref not in recorder.active_claims for ref in refs):
                    recorder.issue("unlinked_official_refs")
                recorder.rule_index += 1
                recorder.append(
                    recorder.occurrences,
                    {
                        "occurrence_id": f"rule:{recorder.rule_index}",
                        "reason": "rule_selection",
                        "rule": "opening",
                        "finding_id": finding.finding_id,
                        "activity_ids": list(finding.activity_ids),
                        "dates": [str(d) for d in finding.dates],
                        "place_ids": list(finding.place_ids),
                        "source_refs": refs,
                        "claim_links": [
                            {"source_ref": ref, "claim_sha256": recorder.active_claims[ref]}
                            for ref in refs
                            if ref in recorder.active_claims
                        ],
                        "representation": selected,
                    },
                )

    _observe(record)
