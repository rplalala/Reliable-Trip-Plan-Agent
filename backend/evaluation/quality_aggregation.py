"""Exact arithmetic and source-row preparation shared by independent reports."""

from fractions import Fraction

from .records import require

DIMENSIONS = ("requirements", "grounding", "non_overlap", "opening", "routes")


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
