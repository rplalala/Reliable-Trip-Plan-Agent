"""Anonymous package acceptance through delivered local material."""

import copy
import json
from collections import Counter

import pytest

from backend.evaluation.human_tasks import build_human_package, prepare_human_material
from backend.evaluation.records import MaterialError

pytest_plugins = ("backend.tests.evaluation.test_intake",)


def config(tasks=None):
    return {
        "schema_version": "rtpeval_human_config_1",
        "public_batch_id": "1" * 32,
        "presentation_id": "2" * 32,
        "rater_ref": "3" * 32,
        "revision": 1,
        "seed": 17,
        "duplicate_min_gap": 1,
        "tasks": tasks or [{"group_id": "g"}],
    }


def review(prepared):
    return {
        "schema_version": "rtpeval_human_display_reviews_1",
        "preparation_hash": prepared["preparation_hash"],
        "reviewer_ref": "researcher",
        "reviewed_at": "2026-10-02T10:00:00+10:00",
        "preserves_facts_and_uncertainty": True,
        "redactions": [],
        "allowed_flags": [],
    }


def package(batch):
    _, _, write, _, _ = batch
    path = write()
    prepared = prepare_human_material(path, config())
    return build_human_package(path, config(), review(prepared))


def test_reviewed_batch_produces_four_anonymous_plans_without_private_metadata(batch):
    result = package(batch)
    public, private = result["public"], result["private"]
    task = public["tasks"][0]
    assert task["input"]["additional_preferences"] == "Prefer architecture"
    assert list(task["plans"]) == ["A", "B", "C", "D"]
    assert all(plan["days"][0]["date"] == "2020-01-01" for plan in task["plans"].values())
    assert public["batch_id"] == "1" * 32
    assert "seed" not in public and "group_id" not in task
    assert set(private["tasks"][0]["labels"].values()) == {"v0", "v1", "v2", "v3"}


def test_metadata_text_blocks_delivery_until_source_linked_redaction(batch):
    _, results, write, _, root = batch
    results["v3"]["itinerary"]["days"][0]["activities"][0]["notes"] = "V3 repaired; time uncertain"
    path = write("v3")
    original = (root / "v3.json").read_bytes()
    prepared = prepare_human_material(path, config())
    reviewed = review(prepared)
    with pytest.raises(MaterialError, match="leakage"):
        build_human_package(path, config(), reviewed)
    field = next(f for f in prepared["fields"] if f["original"] == "V3 repaired; time uncertain")
    reviewed["redactions"] = [
        {**field, "display_text": "Time uncertain", "reason": "Remove version marker"}
    ]
    result = build_human_package(path, config(), reviewed)
    encoded = json.dumps(result["public"])
    assert "Time uncertain" in encoded and "V3 repaired" not in encoded
    assert (root / "v3.json").read_bytes() == original
    stale = copy.deepcopy(reviewed)
    stale["redactions"][0]["source_sha256"] = "0" * 64
    with pytest.raises(MaterialError, match="source"):
        build_human_package(path, config(), stale)


def test_unbound_transfer_is_visible_with_labelled_display_only_arrival(batch):
    _, results, write, _, _ = batch
    results["v1"]["itinerary"]["transfers"] = [
        {
            "from_activity_id": "missing",
            "to_activity_id": "b",
            "mode": "WALK",
            "departure_time": "2020-01-01T23:50:00+10:00",
            "provider_duration_seconds": 1800,
            "reserve_seconds": 300,
            "unknowns": ["Travel time uncertain"],
            "calculation_basis": "Estimated duration",
            "validation_state": "UNKNOWN",
        }
    ]
    path = write("v1")
    before = path.parent.joinpath("v1.json").read_bytes()
    prepared = prepare_human_material(path, config())
    result = build_human_package(path, config(), review(prepared))
    label = next(k for k, v in result["private"]["tasks"][0]["labels"].items() if v == "v1")
    items = result["public"]["tasks"][0]["plans"][label]["days"][0]["items"]
    transfer = next(i for i in items if i["kind"] == "travel")
    assert transfer["fields"]["inferred_arrival"] == "2020-01-02T00:20:00+10:00"
    assert transfer["fields"].get("arrival_time") is None
    assert "Arrival not supplied; inferred time is display arithmetic only" in transfer["notices"]
    assert "Transport association uncertain" in transfer["notices"]
    assert transfer["fields"]["unknowns"] == ["Travel time uncertain"]
    assert transfer["fields"]["referenced_destination"] == "Museum B"
    assert "referenced_origin" not in transfer["fields"]
    assert "Walking" not in json.dumps(items)
    assert "validation_state" not in json.dumps(result["public"])
    assert path.parent.joinpath("v1.json").read_bytes() == before


def expand(batch, count):
    manifest, _, write, save, root = batch
    write()
    template = copy.deepcopy(manifest["groups"][0])
    for i in range(1, count):
        group = copy.deepcopy(template)
        group["group_id"] = f"g{i}"
        spec = json.loads((root / "requirements.json").read_text())
        spec["group_id"] = group["group_id"]
        group["requirement_spec_ref"] = save(f"requirements-{i}.json", spec, spec["schema_version"])
        for v, run in group["selected_runs"].items():
            run["run_id"] = f"run-{i}-{v}"
            for field in ("usage_ref", "provenance_ref"):
                envelope = json.loads((root / run[field]["path"]).read_text())
                envelope.update(group_id=group["group_id"], run_id=run["run_id"])
                run[field] = save(f"{i}-{field}-{v}.json", envelope, envelope["schema_version"])
        manifest["groups"].append(group)
        manifest["selected_group_ids"].append(group["group_id"])
    return write()


def test_frozen_balanced_assignment_includes_spaced_duplicate_without_public_marker(batch):
    path = expand(batch, 5)
    selections = [{"group_id": g} for g in ("g", "g1", "g2", "g3", "g4")]
    selections.append({"group_id": "g", "duplicate_of": 0})
    cfg = config(selections)
    prepared = prepare_human_material(path, cfg)
    first = build_human_package(path, cfg, review(prepared))
    assert first == build_human_package(path, cfg, review(prepared))
    for v in ("v0", "v1", "v2", "v3"):
        counts = Counter(
            label
            for task in first["private"]["tasks"]
            for label, version in task["labels"].items()
            if version == v
        )
        assert sorted(counts.values()) == [1, 1, 2, 2]
    assert "duplicate_of" not in json.dumps(first["public"])
    assert first["private"]["tasks"][-1]["duplicate_of"] == 0


@pytest.mark.parametrize(
    "tasks",
    [
        [{"group_id": "g"}, {"group_id": "g"}],
        [{"group_id": "g"}, {"group_id": "g", "duplicate_of": 0}],
        [{"group_id": "g", "duplicate_of": 5}],
    ],
)
def test_invalid_duplicate_selection_is_material_error_not_reduced_cohort(batch, tasks):
    _, _, write, _, _ = batch
    with pytest.raises(MaterialError):
        prepare_human_material(write(), config(tasks))


def test_duplicate_journey_retains_distinct_uncertainty_once_and_conflict_stays_separate(batch):
    _, results, write, _, _ = batch
    transport = {
        "from_activity_id": "a",
        "to_activity_id": "b",
        "mode": "WALK",
        "departure_time": "2020-01-01T10:00:00+00:00",
        "arrival_time": "2020-01-01T10:20:00+00:00",
        "provider_duration_seconds": 1200,
        "unknowns": ["Estimated duration"],
    }
    second = {**transport, "unknowns": ["Access uncertain"]}
    results["v1"]["itinerary"]["transfers"] = [transport, second, copy.deepcopy(second)]
    path = write("v1")
    material = build_human_package(path, config(), review(prepare_human_material(path, config())))
    label = next(k for k, v in material["private"]["tasks"][0]["labels"].items() if v == "v1")
    items = material["public"]["tasks"][0]["plans"][label]["days"][0]["items"]
    transfers = [i for i in items if i["kind"] == "travel"]
    assert len(transfers) == 1
    assert transfers[0]["fields"]["unknowns"] == ["Estimated duration", "Access uncertain"]
    second["arrival_time"] = "2020-01-01T10:25:00+00:00"
    results["v1"]["itinerary"]["transfers"] = [transport, second]
    path = write("v1")
    material = build_human_package(path, config(), review(prepare_human_material(path, config())))
    transfers = [
        i
        for i in material["public"]["tasks"][0]["plans"][label]["days"][0]["items"]
        if i["kind"] == "travel"
    ]
    assert len(transfers) == 2
    assert all(
        "Conflicting transport claims; no alternative selected" in t["notices"] for t in transfers
    )


@pytest.mark.parametrize(
    "duration,departure",
    [
        (None, "2020-01-01T10:00:00+00:00"),
        (True, "bad"),
        (-2, "bad"),
        (60, "bad"),
        (60, "2020-01-01"),
    ],
)
def test_missing_or_invalid_operands_do_not_invent_arrival(batch, duration, departure):
    _, results, write, _, _ = batch
    results["v2"]["itinerary"]["transfers"] = [
        {"mode": "WALK", "departure_time": departure, "provider_duration_seconds": duration}
    ]
    path = write("v2")
    material = build_human_package(path, config(), review(prepare_human_material(path, config())))
    encoded = json.dumps(material["public"])
    assert "inferred_arrival" not in encoded
    assert "inference unavailable" in encoded


def test_transport_display_uses_one_neutral_shape_and_keeps_private_batch_alias(batch):
    _, results, write, _, _ = batch
    results["v1"]["itinerary"]["transfers"] = [
        {
            "from_activity_id": "a",
            "to_activity_id": "b",
            "mode": "WALK",
            "departure_time": "2020-01-01T10:00:00+00:00",
            "arrival_time": "2020-01-01T10:20:00+00:00",
            "provider_duration_seconds": 1200,
        }
    ]
    path = write("v1")
    material = build_human_package(path, config(), review(prepare_human_material(path, config())))
    public = material["public"]
    for version in ("v0", "v1"):
        label = next(
            k for k, v in material["private"]["tasks"][0]["labels"].items() if v == version
        )
        rows = public["tasks"][0]["plans"][label]["days"][0]["items"]
        travel = next(row for row in rows if row["kind"] == "travel")
        assert travel["fields"]["departure_time"] == "2020-01-01T10:00:00+00:00"
        assert travel["fields"]["arrival_time"] == "2020-01-01T10:20:00+00:00"
    assert "provider_duration_seconds" not in json.dumps(public)
    assert material["private"]["preparation"]["source_batch"] == {
        "batch_id": "batch",
        "revision": "1",
    }
