"""Route preparation/scoring through local public boundaries; synthetic evidence only."""

import asyncio
import copy
import json

import pytest

from backend.evaluation.routes import prepare_routes, score_routes
from backend.evaluation.snapshot import (
    AcquisitionPolicy,
    Response,
    acquire_snapshot,
    build_evidence_plan,
)
from backend.tests.evaluation import test_requirement_schedule as schedule_tests

pytest_plugins = ("backend.tests.evaluation.test_intake",)
prepared_scenario = schedule_tests.scenario


def reviews(intake, **fields):
    group = intake.to_dict()["inventory"][0]
    return {
        "schema_version": "rtpeval_route_reviews_1",
        "batch_id": "batch",
        "revision": "1",
        "groups": [
            {
                "group_id": "g",
                "input_sha256": group["input_sha256"],
                "reviewer_ref": "independent-reviewer",
                "reviewed_at": "2026-10-02T00:00:00Z",
                "status": "unrestricted",
                **fields,
            }
        ],
    }


def protection(start="10:10", end="10:20", scope="scheduled_commitments"):
    return {
        "obligation_id": "rest",
        "kind": "protected_time",
        "resolution": "resolved",
        "date": "2020-01-01",
        "interval": {"kind": "clock", "start": start, "end": end},
        "scope": scope,
        "source_refs": schedule_tests.SOURCE,
    }


def no_departure(results):
    for version, result in results.items():
        day = result["itinerary"]["days"][0]
        day["activities"] = [a for a in day["activities"] if a["activity_kind"] != "transport"]
        day["activities"][-1]["start_time"] = "2020-01-01T11:00:00Z"
        if version != "v0":
            result["itinerary"]["transfers"] = [
                {
                    "from_activity_id": "a",
                    "to_activity_id": "b",
                    "mode": "WALK",
                }
            ]


def test_unstated_departure_waits_for_longest_continuous_fragment(prepared_scenario):
    intake, identity, _ = prepared_scenario([protection()], change=no_departure)
    before = copy.deepcopy(intake.to_dict())
    report = prepare_routes(
        intake, identity, schedule_tests.context(intake), route_reviews=reviews(intake)
    ).to_dict()
    assert report["status"] == "complete"
    leg = next(r for r in report["results"] if r["version"] == "v1")["legs"][0]
    assert leg["selected_interval"]["start"] == "2020-01-01T10:20:00+00:00"
    assert leg["available_nanoseconds"] == 2400000000000
    assert len(leg["fragments"]) == 2
    assert leg["deadline_kind"] == "next_visit"
    assert leg["schedule_tolerance_seconds"] == 300
    assert intake.to_dict() == before


def coordinates(identity, **fields):
    ids = sorted(
        {r["canonical_place_id"] for r in identity.to_dict()["records"] if r["canonical_place_id"]}
    )
    return {
        "schema_version": "rtpeval_route_coordinates_1",
        "batch_id": "batch",
        "revision": "1",
        "records": [
            {
                "place_id": pid,
                "latitude": i,
                "longitude": i + 1,
                "evidence_sha256": "a" * 64,
                "source_ref": "synthetic-coordinate-evidence",
                "reviewer_ref": "independent-reviewer",
                "reviewed_at": "2026-10-02T00:00:00Z",
            }
            for i, pid in enumerate(ids)
        ],
        **fields,
    }


@pytest.fixture
def route_case(prepared_scenario, batch, tmp_path, monkeypatch):
    sequence = 0
    _, source_results, _, _, _ = batch
    baseline = copy.deepcopy(source_results)

    def build(
        element=None,
        *,
        change=no_departure,
        obligations=(),
        options=None,
        review_change=None,
        coordinate_change=None,
        context_change=None,
        requested="2019-12-01T00:00:00Z",
        unresolved_names=(),
        paired=False,
        status_code=200,
    ):
        nonlocal sequence
        source_results.clear()
        source_results.update(copy.deepcopy(baseline))
        intake, identity, _ = prepared_scenario(
            obligations, change, unresolved_names=unresolved_names
        )
        ctx, review, coords = schedule_tests.context(intake), reviews(intake), coordinates(identity)
        if options is not None:
            coords["mode_options"] = options
        if review_change:
            review_change(review)
        if coordinate_change:
            coordinate_change(coords)
        preparation = prepare_routes(
            intake, identity, ctx, route_reviews=review, coordinate_evidence=coords, paired=paired
        ).to_dict()
        assert preparation["status"] == "complete", preparation
        contexts = preparation["route_contexts"]
        if context_change:
            context_change(contexts)
        plan = build_evidence_plan(intake, identity, contexts, paired=paired)
        sequence += 1
        directory = tmp_path / f"routes-{sequence}"
        monkeypatch.setattr("backend.evaluation.snapshot._now", lambda: requested)
        if element is None:
            element = {
                "status": {},
                "condition": "ROUTE_EXISTS",
                "duration": "1800s",
                "distanceMeters": 2500,
            }
        data = [{"originIndex": 0, "destinationIndex": 0, **element}]

        async def transport(request):
            body = (
                data
                if request["operation"] == "route_matrix"
                else {"id": request["parameters"]["place_id"]}
            )
            return Response(status_code, json.dumps(body).encode())

        asyncio.run(
            acquire_snapshot(
                plan, directory, transport, AcquisitionPolicy(max_sends=len(plan["requests"]) or 1)
            )
        )
        return intake, identity, directory, ctx, review, coords, plan

    return build


def score(case, **kwargs):
    intake, identity, directory, ctx, review, coords, _ = case
    return score_routes(
        intake, identity, directory, ctx, route_reviews=review, coordinate_evidence=coords, **kwargs
    ).to_dict()


def first(report, version="v1"):
    return next(r for r in report["results"] if r["version"] == version)["routes"]


def test_frozen_walk_fits_longest_interval_without_provider_or_source_rewrite(route_case):
    case = route_case(obligations=[protection()])
    report = score(case)
    assert report["status"] == "complete", report
    route = first(report)
    leg = route["checks"][0]
    assert leg["state"] == "PASS"
    assert leg["duration_nanoseconds"] == 1800000000000
    assert leg["raw_deficit_nanoseconds"] == 0
    assert route["complete_evidence_count"] == 1
    assert score(case) == report


def test_explicit_departure_before_protection_is_not_replaced_by_longer_gap(route_case):
    def explicit(results):
        no_departure(results)
        for version, result in results.items():
            if version != "v0":
                result["itinerary"]["transfers"][0]["departure_time"] = "2020-01-01T10:00:00Z"

    route = first(score(route_case(obligations=[protection()], change=explicit)))
    leg = route["checks"][0]
    assert leg["state"] == "FAIL"
    assert leg["evaluation_departure"] == "2020-01-01T10:00:00+00:00"
    assert leg["schedule_tolerance_seconds"] == 0
    assert leg["raw_deficit_nanoseconds"] == 1200000000000


@pytest.mark.parametrize(
    "duration,state", [("1800s", "PASS"), ("1800.000000001s", "FAIL"), ("1920s", "FAIL")]
)
def test_hard_boundary_never_borrows_schedule_tolerance(route_case, duration, state):
    case = route_case(
        {"status": {}, "condition": "ROUTE_EXISTS", "duration": duration, "distanceMeters": 2000},
        obligations=[protection("10:30", "11:00")],
    )
    leg = first(score(case))["checks"][0]
    assert leg["state"] == state
    assert leg["components"]["schedule"]["tolerance_seconds"] == 0


@pytest.mark.parametrize(
    "duration,distance,state,complete",
    [
        ("3600s", None, "FAIL", False),
        (None, 3001, "FAIL", False),
        ("1800s", None, "UNKNOWN", False),
        ("3000s", 3000, "PASS", True),
        ("3000.000000001s", 3000, "FAIL", True),
    ],
)
def test_cap_failure_is_decisive_with_other_component_unknown(
    route_case, duration, distance, state, complete
):
    element = {"status": {}, "condition": "ROUTE_EXISTS"}
    if duration is not None:
        element["duration"] = duration
    if distance is not None:
        element["distanceMeters"] = distance
    route = first(score(route_case(element)))
    leg = route["checks"][0]
    assert leg["state"] == state
    assert leg["complete_evidence"] is complete
    assert route["conditional_compliance"]["denominator"] == (0 if state == "UNKNOWN" else 1)


@pytest.mark.parametrize("duration,state", [("2100s", "PASS"), ("2100.000000001s", "FAIL")])
def test_next_visit_deadline_retains_exact_five_minute_tolerance(route_case, duration, state):
    def short(results):
        no_departure(results)
        for result in results.values():
            result["itinerary"]["days"][0]["activities"][-1]["start_time"] = "2020-01-01T10:30:00Z"

    leg = first(
        score(
            route_case(
                {
                    "status": {},
                    "condition": "ROUTE_EXISTS",
                    "duration": duration,
                    "distanceMeters": 2000,
                },
                change=short,
            )
        )
    )["checks"][0]
    assert leg["state"] == state
    assert leg["raw_deficit_seconds_exact"] == ("300" if state == "PASS" else "300.000000001")


def test_drive_reserve_is_counted_once_and_kept_out_of_provider_burden(route_case):
    def drive(results):
        no_departure(results)
        for version, result in results.items():
            result["itinerary"]["days"][0]["activities"][-1]["start_time"] = "2020-01-01T10:25:00Z"
            if version != "v0":
                result["itinerary"]["transfers"][0].update(
                    mode="DRIVE", reserve_seconds=99999, validation_state="FAIL"
                )

    route = first(
        score(
            route_case(
                {"status": {}, "condition": "ROUTE_EXISTS", "duration": "1200s"}, change=drive
            )
        )
    )
    leg = route["checks"][0]
    assert leg["state"] == "PASS"
    assert leg["raw_deficit_seconds_exact"] == "300"
    assert route["observed_transfer_burden"]["duration_seconds_exact"] == "1200"
    assert route["observed_transfer_burden"]["product_reserve_seconds_subtotal"] == 600


@pytest.mark.parametrize(
    "element,state",
    [
        ({"status": {}, "condition": "ROUTE_NOT_FOUND"}, "FAIL"),
        ({"status": {"code": 7}, "condition": "ROUTE_NOT_FOUND"}, "UNKNOWN"),
        ({"condition": "ROUTE_NOT_FOUND"}, "UNKNOWN"),
        ({"status": {}, "condition": "ROUTE_NOT_FOUND", "duration": "0s"}, "UNKNOWN"),
        ({"status": {}, "condition": "ROUTE_EXISTS", "duration": "-1s"}, "UNKNOWN"),
        ({"status": {}, "condition": "ROUTE_EXISTS", "duration": "nan"}, "UNKNOWN"),
    ],
)
def test_no_route_and_invalid_raw_response_do_not_invent_zero_duration(route_case, element, state):
    route = first(score(route_case(element)))
    leg = route["checks"][0]
    assert leg["state"] == state
    assert leg["duration_nanoseconds"] is None
    assert leg["raw_deficit_nanoseconds"] is None
    assert route["observed_transfer_burden"]["duration_seconds_exact"] is None


def test_applicable_returned_traffic_fallback_is_retained(route_case):
    case = route_case(
        {
            "status": {},
            "condition": "ROUTE_EXISTS",
            "duration": "1800.25s",
            "distanceMeters": 2500,
            "fallbackInfo": {
                "routingMode": "FALLBACK_TRAFFIC_UNAWARE",
                "reason": "LATENCY_EXCEEDED",
            },
        }
    )
    leg = first(score(case))["checks"][0]
    assert leg["state"] == "PASS"
    assert leg["duration_seconds_exact"] == "1800.25"
    assert leg["observation"]["element"]["fallbackInfo"]["reason"] == "LATENCY_EXCEEDED"


def test_malformed_status_message_does_not_establish_available_route(route_case):
    case = route_case(
        {
            "status": {"message": 123},
            "condition": "ROUTE_EXISTS",
            "duration": "3600s",
            "distanceMeters": 4000,
        }
    )
    leg = first(score(case))["checks"][0]
    assert leg["state"] == "UNKNOWN"
    assert leg["response_applicable"] is False


@pytest.mark.parametrize(
    "mismatch,reason",
    [
        ("mode", "query_mode_mismatch"),
        ("departure", "query_departure_mismatch"),
        ("coordinates", "query_origin_mismatch"),
        ("options", "query_options_mismatch"),
    ],
)
def test_valid_but_inapplicable_context_cannot_prove_cap_failure(route_case, mismatch, reason):
    def alter(contexts):
        for context in contexts:
            if mismatch == "mode":
                context["mode"] = "DRIVE"
            elif mismatch == "departure":
                context["departure"] = "2020-01-01T10:01:00Z"
            elif mismatch == "coordinates":
                context["origin"]["latitude"] += 1
            else:
                context["routing_options"]["language_code"] = "fr"

    case = route_case(
        {"status": {}, "condition": "ROUTE_EXISTS", "duration": "3600s", "distanceMeters": 4000},
        options={"WALK": {"time_basis": "explicit_departure", "routing_options": {}}},
        context_change=alter,
    )
    leg = first(score(case))["checks"][0]
    assert leg["state"] == "UNKNOWN"
    assert reason in leg["context_reasons"]
    assert leg["duration_nanoseconds"] is None


def test_same_instant_query_with_other_offset_is_applicable(route_case):
    def alter(contexts):
        for context in contexts:
            context["departure"] = "2020-01-01T11:00:00+01:00"

    case = route_case(
        options={"WALK": {"time_basis": "explicit_departure", "routing_options": {}}},
        context_change=alter,
    )
    assert first(score(case))["checks"][0]["state"] == "PASS"


def test_historical_walk_query_does_not_shift_to_acquisition_day(route_case):
    case = route_case(
        options={"WALK": {"time_basis": "explicit_departure", "routing_options": {}}},
        requested="2026-10-02T00:00:00Z",
    )
    leg = first(score(case))["checks"][0]
    assert leg["state"] == "UNKNOWN"
    assert "historical_query_unsupported" in leg["context_reasons"]
    assert leg["evaluation_departure"] == "2020-01-01T10:00:00+00:00"


def test_missing_mode_policy_prevents_pass_but_not_independent_proven_failure(route_case):
    case = route_case()
    intake, identity, directory, ctx, _, coords, _ = case
    leg = first(
        score_routes(intake, identity, directory, ctx, coordinate_evidence=coords).to_dict()
    )["checks"][0]
    assert leg["state"] == "UNKNOWN"
    assert leg["components"]["mode_policy"]["reason"] == "request_mode_policy_unavailable"


def test_known_disallowed_mode_is_failure_without_changing_query_mode(route_case):
    def restrict(review):
        review["groups"][0].update(
            status="restricted",
            policies=[
                {
                    "policy_id": "mode-rule",
                    "scope": "whole_trip",
                    "allowed_modes": ["DRIVE"],
                    "source_refs": schedule_tests.SOURCE,
                }
            ],
        )

    leg = first(score(route_case(review_change=restrict)))["checks"][0]
    assert leg["state"] == "FAIL"
    assert leg["mode"] == "WALK"
    assert leg["components"]["mode_policy"]["reason"] == "claimed_mode_disallowed"


@pytest.mark.parametrize("fault", ["stale", "duplicate", "quote", "contradiction", "foreign_field"])
def test_invalid_independent_mode_review_rejects_whole_material(prepared_scenario, fault):
    intake, identity, _ = prepared_scenario(change=no_departure)
    review = reviews(intake)
    if fault == "stale":
        review["groups"][0]["input_sha256"] = "0" * 64
    elif fault == "duplicate":
        review["groups"].append(copy.deepcopy(review["groups"][0]))
    elif fault == "foreign_field":
        review["groups"][0]["itinerary_mode"] = "DRIVE"
    else:
        review["groups"][0].update(
            status="restricted",
            policies=[
                {
                    "policy_id": "mode-rule",
                    "scope": "whole_trip",
                    "allowed_modes": ["DRIVE"],
                    "source_refs": schedule_tests.SOURCE
                    if fault == "contradiction"
                    else [{"field_path": "additional_preferences", "quote": "not in Input"}],
                }
            ],
        )
        if fault == "contradiction":
            other = copy.deepcopy(review["groups"][0]["policies"][0])
            other.update(policy_id="other", allowed_modes=["WALK"])
            review["groups"][0]["policies"].append(other)
    report = prepare_routes(intake, identity, route_reviews=review).to_dict()
    assert report["status"] == "needs_material_correction"
    assert report["results"] == []


def test_same_canonical_is_na_and_unknown_identity_keeps_candidate(route_case):
    def same(results):
        no_departure(results)
        for result in results.values():
            result["itinerary"]["days"][0]["activities"][-1].update(
                title="Museum A", place_name="Museum A"
            )

    route = first(score(route_case(change=same)))
    assert route["counts"] == {"PASS": 0, "FAIL": 0, "UNKNOWN": 0, "N/A": 1}
    assert route["applicable_count"] == 0
    unknown = first(score(route_case(unresolved_names=["Museum B"])))
    assert unknown["applicable_count"] == 1
    assert unknown["counts"]["UNKNOWN"] == 1


def test_conflicting_transfer_modes_do_not_choose_favorable_query(route_case):
    def conflict(results):
        no_departure(results)
        for version, result in results.items():
            if version != "v0":
                other = copy.deepcopy(result["itinerary"]["transfers"][0])
                other["mode"] = "DRIVE"
                result["itinerary"]["transfers"].append(other)

    leg = first(score(route_case(change=conflict)))["checks"][0]
    assert leg["state"] == "UNKNOWN"
    assert leg["mode"] is None
    assert leg["evidence_reference"]["request_key"] is None


def test_exact_duplicate_claims_keep_one_occurrence_score_unit(route_case):
    def duplicate(results):
        no_departure(results)
        for version, result in results.items():
            if version != "v0":
                result["itinerary"]["transfers"].append(
                    copy.deepcopy(result["itinerary"]["transfers"][0])
                )

    route = first(score(route_case(change=duplicate)))
    assert route["applicable_count"] == 1
    assert route["counts"]["PASS"] == 1
    assert len(route["checks"][0]["claims"]) == 2


def test_invalid_explicit_departure_cannot_fall_back_to_default(route_case):
    def invalid(results):
        no_departure(results)
        for version, result in results.items():
            if version != "v0":
                result["itinerary"]["transfers"][0]["departure_time"] = "broken"

    leg = first(score(route_case(change=invalid)))["checks"][0]
    assert leg["state"] == "UNKNOWN"
    assert leg["selected_interval"] is None
    assert "invalid_timestamp" in leg["reasons"]


def test_foreign_or_corrupt_snapshot_requires_whole_material_correction(route_case):
    case = route_case()
    directory, plan = case[2], case[6]
    snapshot = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    snapshot["plan"]["legs"][0]["group_id"] = "foreign"
    from backend.evaluation.records import canonical_digest

    snapshot["plan_hash"] = canonical_digest(snapshot["plan"])
    (directory / "manifest.json").write_text(json.dumps(snapshot), encoding="utf-8")
    report = score(case)
    assert report["status"] == "needs_material_correction"
    assert report["results"] == []
    assert score(case, expected_plan=plan)["status"] == "needs_material_correction"


def test_v0_activity_is_authoritative_and_later_versions_do_not_fall_back(route_case):
    report = score(route_case(change=None))
    assert first(report, "v0")["counts"]["PASS"] == 1
    for version in ("v1", "v2", "v3"):
        leg = first(report, version)["checks"][0]
        assert leg["state"] == "UNKNOWN"
        assert leg["claims_present"] is False
        assert leg["mode"] is None
    assert report["results"][1]["ignored_transport"]


def test_equal_longest_fragments_choose_earliest_without_summing_gaps(route_case):
    case = route_case(
        {"status": {}, "condition": "ROUTE_EXISTS", "duration": "1560s", "distanceMeters": 2500},
        obligations=[protection("10:20", "10:40")],
    )
    leg = first(score(case))["checks"][0]
    assert leg["selected_interval"]["start"] == "2020-01-01T10:00:00+00:00"
    assert leg["available_nanoseconds"] == 1200000000000
    assert leg["state"] == "FAIL"


def test_primary_visit_only_protection_does_not_block_travel(route_case):
    leg = first(score(route_case(obligations=[protection(scope="primary_visits")])))["checks"][0]
    assert leg["state"] == "PASS"
    assert leg["available_nanoseconds"] == 3600000000000
    assert leg["blockers"] == []


def test_unknown_generic_occupancy_is_conservative_but_disjoint_unknown_does_not_contaminate(
    route_case,
):
    from backend.tests.evaluation.test_intake import activity

    def uncertain(start, end):
        def change(results):
            no_departure(results)
            for result in results.values():
                rest = activity("rest", "Rest", start, end, "free_time")
                rest["notes"] = "Reserved arrangement needs review"
                result["itinerary"]["days"][0]["activities"].append(rest)

        return change

    leg = first(score(route_case(change=uncertain("10:10", "10:20"))))["checks"][0]
    assert leg["state"] == "UNKNOWN"
    assert "occupied_time_unresolved" in leg["reasons"]
    assert leg["selected_interval"] is None
    disjoint = first(score(route_case(change=uncertain("12:00", "12:30"))))["checks"][0]
    assert disjoint["state"] == "PASS"


def test_unresolved_adjacency_suppresses_population_rates_and_provider_verdict(route_case):
    def overlap(results):
        no_departure(results)
        for result in results.values():
            result["itinerary"]["days"][0]["activities"][-1]["start_time"] = "2020-01-01T09:30:00Z"

    route = first(
        score(
            route_case(
                {
                    "status": {},
                    "condition": "ROUTE_EXISTS",
                    "duration": "3600s",
                    "distanceMeters": 4000,
                },
                change=overlap,
            )
        )
    )
    assert route["counts"]["UNKNOWN"] == 1
    assert route["conditional_compliance"]["rate"] is None
    assert route["applicable_denominator"] is None
    assert route["observed_transfer_burden"]["full_scope_complete"] is False


def test_tolerance_passes_are_explicitly_labelled_in_component_report(route_case):
    def short(results):
        no_departure(results)
        for result in results.values():
            result["itinerary"]["days"][0]["activities"][-1]["start_time"] = "2020-01-01T10:44:00Z"

    leg = first(
        score(
            route_case(
                {
                    "status": {},
                    "condition": "ROUTE_EXISTS",
                    "duration": "2940s",
                    "distanceMeters": 2500,
                },
                change=short,
            )
        )
    )["checks"][0]
    assert leg["state"] == "PASS"
    assert leg["components"]["duration_cap"]["classification"] == "within_tolerance"
    assert leg["components"]["schedule"]["classification"] == "within_tolerance"


def test_non_string_submitted_clock_remains_unknown_interpretation(route_case):
    def invalid(results):
        no_departure(results)
        for version, result in results.items():
            if version != "v0":
                result["itinerary"]["transfers"][0]["departure_time"] = {"invalid": "clock"}

    case = route_case(change=invalid)
    leg = first(score(case))["checks"][0]
    assert leg["state"] == "UNKNOWN"
    assert "invalid_timestamp" in leg["reasons"]


def test_paired_v3_occurrences_are_independent_and_scope_is_not_inferred(route_case):
    def paired(results):
        no_departure(results)
        results["v3"]["v3"] = {
            "draft": copy.deepcopy(results["v3"]["itinerary"]),
            "final_primary": copy.deepcopy(results["v3"]["itinerary"]),
        }

    case = route_case(change=paired, paired=True)
    report = score(case, paired=True, expected_plan=case[6])
    assert report["status"] == "complete"
    assert [(r["version"], r["projection"]) for r in report["results"]][-3:] == [
        ("v3", "final"),
        ("v3", "draft"),
        ("v3", "final_primary"),
    ]
    assert sum(r["routes"]["applicable_count"] for r in report["results"]) == 6
    assert score(case)["status"] == "needs_material_correction"


@pytest.mark.parametrize(
    "time_basis,state", [("explicit_departure", "PASS"), ("time_independent", "UNKNOWN")]
)
def test_transit_requires_applicable_explicit_departure(route_case, time_basis, state):
    def transit(results):
        no_departure(results)
        for version, result in results.items():
            if version != "v0":
                result["itinerary"]["transfers"][0]["mode"] = "TRANSIT"

    case = route_case(
        {"status": {}, "condition": "ROUTE_EXISTS", "duration": "3000s"},
        change=transit,
        options={"TRANSIT": {"time_basis": time_basis, "routing_options": {}}},
        requested="2020-01-02T00:00:00Z",
    )
    leg = first(score(case))["checks"][0]
    assert leg["state"] == state
    if state == "UNKNOWN":
        assert "time_independent_mode_unsupported" in leg["context_reasons"]


def test_raw_hash_change_is_integrity_failure_not_smaller_coverage(route_case):
    case = route_case()
    manifest = json.loads((case[2] / "manifest.json").read_text(encoding="utf-8"))
    raw = manifest["records"][0]["attempts"][0]["raw"]["path"]
    (case[2] / raw).write_bytes(b"tampered")
    report = score(case)
    assert report["status"] == "needs_material_correction"
    assert report["results"] == []


def test_fixed_generic_review_changes_available_fragment_without_changing_sources(route_case):
    from backend.tests.evaluation.test_intake import activity

    def rest(results):
        no_departure(results)
        for result in results.values():
            item = activity("rest", "Rest", "10:30", "11:00", "free_time")
            item["notes"] = "Reserved rest"
            result["itinerary"]["days"][0]["activities"].append(item)

    case = route_case(
        {"status": {}, "condition": "ROUTE_EXISTS", "duration": "1920s", "distanceMeters": 2500},
        change=rest,
    )
    intake = case[0]
    decisions = schedule_tests.occupancy_review(intake)
    # Review all four source-preserved representations independently.
    item = decisions["records"][0]
    decisions["records"] = [
        {**item, "source": run["final"]["activities"][-1]["source"]}
        for run in intake.to_dict()["inventory"][0]["runs"].values()
    ]
    leg = first(score(case, occupancy_reviews=decisions))["checks"][0]
    assert leg["state"] == "FAIL"
    assert leg["deadline_kind"] == "hard_boundary"
    assert leg["raw_deficit_seconds_exact"] == "120"
    for item in decisions["records"]:
        item["occupancy"] = "uncommitted"
    assert first(score(case, occupancy_reviews=decisions))["checks"][0]["state"] == "PASS"


@pytest.mark.parametrize(
    "day,gap_start,reason",
    [("2020-11-01", "01:15", "dst_fold"), ("2020-03-08", "02:30", "dst_gap")],
)
def test_dst_uncertainty_remains_route_unknown(route_case, day, gap_start, reason):
    def clocks(results):
        no_departure(results)
        for result in results.values():
            delivered = result["itinerary"]["days"][0]
            delivered["date"] = day
            delivered["activities"][0].update(
                start_time=day + "T00:30:00", end_time=day + "T" + gap_start + ":00"
            )
            delivered["activities"][-1].update(
                start_time=day + "T04:00:00", end_time=day + "T05:00:00"
            )

    case = route_case(change=clocks)
    ctx = copy.deepcopy(case[3])
    ctx["groups"][0]["timezone"] = "America/New_York"
    report = score_routes(
        case[0], case[1], case[2], ctx, route_reviews=case[4], coordinate_evidence=case[5]
    ).to_dict()
    leg = first(report)["checks"][0]
    assert leg["state"] == "UNKNOWN"
    assert reason in leg["reasons"]


def test_missing_timezone_never_uses_host_for_naive_clocks(route_case):
    def naive(results):
        no_departure(results)
        for result in results.values():
            for activity in result["itinerary"]["days"][0]["activities"]:
                activity["start_time"] = (
                    activity["start_time"].replace("+00:00", "").removesuffix("Z")
                )
                activity["end_time"] = activity["end_time"].replace("+00:00", "").removesuffix("Z")

    case = route_case(change=naive)
    assert first(score(case))["checks"][0]["state"] == "PASS"
    report = score_routes(
        case[0], case[1], case[2], route_reviews=case[4], coordinate_evidence=case[5]
    ).to_dict()
    leg = first(report)["checks"][0]
    assert leg["state"] == "UNKNOWN"
    assert "timezone_missing" in leg["reasons"]


def test_empty_applicable_population_has_unavailable_rates(route_case):
    def empty(results):
        for result in results.values():
            result["itinerary"]["days"][0]["activities"] = []

    route = first(score(route_case(change=empty)))
    assert route["state"] == "N/A"
    assert route["applicable_count"] == 0
    assert route["conditional_compliance"]["rate"] is None


def test_repeated_venue_occurrences_and_request_dedup_keep_score_units(route_case):
    from backend.tests.evaluation.test_intake import activity

    def repeated(results):
        no_departure(results)
        for version, result in results.items():
            day = result["itinerary"]["days"][0]
            day["activities"].extend(
                [
                    activity("a2", "Museum A", "12:00", "12:30", place="Museum A"),
                    activity("b2", "Museum B", "13:30", "14:30", place="Museum B"),
                ]
            )
            if version != "v0":
                result["itinerary"]["transfers"].extend(
                    [
                        {"from_activity_id": "b", "to_activity_id": "a2", "mode": "WALK"},
                        {"from_activity_id": "a2", "to_activity_id": "b2", "mode": "WALK"},
                    ]
                )

    case = route_case(change=repeated)
    assert len([r for r in case[6]["requests"] if r["operation"] == "route_matrix"]) == 2
    route = first(score(case))
    assert route["applicable_count"] == 3
    assert route["observed_transfer_burden"]["observed_leg_count"] == 3
    assert route["observed_transfer_burden"]["duration_seconds_exact"] == "5400"


@pytest.mark.parametrize(
    "fault", ["foreign_id", "duplicate", "nan", "bool", "hash", "options_type"]
)
def test_coordinate_preparation_must_be_independent_typed_and_linked(prepared_scenario, fault):
    intake, identity, _ = prepared_scenario(change=no_departure)
    coords = coordinates(identity)
    point = coords["records"][0]
    if fault == "foreign_id":
        point["place_id"] = "foreign"
    elif fault == "duplicate":
        coords["records"].append(copy.deepcopy(point))
    elif fault == "nan":
        point["latitude"] = float("nan")
    elif fault == "bool":
        point["longitude"] = True
    elif fault == "hash":
        point["evidence_sha256"] = "missing"
    else:
        coords["mode_options"] = {
            "WALK": {"time_basis": "time_independent", "routing_options": {"language_code": 123}}
        }
    report = prepare_routes(intake, identity, coordinate_evidence=coords).to_dict()
    assert report["status"] == "needs_material_correction"
    assert report["results"] == []


def test_known_disjoint_transfer_alternatives_do_not_poison_earlier_leg(route_case):
    from backend.tests.evaluation.test_intake import activity

    def alternatives(results):
        no_departure(results)
        for version, result in results.items():
            day = result["itinerary"]["days"][0]
            day["activities"].extend(
                [
                    activity("c", "Museum C", "12:00", "13:00", place="Museum C"),
                    activity("d", "Museum D", "14:00", "15:00", place="Museum D"),
                ]
            )
            if version != "v0":
                result["itinerary"]["transfers"].extend(
                    [
                        {
                            "from_activity_id": "b",
                            "to_activity_id": "c",
                            "mode": "WALK",
                            "departure_time": "2020-01-01T11:30:00Z",
                            "arrival_time": "2020-01-01T11:50:00Z",
                        },
                        {
                            "from_activity_id": "c",
                            "to_activity_id": "d",
                            "mode": "WALK",
                            "departure_time": "2020-01-01T13:00:00Z",
                            "arrival_time": "2020-01-01T13:30:00Z",
                        },
                        {
                            "from_activity_id": "c",
                            "to_activity_id": "d",
                            "mode": "WALK",
                            "departure_time": "2020-01-01T13:10:00Z",
                            "arrival_time": "2020-01-01T13:40:00Z",
                        },
                    ]
                )

    route = first(score(route_case(change=alternatives)))
    assert route["checks"][0]["state"] == "PASS"
    assert "occupied_time_unresolved" not in route["checks"][0]["reasons"]
    assert route["checks"][-1]["state"] == "UNKNOWN"


def test_unresolved_other_day_keeps_observed_subtotal_without_claiming_full_burden(route_case):
    from backend.tests.evaluation.test_intake import activity

    def uncertain_day(results):
        no_departure(results)
        for result in results.values():
            unknown = activity("unknown", "Special experience", "09:00", "10:00", "unknown")
            unknown["start_time"] = unknown["start_time"].replace("2020-01-01", "2020-01-02")
            unknown["end_time"] = unknown["end_time"].replace("2020-01-01", "2020-01-02")
            result["itinerary"]["days"].append({"date": "2020-01-02", "activities": [unknown]})

    route = first(score(route_case(change=uncertain_day)))
    assert route["counts"]["PASS"] == 1
    assert route["applicable_denominator"] is None
    assert route["observed_transfer_burden"]["duration_seconds_exact"] == "1800"
    assert route["observed_transfer_burden"]["full_scope_complete"] is False
    days = {d["date"]: d for d in route["daily_observed_transfer_burden"]}
    assert days["2020-01-01"]["full_scope_complete"] is True
    assert days["2020-01-02"]["full_scope_complete"] is False


def test_same_day_unresolved_population_also_prevents_complete_daily_burden(route_case):
    from backend.tests.evaluation.test_intake import activity

    def unknown(results):
        no_departure(results)
        for result in results.values():
            result["itinerary"]["days"][0]["activities"].append(
                activity("unknown", "Special experience", "12:00", "13:00", "unknown")
            )

    route = first(score(route_case(change=unknown)))
    assert route["daily_observed_transfer_burden"][0]["full_scope_complete"] is False


def test_nanosecond_query_mismatch_is_not_silently_truncated(route_case):
    def alter(contexts):
        for context in contexts:
            context["departure"] = "2020-01-01T10:00:00.000000001Z"

    case = route_case(
        options={"WALK": {"time_basis": "explicit_departure", "routing_options": {}}},
        context_change=alter,
    )
    leg = first(score(case))["checks"][0]
    assert leg["state"] == "UNKNOWN"
    assert "unsupported_query_timestamp_precision" in leg["context_reasons"]


@pytest.mark.parametrize("fault", ["wrong_mode_preference", "string_modifier", "empty_locale"])
def test_supported_wire_with_unsupported_provider_options_is_unknown(route_case, fault):
    options = {
        "wrong_mode_preference": {"routing_preference": "TRAFFIC_AWARE"},
        "string_modifier": {"avoid_tolls": "true"},
        "empty_locale": {"language_code": ""},
    }[fault]
    case = route_case(
        options={"WALK": {"time_basis": "time_independent", "routing_options": options}}
    )
    leg = first(score(case))["checks"][0]
    assert leg["state"] == "UNKNOWN"
    assert leg["context_reasons"]


def test_missing_coordinates_and_provider_error_retain_full_candidate_counts(route_case):
    case = route_case()
    report = score_routes(case[0], case[1], case[2], case[3], route_reviews=case[4]).to_dict()
    route = first(report)
    assert route["applicable_count"] == 1
    assert route["counts"]["UNKNOWN"] == 1
    assert route["duration_available_count"] == 0
    assert first(score(route_case(status_code=503)))["counts"]["UNKNOWN"] == 1


def test_explicit_input_mode_can_supply_basis_without_manufacturing_transfers(
    batch, prepared_scenario
):
    manifest, results, _, save, root = batch
    original = json.loads((root / "input.json").read_text(encoding="utf-8"))
    original["additional_preferences"] = "Use WALK between all visits."
    ref = save("input.json", original)
    manifest["groups"][0]["input_ref"] = ref
    spec = json.loads((root / "requirements.json").read_text(encoding="utf-8"))
    spec["input_sha256"] = ref["sha256"]
    save("requirements.json", spec)
    for version in results:
        provenance = json.loads((root / (version + "-provenance.json")).read_text(encoding="utf-8"))
        provenance["input_sha256"] = ref["sha256"]
        manifest["groups"][0]["selected_runs"][version]["provenance_ref"] = save(
            version + "-provenance.json", provenance, "rtpeval_provenance_1"
        )

    def missing(results):
        no_departure(results)
        for result in results.values():
            result["itinerary"]["transfers"] = []

    intake, identity, _ = prepared_scenario(change=missing)
    sources = [{"field_path": "additional_preferences", "quote": "Use WALK between all visits."}]
    review = reviews(
        intake,
        status="restricted",
        policies=[
            {
                "policy_id": "walk-only",
                "scope": "whole_trip",
                "allowed_modes": ["WALK"],
                "source_refs": sources,
            }
        ],
        stated_mode={"mode": "WALK", "source_refs": sources},
    )
    prepared = prepare_routes(
        intake,
        identity,
        schedule_tests.context(intake),
        route_reviews=review,
        coordinate_evidence=coordinates(identity),
    ).to_dict()
    assert prepared["status"] == "complete"
    assert len(prepared["route_contexts"]) == 4
    for result in prepared["results"]:
        leg = result["legs"][0]
        assert leg["mode"] == "WALK"
        assert leg["mode_basis"] == "original_input_review"
        assert leg["claims_present"] is False


def test_interday_visits_never_become_route_checks(route_case):
    def separate(results):
        no_departure(results)
        for result in results.values():
            visits = result["itinerary"]["days"][0]["activities"]
            second = visits.pop()
            second["start_time"] = "2020-01-02T09:00:00Z"
            second["end_time"] = "2020-01-02T10:00:00Z"
            result["itinerary"]["days"].append({"date": "2020-01-02", "activities": [second]})
            result["itinerary"]["transfers"] = []

    route = first(score(route_case(change=separate)))
    assert route["checks"] == []
    assert route["applicable_count"] == 0


def test_v0_segmented_transport_is_not_collapsed_into_single_mode_route(route_case):
    from backend.tests.evaluation.test_intake import activity

    def segmented(results):
        original = results["v0"]["itinerary"]["days"][0]["activities"]
        original[1]["end_time"] = "2020-01-01T10:10:00Z"
        original.append(activity("transit", "Public transit", "10:10", "10:20", "transport"))

    leg = first(score(route_case(change=segmented)), "v0")["checks"][0]
    assert leg["state"] == "UNKNOWN"
    assert "transport_claims_conflicting_or_segmented" in leg["reasons"]


@pytest.mark.parametrize("alternative_start,state", [("10:30", "FAIL"), ("10:35", "UNKNOWN")])
def test_other_transport_alternative_at_deadline_cannot_borrow_visit_tolerance(
    route_case, alternative_start, state
):
    from backend.tests.evaluation.test_intake import activity

    def alternatives(results):
        no_departure(results)
        for version, result in results.items():
            day = result["itinerary"]["days"][0]
            day["activities"][-1]["start_time"] = "2020-01-01T10:30:00Z"
            day["activities"].extend(
                [
                    activity("c", "Museum C", "12:00", "13:00", place="Museum C"),
                    activity("d", "Museum D", "14:00", "15:00", place="Museum D"),
                ]
            )
            if version != "v0":
                result["itinerary"]["transfers"].extend(
                    [
                        {
                            "from_activity_id": "b",
                            "to_activity_id": "c",
                            "mode": "WALK",
                            "departure_time": "2020-01-01T11:30:00Z",
                            "arrival_time": "2020-01-01T11:50:00Z",
                        },
                        {
                            "from_activity_id": "c",
                            "to_activity_id": "d",
                            "mode": "WALK",
                            "departure_time": "2020-01-01T10:30:00Z",
                            "arrival_time": "2020-01-01T10:45:00Z",
                        },
                        {
                            "from_activity_id": "c",
                            "to_activity_id": "d",
                            "mode": "WALK",
                            "departure_time": "2020-01-01T" + alternative_start + ":00Z",
                            "arrival_time": "2020-01-01T10:50:00Z",
                        },
                    ]
                )

    case = route_case(
        {"status": {}, "condition": "ROUTE_EXISTS", "duration": "1920s", "distanceMeters": 2500},
        change=alternatives,
    )
    leg = first(score(case))["checks"][0]
    assert leg["state"] == state
    if state == "FAIL":
        assert leg["deadline_kind"] == "hard_boundary"
        assert leg["raw_deficit_seconds_exact"] == "120"
