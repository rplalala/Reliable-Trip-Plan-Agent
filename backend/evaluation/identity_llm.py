"""Uniform offline LLM identity judgments over independent, source-bound facts."""

import json
from dataclasses import dataclass
from datetime import datetime

from .identity import (
    IDENTITY_VERSION,
    SUBJECT_SCOPE_VERSION,
    IdentityResult,
    _claimed_id_status,
    _evidence_candidates,
    _high_impact,
    _intake_dict,
    _observation_index,
    _summaries,
    identity_references,
)
from .identity_assistance import IdentityAssistancePacket
from .intake import _constant, _float, _pairs
from .records import canonical_digest as digest
from .records import freeze, text, thaw

POLICY_VERSION = "llm_identity_judgment_1"
PACKET_VERSION = "rtpeval_identity_judgment_packet_1"
RESULT_VERSION = "rtpeval_identity_model_result_1"
ADDRESS_STATES = (
    "equivalent",
    "different_precision",
    "incorrect_claim",
    "different_place",
    "unknown",
    "not_supplied",
)
DESTINATION_STATES = ("consistent", "contradictory", "unknown")
INSTRUCTIONS = """Judge every supplied identity reference using only independent candidate facts.
Original planner claims are comparison inputs, not evidence. Provider rank is not confidence.
Select a supplied candidate only when it represents the intended venue; otherwise return
unknown or no_supported_match with candidate_id null. Do not invent candidates or facts.
Compare name, destination, location, supplied ID, and all conflicting provider observations.
High-impact subjects and visits need the same judgment as ordinary visits, without humans.
For address_assessment distinguish equivalent wording, different_precision, incorrect_claim
(the intended venue is identifiable but the original address is wrong), different_place,
unknown, and not_supplied. A match must not have different_place or unknown address assessment.
Different branches/cities are different_place, not harmless spelling differences. Insufficient
facts mean unknown. An incorrect original address may coexist with an identified venue;
preserve the original claim. Destination must be consistent for a match. Cite the original
claim fields and independent candidate name/address supporting each match. Explain all
judgments; do not certify opening hours, routes, or factual accuracy of model judgments."""


@dataclass(frozen=True)
class IdentityJudgmentPacket:
    data: object

    def to_dict(self):
        return thaw(self.data)


def _packet(cases):
    return IdentityAssistancePacket(
        cases,
        additional_fields={
            "claimed_place_id": "p",
            "requested_place_id": "p",
        },
    )


def judgment_schema():
    """Strict portable model output schema; no provider-specific runtime dependency."""
    properties = {
        "reference_id": {"type": "string"},
        "decision": {"type": "string", "enum": ["match", "unknown", "no_supported_match"]},
        "candidate_id": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        "rationale": {"type": "string"},
        "evidence_fields": {"type": "array", "items": {"type": "string"}},
        "address_assessment": {"type": "string", "enum": list(ADDRESS_STATES)},
        "destination_assessment": {"type": "string", "enum": list(DESTINATION_STATES)},
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["decisions"],
        "properties": {
            "decisions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": properties,
                    "required": list(properties),
                },
            }
        },
    }


def _cases(prepared, evidence):
    refs = identity_references(prepared)
    observed = _observation_index(evidence, refs, prepared)
    cases = []
    for ref in refs:
        detail, search = _evidence_candidates(observed.get(ref["reference_id"]))
        candidates = {}
        for candidate in ([detail] if detail else []) + search:
            pid = candidate["place_id"]
            if pid not in candidates:
                candidates[pid] = {**candidate, "observations": []}
            candidates[pid]["observations"].append(candidate)
        cases.append(
            {
                "reference_id": ref["reference_id"],
                "kind": ref["kind"],
                "version": ref["version"],
                "projection": ref["projection"],
                "source": ref["source"],
                "claim": {
                    "place_name": ref["name"],
                    "original_title": ref["original_title"],
                    "destination": ref["destination"],
                    "location": ref["location"],
                    "claimed_place_id": ref["claimed_place_id"],
                },
                "observation": observed.get(ref["reference_id"]),
                "candidates": list(candidates.values()),
            }
        )
    return refs, observed, cases


def prepare_identity_judgment(intake, evidence, *, model):
    """Freeze a complete model request without executing a model or provider."""
    if not text(model):
        raise ValueError("An explicit judgment model is required")
    prepared = _intake_dict(intake)
    refs, _, cases = _cases(prepared, evidence)
    if not refs:
        raise ValueError("No applicable identity references")
    packet = _packet(cases)
    request = {
        "model": model,
        "instructions": INSTRUCTIONS + "\n" + packet.payload["instructions"],
        "input": json.dumps(
            {"cases": packet.payload["cases"]},
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ),
        "tools": [],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "IdentityJudgments",
                "strict": True,
                "schema": packet.constrain_schema(judgment_schema()),
            }
        },
    }
    return IdentityJudgmentPacket(
        freeze(
            {
                "schema_version": PACKET_VERSION,
                "batch_id": prepared["batch_id"],
                "batch_revision": prepared["revision"],
                "intake_sha256": digest(prepared),
                "evidence_sha256": digest(evidence),
                "reference_set_digest": digest(refs),
                "reference_maps": packet.manifest,
                "request": request,
                "request_sha256": digest(request),
            }
        )
    )


def _decisions(intake, evidence, cases, material):
    if material is None:
        return {}, None
    if not isinstance(material, dict) or material.get("schema_version") != RESULT_VERSION:
        raise ValueError("Invalid identity model result envelope")
    saved = material["packet"]
    model = saved["request"]["model"]
    expected = prepare_identity_judgment(intake, evidence, model=model).to_dict()
    if saved != expected:
        raise ValueError("Identity model packet/source mismatch")
    start = datetime.fromisoformat(material["requested_at"])
    end = datetime.fromisoformat(material["retrieved_at"])
    if start.utcoffset() is None or end.utcoffset() is None or end < start:
        raise ValueError("Invalid identity model response chronology")
    response = material["response"]
    if (
        not isinstance(response, dict)
        or response.get("status") != "completed"
        or not text(response.get("id"))
        or response.get("model") != model
        or digest(response) != material.get("response_sha256")
        or not isinstance(response.get("output"), list)
        or any(
            not isinstance(m, dict) or m.get("type") not in ("message", "reasoning")
            for m in response["output"]
        )
    ):
        raise ValueError("Invalid identity model response/provenance")
    messages = [m for m in response["output"] if m["type"] == "message"]
    if any(
        m.get("role") != "assistant"
        or not isinstance(m.get("content"), list)
        or any(
            not isinstance(c, dict) or c.get("type") != "output_text" or not text(c.get("text"))
            for c in m["content"]
        )
        for m in messages
    ):
        raise ValueError("Malformed identity model message content")
    texts = [
        c["text"]
        for m in messages
        if m.get("type") == "message" and m.get("role") == "assistant"
        for c in m["content"]
        if c.get("type") == "output_text"
    ]
    if len(texts) != 1 or not text(texts[0]):
        raise ValueError("One bounded identity model output required")
    wire = json.loads(
        texts[0], object_pairs_hook=_pairs, parse_constant=_constant, parse_float=_float
    )
    if (
        not isinstance(wire, dict)
        or set(wire) != {"decisions"}
        or not isinstance(wire["decisions"], list)
    ):
        raise ValueError("Invalid identity judgment response schema")
    fields = set(judgment_schema()["properties"]["decisions"]["items"]["properties"])
    for row in wire["decisions"]:
        if (
            not isinstance(row, dict)
            or set(row) != fields
            or not text(row["reference_id"])
            or not isinstance(row["decision"], str)
            or row["candidate_id"] is not None
            and not text(row["candidate_id"])
            or row["address_assessment"] not in ADDRESS_STATES
            or row["destination_assessment"] not in DESTINATION_STATES
        ):
            raise ValueError("Invalid identity judgment fields")
    canonical = _packet(cases).resolve(wire)
    by_ref = {c["reference_id"]: c for c in cases}
    decisions = {}
    for row in canonical["decisions"]:
        case = by_ref[row["reference_id"]]
        candidate = next(
            (c for c in case["candidates"] if c["place_id"] == row["candidate_id"]), None
        )
        cited = set(row["evidence_fields"])
        allowed = {
            "claim.place_name",
            "claim.destination",
            "claim.location",
            "claim.claimed_place_id",
            "claim.original_title",
            "candidate.display_name",
            "candidate.formatted_address",
            "candidate.address_components",
            "candidate.observations",
        }
        for field in cited:
            if field not in allowed:
                raise ValueError("Unsupported identity judgment citation")
            owner, key = field.split(".")
            value = (case["claim"] if owner == "claim" else candidate or {}).get(key)
            if not value or isinstance(value, str) and not text(value):
                raise ValueError("Empty identity judgment citation")
            if key == "address_components" and (
                not isinstance(value, list)
                or any(
                    not isinstance(c, dict)
                    or not text(c.get("longText"))
                    or "shortText" in c
                    and not isinstance(c["shortText"], str)
                    or "types" in c
                    and (not isinstance(c["types"], list) or not all(text(t) for t in c["types"]))
                    for c in value
                )
            ):
                raise ValueError("Malformed cited address components")
        if row["decision"] == "match":
            required = {
                "claim.place_name",
                "claim.destination",
                "candidate.display_name",
                "candidate.formatted_address",
            }
            has_location = text(case["claim"]["location"])
            if has_location:
                required.add("claim.location")
            if text(case["claim"]["claimed_place_id"]):
                required.add("claim.claimed_place_id")
            if not required <= cited:
                raise ValueError("Independent and original identity support citations required")
            if (row["address_assessment"] == "not_supplied") == has_location:
                raise ValueError("Address assessment contradicts original location presence")
        decisions[row["reference_id"]] = row
    return decisions, {
        "model": model,
        "response_id": response["id"],
        "request_sha256": expected["request_sha256"],
        "response_sha256": material["response_sha256"],
        "material_sha256": digest(material),
        "requested_at": material["requested_at"],
        "retrieved_at": material["retrieved_at"],
        "origin": "llm",
    }


def resolve_llm_identities(intake, evidence, *, model_result=None):
    """Keep missing judgments unresolved; no human or automatic-name fallback."""
    prepared = _intake_dict(intake)
    refs, observed, cases = _cases(prepared, evidence)
    decisions, provenance = _decisions(prepared, evidence, cases, model_result)
    subjects = [r for r in refs if r["kind"] == "requirement_subject"]
    records = []
    for ref in refs:
        observation = observed.get(ref["reference_id"])
        detail, search = _evidence_candidates(observation)
        judgment = decisions.get(ref["reference_id"])
        canonical = None
        reason = "model_judgment_missing"
        if judgment:
            reason = "model_" + judgment["decision"]
            if judgment["decision"] == "match":
                if judgment["destination_assessment"] != "consistent" or judgment[
                    "address_assessment"
                ] in ("different_place", "unknown"):
                    reason = "model_conflicting_assessment"
                else:
                    canonical = judgment["candidate_id"]
        records.append(
            {
                **{
                    k: ref[k]
                    for k in (
                        "reference_id",
                        "kind",
                        "source",
                        "group_id",
                        "version",
                        "projection",
                        "audit_key",
                    )
                },
                "resolution": "resolved" if canonical else "unresolved",
                "reason": reason,
                "canonical_place_id": canonical,
                "decision_route": "llm_judgment" if canonical else None,
                "claimed_id_association": _claimed_id_status(ref, observation, canonical),
                "high_impact": _high_impact(ref, subjects, observed),
                "audit_selected": False,
                "evidence_hash": digest(observation),
                "observation_id": observation.get("observation_id") if observation else None,
                "review_history": [],
                "candidate_ids": sorted(
                    {c["place_id"] for c in ([detail] if detail else []) + search}
                ),
                "original_claim": {
                    "place_name": ref["name"],
                    "destination": ref["destination"],
                    "location": ref["location"],
                },
                "model_judgment": judgment,
            }
        )
    queue = [
        {"reference_id": r["reference_id"], "reason": r["reason"]}
        for r in records
        if r["resolution"] == "unresolved"
    ]
    return IdentityResult(
        "needs_model_judgment" if queue else "complete",
        freeze(
            {
                "schema_version": IDENTITY_VERSION,
                "subject_scope_version": SUBJECT_SCOPE_VERSION,
                "association_policy_version": POLICY_VERSION,
                "reference_set_digest": digest(refs),
                "batch_id": prepared["batch_id"],
                "batch_revision": prepared["revision"],
                "source_hashes": prepared["source_hashes"],
                "evidence_hash": digest(evidence),
                "review_hash": None,
                "audit_plan_hash": None,
                "audit_selected_reference_ids": [],
                "records": records,
                "review_queue": [],
                "judgment_queue": queue,
                "model_judgment_provenance": provenance,
                "groups": _summaries(refs, records, prepared),
                "identity_llm_replay": {"evidence": evidence, "model_result": model_result},
            }
        ),
    )


def needs_llm_replay(report):
    """Identify structured model markers even if a policy stamp was substituted."""
    if not isinstance(report, dict):
        return False
    records = report.get("records")
    records = records if isinstance(records, list) else []
    return (
        report.get("association_policy_version") == POLICY_VERSION
        or "identity_llm_replay" in report
        or "model_judgment_provenance" in report
        or any(
            isinstance(r, dict)
            and ("model_judgment" in r or r.get("decision_route") == "llm_judgment")
            for r in records
        )
    )


def verify_llm_report(intake, report):
    """Recompute every field from the original intake, evidence and saved model result."""
    try:
        replay = report["identity_llm_replay"]
        return (
            report.get("association_policy_version") == POLICY_VERSION
            and resolve_llm_identities(
                intake, replay["evidence"], model_result=replay["model_result"]
            ).to_dict()
            == report
        )
    except (ValueError, KeyError, TypeError, AttributeError):
        return False
