"""Offline checks that absence or diagnostics cannot stand in for a transfer."""

import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "transport_inspection", Path(__file__).with_name("inspect_result.py")
)
inspection = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inspection)


def result():
    def activity(key, start, end):
        return {
            "activity_id": key,
            "activity_kind": "main_poi",
            "source_place_id": key,
            "title": key,
            "place_name": key,
            "start_time": f"2026-10-03T{start}:00+02:00",
            "end_time": f"2026-10-03T{end}:00+02:00",
        }

    return {
        "system_version": "v1",
        "itinerary": {
            "destination": "Berlin, Germany",
            "start_date": "2026-10-03",
            "end_date": "2026-10-03",
            "days": [
                {
                    "date": "2026-10-03",
                    "activities": [
                        activity("a", "09:00", "10:00"),
                        activity("b", "11:00", "12:00"),
                    ],
                }
            ],
            "route_diagnostics": [
                {"from_activity_id": "a", "to_activity_id": "b", "result": "PASS"}
            ],
        },
    }


def transfer():
    return {
        "from_activity_id": "a",
        "to_activity_id": "b",
        "origin_place_id": "a",
        "destination_place_id": "b",
        "mode": "WALK",
        "mode_source": "APPLICATION",
        "departure_time": "2026-10-03T10:00:00+02:00",
        "arrival_time": "2026-10-03T10:20:00+02:00",
        "calculation_basis": "provider",
        "validation_state": "PASS",
    }


def test_diagnostic_pass_cannot_replace_missing_transfer():
    assert inspection.inspect(result())["missing_or_invalid_binding_count"] == 1


def test_occurrence_bound_transfer_is_structurally_complete():
    payload = result()
    payload["itinerary"]["transfers"] = [transfer()]
    assert inspection.inspect(payload)["missing_or_invalid_binding_count"] == 0


def test_duplicate_or_wrong_identity_transfer_is_not_complete():
    payload = result()
    payload["itinerary"]["transfers"] = [transfer(), transfer()]
    assert inspection.inspect(payload)["missing_or_invalid_binding_count"] == 1
    payload["itinerary"]["transfers"] = [{**transfer(), "origin_place_id": "different"}]
    assert inspection.inspect(payload)["missing_or_invalid_binding_count"] == 1


def test_model_transport_in_tool_version_fails_source_boundary():
    payload = result()
    payload["itinerary"]["days"][0]["activities"][0]["activity_kind"] = "transport"
    assert inspection.inspect(payload)["transport_source_boundary_passed"] is False
