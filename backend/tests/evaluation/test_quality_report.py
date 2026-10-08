"""Quality aggregation through real frozen, synthetic evidence boundaries."""

import asyncio
import copy
import json

import pytest

from backend.evaluation.identity import identity_references
from backend.evaluation.identity_llm import resolve_llm_identities as resolve_identities
from backend.evaluation.quality_report import build_quality_report
from backend.evaluation.records import canonical_digest
from backend.evaluation.routes import prepare_routes
from backend.evaluation.snapshot import (
    AcquisitionPolicy,
    Response,
    acquire_snapshot,
    build_evidence_plan,
    load_snapshot,
)
from backend.tests.evaluation import test_requirement_schedule as schedule_tests
from backend.tests.evaluation import test_routes as route_tests
from backend.tests.evaluation.test_daily_density import density_reviews
from backend.tests.evaluation.test_identity import evidence, search
from backend.tests.evaluation.test_identity_llm import model_material
from backend.tests.evaluation.test_intake import activity

pytest_plugins = ("backend.tests.evaluation.test_intake",)
prepared_scenario = route_tests.prepared_scenario
route_case = route_tests.route_case
STAMP = "2026-10-02T00:00:00Z"


def report(case, **kwargs):
    intake, identity, directory, context, reviews, coordinates, plan = case
    return build_quality_report(
        intake,
        identity,
        directory,
        context,
        route_reviews=reviews,
        coordinate_evidence=coordinates,
        expected_plan=plan,
        generated_at=STAMP,
        **kwargs,
    ).to_dict()


def replay_evidence(case, *, identity=None, payload=None):
    """Acquire another synthetic snapshot through the public transport seam."""
    intake, original_identity, directory, context, reviews, coordinates, _ = case
    identity = original_identity if identity is None else identity
    prepared = prepare_routes(
        intake, identity, context, route_reviews=reviews, coordinate_evidence=coordinates
    ).to_dict()
    plan = build_evidence_plan(intake, identity, prepared["route_contexts"])
    old = {
        r["key"]: (directory / r["attempts"][-1]["raw"]["path"]).read_bytes()
        for r in load_snapshot(directory)["records"]
        if r["attempts"]
    }

    async def transport(request):
        body = json.dumps(payload(request)).encode() if payload else old[request["key"]]
        return Response(200, body)

    target = directory.parent / (directory.name + "-replayed")
    asyncio.run(
        acquire_snapshot(
            plan, target, transport, AcquisitionPolicy(max_sends=len(plan["requests"]) or 1)
        )
    )
    return intake, identity, target, context, reviews, coordinates, plan


def test_verified_scores_use_known_units_and_one_common_mask(route_case):
    out = report(route_case())
    assert out["status"] == "complete", out["diagnostics"]
    group = out["groups"][0]
    assert group["included_dimensions"] == ["grounding", "non_overlap", "opening", "routes"]
    versions = group["versions"]
    dimensions = versions["v1"]["dimensions"]
    assert dimensions["grounding"]["counts"] == {"PASS": 2, "FAIL": 0, "UNKNOWN": 0}
    assert dimensions["non_overlap"]["denominator"] == 3
    assert dimensions["opening"]["counts"] == {"PASS": 0, "FAIL": 0, "UNKNOWN": 2}
    assert dimensions["opening"]["verified_score_0_100"] == 0
    assert dimensions["opening"]["conditional_compliance"] is None
    assert dimensions["routes"]["denominator"] == 1
    assert dimensions["non_overlap"]["counts"] == {"PASS": 0, "FAIL": 0, "UNKNOWN": 3}
    assert versions["v1"]["auxiliary_total"]["score_0_100"] == 50
    assert versions["v1"]["auxiliary_total"]["exact_fraction"] == {"numerator": 1, "denominator": 2}
    assert versions["v0"]["auxiliary_total"]["score_0_100"] == 50
    assert versions["v1"]["primary_metrics"]["routes"]["checks"][0]["state"] == "PASS"


def test_final_report_deducts_daily_penalty_without_replacing_verified_metrics(route_case):
    case = route_case()
    prepared = case[0].to_dict()
    group = prepared["inventory"][0]
    reviews = {
        "schema_version": "rtpeval_density_reviews_1",
        "batch_id": prepared["batch_id"],
        "batch_revision": prepared["revision"],
        "groups": [
            {
                "group_id": group["group_id"],
                "input_sha256": group["input_sha256"],
                "reviewer_ref": "independent-reviewer",
                "reviewed_at": STAMP,
                "review_origin": "agent",
                "rationale": "Architecture preference implies no count.",
                "default": {
                    "profile": "ordinary",
                    "exact_count": None,
                    "source_refs": [
                        {
                            "field_path": "additional_preferences",
                            "quote": "Prefer architecture",
                        }
                    ],
                },
                "days": [],
            }
        ],
    }
    out = report(case, density_reviews=reviews)
    assert out["status"] == "complete", out["diagnostics"]
    v1 = out["groups"][0]["versions"]["v1"]
    assert v1["daily_density"]["mean_penalty_0_100"] == 0
    assert v1["overall_total"]["score_0_100"] == 50
    assert v1["auxiliary_total"]["score_0_100"] == 50
    assert out["source_hashes"]["preparation"]["density_reviews"] == canonical_digest(reviews)
    missing = report(case)["groups"][0]["versions"]["v1"]
    assert missing["overall_total"]["score_0_100"] is None
    assert missing["overall_total"]["reason"] == "density_penalty_unresolved"


def test_known_unknown_identity_has_no_fabrication_penalty(route_case):
    group = report(route_case(unresolved_names=["Museum A", "Museum B"]))["groups"][0]
    for version in group["versions"].values():
        dim = version["dimensions"]["grounding"]
        assert dim["counts"] == {"PASS": 0, "FAIL": 0, "UNKNOWN": 2}
        assert dim["denominator"] == 2
        assert dim["rates"]["unknown_rate"] == 1
        assert dim["verified_score_0_100"] == 0


def test_legacy_metadata_cannot_supply_a_new_grounding_verdict(route_case):
    case = route_case()
    historical = case[1]
    legacy = historical.to_dict()
    for row in legacy["records"]:
        row["grounding_verdict"] = "FAIL"
    out = report(replay_evidence(case, identity=legacy))
    assert out["status"] == "complete", out["diagnostics"]
    for version in out["groups"][0]["versions"].values():
        assert version["dimensions"]["grounding"]["counts"] == {"PASS": 2, "FAIL": 0, "UNKNOWN": 0}


@pytest.mark.parametrize("version", ["v0", "v1", "v2", "v3"])
@pytest.mark.parametrize("assessment", ["incorrect_claim", "different_place", "unknown"])
def test_address_errors_are_failures_without_repairing_any_version(route_case, version, assessment):
    def change(results):
        route_tests.no_departure(results)
        results[version]["itinerary"]["days"][0]["activities"][0]["location"] = "Wrong address"

    case = route_case(change=change)
    intake = case[0]
    original = copy.deepcopy(intake.to_dict())
    observed = evidence(
        intake,
        [
            search(r, r["name"], place_id="canonical-" + r["name"])
            for r in identity_references(intake)
        ],
    )

    def choose(row, selected):
        if selected["claim"]["location"]:
            row["address_assessment"] = assessment
            row["evidence_fields"].append("claim.location")

    identity = resolve_identities(
        intake, observed, model_result=model_material(intake, observed, decisions=choose)
    ).to_dict()
    assert identity["status"] == ("needs_model_judgment" if assessment == "unknown" else "complete")
    assert len(identity["judgment_queue"]) == (1 if assessment == "unknown" else 0)
    accepted = replay_evidence(case, identity=identity)
    out = report(accepted)
    assert out["status"] == "complete", out["diagnostics"]
    versions = out["groups"][0]["versions"]
    expected = {"PASS": 1, "FAIL": 1, "UNKNOWN": 0}
    if assessment == "unknown":
        expected = {"PASS": 1, "FAIL": 0, "UNKNOWN": 1}
    assert versions[version]["dimensions"]["grounding"]["counts"] == expected
    assert versions[version]["dimensions"]["grounding"]["denominator"] == 2
    assert versions[version]["dimensions"]["routes"]["counts"] == {
        "PASS": 0,
        "FAIL": 0,
        "UNKNOWN": 1,
    }
    for other in {"v0", "v1", "v2", "v3"} - {version}:
        assert versions[other]["dimensions"]["grounding"]["counts"] == {
            "PASS": 2,
            "FAIL": 0,
            "UNKNOWN": 0,
        }
    assert intake.to_dict() == original


def test_single_version_no_checks_keeps_raw_na_and_zero_contribution(route_case):
    def change(results):
        route_tests.no_departure(results)
        results["v0"]["itinerary"]["days"][0]["activities"] = results["v0"]["itinerary"]["days"][0][
            "activities"
        ][:1]

    group = report(route_case(change=change))["groups"][0]
    dimension = group["versions"]["v0"]["dimensions"]["routes"]
    assert "routes" in group["included_dimensions"]
    assert dimension["state"] == "N/A"
    assert dimension["denominator"] == 0
    assert dimension["verified_score_0_100"] is None
    assert dimension["rates"]["unknown_rate"] is None
    assert dimension["counts"] == {"PASS": 0, "FAIL": 0, "UNKNOWN": 0}
    assert dimension["contribution"] == {
        "score_0_100": 0,
        "exact_fraction": {"numerator": 0, "denominator": 1},
        "reason": "no_checks",
    }
    assert group["versions"]["v0"]["auxiliary_total"]["score_0_100"] == 50


def test_genuinely_unknown_role_keeps_unknown_population_and_asymmetric_totals(route_case):
    def change(results):
        route_tests.no_departure(results)
        first = results["v0"]["itinerary"]["days"][0]["activities"][0]
        first.update(activity_kind="unknown", place_name=None, title="Unclassified experience")

    out = report(route_case(change=change))
    assert out["status"] == "complete"
    group = out["groups"][0]
    v0 = group["versions"]["v0"]
    assert v0["primary_metrics"]["grounding"]["unresolved_role_count"] == 1
    dim = v0["dimensions"]["grounding"]
    assert dim["counts"] == {"PASS": 1, "FAIL": 0, "UNKNOWN": 0}
    assert dim["denominator"] is None
    assert all(rate is None for rate in dim["rates"].values())
    assert dim["contribution"]["score_0_100"] is None
    assert v0["auxiliary_total"]["reason"] == "denominator_unresolved"
    assert v0["auxiliary_total"]["score_0_100"] is None
    assert group["versions"]["v1"]["auxiliary_total"]["score_0_100"] == 50
    assert not group["all_totals_available"]
    assert group["included_dimensions"] == ["grounding", "non_overlap", "opening", "routes"]


@pytest.mark.parametrize(
    "title", ["Walk to Museum A", "Walk to Museum A and explore its exhibitions"]
)
def test_title_wording_does_not_make_declared_visit_counts_unknown(route_case, title):
    def change(results):
        route_tests.no_departure(results)
        for result in results.values():
            result["itinerary"]["days"][0]["activities"][0]["title"] = title

    case = route_case(change=change)
    out = report(case, density_reviews=density_reviews(case[0]))
    assert out["status"] == "complete", out["diagnostics"]
    for version in out["groups"][0]["versions"].values():
        assert version["primary_metrics"]["grounding"]["unresolved_role_count"] == 0
        assert version["dimensions"]["grounding"]["denominator"] == 2
        day = version["daily_density"]["days"][0]
        assert day["known_primary_count"] == 2
        assert day["possible_primary_count"] == 0
        assert day["penalty_0_100"] == 0
        assert version["overall_total"]["score_0_100"] is not None


@pytest.mark.parametrize("title", ["Coffee break", "Relax over a drink", "Rest"])
@pytest.mark.parametrize("place", [None, "Hotel Lounge"])
def test_declared_free_time_never_becomes_a_possible_poi(route_case, title, place):
    def change(results):
        route_tests.no_departure(results)
        for result in results.values():
            result["itinerary"]["days"][0]["activities"].append(
                activity("break", title, "10:00", "10:20", "free_time", place=place)
            )

    case = route_case(change=change)
    out = report(case, density_reviews=density_reviews(case[0]))
    assert out["status"] == "complete", out["diagnostics"]
    for version in out["groups"][0]["versions"].values():
        assert version["primary_metrics"]["grounding"]["unresolved_role_count"] == 0
        assert version["dimensions"]["grounding"]["denominator"] == 2
        day = version["daily_density"]["days"][0]
        assert day["known_primary_count"] == 2
        assert day["possible_primary_count"] == 0
        assert day["penalty_0_100"] == 0


@pytest.mark.parametrize("notes", ["Estimated travel time", "Bring water if it is sunny"])
def test_v0_report_scores_are_invariant_under_unrelated_transport_notes(route_case, notes):
    def change(note):
        def apply(results):
            route_tests.no_departure(results)
            travel = activity("travel", "Walking", "10:00", "10:30", "transport")
            travel["notes"] = note
            results["v0"]["itinerary"]["days"][0]["activities"].append(travel)

        return apply

    baseline = report(route_case(change=change("Model estimate")))
    revised = report(route_case(change=change(notes)))
    assert baseline["status"] == revised["status"] == "complete"
    old = baseline["groups"][0]["versions"]["v0"]
    new = revised["groups"][0]["versions"]["v0"]
    for name in ("grounding", "non_overlap", "opening", "routes"):
        assert new["dimensions"][name]["counts"] == old["dimensions"][name]["counts"]
        assert new["dimensions"][name]["denominator"] == old["dimensions"][name]["denominator"]
    assert new["auxiliary_total"] == old["auxiliary_total"]


@pytest.mark.parametrize(
    "mode,pair,known",
    [
        ("WALK", ("a", "b"), True),
        (None, ("a", "b"), False),
        ("WALK", ("b", "a"), False),
    ],
)
def test_structured_transport_report_preserves_independent_uncertainties(
    route_case, mode, pair, known
):
    def change(results):
        route_tests.no_departure(results)
        travel = activity("travel", "Journey between visits", "10:00", "10:30", "transport")
        travel["notes"] = "Walking from Museum A to Museum B"
        travel["transport"] = {"mode": mode, "from_activity_id": pair[0], "to_activity_id": pair[1]}
        results["v0"]["itinerary"]["days"][0]["activities"].append(travel)

    case = route_case(change=change)
    before = copy.deepcopy(case[0].to_dict())
    reviews = density_reviews(case[0])
    out = report(case, density_reviews=reviews)
    assert out["status"] == "complete", out["diagnostics"]
    version = out["groups"][0]["versions"]["v0"]
    dimension = version["dimensions"]["non_overlap"]
    if known:
        assert dimension["denominator"] == 3
        assert dimension["counts"] == {"PASS": 3, "FAIL": 0, "UNKNOWN": 0}
        assert version["primary_metrics"]["routes"]["checks"][0]["state"] == "PASS"
    elif pair == ("a", "b"):
        assert dimension["denominator"] == 3
        assert dimension["counts"] == {"PASS": 3, "FAIL": 0, "UNKNOWN": 0}
        assert version["primary_metrics"]["routes"]["checks"][0]["state"] == "UNKNOWN"
    else:
        assert dimension["denominator"] == 3
        assert dimension["counts"] == {"PASS": 3, "FAIL": 0, "UNKNOWN": 0}
        assert version["primary_metrics"]["routes"]["checks"][0]["state"] == "UNKNOWN"
    assert version["dimensions"]["grounding"]["denominator"] == 2
    assert version["dimensions"]["opening"]["counts"]["UNKNOWN"] == 2
    assert version["daily_density"]["days"][0]["known_primary_count"] == 2
    assert version["daily_density"]["mean_penalty_0_100"] == 0
    assert case[0].to_dict() == before
    assert report(case, density_reviews=reviews) == out


def test_empty_mask_is_unavailable_instead_of_invented_perfect_score(route_case):
    def change(results):
        for result in results.values():
            result["itinerary"]["days"][0]["activities"] = []

    out = report(route_case(change=change))
    assert out["status"] == "complete", out["diagnostics"]
    group = out["groups"][0]
    assert group["included_dimensions"] == []
    for version in group["versions"].values():
        assert version["auxiliary_total"]["score_0_100"] is None
        assert version["auxiliary_total"]["reason"] == "no_scorable_dimensions"


def test_parent_obligations_and_exact_rates_are_not_component_weights(route_case):
    obligations = [
        schedule_tests.required(mode="minimum"),
        schedule_tests.required(mode="minimum", obligation_id="fail", count=2),
        {
            "obligation_id": "unknown",
            "kind": "fixed_visit_time",
            "resolution": "unresolved",
            "source_refs": schedule_tests.SOURCE,
            "reason": "Clock awaits independent review",
        },
    ]
    version = report(route_case(obligations=obligations))["groups"][0]["versions"]["v1"]
    dimension = version["dimensions"]["requirements"]
    assert dimension["counts"] == {"PASS": 1, "FAIL": 1, "UNKNOWN": 1}
    assert dimension["denominator"] == 3
    assert dimension["rates"] == {
        "verified_fraction": 1 / 3,
        "verification_coverage": 2 / 3,
        "unknown_rate": 1 / 3,
        "confirmed_violation_rate": 1 / 3,
    }
    assert dimension["conditional_compliance"] == 0.5
    assert dimension["exact_fractions"]["verified_fraction"] == {"numerator": 1, "denominator": 3}
    assert version["auxiliary_total"]["exact_fraction"] == {"numerator": 7, "denominator": 15}
    assert version["auxiliary_total"]["score_0_100"] == float(140 / 3)


def test_identity_summary_is_not_a_metric_input_and_content_hash_excludes_time(route_case):
    case = list(route_case())
    first = report(case)
    case[1] = case[1].to_dict()
    case[1]["groups"] = [{"forged_verified_score": 100}]
    second = report(case)
    assert second["groups"] == []
    assert second["status"] == "needs_material_correction"
    replayed = replay_evidence(case, identity=case[1])
    corrected = report(replayed)
    assert corrected["status"] == "complete", corrected["diagnostics"]
    for version in ("v0", "v1", "v2", "v3"):
        assert (
            corrected["groups"][0]["versions"][version]["dimensions"]
            == first["groups"][0]["versions"][version]["dimensions"]
        )
    original = build_quality_report(
        replayed[0],
        replayed[1],
        replayed[2],
        replayed[3],
        route_reviews=replayed[4],
        coordinate_evidence=replayed[5],
        expected_plan=replayed[6],
        generated_at="2026-10-03T00:00:00Z",
    ).to_dict()
    assert original["content_hash"] == corrected["content_hash"]
    assert first["stage_availability"]["resource"] == {"report_status": "not_integrated"}
    assert all(not r["usage_available"] for r in first["stage_availability"]["source_runs"])


@pytest.mark.parametrize(
    "fault", ["identity", "context", "coordinates", "expected_plan", "snapshot", "paired"]
)
def test_invalid_material_preserves_no_partial_cohort(route_case, fault):
    case = list(route_case(paired=fault == "paired"))
    if fault == "identity":
        case[1] = case[1].to_dict()
        case[1].pop("subject_scope_version")
    elif fault == "context":
        case[3]["groups"][0]["input_sha256"] = "b" * 64
    elif fault == "coordinates":
        case[5]["records"][0]["evidence_sha256"] = "invalid"
    elif fault == "expected_plan":
        case[6] = copy.deepcopy(case[6])
        case[6]["batch_revision"] = "stale"
    elif fault == "snapshot":
        path = case[2] / "manifest.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["plan_hash"] = "b" * 64
        path.write_text(json.dumps(data), encoding="utf-8")
    out = report(case)
    assert out["status"] == (
        "identity_replay_required" if fault == "identity" else "needs_material_correction"
    )
    assert out["groups"] == []
    assert out["diagnostics"]
    if fault == "paired":
        assert out["diagnostics"][0]["reason"] == "unsupported_snapshot_scope"


def test_findings_only_change_preserves_scores_after_relinking_and_rejects_stale_evidence(
    route_case,
):
    first_case = route_case()
    first = report(first_case)

    def change(results):
        route_tests.no_departure(results)
        results["v3"]["validation"] = {
            "findings": [{"state": "FAIL", "message": "Internal planner diagnosis"}]
        }

    next_case = list(route_case(change=change))
    second = report(next_case)
    assert first["status"] == second["status"] == "complete"
    for version in ("v0", "v1", "v2", "v3"):
        a, b = first["groups"][0]["versions"][version], second["groups"][0]["versions"][version]
        assert a["dimensions"] == b["dimensions"]
        assert a["auxiliary_total"] == b["auxiliary_total"]
    assert first["source_hashes"]["artifacts"] != second["source_hashes"]["artifacts"]
    assert first["content_hash"] != second["content_hash"]
    old_identity = next_case.copy()
    old_identity[1] = first_case[1]
    assert report(old_identity)["status"] == "identity_replay_required"
    next_case[2], next_case[6] = first_case[2], first_case[6]
    assert report(next_case)["groups"] == []


def test_result_is_immutable_and_source_digests_preserve_producer_provenance(route_case):
    case = route_case()
    out = report(case)
    assert out["source_hashes"]["intake"] == canonical_digest(case[0].to_dict())
    assert (
        out["source_hashes"]["snapshot_plan"]
        == out["components"]["routes"]["source_hashes"]["snapshot_plan"]
    )
    result = build_quality_report(
        case[0],
        case[1],
        case[2],
        case[3],
        route_reviews=case[4],
        coordinate_evidence=case[5],
        generated_at=STAMP,
    )
    with pytest.raises(TypeError):
        result.data["groups"][0]["versions"]["v1"]["dimensions"]["grounding"]["counts"]["PASS"] = 0


def test_requirement_population_unknown_keeps_dimension_in_mask(
    prepared_scenario, tmp_path, monkeypatch
):
    intake, identity, _ = prepared_scenario(
        unresolved=[
            {
                "item_id": "unclear",
                "source_refs": schedule_tests.SOURCE,
                "reason": "Unclear hard applicability",
            }
        ]
    )
    context = schedule_tests.context(intake)
    reviews, coordinates = route_tests.reviews(intake), route_tests.coordinates(identity)
    prepared = prepare_routes(
        intake, identity, context, route_reviews=reviews, coordinate_evidence=coordinates
    ).to_dict()
    plan = build_evidence_plan(intake, identity, prepared["route_contexts"])
    monkeypatch.setattr("backend.evaluation.snapshot._now", lambda: "2019-12-01T00:00:00Z")

    async def transport(request):
        body = (
            []
            if request["operation"] == "route_matrix"
            else {"id": request["parameters"]["place_id"]}
        )
        return Response(200, json.dumps(body).encode())

    directory = tmp_path / "unclassified"
    asyncio.run(
        acquire_snapshot(
            plan, directory, transport, AcquisitionPolicy(max_sends=len(plan["requests"]) or 1)
        )
    )
    out = report((intake, identity, directory, context, reviews, coordinates, plan))
    assert out["status"] == "complete", out["diagnostics"]
    group = out["groups"][0]
    assert group["included_dimensions"] == list(
        ("requirements", "grounding", "non_overlap", "opening", "routes")
    )
    for version in group["versions"].values():
        dimension = version["dimensions"]["requirements"]
        assert dimension["known_unit_count"] == 0
        assert dimension["denominator"] is None
        assert dimension["contribution"]["score_0_100"] is None
        assert version["auxiliary_total"]["score_0_100"] is None


def test_mixed_opening_keeps_fail_and_unknown_separate(route_case):
    case = route_case()

    def payload(request):
        if request["operation"] == "route_matrix":
            return [
                {
                    "originIndex": 0,
                    "destinationIndex": 0,
                    "status": {},
                    "condition": "ROUTE_EXISTS",
                    "duration": "1800s",
                    "distanceMeters": 2500,
                }
            ]
        pid = request["parameters"]["place_id"]
        return {
            "id": pid,
            **(
                {"timeZone": {"id": "Etc/UTC"}, "regularOpeningHours": {"periods": []}}
                if pid.endswith("Museum A")
                else {}
            ),
        }

    out = report(replay_evidence(case, payload=payload))
    assert out["status"] == "complete", out["diagnostics"]
    version = out["groups"][0]["versions"]["v1"]
    dimension = version["dimensions"]["opening"]
    assert dimension["counts"] == {"PASS": 0, "FAIL": 1, "UNKNOWN": 1}
    assert dimension["state"] == "FAIL"
    assert dimension["rates"]["confirmed_violation_rate"] == 0.5
    assert dimension["rates"]["unknown_rate"] == 0.5
    assert version["primary_metrics"]["opening"]["duration_subtotals"]


def test_combined_route_fail_is_one_unit_and_missing_duration_stays_null(route_case):
    out = report(route_case({"status": {}, "condition": "ROUTE_NOT_FOUND"}))
    assert out["status"] == "complete"
    version = out["groups"][0]["versions"]["v1"]
    dimension = version["dimensions"]["routes"]
    assert dimension["counts"] == {"PASS": 0, "FAIL": 1, "UNKNOWN": 0}
    assert dimension["denominator"] == 1
    assert version["primary_metrics"]["routes"]["checks"][0]["duration_nanoseconds"] is None
    assert (
        version["primary_metrics"]["routes"]["observed_transfer_burden"]["duration_seconds_exact"]
        is None
    )


def test_common_same_venue_na_excludes_route_weight(route_case):
    def change(results):
        route_tests.no_departure(results)
        for result in results.values():
            result["itinerary"]["days"][0]["activities"][-1].update(
                title="Museum A", place_name="Museum A"
            )

    group = report(route_case(change=change))["groups"][0]
    assert group["included_dimensions"] == ["grounding", "non_overlap", "opening"]
    for version in group["versions"].values():
        assert version["dimensions"]["routes"]["not_applicable_count"] == 1
        assert (
            version["dimensions"]["routes"]["contribution"]["reason"] == "excluded_common_no_checks"
        )
        assert version["descriptive"]["repetition"]["extra_occurrences"] == 1


def test_thirds_are_averaged_as_unrounded_rationals(route_case):
    def change(results):
        route_tests.no_departure(results)
        for result in results.values():
            result["itinerary"]["days"][0]["activities"].append(
                activity("c", "Museum C", "12:00", "13:00", place="Museum C")
            )

    version = report(route_case(change=change, unresolved_names=["Museum C"]))["groups"][0][
        "versions"
    ]["v0"]
    assert version["dimensions"]["grounding"]["exact_fractions"]["verified_fraction"] == {
        "numerator": 2,
        "denominator": 3,
    }
    assert version["auxiliary_total"]["exact_fraction"] == {"numerator": 5, "denominator": 12}


@pytest.mark.parametrize("stamp", [None, "not-time", "2026-10-02T00:00:00"])
def test_pure_boundary_requires_explicit_aware_timestamp(route_case, stamp):
    case = route_case()
    out = build_quality_report(case[0], case[1], case[2], generated_at=stamp).to_dict()
    assert out["status"] == "needs_material_correction"
    assert out["groups"] == []


def test_usage_collection_availability_has_no_quality_contribution(route_case, batch):
    first = report(route_case())
    _, _, _, _, root = batch
    for version in ("v0", "v1", "v2", "v3"):
        path = root / (version + "-usage.json")
        data = json.loads(path.read_text(encoding="utf-8"))
        data["collection_status"] = "partial"
        path.write_text(json.dumps(data), encoding="utf-8")
    second = report(route_case())
    assert first["groups"][0]["included_dimensions"] == second["groups"][0]["included_dimensions"]
    for version in ("v0", "v1", "v2", "v3"):
        a, b = first["groups"][0]["versions"][version], second["groups"][0]["versions"][version]
        assert a["dimensions"] == b["dimensions"]
        assert a["auxiliary_total"] == b["auxiliary_total"]
    assert all(r["usage_available"] for r in second["stage_availability"]["source_runs"])
    assert second["stage_availability"]["resource"]["report_status"] == "not_integrated"
    assert first["content_hash"] != second["content_hash"]


def test_partial_opening_failure_retains_completeness_and_exact_magnitudes(route_case):
    def change(results):
        route_tests.no_departure(results)
        for result in results.values():
            item = result["itinerary"]["days"][0]["activities"][0]
            item.update(start_time="2020-01-01T23:00Z", end_time="2020-01-02T01:00Z")

    case = route_case(change=change, requested="2019-12-26T12:00Z")

    def payload(request):
        return {
            "id": request["parameters"]["place_id"],
            "timeZone": {"id": "Etc/UTC"},
            "currentOpeningHours": {"periods": []},
        }

    out = report(replay_evidence(case, payload=payload))
    assert out["status"] == "complete", out["diagnostics"]
    raw = out["groups"][0]["versions"]["v1"]["primary_metrics"]["opening"]
    check = raw["checks"][0]
    assert check["state"] == "FAIL"
    assert check["evidence_status"] == "partial"
    assert check["confirmed_outside_lower_bound_seconds"] == 3600
    assert check["unknown_seconds"] == 3600
    assert raw["counts"]["FAIL"] == 2
    assert raw["complete_evidence_count"] == 1


def test_multiple_requests_keep_separate_masks_and_four_complete_versions(route_case, batch):
    manifest, results, _, save, root = batch
    second = copy.deepcopy(manifest["groups"][0])
    second["group_id"] = "empty-request"
    spec = json.loads((root / "requirements.json").read_text(encoding="utf-8"))
    spec.update(group_id="empty-request", spec_id="empty-spec")
    second["requirement_spec_ref"] = save("empty-requirements.json", spec, spec["schema_version"])
    for version, run in second["selected_runs"].items():
        result = copy.deepcopy(results[version])
        result["itinerary"]["days"][0]["activities"] = []
        run["run_id"] = "empty-" + version
        run["result_ref"] = save("empty-" + version + ".json", result)
        for kind in ("usage", "provenance"):
            data = json.loads((root / (version + "-" + kind + ".json")).read_text(encoding="utf-8"))
            data.update(
                group_id="empty-request",
                run_id=run["run_id"],
                result_sha256=run["result_ref"]["sha256"],
            )
            run[kind + "_ref"] = save(
                "empty-" + version + "-" + kind + ".json", data, data["schema_version"]
            )
    manifest["groups"].append(second)
    manifest["selected_group_ids"].append("empty-request")
    out = report(route_case())
    assert out["status"] == "complete", out["diagnostics"]
    groups = {group["group_id"]: group for group in out["groups"]}
    assert set(groups) == {"g", "empty-request"}
    assert len(groups["g"]["included_dimensions"]) == 4
    assert groups["empty-request"]["included_dimensions"] == []
    assert groups["empty-request"]["diagnostics"][0]["reason"] == "no_scorable_dimensions"
    for group in groups.values():
        assert set(group["versions"]) == {"v0", "v1", "v2", "v3"}
