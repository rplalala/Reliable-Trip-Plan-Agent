"""Version-scoped evaluation from original claims and independent API observations."""

from ._addresses import destination_matches
from .identity import (
    IDENTITY_VERSION,
    SUBJECT_SCOPE_VERSION,
    IdentityResult,
    _candidate,
    _claimed_id_status,
    _evidence_candidates,
    _intake_dict,
    _observation_index,
    _summaries,
    identity_references,
)
from .records import canonical_digest as digest
from .records import freeze, text

POLICY_VERSION = "versioned_api_identity_1"


def subject_bindings(intake):
    """Retained requirement IDs are claims; independent Details must verify them."""
    return {
        (g["group_id"], s["subject_id"]): s.get("source_place_id")
        for g in _intake_dict(intake)["inventory"]
        for s in g["requirement_spec"]["subjects"]
    }


def _check(ref, observation, binding=None):
    claimed = ref["claimed_place_id"] if ref["kind"] == "primary_visit" else binding
    candidate = None
    if ref["kind"] == "primary_visit" and not text(claimed):
        return "FAIL", "missing_claimed_place_id", None
    if ref["kind"] == "primary_visit" and ref["name_source"] != "place_name":
        return "FAIL", "missing_claimed_place_name", None
    if ref["kind"] == "primary_visit" and not text(ref["location"]):
        return "FAIL", "missing_claimed_address", None
    if binding is not None and not text(binding):
        return "UNKNOWN", "subject_binding_invalid", None
    if text(claimed):
        details = observation.get("details") if observation else None
        if not details or details["status"] != "available":
            return "UNKNOWN", "id_details_unavailable", None
        if details.get("requested_place_id") != claimed:
            return "UNKNOWN", "id_request_mismatch", None
        candidate = _candidate(details.get("place"))
        if candidate is None:
            return "UNKNOWN", "malformed_details", None
        if candidate["place_id"] != claimed:
            return "UNKNOWN", "id_response_mismatch", None
    else:
        search = observation.get("search") if observation else None
        if not search or search["status"] != "available":
            return "UNKNOWN", "subject_search_unavailable", None
        if search.get("query") != ref["name"] or search.get("requested_page_size") != 20:
            return "UNKNOWN", "subject_search_scope_unverified", None
        if search["actual_result_count"] != 1 or len(search["candidates"]) != 1:
            return "UNKNOWN", "subject_search_ambiguous", None
        candidate = _candidate(search["candidates"][0])
        if candidate is None:
            return "UNKNOWN", "malformed_subject_candidate", None
        if not destination_matches(ref["destination"], candidate):
            return "UNKNOWN", "subject_destination_unverified", None
    if ref["name"] != candidate["display_name"]:
        return "FAIL", "api_name_mismatch", None
    if text(ref["location"]) and ref["location"] != candidate["formatted_address"]:
        return "FAIL", "api_address_mismatch", None
    return "PASS", "independent_api_exact_match", candidate["place_id"]


def resolve_versioned_identities(intake, evidence, *, model_result=None):
    """V0 model results never decide other versions or shared requirement subjects."""
    prepared = _intake_dict(intake)
    refs = identity_references(prepared)
    observed = _observation_index(evidence, refs, prepared)
    bindings = subject_bindings(prepared)
    v0_refs = [r for r in refs if r["version"] == "v0"]
    model_records, provenance = {}, None
    if v0_refs:
        from .identity_llm import resolve_llm_identities

        model = resolve_llm_identities(
            prepared, evidence, model_result=model_result, v0_only=True
        ).to_dict()
        model_records = {r["reference_id"]: r for r in model["records"]}
        provenance = model["model_judgment_provenance"]
    elif model_result is not None:
        raise ValueError("Model results require eligible V0 references")
    records = []
    for ref in refs:
        rid = ref["reference_id"]
        if rid in model_records:
            records.append(model_records[rid])
            continue
        observation = observed.get(rid)
        binding = bindings.get((ref["group_id"], ref["source"].get("subject_id")))
        verdict, reason, canonical = _check(ref, observation, binding)
        detail, search = _evidence_candidates(observation)
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
                "grounding_verdict": verdict,
                "decision_route": "independent_api_exact" if canonical else None,
                "claimed_id_association": _claimed_id_status(ref, observation, canonical),
                "high_impact": ref["high_impact"],
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
                "programmatic_judgment": {"verdict": verdict, "reason": reason},
            }
        )
    queue = [
        {"reference_id": r["reference_id"], "reason": r["reason"]}
        for r in records
        if r["grounding_verdict"] == "UNKNOWN"
    ]
    return IdentityResult(
        "needs_evidence" if queue else "complete",
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
                "identity_versioned_replay": {"evidence": evidence, "model_result": model_result},
            }
        ),
    )


def needs_versioned_replay(report):
    if not isinstance(report, dict):
        return False
    records = report.get("records")
    records = records if isinstance(records, list) else []
    return (
        report.get("association_policy_version") == POLICY_VERSION
        or "identity_versioned_replay" in report
        or any(isinstance(r, dict) and "programmatic_judgment" in r for r in records)
    )


def verify_versioned_report(intake, report):
    """Recompute the complete report; stamps alone never certify programmatic verdicts."""
    try:
        replay = report["identity_versioned_replay"]
        return report.get("association_policy_version") == POLICY_VERSION and (
            resolve_versioned_identities(
                intake, replay["evidence"], model_result=replay["model_result"]
            ).to_dict()
            == report
        )
    except (ValueError, KeyError, TypeError, AttributeError):
        return False
