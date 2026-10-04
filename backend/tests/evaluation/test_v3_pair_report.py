"""Independent V3 pairs through report, provenance preparation and CLI seams."""

import asyncio
import copy
import json

import pytest

from backend.evaluation.snapshot import AcquisitionPolicy, Response, acquire_snapshot, load_snapshot
from backend.evaluation.v3_correspondence import prepare_v3_correspondence, read_v3_result_sources
from backend.evaluation.v3_pair_report import build_v3_pair_report
from backend.tests.evaluation import test_routes as route_tests
from backend.tests.evaluation.test_requirement_schedule import required
from backend.tests.evaluation.test_routes import no_departure, protection

pytest_plugins = ("backend.tests.evaluation.test_intake",)
route_case = route_tests.route_case
prepared_scenario = route_tests.prepared_scenario
STAMP = "2026-10-03T00:00:00Z"


@pytest.fixture
def pair_case(route_case):
    def build(
        after=None,
        before=None,
        source_change=None,
        edits=None,
        repair_change=None,
        details_payload=None,
        **kwargs,
    ):
        def change(results):
            no_departure(results)
            draft = copy.deepcopy(results["v3"]["itinerary"])
            if before:
                before(draft)
            final = copy.deepcopy(draft)
            if after:
                after(final)
            results["v3"]["v3"] = {"draft": draft, "final_primary": final}
            if edits is not None:
                repair = adopted_edit(draft, final, edits)
                if repair_change:
                    repair_change(repair)
                results["v3"]["v3"]["repair"] = repair

        case = route_case(change=source_change or change, paired=True, **kwargs)
        if details_payload:
            raw = {
                r["key"]: (case[2] / r["attempts"][-1]["raw"]["path"]).read_bytes()
                for r in load_snapshot(case[2])["records"]
                if r["attempts"]
            }

            async def transport(request):
                if request["operation"] == "places_details":
                    return Response(200, json.dumps(details_payload(request)).encode())
                return Response(200, raw[request["key"]])

            directory = case[2].parent / (case[2].name + "-opening")
            asyncio.run(
                acquire_snapshot(
                    case[6],
                    directory,
                    transport,
                    AcquisitionPolicy(max_sends=len(case[6]["requests"]) or 1),
                )
            )
            return *case[:2], directory, *case[3:]
        return case

    return build


def report(case, **kwargs):
    return build_v3_pair_report(
        case[0],
        case[1],
        case[2],
        case[3],
        route_reviews=case[4],
        coordinate_evidence=case[5],
        expected_plan=case[6],
        generated_at=STAMP,
        **kwargs,
    ).to_dict()


def test_missing_pair_stays_visible_without_fictional_evidence(route_case):
    case = route_case()
    result = build_v3_pair_report(case[0], case[1], None, generated_at=STAMP).to_dict()
    assert result["status"] == "complete"
    assert len(result["groups"]) == 1
    pair = result["groups"][0]
    assert pair["pair_status"] == "pair_unavailable"
    assert pair["available_stages"] == {"draft": False, "final_primary": False}
    assert pair["deltas"] is None
    assert pair["diagnostics"]


def test_identical_pair_reuses_scorers_and_has_exact_zero_deltas(pair_case):
    result = report(pair_case())
    assert result["status"] == "complete", result["diagnostics"]
    pair = result["groups"][0]
    assert pair["pair_status"] == "available"
    assert pair["included_dimensions"] == ["grounding", "non_overlap", "opening", "routes"]
    assert pair["stages"]["draft"]["label"] == "V3 draft"
    assert pair["stages"]["final_primary"]["label"] == "V3 final primary"
    assert pair["stages"]["draft"]["auxiliary_total"]["score_0_100"] == 50
    assert pair["deltas"]["auxiliary_total"]["percentage_points"] == 0
    assert pair["deltas"]["auxiliary_total"]["exact_fraction"] == {"numerator": 0, "denominator": 1}
    assert pair["deltas"]["dimensions"]["requirements"]["verified_score_percentage_points"] is None
    assert pair["deltas"]["dimensions"]["routes"]["denominator"] == 0


def adopted_edit(draft, final, edits):
    return {
        "status": "ACCEPTED_PARTIAL",
        "original": copy.deepcopy(draft),
        "final": copy.deepcopy(final),
        "rounds": [
            {
                "round_index": 1,
                "input_itinerary": copy.deepcopy(draft),
                "adopted": copy.deepcopy(final),
                "result": {
                    "status": "ACCEPTED_PARTIAL",
                    "original": copy.deepcopy(draft),
                    "final": copy.deepcopy(final),
                    "effective_patch": {"edits": edits},
                    "window_adjustments": [],
                },
            }
        ],
    }


def test_adopted_retime_matches_repeated_visits_without_review(pair_case, batch):
    def before(itinerary):
        extra = copy.deepcopy(itinerary["days"][0]["activities"][0])
        extra.update(
            activity_id="a2", start_time="2020-01-01T12:00:00Z", end_time="2020-01-01T13:00:00Z"
        )
        itinerary["days"][0]["activities"].append(extra)

    def after(itinerary):
        itinerary["days"][0]["activities"][0].update(
            start_time="2020-01-01T08:30:00Z", end_time="2020-01-01T09:30:00Z"
        )

    # Attach actual adopted snapshots before source hashes and identities are prepared.
    def change(results):
        no_departure(results)
        draft = copy.deepcopy(results["v3"]["itinerary"])
        before(draft)
        final = copy.deepcopy(draft)
        after(final)
        edit = {
            "operation": "retime",
            "activity_id": "a",
            "date": "2020-01-01",
            "place_id": None,
            "start_time": "2020-01-01T08:30:00Z",
            "end_time": "2020-01-01T09:30:00Z",
        }
        results["v3"]["v3"] = {
            "draft": draft,
            "final_primary": final,
            "repair": adopted_edit(draft, final, [edit]),
        }

    # pair_case exposes the fixture's underlying route builder for source-rich cases.
    case = pair_case(source_change=change)
    sources = read_v3_result_sources(case[0], batch[4] / "manifest.json")
    correspondence = prepare_v3_correspondence(case[0], case[1], sources).to_dict()
    assert correspondence["status"] == "complete", correspondence["diagnostics"]
    group = correspondence["groups"][0]
    assert group["unresolved"] == {"before": [], "after": []}
    relation = next(
        r for r in group["relations"] if r["before"][0]["pointer"].endswith("/activities/0")
    )
    assert relation["relation"] == "modified"
    assert relation["basis"] == "validated_adopted_lineage"
    assert relation["operations"] == ["retime"]
    assert relation["identity_change"] == "same_canonical_venue"


def edit(operation, aid="a", **fields):
    return {
        "operation": operation,
        "activity_id": aid,
        "date": "2020-01-01",
        "place_id": None,
        "start_time": None,
        "end_time": None,
        **fields,
    }


def test_deleted_visit_has_loss_context_and_pair_union_mask(pair_case, batch):
    def after(itinerary):
        itinerary["days"][0]["activities"] = itinerary["days"][0]["activities"][1:]
        itinerary["transfers"] = []

    case = pair_case(after=after, edits=[edit("delete")])
    out = report(case, result_sources=read_v3_result_sources(case[0], batch[4] / "manifest.json"))
    assert out["status"] == "complete", out["diagnostics"]
    pair = out["groups"][0]
    assert "routes" in pair["included_dimensions"]
    assert (
        pair["stages"]["final_primary"]["dimensions"]["routes"]["contribution"]["score_0_100"] == 0
    )
    assert pair["deltas"]["dimensions"]["routes"]["denominator"] == -1
    assert pair["visit_changes"]["removed_count"] == 1
    assert pair["visit_changes"]["added_count"] == 0
    assert out["status"] == "complete"
    removal = next(r for r in pair["correspondence"]["relations"] if r["relation"] == "removed")
    assert removal["after"] == []
    assert removal["operations"] == ["delete"]
    assert "repair_success" not in out


@pytest.mark.parametrize("operation", ["replace", "move"])
def test_adopted_slot_continuity_keeps_venue_and_date_changes_separate(pair_case, batch, operation):
    def after(itinerary):
        activity = itinerary["days"][0]["activities"][0]
        if operation == "replace":
            activity.update(
                place_name="Gallery C", title="Gallery C", source_place_id="canonical-Gallery C"
            )
        else:
            activity.update(start_time="2020-01-02T09:00:00Z", end_time="2020-01-02T10:00:00Z")
            itinerary["days"][0]["activities"].remove(activity)
            itinerary["days"].append({"date": "2020-01-02", "activities": [activity]})

    proposal = edit(
        operation,
        date="2020-01-02" if operation == "move" else "2020-01-01",
        place_id="canonical-Gallery C" if operation == "replace" else None,
        start_time="2020-01-02T09:00:00Z" if operation == "move" else "2020-01-01T09:00:00+00:00",
        end_time="2020-01-02T10:00:00Z" if operation == "move" else "2020-01-01T10:00:00+00:00",
    )
    case = pair_case(after=after, edits=[proposal])
    out = report(case, result_sources=read_v3_result_sources(case[0], batch[4] / "manifest.json"))
    assert out["status"] == "complete", out["diagnostics"]
    row = next(
        r for r in out["groups"][0]["correspondence"]["relations"] if operation in r["operations"]
    )
    assert row["relation"] == ("replaced" if operation == "replace" else "moved")
    assert row["identity_change"] == (
        "changed_canonical_venue" if operation == "replace" else "same_canonical_venue"
    )
    assert out["groups"][0]["correspondence"]["unresolved"] == {"before": [], "after": []}


def test_free_time_split_and_inserted_visit_preserve_source_topology(pair_case, batch):
    def before(itinerary):
        gap = copy.deepcopy(itinerary["days"][0]["activities"][0])
        gap.update(
            activity_id="window",
            activity_kind="free_time",
            title="Free time",
            place_name=None,
            start_time="2020-01-01T10:00:00Z",
            end_time="2020-01-01T11:00:00Z",
        )
        itinerary["days"][0]["activities"].insert(1, gap)

    def after(itinerary):
        activities = itinerary["days"][0]["activities"]
        gap = activities.pop(1)
        left, right, visit = copy.deepcopy(gap), copy.deepcopy(gap), copy.deepcopy(activities[0])
        left.update(activity_id="repair_r1_window_0_0", end_time="2020-01-01T10:10:00Z")
        right.update(activity_id="repair_r1_window_0_1", start_time="2020-01-01T10:40:00Z")
        visit.update(
            activity_id="repair_r1_1",
            title="Gallery C",
            place_name="Gallery C",
            source_place_id="canonical-Gallery C",
            start_time="2020-01-01T10:10:00Z",
            end_time="2020-01-01T10:40:00Z",
        )
        activities.extend([left, visit, right])
        itinerary["transfers"] = []

    def repair_change(repair):
        repair["rounds"][0]["result"]["window_adjustments"] = [
            {
                "root_activity_id": "window",
                "previous_fragment_id": "window",
                "fragment_ids": ["repair_r1_window_0_0", "repair_r1_window_0_1"],
                "authorized_start": "2020-01-01T10:00:00Z",
                "authorized_end": "2020-01-01T11:00:00Z",
                "consumed": [["2020-01-01T10:10:00Z", "2020-01-01T10:40:00Z"]],
            }
        ]

    case = pair_case(
        before=before,
        after=after,
        edits=[
            edit(
                "add",
                None,
                place_id="canonical-Gallery C",
                start_time="2020-01-01T10:10:00Z",
                end_time="2020-01-01T10:40:00Z",
            )
        ],
        repair_change=repair_change,
    )
    out = report(case, result_sources=read_v3_result_sources(case[0], batch[4] / "manifest.json"))
    assert out["status"] == "complete", out["diagnostics"]
    pair = out["groups"][0]
    split = next(r for r in pair["correspondence"]["relations"] if r["relation"] == "split")
    assert len(split["before"]) == 1 and len(split["after"]) == 2
    assert pair["visit_changes"]["added_count"] == 1
    assert pair["visit_changes"]["removed_count"] == 0
    assert pair["correspondence"]["unresolved"] == {"before": [], "after": []}


@pytest.mark.parametrize("unused_status", ["rejected", "pending", "rolled_back"])
def test_partial_round_uses_only_actually_adopted_components(pair_case, batch, unused_status):
    def after(itinerary):
        itinerary["days"][0]["activities"][1].update(
            start_time="2020-01-01T12:00:00Z", end_time="2020-01-01T12:30:00Z"
        )

    def repair_change(repair):
        result = repair["rounds"][0]["result"]
        result["components"] = [
            {
                "component_id": "component_1",
                "edit_indices": [0],
                "status": "accepted",
                "proposal": copy.deepcopy(repair["final"]),
            },
            {
                "component_id": "component_2",
                "edit_indices": [1],
                "status": unused_status,
                "proposal": copy.deepcopy(repair["original"]),
            },
        ]

    case = pair_case(
        after=after,
        edits=[
            edit("retime", "b", start_time="2020-01-01T12:00:00Z", end_time="2020-01-01T12:30:00Z"),
            edit(
                "add",
                None,
                place_id="canonical-Never adopted",
                start_time="2020-01-01T14:00:00Z",
                end_time="2020-01-01T15:00:00Z",
            ),
        ],
        repair_change=repair_change,
    )
    out = report(case, result_sources=read_v3_result_sources(case[0], batch[4] / "manifest.json"))
    pair = out["groups"][0]
    assert pair["correspondence"]["diagnostics"] == []
    assert pair["correspondence"]["unresolved"] == {"before": [], "after": []}
    assert pair["visit_changes"]["added_count"] == 0
    assert sorted(op for r in pair["correspondence"]["relations"] for op in r["operations"]) == [
        "retime"
    ]


def test_incomplete_embedded_chain_retains_valid_aggregate_and_canonical_fallback(pair_case, batch):
    def after(itinerary):
        itinerary["days"][0]["activities"][0].update(
            start_time="2020-01-01T08:00:00Z", end_time="2020-01-01T09:00:00Z"
        )

    def inconsistent(repair):
        repair["rounds"][0]["input_itinerary"]["days"][0]["activities"][0]["title"] = "Wrong source"

    case = pair_case(
        after=after,
        edits=[edit("retime", start_time="2020-01-01T08:00:00Z", end_time="2020-01-01T09:00:00Z")],
        repair_change=inconsistent,
    )
    out = report(case, result_sources=read_v3_result_sources(case[0], batch[4] / "manifest.json"))
    pair = out["groups"][0]
    assert pair["pair_status"] == "available"
    assert pair["deltas"]["auxiliary_total"]["percentage_points"] == 0
    assert pair["correspondence"]["diagnostics"][0]["reason"] == "embedded_lineage_unavailable"
    assert pair["correspondence"]["unresolved"] == {"before": [], "after": []}
    assert any(
        r["basis"] == "unique_independent_canonical_identity"
        for r in pair["correspondence"]["relations"]
    )


def test_opening_improvement_reports_requirement_and_route_regressions(pair_case, batch):
    def after(itinerary):
        itinerary["days"][0]["activities"][0].update(
            start_time="2020-01-01T10:00:00Z", end_time="2020-01-01T10:45:00Z"
        )

    def details(request):
        return {
            "id": request["parameters"]["place_id"],
            "timeZone": {"id": "Etc/UTC"},
            "regularOpeningHours": {
                "periods": [
                    {
                        "open": {"day": 3, "hour": 10, "minute": 0},
                        "close": {"day": 3, "hour": 18, "minute": 0},
                    }
                ]
            },
        }

    obligation = required()
    fixed = {
        "obligation_id": "fixed-a",
        "kind": "fixed_visit_time",
        "resolution": "resolved",
        "subject_ref": "a",
        "date": "2020-01-01",
        "match": "single_visit",
        "conditions": {"start_at": "09:00"},
        "source_refs": obligation["source_refs"],
    }
    case = pair_case(
        after=after,
        edits=[edit("retime", start_time="2020-01-01T10:00:00Z", end_time="2020-01-01T10:45:00Z")],
        obligations=[fixed],
        details_payload=details,
    )
    pair = report(case, result_sources=read_v3_result_sources(case[0], batch[4] / "manifest.json"))[
        "groups"
    ][0]
    opening = next(r for r in pair["continuity"]["opening"] if r["before"]["activity_id"] == "a")
    assert opening["transition"] == "resolved"
    assert opening["before"]["state"] == "FAIL" and opening["after"]["state"] == "PASS"
    requirement = pair["continuity"]["requirements"][0]
    assert requirement["obligation_id"] == "fixed-a" and requirement["transition"] == "regression"
    assert pair["continuity"]["routes"][0]["transition"] == "regression"
    assert pair["deltas"]["dimensions"]["opening"]["verified_score_percentage_points"] == 50


def test_new_overlap_is_traced_by_continued_participants(pair_case, batch):
    def after(itinerary):
        itinerary["days"][0]["activities"][1].update(
            start_time="2020-01-01T09:30:00Z", end_time="2020-01-01T10:30:00Z"
        )

    case = pair_case(
        after=after,
        edits=[
            edit("retime", "b", start_time="2020-01-01T09:30:00Z", end_time="2020-01-01T10:30:00Z")
        ],
    )
    pair = report(case, result_sources=read_v3_result_sources(case[0], batch[4] / "manifest.json"))[
        "groups"
    ][0]
    conflict = next(
        c for c in pair["continuity"]["conflicts"] if c["transition"] == "introduced_conflict"
    )
    assert conflict["before"] is None
    assert conflict["after"]["state"] == "FAIL"
    assert conflict["after"]["seconds"] == 1800
    assert len(conflict["continued_participants"]) == 2


def test_retained_protection_conflict_can_resolve_without_erasing_obligation(pair_case, batch):
    def after(itinerary):
        itinerary["days"][0]["activities"][0].update(
            start_time="2020-01-01T08:00:00Z", end_time="2020-01-01T09:00:00Z"
        )

    case = pair_case(
        after=after,
        edits=[edit("retime", start_time="2020-01-01T08:00:00Z", end_time="2020-01-01T09:00:00Z")],
        obligations=[protection("09:30", "10:00")],
    )
    pair = report(case, result_sources=read_v3_result_sources(case[0], batch[4] / "manifest.json"))[
        "groups"
    ][0]
    conflict = next(
        c
        for c in pair["continuity"]["protection_conflicts"]
        if c["obligation_id"] == "rest" and c["transition"] == "resolved"
    )
    assert conflict["scope"] == "scheduled_commitments"
    assert conflict["before"]["state"] == "FAIL"
    assert conflict["after"] is None
    assert pair["stages"]["final_primary"]["dimensions"]["requirements"]["denominator"] == 1


@pytest.mark.parametrize(
    "scope,state,outcome",
    [("primary_visits", "PASS", "resolved"), ("scheduled_commitments", "UNKNOWN", "unresolved")],
)
def test_controlled_protection_target_resolves_by_original_obligation_id(
    pair_case, scope, state, outcome
):
    from backend.evaluation._controlled_goals import Goal, target_outcome

    def after(itinerary):
        itinerary["days"][0]["activities"][0].update(
            start_time="2020-01-01T08:00:00Z", end_time="2020-01-01T09:00:00Z"
        )

    case = pair_case(after=after, obligations=[protection("09:30", "10:00", scope=scope)])
    pair = report(case)["groups"][0]
    projections = case[0].to_dict()["inventory"][0]["runs"]["v3"]["optional"]
    for label in ("draft", "final_primary"):
        pair["stages"][label]["controlled_projection"] = projections[label]
    goal = Goal.model_validate(
        {
            "goal_id": "respect-rest",
            "basis": "confirmed_conflict",
            "condition": {
                "kind": "check",
                "dimension": "protection_conflicts",
                "obligation_id": "rest",
            },
        }
    )
    result = target_outcome(goal, pair)
    assert result["before"]["state"] == "FAIL"
    assert "resolved" in result["transitions"]
    assert result["after"]["state"] == state
    assert result["independent_outcome"] == outcome

    protected = pair["stages"]["final_primary"]["primary_metrics"]["requirements"]["checks"][0]
    protected["state"] = "UNKNOWN"
    assert target_outcome(goal, pair)["independent_outcome"] == "unresolved"
    protected["state"] = "PASS"

    # A missing protected blocker must never turn conflict absence into verification.
    pair["stages"]["final_primary"]["occupancy"]["blockers"] = []
    assert target_outcome(goal, pair)["independent_outcome"] == "unresolved"


def repeated_before(itinerary):
    extra = copy.deepcopy(itinerary["days"][0]["activities"][0])
    extra.update(
        activity_id="a2", start_time="2020-01-01T12:00:00Z", end_time="2020-01-01T13:00:00Z"
    )
    itinerary["days"][0]["activities"].append(extra)


def retimed_after(itinerary):
    itinerary["days"][0]["activities"][0].update(
        start_time="2020-01-01T08:00:00Z", end_time="2020-01-01T09:00:00Z"
    )


def test_residual_duplicate_venue_is_not_matched_by_greedy_leftover(pair_case):
    case = pair_case(before=repeated_before, after=retimed_after)
    pair = report(case)["groups"][0]
    assert pair["pair_status"] == "available"
    assert pair["deltas"]["auxiliary_total"]["percentage_points"] == 0
    assert len(pair["correspondence"]["unresolved"]["before"]) == 1
    assert len(pair["correspondence"]["unresolved"]["after"]) == 1
    assert any(
        c["transition"] == "unresolved_correspondence" for c in pair["continuity"]["opening"]
    )


def correspondence_review(case, relation="modified"):
    group = case[0].to_dict()["inventory"][0]
    run = group["runs"]["v3"]
    return {
        "schema_version": "rtpeval_v3_correspondence_1",
        "batch_id": "batch",
        "batch_revision": "1",
        "records": [
            {
                "group_id": "g",
                "run_id": "run-v3",
                "result_sha256": run["final"]["context"]["artifact_sha256"],
                "before": [run["optional"]["draft"]["activities"][0]["source"]],
                "after": [run["optional"]["final_primary"]["activities"][0]["source"]],
                "relation": relation,
                "reviewer_ref": "independent-reviewer",
                "reviewed_at": STAMP,
                "rationale": "Source comparison confirms this visit was retimed.",
            }
        ],
    }


def test_evidence_backed_review_resolves_only_remaining_correspondence(pair_case):
    case = pair_case(before=repeated_before, after=retimed_after)
    baseline = report(case)
    out = report(case, correspondence_reviews=correspondence_review(case))
    assert out["status"] == "complete", out["diagnostics"]
    pair = out["groups"][0]
    assert pair["correspondence"]["unresolved"] == {"before": [], "after": []}
    assert pair["deltas"] == baseline["groups"][0]["deltas"]
    assert any(
        r["basis"] == "independent_correspondence_review"
        for r in pair["correspondence"]["relations"]
    )
