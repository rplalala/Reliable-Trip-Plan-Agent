"""Application-owned time occupancy and location adjacency; no text interpretation."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from pydantic import Field

from backend.app.versions.v3.models import ValidationModel


class TimeWindow(ValidationModel):
    root_activity_id: str
    start: datetime
    end: datetime
    source: str


class ScheduleState(ValidationModel):
    windows: tuple[TimeWindow, ...] = ()
    blank_windows: tuple[TimeWindow, ...] = ()
    day_windows: tuple[TimeWindow, ...] = ()
    # Historical IDs remain here so the stage-original spatial baseline uses the same view.
    lineage: dict[str, str] = Field(default_factory=dict)
    fixed: tuple[TimeWindow, ...] = ()
    unresolved_dates: tuple[str, ...] = ()
    classifications: tuple[dict, ...] = ()
    occupied_transfers: tuple[dict, ...] = ()


def subtract(start, end, intervals):
    pieces = [(start, end)]
    for left, right in sorted(intervals):
        updated = []
        for a, b in pieces:
            if right <= a or left >= b:
                updated.append((a, b))
            else:
                if a < left:
                    updated.append((a, left))
                if right < b:
                    updated.append((right, b))
        pieces = updated
    return pieces


def build_schedule(itinerary, contract, places=(), *, primary_generated=False):
    """None means historical/unassessed, never an assertion of no fixed requirements."""
    windows, lineage, classifications, fixed, unresolved = [], {}, [], [], set()
    zones = {p.timezone_id for p in places if p.timezone_id}
    try:
        zone = ZoneInfo(next(iter(zones))) if len(zones) == 1 else None
    except (ValueError, KeyError):
        zone = None
    day_windows = []
    protections = contract.time_protections
    cost_links = {p.field_path: p for p in getattr(itinerary, "cost_projections", ())}
    from backend.app.schemas.itinerary import ItineraryDay

    schedule_days = list(itinerary.days)
    existing_dates = {d.date for d in schedule_days}
    date_cursor = itinerary.start_date
    while date_cursor <= itinerary.end_date:
        if date_cursor not in existing_dates:
            schedule_days.append(ItineraryDay(date=date_cursor, activities=[]))
        date_cursor += timedelta(days=1)
    for day_index, day in enumerate(schedule_days):
        if day.activities and all(a.start_time.utcoffset() is not None for a in day.activities):
            midnight = datetime.combine(
                day.date, datetime.min.time(), day.activities[0].start_time.tzinfo
            )
            day_windows.append(
                TimeWindow(
                    root_activity_id=f"calendar:{day.date}",
                    start=midnight,
                    end=midnight + timedelta(days=1),
                    source="existing_day_calendar_gaps",
                )
            )
        relevant = [p for p in protections or () if not p.dates or day.date in p.dates]
        for index, protection in enumerate(relevant):
            if protection.status == "unresolved" or zone is None:
                unresolved.add(str(day.date))
                continue
            fixed.append(
                TimeWindow(
                    root_activity_id=f"requirement_time_{day.date}_{index}",
                    start=datetime.combine(day.date, protection.start_time, zone),
                    end=datetime.combine(day.date, protection.end_time, zone),
                    source=protection.model_dump_json(),
                )
            )
        for activity_index, activity in enumerate(day.activities):
            if activity.activity_kind != "free_time":
                continue
            reason = "generated_locationless_placeholder"
            if not primary_generated or protections is None:
                reason = "time_provenance_unassessed"
            elif str(day.date) in unresolved:
                reason = "scoped_time_requirement_unresolved"
            elif activity.source_place_id or activity.location or activity.place_name:
                reason = "location_commitment"
            elif activity.estimated_cost is not None or (
                (
                    projection := cost_links.get(
                        f"days[{day_index}].activities[{activity_index}].estimated_cost"
                    )
                )
                is not None
                and projection.projection not in {"explicit_null", "invalid_set_null"}
            ):
                reason = "cost_obligation"
            elif activity.start_time.utcoffset() is None:
                reason = "time_zone_unavailable"
            if reason == "generated_locationless_placeholder":
                windows.append(
                    TimeWindow(
                        root_activity_id=activity.activity_id,
                        start=activity.start_time,
                        end=activity.end_time,
                        source="primary_generation:activity:" + activity.activity_id,
                    )
                )
                lineage[activity.activity_id] = activity.activity_id
            classifications.append(
                dict(
                    activity_id=activity.activity_id,
                    reason=reason,
                    disposition="elastic_with_fixed_exclusions"
                    if activity.activity_id in lineage
                    else "protected_or_uncertain",
                )
            )
    return ScheduleState(
        windows=tuple(windows),
        day_windows=tuple(day_windows),
        lineage=lineage,
        fixed=tuple(fixed),
        unresolved_dates=tuple(sorted(unresolved)),
        classifications=tuple(classifications),
    )


def ordered_activities(day, schedule=None):
    elastic = schedule.lineage if schedule else {}
    return sorted(
        (a for a in day.activities if a.activity_id not in elastic), key=lambda a: a.start_time
    )


def available_intervals(left, right, schedule=None):
    if left.end_time.utcoffset() is None or right.start_time.utcoffset() is None:
        return []
    blocked = [(w.start, w.end) for w in schedule.fixed] if schedule else []
    return (
        subtract(left.end_time, right.start_time, blocked)
        if right.start_time > left.end_time
        else []
    )


def available_minutes(left, right, schedule=None, *, at_departure=False):
    try:
        gaps = available_intervals(left, right, schedule)
        if at_departure:
            return next(((b - a).total_seconds() / 60 for a, b in gaps if a == left.end_time), 0)
        if gaps:
            return max((b - a).total_seconds() / 60 for a, b in gaps)
        return min(0, (right.start_time - left.end_time).total_seconds() / 60)
    except TypeError:
        return None


def window_projection(itinerary, schedule, roots):
    if schedule is None:
        return []
    windows = {w.root_activity_id: w for w in schedule.windows}
    rows = []
    for day in itinerary.days:
        occupied = [
            (a.start_time, a.end_time)
            for a in day.activities
            if a.activity_id not in schedule.lineage
        ]
        occupied += [(w.start, w.end) for w in schedule.fixed]
        for a in day.activities:
            root = schedule.lineage.get(a.activity_id)
            if root not in roots:
                continue
            w = windows[root]
            for start, end in subtract(
                max(a.start_time, w.start), min(a.end_time, w.end), occupied
            ):
                rows.append(
                    dict(
                        root_activity_id=root,
                        fragment_id=a.activity_id,
                        start=start.isoformat(),
                        end=end.isoformat(),
                        source=w.source,
                    )
                )
    for w in schedule.blank_windows:
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
    return rows


def retained_transfers(original, proposed, schedule):
    """Keep only reservations whose endpoints and adjacency are unchanged.

    Superseded reservations remain in prior round audit, not as simultaneous travel.
    Removing a reservation does not recreate or enlarge a free-time fragment.
    """
    if schedule is None:
        return ()
    old = {a.activity_id: a for d in original.days for a in d.activities}
    new = {a.activity_id: a for d in proposed.days for a in d.activities}
    pairs = {
        (a.activity_id, b.activity_id)
        for d in proposed.days
        for ordered in [ordered_activities(d, schedule)]
        for a, b in zip(ordered, ordered[1:], strict=False)
    }
    return tuple(
        t
        for t in schedule.occupied_transfers
        if (t["from_activity_id"], t["to_activity_id"]) in pairs
        and all(new.get(t[k]) == old.get(t[k]) for k in ("from_activity_id", "to_activity_id"))
    )


def check_time_permissions(original, proposed, schedule):
    if schedule is None:
        return
    old = {a.activity_id: a for d in original.days for a in d.activities}
    new = {a.activity_id: a for d in proposed.days for a in d.activities}
    for a in old.values():
        if (
            a.activity_kind not in {"generic_activity", "unknown", "transport"}
            or new.get(a.activity_id) == a
        ):
            continue
        if str(a.start_time.date()) in schedule.unresolved_dates or any(
            a.start_time.utcoffset() is not None
            and max(a.start_time, w.start) < min(a.end_time, w.end)
            for w in schedule.fixed
        ):
            raise ValueError("Existing activity in protected user time has no safe change binding")
    for day in proposed.days:
        for a in day.activities:
            if a.activity_id in schedule.lineage or a == old.get(a.activity_id):
                continue
            if str(day.date) in schedule.unresolved_dates:
                raise ValueError("Changed arrangement intersects unresolved time requirement scope")
            for transfer in retained_transfers(original, proposed, schedule):
                start, end = (
                    datetime.fromisoformat(transfer["start"]),
                    datetime.fromisoformat(transfer["end"]),
                )
                if max(a.start_time, start) < min(a.end_time, end):
                    raise ValueError("Changed arrangement overlaps adopted transfer reservation")
            for w in schedule.fixed:
                if a.start_time.utcoffset() is None:
                    raise ValueError("Cannot compare fixed time with unknown activity timezone")
                if max(a.start_time, w.start) < min(a.end_time, w.end):
                    raise ValueError("Changed arrangement overlaps fixed user time")


def consume_windows(original, proposed, scope, schedule, places, evidence, policy, *, prefix):
    """Atomic derived edits after patch authorization; reserve only actual affected transfers."""
    if schedule is None or not scope.window_roots:
        return proposed, schedule, ()
    windows = {w.root_activity_id: w for w in schedule.windows}
    if len(set(scope.window_roots)) != len(scope.window_roots) or any(
        root not in windows or windows[root].start.date() not in scope.dates
        for root in scope.window_roots
    ):
        raise ValueError("Invalid elastic window scope")
    from backend.app.schemas.itinerary import Activity
    from backend.app.versions.v3.repair_spatial import layout_measure

    check_time_permissions(original, proposed, schedule)
    old = {a.activity_id: a for d in original.days for a in d.activities}
    result = proposed.model_copy(deep=True)
    lineage = dict(schedule.lineage)
    transfers, audit = [], []
    occupied = [
        (a.start_time, a.end_time)
        for d in proposed.days
        for a in d.activities
        if a.activity_id not in schedule.lineage and a != old.get(a.activity_id)
    ]
    for day in proposed.days:
        ordered = ordered_activities(day, schedule)
        for left, right in zip(ordered, ordered[1:], strict=False):
            if left == old.get(left.activity_id) and right == old.get(right.activity_id):
                continue
            if not left.source_place_id or not right.source_place_id:
                continue  # Unknown real activities remain barriers in route/spatial checks.
            minutes, basis, refs = layout_measure(
                left,
                right,
                scope.travel_mode or "WALK",
                evidence,
                scope.routing_preference,
                schedule,
            )
            if minutes is None:
                minutes, basis = policy.fallback_reserve_minutes, "policy_reserve_route_unknown"
            duration = timedelta(minutes=minutes)
            interval = next(
                (
                    (a, a + duration)
                    for a, b in available_intervals(left, right, schedule)
                    if b - a >= duration and (basis != "time_applicable" or a == left.end_time)
                ),
                None,
            )
            if interval is None:
                raise ValueError("Insufficient unoccupied transfer window")
            occupied.append(interval)
            transfers.append(
                dict(
                    from_activity_id=left.activity_id,
                    to_activity_id=right.activity_id,
                    start=interval[0].isoformat(),
                    end=interval[1].isoformat(),
                    basis=basis,
                    evidence_refs=list(refs),
                )
            )
    windows = {w.root_activity_id: w for w in schedule.windows}
    for day in result.days:
        updated = []
        for a in day.activities:
            root = lineage.get(a.activity_id)
            if root not in scope.window_roots:
                updated.append(a)
                continue
            w = windows[root]
            if not w.start <= a.start_time < a.end_time <= w.end or a.activity_kind != "free_time":
                raise ValueError("Placeholder exceeds original authorization")
            cuts = [
                (max(left, a.start_time), min(right, a.end_time))
                for left, right in occupied
                if max(left, a.start_time) < min(right, a.end_time)
            ]
            # Fixed user time is never consumed, including by transfer reservations.
            for left, right in cuts:
                if any(
                    max(left, f.start, a.start_time) < min(right, f.end, a.end_time)
                    for f in schedule.fixed
                ):
                    raise ValueError("Placeholder consumption overlaps fixed user time")
            if not cuts:
                updated.append(a)
                continue
            pieces = subtract(a.start_time, a.end_time, cuts)
            ids = []
            for index, (start, end) in enumerate(pieces):
                aid = f"{prefix}_window_{len(audit)}_{index}"
                if (
                    aid in old
                    or aid in lineage
                    or any(aid == x.activity_id for d in proposed.days for x in d.activities)
                ):
                    raise ValueError("Window fragment ID collision")
                fragment = Activity.model_validate(
                    {
                        **a.model_dump(),
                        "activity_id": aid,
                        "start_time": start,
                        "end_time": end,
                    }
                )
                updated.append(fragment)
                lineage[aid] = root
                ids.append(aid)
            audit.append(
                dict(
                    root_activity_id=root,
                    previous_fragment_id=a.activity_id,
                    fragment_ids=ids,
                    authorized_start=w.start.isoformat(),
                    authorized_end=w.end.isoformat(),
                    source=w.source,
                    consumed=[(left.isoformat(), right.isoformat()) for left, right in cuts],
                )
            )
        day.activities = updated
    # Null/unknown cost projections are not financial obligations. Remove stale paths for
    # consumed placeholders; immutable originals retain their observations.
    if hasattr(result, "set_cost_projections"):
        paths = {
            f"days[{di}].activities[{ai}].estimated_cost": a.activity_id
            for di, d in enumerate(proposed.days)
            for ai, a in enumerate(d.activities)
        }
        new = {
            a.activity_id: f"days[{di}].activities[{ai}].estimated_cost"
            for di, d in enumerate(result.days)
            for ai, a in enumerate(d.activities)
        }
        from dataclasses import replace

        result.set_cost_projections(
            tuple(
                replace(p, field_path=new[paths[p.field_path]])
                for p in proposed.cost_projections
                if paths.get(p.field_path) in new
            )
        )
    type(result).model_validate(result.model_dump())
    return (
        result,
        schedule.model_copy(
            update={
                "lineage": lineage,
                "occupied_transfers": (
                    *retained_transfers(original, proposed, schedule),
                    *transfers,
                ),
            }
        ),
        tuple(audit),
    )
