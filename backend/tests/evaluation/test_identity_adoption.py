"""V0 proposal adoption through offline reports and downstream preparation."""

import asyncio
import copy
import hashlib
import json
from pathlib import Path

import pytest

from backend.evaluation.identity import identity_references
from backend.evaluation.identity import resolve_legacy_identities as resolve_identities
from backend.evaluation.identity_adoption import (
    resolve_legacy_v0_identities as resolve_v0_identities,
)
from backend.evaluation.identity_assistance import IdentityAssistancePacket
from backend.evaluation.intake import load_batch
from backend.evaluation.records import canonical_digest
from backend.evaluation.routes import prepare_routes
from backend.evaluation.snapshot import (
    AcquisitionPolicy,
    Response,
    acquire_snapshot,
    build_evidence_plan,
    build_identity_plan,
    identity_evidence,
)
from backend.evaluation.snapshot_coordinates import prepare_snapshot_coordinates
from backend.tests.evaluation.test_identity import plan, review_envelope
from backend.tests.evaluation.test_requirement_schedule import context

pytest_plugins = ("backend.tests.evaluation.test_intake",)


@pytest.fixture
def adoption_case(batch, tmp_path, request):
    """Persist independently supplied synthetic facts and original model wire material."""
    options = getattr(request, "param", {})
    manifest, results, write, batch_save, root = batch
    if options.get("repeat_visits"):
        from backend.tests.evaluation.test_intake import activity

        results["v0"]["itinerary"]["days"][0]["activities"].extend(
            [
                activity("t2", "Walking", "11:30", "11:50", "transport"),
                activity("c", "Museum A again", "12:00", "13:00", place="Museum A"),
                activity("t3", "Walking", "13:00", "13:20", "transport"),
                activity("d", "Museum B again", "13:30", "14:30", place="Museum B"),
            ]
        )
        write("v0")
    if options.get("claimed_location"):
        results["v0"]["itinerary"]["days"][0]["activities"][0]["location"] = options[
            "claimed_location"
        ]
        write("v0")
    if options.get("transport_mode"):
        results["v0"]["itinerary"]["days"][0]["activities"][1]["transport"] = {
            "mode": options["transport_mode"],
            "from_activity_id": "a",
            "to_activity_id": "b",
        }
        write("v0")
    if options.get("high_impact"):
        spec = json.loads((root / "requirements.json").read_text())
        spec["subjects"] = [{"subject_id": "subject-a", "place_name": "Museum A"}]
        spec["obligations"] = [
            {
                "obligation_id": "required-a",
                "kind": "required_visit",
                "resolution": "resolved",
                "subject_ref": "subject-a",
                "count": {"mode": "exact", "value": 1},
                "source_refs": [{"field_path": "additional_preferences", "quote": "architecture"}],
            }
        ]
        manifest["groups"][0]["requirement_spec_ref"] = batch_save(
            "requirements.json", spec, spec["schema_version"]
        )
    intake = load_batch(write())
    view = intake.to_dict()
    refs = [
        r
        for r in identity_references(intake)
        if r["version"] == "v0" or r["kind"] == "requirement_subject"
    ]
    bodies = {}

    async def transport(request):
        name = request["parameters"]["query"]
        candidate = {
            "id": "shared-venue" if options.get("shared_venue") else "canonical-" + name,
            "displayName": {
                "text": name if options.get("strict") else name.replace("Museum", "Gallery")
            },
            "formattedAddress": "Example City, Country",
            "businessStatus": "OPERATIONAL",
            "location": {"latitude": 10 if name == "Museum A" else 11, "longitude": 20},
        }
        if options.get("coordinates_missing"):
            candidate.pop("location")
        if options.get("components") == "partial":
            candidate["addressComponents"] = [{"longText": "Museum grounds"}]
        elif options.get("components") == "repeated":
            candidate["addressComponents"] = [
                {"longText": "District", "types": ["sublocality"]},
                {"longText": "Neighborhood", "types": ["sublocality"]},
            ]
        elif options.get("components") == "invalid":
            candidate["addressComponents"] = [{"longText": "Museum grounds", "types": 42}]
        bodies[name] = candidate
        candidates = [candidate]
        if options.get("multiple") and name == "Museum A":
            alternative = copy.deepcopy(candidate)
            alternative.update(id="alternate-gallery", displayName={"text": "Another gallery"})
            candidates.append(alternative)
        payload = {"places": candidates}
        if options.get("pagination"):
            payload["nextPageToken"] = "remaining-page"
        return Response(200, json.dumps(payload).encode())

    directory = tmp_path / "identity-snapshot"
    snapshot = asyncio.run(
        acquire_snapshot(
            build_identity_plan(intake), directory, transport, AcquisitionPolicy(max_sends=10)
        )
    )
    observed = identity_evidence(snapshot, historical=bool(options.get("pagination")))
    queued = {q["reference_id"]: q["search"]["candidates"] for q in observed["records"]}
    cases = [
        {
            "reference_id": ref["reference_id"],
            "claim": {
                "place_name": ref["name"],
                "destination": ref["destination"],
                "location": ref["location"],
            },
            "candidates": list(reversed(queued[ref["reference_id"]])),
        }
        for ref in refs
    ]
    packet = IdentityAssistancePacket(cases)
    proposals = {
        "decisions": [
            {
                "reference_id": ref["reference_id"],
                "candidate_id": "shared-venue"
                if options.get("shared_venue")
                else "canonical-" + ref["name"],
                "decision": "match",
                "rationale": "The supplied name variant and address denote the intended museum.",
                "evidence_fields": [
                    "claim.place_name",
                    "candidate.display_name",
                    "candidate.formatted_address",
                ],
            }
            for ref in refs
        ]
    }
    if options.get("components") and options.get("cite_components", True):
        for decision in proposals["decisions"]:
            decision["evidence_fields"].append("candidate.address_components")
    if "fields" in options:
        for decision in proposals["decisions"]:
            decision["evidence_fields"] = options["fields"]
    if "decision" in options:
        proposals["decisions"][0].update(
            decision=options["decision"], candidate_id=None, evidence_fields=[]
        )
    judge = {"instructions": "Match supplied facts only.", "cases": cases}
    response = {
        "id": "response-fixture",
        "status": "completed",
        "model": "fixture-model",
        "created_at": 1791156399 + options.get("provider_clock_skew", 0),
        "output": [
            {
                "type": "message",
                "role": "assistant",
                "content": [
                    {"type": "output_text", "text": json.dumps(packet.references.encode(proposals))}
                ],
            }
        ],
    }

    def save(name, value):
        path = root / name
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        return {"path": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}

    artifacts = {
        "intake": save("source-view.json", view),
        "result": {
            "path": "v0.json",
            "sha256": manifest["groups"][0]["selected_runs"]["v0"]["result_ref"]["sha256"],
        },
        "input": {"path": "input.json", "sha256": manifest["groups"][0]["input_ref"]["sha256"]},
        "provenance": {
            "path": "v0-provenance.json",
            "sha256": manifest["groups"][0]["selected_runs"]["v0"]["provenance_ref"]["sha256"],
        },
        "snapshot": {
            "path": "identity-snapshot/manifest.json",
            "sha256": hashlib.sha256((directory / "manifest.json").read_bytes()).hexdigest(),
        },
        "judge_input": save("judge.json", judge),
        "reference_maps": save("reference-maps.json", {"v0_identity": packet.manifest}),
        "response": save("response.json", response),
        "audit_plan": save("audit.json", plan(intake)),
    }
    # Imported at fixture execution, after the missing public entry point gives the red gate.
    from backend.evaluation.identity_adoption import proposal_schema

    request = {
        "model": "fixture-model",
        "instructions": judge["instructions"] + "\n" + packet.payload["instructions"],
        "input": json.dumps({"cases": packet.payload["cases"]}),
        "text": {
            "format": {
                "type": "json_schema",
                "name": "V0IdentityProposals",
                "strict": True,
                "schema": packet.constrain_schema(proposal_schema()),
            }
        },
        "tools": [],
    }
    artifacts["requests"] = save("requests.json", {"v0_identity": request})
    freeze = {
        "source_hashes": {ref["path"]: ref["sha256"] for ref in artifacts.values()},
        "file_hashes": {
            "requests.json": artifacts["requests"]["sha256"],
            "reference-maps.json": artifacts["reference_maps"]["sha256"],
        },
    }
    if options.get("historical_provenance"):
        freeze["source_hashes"].pop(artifacts["provenance"]["path"])
    artifacts["freeze"] = save("freeze.json", freeze)
    artifacts["authorization"] = save(
        "authorization.json",
        {
            "status": "user_authorized",
            "manifest_sha256": artifacts["freeze"]["sha256"],
            "authorized_at": "2026-10-05",
        },
    )
    if options.get("missing_freeze"):
        artifacts["freeze"] = artifacts["authorization"] = None
    artifacts["attempts"] = save(
        "attempts.json",
        {
            "attempts": [
                {
                    "case": "v0_identity",
                    "request": request,
                    "request_sha256": hashlib.sha256(
                        json.dumps(request, sort_keys=True).encode()
                    ).hexdigest(),
                    "response_sha256": artifacts["response"]["sha256"],
                    "started_at": (
                        "2026-10-04T23:26:39Z"
                        if options.get("utc_receipt")
                        else "2026-10-05T10:26:39+11:00"
                    ),
                    "http_status": 200,
                }
            ]
        },
    )
    material = {
        "schema_version": "rtpeval_v0_identity_material_1",
        "artifact_root": str(root),
        "group_id": "g",
        "artifacts": artifacts,
        "authorization_timezone": "Australia/Sydney",
    }
    path = root / "adoption.json"

    def persist():
        path.write_text(json.dumps(material), encoding="utf-8")
        return path

    return intake, observed, persist(), material, save, persist, refs, results


def test_alias_proposals_are_adopted_offline_while_one_automatic_match_waits_for_audit(
    adoption_case,
):
    intake, evidence, bundle, _, _, _, refs, _ = adoption_case
    before = copy.deepcopy(intake.to_dict())
    native = resolve_identities(intake, evidence, audit_plan=plan(intake)).to_dict()
    assert all(r["resolution"] == "unresolved" for r in native["records"])
    report = resolve_v0_identities(intake, bundle).to_dict()
    selected = [
        r for r in report["records"] if r["reference_id"] in {r["reference_id"] for r in refs}
    ]
    assert sorted(r["reason"] for r in selected) == ["audit_pending", "model_supported_association"]
    adopted = next(r for r in selected if r["resolution"] == "resolved")
    assert adopted["decision_route"] == "model_assisted"
    assert adopted["canonical_place_id"] in ("canonical-Museum A", "canonical-Museum B")
    assert report["adoption_counts"] == {"adopted": 1, "review_pending": 1, "unknown": 0}
    assert report["leg_identity_eligibility"][0]["identity_eligible"] is False
    assert intake.to_dict() == before
    assert [r for r in report["records"] if r["version"] != "v0"] == [
        r for r in native["records"] if r["version"] != "v0"
    ]


def test_reviewed_report_replays_at_coordinate_evidence_plan_and_route_consumers(adoption_case):
    intake, evidence, bundle, material, _, _, _, _ = adoption_case
    first = resolve_v0_identities(intake, bundle).to_dict()
    pending = next(r for r in first["records"] if r["version"] == "v0" and r["audit_selected"])
    observation = next(
        r for r in evidence["records"] if r["reference_id"] == pending["reference_id"]
    )
    reviews = review_envelope(
        intake, observation, pending["reference_id"], pending["model_proposal"]["candidate_id"]
    )
    report = resolve_v0_identities(intake, bundle, reviews)
    directory = bundle.parent / "identity-snapshot"
    coordinates = prepare_snapshot_coordinates(intake, report, directory).to_dict()
    assert coordinates["status"] == "complete"
    assert {r["place_id"] for r in coordinates["records"]} == {
        "canonical-Museum A",
        "canonical-Museum B",
    }
    assert build_evidence_plan(intake, report, [])["identity_report_hash"] == canonical_digest(
        report.to_dict()
    )
    routes = prepare_routes(intake, report, context(intake), identity_snapshot_directory=directory)
    assert routes.status == "complete"
    assert report.to_dict()["leg_identity_eligibility"][0]["identity_eligible"] is True
    forged = report.to_dict()
    next(r for r in forged["records"] if r["version"] == "v0")["canonical_place_id"] = "foreign"
    assert prepare_routes(intake, forged, context(intake)).status == "identity_replay_required"
    assert (
        material["artifacts"]["response"]["sha256"]
        == hashlib.sha256((bundle.parent / "response.json").read_bytes()).hexdigest()
    )


@pytest.mark.parametrize("adoption_case", [{"multiple": True}], indirect=True)
def test_candidates_can_be_reordered_without_changing_independent_facts(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = resolve_v0_identities(intake, bundle).to_dict()
    assert report["adoption_counts"]["adopted"] == 1
    assert all(
        r["model_proposal"]["candidate_id"] != "alternate-gallery"
        for r in report["records"]
        if r["version"] == "v0"
    )


@pytest.mark.parametrize("adoption_case", [{"historical_provenance": True}], indirect=True)
def test_historical_freeze_binds_original_source_even_without_extra_provenance_file(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    assert (
        resolve_v0_identities(intake, bundle).to_dict()["model_assistance_provenance"][
            "audit_freeze_verified"
        ]
        is True
    )


@pytest.mark.parametrize("adoption_case", [{"utc_receipt": True}], indirect=True)
def test_date_only_authorization_uses_declared_timezone_instead_of_receipt_utc_date(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    assert resolve_v0_identities(intake, bundle).to_dict()["adoption_counts"]["adopted"] == 1


@pytest.mark.parametrize("adoption_case", [{"components": "partial"}], indirect=True)
def test_partial_provider_address_component_is_raw_evidence_without_invented_types(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    before = (bundle.parent / "judge.json").read_bytes()
    report = resolve_v0_identities(intake, bundle).to_dict()
    assert report["adoption_counts"] == {"adopted": 1, "review_pending": 1, "unknown": 0}
    assert (bundle.parent / "judge.json").read_bytes() == before


@pytest.mark.parametrize("adoption_case", [{"components": "repeated"}], indirect=True)
def test_repeated_address_types_do_not_reintroduce_native_semantic_veto(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = resolve_v0_identities(intake, bundle).to_dict()
    selected = [r for r in report["records"] if r["version"] == "v0"]
    assert {r["native_reason"] for r in selected} == {"malformed_address_components"}
    assert report["adoption_counts"]["adopted"] == 1


@pytest.mark.parametrize("adoption_case", [{"components": "invalid"}], indirect=True)
def test_shape_invalid_cited_field_remains_ineligible(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = resolve_v0_identities(intake, bundle).to_dict()
    assert report["adoption_counts"] == {"adopted": 0, "review_pending": 0, "unknown": 2}
    assert {r["reason"] for r in report["records"] if r["version"] == "v0"} == {
        "invalid_cited_field"
    }


@pytest.mark.parametrize(
    "adoption_case", [{"components": "invalid", "cite_components": False}], indirect=True
)
def test_uncited_optional_malformed_components_do_not_override_valid_name_address_support(
    adoption_case,
):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    assert resolve_v0_identities(intake, bundle).to_dict()["adoption_counts"]["adopted"] == 1


@pytest.mark.parametrize(
    "adoption_case",
    [
        {"fields": ["candidate.display_name"]},
        {"fields": ["candidate.display_name", "candidate.formatted_address", "claim.location"]},
        {"fields": ["candidate.display_name", "candidate.formatted_address", "candidate.rating"]},
    ],
    indirect=True,
)
def test_unsupported_absent_or_empty_citations_are_reported_per_reference(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = resolve_v0_identities(intake, bundle).to_dict()
    assert report["adoption_counts"] == {"adopted": 0, "review_pending": 0, "unknown": 2}


@pytest.mark.parametrize(
    "adoption_case", [{"decision": "unknown"}, {"decision": "no_supported_match"}], indirect=True
)
def test_model_unknown_is_not_a_fabrication_verdict(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = resolve_v0_identities(intake, bundle).to_dict()
    assert report["adoption_counts"] == {"adopted": 0, "review_pending": 1, "unknown": 1}


@pytest.mark.parametrize("adoption_case", [{"missing_freeze": True}], indirect=True)
def test_missing_pre_response_freeze_blocks_automatic_adoption(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = resolve_v0_identities(intake, bundle).to_dict()
    assert report["adoption_counts"] == {"adopted": 0, "review_pending": 2, "unknown": 0}
    assert {r["reason"] for r in report["records"] if r["version"] == "v0"} == {
        "audit_freeze_unverified"
    }


@pytest.mark.parametrize("adoption_case", [{"high_impact": True}], indirect=True)
def test_requirement_subject_and_possible_visit_still_require_genuine_review(adoption_case):
    intake, _, bundle, _, _, _, refs, _ = adoption_case
    report = resolve_v0_identities(intake, bundle).to_dict()
    protected = [
        r
        for r in report["records"]
        if r["reference_id"] in {r["reference_id"] for r in refs if r["name"] == "Museum A"}
    ]
    assert len(protected) == 2
    assert {r["reason"] for r in protected} == {"high_impact_review"}
    assert all(r["canonical_place_id"] is None for r in protected)


@pytest.mark.parametrize("adoption_case", [{"strict": True, "decision": "unknown"}], indirect=True)
def test_native_supported_identity_is_not_displaced_by_model_unknown(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = resolve_v0_identities(intake, bundle).to_dict()
    resolved = [
        r for r in report["records"] if r["version"] == "v0" and r["resolution"] == "resolved"
    ]
    assert len(resolved) == 1
    assert resolved[0]["decision_route"] == "name_search"


@pytest.mark.parametrize("decision", ["confirm", "reject", "unresolved"])
def test_genuine_human_decisions_take_precedence_over_model_proposals(adoption_case, decision):
    intake, evidence, bundle, _, _, _, refs, _ = adoption_case
    ref = refs[0]
    observation = next(r for r in evidence["records"] if r["reference_id"] == ref["reference_id"])
    reviews = review_envelope(
        intake,
        observation,
        ref["reference_id"],
        "canonical-Museum A" if decision == "confirm" else None,
        decision,
    )
    report = resolve_v0_identities(intake, bundle, reviews).to_dict()
    row = next(r for r in report["records"] if r["reference_id"] == ref["reference_id"])
    assert row["canonical_place_id"] == ("canonical-Museum A" if decision == "confirm" else None)
    assert row["decision_route"] == ("human_adjudication" if decision == "confirm" else None)
    assert row["reason"] == (
        "reviewed_confirmation" if decision == "confirm" else "reviewed_" + decision
    )


@pytest.mark.parametrize("role", ["response", "reference_maps", "result", "snapshot", "audit_plan"])
def test_changed_frozen_material_is_rejected_without_partial_adoption(adoption_case, role):
    intake, _, bundle, material, _, _, _, _ = adoption_case
    path = bundle.parent / material["artifacts"][role]["path"]
    path.write_bytes(path.read_bytes() + b" ")
    with pytest.raises(ValueError, match="hash mismatch"):
        resolve_v0_identities(intake, bundle)


@pytest.mark.parametrize("mutation", ["wrong_version", "changed_projection", "changed_claim"])
def test_source_labels_and_projection_are_not_trusted(adoption_case, mutation):
    intake, _, bundle, material, save, persist, _, _ = adoption_case
    if mutation == "wrong_version":
        result = json.loads((bundle.parent / "v0.json").read_text())
        result["system_version"] = "v1"
        material["artifacts"]["result"] = save("v0.json", result)
    else:
        view = intake.to_dict()
        if mutation == "changed_projection":
            view["inventory"][0]["runs"]["v0"]["final"]["activities"][0]["original"]["title"] = (
                "Foreign"
            )
        else:
            view["inventory"][0]["input"]["destination"] = "Other City"
        material["artifacts"]["intake"] = save("source-view.json", view)
        intake = view
    with pytest.raises(ValueError, match="source|projection"):
        resolve_v0_identities(intake, persist())


@pytest.mark.parametrize(
    "wire_fault", ["unknown_ref", "unknown_candidate", "duplicate", "missing", "foreign_candidate"]
)
def test_response_reference_errors_fail_whole_material(adoption_case, wire_fault):
    intake, _, _, material, save, persist, _, _ = adoption_case
    response = json.loads((Path(material["artifact_root"]) / "response.json").read_text())
    wire = json.loads(response["output"][0]["content"][0]["text"])
    if wire_fault == "unknown_ref":
        wire["decisions"][0]["reference_id"] = "r99"
    elif wire_fault == "unknown_candidate":
        wire["decisions"][0]["candidate_id"] = "p99"
    elif wire_fault == "duplicate":
        wire["decisions"][1] = wire["decisions"][0]
    elif wire_fault == "missing":
        wire["decisions"].pop()
    else:
        wire["decisions"][0]["candidate_id"] = wire["decisions"][1]["candidate_id"]
    response["output"][0]["content"][0]["text"] = json.dumps(wire)
    material["artifacts"]["response"] = save("response.json", response)
    with pytest.raises(ValueError):
        resolve_v0_identities(intake, persist())


def test_offline_cli_reports_pending_review_and_material_errors(adoption_case, capsys):
    from backend.evaluation.identity_adoption_cli import main

    _, _, bundle, _, _, _, _, _ = adoption_case
    assert main([str(bundle), "--legacy"]) == 3
    report = json.loads(capsys.readouterr().out)
    assert report["adoption_counts"]["adopted"] == 1
    assert main([str(bundle) + ".missing"]) == 2
    assert json.loads(capsys.readouterr().out)["status"] == "needs_evidence_correction"


def test_relabeling_assisted_report_as_native_cannot_bypass_replay(adoption_case):
    from backend.evaluation.identity import ASSOCIATION_POLICY_VERSION

    intake, _, bundle, _, _, _, _, _ = adoption_case
    forged = resolve_v0_identities(intake, bundle).to_dict()
    forged["association_policy_version"] = ASSOCIATION_POLICY_VERSION
    assert prepare_routes(intake, forged, context(intake)).status == "identity_replay_required"
    with pytest.raises(ValueError, match="replay"):
        build_evidence_plan(intake, forged, [])


def test_malformed_native_records_keep_existing_replay_required_result(adoption_case):
    intake, evidence, _, _, _, _, _, _ = adoption_case
    native = resolve_identities(intake, evidence, audit_plan=plan(intake)).to_dict()
    native["records"] = None
    assert prepare_routes(intake, native, context(intake)).status == "identity_replay_required"


@pytest.mark.parametrize("field", ["audit_selected", "high_impact", "review_history"])
def test_altered_assistance_review_and_audit_state_is_rejected(adoption_case, field):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = resolve_v0_identities(intake, bundle).to_dict()
    row = next(r for r in report["records"] if r["version"] == "v0")
    row[field] = [{"decision": "confirm"}] if field == "review_history" else not row[field]
    assert prepare_routes(intake, report, context(intake)).status == "identity_replay_required"


@pytest.mark.parametrize("fault", ["missing_response_id", "unexpected_tool"])
def test_saved_response_requires_provenance_and_no_unexpected_tools(adoption_case, fault):
    intake, _, _, material, save, persist, _, _ = adoption_case
    root = Path(material["artifact_root"])
    response = json.loads((root / "response.json").read_text())
    if fault == "missing_response_id":
        response.pop("id")
    else:
        response["output"].append({"type": "function_call", "name": "unapproved_tool"})
    material["artifacts"]["response"] = save("response.json", response)
    receipt = json.loads((root / "attempts.json").read_text())
    receipt["attempts"][0]["response_sha256"] = material["artifacts"]["response"]["sha256"]
    material["artifacts"]["attempts"] = save("attempts.json", receipt)
    with pytest.raises(ValueError, match="response"):
        resolve_v0_identities(intake, persist())


@pytest.mark.parametrize("adoption_case", [{"provider_clock_skew": 3600}], indirect=True)
def test_provider_clock_does_not_replace_authorized_preflight_and_send_binding(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    assert resolve_v0_identities(intake, bundle).to_dict()["adoption_counts"]["adopted"] == 1


@pytest.mark.parametrize(
    "authorized_at",
    ["2026-10-05T23:00:00+11:00", "2026-10-05T00:00:00Z", "2026-10-05T00:00:00"],
)
def test_precise_authorization_after_send_is_rejected(adoption_case, authorized_at):
    intake, _, _, material, save, persist, _, _ = adoption_case
    authorization = json.loads((Path(material["artifact_root"]) / "authorization.json").read_text())
    authorization["authorized_at"] = authorized_at
    material["artifacts"]["authorization"] = save("authorization.json", authorization)
    with pytest.raises(ValueError, match="chronology"):
        resolve_v0_identities(intake, persist())


def test_precise_authorization_before_send_preserves_automatic_adoption(adoption_case):
    intake, _, _, material, save, persist, _, _ = adoption_case
    authorization = json.loads((Path(material["artifact_root"]) / "authorization.json").read_text())
    authorization["authorized_at"] = "2026-10-04T23:00:00Z"
    material["artifacts"]["authorization"] = save("authorization.json", authorization)
    assert resolve_v0_identities(intake, persist()).to_dict()["adoption_counts"]["adopted"] == 1


@pytest.mark.parametrize("adoption_case", [{"strict": True, "missing_freeze": True}], indirect=True)
def test_missing_model_freeze_keeps_already_accepted_native_associations(adoption_case):
    intake, evidence, bundle, _, _, _, _, _ = adoption_case
    native = resolve_identities(intake, evidence, audit_plan=plan(intake)).to_dict()
    assisted = resolve_v0_identities(intake, bundle).to_dict()
    for previous in native["records"]:
        current = next(
            r for r in assisted["records"] if r["reference_id"] == previous["reference_id"]
        )
        assert {key: current[key] for key in previous} == previous
