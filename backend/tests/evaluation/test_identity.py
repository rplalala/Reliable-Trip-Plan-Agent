"""Offline identity association and adjudication with synthetic evidence."""

import copy
import json

import pytest

from backend.evaluation.identity import (
    AUDIT_VERSION,
    EVIDENCE_VERSION,
    REVIEW_VERSION,
    _digest,
    identity_references,
    resolve_identities,
)
from backend.evaluation.identity_cli import main as identity_main
from backend.evaluation.intake import load_batch

pytest_plugins = ("backend.tests.evaluation.test_intake",)


@pytest.fixture
def intake_batch(batch):
    return batch


def prepared(intake_batch, change=None):
    manifest, results, write, save, root = intake_batch
    version = None
    if change:
        version = change(manifest, results, save, root)
    return load_batch(write(version))


def plan(intake, count=1):
    value = intake.to_dict()
    return {
        "schema_version": AUDIT_VERSION,
        "batch_id": value["batch_id"],
        "batch_revision": value["revision"],
        "seed": "fixed-before-inspection",
        "sample_count": count,
    }


def evidence(intake, records):
    value = intake.to_dict()
    return {
        "schema_version": EVIDENCE_VERSION,
        "batch_id": value["batch_id"],
        "batch_revision": value["revision"],
        "records": records,
    }


def search(reference, name, address="Example City", place_id="place-a", raw_count=1):
    return {
        "reference_id": reference["reference_id"],
        "observation_id": "observation-" + reference["reference_id"],
        "source_kind": "independent_google_places",
        "search": {
            "status": "available",
            "query": reference["name"],
            "requested_page_size": 20,
            "retrieved_at": "2026-09-29T00:00:00Z",
            "actual_result_count": raw_count,
            "candidates": [
                {
                    "place_id": place_id,
                    "display_name": name,
                    "formatted_address": "10 Main St, " + address + ", Country",
                    "provider_rank": 0,
                }
            ],
        },
    }


def details(reference, name, place_id="place-a", address="Example City", returned_id=None):
    return {
        "reference_id": reference["reference_id"],
        "observation_id": "observation-" + reference["reference_id"],
        "source_kind": "independent_google_places",
        "details": {
            "status": "available",
            "requested_place_id": reference["claimed_place_id"],
            "retrieved_at": "2026-09-29T00:00:00Z",
            "place": {
                "place_id": returned_id or place_id,
                "display_name": name,
                "formatted_address": "10 Main St, " + address + ", Country",
            },
        },
    }


def review_envelope(intake, observation, reference_id, canonical_id, decision="confirm"):
    value = intake.to_dict()
    return {
        "schema_version": REVIEW_VERSION,
        "batch_id": value["batch_id"],
        "batch_revision": value["revision"],
        "records": [
            {
                "reference_id": reference_id,
                "evidence_hash": _digest(observation),
                "revision": 1,
                "decision": decision,
                "canonical_place_id": canonical_id,
                "reviewer_ref": "independent-reviewer",
                "reviewed_at": "2026-09-29T01:00:00Z",
                "rationale": "Reviewed name and independent candidate context",
            }
        ],
    }


def visit(refs, version, name="Museum A"):
    return next(
        ref
        for ref in refs
        if ref["version"] == version and ref["projection"] == "final" and ref["name"] == name
    )


def test_name_only_and_supplied_id_paths_use_same_strict_evidence(intake_batch):
    def add_id(_, results, _save, _root):
        results["v1"]["itinerary"]["days"][0]["activities"][0]["source_place_id"] = "place-a"
        return "v1"

    intake = prepared(intake_batch, add_id)
    refs = identity_references(intake)
    v0, v1 = visit(refs, "v0"), visit(refs, "v1")
    id_observation = details(v1, "Museum A")
    id_observation["search"] = search(v1, "Museum A")["search"]
    observations = evidence(intake, [search(v0, "Museum A"), id_observation])
    first = resolve_identities(intake, observations, audit_plan=plan(intake))
    items = {item["reference_id"]: item for item in first.to_dict()["records"]}
    assert {items[v0["reference_id"]]["resolution"], items[v1["reference_id"]]["resolution"]} == {
        "resolved",
        "unresolved",
    }
    assert sum(items[r["reference_id"]]["audit_selected"] for r in (v0, v1)) == 1
    pending = v0 if items[v0["reference_id"]]["audit_selected"] else v1
    observed = next(
        r for r in observations["records"] if r["reference_id"] == pending["reference_id"]
    )
    reviews = review_envelope(intake, observed, pending["reference_id"], "place-a")
    second = resolve_identities(intake, observations, reviews, plan(intake)).to_dict()
    items = {item["reference_id"]: item for item in second["records"]}
    assert all(items[r["reference_id"]]["resolution"] == "resolved" for r in (v0, v1))
    assert items[v0["reference_id"]]["claimed_id_association"] == "absent"
    assert items[v1["reference_id"]]["claimed_id_association"] == "consistent"
    assert second["groups"][0]["versions"]["v0"]["final"]["applicable_visits"] == 2
    assert second["groups"][0]["versions"]["v0"]["final"]["resolved_visits"] == 1


@pytest.mark.parametrize(
    ("mutation", "reason"),
    [
        (lambda o: o["search"].update(actual_result_count=2), "competing_or_malformed_candidates"),
        (
            lambda o: o["search"]["candidates"][0].update(display_name="Museo A"),
            "name_mismatch_or_alias",
        ),
        (
            lambda o: o["search"]["candidates"][0].update(
                formatted_address="10 Main St, Other City, Country"
            ),
            "destination_unverified",
        ),
        (
            lambda o: o["search"]["candidates"][0].pop("place_id"),
            "competing_or_malformed_candidates",
        ),
        (
            lambda o: o["search"].update(requested_page_size=1),
            "search_scope_unverified",
        ),
        (
            lambda o: o["search"].update(query="Museum B"),
            "search_query_mismatch",
        ),
        (
            lambda o: o["search"].update(actual_result_count=0, candidates=[]),
            "no_candidate_found",
        ),
        (lambda o: o["search"].update(status="provider_error"), "name_search_unavailable"),
    ],
)
def test_uncertain_searches_require_review(intake_batch, mutation, reason):
    intake = prepared(intake_batch)
    ref = visit(identity_references(intake), "v0")
    observation = search(ref, "Museum A")
    mutation(observation)
    result = resolve_identities(intake, evidence(intake, [observation]), audit_plan=plan(intake))
    record = next(
        item for item in result.to_dict()["records"] if item["reference_id"] == ref["reference_id"]
    )
    assert record["resolution"] == "unresolved"
    assert record["reason"] == reason
    assert record["canonical_place_id"] is None


def test_supplied_id_mismatch_and_conflicting_location_are_not_auto_bound(intake_batch):
    def add_id(_, results, _save, _root):
        activity = results["v1"]["itinerary"]["days"][0]["activities"][0]
        activity["source_place_id"] = "place-a"
        activity["location"] = "Other District"
        return "v1"

    intake = prepared(intake_batch, add_id)
    ref = visit(identity_references(intake), "v1")
    observation = details(ref, "Museum A", returned_id="wrong-returned-id")
    first = resolve_identities(intake, evidence(intake, [observation]), audit_plan=plan(intake))
    record = next(r for r in first.to_dict()["records"] if r["reference_id"] == ref["reference_id"])
    assert record["reason"] == "id_response_mismatch"
    observation["details"]["place"]["place_id"] = "place-a"
    second = resolve_identities(intake, evidence(intake, [observation]), audit_plan=plan(intake))
    record = next(
        r for r in second.to_dict()["records"] if r["reference_id"] == ref["reference_id"]
    )
    assert record["reason"] == "location_association_unverified"
    assert record["claimed_id_association"] == "unverifiable"


def test_supplied_id_same_name_branch_requires_competition_check(intake_batch):
    def add_id(_, results, _save, _root):
        results["v1"]["itinerary"]["days"][0]["activities"][0]["source_place_id"] = "place-a"
        return "v1"

    intake = prepared(intake_batch, add_id)
    ref = visit(identity_references(intake), "v1")
    observation = details(ref, "Museum A")
    first = resolve_identities(intake, evidence(intake, [observation]), audit_plan=plan(intake))
    record = next(r for r in first.to_dict()["records"] if r["reference_id"] == ref["reference_id"])
    assert record["reason"] == "branch_ambiguity_unchecked"
    observation["search"] = search(ref, "Museum A", raw_count=2)["search"]
    second = resolve_identities(intake, evidence(intake, [observation]), audit_plan=plan(intake))
    record = next(
        r for r in second.to_dict()["records"] if r["reference_id"] == ref["reference_id"]
    )
    assert record["reason"] == "competing_candidate"

    def add_specific_location(_, results, _save, _root):
        activity = results["v1"]["itinerary"]["days"][0]["activities"][0]
        activity["source_place_id"] = "place-a"
        activity["location"] = "10 Main St"
        return "v1"

    specific = prepared(intake_batch, add_specific_location)
    specific_ref = visit(identity_references(specific), "v1")
    specific_observation = details(specific_ref, "Museum A")
    third = resolve_identities(
        specific, evidence(specific, [specific_observation]), audit_plan=plan(specific)
    )
    record = next(
        r for r in third.to_dict()["records"] if r["reference_id"] == specific_ref["reference_id"]
    )
    assert record["reason"] == "audit_pending"


def test_same_address_distinct_ids_and_closed_status_do_not_merge(intake_batch):
    intake = prepared(intake_batch)
    ref = visit(identity_references(intake), "v0")
    observation = search(ref, "Museum A")
    observation["search"]["actual_result_count"] = 2
    second = copy.deepcopy(observation["search"]["candidates"][0])
    second["place_id"] = "different-id"
    second["provider_rank"] = 1
    observation["search"]["candidates"].append(second)
    report = resolve_identities(intake, evidence(intake, [observation]), audit_plan=plan(intake))
    record = next(
        r for r in report.to_dict()["records"] if r["reference_id"] == ref["reference_id"]
    )
    assert record["resolution"] == "unresolved"
    assert record["reason"] == "competing_or_malformed_candidates"
    observation["search"]["candidates"] = observation["search"]["candidates"][:1]
    observation["search"]["actual_result_count"] = 1
    observation["search"]["candidates"][0]["business_status"] = "CLOSED_PERMANENTLY"
    report = resolve_identities(intake, evidence(intake, [observation]), audit_plan=plan(intake))
    record = next(
        r for r in report.to_dict()["records"] if r["reference_id"] == ref["reference_id"]
    )
    assert record["reason"] == "audit_pending"


def test_review_history_replays_latest_revision(intake_batch):
    intake = prepared(intake_batch)
    ref = visit(identity_references(intake), "v0")
    observation = search(ref, "Museum A")
    snapshot = evidence(intake, [observation])
    reviews = review_envelope(intake, observation, ref["reference_id"], "place-a")
    first = copy.deepcopy(reviews["records"][0])
    first.update(decision="unresolved", canonical_place_id=None)
    reviews["records"].insert(0, first)
    reviews["records"][1]["revision"] = 2
    report = resolve_identities(intake, snapshot, reviews, plan(intake))
    record = next(
        r for r in report.to_dict()["records"] if r["reference_id"] == ref["reference_id"]
    )
    assert record["resolution"] == "resolved"
    assert [r["revision"] for r in record["review_history"]] == [1, 2]
    reviews["records"][1]["revision"] = 3
    with pytest.raises(ValueError, match="continuous"):
        resolve_identities(intake, snapshot, reviews, plan(intake))


def test_wrong_id_retains_conflict_after_reviewed_name_binding(intake_batch):
    def add_id(_, results, _save, _root):
        results["v1"]["itinerary"]["days"][0]["activities"][0]["source_place_id"] = "wrong-id"
        return "v1"

    intake = prepared(intake_batch, add_id)
    ref = visit(identity_references(intake), "v1")
    observation = details(ref, "Museum B", place_id="wrong-id")
    observation["search"] = search(ref, "Museum A", place_id="right-id")["search"]
    prepared_evidence = evidence(intake, [observation])
    before = resolve_identities(intake, prepared_evidence, audit_plan=plan(intake)).to_dict()
    initial = next(
        item for item in before["records"] if item["reference_id"] == ref["reference_id"]
    )
    assert initial["resolution"] == "unresolved"
    reviews = review_envelope(intake, observation, ref["reference_id"], "right-id")
    after = resolve_identities(intake, prepared_evidence, reviews, plan(intake)).to_dict()
    record = next(item for item in after["records"] if item["reference_id"] == ref["reference_id"])
    assert record["resolution"] == "resolved"
    assert record["canonical_place_id"] == "right-id"
    assert record["claimed_id_association"] == "conflicting"
    assert (
        after["groups"][0]["versions"]["v1"]["final"]["claimed_id_association"]["conflicting"] == 1
    )


def test_high_impact_subject_and_possible_visit_match_require_review(intake_batch):
    def add_requirement(manifest, _results, save, root):
        spec = json.loads((root / "requirements.json").read_text(encoding="utf-8"))
        spec["subjects"] = [{"subject_id": "subject-a", "place_name": "Museum A"}]
        spec["obligations"] = [
            {
                "obligation_id": "required-a",
                "kind": "required_visit",
                "resolution": "resolved",
                "subject_ref": "subject-a",
                "source_refs": [{"field_path": "additional_preferences", "quote": "architecture"}],
            }
        ]
        manifest["groups"][0]["requirement_spec_ref"] = save(
            "requirements.json", spec, "rtpeval_requirements_1"
        )

    intake = prepared(intake_batch, add_requirement)
    refs = identity_references(intake)
    subject = next(ref for ref in refs if ref["kind"] == "requirement_subject")
    v0 = visit(refs, "v0")
    observations = evidence(intake, [search(subject, "Museum A"), search(v0, "Museum A")])
    report = resolve_identities(intake, observations, audit_plan=plan(intake)).to_dict()
    items = {item["reference_id"]: item for item in report["records"]}
    assert items[subject["reference_id"]]["reason"] == "high_impact_review"
    assert items[v0["reference_id"]]["reason"] == "high_impact_review"
    assert not report["audit_selected_reference_ids"]


def test_missing_subject_evidence_keeps_other_visits_reviewable(intake_batch):
    def add_requirement(manifest, _results, save, root):
        spec = json.loads((root / "requirements.json").read_text(encoding="utf-8"))
        spec["subjects"] = [{"subject_id": "subject-a", "place_name": "Unseen Place"}]
        spec["obligations"] = [
            {
                "obligation_id": "required-a",
                "kind": "required_visit",
                "resolution": "resolved",
                "subject_ref": "subject-a",
                "source_refs": [{"field_path": "additional_preferences", "quote": "architecture"}],
            }
        ]
        manifest["groups"][0]["requirement_spec_ref"] = save(
            "requirements.json", spec, "rtpeval_requirements_1"
        )

    intake = prepared(intake_batch, add_requirement)
    ref = visit(identity_references(intake), "v0")
    report = resolve_identities(
        intake, evidence(intake, [search(ref, "Museum A")]), audit_plan=plan(intake)
    ).to_dict()
    record = next(r for r in report["records"] if r["reference_id"] == ref["reference_id"])
    assert record["reason"] == "high_impact_review"


def test_stale_or_unlinked_review_is_rejected(intake_batch):
    intake = prepared(intake_batch)
    ref = visit(identity_references(intake), "v0")
    observation = search(ref, "Museum A")
    snapshot = evidence(intake, [observation])
    reviews = review_envelope(intake, observation, ref["reference_id"], "place-a")
    reviews["records"][0]["evidence_hash"] = "stale"
    with pytest.raises(ValueError, match="Stale"):
        resolve_identities(intake, snapshot, reviews, plan(intake))
    reviews["records"][0]["evidence_hash"] = _digest(observation)
    reviews["records"][0]["canonical_place_id"] = "invented-id"
    with pytest.raises(ValueError, match="absent"):
        resolve_identities(intake, snapshot, reviews, plan(intake))
    unlinked = copy.deepcopy(snapshot)
    unlinked["records"][0]["reference_id"] = "foreign-reference"
    with pytest.raises(ValueError, match="Unlinked"):
        resolve_identities(intake, unlinked, audit_plan=plan(intake))


def test_v3_internal_findings_cannot_change_identity_result(intake_batch):
    intake = prepared(intake_batch)
    ref = visit(identity_references(intake), "v3")
    snapshot = evidence(intake, [search(ref, "Museum A")])
    before = resolve_identities(intake, snapshot, audit_plan=plan(intake)).to_dict()
    changed = copy.deepcopy(intake.to_dict())
    changed["inventory"][0]["runs"]["v3"]["internal_findings"] = [{"status": "FAIL"}]
    after = resolve_identities(changed, snapshot, audit_plan=plan(intake)).to_dict()
    assert before == after


def test_v3_finding_only_file_change_keeps_audit_choice_and_grounding(intake_batch):
    _manifest, results, write, _save, _root = intake_batch
    initial_intake = load_batch(write())
    initial_ref = visit(identity_references(initial_intake), "v3")
    initial = resolve_identities(
        initial_intake,
        evidence(initial_intake, [search(initial_ref, "Museum A")]),
        audit_plan=plan(initial_intake),
    ).to_dict()
    results["v3"]["v3"] = {"internal_findings": [{"status": "FAIL"}]}
    changed_intake = load_batch(write("v3"))
    changed_ref = visit(identity_references(changed_intake), "v3")
    changed = resolve_identities(
        changed_intake,
        evidence(changed_intake, [search(changed_ref, "Museum A")]),
        audit_plan=plan(changed_intake),
    ).to_dict()
    assert initial_ref["reference_id"] != changed_ref["reference_id"]
    assert initial_ref["audit_key"] == changed_ref["audit_key"]
    assert initial["groups"] == changed["groups"]
    assert [r["audit_key"] for r in initial["records"] if r["audit_selected"]] == [
        r["audit_key"] for r in changed["records"] if r["audit_selected"]
    ]


def test_identity_cli_replays_local_files_without_network(intake_batch, monkeypatch, capsys):
    import socket

    _manifest, _results, write, save, root = intake_batch
    manifest_path = write()
    intake = load_batch(manifest_path)
    ref = visit(identity_references(intake), "v0")
    save("identity-evidence.json", evidence(intake, [search(ref, "Museum A")]))
    save("identity-audit.json", plan(intake))

    def forbidden(*_args, **_kwargs):
        raise AssertionError("No network is permitted during identity replay")

    monkeypatch.setattr(socket.socket, "connect", forbidden)
    monkeypatch.setattr(socket, "create_connection", forbidden)
    exit_code = identity_main(
        [
            str(manifest_path),
            str(root / "identity-evidence.json"),
            str(root / "identity-audit.json"),
        ]
    )
    assert exit_code == 3
    assert json.loads(capsys.readouterr().out)["status"] == "needs_adjudication"


@pytest.mark.parametrize("location", ["Country", "State", "2000"])
def test_generic_location_cannot_bypass_branch_search(intake_batch, location):
    def change(_, results, _save, _root):
        activity = results["v1"]["itinerary"]["days"][0]["activities"][0]
        activity.update(source_place_id="place-a", location=location)
        return "v1"

    intake = prepared(intake_batch, change)
    ref = visit(identity_references(intake), "v1")
    observation = details(ref, "Museum A")
    observation["details"]["place"]["formatted_address"] += ", State, 2000"
    report = resolve_identities(
        intake, evidence(intake, [observation]), audit_plan=plan(intake)
    ).to_dict()
    record = next(r for r in report["records"] if r["reference_id"] == ref["reference_id"])
    assert record["reason"] == "branch_ambiguity_unchecked"
    assert record["canonical_place_id"] is None


@pytest.mark.parametrize(
    "field,value",
    [
        ("display_name", "Different Museum"),
        ("formatted_address", "20 Other St, Other City, Country"),
        ("formatted_address", "20 Other St, Example City, Country"),
    ],
)
def test_search_details_contradiction_requires_review(intake_batch, field, value):
    def change(_, results, _save, _root):
        results["v1"]["itinerary"]["days"][0]["activities"][0]["source_place_id"] = "place-a"
        return "v1"

    intake = prepared(intake_batch, change)
    ref = visit(identity_references(intake), "v1")
    observation = details(ref, "Museum A")
    observation["search"] = search(ref, "Museum A")["search"]
    observation["search"]["candidates"][0][field] = value
    report = resolve_identities(
        intake, evidence(intake, [observation]), audit_plan=plan(intake)
    ).to_dict()
    record = next(r for r in report["records"] if r["reference_id"] == ref["reference_id"])
    assert record["reason"] == "contradictory_search_evidence"
    assert record["canonical_place_id"] is None


@pytest.mark.parametrize("version", ["v0", "v1", "v2", "v3"])
@pytest.mark.parametrize(
    "title,expected",
    [
        ("Visit National Aviation Museum", "title_association_unverified"),
        ("Visit Museum A", "audit_pending"),
        ("Museum A and National Aviation Museum", "title_association_unverified"),
    ],
)
def test_title_claim_must_agree_before_automatic_binding(intake_batch, version, title, expected):
    def change(_, results, _save, _root):
        activity = results[version]["itinerary"]["days"][0]["activities"][0]
        activity["title"] = title
        if version != "v0":
            activity["source_place_id"] = "place-a"
        return version

    intake = prepared(intake_batch, change)
    ref = visit(identity_references(intake), version)
    observation = search(ref, "Museum A")
    if version != "v0":
        observation.update(details(ref, "Museum A"))
    report = resolve_identities(
        intake, evidence(intake, [observation]), audit_plan=plan(intake)
    ).to_dict()
    record = next(r for r in report["records"] if r["reference_id"] == ref["reference_id"])
    assert record["reason"] == expected
    assert record["canonical_place_id"] is None


@pytest.mark.parametrize("claimed", [{"bad": "id"}, ["bad-id"]])
def test_malformed_id_with_subject_preserves_batch_report(intake_batch, claimed):
    def change(manifest, results, save, root):
        results["v0"]["itinerary"]["days"][0]["activities"][0]["source_place_id"] = claimed
        spec = json.loads((root / "requirements.json").read_text(encoding="utf-8"))
        spec["subjects"] = [{"subject_id": "subject-a", "place_name": "Unrelated Museum"}]
        spec["obligations"] = [
            {
                "obligation_id": "required-a",
                "kind": "required_visit",
                "resolution": "resolved",
                "subject_ref": "subject-a",
                "source_refs": [{"field_path": "additional_preferences", "quote": "architecture"}],
            }
        ]
        manifest["groups"][0]["requirement_spec_ref"] = save(
            "requirements.json", spec, "rtpeval_requirements_1"
        )
        return "v0"

    intake = prepared(intake_batch, change)
    assert intake.status == "accepted"
    refs = identity_references(intake)
    subject = next(r for r in refs if r["kind"] == "requirement_subject")
    bad = visit(refs, "v0")
    observations = [search(subject, "Unrelated Museum", place_id="subject-id")]
    observations.extend(
        search(r, r["name"], place_id="visit-id") for r in refs if r["kind"] == "primary_visit"
    )
    report = resolve_identities(
        intake, evidence(intake, observations), audit_plan=plan(intake)
    ).to_dict()
    records = {r["reference_id"]: r for r in report["records"]}
    assert records[bad["reference_id"]]["reason"] == "malformed_claimed_id"
    assert records[bad["reference_id"]]["canonical_place_id"] is None
    assert len(records) == len(refs)
    assert sum(r["resolution"] == "resolved" for r in records.values()) == 6
