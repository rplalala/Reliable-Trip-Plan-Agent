"""Explicit offline V0 association backed by immutable, source-linked model material."""

import hashlib
import json
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from .identity import (
    _evidence_candidates,
    _resolve_identities,
    identity_references,
)
from .identity_assistance import IdentityAssistancePacket
from .intake import _constant, _float, _pairs, _read
from .projection import project
from .records import canonical_digest, freeze, require, text, thaw
from .snapshot import build_identity_plan, identity_evidence, load_snapshot

POLICY_VERSION = "v0_model_assisted_association_1"
MATERIAL_VERSION = "rtpeval_v0_identity_material_1"


def proposal_schema():
    """The saved adapter's strict output schema, before local-reference constraints."""
    properties = {
        "reference_id": {"title": "Reference Id", "type": "string"},
        "decision": {
            "enum": ["match", "unknown", "no_supported_match"],
            "title": "Decision",
            "type": "string",
        },
        "candidate_id": {"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Candidate Id"},
        "rationale": {"title": "Rationale", "type": "string"},
        "evidence_fields": {
            "items": {"type": "string"},
            "title": "Evidence Fields",
            "type": "array",
        },
    }
    return {
        "$defs": {
            "IdentityDecision": {
                "additionalProperties": False,
                "properties": properties,
                "required": list(properties),
                "title": "IdentityDecision",
                "type": "object",
            }
        },
        "additionalProperties": False,
        "properties": {
            "decisions": {
                "items": {"$ref": "#/$defs/IdentityDecision"},
                "title": "Decisions",
                "type": "array",
            }
        },
        "required": ["decisions"],
        "title": "IdentityProposals",
        "type": "object",
    }


def _proposals(raw):
    value = json.loads(raw, object_pairs_hook=_pairs, parse_constant=_constant, parse_float=_float)
    require(
        isinstance(value, dict)
        and set(value) == {"decisions"}
        and isinstance(value["decisions"], list),
        "response",
        "Invalid proposal response",
    )
    fields = set(proposal_schema()["$defs"]["IdentityDecision"]["properties"])
    for row in value["decisions"]:
        require(
            isinstance(row, dict)
            and set(row) == fields
            and text(row["reference_id"])
            and isinstance(row["decision"], str)
            and (row["candidate_id"] is None or text(row["candidate_id"]))
            and text(row["rationale"])
            and isinstance(row["evidence_fields"], list)
            and all(isinstance(field, str) for field in row["evidence_fields"]),
            "response",
            "Invalid proposal response fields",
        )
    return value


@dataclass(frozen=True)
class V0IdentityMaterial:
    intake: object
    evidence: object
    audit_plan: object
    decisions: object
    reference_ids: frozenset
    audit_frozen: bool
    replay: object
    provenance: object


def _value(value):
    return value.to_dict() if hasattr(value, "to_dict") else thaw(value)


def _wire_digest(value):
    """Preserve the saved SDK executor's JSON hash format, distinct from RTPEval digests."""
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def _artifact(root, ref):
    require(isinstance(ref, dict) and text(ref.get("path")), "material", "Artifact required")
    relative = Path(ref["path"])
    path = (root / relative).resolve()
    require(
        not relative.is_absolute() and not relative.drive and path.is_relative_to(root),
        "material",
        "Artifact path escapes root",
    )
    value, digest = _read(path)
    require(digest == ref.get("sha256"), relative.as_posix(), "Frozen artifact hash mismatch")
    return value, path


def _eligible(decision, case):
    if decision["decision"] != "match":
        return decision["decision"]
    candidate = next(c for c in case["candidates"] if c["place_id"] == decision["candidate_id"])
    fields = decision["evidence_fields"]
    if not {"candidate.display_name", "candidate.formatted_address"}.issubset(fields):
        return "independent_support_missing"
    allowed = {
        "claim.place_name",
        "claim.destination",
        "claim.location",
        "candidate.display_name",
        "candidate.formatted_address",
        "candidate.address_components",
    }
    for field in fields:
        if field not in allowed:
            return "unsupported_evidence_field"
        owner, key = field.split(".")
        value = (case["claim"] if owner == "claim" else candidate).get(key)
        if key != "address_components":
            if not text(value):
                return "invalid_cited_field"
        elif (
            not isinstance(value, list)
            or not value
            or any(
                not isinstance(row, dict)
                or not text(row.get("longText"))
                or "types" in row
                and (
                    not isinstance(row["types"], list)
                    or not all(text(kind) for kind in row["types"])
                )
                or "shortText" in row
                and not isinstance(row["shortText"], str)
                for row in value
            )
        ):
            return "invalid_cited_field"
    return "eligible"


def _source(prepared, values, refs):
    group = next(g for g in prepared["inventory"] if g["group_id"] == values["group_id"])
    run = group["runs"].get("v0")
    require(isinstance(run, dict), "source", "Selected V0 run required")
    result, digest, provenance = values["result"], values["result_hash"], values["provenance"]
    context = run["final"]["context"]
    require(
        result.get("system_version") == "v0"
        and context["artifact_sha256"] == digest
        and values["input"] == group["input"]
        and values["input_hash"] == group["input_sha256"]
        and provenance.get("version") == "v0"
        and provenance.get("run_id") == context["run_id"]
        and provenance.get("input_sha256") == group["input_sha256"]
        and provenance.get("result_sha256") == digest
        and (
            run.get("provenance_hash") is None
            or run["provenance_hash"] == values["provenance_hash"]
        ),
        "source",
        "Original V0 source/provenance mismatch",
    )
    require(
        project(result.get("itinerary"), context, version="v0") == run["final"],
        "source",
        "V0 projection does not replay from original source",
    )
    selected = [
        r
        for r in refs
        if r["group_id"] == group["group_id"]
        and (
            r["version"] == "v0"
            and r["projection"] == "final"
            or r["kind"] == "requirement_subject"
        )
    ]
    return selected


def _authorization_precedes_send(value, started, timezone):
    try:
        authorized_date = date.fromisoformat(value)
    except ValueError:
        authorized = datetime.fromisoformat(value)
        return authorized.utcoffset() is not None and authorized <= started
    return authorized_date <= started.astimezone(ZoneInfo(timezone)).date()


def _freeze_verified(values, artifacts, request):
    if values.get("freeze") is None or values.get("authorization") is None:
        return False
    frozen, authorization = values["freeze"], values["authorization"]
    require(
        authorization.get("status") == "user_authorized"
        and authorization.get("manifest_sha256") == artifacts["freeze"]["sha256"],
        "freeze",
        "Audit freeze authorization mismatch",
    )
    # The authorized preflight binds the historical seed/count and request/map before send.
    for role in ("intake", "result", "input", "snapshot", "judge_input", "audit_plan"):
        ref = artifacts[role]
        known = frozen.get("source_hashes", {})
        require(known.get(ref["path"]) == ref["sha256"], "freeze", "Unbound frozen source")
    for role in ("requests", "reference_maps"):
        ref = artifacts[role]
        require(
            frozen.get("file_hashes", {}).get(Path(ref["path"]).name) == ref["sha256"],
            "freeze",
            "Unbound frozen model packet",
        )
    attempts = values["attempts"]
    attempts = attempts["attempts"] if isinstance(attempts, dict) else attempts
    sends = [a for a in attempts if a.get("case") == "v0_identity"]
    require(len(sends) == 1, "freeze", "Unique saved V0 send required")
    send = sends[0]
    started = datetime.fromisoformat(send["started_at"])
    require(
        started.utcoffset() is not None
        and send.get("http_status") == 200
        and send.get("request") == request
        and send.get("request_sha256") == _wire_digest(request)
        and send.get("response_sha256") == artifacts["response"]["sha256"]
        and _authorization_precedes_send(
            authorization["authorized_at"], started, values["authorization_timezone"]
        ),
        "freeze",
        "Frozen request/response chronology mismatch",
    )
    return True


def load_v0_material(intake, bundle_path):
    """Re-read frozen source, snapshot and wire bytes without any network dependency."""
    prepared = _value(intake)
    path = Path(bundle_path).resolve()
    bundle, bundle_hash = _read(path)
    require(bundle.get("schema_version") == MATERIAL_VERSION, "material", "Unsupported material")
    root = (path.parent / bundle["artifact_root"]).resolve()
    artifacts = bundle["artifacts"]
    values = {
        "group_id": bundle["group_id"],
        "authorization_timezone": bundle["authorization_timezone"],
    }
    paths = {}
    for role, ref in artifacts.items():
        if ref is None:
            values[role] = None
            continue
        values[role], paths[role] = _artifact(root, ref)
        values[role + "_hash"] = ref["sha256"]
    if prepared is None:
        prepared = values["intake"]
    require(values["intake"] == prepared, "intake", "Frozen intake mismatch")
    refs = identity_references(prepared)
    selected = _source(prepared, values, refs)
    snapshot = load_snapshot(paths["snapshot"].parent, expected_plan=build_identity_plan(prepared))
    observed = identity_evidence(snapshot)
    observations = {r["reference_id"]: r for r in observed["records"]}
    judge = values["judge_input"]
    require(text(judge.get("instructions")), "judge", "Judging instructions required")
    cases = judge["cases"]
    packet = IdentityAssistancePacket(cases)
    require(
        set(packet.candidates) == {r["reference_id"] for r in selected},
        "judge",
        "Complete V0/subject proposal coverage required",
    )
    by_ref = {r["reference_id"]: r for r in selected}
    for case in cases:
        ref = by_ref[case["reference_id"]]
        detail, candidates = _evidence_candidates(observations.get(ref["reference_id"]))
        require(
            case["claim"]
            == {
                "place_name": ref["name"],
                "destination": ref["destination"],
                "location": ref["location"],
            }
            and {c["place_id"]: c for c in case["candidates"]}
            == {c["place_id"]: c for c in ([detail] if detail else []) + candidates},
            "judge",
            "Candidate packet does not match independent observations/source claims",
        )
    require(
        values["reference_maps"]["v0_identity"] == packet.manifest,
        "map",
        "Short-reference map mismatch",
    )
    request = values["requests"]["v0_identity"]
    require(
        request["instructions"] == judge["instructions"] + "\n" + packet.payload["instructions"]
        and json.loads(request["input"]) == {"cases": packet.payload["cases"]}
        and request.get("tools") == []
        and request["text"]["format"]
        == {
            "type": "json_schema",
            "name": "V0IdentityProposals",
            "strict": True,
            "schema": packet.constrain_schema(proposal_schema()),
        },
        "request",
        "Saved judging request/schema mismatch",
    )
    response = values["response"]
    require(
        response.get("status") == "completed"
        and text(response.get("id"))
        and text(request.get("model"))
        and response.get("model") == request["model"]
        and isinstance(response.get("output"), list)
        and all(
            isinstance(item, dict) and item.get("type") in ("message", "reasoning")
            for item in response["output"]
        ),
        "response",
        "Completed matching-model response required",
    )
    texts = [
        c["text"]
        for message in response["output"]
        if message.get("type") == "message" and message.get("role") == "assistant"
        for c in message["content"]
        if c.get("type") == "output_text"
    ]
    require(len(texts) == 1, "response", "One bounded model output required")
    wire = _proposals(texts[0])
    canonical = packet.resolve(wire)
    cases_by_id = {c["reference_id"]: c for c in cases}
    decisions = {
        d["reference_id"]: {**d, "eligibility": _eligible(d, cases_by_id[d["reference_id"]])}
        for d in canonical["decisions"]
    }
    frozen = _freeze_verified(values, artifacts, request)
    return V0IdentityMaterial(
        freeze(prepared),
        freeze(observed),
        freeze(values["audit_plan"]),
        freeze(decisions),
        frozenset(decisions),
        frozen,
        freeze({"path": str(path), "sha256": bundle_hash}),
        freeze(
            {
                "artifacts": artifacts,
                "reference_map_sha256": packet.mapping_sha256,
                "judging_request_sha256": _wire_digest(request),
                "restored_proposals_sha256": canonical_digest(canonical),
                "model": response["model"],
                "response_id": response.get("id"),
                "response_created_at": response.get("created_at"),
                "audit_freeze_basis": "authorized_manifest_and_saved_send_binding",
                "audit_freeze_verified": frozen,
            }
        ),
    )


def resolve_v0_identities(intake, bundle_path, reviews=None):
    """Explicit opt-in; native resolution remains independently callable and unchanged."""
    material = load_v0_material(intake, bundle_path)
    return _resolve_identities(
        thaw(material.intake), thaw(material.evidence), reviews, thaw(material.audit_plan), material
    )


def verify_v0_report(intake, report):
    """Accept this policy only after exact replay of its source-linked local material."""
    try:
        replay = report["model_assistance_replay"]
        _, digest = _read(Path(replay["bundle"]["path"]))
        if digest != replay["bundle"]["sha256"]:
            return False
        expected = resolve_v0_identities(intake, replay["bundle"]["path"], replay["reviews"])
        return expected.to_dict() == report
    except (ValueError, TypeError, KeyError, OSError, StopIteration):
        return False


def needs_v0_replay(report):
    """Structured assistance markers must not be accepted under a substituted native stamp."""
    if not isinstance(report, dict):
        return False
    records = report.get("records")
    records = records if isinstance(records, list) else []
    return (
        report.get("association_policy_version") == POLICY_VERSION
        or "model_assistance_replay" in report
        or "model_assistance_provenance" in report
        or any(
            isinstance(r, dict)
            and (r.get("decision_route") == "model_assisted" or "model_proposal" in r)
            for r in records
        )
    )


def adoption_summary(prepared, records, material):
    """Expose adoption and directed endpoint eligibility without claiming route feasibility."""
    by_id = {r["reference_id"]: r for r in records}
    selected = [by_id[rid] for rid in material.reference_ids]
    pending = {"high_impact_review", "audit_pending", "audit_freeze_unverified"}
    counts = {
        "adopted": sum(r["resolution"] == "resolved" for r in selected),
        "review_pending": sum(
            r["resolution"] == "unresolved" and r["reason"] in pending for r in selected
        ),
        "unknown": sum(
            r["resolution"] == "unresolved" and r["reason"] not in pending for r in selected
        ),
    }
    legs = []
    for group in prepared["inventory"]:
        for version, run in group["runs"].items():
            if version != "v0":
                continue
            for leg in run["final"]["legs"]:
                ends = [leg[key]["record_id"] for key in ("from_source", "to_source")]
                if not set(ends).issubset(material.reference_ids):
                    continue
                blocked = [
                    {"reference_id": rid, "reason": by_id[rid]["reason"]}
                    for rid in ends
                    if by_id[rid]["resolution"] != "resolved"
                ]
                legs.append(
                    {
                        "group_id": group["group_id"],
                        "origin_reference": ends[0],
                        "destination_reference": ends[1],
                        "identity_eligible": not blocked,
                        "blockers": blocked,
                    }
                )
    return {"adoption_counts": counts, "leg_identity_eligibility": legs}
