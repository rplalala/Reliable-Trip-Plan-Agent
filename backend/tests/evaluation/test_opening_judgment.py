"""Missing-hours access assessments through public scorer and offline CLIs."""

import json
import socket

import pytest

from backend.evaluation.opening import score_opening
from backend.tests.evaluation import test_opening as opening_tests
from backend.tests.evaluation import test_requirement_schedule as schedule_tests

pytest_plugins = ("backend.tests.evaluation.test_intake",)
prepared_scenario = schedule_tests.scenario
opening_scenario = opening_tests.opening_scenario


def prepare(opening_scenario, tmp_path, capsys, **scenario):
    from backend.evaluation.opening_judgment_cli import main

    intake, identity, directory, plan, root = opening_scenario(**scenario)
    identity_path = root / "identity.json"
    identity_path.write_text(json.dumps(identity.to_dict()), encoding="utf-8")
    packet_path = tmp_path / "packet.json"
    assert (
        main(
            [
                "prepare",
                str(root / "manifest.json"),
                str(identity_path),
                str(directory),
                "--model",
                "fixture-model",
                "--output",
                str(packet_path),
            ]
        )
        == 0
    )
    capsys.readouterr()
    return intake, identity, directory, packet_path, json.loads(packet_path.read_bytes())


def material(packet, state="PASS", **changes):
    decisions = []
    for case in packet["cases"]:
        activity = case["activity"]
        quote_field = changes.get("activity_field", "notes" if activity["notes"] else "title")
        decisions.append(
            {
                "reference_id": case["reference_id"],
                "state": state,
                "access_mode": "public_outdoor" if state == "PASS" else "ambiguous",
                "intent_basis": "original_activity" if state == "PASS" else "unresolved",
                "venue_category": "public_area",
                "visit_window": "reasonable" if state == "PASS" else "unknown",
                "restrictions": "none_known" if state == "PASS" else "uncertain",
                "rationale": "The original waterfront walk is reasonable in this daytime interval.",
                "activity_field": quote_field,
                "activity_quote": activity[quote_field],
                **changes,
            }
        )
    return {
        "schema_version": "rtpeval_opening_judgment_material_2",
        "packet": packet,
        "request": {
            **packet["request"],
            "max_output_tokens": 3000,
            "store": False,
            "reasoning": {"effort": "medium"},
        },
        "provider": "azure_foundry",
        "requested_at": "2026-10-09T01:00:00Z",
        "retrieved_at": "2026-10-09T01:00:01Z",
        "response": {
            "id": "fixture-response",
            "model": "fixture-model",
            "status": "completed",
            "output": [
                {
                    "type": "message",
                    "role": "assistant",
                    "content": [
                        {"type": "output_text", "text": json.dumps({"decisions": decisions})},
                    ],
                }
            ],
            "usage": {
                "input_tokens": 100,
                "output_tokens": 20,
                "total_tokens": 120,
                "input_tokens_details": {"cached_tokens": 0},
            },
        },
    }


def walks(results):
    for result in results.values():
        for activity in result["itinerary"]["days"][0]["activities"]:
            activity["notes"] = "Walk along the public waterfront and enjoy the harbour views."


def invalid_clocks(results):
    for result in results.values():
        for activity in result["itinerary"]["days"][0]["activities"]:
            activity.update(start_time="invalid", end_time="invalid")


def landmarks(results):
    for result in results.values():
        activities = result["itinerary"]["days"][0]["activities"]
        for index, name in ((0, "City Harbour Bridge"), (2, "Old Waterfront")):
            activities[index].update(title=name, place_name=name, notes="Visit the landmark.")


def test_packet_and_import_ignore_intake_mapping_order(
    opening_scenario, tmp_path, capsys
):
    from backend.evaluation.opening_judgment import prepare_packet

    intake, identity, directory, _, packet = prepare(
        opening_scenario,
        tmp_path,
        capsys,
        change=walks,
        payload={"timeZone": {"id": "Etc/UTC"}},
    )
    reordered = json.loads(json.dumps(intake.to_dict(), sort_keys=True))
    assert len(packet["cases"]) == 8
    assert prepare_packet(reordered, identity, directory, None, model="fixture-model") == packet
    raw = material(packet)
    original_bytes = json.dumps(raw)
    expected = score_opening(intake, identity, directory, opening_judgment=raw).to_dict()
    actual = score_opening(reordered, identity, directory, opening_judgment=raw).to_dict()
    assert actual["status"] == "complete"
    assert actual == expected
    assert json.dumps(raw) == original_bytes


def test_inferred_public_landmark_access_passes_equally_for_all_versions(
    opening_scenario, tmp_path, capsys
):
    intake, identity, directory, _, packet = prepare(
        opening_scenario,
        tmp_path,
        capsys,
        payload={"timeZone": {"id": "Etc/UTC"}, "types": ["tourist_attraction"]},
        change=landmarks,
    )
    report = score_opening(
        intake,
        identity,
        directory,
        opening_judgment=material(
            packet, intent_basis="public_landmark_default", venue_category="public_landmark"
        ),
    ).to_dict()
    assert report["status"] == "complete", report["diagnostics"]
    assert {row["version"] for row in report["results"]} == {"v0", "v1", "v2", "v3"}
    for row in report["results"]:
        check = row["opening"]["checks"][0]
        assert check["state"] == "PASS"
        assert check["access_judgment"]["intent_basis"] == "public_landmark_default"
        assert check["evidence_status"] == "missing"
        assert check["unknown_seconds"] == 3600


@pytest.mark.parametrize("category", ["museum", "indoor_attraction", "other", "unknown"])
def test_nonpublic_venue_cannot_receive_default_exterior_pass(
    opening_scenario, tmp_path, capsys, category
):
    intake, identity, directory, _, packet = prepare(
        opening_scenario,
        tmp_path,
        capsys,
        payload={"timeZone": {"id": "Etc/UTC"}},
    )
    report = score_opening(
        intake,
        identity,
        directory,
        opening_judgment=material(
            packet,
            intent_basis="public_landmark_default",
            venue_category=category,
            access_mode="exterior",
        ),
    ).to_dict()
    assert report["status"] == "needs_material_correction"
    assert report["results"] == []


@pytest.mark.parametrize("types", [None, ["tourist_attraction", "historical_landmark"]])
def test_public_landmark_packet_retains_only_supplied_provider_types(
    opening_scenario, tmp_path, capsys, types
):
    payload = {"timeZone": {"id": "Etc/UTC"}}
    if types is not None:
        payload["types"] = types
    _, _, _, _, packet = prepare(
        opening_scenario,
        tmp_path,
        capsys,
        payload=payload,
        change=landmarks,
    )
    assert all(case["venue"]["types"] == types for case in packet["cases"])


def test_conditional_interior_note_is_preserved_with_default_landmark_judgment(
    opening_scenario, tmp_path, capsys, monkeypatch
):
    from backend.evaluation.opening_judgment_cli import main

    note = "Operating details are unknown; verify if planning interior access."

    def conditional_landmarks(results):
        landmarks(results)
        for result in results.values():
            for activity in result["itinerary"]["days"][0]["activities"]:
                activity["notes"] = note

    _, _, directory, packet_path, packet = prepare(
        opening_scenario,
        tmp_path,
        capsys,
        payload={"timeZone": {"id": "Etc/UTC"}},
        change=conditional_landmarks,
    )
    sent_cases = json.loads(packet["request"]["input"])["cases"]
    assert all(case["activity"]["notes"] == note for case in sent_cases)
    raw = material(packet, intent_basis="public_landmark_default", venue_category="public_landmark")
    material_path = tmp_path / "conditional-material.json"
    material_path.write_text(json.dumps(raw), encoding="utf-8")
    output = tmp_path / "conditional-opening.json"
    monkeypatch.setattr(
        socket, "socket", lambda *a, **k: pytest.fail("Offline import used network")
    )
    assert (
        main(
            [
                "import",
                str(packet_path.parent / "manifest.json"),
                str(tmp_path / "identity.json"),
                str(directory),
                "--material",
                str(material_path),
                "--output",
                str(output),
            ]
        )
        == 0
    )
    capsys.readouterr()
    report = json.loads(output.read_bytes())
    for row in report["results"]:
        check = row["opening"]["checks"][0]
        assert check["state"] == "PASS"
        assert check["access_judgment"]["activity_quote"] == note
        assert check["access_judgment"]["intent_basis"] == "public_landmark_default"


def test_explicit_museum_exterior_does_not_approve_admission(opening_scenario, tmp_path, capsys):
    def outside_only(results):
        for result in results.values():
            for activity in result["itinerary"]["days"][0]["activities"]:
                activity["notes"] = "View the museum facade only; no indoor entry or ticketed tour."

    intake, identity, directory, _, packet = prepare(
        opening_scenario,
        tmp_path,
        capsys,
        payload={"timeZone": {"id": "Etc/UTC"}},
        change=outside_only,
    )
    report = score_opening(
        intake,
        identity,
        directory,
        opening_judgment=material(
            packet,
            intent_basis="original_activity",
            venue_category="museum",
            access_mode="exterior",
        ),
    ).to_dict()
    assert report["status"] == "complete"
    for row in report["results"]:
        check = row["opening"]["checks"][0]
        assert check["state"] == "PASS"
        assert check["access_judgment"]["venue_category"] == "museum"
        assert check["unknown_seconds"] == 3600


@pytest.mark.parametrize(
    "intent,mode",
    [
        ("Enter the museum galleries.", "indoor"),
        ("Take the paid bridge climb with a ticket.", "ticketed"),
    ],
)
def test_explicit_restricted_activity_stays_unknown_without_access_evidence(
    opening_scenario, tmp_path, capsys, intent, mode
):
    def restricted(results):
        for result in results.values():
            for activity in result["itinerary"]["days"][0]["activities"]:
                activity["notes"] = intent

    intake, identity, directory, _, packet = prepare(
        opening_scenario,
        tmp_path,
        capsys,
        payload={"timeZone": {"id": "Etc/UTC"}},
        change=restricted,
    )
    raw = material(
        packet,
        "UNKNOWN",
        access_mode=mode,
        intent_basis="original_activity",
        venue_category="museum" if mode == "indoor" else "public_landmark",
    )
    report = score_opening(intake, identity, directory, opening_judgment=raw).to_dict()
    assert report["status"] == "complete"
    assert all(row["opening"]["counts"]["UNKNOWN"] == 2 for row in report["results"])


def test_unresolved_intent_cannot_pass_and_previous_material_is_stale(
    opening_scenario, tmp_path, capsys
):
    intake, identity, directory, _, packet = prepare(
        opening_scenario,
        tmp_path,
        capsys,
        payload={"timeZone": {"id": "Etc/UTC"}},
        change=landmarks,
    )
    raw = material(packet, intent_basis="unresolved", venue_category="public_landmark")
    assert (
        score_opening(intake, identity, directory, opening_judgment=raw).status
        == "needs_material_correction"
    )
    raw = material(packet)
    raw["schema_version"] = "rtpeval_opening_judgment_material_1"
    assert (
        score_opening(intake, identity, directory, opening_judgment=raw).status
        == "needs_material_correction"
    )


def test_public_walk_can_pass_without_fabricating_api_hours(opening_scenario, tmp_path, capsys):
    intake, identity, directory, _, packet = prepare(
        opening_scenario,
        tmp_path,
        capsys,
        payload={"timeZone": {"id": "Etc/UTC"}},
        change=walks,
    )
    report = score_opening(intake, identity, directory, opening_judgment=material(packet)).to_dict()
    assert report["status"] == "complete", report["diagnostics"]
    opening = opening_tests.first(report)
    check = opening["checks"][0]
    assert check["state"] == "PASS"
    assert check["basis"] == "llm_access_reasonableness"
    assert check["evidence_status"] == "missing"
    assert check["known_open_seconds"] == 0
    assert check["unknown_seconds"] == 3600
    assert opening["llm_decidable_count"] == 2
    assert opening["complete_evidence_count"] == 0
    assert report["rules"]["version"] == "rtpeval_opening_rules_4"


@pytest.mark.parametrize(
    "changes",
    [
        {"access_mode": "indoor"},
        {"access_mode": "ticketed"},
        {"visit_window": "unreasonable"},
        {"restrictions": "applicable_restriction"},
    ],
)
def test_unsupported_access_cannot_be_imported_as_pass(opening_scenario, tmp_path, capsys, changes):
    intake, identity, directory, _, packet = prepare(
        opening_scenario,
        tmp_path,
        capsys,
        payload={"timeZone": {"id": "Etc/UTC"}},
        change=walks,
    )
    report = score_opening(
        intake, identity, directory, opening_judgment=material(packet, **changes)
    ).to_dict()
    assert report["status"] == "needs_material_correction"
    assert report["results"] == []
    accepted = score_opening(
        intake, identity, directory, opening_judgment=material(packet, "UNKNOWN", **changes)
    ).to_dict()
    assert accepted["status"] == "complete"
    assert opening_tests.first(accepted)["checks"][0]["state"] == "UNKNOWN"


@pytest.mark.parametrize(
    "payload,change,names",
    [
        ({"timeZone": {"id": "Etc/UTC"}, "currentOpeningHours": {"periods": []}}, None, ()),
        ({"timeZone": {"id": "Etc/UTC"}, "regularOpeningHours": {"periods": []}}, None, ()),
        ({"timeZone": {"id": "Etc/UTC"}, "regularOpeningHours": {"periods": "invalid"}}, None, ()),
        ({}, None, ()),
        ({"timeZone": {"id": "Etc/UTC"}}, invalid_clocks, ()),
        ({"timeZone": {"id": "Etc/UTC"}}, None, ("Museum A", "Museum B")),
    ],
)
def test_invalid_or_api_decided_visits_are_never_model_cases(
    opening_scenario, tmp_path, capsys, payload, change, names
):
    _, _, _, _, packet = prepare(
        opening_scenario,
        tmp_path,
        capsys,
        payload=payload,
        change=change,
        unresolved_names=names,
    )
    assert packet["cases"] == []


def test_query_instant_status_without_either_schedule_still_allows_access_review(
    opening_scenario,
    tmp_path,
    capsys,
):
    intake, identity, directory, _, packet = prepare(
        opening_scenario,
        tmp_path,
        capsys,
        change=walks,
        payload={"timeZone": {"id": "Etc/UTC"}, "currentOpeningHours": {"openNow": False}},
    )
    assert len(packet["cases"]) == 8
    report = score_opening(intake, identity, directory, opening_judgment=material(packet)).to_dict()
    assert opening_tests.first(report)["checks"][0]["state"] == "PASS"


def test_direct_import_rejects_material_from_another_implementation(
    opening_scenario,
    tmp_path,
    capsys,
):
    intake, identity, directory, _, packet = prepare(
        opening_scenario,
        tmp_path,
        capsys,
        change=walks,
        payload={"timeZone": {"id": "Etc/UTC"}},
    )
    assert "opening.py" in packet["implementation_hashes"]
    packet["implementation_hashes"]["opening.py"] = "0" * 64
    report = score_opening(intake, identity, directory, opening_judgment=material(packet)).to_dict()
    assert report["status"] == "needs_material_correction"
    assert report["results"] == []


@pytest.mark.parametrize(
    "fault",
    [
        "source", "quote", "request_model", "request_input_order", "partial", "foreign",
        "failed", "usage", "timestamp",
    ],
)
def test_foreign_partial_or_malformed_judgments_are_rejected(
    opening_scenario, tmp_path, capsys, fault
):
    intake, identity, directory, _, packet = prepare(
        opening_scenario,
        tmp_path,
        capsys,
        payload={"timeZone": {"id": "Etc/UTC"}},
        change=walks,
    )
    raw = material(packet)
    output = raw["response"]["output"][0]["content"][0]
    decisions = json.loads(output["text"])["decisions"]
    if fault == "source":
        raw["packet"]["cases"][0]["activity"]["notes"] = "Rewritten visit"
    elif fault == "quote":
        decisions[0]["activity_quote"] = "Invented exterior visit"
    elif fault == "request_model":
        raw["request"]["model"] = "foreign-model"
    elif fault == "request_input_order":
        raw["request"]["input"] = json.dumps(
            json.loads(raw["request"]["input"]), indent=2
        )
    elif fault == "partial":
        decisions.pop()
    elif fault == "foreign":
        decisions[0]["reference_id"] = "visit999"
    elif fault == "failed":
        raw["response"]["status"] = "incomplete"
    elif fault == "usage":
        raw["response"]["usage"]["total_tokens"] = 999
    else:
        raw["retrieved_at"] = "2026-10-08T00:00Z"
    output["text"] = json.dumps({"decisions": decisions})
    report = score_opening(intake, identity, directory, opening_judgment=raw).to_dict()
    assert report["status"] == "needs_material_correction"
    assert report["results"] == []


def test_import_and_opening_cli_replay_saved_model_without_network(
    opening_scenario, tmp_path, capsys, monkeypatch
):
    from backend.evaluation.opening_cli import main as opening_cli
    from backend.evaluation.opening_judgment_cli import main

    _, _, directory, packet_path, packet = prepare(
        opening_scenario,
        tmp_path,
        capsys,
        payload={"timeZone": {"id": "Etc/UTC"}},
        change=walks,
    )
    manifest = packet_path.parent / "manifest.json"
    # All fixture source files are written directly in tmp_path by the batch fixture.
    assert manifest.is_file()
    material_path = tmp_path / "material.json"
    material_path.write_text(json.dumps(material(packet)), encoding="utf-8")
    output = tmp_path / "imported.json"
    monkeypatch.setattr(
        socket, "socket", lambda *a, **k: pytest.fail("Offline import constructed a socket")
    )
    base = [str(manifest), str(tmp_path / "identity.json"), str(directory)]
    assert main(["import", *base, "--material", str(material_path), "--output", str(output)]) == 0
    capsys.readouterr()
    expected = json.loads(output.read_bytes())
    assert opening_cli([*base, "--opening-judgment", str(material_path)]) == 0
    actual = json.loads(capsys.readouterr().out)
    actual.pop("preparation_file_sha256")
    assert actual == expected
