"""V0 correspondence output contracts through offline public seams."""

import asyncio
import copy
import json

import pytest

from backend.evaluation.identity import identity_references, resolve_identities
from backend.evaluation.identity_cli import main as identity_main
from backend.evaluation.identity_llm import prepare_identity_judgment
from backend.evaluation.preparation import identity_ready
from backend.evaluation.quality_report import build_quality_report
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
from backend.tests.evaluation.test_identity import evidence, prepared, search
from backend.tests.evaluation.test_identity_llm import model_material
from backend.tests.evaluation.test_requirement_schedule import context

pytest_plugins = ("backend.tests.evaluation.test_intake",)


def test_current_packet_enumerates_supported_citations_and_preserves_historical_schema(batch):
    def supplied(_manifest, results, _save, _root):
        results["v0"]["itinerary"]["days"][0]["activities"][0]["location"] = "10 Main St"
        return "v0"

    intake = prepared(batch, supplied)
    observed = evidence(intake, [])
    packet = prepare_identity_judgment(intake, observed, model="fixture-model").to_dict()
    variants = packet["request"]["text"]["format"]["schema"]["properties"]["decisions"]["items"][
        "anyOf"
    ]
    properties = next(
        v["properties"]
        for v in variants
        if "not_supplied" not in v["properties"]["address_assessment"]["enum"]
    )
    assert properties["evidence_fields"]["items"]["enum"] == [
        "claim.place_name",
        "claim.destination",
        "claim.location",
        "claim.claimed_place_id",
        "claim.original_title",
        "candidate.display_name",
        "candidate.formatted_address",
        "candidate.address_components",
        "candidate.observations",
        "case.candidates",
    ]
    assert packet["association_policy_version"] == "v0_identity_correspondence_3"
    cases = json.loads(packet["request"]["input"])["cases"]
    assert {c["version"] for c in cases} == {"v0"}
    absent = next(
        v["properties"]
        for v in variants
        if v["properties"]["address_assessment"]["enum"] == ["not_supplied"]
    )
    assert "claim.location" not in absent["evidence_fields"]["items"]["enum"]
    assert absent["reference_id"]["enum"] == [
        c["reference_id"] for c in cases if c["claim"]["location"] is None
    ]
    assert properties["reference_id"]["enum"] == [
        c["reference_id"] for c in cases if c["claim"]["location"]
    ]
    historical = prepare_identity_judgment(
        intake, observed, model="fixture-model", historical=True
    ).to_dict()
    items = historical["request"]["text"]["format"]["schema"]["properties"]["decisions"]["items"][
        "properties"
    ]["evidence_fields"]["items"]
    assert items == {"type": "string"}


@pytest.mark.parametrize("decision", ["unknown", "no_supported_match"])
@pytest.mark.parametrize(
    "assessment",
    ["unknown", "different_precision", "equivalent", "incorrect_claim", "different_place"],
)
def test_missing_address_requires_not_supplied_even_without_match(batch, decision, assessment):
    intake = prepared(batch)
    observed = evidence(intake, [])

    def incompatible(row, _case):
        row.update(decision=decision, address_assessment=assessment)

    material = model_material(intake, observed, decisions=incompatible, historical=False)
    with pytest.raises(ValueError, match="location presence"):
        resolve_identities(intake, observed, model_result=material)


@pytest.mark.parametrize("assessment", ["incorrect_claim", "different_place"])
def test_recognized_wrong_address_keeps_correspondence_and_failure_downstream(batch, assessment):
    def wrong(_manifest, results, _save, _root):
        results["v0"]["itinerary"]["days"][0]["activities"][0]["location"] = "Wrong address"
        return "v0"

    intake = prepared(batch, wrong)
    original = intake.to_dict()
    root = batch[4]

    async def transport(request):
        name = request["parameters"].get("query") or "Museum A"
        place = {
            "id": "venue-a" if name == "Museum A" else "venue-b",
            "displayName": {"text": name},
            "formattedAddress": "10 Main St, Example City, Country",
            "location": {"latitude": 1, "longitude": 2},
        }
        return Response(
            200,
            json.dumps({"places": [place]} if "query" in request["parameters"] else place).encode(),
        )

    directory = root / "independent"
    snapshot = asyncio.run(
        acquire_snapshot(
            build_identity_plan(intake),
            directory,
            transport,
            AcquisitionPolicy(max_sends=20, max_attempts=1),
        )
    )
    observed = identity_evidence(snapshot)

    def assess(row, case):
        if case["claim"]["location"]:
            row["address_assessment"] = assessment
            row["evidence_fields"].append("claim.location")

    material = model_material(intake, observed, decisions=assess, historical=False)
    saved = copy.deepcopy(material)
    report = resolve_identities(intake, observed, model_result=material).to_dict()
    visits = [r for r in report["records"] if r["version"] == "v0"]
    failed = visits[0]
    assert failed["candidate_correspondence"] == {"decision": "match", "candidate_id": "venue-a"}
    assert failed["grounding_verdict"] == "FAIL"
    assert failed["canonical_place_id"] is None
    assert visits[1]["grounding_verdict"] == "PASS"
    assert identity_ready(original, report)
    coordinates = prepare_snapshot_coordinates(intake, report, directory).to_dict()
    assert coordinates["status"] == "complete", coordinates
    assert any(
        r["reference_id"] == failed["reference_id"] for r in coordinates["unadopted_references"]
    )
    routes = prepare_routes(
        intake, report, context(intake), identity_snapshot_directory=directory
    ).to_dict()
    leg = next(r for r in routes["results"] if r["version"] == "v0")["legs"][0]
    assert leg["canonical_endpoints"] == [None, "venue-b"]
    assert leg["identity_grounding_verdicts"] == ["FAIL", "PASS"]
    assert leg["expected_context"] is None
    downstream = root / "downstream"
    asyncio.run(
        acquire_snapshot(
            build_evidence_plan(intake, report, []),
            downstream,
            transport,
            AcquisitionPolicy(max_sends=20, max_attempts=1),
        )
    )
    quality = build_quality_report(
        intake, report, downstream, context(intake), generated_at="2026-10-06T00:00:00Z"
    ).to_dict()
    assert quality["status"] == "complete", quality["diagnostics"]
    v0 = quality["groups"][0]["versions"]["v0"]["dimensions"]["grounding"]
    assert v0["counts"] == {"PASS": 1, "FAIL": 1, "UNKNOWN": 0}
    assert v0["rates"]["verified_fraction"] == 0.5
    metrics = quality["groups"][0]["versions"]["v0"]["primary_metrics"]
    assert (
        metrics["grounding"]["checks"][0]["identity"]["candidate_correspondence"]
        == failed["candidate_correspondence"]
    )
    assert metrics["opening"]["checks"][0]["identity_grounding_verdict"] == "FAIL"
    assert intake.to_dict() == original
    assert material == saved


@pytest.mark.parametrize("decision", ["unknown", "no_supported_match"])
def test_no_candidates_is_unknown_and_never_fills_an_address(batch, decision):
    intake = prepared(batch)
    observed = evidence(intake, [])
    material = model_material(
        intake,
        observed,
        historical=False,
        decisions=lambda row, _case: row.update(decision=decision),
    )
    report = resolve_identities(intake, observed, model_result=material).to_dict()
    visits = [r for r in report["records"] if r["version"] == "v0"]
    assert {r["grounding_verdict"] for r in visits} == {"UNKNOWN"}
    assert all(
        r["canonical_place_id"] is None and r["original_claim"]["location"] is None for r in visits
    )
    assert all(r["model_judgment"]["address_assessment"] == "not_supplied" for r in visits)
    assert identity_ready(intake.to_dict(), report)


@pytest.mark.parametrize("decision", ["match", "unknown", "no_supported_match"])
def test_present_address_forbids_not_supplied_for_every_decision(batch, decision):
    def supplied(_manifest, results, _save, _root):
        results["v0"]["itinerary"]["days"][0]["activities"][0]["location"] = "10 Main St"
        return "v0"

    intake = prepared(batch, supplied)
    observed = evidence(
        intake, [search(r, r["name"]) for r in identity_references(intake) if r["version"] == "v0"]
    )

    def assess(row, _case):
        row.update(decision=decision)
        if decision != "match":
            row.update(candidate_id=None, evidence_fields=[])

    material = model_material(intake, observed, decisions=assess, historical=False)
    with pytest.raises(ValueError, match="location presence"):
        resolve_identities(intake, observed, model_result=material)


@pytest.mark.parametrize(
    "citation",
    [
        "candidate.place_id",
        "candidate.location",
        "candidate.name",
        "candidate.address",
        "candidate.opening_hours",
        "claim.location",
        "claim.claimed_place_id",
        "candidate.address_components",
        " case.candidates",
        "candidate.formatted_address ",
    ],
)
def test_unsupported_or_empty_citations_are_rejected_without_normalization(batch, citation):
    intake = prepared(batch)
    observed = evidence(
        intake, [search(r, r["name"]) for r in identity_references(intake) if r["version"] == "v0"]
    )
    material = model_material(
        intake,
        observed,
        historical=False,
        decisions=lambda row, _case: row["evidence_fields"].append(citation),
    )
    saved = copy.deepcopy(material)
    with pytest.raises(ValueError, match="citation"):
        resolve_identities(intake, observed, model_result=material)
    assert material == saved


def test_supported_nonempty_citations_import_through_cli_with_short_ids(batch, capsys):
    def supplied(_manifest, results, _save, _root):
        results["v0"]["itinerary"]["days"][0]["activities"][0].update(
            location="10 Main St", source_place_id="venue-a"
        )
        return "v0"

    intake = prepared(batch, supplied)
    refs = [r for r in identity_references(intake) if r["version"] == "v0"]
    observations = [
        search(r, r["name"], place_id="venue-a" if index == 0 else "venue-b")
        for index, r in enumerate(refs)
    ]
    for observation in observations:
        observation["search"]["candidates"][0]["address_components"] = [
            {"longText": "Example City", "types": ["locality"]}
        ]
    observed = evidence(intake, observations)

    def support(row, case):
        row["evidence_fields"].extend(
            [
                "claim.original_title",
                "candidate.address_components",
                "candidate.observations",
                "case.candidates",
            ]
        )
        if case["claim"]["location"]:
            row["address_assessment"] = "different_precision"
            row["evidence_fields"].extend(["claim.location", "claim.claimed_place_id"])

    material = model_material(intake, observed, decisions=support, historical=False)
    original = intake.to_dict()
    saved = copy.deepcopy(material)
    _manifest, _results, write, save, root = batch
    save("observed.json", observed)
    save("model.json", material)
    assert (
        identity_main(
            [str(write()), str(root / "observed.json"), "--prepare", "--model", "fixture-model"]
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out) == material["packet"]
    assert (
        identity_main(
            [str(write()), str(root / "observed.json"), "--model-result", str(root / "model.json")]
        )
        == 0
    )
    report = json.loads(capsys.readouterr().out)
    visits = [r for r in report["records"] if r["version"] == "v0"]
    assert [r["canonical_place_id"] for r in visits] == ["venue-a", "venue-b"]
    assert [r["grounding_verdict"] for r in visits] == ["PASS", "PASS"]
    assert (
        report["model_judgment_provenance"]["association_policy_version"]
        == "v0_identity_correspondence_3"
    )
    assert identity_ready(original, report)
    assert material == saved and intake.to_dict() == original
    forged = copy.deepcopy(report)
    next(r for r in forged["records"] if r["version"] == "v0")["candidate_correspondence"][
        "candidate_id"
    ] = "venue-b"
    assert not identity_ready(original, forged)


@pytest.mark.parametrize(
    "fault",
    [
        "partial",
        "duplicate",
        "foreign_reference",
        "foreign_candidate",
        "old_policy",
        "request",
        "response_hash",
        "source",
    ],
)
def test_current_import_requires_complete_owned_decisions_and_exact_provenance(batch, fault):
    intake = prepared(batch)
    refs = [r for r in identity_references(intake) if r["version"] == "v0"]
    observed = evidence(
        intake, [search(r, r["name"], place_id="venue-" + str(i)) for i, r in enumerate(refs)]
    )
    material = model_material(intake, observed, historical=False)
    response = material["response"]
    content = response["output"][0]["content"][0]
    wire = json.loads(content["text"])
    if fault == "partial":
        wire["decisions"].pop()
    elif fault == "duplicate":
        wire["decisions"][1] = copy.deepcopy(wire["decisions"][0])
    elif fault == "foreign_reference":
        wire["decisions"][0]["reference_id"] = "r999"
    elif fault == "foreign_candidate":
        wire["decisions"][0]["candidate_id"] = wire["decisions"][1]["candidate_id"]
    elif fault == "old_policy":
        material["packet"]["association_policy_version"] = "v0_identity_correspondence_1"
    elif fault == "request":
        material["packet"]["request"]["instructions"] += " Altered"
        material["packet"]["request_sha256"] = canonical_digest(material["packet"]["request"])
    elif fault == "source":
        observed["records"][0]["search"]["candidates"][0]["display_name"] = "Changed"
    content["text"] = json.dumps(wire)
    material["response_sha256"] = canonical_digest(response) if fault != "response_hash" else "bad"
    saved = copy.deepcopy(material)
    with pytest.raises(ValueError):
        resolve_identities(intake, observed, model_result=material)
    assert material == saved


@pytest.mark.parametrize(
    "assessment,destination",
    [("unknown", "consistent"), ("equivalent", "unknown")],
)
def test_correspondence_with_insufficient_correctness_support_stays_unknown(
    batch, assessment, destination
):
    def supplied(_manifest, results, _save, _root):
        results["v0"]["itinerary"]["days"][0]["activities"][0]["location"] = "10 Main St"
        return "v0"

    intake = prepared(batch, supplied)
    observed = evidence(
        intake, [search(r, r["name"]) for r in identity_references(intake) if r["version"] == "v0"]
    )

    def assess(row, case):
        if case["claim"]["location"]:
            row.update(address_assessment=assessment, destination_assessment=destination)
            row["evidence_fields"].append("claim.location")

    material = model_material(intake, observed, decisions=assess, historical=False)
    report = resolve_identities(intake, observed, model_result=material).to_dict()
    visit = next(r for r in report["records"] if r["version"] == "v0")
    assert visit["candidate_correspondence"] == {"decision": "match", "candidate_id": "place-a"}
    assert visit["grounding_verdict"] == "UNKNOWN"
    assert visit["canonical_place_id"] is None
    assert identity_ready(intake.to_dict(), report)


@pytest.mark.parametrize("decision", ["match", "unknown", "no_supported_match"])
def test_supported_destination_conflict_is_fail_without_an_original_address(batch, decision):
    intake = prepared(batch)
    refs = [r for r in identity_references(intake) if r["version"] == "v0"]
    observed = evidence(intake, [search(r, r["name"], address="Other City") for r in refs])

    def conflict(row, _case):
        row.update(decision=decision, destination_assessment="contradictory")
        if decision != "match":
            row.update(
                candidate_id=None,
                evidence_fields=["claim.place_name", "claim.destination", "case.candidates"],
            )

    material = model_material(intake, observed, decisions=conflict, historical=False)
    report = resolve_identities(intake, observed, model_result=material).to_dict()
    visit = next(r for r in report["records"] if r["version"] == "v0")
    assert visit["candidate_correspondence"]["decision"] == decision
    assert visit["model_judgment"]["address_assessment"] == "not_supplied"
    assert visit["grounding_verdict"] == "FAIL"
    assert visit["canonical_place_id"] is None
    assert visit["original_claim"]["location"] is None
    assert identity_ready(intake.to_dict(), report)
    leg = next(
        r
        for r in prepare_routes(intake, report, context(intake)).to_dict()["results"]
        if r["version"] == "v0"
    )["legs"][0]
    assert leg["canonical_endpoints"] == [None, None]
    assert leg["identity_grounding_verdicts"] == ["FAIL", "FAIL"]
    assert leg["expected_context"] is None


@pytest.mark.parametrize("fault", ["original_support", "candidate_support", "empty_candidates"])
def test_destination_failure_requires_original_and_independent_citations(batch, fault):
    intake = prepared(batch)
    refs = [r for r in identity_references(intake) if r["version"] == "v0"]
    observed = evidence(
        intake, [] if fault == "empty_candidates" else [search(r, r["name"]) for r in refs]
    )

    def unsupported(row, _case):
        row.update(decision="unknown", candidate_id=None, destination_assessment="contradictory")
        row["evidence_fields"] = (
            ["case.candidates"]
            if fault == "original_support"
            else ["claim.place_name", "claim.destination"]
        )

    material = model_material(intake, observed, decisions=unsupported, historical=False)
    with pytest.raises(ValueError, match="Destination failure"):
        resolve_identities(intake, observed, model_result=material)
