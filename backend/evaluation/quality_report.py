"""Replay final projections into a multimetric report and auxiliary verified scores."""

from dataclasses import dataclass
from datetime import datetime
from fractions import Fraction
from pathlib import Path

from .intake import VERSIONS, _read
from .opening import score_opening
from .preparation import identity_ready
from .records import MaterialError, canonical_digest, freeze, require, thaw
from .requirement_schedule import score_requirement_schedule
from .routes import score_routes
from .snapshot import load_snapshot

REPORT_VERSION = "rtpeval_quality_report_1"
DIMENSIONS = ("requirements", "grounding", "non_overlap", "opening", "routes")
RULES_PROFILE = {
    "profile_id": "rtpeval_verified_quality_1",
    "dimensions": list(DIMENSIONS),
    "verified_fraction": "PASS / (PASS + FAIL + UNKNOWN)",
    "total": "unrounded rational mean over the group common mask",
    "exclude": "all four established denominators equal zero",
    "included_no_checks": "raw N/A; contribution zero",
    "unresolved_denominator": "include; dimension and affected total unavailable",
    "empty_mask": "total unavailable",
    "scope": "final projections only; no optional track contributions",
}


@dataclass(frozen=True)
class QualityReportResult:
    """Immutable completed replay or whole-batch material diagnostics."""

    status: str
    data: object

    def to_dict(self):
        return {**thaw(self.data), "status": self.status}


def quality_content_hash(report):
    """Hash all report content except creation time and the hash itself."""
    return canonical_digest(
        {key: value for key, value in report.items() if key not in ("generated_at", "content_hash")}
    )


def _value(value):
    return value.to_dict() if hasattr(value, "to_dict") else value


def _fraction(value):
    return {"numerator": value.numerator, "denominator": value.denominator}


def _dimension(raw, denominator):
    counts = {state: raw["counts"].get(state, 0) for state in ("PASS", "FAIL", "UNKNOWN")}
    known = sum(counts.values())
    require(
        all(type(count) is int and count >= 0 for count in counts.values())
        and (denominator is None or type(denominator) is int and denominator == known),
        "dimensions",
        "Component counts and established denominator must agree",
    )
    state = (
        "UNKNOWN"
        if denominator is None
        else "FAIL"
        if counts["FAIL"]
        else "UNKNOWN"
        if counts["UNKNOWN"]
        else "PASS"
        if known
        else "N/A"
    )
    out = {
        "state": state,
        "counts": counts,
        "known_unit_count": known,
        "denominator": denominator,
        "denominator_unresolved": denominator is None,
        "not_applicable_count": raw["counts"].get("N/A", 0),
        "rates": {},
        "exact_fractions": {},
        "conditional_compliance": None,
        "verified_score_0_100": None,
    }
    out["exact_fractions"]["conditional_compliance"] = None
    numerators = {
        "verified_fraction": counts["PASS"],
        "verification_coverage": counts["PASS"] + counts["FAIL"],
        "unknown_rate": counts["UNKNOWN"],
        "confirmed_violation_rate": counts["FAIL"],
    }
    for name, numerator in numerators.items():
        rate = Fraction(numerator, denominator) if denominator else None
        out["rates"][name] = float(rate) if rate is not None else None
        out["exact_fractions"][name] = (
            {"numerator": numerator, "denominator": denominator} if rate is not None else None
        )
    if denominator:
        out["verified_score_0_100"] = float(Fraction(100 * counts["PASS"], denominator))
        decisive = counts["PASS"] + counts["FAIL"]
        if decisive:
            out["conditional_compliance"] = float(Fraction(counts["PASS"], decisive))
            out["exact_fractions"]["conditional_compliance"] = {
                "numerator": counts["PASS"],
                "denominator": decisive,
            }
    return out


def _grounding(projection, identities):
    checks, roles = [], []
    for activity in projection["activities"]:
        if activity["evaluation_role"] == "primary_visit":
            identity = identities[activity["source"]["record_id"]]
            checks.append(
                {
                    "state": "PASS" if identity["resolution"] == "resolved" else "UNKNOWN",
                    "source": activity["source"],
                    "identity": identity,
                }
            )
        elif activity["evaluation_role"] == "unresolved":
            roles.append({"source": activity["source"], "reason": activity["reason"]})
    counts = {
        state: sum(check["state"] == state for check in checks)
        for state in ("PASS", "FAIL", "UNKNOWN")
    }
    return {
        "checks": checks,
        "counts": counts,
        "applicable_denominator": None if roles else len(checks),
        "unresolved_role_count": len(roles),
        "unresolved_role_records": roles,
        "claimed_id_association": {
            state: sum(check["identity"]["claimed_id_association"] == state for check in checks)
            for state in ("absent", "consistent", "conflicting", "unverifiable")
        },
    }


def _index(component, expected):
    indexed = {}
    for row in component["results"]:
        key = tuple(row[field] for field in ("group_id", "version", "run_id", "projection"))
        require(key in expected and key not in indexed, "components", "Foreign/duplicate row")
        require(
            all(row["source_hashes"].get(name) == value for name, value in expected[key].items()),
            "components",
            "Component source hash mismatch",
        )
        indexed[key] = row
    require(set(indexed) == set(expected), "components", "Incomplete four-version component")
    return indexed


def _totals(versions):
    mask = [
        name
        for name in DIMENSIONS
        if any(version["dimensions"][name]["denominator"] != 0 for version in versions.values())
    ]
    for version in versions.values():
        contributions = []
        for name, dimension in version["dimensions"].items():
            denominator = dimension["denominator"]
            reason = (
                "excluded_common_no_checks"
                if name not in mask
                else "denominator_unresolved"
                if denominator is None
                else "no_checks"
                if denominator == 0
                else None
            )
            fraction = (
                None
                if name not in mask or denominator is None
                else Fraction(dimension["counts"]["PASS"], denominator)
                if denominator
                else Fraction(0)
            )
            dimension["contribution"] = {
                "score_0_100": float(fraction * 100) if fraction is not None else None,
                "exact_fraction": _fraction(fraction) if fraction is not None else None,
                "reason": reason,
            }
            if name in mask:
                contributions.append(fraction)
        unavailable = [name for name in mask if version["dimensions"][name]["denominator"] is None]
        total = sum(contributions, Fraction(0)) / len(mask) if mask and not unavailable else None
        version["auxiliary_total"] = {
            "score_0_100": float(total * 100) if total is not None else None,
            "exact_fraction": _fraction(total) if total is not None else None,
            "total_included_dimensions": len(mask),
            "reason": "no_scorable_dimensions"
            if not mask
            else "denominator_unresolved"
            if unavailable
            else None,
            "unavailable_dimensions": unavailable,
        }
    return mask


def build_quality_report(
    intake,
    identity_report,
    snapshot_directory,
    schedule_context=None,
    occupancy_reviews=None,
    route_reviews=None,
    coordinate_evidence=None,
    *,
    expected_plan=None,
    generated_at,
):
    """Compose existing offline scorers without accepting caller-authored metric summaries."""
    prepared, identity = _value(intake), _value(identity_report)
    base = {
        "schema_version": REPORT_VERSION,
        "generated_at": generated_at,
        "rules_profile_id": RULES_PROFILE["profile_id"],
        "rules_profile": RULES_PROFILE,
        "rules_profile_hash": canonical_digest(RULES_PROFILE),
        "groups": [],
        "diagnostics": [],
    }
    status = "needs_material_correction"
    try:
        require(isinstance(generated_at, str), "generated_at", "Offset-aware timestamp required")
        stamp = datetime.fromisoformat(generated_at)
        require(stamp.utcoffset() is not None, "generated_at", "Offset-aware timestamp required")
        require(
            isinstance(prepared, dict) and prepared.get("status") == "accepted",
            "intake",
            "Accepted intake required",
        )
        base.update(batch_id=prepared["batch_id"], batch_revision=prepared["revision"])
        if not identity_ready(prepared, identity):
            status = "identity_replay_required"
            raise MaterialError(
                status, "identity", "Identity policy/source/reference linkage is invalid"
            )
        snapshot = load_snapshot(snapshot_directory, expected_plan=_value(expected_plan))
        require(
            snapshot["plan"]["paired"] is False,
            "snapshot.plan.paired",
            "Final-only snapshot required; paired evidence aggregation is unsupported",
            reason="unsupported_snapshot_scope",
        )
        components = {
            "requirement_schedule": score_requirement_schedule(
                intake,
                identity_report,
                schedule_context,
                occupancy_reviews,
                paired=False,
            ).to_dict(),
            "opening": score_opening(
                intake,
                identity_report,
                snapshot_directory,
                schedule_context,
                paired=False,
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
                paired=False,
                expected_plan=expected_plan,
            ).to_dict(),
        }
        failures = [
            component for component in components.values() if component["status"] != "complete"
        ]
        if failures:
            status = failures[0]["status"]
            base["diagnostics"] = [d for component in failures for d in component["diagnostics"]]
        else:
            _, manifest_hash = _read(Path(snapshot_directory) / "manifest.json")
            for name in ("opening", "routes"):
                require(
                    components[name]["source_hashes"]["snapshot_manifest"] == manifest_hash
                    and components[name]["source_hashes"]["snapshot_plan"] == snapshot["plan_hash"],
                    name,
                    "Incompatible snapshot linkage",
                )
            expected = {}
            for group in prepared["inventory"]:
                require(
                    set(group["runs"]) == set(VERSIONS), "runs", "Exactly four versions required"
                )
                for version, run in group["runs"].items():
                    expected[
                        (group["group_id"], version, run["final"]["context"]["run_id"], "final")
                    ] = {
                        "input": group["input_sha256"],
                        "requirement_spec": group["requirement_spec_sha256"],
                        "result": run["final"]["context"]["artifact_sha256"],
                    }
            indexed = {name: _index(component, expected) for name, component in components.items()}
            identities = {record["reference_id"]: record for record in identity["records"]}
            groups = []
            for group in prepared["inventory"]:
                versions = {}
                for version in VERSIONS:
                    run = group["runs"][version]
                    key = (group["group_id"], version, run["final"]["context"]["run_id"], "final")
                    schedule = indexed["requirement_schedule"][key]
                    metrics = {
                        "requirements": schedule["requirements"],
                        "grounding": _grounding(run["final"], identities),
                        "non_overlap": schedule["non_overlap"],
                        "opening": indexed["opening"][key]["opening"],
                        "routes": indexed["routes"][key]["routes"],
                    }
                    dimensions = {
                        name: _dimension(
                            raw,
                            raw["denominator"]
                            if name in ("requirements", "non_overlap")
                            else raw["applicable_denominator"],
                        )
                        for name, raw in metrics.items()
                    }
                    versions[version] = {
                        "run_id": key[2],
                        "projection": "final",
                        "dimensions": dimensions,
                        "primary_metrics": metrics,
                        "schedule_measures": schedule["schedule_measures"],
                        "descriptive": schedule["descriptive"],
                        "occupancy": schedule["occupancy"],
                        "component_source_hashes": {
                            name: indexed[name][key]["source_hashes"] for name in components
                        },
                    }
                mask = _totals(versions)
                groups.append(
                    {
                        "group_id": group["group_id"],
                        "included_dimensions": mask,
                        "total_included_dimensions": len(mask),
                        "dimension_weights": {
                            name: _fraction(Fraction(1, len(mask))) for name in mask
                        },
                        "diagnostics": [
                            {
                                "reason": "no_scorable_dimensions",
                                "explanation": "Reconcile applicability before interpreting totals",
                            }
                        ]
                        if not mask
                        else [],
                        "all_totals_available": all(
                            v["auxiliary_total"]["score_0_100"] is not None
                            for v in versions.values()
                        ),
                        "versions": versions,
                    }
                )
            base.update(
                groups=groups,
                components={
                    name: {k: v for k, v in component.items() if k != "results"}
                    for name, component in components.items()
                },
                source_hashes={
                    "artifacts": prepared["source_hashes"],
                    "intake": canonical_digest(prepared),
                    "identity_report": canonical_digest(identity),
                    "identity_evidence": identity["evidence_hash"],
                    "identity_review": identity["review_hash"],
                    "identity_audit": identity["audit_plan_hash"],
                    "identity_references": identity["reference_set_digest"],
                    "snapshot_manifest": manifest_hash,
                    "snapshot_plan": snapshot["plan_hash"],
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
                },
                stage_availability={
                    "resource": {"report_status": "not_integrated"},
                    "human": {"report_status": "not_integrated"},
                    "mechanism": {"report_status": "not_integrated"},
                    "source_runs": [
                        {
                            "group_id": group["group_id"],
                            "version": version,
                            "usage_available": run["usage_available"],
                            "usage_hash": run["usage_hash"],
                            "paired_available": run["paired_available"],
                            "optional_projections": {
                                name: value is not None for name, value in run["optional"].items()
                            },
                        }
                        for group in prepared["inventory"]
                        for version, run in group["runs"].items()
                    ],
                },
            )
            status = "complete"
    except (MaterialError, ValueError, KeyError, TypeError, OSError) as exc:
        base["groups"] = []
        base["diagnostics"] = [
            exc.diagnostic
            if isinstance(exc, MaterialError)
            else {"reason": "material_invalid", "explanation": str(exc)}
        ]
    base["status"] = status
    base["content_hash"] = quality_content_hash(base)
    return QualityReportResult(status, freeze(base))
