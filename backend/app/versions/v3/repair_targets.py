"""B target dependencies and executable visit satisfaction, never text interpretation."""

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from backend.app.versions.v3.repair_models import RelatedTarget
from backend.app.versions.v3.repair_schedule import TimeWindow, ordered_activities, subtract


def visit_rules(context):
    named = {r.requirement_id: r for r in context.contract.named_places}
    resolved = {}
    for binding in context.named_resolutions:
        n = named.get(binding.search_intent_id)
        if (
            n
            and binding.status == "resolved"
            and binding.resolved_place_id
            and sum(b.search_intent_id == n.requirement_id for b in context.named_resolutions) == 1
            and binding.matching_place_ids == (binding.resolved_place_id,)
            and binding.named_place_intent.place_text == n.place_text
            and binding.named_place_intent.source_text in {r.quote for r in n.source_refs}
        ):
            resolved[n.requirement_id] = binding.resolved_place_id
    rules = []
    for n in named.values():
        pid = resolved.get(n.requirement_id)
        if pid and n.inclusion == "REQUIRED":
            rules.append((pid, 1, (), context.contract.visit_requirements is None))
    for v in context.contract.visit_requirements or ():
        pid = resolved.get(v.requirement_id)
        if pid:
            rules.append((pid, v.minimum_visits, v.dates, v.status == "unresolved"))
    return rules


def main_visits(itinerary, pid):
    return [
        (d.date, a)
        for d in itinerary.days
        for a in d.activities
        if a.activity_kind == "main_poi" and a.source_place_id == pid
    ]


def protect_visits(original, proposed, context):
    for pid, count, dates, uncertain in visit_rules(context):
        before, after = main_visits(original, pid), main_visits(proposed, pid)
        from backend.app.versions.v3.repair_obligations import bind_visits, visit_binding

        modes = {
            v.access_mode
            for v in context.contract.visit_requirements or ()
            if v.access_mode
            and any(
                n.requirement_id == v.requirement_id
                and b.search_intent_id == n.requirement_id
                and b.resolved_place_id == pid
                for n in context.contract.named_places
                for b in context.named_resolutions
            )
        }
        if modes:
            old_bindings, new_bindings = (
                bind_visits(original, context),
                bind_visits(proposed, context),
            )
            before = [
                (d, a)
                for d, a in before
                if (binding := visit_binding(a, old_bindings)) and binding.mode in modes
            ]
            after = [
                (d, a)
                for d, a in after
                if (binding := visit_binding(a, new_bindings)) and binding.mode in modes
            ]

        if uncertain:
            retained = {a.activity_id: (day, a) for day, a in after}
            if any(
                a.activity_id not in retained
                or retained[a.activity_id][0] != day
                or retained[a.activity_id][1].source_place_id != pid
                for day, a in before
            ):
                raise ValueError(
                    "REQUIRED or explicit visit requirement is unassessed or unresolved"
                )
            continue
        if min(len(after), count) < min(len(before), count):
            raise ValueError("REQUIRED visit satisfaction decreased")
        for day in dates:
            if any(d == day for d, _ in before) and not any(d == day for d, _ in after):
                raise ValueError("Required visit date satisfaction decreased")


def repeat_excess(itinerary, pid, context=None):
    count = max((n for p, n, _, _ in visit_rules(context) if p == pid), default=1) if context else 1
    return max(0, len(main_visits(itinerary, pid)) - count)


def movable(activity, context):
    if context is None:
        return True
    if context.contract.visit_requirements is None:
        return False
    return not any(
        pid == activity.source_place_id and (activity.start_time.date() in dates or uncertain)
        for pid, _, dates, uncertain in visit_rules(context)
    )


def prepare_blank_windows(itinerary, context, policy):
    state = context.schedule
    if state is None:
        return None
    zones = {p.timezone_id for p in context.places if p.timezone_id}
    try:
        zone = ZoneInfo(next(iter(zones))) if len(zones) == 1 else None
    except (ValueError, ZoneInfoNotFoundError):
        zone = None
    windows = []
    existing = {d.date: d.activities for d in itinerary.days}
    day = itinerary.start_date
    while day <= itinerary.end_date:
        if (
            not existing.get(day)
            and zone
            and context.contract.time_protections is not None
            and str(day) not in state.unresolved_dates
        ):
            start = datetime.combine(day, time(policy.blank_day_start_hour), zone)
            end = datetime.combine(day, time(), zone) + timedelta(hours=policy.blank_day_end_hour)
            windows.append(
                TimeWindow(
                    root_activity_id=f"blank:{day}",
                    start=start,
                    end=end,
                    source="application_blank_day_policy",
                )
            )
        day += timedelta(days=1)
    return state.model_copy(update={"blank_windows": tuple(windows)})


def check_blank_windows(original, proposed, context):
    if context.schedule is None:
        return
    old = {a.activity_id: a for d in original.days for a in d.activities}
    blank = {
        w.start.date(): w for w in (*context.schedule.day_windows, *context.schedule.blank_windows)
    }
    original_days = {d.date: d for d in original.days}
    for day in proposed.days:
        needs_window = (
            day.date in blank
            or day.date not in original_days
            or not original_days[day.date].activities
        )
        if not needs_window:
            continue
        for a in day.activities:
            if a == old.get(a.activity_id):
                continue
            w = blank.get(day.date)
            if (
                w is None
                or a.start_time.utcoffset() is None
                or not w.start <= a.start_time < a.end_time <= w.end
            ):
                raise ValueError("Blank date lacks an applicable authorized local window")


def related_progress(original, proposed, scope, schedule=None):
    old = {a.activity_id: (d.date, a) for d in original.days for a in d.activities}
    new = {a.activity_id: (d.date, a) for d in proposed.days for a in d.activities}
    active = {r.permission.target_id: r for r in scope.active_related}
    for permission in scope.coverage_permissions:
        triggers = tuple(
            aid
            for aid in permission.trigger_activity_ids
            if aid in old
            and (
                aid not in new
                or old[aid][0] != new[aid][0]
                or old[aid][1].source_place_id != new[aid][1].source_place_id
            )
        )
        if not triggers and permission.target_id not in active:
            continue
        activities = [a for d in proposed.days if d.date == permission.date for a in d.activities]
        before = len(
            {
                a.source_place_id
                for d in original.days
                if d.date == permission.date
                for a in d.activities
                if a.activity_kind == "main_poi" and a.source_place_id
            }
        )
        after = len(
            {
                a.source_place_id
                for a in activities
                if a.activity_kind == "main_poi" and a.source_place_id
            }
        )
        uncertain = any(
            a.activity_kind == "unknown"
            or (a.activity_kind == "main_poi" and not a.source_place_id)
            for a in activities
        )
        ordered = [
            a
            for d in proposed.days
            if d.date == permission.date
            for a in ordered_activities(d, schedule)
        ]
        prior = active.get(permission.target_id)
        active[permission.target_id] = RelatedTarget(
            permission=permission,
            activated_by=prior.activated_by if prior else triggers,
            before=prior.before if prior else before,
            after=after,
            affected_adjacency=tuple(
                (a.activity_id, b.activity_id) for a, b in zip(ordered, ordered[1:], strict=False)
            ),
            status="unknown"
            if uncertain
            else "resolved"
            if after >= permission.minimum_count
            else "unresolved",
        )
    return tuple(active.values())


def insertion_windows(itinerary, schedule, scope):
    from backend.app.versions.v3.repair_schedule import window_projection

    rows = window_projection(itinerary, schedule, scope.window_roots)
    if schedule is None:
        return rows
    for w in schedule.day_windows:
        if w.start.date() not in scope.dates:
            continue
        occupied = [(a.start_time, a.end_time) for d in itinerary.days for a in d.activities]
        occupied.extend((f.start, f.end) for f in schedule.fixed)
        occupied.extend(
            (datetime.fromisoformat(t["start"]), datetime.fromisoformat(t["end"]))
            for t in schedule.occupied_transfers
        )
        for start, end in subtract(w.start, w.end, occupied):
            rows.append(
                dict(
                    root_activity_id=w.root_activity_id,
                    fragment_id=None,
                    start=start.isoformat(),
                    end=end.isoformat(),
                    source=w.source,
                )
            )
    return [r for r in rows if datetime.fromisoformat(r["start"]).date() in scope.dates]


def dispensable_visit(itinerary, activity_id, context):
    """Conditional permission only; the complete atomic patch is checked again."""
    trial = itinerary.model_copy(deep=True)
    for day in trial.days:
        day.activities = [a for a in day.activities if a.activity_id != activity_id]
    try:
        protect_visits(itinerary, trial, context)
    except ValueError:
        return False
    return True
