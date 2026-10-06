"""Neutral source/policy and reviewed timezone validation shared by offline scorers."""

import re
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .identity import ASSOCIATION_POLICY_VERSION, SUBJECT_SCOPE_VERSION, identity_references
from .records import canonical_digest as stable_id
from .records import require, text


def identity_ready(intake, identity):
    from .identity_adoption import POLICY_VERSION, needs_v0_replay, verify_v0_report
    from .identity_llm import needs_llm_replay, verify_llm_report
    from .identity_program import needs_versioned_replay, verify_versioned_report

    if needs_versioned_replay(identity):
        return verify_versioned_report(intake, identity)
    if needs_llm_replay(identity):
        return verify_llm_report(intake, identity)
    if needs_v0_replay(identity):
        return identity.get("association_policy_version") == POLICY_VERSION and verify_v0_report(
            intake, identity
        )
    refs = identity_references(intake)
    if not isinstance(identity, dict) or (
        identity.get("status") not in ("complete", "needs_adjudication")
        or identity.get("schema_version") != "rtpeval_identity_1"
        or identity.get("subject_scope_version") != SUBJECT_SCOPE_VERSION
        or identity.get("association_policy_version") != ASSOCIATION_POLICY_VERSION
        or identity.get("reference_set_digest") != stable_id(refs)
        or identity.get("source_hashes") != intake["source_hashes"]
        or (identity.get("batch_id"), identity.get("batch_revision"))
        != (intake["batch_id"], intake["revision"])
    ):
        return False
    records = identity.get("records")
    if not isinstance(records, list) or len(records) != len(refs):
        return False
    for key in ("evidence_hash", "audit_plan_hash"):
        if not text(identity.get(key)) or not re.fullmatch(r"[0-9a-f]{64}", identity[key]):
            return False
    if (
        "review_hash" not in identity
        or identity["review_hash"] is not None
        and (
            not text(identity["review_hash"])
            or not re.fullmatch(r"[0-9a-f]{64}", identity["review_hash"])
        )
    ):
        return False
    for item in records:
        if not isinstance(item, dict) or not text(item.get("reference_id")):
            return False
        if item.get("resolution") not in ("resolved", "unresolved"):
            return False
        if item["resolution"] == "resolved" and not text(item.get("canonical_place_id")):
            return False
        if item["resolution"] == "unresolved" and item.get("canonical_place_id") is not None:
            return False
        if (
            type(item.get("high_impact")) is not bool
            or type(item.get("audit_selected")) is not bool
        ):
            return False
        if item["resolution"] == "resolved" and (item["high_impact"] or item["audit_selected"]):
            if item.get("decision_route") != "human_adjudication" or not item.get("review_history"):
                return False
    indexed = {item["reference_id"]: item for item in records}
    if len(indexed) != len(refs):
        return False
    return all(
        ref["reference_id"] in indexed
        and all(
            indexed[ref["reference_id"]].get(key) == ref[key]
            for key in ("source", "kind", "group_id", "version", "projection", "audit_key")
        )
        for ref in refs
    )


def _review_provenance(record, pointer):
    require(
        text(record.get("reviewer_ref")) and text(record.get("reviewed_at")),
        pointer,
        "Review provenance is required",
    )
    try:
        parsed = datetime.fromisoformat(record["reviewed_at"])
    except ValueError:
        parsed = None
    require(
        parsed is not None and parsed.utcoffset() is not None,
        pointer,
        "Review timestamp requires an offset",
    )


def schedule_timezones(intake, envelope):
    if envelope is None:
        return {}
    require(
        isinstance(envelope, dict)
        and envelope.get("schema_version") == "rtpeval_schedule_context_1"
        and envelope.get("batch_id") == intake["batch_id"]
        and text(envelope.get("revision"))
        and isinstance(envelope.get("groups"), list),
        "context",
        "Invalid time context envelope",
    )
    groups = {group["group_id"]: group for group in intake["inventory"]}
    zones = {}
    for record in envelope["groups"]:
        require(
            isinstance(record, dict) and text(record.get("group_id")), "context", "Invalid group"
        )
        gid = record["group_id"]
        require(
            gid in groups
            and gid not in zones
            and record.get("input_sha256") == groups[gid]["input_sha256"],
            "context",
            "Stale/duplicate context group",
        )
        require(
            text(record.get("source_ref")) and text(record.get("timezone")),
            gid,
            "Independent zone evidence reference required",
        )
        _review_provenance(record, gid)
        try:
            ZoneInfo(record["timezone"])
        except (ZoneInfoNotFoundError, ValueError):
            require(False, gid, "Unknown IANA timezone")
        zones[gid] = record["timezone"]
    return zones
