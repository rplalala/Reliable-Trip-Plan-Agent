"""Independent draft/final-primary diagnostics for selected V3 runs."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from pathlib import Path

from ._v3_continuity import build_continuity
from .intake import _read
from .opening import score_opening
from .preparation import identity_ready
from .quality_aggregation import DIMENSIONS, _dimension, _fraction, _grounding, _index, _totals
from .records import MaterialError, canonical_digest, freeze, require, thaw
from .requirement_schedule import score_requirement_schedule
from .routes import score_routes
from .snapshot import load_snapshot
from .v3_correspondence import prepare_v3_correspondence

REPORT_VERSION = "rtpeval_v3_pair_report_1"
STAGES = ("draft", "final_primary")
RULES = {
    "profile_id": "rtpeval_v3_pair_rules_1",
    "scope": "selected same-run V3 draft and final_primary",
    "mask": "pair union; exclude only two established zero denominators",
    "delta": "after minus before; exact fractions; unavailable remains null",
    "correspondence": "validated adopted sources before unique fallback and review",
    "quality": "independent checks; deletion and replacement do not repair old facts",
}


@dataclass(frozen=True)
class V3PairReport:
    """Immutable replay result retaining every selected group."""

    status: str
    data: object

    def to_dict(self):
        return {**thaw(self.data), "status": self.status}


def pair_content_hash(report):
    """Hash semantic report content independently of creation time."""
    return canonical_digest(
        {key: value for key, value in report.items() if key not in ("generated_at", "content_hash")}
    )


def _value(value):
    return value.to_dict() if hasattr(value, "to_dict") else thaw(value)


def _difference(before, after):
    return after - before if before is not None and after is not None else None


def _fraction_delta(before, after):
    if before is None or after is None:
        return {"percentage_points": None, "exact_fraction": None}
    delta = Fraction(after["numerator"], after["denominator"]) - Fraction(
        before["numerator"], before["denominator"]
    )
    return {"percentage_points": float(100 * delta), "exact_fraction": _fraction(delta)}


def _observed_changes(before, after):
    output = {}
    for key in sorted(before.keys() | after.keys()):
        a, b = before.get(key), after.get(key)
        if isinstance(a, dict) or isinstance(b, dict):
            output[key] = _observed_changes(
                a if isinstance(a, dict) else {}, b if isinstance(b, dict) else {}
            )
        elif any(type(v) in (int, float) for v in (a, b)) or key.endswith("_exact"):
            delta = None
            if a is not None and b is not None and type(a) is not bool and type(b) is not bool:
                try:
                    delta = (
                        b - a
                        if type(a) is type(b) is int
                        else str(Decimal(str(b)) - Decimal(str(a)))
                    )
                except InvalidOperation:
                    pass
            output[key] = {
                "before": a,
                "after": b,
                "delta": delta,
                "interpretation": "observed_value_difference",
            }
    return output


def _deltas(stages):
    before, after = (stages[name] for name in STAGES)
    dimensions = {}
    for name in DIMENSIONS:
        a, b = before["dimensions"][name], after["dimensions"][name]
        exact = _fraction_delta(
            a["exact_fractions"]["verified_fraction"], b["exact_fractions"]["verified_fraction"]
        )
        dimensions[name] = {
            "counts": {state: b["counts"][state] - a["counts"][state] for state in a["counts"]},
            "not_applicable_count": b["not_applicable_count"] - a["not_applicable_count"],
            "known_unit_count": b["known_unit_count"] - a["known_unit_count"],
            "denominator": _difference(a["denominator"], b["denominator"]),
            "verified_score_percentage_points": exact["percentage_points"],
            "verified_fraction_exact_delta": exact["exact_fraction"],
            "rates": {
                key: _fraction_delta(a["exact_fractions"][key], b["exact_fractions"][key])
                for key in a["exact_fractions"]
            },
            "contribution": _fraction_delta(
                a["contribution"]["exact_fraction"], b["contribution"]["exact_fraction"]
            ),
        }
    output = {
        "dimensions": dimensions,
        "auxiliary_total": _fraction_delta(
            before["auxiliary_total"]["exact_fraction"], after["auxiliary_total"]["exact_fraction"]
        ),
    }
    output["population"] = {
        key: after["population"][key] - value for key, value in before["population"].items()
    }
    output["schedule_measures"] = _observed_changes(
        before["schedule_measures"], after["schedule_measures"]
    )
    output["date_coverage"] = _observed_changes(
        before["descriptive"]["coverage"], after["descriptive"]["coverage"]
    )
    output["repetition"] = _observed_changes(
        before["descriptive"]["repetition"], after["descriptive"]["repetition"]
    )
    old_days = {d["date"]: d for d in before["descriptive"]["density"]}
    new_days = {d["date"]: d for d in after["descriptive"]["density"]}
    output["density"] = [
        {
            "date": day,
            "before": old_days.get(day),
            "after": new_days.get(day),
            "changes": _observed_changes(old_days.get(day, {}), new_days.get(day, {})),
        }
        for day in sorted(old_days.keys() | new_days.keys())
    ]
    for name in ("opening", "routes"):
        output[name + "_availability"] = _observed_changes(
            {
                key: value
                for key, value in before["primary_metrics"][name].items()
                if key.endswith(("count", "coverage")) or key in ("evidence_counts", "basis_counts")
            },
            {
                key: value
                for key, value in after["primary_metrics"][name].items()
                if key.endswith(("count", "coverage")) or key in ("evidence_counts", "basis_counts")
            },
        )
    output["opening_duration_subtotals"] = _observed_changes(
        before["primary_metrics"]["opening"]["duration_subtotals"],
        after["primary_metrics"]["opening"]["duration_subtotals"],
    )
    output["route_observed_burden"] = _observed_changes(
        before["primary_metrics"]["routes"]["observed_transfer_burden"],
        after["primary_metrics"]["routes"]["observed_transfer_burden"],
    )
    return output


def _stage(group, projection, label, indexed, identities):
    key = (group["group_id"], "v3", projection["context"]["run_id"], label)
    schedule = indexed["requirement_schedule"][key]
    metrics = {
        "requirements": schedule["requirements"],
        "grounding": _grounding(projection, identities),
        "non_overlap": schedule["non_overlap"],
        "opening": indexed["opening"][key]["opening"],
        "routes": indexed["routes"][key]["routes"],
    }
    visits = [a for a in projection["activities"] if a["evaluation_role"] == "primary_visit"]
    canonical = [identities[a["source"]["record_id"]]["canonical_place_id"] for a in visits]
    return {
        "label": "V3 draft" if label == "draft" else "V3 final primary",
        "projection": label,
        "projection_context": projection["context"],
        "population": {
            "primary_visit_count": len(visits),
            "unique_canonical_venue_count": len(set(canonical) - {None}),
            "unresolved_identity_count": canonical.count(None),
        },
        "dimensions": {
            name: _dimension(
                raw,
                raw["denominator"]
                if name in ("requirements", "non_overlap")
                else raw["applicable_denominator"],
            )
            for name, raw in metrics.items()
        },
        "primary_metrics": metrics,
        "schedule_measures": schedule["schedule_measures"],
        "descriptive": schedule["descriptive"],
        "occupancy": schedule["occupancy"],
        "component_source_hashes": {name: indexed[name][key]["source_hashes"] for name in indexed},
    }


def build_v3_pair_report(
    intake,
    identity_report,
    snapshot_directory,
    schedule_context=None,
    occupancy_reviews=None,
    route_reviews=None,
    coordinate_evidence=None,
    *,
    expected_plan=None,
    identity_snapshot_directory=None,
    result_sources=None,
    correspondence_reviews=None,
    edit_provenance=None,
    generated_at,
):
    """Replay optional V3 pairs; missing stages never acquire synthetic after results."""
    prepared, identity = _value(intake), _value(identity_report)
    base = {
        "schema_version": REPORT_VERSION,
        "generated_at": generated_at,
        "rules_profile": RULES,
        "rules_profile_hash": canonical_digest(RULES),
        "groups": [],
        "diagnostics": [],
    }
    status = "needs_material_correction"
    try:
        require(isinstance(generated_at, str), "generated_at", "Offset-aware timestamp required")
        require(
            datetime.fromisoformat(generated_at).utcoffset() is not None,
            "generated_at",
            "Offset-aware timestamp required",
        )
        require(prepared.get("status") == "accepted", "intake", "Accepted intake required")
        if not identity_ready(prepared, identity):
            status = "identity_replay_required"
            raise MaterialError(status, "identity", "Current linked identity report required")
        base.update(batch_id=prepared["batch_id"], batch_revision=prepared["revision"])
        valid_pairs = any(
            group["runs"]["v3"]["paired_available"] for group in prepared["inventory"]
        )
        require(
            not valid_pairs or snapshot_directory is not None,
            "snapshot",
            "Frozen paired snapshot required for available pairs",
        )
        indexed = None
        if snapshot_directory is not None:
            snapshot = load_snapshot(snapshot_directory, expected_plan=_value(expected_plan))
            require(
                snapshot["plan"]["paired"] is True,
                "snapshot/plan",
                "Paired evidence scope required",
            )
            components = {
                "requirement_schedule": score_requirement_schedule(
                    intake, identity_report, schedule_context, occupancy_reviews, paired=True
                ).to_dict(),
                "opening": score_opening(
                    intake,
                    identity_report,
                    snapshot_directory,
                    schedule_context,
                    paired=True,
                    expected_plan=expected_plan,
                ).to_dict(),
                "routes": score_routes(
                    intake,
                    identity_report,
                    snapshot_directory,
                    schedule_context,
                    occupancy_reviews,
                    route_reviews,
                    coordinate_evidence,
                    paired=True,
                    expected_plan=expected_plan,
                    identity_snapshot_directory=identity_snapshot_directory,
                ).to_dict(),
            }
            for component in components.values():
                if component["status"] != "complete":
                    status = component["status"]
                    raise MaterialError(status, "components", str(component["diagnostics"]))
            _, manifest_hash = _read(Path(snapshot_directory) / "manifest.json")
            for name in ("opening", "routes"):
                require(
                    components[name]["source_hashes"]["snapshot_manifest"] == manifest_hash
                    and components[name]["source_hashes"]["snapshot_plan"] == snapshot["plan_hash"],
                    name,
                    "Component snapshot mismatch",
                )
            expected = {}
            for group in prepared["inventory"]:
                for version, run in group["runs"].items():
                    projections = {
                        "final": run["final"],
                        **(run["optional"] if version == "v3" else {}),
                    }
                    for label, projection in projections.items():
                        if projection is not None:
                            expected[
                                (group["group_id"], version, projection["context"]["run_id"], label)
                            ] = {
                                "input": group["input_sha256"],
                                "requirement_spec": group["requirement_spec_sha256"],
                                "result": projection["context"]["artifact_sha256"],
                            }
            indexed = {name: _index(component, expected) for name, component in components.items()}
            base["components"] = {
                name: {k: v for k, v in component.items() if k != "results"}
                for name, component in components.items()
            }
            base["snapshot_hashes"] = {"manifest": manifest_hash, "plan": snapshot["plan_hash"]}
        identities = {r["reference_id"]: r for r in identity["records"]}
        correspondence = prepare_v3_correspondence(
            intake, identity_report, result_sources, correspondence_reviews, edit_provenance
        ).to_dict()
        require(
            correspondence["status"] == "complete",
            "correspondence",
            str(correspondence["diagnostics"]),
        )
        correspondence_groups = {g["group_id"]: g for g in correspondence["groups"]}
        base["correspondence_preparation"] = {
            k: v for k, v in correspondence.items() if k != "groups"
        }
        for group in prepared["inventory"]:
            run = group["runs"]["v3"]
            available = {name: run["optional"].get(name) is not None for name in STAGES}
            pair = {
                "group_id": group["group_id"],
                "run_id": run["final"]["context"]["run_id"],
                "pair_status": "pair_unavailable",
                "available_stages": available,
                "correspondence": correspondence_groups[group["group_id"]],
                "stages": {},
                "deltas": None,
                "diagnostics": [
                    d
                    for d in prepared["projection_diagnostics"]
                    if d.get("run_id") == run["final"]["context"]["run_id"]
                ],
            }
            if indexed is not None:
                pair["stages"] = {
                    name: _stage(group, run["optional"][name], name, indexed, identities)
                    for name in STAGES
                    if available[name]
                }
                if all(available.values()):
                    pair["pair_status"] = "available"
                    pair["included_dimensions"] = _totals(pair["stages"])
                    pair["deltas"] = _deltas(pair["stages"])
                    activities = {
                        a["source"]["record_id"]: a
                        for p in run["optional"].values()
                        for a in p["activities"]
                    }
                    relations = pair["correspondence"]["relations"]
                    pair["visit_changes"] = {
                        "replaced_count": sum(r["relation"] == "replaced" for r in relations),
                        "confirmed_venue_loss_count": sum(
                            r["identity_change"] == "changed_canonical_venue"
                            and "primary_visit" in r["roles"]["before"]
                            for r in relations
                            if r["before"] and r["after"]
                        ),
                        "primary_role_loss_count": sum(
                            "primary_visit" in r["roles"]["before"]
                            and "primary_visit" not in r["roles"]["after"]
                            for r in relations
                            if r["before"] and r["after"]
                        ),
                        "removed_count": sum(
                            activities[s["record_id"]]["evaluation_role"] == "primary_visit"
                            for r in relations
                            if r["relation"] == "removed"
                            for s in r["before"]
                        ),
                        "added_count": sum(
                            activities[s["record_id"]]["evaluation_role"] == "primary_visit"
                            for r in relations
                            if r["relation"] == "added"
                            for s in r["after"]
                        ),
                        "unresolved_before": pair["correspondence"]["unresolved"]["before"],
                        "unresolved_after": pair["correspondence"]["unresolved"]["after"],
                    }
                    pair["continuity"] = build_continuity(pair["stages"], pair["correspondence"])
            base["groups"].append(pair)
        base["source_hashes"] = {
            "artifacts": prepared["source_hashes"],
            "intake": canonical_digest(prepared),
            "identity_report": canonical_digest(identity),
            "preparation": {
                name: canonical_digest(_value(value)) if value is not None else None
                for name, value in {
                    "schedule_context": schedule_context,
                    "occupancy_reviews": occupancy_reviews,
                    "route_reviews": route_reviews,
                    "coordinate_evidence": coordinate_evidence,
                    "expected_plan": expected_plan,
                }.items()
            },
        }
        status = "complete"
    except (MaterialError, ValueError, KeyError, TypeError, OSError) as exc:
        base["groups"] = []
        base["diagnostics"] = [
            exc.diagnostic
            if isinstance(exc, MaterialError)
            else {"reason": "material_invalid", "explanation": str(exc)}
        ]
    base["status"] = status
    base["content_hash"] = pair_content_hash(base)
    return V3PairReport(status, freeze(base))
