"""Version-owned requirement binding through offline evaluator public seams."""

import asyncio
import copy
import json

import pytest

from backend.evaluation.identity import identity_references, resolve_identities
from backend.evaluation.identity_cli import main as identity_main
from backend.evaluation.identity_llm import prepare_identity_judgment
from backend.evaluation.identity_program import resolve_versioned_identities
from backend.evaluation.preparation import identity_ready
from backend.evaluation.requirement_schedule import score_requirement_schedule
from backend.evaluation.snapshot import (
    AcquisitionPolicy,
    Response,
    acquire_snapshot,
    build_evidence_plan,
    build_identity_plan,
    identity_evidence,
)
from backend.tests.evaluation.test_identity import details, evidence, prepared, search
from backend.tests.evaluation.test_identity_llm import model_material
from backend.tests.evaluation.test_requirement_schedule import context

pytest_plugins = ("backend.tests.evaluation.test_intake",)


def requirement_batch(
    batch,
    *,
    bound=True,
    location=None,
    destination=None,
    identified=False,
    kind="required_visit",
):
    def change(manifest, _results, save, root):
        spec = json.loads((root / "requirements.json").read_text())
        if destination:
            original = json.loads((root / "input.json").read_text())
            original["destination"] = destination
            manifest["groups"][0]["input_ref"] = save("input.json", original)
            spec["input_sha256"] = manifest["groups"][0]["input_ref"]["sha256"]
            for version, result in _results.items():
                result["itinerary"]["destination"] = destination
                provenance = json.loads((root / f"{version}-provenance.json").read_text())
                provenance["input_sha256"] = spec["input_sha256"]
                manifest["groups"][0]["selected_runs"][version]["provenance_ref"] = save(
                    f"{version}-provenance.json", provenance, "rtpeval_provenance_1"
                )
                batch[2](version)
        subject = {"subject_id": "museum", "place_name": "Museum A"}
        if bound:
            subject["source_place_id"] = "venue-a"
        if location is not None:
            subject["location"] = location
        spec["subjects"] = [subject]
        spec["obligations"] = [
            {
                "obligation_id": "visit",
                "kind": "required_visit",
                "resolution": "resolved",
                "subject_ref": "museum",
                "count": {"mode": "exact", "value": 1},
                "source_refs": [{"field_path": "additional_preferences", "quote": "architecture"}],
            }
        ]
        obligation = spec["obligations"][0]
        if kind != "required_visit":
            obligation["kind"] = kind
            del obligation["count"]
            if kind == "excluded_visit":
                obligation["scope"] = "whole_trip"
            else:
                obligation.update(
                    date="2020-01-01",
                    match="single_visit",
                    conditions={"duration": {"mode": "exact", "seconds": 3600}},
                )
        manifest["groups"][0]["requirement_spec_ref"] = save(
            "requirements.json", spec, spec["schema_version"]
        )
        if identified:
            for version in ("v1", "v2", "v3"):
                for activity in _results[version]["itinerary"]["days"][0]["activities"]:
                    if activity["activity_kind"] == "main_poi":
                        activity.update(
                            source_place_id="venue-" + activity["activity_id"],
                            location="10 Main St, Example City, Country",
                        )
                batch[2](version)

    return prepared(batch, change)


def test_each_version_owns_target_and_only_v0_target_enters_model_packet(batch):
    intake = requirement_batch(batch)
    subject = next(r for r in identity_references(intake) if r["kind"] == "requirement_subject")
    observed = evidence(
        intake, [details({**subject, "claimed_place_id": "venue-a"}, "Museum A", "venue-a")]
    )
    report = resolve_identities(intake, observed).to_dict()
    targets = [r for r in report["records"] if r["kind"] == "requirement_subject"]
    assert {r["version"]: r["grounding_verdict"] for r in targets} == {
        "v0": "UNKNOWN",
        "v1": "PASS",
        "v2": "PASS",
        "v3": "PASS",
    }
    assert len({r["reference_id"] for r in targets}) == 4
    assert identity_ready(intake.to_dict(), report)
    packet = prepare_identity_judgment(intake, observed, model="fixture-model").to_dict()
    cases = json.loads(packet["request"]["input"])["cases"]
    assert {c["version"] for c in cases} == {"v0"}
    assert sum(c["kind"] == "requirement_subject" for c in cases) == 1
    target = next(c for c in cases if c["kind"] == "requirement_subject")
    assert target["claim"]["claimed_place_id"] is not None


def test_old_packet_requires_explicit_historical_program_replay(batch, capsys):
    intake = requirement_batch(batch, bound=False)
    refs = identity_references(intake)
    observed = evidence(intake, [search(r, r["name"], place_id="venue-" + r["name"]) for r in refs])
    old_model = model_material(intake, observed, historical=False, legacy_v0=True)
    with pytest.raises(ValueError, match="packet/source mismatch"):
        resolve_identities(intake, observed, model_result=old_model)
    old_report = resolve_versioned_identities(
        intake, observed, model_result=old_model, historical=True
    ).to_dict()
    assert old_report["association_policy_version"] == "versioned_api_identity_1"
    assert identity_ready(intake.to_dict(), old_report)
    save = batch[3]
    save("observed.json", observed)
    save("model.json", old_model)
    root = batch[4]
    assert (
        identity_main(
            [
                str(root / "manifest.json"),
                str(root / "observed.json"),
                "--model-result",
                str(root / "model.json"),
                "--historical-program",
            ]
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out) == old_report


def test_program_target_filters_all_candidates_before_unique_id_binding(batch):
    intake = requirement_batch(batch, bound=False)
    subject = next(r for r in identity_references(intake) if r["kind"] == "requirement_subject")
    observation = search(subject, "Museum A", place_id="venue-a")
    unrelated = copy.deepcopy(observation["search"]["candidates"][0])
    unrelated.update(place_id="annex", display_name="Museum A Annex", provider_rank=0)
    observation["search"]["candidates"][0]["provider_rank"] = 9
    observation["search"].update(actual_result_count=2)
    observation["search"]["candidates"].insert(0, unrelated)
    report = resolve_identities(intake, evidence(intake, [observation])).to_dict()
    target = next(
        r for r in report["records"] if r["kind"] == "requirement_subject" and r["version"] == "v1"
    )
    assert target["grounding_verdict"] == "PASS"
    assert target["canonical_place_id"] == "venue-a"


@pytest.mark.parametrize("kind", ["required_visit", "excluded_visit", "fixed_visit_time"])
def test_requirement_checks_do_not_borrow_program_target_for_v0(batch, kind):
    intake = requirement_batch(batch, identified=True, kind=kind)
    refs = identity_references(intake)
    observations = []
    for ref in refs:
        if ref["kind"] == "requirement_subject":
            observations.append(
                details({**ref, "claimed_place_id": "venue-a"}, "Museum A", "venue-a")
            )
        elif ref["version"] == "v0":
            observations.append(
                search(
                    ref, ref["name"], place_id="venue-a" if ref["name"] == "Museum A" else "venue-b"
                )
            )
        else:
            observations.append(details(ref, ref["name"], ref["claimed_place_id"]))
    observed = evidence(intake, observations)

    def uncertain_target(row, case):
        if case["kind"] == "requirement_subject":
            row.update(
                decision="unknown",
                candidate_id=None,
                evidence_fields=[],
                destination_assessment="unknown",
            )

    pending = resolve_identities(intake, observed).to_dict()
    report = resolve_identities(
        intake,
        observed,
        model_result=model_material(intake, observed, decisions=uncertain_target, historical=False),
    ).to_dict()
    assert [r for r in pending["records"] if r["version"] != "v0"] == [
        r for r in report["records"] if r["version"] != "v0"
    ]
    scored = score_requirement_schedule(intake, report, context(intake)).to_dict()
    assert scored["status"] == "complete", scored["diagnostics"]
    program_state = "FAIL" if kind == "excluded_visit" else "PASS"
    assert {r["version"]: r["requirements"]["state"] for r in scored["results"]} == {
        "v0": "UNKNOWN",
        "v1": program_state,
        "v2": program_state,
        "v3": program_state,
    }
    plan = build_evidence_plan(intake, report, [])
    assert {r["reference_id"] for r in plan["references"]} == {
        r["reference_id"] for r in report["records"]
    }


def test_program_target_uses_typed_region_city_and_hierarchical_sublocalities(batch):
    intake = requirement_batch(batch, bound=False, destination="Example City, Country")
    subject = next(r for r in identity_references(intake) if r["kind"] == "requirement_subject")
    observation = search(subject, "Museum A", address="District", place_id="venue-a")
    observation["search"]["candidates"][0]["address_components"] = [
        {"longText": "Main St", "types": ["sublocality_level_4", "sublocality", "political"]},
        {"longText": "District", "types": ["sublocality_level_1", "sublocality", "political"]},
        {"longText": "Example City", "types": ["administrative_area_level_1", "political"]},
        {"longText": "Country", "shortText": "CC", "types": ["country", "political"]},
    ]
    report = resolve_identities(intake, evidence(intake, [observation])).to_dict()
    target = next(
        r for r in report["records"] if r["kind"] == "requirement_subject" and r["version"] == "v1"
    )
    assert target["grounding_verdict"] == "PASS"


@pytest.mark.parametrize(
    "fault",
    [
        "no_match",
        "multiple_ids",
        "missing_candidate",
        "missing_time",
        "missing_source",
        "missing_query",
        "page_saturated",
        "no_hits",
        "wrong_query",
        "next_page",
        "malformed",
        "typed_conflict",
        "id_conflict",
        "wrong_destination",
    ],
)
def test_incomplete_or_nonunique_target_evidence_stays_unknown(batch, fault):
    intake = requirement_batch(batch, bound=False)
    subject = next(r for r in identity_references(intake) if r["kind"] == "requirement_subject")
    observation = search(subject, "Museum A", place_id="venue-a")
    data = observation["search"]
    candidate = data["candidates"][0]
    if fault == "no_match":
        candidate["display_name"] = "Museum a"
    elif fault in ("multiple_ids", "id_conflict"):
        other = copy.deepcopy(candidate)
        other.update(place_id="venue-other" if fault == "multiple_ids" else "venue-a")
        if fault == "id_conflict":
            other["display_name"] = "Other venue"
        data["candidates"].append(other)
        data["actual_result_count"] = 2
    elif fault == "missing_candidate":
        data["actual_result_count"] = 2
    elif fault == "missing_time":
        del data["retrieved_at"]
    elif fault == "missing_source":
        del observation["source_kind"]
    elif fault == "missing_query":
        del data["query"]
    elif fault == "page_saturated":
        data.update(
            actual_result_count=20, candidates=[copy.deepcopy(candidate) for _ in range(20)]
        )
    elif fault == "no_hits":
        data.update(actual_result_count=0, candidates=[])
    elif fault == "wrong_query":
        data["query"] = "another query"
    elif fault == "next_page":
        data["next_page_token"] = "another-page"
    elif fault == "malformed":
        del candidate["place_id"]
    elif fault == "typed_conflict":
        candidate["address_components"] = [
            {"longText": "Example City", "types": ["locality"]},
            {"longText": "Other City", "types": ["locality"]},
        ]
    else:
        candidate["formatted_address"] = "10 Main St, Other City, Country"
    report = resolve_identities(intake, evidence(intake, [observation])).to_dict()
    targets = [r for r in report["records"] if r["kind"] == "requirement_subject"]
    assert {r["grounding_verdict"] for r in targets} == {"UNKNOWN"}
    assert all(r["canonical_place_id"] is None for r in targets)
    assert identity_ready(intake.to_dict(), report)


def test_snapshot_retains_pagination_uncertainty_for_program_targets(batch):
    intake = requirement_batch(batch, bound=False)

    async def transport(request):
        name = request["parameters"]["query"]
        return Response(
            200,
            json.dumps(
                {
                    "places": [
                        {
                            "id": "venue-a",
                            "displayName": {"text": name},
                            "formattedAddress": "10 Main St, Example City, Country",
                        }
                    ],
                    "nextPageToken": "remaining-page",
                }
            ).encode(),
        )

    snapshot = asyncio.run(
        acquire_snapshot(
            build_identity_plan(intake),
            batch[4] / "snapshot",
            transport,
            AcquisitionPolicy(max_sends=20, max_attempts=1),
        )
    )
    report = resolve_identities(intake, identity_evidence(snapshot)).to_dict()
    targets = [r for r in report["records"] if r["kind"] == "requirement_subject"]
    assert {r["grounding_verdict"] for r in targets} == {"UNKNOWN"}


@pytest.mark.parametrize("assessment,expected", [("consistent", "PASS"), ("contradictory", "FAIL")])
def test_v0_target_model_verdict_and_requirement_failure_are_version_owned(
    batch, assessment, expected
):
    intake = requirement_batch(batch, identified=True)
    refs = identity_references(intake)
    observations = [
        details({**r, "claimed_place_id": "venue-a"}, "Museum A", "venue-a")
        if r["kind"] == "requirement_subject"
        else search(r, r["name"], place_id="venue-a" if r["name"] == "Museum A" else "venue-b")
        if r["version"] == "v0"
        else details(r, r["name"], r["claimed_place_id"])
        for r in refs
    ]
    observed = evidence(intake, observations)

    def assess(row, case):
        if case["kind"] == "requirement_subject":
            row["destination_assessment"] = assessment

    report = resolve_identities(
        intake,
        observed,
        model_result=model_material(intake, observed, decisions=assess, historical=False),
    ).to_dict()
    targets = {r["version"]: r for r in report["records"] if r["kind"] == "requirement_subject"}
    assert targets["v0"]["grounding_verdict"] == expected
    assert all(targets[v]["grounding_verdict"] == "PASS" for v in ("v1", "v2", "v3"))
    scored = score_requirement_schedule(intake, report, context(intake)).to_dict()
    assert {r["version"]: r["requirements"]["state"] for r in scored["results"]} == {
        "v0": expected,
        "v1": "PASS",
        "v2": "PASS",
        "v3": "PASS",
    }
    altered = copy.deepcopy(report)
    next(
        r for r in altered["records"] if r["kind"] == "requirement_subject" and r["version"] == "v1"
    )["evidence_reference_id"] = "foreign"
    assert not identity_ready(intake.to_dict(), altered)


@pytest.mark.parametrize(
    "second_address,expected",
    [
        ("10 Main St, Example City, Country", "PASS"),
        ("20 Main St, Example City, Country", "UNKNOWN"),
    ],
)
def test_same_id_duplicates_must_agree_before_adopting_target(batch, second_address, expected):
    intake = requirement_batch(batch, bound=False)
    subject = next(r for r in identity_references(intake) if r["kind"] == "requirement_subject")
    observation = search(subject, "Museum A", place_id="venue-a")
    second = copy.deepcopy(observation["search"]["candidates"][0])
    second.update(formatted_address=second_address, provider_rank=8)
    observation["search"].update(actual_result_count=2)
    observation["search"]["candidates"].append(second)
    report = resolve_identities(intake, evidence(intake, [observation])).to_dict()
    target = next(
        r for r in report["records"] if r["kind"] == "requirement_subject" and r["version"] == "v1"
    )
    assert target["grounding_verdict"] == expected


@pytest.mark.parametrize("discriminator", ["address", "destination"])
def test_strict_destination_and_supplied_address_disambiguate_same_name_ids(batch, discriminator):
    address = "10 Main St, Example City, Country"
    intake = requirement_batch(
        batch, bound=False, location=address if discriminator == "address" else None
    )
    subject = next(r for r in identity_references(intake) if r["kind"] == "requirement_subject")
    observation = search(subject, "Museum A", place_id="venue-a")
    second = copy.deepcopy(observation["search"]["candidates"][0])
    second.update(
        place_id="venue-other",
        formatted_address=(
            "20 Main St, Example City, Country"
            if discriminator == "address"
            else "10 Main St, Other City, Country"
        ),
    )
    observation["search"].update(actual_result_count=2)
    observation["search"]["candidates"].append(second)
    report = resolve_identities(intake, evidence(intake, [observation])).to_dict()
    target = next(
        r for r in report["records"] if r["kind"] == "requirement_subject" and r["version"] == "v1"
    )
    assert target["canonical_place_id"] == "venue-a"
