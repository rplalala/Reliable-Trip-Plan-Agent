"""Prepare source-linked anonymous material without executing a planner."""

import math
import random
import re
from datetime import datetime, timedelta
from pathlib import Path

from .intake import VERSIONS, _artifact, _read, load_batch
from .records import canonical_digest, require, text

LABELS = ("A", "B", "C", "D")
DIMENSIONS = ("preference", "pace", "usefulness")
INPUT_FIELDS = (
    "destination",
    "start_date",
    "end_date",
    "traveler_count",
    "budget",
    "additional_preferences",
)
ACTIVITY_FIELDS = (
    "title",
    "place_name",
    "location",
    "start_time",
    "end_time",
    "estimated_cost",
    "notes",
)
TRANSFER_FIELDS = (
    "mode",
    "departure_time",
    "arrival_time",
    "provider_duration_seconds",
    "distance_meters",
    "reserve_seconds",
    "unknowns",
    "calculation_basis",
)
LEAK = re.compile(r"\b(?:v[0-3]|rag|google|repair|validation|planner|llm)\b", re.I)


def _config(config, group_ids):
    require(isinstance(config, dict), "config", "Expected presentation configuration")
    require(
        config.get("schema_version") == "rtpeval_human_config_1", "config", "Unsupported config"
    )
    for key in ("public_batch_id", "presentation_id", "rater_ref"):
        require(
            isinstance(config.get(key), str) and re.fullmatch(r"[0-9a-f]{32}", config[key]),
            key,
            "Expected opaque 32-character hexadecimal identifier",
        )
    require(
        type(config.get("revision")) is int and config["revision"] > 0,
        "revision",
        "Expected positive presentation revision",
    )
    require(type(config.get("seed")) is int, "seed", "Expected explicit integer seed")
    require(
        type(config.get("duplicate_min_gap")) is int and config["duplicate_min_gap"] >= 1,
        "duplicate_min_gap",
        "Expected positive duplicate separation",
    )
    tasks = config.get("tasks")
    require(isinstance(tasks, list) and tasks, "tasks", "Explicit nonempty task selection required")
    seen = set()
    for index, task in enumerate(tasks):
        require(
            isinstance(task, dict) and task.get("group_id") in group_ids,
            "tasks",
            "Unknown selected group",
        )
        require(set(task) <= {"group_id", "duplicate_of"}, "tasks", "Unsupported selection field")
        if "duplicate_of" in task:
            original = task["duplicate_of"]
            require(
                type(original) is int and 0 <= original < index,
                "duplicate_of",
                "Expected preceding original task index",
            )
            require(
                "duplicate_of" not in tasks[original]
                and tasks[original]["group_id"] == task["group_id"],
                "duplicate_of",
                "Duplicate must reference its original main group",
            )
            require(
                all(
                    index - earlier - 1 >= config["duplicate_min_gap"]
                    for earlier, selection in enumerate(tasks[:index])
                    if selection["group_id"] == task["group_id"]
                ),
                "duplicate_of",
                "Insufficient duplicate separation",
            )
        else:
            require(
                task["group_id"] not in seen,
                "tasks",
                "Repeated main group requires duplicate marker",
            )
            seen.add(task["group_id"])


def _material(manifest_path, config, replacements=None):
    intake = load_batch(manifest_path).to_dict()
    require(intake["status"] == "accepted", "manifest", "Intake requires material correction")
    path = Path(manifest_path).resolve()
    manifest, digest = _read(path)
    require(
        digest == intake["source_hashes"]["manifest"], "manifest", "Source changed after intake"
    )
    groups = {g["group_id"]: g for g in manifest["groups"]}
    inventory = {g["group_id"]: g for g in intake["inventory"]}
    _config(config, set(groups))
    selected = {t["group_id"] for t in config["tasks"]}
    fields, candidates, sources = [], {}, dict(intake["source_hashes"])

    def display(value, source_key, pointer, source_hash):
        if isinstance(value, str):
            field_ref = source_key + pointer
            fields.append(
                {
                    "field_ref": field_ref,
                    "source_pointer": pointer,
                    "source_sha256": source_hash,
                    "original": value,
                    "original_sha256": canonical_digest(value),
                    "flagged": bool(LEAK.search(value)),
                }
            )
            return (replacements or {}).get(field_ref, value)
        if isinstance(value, list):
            return [
                display(v, source_key, f"{pointer}/{i}", source_hash) for i, v in enumerate(value)
            ]
        if isinstance(value, dict):
            require(set(value) <= {"amount", "currency"}, pointer, "Unsupported display object")
            return {
                k: display(v, source_key, pointer + "/" + k, source_hash) for k, v in value.items()
            }
        require(
            value is None or type(value) in (int, float, bool), pointer, "Unsupported display value"
        )
        return value

    for gid in sorted(selected):
        group = groups[gid]
        original, input_hash = _artifact(path.parent, group["input_ref"])
        require(input_hash == inventory[gid]["input_sha256"], gid, "Input changed after intake")
        sources[gid + "/input"] = input_hash
        request = {
            k: display(original[k], gid + "/input", "/" + k, input_hash)
            for k in INPUT_FIELDS
            if k in original
        }
        plans = {}
        for version in VERSIONS:
            raw, raw_hash = _artifact(path.parent, group["selected_runs"][version]["result_ref"])
            key = gid + "/" + version
            sources[key] = raw_hash
            projection = inventory[gid]["runs"][version]["final"]
            require(
                raw_hash == projection["context"]["artifact_sha256"],
                key,
                "Result changed after intake",
            )
            roles = {a["source"]["pointer"]: a["evaluation_role"] for a in projection["activities"]}
            claims = {
                c["source"]["pointer"]: c for leg in projection["legs"] for c in leg["claims"]
            }
            claims.update({c["source"]["pointer"]: c for c in projection["unbound_transport"]})
            claim_legs = {
                c["source"]["pointer"]: leg for leg in projection["legs"] for c in leg["claims"]
            }
            merged_transfers = {}
            itinerary = raw["itinerary"]
            days = []
            for d, day in enumerate(itinerary["days"]):
                items = []
                for a, activity in enumerate(day["activities"]):
                    base = f"/itinerary/days/{d}/activities/{a}"
                    if version != "v0" and roles[base] == "transport":
                        continue
                    items.append(
                        {
                            "kind": "travel" if roles[base] == "transport" else "activity",
                            "fields": {
                                (
                                    {
                                        "start_time": "departure_time",
                                        "end_time": "arrival_time",
                                    }.get(k, k)
                                    if roles[base] == "transport"
                                    else k
                                ): display(activity[k], key, base + "/" + k, raw_hash)
                                for k in ACTIVITY_FIELDS
                                if k in activity
                            },
                            "notices": ["Transport association uncertain"]
                            if base in claims and claims[base]["association_status"] != "unique"
                            else [],
                        }
                    )
                days.append(
                    {
                        "date": display(day["date"], key, f"/itinerary/days/{d}/date", raw_hash),
                        "items": items,
                    }
                )
            if version != "v0":
                endpoints = {
                    a.get("activity_id"): (a, f"/itinerary/days/{d}/activities/{i}")
                    for d, day in enumerate(itinerary["days"])
                    for i, a in enumerate(day["activities"])
                }
                for t, transfer in enumerate(itinerary.get("transfers", [])):
                    base = f"/itinerary/transfers/{t}"
                    require(
                        isinstance(transfer, dict), base, "Malformed transfer requires correction"
                    )
                    row = {
                        "kind": "travel",
                        "fields": {
                            {"provider_duration_seconds": "duration_seconds"}.get(k, k): display(
                                transfer[k], key, base + "/" + k, raw_hash
                            )
                            for k in TRANSFER_FIELDS
                            if k in transfer
                        },
                        "notices": [],
                    }
                    for reference, field in (
                        ("from_activity_id", "referenced_origin"),
                        ("to_activity_id", "referenced_destination"),
                    ):
                        endpoint = endpoints.get(transfer.get(reference))
                        if endpoint:
                            activity, pointer = endpoint
                            name = "place_name" if text(activity.get("place_name")) else "title"
                            if text(activity.get(name)):
                                row["fields"][field] = display(
                                    activity[name], key, pointer + "/" + name, raw_hash
                                )
                    if not transfer.get("arrival_time"):
                        inferred = _inferred_arrival(transfer)
                        if inferred:
                            row["fields"]["inferred_arrival"] = inferred
                            row["notices"].append(
                                "Arrival not supplied; inferred time is display arithmetic only"
                            )
                        else:
                            row["notices"].append("Arrival not supplied; inference unavailable")
                    claim = claims.get(base)
                    if claim is None or claim["association_status"] != "unique":
                        row["notices"].append("Transport association uncertain")
                    leg = claim_legs.get(base)
                    if leg and leg["journey"]["agreement"] == "conflicting":
                        row["notices"].append(
                            "Conflicting transport claims; no alternative selected"
                        )
                    departure = transfer.get("departure_time")
                    day_index = next(
                        (
                            i
                            for i, day in enumerate(itinerary["days"])
                            if isinstance(departure, str)
                            and departure.startswith(day["date"] + "T")
                        ),
                        None,
                    )
                    if day_index is None:
                        day_index = next(
                            (
                                i
                                for i, day in enumerate(itinerary["days"])
                                if any(
                                    a.get("activity_id") == transfer.get("from_activity_id")
                                    for a in day["activities"]
                                )
                            ),
                            0,
                        )
                        row["notices"].append("Displayed day association uncertain")
                    identity = None
                    if (
                        claim
                        and claim["association_status"] == "unique"
                        and leg
                        and transfer.get("departure_time")
                    ):
                        identity = canonical_digest(
                            [
                                leg["from_source"],
                                leg["to_source"],
                                transfer.get("mode"),
                                transfer.get("departure_time"),
                                transfer.get("arrival_time"),
                                transfer.get("provider_duration_seconds")
                                if not transfer.get("arrival_time")
                                else None,
                            ]
                        )
                    if identity in merged_transfers:
                        target = merged_transfers[identity]
                        for field, value in row["fields"].items():
                            if field not in target["fields"]:
                                target["fields"][field] = value
                            elif target["fields"][field] != value:
                                old = target["fields"][field]
                                values = old if isinstance(old, list) else [old]
                                for extra in value if isinstance(value, list) else [value]:
                                    if extra not in values:
                                        values.append(extra)
                                target["fields"][field] = values
                        target["notices"] = list(dict.fromkeys(target["notices"] + row["notices"]))
                    else:
                        days[day_index]["items"].append(row)
                        if identity:
                            merged_transfers[identity] = row
            for day in days:
                clocks = [
                    i["fields"].get("start_time", i["fields"].get("departure_time"))
                    for i in day["items"]
                ]
                try:
                    parsed = [datetime.fromisoformat(c) for c in clocks]
                    indexed = sorted(
                        zip(parsed, day["items"], strict=True), key=lambda pair: pair[0]
                    )
                    day["items"] = [item for _, item in indexed]
                except (ValueError, TypeError):
                    for item in day["items"]:
                        item["notices"].append(
                            "Chronological ordering unavailable; source order retained"
                        )
            plans[version] = {"days": days}
        candidates[gid] = {"input": request, "plans": plans}
    prepared = {
        "schema_version": "rtpeval_human_preparation_1",
        "config": config,
        "source_hashes": sources,
        "source_batch": {"batch_id": intake["batch_id"], "revision": intake["revision"]},
        "groups": candidates,
        "fields": fields,
    }
    prepared["preparation_hash"] = canonical_digest(prepared)
    return prepared


def _inferred_arrival(transfer):
    duration = transfer.get("provider_duration_seconds")
    clock = transfer.get("departure_time")
    if not isinstance(clock, str) or not re.match(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}", clock):
        return None
    if type(duration) not in (int, float) or not math.isfinite(duration) or duration < 0:
        return None
    try:
        departure = datetime.fromisoformat(clock)
        return (departure + timedelta(seconds=duration)).isoformat()
    except (KeyError, ValueError, TypeError, OverflowError):
        return None


def prepare_human_material(manifest_path, config):
    """Return researcher-only prospective content and exact source-linked review fields."""
    return _material(manifest_path, config)


def _review(prepared, review):
    require(isinstance(review, dict), "review", "Expected review object")
    require(
        review.get("schema_version") == "rtpeval_human_display_reviews_1"
        and review.get("preparation_hash") == prepared["preparation_hash"]
        and review.get("preserves_facts_and_uncertainty") is True
        and text(review.get("reviewer_ref")),
        "review",
        "A complete source-linked review is required",
    )
    try:
        require(
            datetime.fromisoformat(review["reviewed_at"]).utcoffset() is not None,
            "reviewed_at",
            "Expected offset-aware review timestamp",
        )
    except (KeyError, TypeError, ValueError) as exc:
        require(False, "reviewed_at", f"Invalid review timestamp: {exc}")
    fields = {f["field_ref"]: f for f in prepared["fields"]}
    replacements, exemptions = {}, set()
    for array, destination in (("redactions", replacements), ("allowed_flags", exemptions)):
        require(isinstance(review.get(array), list), array, "Expected review decisions array")
        for decision in review[array]:
            require(isinstance(decision, dict), array, "Expected review decision")
            ref = decision.get("field_ref")
            require(
                ref in fields and ref not in destination, array, "Unknown/duplicate source field"
            )
            field = fields[ref]
            require(
                all(decision.get(k) == field[k] for k in ("source_sha256", "original_sha256")),
                ref,
                "Review source linkage mismatch",
            )
            require(text(decision.get("reason")), ref, "Review rationale required")
            if array == "redactions":
                require(text(decision.get("display_text")), ref, "Redacted display text required")
                replacements[ref] = decision["display_text"]
            else:
                exemptions.add(ref)
    for ref, field in fields.items():
        candidate = replacements.get(ref, field["original"])
        require(
            not LEAK.search(candidate) or ref in exemptions,
            ref,
            "Unresolved presentation leakage requires researcher correction",
        )
    return replacements


def build_human_package(manifest_path, config, display_review):
    """Re-read linked source bytes and produce separate public and private artifacts."""
    prepared = prepare_human_material(manifest_path, config)
    replacements = _review(prepared, display_review)
    displayed = _material(manifest_path, config, replacements)
    require(
        displayed["source_hashes"] == prepared["source_hashes"],
        "source",
        "Source changed during review",
    )
    public_tasks, private_tasks = [], []
    rng = random.Random(config["seed"])
    schedule = []
    while len(schedule) < len(config["tasks"]):
        versions = list(VERSIONS)
        rng.shuffle(versions)
        shifts = list(range(4))
        rng.shuffle(shifts)
        schedule.extend(
            dict(zip(LABELS, versions[shift:] + versions[:shift], strict=True)) for shift in shifts
        )
    for index, selection in enumerate(config["tasks"]):
        candidate = displayed["groups"][selection["group_id"]]
        task_id = f"task-{index + 1}"
        labels = schedule[index]
        public_tasks.append(
            {
                "task_id": task_id,
                "input": candidate["input"],
                "plans": {label: candidate["plans"][v] for label, v in labels.items()},
            }
        )
        private_tasks.append({"task_id": task_id, **selection, "labels": labels})
    public = {
        "schema_version": "rtpeval_human_package_1",
        "batch_id": config["public_batch_id"],
        "batch_revision": config["revision"],
        "presentation_id": config["presentation_id"],
        "rater_ref": config["rater_ref"],
        "dimensions": list(DIMENSIONS),
        "tasks": public_tasks,
    }
    public["presentation_hash"] = canonical_digest(public)
    private = {
        "schema_version": "rtpeval_human_mapping_1",
        "public_sha256": canonical_digest(public),
        "preparation": prepared,
        "display_review": display_review,
        "tasks": private_tasks,
        "assignment_policy": "seeded_shuffled_latin_blocks_1",
        "position_counts": {
            population: {
                v: {
                    label: sum(
                        t["labels"][label] == v
                        for t in private_tasks
                        if population == "combined"
                        or ("duplicate_of" in t) == (population == "duplicate")
                    )
                    for label in LABELS
                }
                for v in VERSIONS
            }
            for population in ("main", "duplicate", "combined")
        },
    }
    private["content_hash"] = canonical_digest(private)
    return {"public": public, "private": private}
