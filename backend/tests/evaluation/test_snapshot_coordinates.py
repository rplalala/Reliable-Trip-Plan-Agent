"""Independent snapshot coordinates through public route preparation boundaries."""

import asyncio
import copy
import json
import socket

import pytest

from backend.evaluation.identity import identity_references, resolve_identities
from backend.evaluation.intake import load_batch
from backend.evaluation.records import canonical_digest
from backend.evaluation.route_cli import main
from backend.evaluation.routes import prepare_routes, score_routes
from backend.evaluation.snapshot import (
    AcquisitionPolicy,
    Response,
    acquire_snapshot,
    build_identity_plan,
    identity_evidence,
)
from backend.tests.evaluation.test_identity import plan, review_envelope
from backend.tests.evaluation.test_requirement_schedule import context
from backend.tests.evaluation.test_routes import reviews

pytest_plugins = ("backend.tests.evaluation.test_intake",)


@pytest.fixture
def coordinate_case(batch, tmp_path):
    def build(
        change=None,
        duplicate=None,
        supplied_id=False,
        details_change=None,
        paired=False,
        optional_tracks=False,
        malformed_search=False,
    ):
        if optional_tracks:
            itinerary = batch[1]["v3"]["itinerary"]
            batch[1]["v3"]["v3"] = {
                "draft": copy.deepcopy(itinerary),
                "final_primary": copy.deepcopy(itinerary),
            }
            batch[2]("v3")
        if supplied_id:
            batch[1]["v1"]["itinerary"]["days"][0]["activities"][0]["source_place_id"] = (
                "canonical-Museum A"
            )
        intake = load_batch(batch[2]("v1" if supplied_id else None))
        request_plan = build_identity_plan(intake, paired=paired)

        async def transport(request):
            details = request["operation"] == "places_details"
            name = (
                request["parameters"]["place_id"].removeprefix("canonical-")
                if details
                else request["parameters"]["query"]
            )
            candidate = {
                "id": "canonical-" + name,
                "displayName": {"text": name},
                "formattedAddress": "10 Main St, Example City, Country",
                "location": {"latitude": 10 if name == "Museum A" else 11, "longitude": 20},
            }
            if change:
                change(candidate)
            if details and details_change:
                details_change(candidate)
            places = [candidate]
            if malformed_search and name == "Museum A" and not details:
                places = None
            if duplicate is not None and name == "Museum A":
                extra = copy.deepcopy(candidate)
                extra["location"] = duplicate
                places.append(extra)
            return Response(200, json.dumps(candidate if details else {"places": places}).encode())

        directory = tmp_path / "identity-snapshot"
        snapshot = asyncio.run(
            acquire_snapshot(request_plan, directory, transport, AcquisitionPolicy(max_sends=10))
        )
        evidence = identity_evidence(snapshot)
        observed = {r["reference_id"]: r for r in evidence["records"]}
        reviews = {
            "schema_version": "rtpeval_identity_reviews_1",
            "batch_id": "batch",
            "batch_revision": "1",
            "records": [],
        }
        for ref in identity_references(intake):
            observation = observed[ref["reference_id"]]
            if not any(
                observation.get(kind, {}).get("status") == "available"
                for kind in ("search", "details")
            ):
                continue
            reviews["records"].extend(
                review_envelope(
                    intake,
                    observed[ref["reference_id"]],
                    ref["reference_id"],
                    "canonical-" + ref["name"],
                )["records"]
            )
        identity = resolve_identities(intake, evidence, reviews, plan(intake))
        return intake, identity, directory, snapshot

    return build


def test_malformed_search_preserves_usable_details_and_other_places(coordinate_case):
    intake, identity, directory, snapshot = coordinate_case(supplied_id=True, malformed_search=True)
    report = prepare_routes(
        intake, identity, context(intake), identity_snapshot_directory=directory
    ).to_dict()
    assert report["status"] == "complete"
    assert len(report["results"]) == 4
    coordinates = report["coordinate_preparation"]
    assert coordinates["diagnostics"] == []
    assert [point["place_id"] for point in coordinates["records"]] == [
        "canonical-Museum A",
        "canonical-Museum B",
    ]
    assert len(coordinates["records"][0]["observations"]) == 1
    assert coordinates["records"][0]["observations"][0]["pointer"] == "/location"
    assert any(
        row.get("search", {}).get("status") == "malformed"
        for row in identity_evidence(snapshot)["records"]
    )


def test_snapshot_coordinates_remove_duplicate_route_preparation(coordinate_case):
    intake, identity, directory, _ = coordinate_case()
    before = {p: p.read_bytes() for p in directory.rglob("*") if p.is_file()}
    report = prepare_routes(
        intake, identity, context(intake), identity_snapshot_directory=directory
    ).to_dict()
    assert report["status"] == "complete"
    assert len(report["results"]) == 4
    assert len(report["route_contexts"]) == 1
    assert report["route_contexts"][0]["origin"]["latitude"] == 10
    assert report["route_contexts"][0]["destination"]["latitude"] == 11
    assert len(report["coordinate_preparation"]["records"]) == 2
    assert report["coordinate_preparation"]["diagnostics"] == []
    assert {p: p.read_bytes() for p in directory.rglob("*") if p.is_file()} == before


@pytest.mark.parametrize(
    "location",
    [
        None,
        {"latitude": 999, "longitude": 20},
        {"latitude": 10, "longitude": True},
        {"latitude": "10", "longitude": 20},
        {"latitude": 10**400, "longitude": 20},
    ],
)
def test_invalid_coordinates_block_only_the_affected_place(coordinate_case, location):
    def change(candidate):
        if candidate["id"] == "canonical-Museum A":
            candidate["location"] = location

    intake, identity, directory, _ = coordinate_case(change)
    report = prepare_routes(
        intake, identity, context(intake), identity_snapshot_directory=directory
    ).to_dict()
    assert report["status"] == "complete"
    assert len(report["results"]) == 4
    assert report["route_contexts"] == []
    assert [p["place_id"] for p in report["coordinate_preparation"]["records"]] == [
        "canonical-Museum B"
    ]
    assert report["coordinate_preparation"]["diagnostics"][0]["reason"] == "coordinates_invalid"


@pytest.mark.parametrize(
    "duplicate,expected",
    [
        ({"latitude": 10, "longitude": 20}, "complete"),
        ({"latitude": 10.1, "longitude": 20}, "coordinates_conflicting"),
    ],
)
def test_repeated_observations_must_agree_before_coordinate_adoption(
    coordinate_case, duplicate, expected
):
    intake, identity, directory, _ = coordinate_case(duplicate=duplicate)
    report = prepare_routes(
        intake, identity, context(intake), identity_snapshot_directory=directory
    ).to_dict()
    assert report["status"] == "complete"
    if expected == "complete":
        assert len(report["route_contexts"]) == 1
        assert len(report["coordinate_preparation"]["records"][0]["observations"]) == 2
    else:
        assert report["route_contexts"] == []
        assert report["coordinate_preparation"]["diagnostics"][0]["reason"] == expected


def test_cli_uses_snapshot_without_coordinate_file(coordinate_case, capsys):
    intake, identity, directory, _ = coordinate_case()
    root = directory.parent
    (root / "identity.json").write_text(json.dumps(identity.to_dict()), encoding="utf-8")
    (root / "context.json").write_text(json.dumps(context(intake)), encoding="utf-8")
    args = [
        "prepare",
        str(root / "manifest.json"),
        str(root / "identity.json"),
        "--context",
        str(root / "context.json"),
        "--identity-snapshot",
        str(directory),
    ]
    assert main(args) == 0
    report = json.loads(capsys.readouterr().out)
    assert len(report["route_contexts"]) == 1
    assert main(args) == 0
    assert json.loads(capsys.readouterr().out) == report


@pytest.fixture
def scored_coordinate_case(coordinate_case):
    intake, identity, directory, _ = coordinate_case()
    prepared = prepare_routes(
        intake,
        identity,
        context(intake),
        route_reviews=reviews(intake),
        identity_snapshot_directory=directory,
    ).to_dict()

    async def transport(request):
        if request["operation"] == "route_matrix":
            payload = [
                {
                    "originIndex": 0,
                    "destinationIndex": 0,
                    "condition": "ROUTE_EXISTS",
                    "status": {"code": 0},
                    "duration": "1800s",
                    "distanceMeters": 1000,
                }
            ]
        else:
            payload = {"id": request["parameters"]["place_id"]}
        return Response(200, json.dumps(payload).encode())

    evidence_directory = directory.parent / "route-snapshot"
    asyncio.run(
        acquire_snapshot(
            prepared["evidence_plan"],
            evidence_directory,
            transport,
            AcquisitionPolicy(max_sends=10),
        )
    )
    return intake, identity, directory, evidence_directory


def test_route_scoring_replays_the_same_snapshot_coordinate_source(scored_coordinate_case):
    intake, identity, directory, route_directory = scored_coordinate_case
    report = score_routes(
        intake,
        identity,
        route_directory,
        context(intake),
        route_reviews=reviews(intake),
        identity_snapshot_directory=directory,
    ).to_dict()
    assert report["status"] == "complete"
    assert report["results"][0]["routes"]["counts"]["PASS"] == 1
    assert len(report["coordinate_preparation"]["records"]) == 2


def test_quality_report_forwards_the_same_coordinate_source(scored_coordinate_case):
    from backend.evaluation.quality_report import build_quality_report

    intake, identity, directory, route_directory = scored_coordinate_case
    report = build_quality_report(
        intake,
        identity,
        route_directory,
        context(intake),
        route_reviews=reviews(intake),
        identity_snapshot_directory=directory,
        generated_at="2026-10-03T00:00:00Z",
    ).to_dict()
    assert report["status"] == "complete"
    assert report["groups"][0]["versions"]["v0"]["primary_metrics"]["routes"]["counts"]["PASS"] == 1


@pytest.mark.parametrize(
    "fault",
    [
        "raw_hash",
        "foreign_batch",
        "evidence_hash",
        "observation_hash",
        "observation_id",
        "missing_directory",
    ],
)
def test_coordinate_source_corruption_rejects_whole_preparation(coordinate_case, fault):
    intake, identity, directory, snapshot = coordinate_case()
    adopted = identity.to_dict()
    if fault == "raw_hash":
        raw = directory / snapshot["records"][0]["attempts"][-1]["raw"]["path"]
        raw.write_bytes(b"{}")
    elif fault == "foreign_batch":
        snapshot["plan"]["batch_id"] = "foreign"
        snapshot["plan_hash"] = canonical_digest(snapshot["plan"])
        (directory / "manifest.json").write_text(json.dumps(snapshot), encoding="utf-8")
    elif fault == "evidence_hash":
        adopted["evidence_hash"] = "a" * 64
    elif fault == "observation_hash":
        adopted["records"][0]["evidence_hash"] = "a" * 64
    elif fault == "observation_id":
        adopted["records"][0]["observation_id"] = "foreign"
    else:
        directory = directory / "missing"
    report = prepare_routes(
        intake, adopted, context(intake), identity_snapshot_directory=directory
    ).to_dict()
    assert report["status"] == "needs_material_correction"
    assert report["results"] == report["route_contexts"] == []


def test_missing_coordinates_keep_all_route_candidates(coordinate_case):
    intake, identity, directory, _ = coordinate_case(lambda c: c.pop("location"))
    report = prepare_routes(
        intake, identity, context(intake), identity_snapshot_directory=directory
    ).to_dict()
    assert report["status"] == "complete"
    assert len(report["evidence_plan"]["legs"]) == 4
    assert report["route_contexts"] == []
    assert report["coordinate_preparation"]["records"] == []
    assert [d["reason"] for d in report["coordinate_preparation"]["diagnostics"]] == [
        "coordinates_missing"
    ] * 2


def test_search_and_details_conflict_is_local_coordinate_uncertainty(coordinate_case):
    intake, identity, directory, _ = coordinate_case(
        supplied_id=True, details_change=lambda c: c["location"].update(latitude=12)
    )
    report = prepare_routes(
        intake, identity, context(intake), identity_snapshot_directory=directory
    ).to_dict()
    assert report["status"] == "complete"
    assert report["route_contexts"] == []
    assert report["coordinate_preparation"]["diagnostics"][0]["reason"] == "coordinates_conflicting"


def test_paired_snapshot_provenance_and_truthful_sources(coordinate_case):
    from backend.evaluation.snapshot_coordinates import prepare_snapshot_coordinates

    intake, identity, directory, snapshot = coordinate_case(
        supplied_id=True, paired=True, optional_tracks=True
    )
    prepared = prepare_snapshot_coordinates(intake, identity, directory).to_dict()
    assert prepared["status"] == "complete"
    assert len(prepared["records"]) == 2
    point = prepared["records"][0]
    assert len(point["observations"]) == 2
    assert "reviewer_ref" not in point and "reviewed_at" not in point
    assert point["source_kind"] == "independent_snapshot"
    hashes = {r["attempts"][-1]["raw"]["sha256"] for r in snapshot["records"]}
    assert all(
        o["raw_sha256"] in hashes and o["pointer"].endswith("/location")
        for o in point["observations"]
    )


def test_adopted_id_without_coordinate_source_does_not_fall_back_to_name(coordinate_case):
    intake, identity, directory, _ = coordinate_case()
    adopted = identity.to_dict()
    record = next(
        r
        for r in adopted["records"]
        if r["version"] == "v0" and r["canonical_place_id"] == "canonical-Museum A"
    )
    record["canonical_place_id"] = "canonical-reviewed-other-place"
    report = prepare_routes(
        intake, adopted, context(intake), identity_snapshot_directory=directory
    ).to_dict()
    assert report["status"] == "complete"
    assert report["route_contexts"] == []
    assert {
        "place_id": "canonical-reviewed-other-place",
        "reason": "coordinates_missing",
    } in report["coordinate_preparation"]["diagnostics"]


def test_coordinate_replay_is_deterministic_without_socket_access(
    scored_coordinate_case, monkeypatch
):
    intake, identity, directory, route_directory = scored_coordinate_case
    before = {p: p.read_bytes() for p in directory.parent.rglob("*") if p.is_file()}

    def forbidden(*_args, **_kwargs):
        raise AssertionError("Coordinate replay must not access network")

    monkeypatch.setattr(socket, "socket", forbidden)
    report = score_routes(
        intake,
        identity,
        route_directory,
        context(intake),
        route_reviews=reviews(intake),
        identity_snapshot_directory=directory,
    ).to_dict()
    assert report["status"] == "complete"
    assert (
        score_routes(
            intake,
            identity,
            route_directory,
            context(intake),
            route_reviews=reviews(intake),
            identity_snapshot_directory=directory,
        ).to_dict()
        == report
    )
    assert {p: p.read_bytes() for p in directory.parent.rglob("*") if p.is_file()} == before


def test_snapshot_and_reviewed_coordinates_cannot_compete(coordinate_case):
    from backend.tests.evaluation.test_routes import coordinates

    intake, identity, directory, _ = coordinate_case()
    report = prepare_routes(
        intake,
        identity,
        coordinate_evidence=coordinates(identity),
        identity_snapshot_directory=directory,
    ).to_dict()
    assert report["status"] == "needs_material_correction"
    assert report["results"] == []


def test_unresolved_identity_is_not_repaired_by_coordinates(coordinate_case):
    intake, identity, directory, _ = coordinate_case()
    adopted = identity.to_dict()
    record = next(
        r
        for r in adopted["records"]
        if r["version"] == "v0" and r["canonical_place_id"] == "canonical-Museum A"
    )
    record.update(resolution="unresolved", canonical_place_id=None)
    report = prepare_routes(
        intake, adopted, context(intake), identity_snapshot_directory=directory
    ).to_dict()
    assert report["status"] == "complete"
    assert report["route_contexts"] == []
    assert "identity_unresolved" in report["results"][0]["legs"][0]["reasons"]


def test_quality_cli_uses_automatic_coordinates(scored_coordinate_case, capsys):
    from backend.evaluation.quality_report_cli import main as quality_main

    intake, identity, directory, route_directory = scored_coordinate_case
    root = directory.parent
    for name, value in (
        ("identity", identity.to_dict()),
        ("context", context(intake)),
        ("reviews", reviews(intake)),
    ):
        (root / (name + ".json")).write_text(json.dumps(value), encoding="utf-8")
    args = [
        str(root / "manifest.json"),
        str(root / "identity.json"),
        str(route_directory),
        "--context",
        str(root / "context.json"),
        "--route-reviews",
        str(root / "reviews.json"),
        "--identity-snapshot",
        str(directory),
        "--generated-at",
        "2026-10-03T00:00:00Z",
    ]
    assert quality_main(args) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["groups"][0]["versions"]["v0"]["primary_metrics"]["routes"]["counts"]["PASS"] == 1
