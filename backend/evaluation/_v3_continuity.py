"""Independent check transitions over established occurrence correspondence."""

from datetime import datetime
from decimal import Decimal


def _transition(before, after, compatible=True):
    if before is None:
        return "added"
    if after is None:
        return "removed"
    if not compatible:
        return "not_comparable"
    states = before["state"], after["state"]
    return {
        ("FAIL", "PASS"): "resolved",
        ("PASS", "FAIL"): "regression",
        ("PASS", "UNKNOWN"): "lost_verification",
        ("FAIL", "UNKNOWN"): "unverified_change",
        ("UNKNOWN", "FAIL"): "unknown_to_fail",
        ("UNKNOWN", "PASS"): "verification_gained",
    }.get(states, "unchanged" if states[0] == states[1] else "state_changed")


def _compare(before, after, *, compatible=True, magnitude=None):
    transition = _transition(before, after, compatible)
    partial = None
    if (
        compatible
        and before is not None
        and after is not None
        and before["state"] == after["state"] == "FAIL"
        and magnitude
    ):
        a, b = before.get(magnitude), after.get(magnitude)
        if a is not None and b is not None:
            a, b = Decimal(str(a)), Decimal(str(b))
            if b < a:
                partial = {
                    "field": magnitude,
                    "before": str(a),
                    "after": str(b),
                    "reduction": str(a - b),
                }
                transition = "partial_observed_improvement"
    return {
        "before": before,
        "after": after,
        "transition": transition,
        "partial_observed_improvement": partial,
    }


def build_continuity(stages, correspondence):
    """Preserve raw checks while attributing only independently supported transitions."""
    before, after = (stages[name] for name in ("draft", "final_primary"))
    result = {"requirements": [], "grounding": [], "opening": [], "routes": []}
    old = {c["obligation_id"]: c for c in before["primary_metrics"]["requirements"]["checks"]}
    new = {c["obligation_id"]: c for c in after["primary_metrics"]["requirements"]["checks"]}
    for oid in sorted(old.keys() | new.keys()):
        result["requirements"].append(
            {"obligation_id": oid, **_compare(old.get(oid), new.get(oid))}
        )
    mapping, compatible_endpoints = {}, set()
    established_before, established_after = set(), set()
    for relation in correspondence["relations"]:
        left, right = relation["before"], relation["after"]
        if len(left) == len(right) == 1 or relation["relation"] == "removed":
            established_before.update(s["record_id"] for s in left)
        if len(left) == len(right) == 1 or relation["relation"] == "added":
            established_after.update(s["record_id"] for s in right)
        compatible = (
            relation["identity_change"] == "same_canonical_venue"
            and relation["roles"]["before"] == relation["roles"]["after"]
        )
        if len(left) == len(right) == 1:
            mapping[left[0]["record_id"]] = right[0]["record_id"]
            if compatible:
                compatible_endpoints.add(left[0]["record_id"])
        for dimension in ("grounding", "opening"):
            old_checks = {
                c["source"]["record_id"]: c for c in before["primary_metrics"][dimension]["checks"]
            }
            new_checks = {
                c["source"]["record_id"]: c for c in after["primary_metrics"][dimension]["checks"]
            }
            if len(left) <= 1 and len(right) <= 1:
                a = old_checks.get(left[0]["record_id"]) if left else None
                b = new_checks.get(right[0]["record_id"]) if right else None
                if a is not None or b is not None:
                    result[dimension].append(
                        {
                            "relation": relation["relation"],
                            **_compare(
                                a,
                                b,
                                compatible=compatible,
                                magnitude="outside_seconds"
                                if dimension == "opening"
                                and a
                                and b
                                and a.get("basis") == b.get("basis")
                                else None,
                            ),
                        }
                    )
            else:
                result[dimension].append(
                    {
                        "relation": relation["relation"],
                        "before_checks": [
                            old_checks[s["record_id"]] for s in left if s["record_id"] in old_checks
                        ],
                        "after_checks": [
                            new_checks[s["record_id"]]
                            for s in right
                            if s["record_id"] in new_checks
                        ],
                        "transition": "structural_change",
                    }
                )
    for dimension in ("grounding", "opening"):
        for label, stage in (("before", before), ("after", after)):
            unresolved = {s["record_id"] for s in correspondence["unresolved"][label]}
            for check in stage["primary_metrics"][dimension]["checks"]:
                if check["source"]["record_id"] in unresolved:
                    result[dimension].append(
                        {
                            "before": check if label == "before" else None,
                            "after": check if label == "after" else None,
                            "transition": "unresolved_correspondence",
                        }
                    )

    def endpoints(check):
        return tuple(check[field]["record_id"] for field in ("from_source", "to_source"))

    old_routes = before["primary_metrics"]["routes"]["checks"]
    new_routes = {endpoints(c): c for c in after["primary_metrics"]["routes"]["checks"]}
    used = set()
    for check in old_routes:
        pair = endpoints(check)
        target = tuple(mapping.get(sid) for sid in pair)
        other = new_routes.get(target)
        if other is not None:
            used.add(target)
            comparable = all(sid in compatible_endpoints for sid in pair)
            result["routes"].append(
                {
                    **_compare(
                        check,
                        other,
                        compatible=comparable,
                        magnitude="raw_deficit_nanoseconds"
                        if all(
                            check.get(k) == other.get(k)
                            for k in (
                                "mode",
                                "reserve_seconds",
                                "deadline_kind",
                                "schedule_tolerance_seconds",
                            )
                        )
                        and check.get("complete_evidence")
                        and other.get("complete_evidence")
                        else None,
                    ),
                    "connection_lineage": "continued_endpoints",
                    "context_changed": any(
                        check.get(key) != other.get(key)
                        for key in (
                            "declared_day",
                            "mode",
                            "evaluation_departure",
                            "canonical_endpoints",
                        )
                    )
                    or _query_context(check) != _query_context(other),
                }
            )
        else:
            result["routes"].append(
                {
                    "before": check,
                    "after": None,
                    "transition": "structural_leg_removed"
                    if all(sid in established_before for sid in pair)
                    else "unresolved_correspondence",
                }
            )
    for pair, check in new_routes.items():
        if pair not in used:
            result["routes"].append(
                {
                    "before": None,
                    "after": check,
                    "transition": "structural_leg_added"
                    if all(sid in established_after for sid in pair)
                    else "unresolved_correspondence",
                }
            )
    result["conflicts"], result["protection_conflicts"] = _conflicts(
        before, after, correspondence, result["routes"]
    )
    return result


def _query_context(check):
    context = check.get("expected_context")
    return {key: value for key, value in context.items() if key != "leg_id"} if context else None


def _unit_key(unit, stage, mapping=None):
    if unit["kind"] == "transport":
        ids = {s["record_id"] for s in unit["sources"]}
        routes = [
            c
            for c in stage["primary_metrics"]["routes"]["checks"]
            if ids and ids == {claim["source"]["record_id"] for claim in c["claims"]}
        ]
        if len(routes) != 1:
            return None
        sources = tuple(routes[0][field]["record_id"] for field in ("from_source", "to_source"))
    else:
        sources = tuple(s["record_id"] for s in unit["sources"])
    if mapping is not None:
        sources = tuple(mapping.get(sid) for sid in sources)
    return (unit["kind"], sources) if sources and None not in sources else None


def _non_conflict(left, right):
    if not left["time_complete"] or not right["time_complete"]:
        return False
    for a in left["intervals"]:
        for b in right["intervals"]:
            if max(datetime.fromisoformat(a["start"]), datetime.fromisoformat(b["start"])) < min(
                datetime.fromisoformat(a["end"]), datetime.fromisoformat(b["end"])
            ):
                return False
    return True


def _participant_changed(unit, stage, activity_ids, structural_legs):
    key = _unit_key(unit, stage)
    return key is not None and (
        any(sid in activity_ids for sid in key[1])
        or (unit["kind"] == "transport" and key[1] in structural_legs)
    )


def _conflicts(before, after, correspondence, route_changes):
    changed_legs = {}
    for side, transition in (
        ("before", "structural_leg_removed"),
        ("after", "structural_leg_added"),
    ):
        changed_legs[side] = {
            tuple(row[side][field]["record_id"] for field in ("from_source", "to_source"))
            for row in route_changes
            if row["transition"] == transition
        }
    mapping, added, removed = {}, set(), set()
    for relation in correspondence["relations"]:
        left, right = relation["before"], relation["after"]
        venue_changed = (
            len(left) == len(right) == 1
            and relation["identity_change"] == "changed_canonical_venue"
        )
        if (
            len(left) == len(right) == 1
            and relation["roles"]["before"] == relation["roles"]["after"]
            and relation["identity_change"] != "changed_canonical_venue"
            and (
                "primary_visit" not in relation["roles"]["before"]
                or relation["identity_change"] == "same_canonical_venue"
            )
        ):
            mapping[left[0]["record_id"]] = right[0]["record_id"]
        if relation["relation"] == "added" or venue_changed:
            added.update(s["record_id"] for s in right)
        if relation["relation"] == "removed" or venue_changed:
            removed.update(s["record_id"] for s in left)
    old_units = {u["commitment_id"]: u for u in before["occupancy"]["commitments"]}
    new_units = {u["commitment_id"]: u for u in after["occupancy"]["commitments"]}
    new_keys = {}
    for uid, unit in new_units.items():
        key = _unit_key(unit, after)
        if key is not None:
            new_keys.setdefault(key, []).append(uid)
    unit_map = {}
    for uid, unit in old_units.items():
        matches = new_keys.get(_unit_key(unit, before, mapping), [])
        if len(matches) == 1:
            unit_map[uid] = matches[0]
    inverse = {new: old for old, new in unit_map.items()}
    old_pairs = {
        tuple(sorted(c["commitment_ids"])): c
        for c in before["schedule_measures"]["commitment_pairs"]
    }
    new_pairs = {
        tuple(sorted(c["commitment_ids"])): c
        for c in after["schedule_measures"]["commitment_pairs"]
    }
    output, used = [], set()
    for ids, conflict in old_pairs.items():
        target = (
            tuple(sorted(unit_map[uid] for uid in ids))
            if all(uid in unit_map for uid in ids)
            else None
        )
        other = new_pairs.get(target)
        if target is None:
            known_removal = any(
                _participant_changed(old_units[uid], before, removed, changed_legs["before"])
                for uid in ids
            )
            output.append(
                {
                    "before": conflict,
                    "after": None,
                    "transition": "removed_participant"
                    if known_removal
                    else "unresolved_correspondence",
                    "continued_participants": [],
                }
            )
        elif other is not None:
            used.add(target)
            magnitude = "seconds" if conflict["status"] == other["status"] == "complete" else None
            output.append(
                {
                    **_compare(conflict, other, magnitude=magnitude),
                    "continued_participants": list(target),
                }
            )
        else:
            clear = _non_conflict(*(new_units[uid] for uid in target))
            output.append(
                {
                    "before": conflict,
                    "after": None,
                    "transition": "resolved"
                    if clear and conflict["state"] == "FAIL"
                    else "lost_verification",
                    "continued_participants": list(target),
                }
            )
    for ids, conflict in new_pairs.items():
        if ids in used:
            continue
        previous = (
            tuple(inverse[uid] for uid in ids) if all(uid in inverse for uid in ids) else None
        )
        known_absence = previous is not None and _non_conflict(
            *(old_units[uid] for uid in previous)
        )
        known_addition = any(
            _participant_changed(new_units[uid], after, added, changed_legs["after"]) for uid in ids
        )
        output.append(
            {
                "before": None,
                "after": conflict,
                "transition": "introduced_conflict"
                if conflict["state"] == "FAIL" and (known_absence or known_addition)
                else "unresolved_attribution",
                "continued_participants": list(ids) if previous is not None else [],
            }
        )
    protections = []

    def blockers(stage):
        return {
            oid: {
                "scope": block["scope"],
                "time_complete": True,
                "intervals": [block["original_intervals"][oid]],
            }
            for block in stage["occupancy"]["blockers"]
            for oid in block["obligation_ids"]
        }

    old_blocks, new_blocks = blockers(before), blockers(after)
    old_protections = {
        (c["commitment_id"], c["obligation_id"]): c
        for c in before["schedule_measures"]["protection_conflicts"]
    }
    new_protections = {
        (c["commitment_id"], c["obligation_id"]): c
        for c in after["schedule_measures"]["protection_conflicts"]
    }
    used = set()
    for (uid, oid), conflict in old_protections.items():
        target = unit_map.get(uid)
        other = new_protections.get((target, oid))
        if other is not None:
            used.add((target, oid))
            record = _compare(conflict, other)
        else:
            clear = (
                target is not None
                and oid in new_blocks
                and _non_conflict(new_units[target], new_blocks[oid])
            )
            removed_participant = _participant_changed(
                old_units[uid], before, removed, changed_legs["before"]
            )
            record = {
                "before": conflict,
                "after": None,
                "transition": "resolved"
                if clear and conflict["state"] == "FAIL"
                else "removed_participant"
                if removed_participant
                else "unresolved_correspondence"
                if target is None
                else "lost_verification",
            }
        protections.append(
            {
                **record,
                "obligation_id": oid,
                "scope": old_blocks.get(oid, {}).get("scope"),
                "continued_participant": target,
            }
        )
    for (uid, oid), conflict in new_protections.items():
        if (uid, oid) in used:
            continue
        previous = inverse.get(uid)
        clear = (
            previous is not None
            and oid in old_blocks
            and _non_conflict(old_units[previous], old_blocks[oid])
        )
        addition = _participant_changed(new_units[uid], after, added, changed_legs["after"])
        protections.append(
            {
                "before": None,
                "after": conflict,
                "transition": "introduced_conflict"
                if conflict["state"] == "FAIL" and (clear or addition)
                else "unresolved_attribution",
                "obligation_id": oid,
                "scope": new_blocks.get(oid, {}).get("scope"),
                "continued_participant": uid if previous is not None else None,
            }
        )
    return output, protections
