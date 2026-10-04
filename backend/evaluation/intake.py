"""Read a delivered batch without executing planners, models or providers."""

import hashlib
import json
import math
from datetime import date
from pathlib import Path

from .projection import project
from .records import IntakeResult, MaterialError, freeze, require, text

VERSIONS = ("v0", "v1", "v2", "v3")


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _constant(value):
    raise ValueError(f"Nonfinite JSON constant: {value}")


def _float(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("Nonfinite JSON number")
    return number


def _read(path):
    try:
        raw = path.read_bytes()
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_pairs,
            parse_constant=_constant,
            parse_float=_float,
        )
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        raise MaterialError("artifact_integrity_error", path.name, str(exc)) from exc
    require(isinstance(value, dict), path.name, "Artifact must be a JSON object")
    return value, hashlib.sha256(raw).hexdigest()


def _artifact(root, ref, schema=None):
    require(isinstance(ref, dict), "artifact_ref", "Missing artifact reference")
    name = ref.get("path")
    require(text(name), "artifact_ref/path", "Missing relative artifact path")
    relative = Path(name)
    require(not relative.is_absolute() and not relative.drive, name, "Absolute path is forbidden")
    path = (root / relative).resolve()
    require(path.is_relative_to(root), name, "Artifact path escapes batch root")
    require(ref.get("media_type") == "application/json", name, "Unsupported media type")
    require(ref.get("availability") == "available", name, "Required envelope must be present")
    value, digest = _read(path)
    require(ref.get("sha256") == digest, name, "Artifact hash mismatch")
    if schema:
        require(
            value.get("schema_version") == schema,
            name,
            "Unsupported artifact schema",
            "unsupported_wire_version",
        )
        require(ref.get("schema_version") == schema, name, "Reference schema mismatch")
    elif ref.get("schema_version") is not None:
        require(
            ref["schema_version"] == value.get("input_version"),
            name,
            "Unsupported declared wire version",
            "unsupported_wire_version",
        )
    return value, digest


def _input(value):
    require(
        value.get("input_version") == "planning_request_2",
        "input",
        "Unsupported input version",
        "unsupported_wire_version",
    )
    require(text(value.get("destination")), "input/destination", "Missing destination")
    try:
        start = date.fromisoformat(value.get("start_date", ""))
        end = date.fromisoformat(value.get("end_date", ""))
        require(start <= end, "input", "Reversed request dates")
    except (ValueError, TypeError) as exc:
        raise MaterialError("artifact_integrity_error", "input", "Invalid request dates") from exc
    require(
        type(value.get("traveler_count")) is int and value["traveler_count"] > 0,
        "input/traveler_count",
        "Expected positive traveler count",
    )
    require(isinstance(value.get("budget"), dict), "input/budget", "Missing budget object")
    # No current-date window, request interpreter or provider validation is invoked.


def _requirements(spec, group_id, input_hash, original):
    require(
        spec.get("group_id") == group_id and spec.get("input_sha256") == input_hash,
        "requirement_spec",
        "RequirementSpec input/group mismatch",
    )
    review = spec.get("review")
    require(
        isinstance(review, dict)
        and review.get("status") == "reviewed"
        and text(review.get("reviewer_ref"))
        and text(review.get("reviewed_at")),
        "requirement_spec/review",
        "An explicit reviewed RequirementSpec is required",
    )
    for field in ("spec_id", "revision"):
        require(
            text(spec.get(field)), "requirement_spec/" + field, "Missing specification identity"
        )
    for field in ("subjects", "obligations", "soft_preferences", "unresolved_items"):
        require(isinstance(spec.get(field), list), "requirement_spec/" + field, "Expected array")
    subjects = set()
    for subject in spec["subjects"]:
        require(
            isinstance(subject, dict) and text(subject.get("subject_id")),
            "subjects",
            "Missing subject identity",
        )
        require(subject["subject_id"] not in subjects, "subjects", "Duplicate subject ID")
        subjects.add(subject["subject_id"])
    ids = set()
    for obligation in spec["obligations"]:
        require(isinstance(obligation, dict), "obligations", "Expected obligation object")
        oid = obligation.get("obligation_id")
        require(text(oid) and oid not in ids, "obligations", "Invalid/duplicate obligation ID")
        ids.add(oid)
        require(text(obligation.get("kind")), oid, "Missing obligation kind")
        if obligation.get("kind") in ("required_visit", "excluded_visit"):
            require(obligation.get("subject_ref") in subjects, oid, "Unknown requirement subject")
        require(
            obligation.get("resolution") in ("resolved", "unresolved", "unsupported"),
            oid,
            "Missing obligation resolution",
        )
        refs = obligation.get("source_refs")
        require(
            isinstance(refs, list) and bool(refs), oid, "Obligation needs original-input sources"
        )
        for ref in refs:
            require(isinstance(ref, dict), oid, "Invalid source reference")
            field = ref.get("field_path")
            require(text(field) and field in original, oid, "Unknown original input field")
            if "quote" in ref:
                quote, value = ref["quote"], original[field]
                occurrence = ref.get("occurrence", 0)
                require(
                    text(quote)
                    and isinstance(value, str)
                    and type(occurrence) is int
                    and occurrence >= 0,
                    oid,
                    "Invalid quote source",
                )
                positions, offset = [], 0
                while (offset := value.find(quote, offset)) >= 0:
                    positions.append(offset)
                    offset += len(quote)
                require(occurrence < len(positions), oid, "Quote occurrence is absent from input")
                if "offset_start" in ref or "offset_end" in ref:
                    require(
                        ref.get("offset_start") == positions[occurrence]
                        and ref.get("offset_end") == positions[occurrence] + len(quote),
                        oid,
                        "Quote offsets do not match original Unicode code points",
                    )


def _reviews(root, manifest, hashes):
    if "projection_reviews_ref" not in manifest:
        return []
    value, digest = _artifact(root, manifest["projection_reviews_ref"], "rtpeval_reviews_1")
    hashes["projection_reviews"] = digest
    require(value.get("batch_id") == manifest["batch_id"], "reviews", "Review batch mismatch")
    records = value.get("records")
    require(isinstance(records, list), "reviews", "Expected review array")
    keys = set()
    for review in records:
        require(isinstance(review, dict), "reviews", "Expected review object")
        fields = (
            "group_id",
            "run_id",
            "artifact_sha256",
            "pointer",
            "reviewer_ref",
            "reviewed_at",
            "rationale",
            "revision",
        )
        require(all(text(review.get(k)) for k in fields), "reviews", "Incomplete review provenance")
        key = tuple(review[k] for k in fields[:4])
        require(key not in keys, "reviews", "Duplicate review decision")
        keys.add(key)
        if "role" in review:
            require(
                review["role"] in {"primary_visit", "transport", "transition", "unresolved"},
                "reviews",
                "Unsupported role",
            )
        if "mode" in review:
            require(review["mode"] in ("WALK", "TRANSIT", "DRIVE", None), "reviews", "Invalid mode")
        require(
            ("from_activity_id" in review) == ("to_activity_id" in review),
            "reviews",
            "Both reviewed transport endpoints are required",
        )
    return records


def load_batch(manifest_path):
    """Read-only public entry point. A fatal error never returns a partial cohort."""
    diagnostics, inventory, hashes = [], [], {}
    try:
        path = Path(manifest_path).resolve()
        root = path.parent
        manifest, hashes["manifest"] = _read(path)
        require(
            manifest.get("schema_version") == "rtpeval_batch_1",
            "manifest",
            "Unsupported batch schema",
            "unsupported_wire_version",
        )
        for key in ("batch_id", "revision", "created_at", "qualification_policy_ref"):
            require(text(manifest.get(key)), "manifest/" + key, "Missing manifest field")
        selected, groups = manifest.get("selected_group_ids"), manifest.get("groups")
        require(
            isinstance(selected, list) and bool(selected) and all(text(g) for g in selected),
            "selected_group_ids",
            "Expected a nonempty group selection",
        )
        require(len(set(selected)) == len(selected), "selected_group_ids", "Duplicate group IDs")
        require(
            isinstance(groups, list) and len(groups) == len(selected),
            "groups",
            "Groups must match selected membership",
        )
        require(all(isinstance(g, dict) for g in groups), "groups", "Invalid group object")
        require(
            [g.get("group_id") for g in groups] == selected,
            "groups",
            "Manifest groups must match selected IDs in order",
        )
        reviews = _reviews(root, manifest, hashes)
        consumed_reviews, run_ids = set(), set()
        for group in groups:
            gid = group["group_id"]
            require(
                group.get("completion_attested") is True,
                gid,
                "Producer completion attestation required; Evaluation does not requalify",
            )
            original, input_hash = _artifact(root, group.get("input_ref"))
            require(
                original.get("input_version") == "planning_request_2",
                gid,
                "Unsupported input version",
                "unsupported_wire_version",
            )
            _input(original)
            spec, spec_hash = _artifact(
                root, group.get("requirement_spec_ref"), "rtpeval_requirements_1"
            )
            _requirements(spec, gid, input_hash, original)
            runs = group.get("selected_runs")
            require(
                isinstance(runs, dict) and set(runs) == set(VERSIONS),
                gid,
                "Exactly four selected versions required",
            )
            projected = {}
            for version in VERSIONS:
                run = runs[version]
                require(isinstance(run, dict), gid, "Expected selected run object")
                rid = run.get("run_id")
                require(text(rid) and rid not in run_ids, gid, "Missing/duplicate selected run ID")
                run_ids.add(rid)
                result, result_hash = _artifact(root, run.get("result_ref"))
                require(result.get("system_version") == version, rid, "Result version mismatch")
                provenance, provenance_hash = _artifact(
                    root, run.get("provenance_ref"), "rtpeval_provenance_1"
                )
                require(
                    tuple(
                        provenance.get(k)
                        for k in ("group_id", "run_id", "version", "input_sha256", "result_sha256")
                    )
                    == (gid, rid, version, input_hash, result_hash),
                    rid,
                    "Provenance input/result/run association mismatch",
                )
                usage, usage_hash = _artifact(root, run.get("usage_ref"), "rtpeval_usage_1")
                require(
                    (
                        usage.get("group_id"),
                        usage.get("version"),
                        usage.get("run_id"),
                        usage.get("result_sha256"),
                    )
                    == (gid, version, rid, result_hash),
                    rid,
                    "Usage/result association mismatch",
                )
                require(
                    usage.get("collection_status") in ("available", "partial", "unavailable"),
                    rid,
                    "Explicit usage collection status required",
                )
                context = {
                    "batch_id": manifest["batch_id"],
                    "group_id": gid,
                    "run_id": rid,
                    "artifact_sha256": result_hash,
                }
                relevant = []
                for index, review in enumerate(reviews):
                    if (review["group_id"], review["run_id"], review["artifact_sha256"]) == (
                        gid,
                        rid,
                        result_hash,
                    ):
                        relevant.append(review)
                        consumed_reviews.add(index)
                final = project(
                    result.get("itinerary"),
                    context,
                    reviews=[r for r in relevant if r["pointer"].startswith("/itinerary/")],
                    version=version,
                )
                require(
                    version == "v3"
                    or all(r["pointer"].startswith("/itinerary/") for r in relevant),
                    rid,
                    "Only V3 can have reviewed draft projections",
                )
                optional = {}
                v3 = result.get("v3")
                for key in ("draft", "final_primary") if version == "v3" else ():
                    prefix = "/v3/" + key
                    try:
                        optional[key] = project(
                            v3.get(key) if isinstance(v3, dict) else None,
                            context,
                            prefix,
                            [r for r in relevant if r["pointer"].startswith(prefix + "/")],
                            version=version,
                        )
                    except (MaterialError, TypeError, KeyError, ValueError) as exc:
                        optional[key] = None
                        diagnostics.append(
                            {
                                "reason": "optional_projection_unavailable",
                                "run_id": rid,
                                "projection": prefix,
                                "details": exc.diagnostic
                                if isinstance(exc, MaterialError)
                                else {
                                    "reason": "invalid_optional_structure",
                                    "explanation": str(exc),
                                },
                            }
                        )
                require(
                    all(
                        r["pointer"].startswith(("/itinerary/", "/v3/draft/", "/v3/final_primary/"))
                        for r in relevant
                    ),
                    rid,
                    "Review points outside an itinerary projection",
                )
                for field in ("destination", "start_date", "end_date"):
                    if final["header"][field] != original.get(field):
                        final["diagnostics"].append(
                            {"reason": "request_output_discrepancy", "field": field, "run_id": rid}
                        )
                projected[version] = {
                    "final": final,
                    "optional": optional,
                    "provenance_hash": provenance_hash,
                    "usage_hash": usage_hash,
                    "usage_available": usage["collection_status"] != "unavailable",
                    "paired_available": bool(optional) and all(optional.values()),
                }
            inventory.append(
                {
                    "group_id": gid,
                    "input": original,
                    "input_sha256": input_hash,
                    "requirement_spec": spec,
                    "requirement_spec_sha256": spec_hash,
                    "protected_intervals": [
                        o for o in spec["obligations"] if o.get("kind") == "protected_time"
                    ],
                    "runs": projected,
                }
            )
        require(consumed_reviews == set(range(len(reviews))), "reviews", "Stale/unlinked reviews")
    except (MaterialError, TypeError, KeyError, OverflowError, ValueError, OSError) as exc:
        detail = (
            exc.diagnostic
            if isinstance(exc, MaterialError)
            else {
                "reason": "artifact_integrity_error",
                "pointer": "manifest",
                "explanation": f"Invalid delivery structure: {exc}",
            }
        )
        return IntakeResult(
            "needs_material_correction",
            freeze(
                {
                    "material_diagnostics": [detail],
                    "inventory": [],
                    "projection_diagnostics": [],
                    "track_availability": {"quality_preparation": False},
                }
            ),
        )
    return IntakeResult(
        "accepted",
        freeze(
            {
                "batch_id": manifest["batch_id"],
                "revision": manifest["revision"],
                "source_hashes": hashes,
                "material_diagnostics": [],
                "inventory": inventory,
                "projection_diagnostics": diagnostics,
                "track_availability": {"quality_preparation": True, "scoring_implemented": False},
            }
        ),
    )
