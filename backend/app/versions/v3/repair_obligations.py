"""C visit intent and business obligations, reusing canonical evidence and A adjacency."""

from backend.app.versions.v3.repair_models import VisitBinding
from backend.app.versions.v3.repair_schedule import ordered_activities


def bind_visits(itinerary, context):
    bindings = list(context.visit_bindings)
    explicit_ids = {b.activity_id for b in bindings}
    for rule in context.contract.visit_requirements or ():
        if not rule.access_mode or rule.status != "executable":
            continue
        named = next(
            (n for n in context.contract.named_places if n.requirement_id == rule.requirement_id),
            None,
        )
        matches = [
            b for b in context.named_resolutions if b.search_intent_id == rule.requirement_id
        ]
        if named is None or len(matches) != 1:
            continue
        resolution = matches[0]
        if (
            resolution.status != "resolved"
            or not resolution.resolved_place_id
            or resolution.matching_place_ids != (resolution.resolved_place_id,)
            or resolution.named_place_intent.place_text != named.place_text
            or resolution.named_place_intent.source_text not in {r.quote for r in named.source_refs}
        ):
            continue
        visits = [
            a
            for d in itinerary.days
            for a in d.activities
            if a.activity_kind == "main_poi" and a.source_place_id == resolution.resolved_place_id
        ]
        # Canonical intent cannot select which of multiple copies is an interior visit.
        if len(visits) == 1 and visits[0].activity_id not in explicit_ids:
            bindings.append(
                VisitBinding(
                    activity_id=visits[0].activity_id,
                    place_id=resolution.resolved_place_id,
                    mode=rule.access_mode,
                    source_refs=tuple(
                        f"requirement:{rule.requirement_id}:{r.start}:{r.end}"
                        for r in rule.source_refs
                    ),
                )
            )
    return tuple(bindings)


def visit_binding(activity, bindings):
    matches = [
        b
        for b in bindings
        if b.activity_id == activity.activity_id and b.place_id == activity.source_place_id
    ]
    return matches[0] if len(matches) == 1 else None


def removed_obligation(finding, original, proposed):
    before = {a.activity_id: (d.date, a) for d in original.days for a in d.activities}
    after = {a.activity_id: (d.date, a) for d in proposed.days for a in d.activities}
    if any(
        i not in after or before[i][1].source_place_id != after[i][1].source_place_id
        for i in finding.activity_ids
    ):
        return True
    return finding.check == "route" and len({after[i][0] for i in finding.activity_ids}) > 1


def route_chain_value(finding, original, proposed, report, schedule):
    if removed_obligation(finding, original, proposed):
        return 0.0
    left, right = finding.activity_ids
    for day in proposed.days:
        ids = [a.activity_id for a in ordered_activities(day, schedule)]
        if left not in ids or right not in ids:
            continue
        lo, hi = sorted((ids.index(left), ids.index(right)))
        pairs = list(zip(ids[lo:hi], ids[lo + 1 : hi + 1], strict=False))
        values = []
        for pair in pairs:
            rows = [f for f in report.findings if f.check == "route" and f.activity_ids == pair]
            if (
                len(rows) != 1
                or rows[0].status not in {"PASS", "CONFIRMED"}
                or rows[0].magnitude is None
            ):
                return None
            values.append(rows[0].magnitude)
        return sum(values) if values else None
    return None
