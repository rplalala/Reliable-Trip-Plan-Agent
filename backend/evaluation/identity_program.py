"""Version-scoped evaluation from original claims and independent API observations."""

from ._addresses import destination_matches, strict_destination_matches
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
from .place_association import program_association, v0_association
from .records import canonical_digest as digest
from .records import freeze, text

LEGACY_POLICY_VERSION = "versioned_api_identity_1"
PREVIOUS_POLICY_VERSION = "versioned_api_identity_2"
POLICY_VERSION = "versioned_api_identity_3"
VERSIONED_TARGET_POLICIES = (PREVIOUS_POLICY_VERSION, POLICY_VERSION)


def subject_bindings(intake):
    """Retained requirement IDs are claims; independent Details must verify them."""
    return {
        (g["group_id"], s["subject_id"]): s.get("source_place_id")
        for g in _intake_dict(intake)["inventory"]
        for s in g["requirement_spec"]["subjects"]
    }


def _subject_search(ref, search):
    if "next_page_token" in search and not text(search["next_page_token"]):
        return "UNKNOWN", "subject_pagination_malformed", None
    if search["actual_result_count"] != len(search["candidates"]) or (
        search["actual_result_count"] >= search["requested_page_size"]
        or search.get("next_page_token")
    ):
        return "UNKNOWN", "subject_search_incomplete", None
    matches, facts = {}, {}
    for raw in search["candidates"]:
        candidate = _candidate(raw)
        if candidate is None:
            return "UNKNOWN", "malformed_subject_candidate", None
        pid = candidate["place_id"]
        identity_facts = {
            key: candidate.get(key)
            for key in ("display_name", "formatted_address", "address_components")
        }
        if pid in facts and facts[pid] != identity_facts:
            return "UNKNOWN", "subject_candidate_facts_conflicting", None
        facts[pid] = identity_facts
        try:
            destination_verified = strict_destination_matches(ref["destination"], candidate)
        except ValueError:
            return "UNKNOWN", "subject_destination_evidence_malformed", None
        if (
            ref["name"] == candidate["display_name"]
            and destination_verified
            and (not text(ref["location"]) or ref["location"] == candidate["formatted_address"])
        ):
            matches[candidate["place_id"]] = candidate
    if len(matches) != 1:
        return "UNKNOWN", "subject_search_ambiguous" if matches else "subject_search_no_match", None
    return "PASS", "independent_api_exact_match", next(iter(matches))


def _check(ref, observation, binding=None, *, historical=False):
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
    if not historical and observation and observation.get("source_kind") is None:
        return "UNKNOWN", "independent_source_missing", None
    if text(claimed):
        details = observation.get("details") if observation else None
        if not details or details["status"] != "available":
            return "UNKNOWN", "id_details_unavailable", None
        if not historical and not text(details.get("retrieved_at")):
            return "UNKNOWN", "id_details_provenance_missing", None
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
        if not historical and not text(search.get("retrieved_at")):
            return "UNKNOWN", "subject_search_provenance_missing", None
        if search.get("query") != ref["name"] or search.get("requested_page_size") != 20:
            return "UNKNOWN", "subject_search_scope_unverified", None
        if not historical:
            return _subject_search(ref, search)
        if search["actual_result_count"] != 1 or len(search["candidates"]) != 1:
            return "UNKNOWN", "subject_search_ambiguous", None
        candidate = _candidate(search["candidates"][0])
        if candidate is None:
            return "UNKNOWN", "malformed_subject_candidate", None
        try:
            destination_verified = destination_matches(ref["destination"], candidate)
        except ValueError:
            return "UNKNOWN", "subject_destination_evidence_malformed", None
        if not destination_verified:
            return "UNKNOWN", "subject_destination_unverified", None
    if ref["name"] != candidate["display_name"]:
        return "FAIL", "api_name_mismatch", None
    if text(ref["location"]) and ref["location"] != candidate["formatted_address"]:
        return "FAIL", "api_address_mismatch", None
    return "PASS", "independent_api_exact_match", candidate["place_id"]


def resolve_versioned_identities(
    intake, evidence, *, model_result=None, historical=False, previous=False
):
    """V0 model results never decide targets or visits of another version."""
    prepared = _intake_dict(intake)
    if historical and previous:
        raise ValueError("Choose one historical identity policy")
    refs = identity_references(prepared)
    observed = _observation_index(evidence, refs, prepared) if historical else {}
    if not historical:
        from .identity_targets import versioned_observations, versioned_references

        refs = versioned_references(prepared)
        observed = versioned_observations(prepared, evidence, refs)
    bindings = subject_bindings(prepared)
    v0_refs = [r for r in refs if r["version"] == "v0"]
    model_records, provenance = {}, None
    if v0_refs:
        from .identity_llm import resolve_llm_identities

        model = resolve_llm_identities(
            prepared, evidence, model_result=model_result, v0_only=True, legacy_v0=historical
        ).to_dict()
        model_records = {r["reference_id"]: r for r in model["records"]}
        provenance = model["model_judgment_provenance"]
    elif model_result is not None:
        raise ValueError("Model results require eligible V0 references")
    records = []
    for ref in refs:
        rid = ref["reference_id"]
        if rid in model_records:
            record = model_records[rid]
            if not historical and not previous and ref["kind"] == "primary_visit":
                record["place_association"] = v0_association(record, observed.get(rid))
            records.append(record)
            continue
        observation = observed.get(rid)
        binding = bindings.get((ref["group_id"], ref["source"].get("subject_id")))
        verdict, reason, canonical = _check(ref, observation, binding, historical=historical)
        detail, search = _evidence_candidates(observation)
        records.append(
            {
                **(
                    {"evidence_reference_id": ref["evidence_reference_id"]}
                    if "evidence_reference_id" in ref
                    else {}
                ),
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
                **(
                    {"place_association": program_association(ref, observation)}
                    if not historical and not previous and ref["kind"] == "primary_visit"
                    else {}
                ),
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
                "association_policy_version": LEGACY_POLICY_VERSION
                if historical
                else PREVIOUS_POLICY_VERSION
                if previous
                else POLICY_VERSION,
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
        report.get("association_policy_version")
        in (*VERSIONED_TARGET_POLICIES, LEGACY_POLICY_VERSION)
        or "identity_versioned_replay" in report
        or any(
            isinstance(r, dict) and ("programmatic_judgment" in r or "place_association" in r)
            for r in records
        )
    )


def verify_versioned_report(intake, report):
    """Recompute the complete report; stamps alone never certify programmatic verdicts."""
    try:
        replay = report["identity_versioned_replay"]
        policy = report.get("association_policy_version")
        return policy in (*VERSIONED_TARGET_POLICIES, LEGACY_POLICY_VERSION) and (
            resolve_versioned_identities(
                intake,
                replay["evidence"],
                model_result=replay["model_result"],
                historical=policy == LEGACY_POLICY_VERSION,
                previous=policy == PREVIOUS_POLICY_VERSION,
            ).to_dict()
            == report
        )
    except (ValueError, KeyError, TypeError, AttributeError):
        return False
