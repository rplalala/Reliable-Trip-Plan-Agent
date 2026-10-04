"""Independent itinerary claims and continuous intervals, without route observations."""

from ._route_rules import HARD_BOUNDARY_TOLERANCE_SECONDS, NANOSECOND, NEXT_VISIT_TOLERANCE_SECONDS
from .occupancy import read_span, union
from .records import canonical_digest, thaw
from .schedule_time import Span, normalize_interval


def nanoseconds(delta):
    return (delta.days * 86400 + delta.seconds) * NANOSECOND + delta.microseconds * 1000


def _overlaps(span, gap):
    return span.start < gap.end and gap.start < span.end


def _free_fragments(gap, blockers):
    spans = union(blockers)
    result, cursor = [], gap.start
    for span in spans:
        if span.end <= cursor or span.start >= gap.end:
            continue
        if cursor < span.start:
            result.append(Span(cursor, min(span.start, gap.end)))
        cursor = max(cursor, span.end)
    if cursor < gap.end:
        result.append(Span(cursor, gap.end))
    return result


def prepare_leg(leg, occupancy, zone, identities):
    lid = canonical_digest(
        {
            "origin_reference": leg["from_source"]["record_id"],
            "destination_reference": leg["to_source"]["record_id"],
        }
    )
    canonical = [
        identities[s["record_id"]]["canonical_place_id"]
        for s in (leg["from_source"], leg["to_source"])
    ]
    claims = leg["claims"]
    unique = {canonical_digest([c["mode"], c["start"], c["end"]]): c for c in claims}
    claim = next(iter(unique.values())) if len(unique) == 1 else None
    mode, departure = (claim["mode"], claim["start"]) if claim else (None, None)
    reasons = []
    if len(unique) > 1:
        reasons.append("transport_claims_conflicting_or_segmented")
    gap_record = normalize_interval(leg["gap_start"], leg["gap_end"], leg["declared_day"], zone)
    gap = gap_record.span
    if gap is None:
        reasons.extend(gap_record.reasons)
    if leg["adjacency_status"] == "unresolved":
        reasons.append("adjacency_unresolved")
    blockers = []
    blocker_records = []
    own_sources = {s["record_id"] for s in (leg["from_source"], leg["to_source"])}
    own_sources.update(c["source"]["record_id"] for c in claims)
    if gap:
        for blocker in thaw(occupancy.blockers):
            if blocker["scope"] == "scheduled_commitments":
                span = read_span(blocker["interval"])
                if _overlaps(span, gap) or span.start == gap.end:
                    blockers.append(span)
                    blocker_records.append(blocker)
        for unit in occupancy.commitments:
            if any(s["record_id"] in own_sources for s in unit.sources):
                continue
            if unit.complete:
                for span in unit.guaranteed:
                    if _overlaps(span, gap) or span.start == gap.end:
                        blockers.append(span)
                        blocker_records.append(unit.to_dict())
            elif unit.declared_day in (None, leg["declared_day"]):
                guaranteed = unit.guaranteed
                for span in guaranteed:
                    if _overlaps(span, gap) or span.start == gap.end:
                        blockers.append(span)
                        blocker_records.append(unit.to_dict())
                guaranteed_deadline = any(span.start == gap.end for span in guaranteed)
                if any(
                    scenario is None
                    or any(
                        _overlaps(span, gap) or (span.start == gap.end and not guaranteed_deadline)
                        for span in scenario
                    )
                    for scenario in unit.scenarios
                ):
                    reasons.append("occupied_time_unresolved")
        for item in thaw(occupancy.candidates):
            if item.get("interval"):
                uncertain = _overlaps(read_span(item["interval"]), gap)
            else:
                uncertain = item.get("declared_day") in (None, leg["declared_day"])
            if uncertain:
                reasons.append("occupied_time_unresolved")
        for item in thaw(occupancy.pending_protections):
            if item["scope"] in (None, "scheduled_commitments") and item["date"] in (
                None,
                leg["declared_day"],
            ):
                reasons.append("protection_time_unresolved")
    fragments = _free_fragments(gap, blockers) if gap else []
    selected = None
    explicit = None
    if departure is not None and gap:
        clock = normalize_interval(departure, leg["gap_end"], leg["declared_day"], zone)
        reasons.extend(clock.reasons)
        explicit = clock.span.start if clock.span else None
        if explicit:
            selected = next(
                (Span(explicit, f.end) for f in fragments if f.start <= explicit < f.end), None
            )
        if selected is None:
            reasons.append("explicit_departure_outside_free_interval")
    elif fragments and len(unique) <= 1:
        selected = min(fragments, key=lambda f: (-nanoseconds(f.end - f.start), f.start))
    if not selected:
        reasons.append("continuous_interval_unavailable")
    if reasons:
        selected = None
    hard = bool(selected and any(b.start == selected.end for b in blockers))
    return {
        "leg_id": lid,
        "declared_day": leg["declared_day"],
        "from_source": leg["from_source"],
        "to_source": leg["to_source"],
        "from_activity_id": leg["from_activity_id"],
        "to_activity_id": leg["to_activity_id"],
        "canonical_endpoints": canonical,
        "claims": claims,
        "claims_present": bool(claims),
        "ignored_transport_is_not_fallback": True,
        "mode": mode,
        "mode_basis": "itinerary" if mode else None,
        "submitted_departure": departure,
        "explicit_departure": explicit.isoformat() if explicit else None,
        "gap": gap_record.to_dict(),
        "blockers": blocker_records,
        "fragments": [f.to_dict() for f in fragments],
        "selected_interval": selected.to_dict() if selected else None,
        "evaluation_departure": selected.start.isoformat() if selected else None,
        "available_nanoseconds": nanoseconds(selected.end - selected.start) if selected else None,
        "deadline_kind": "hard_boundary" if hard else "next_visit" if selected else None,
        "schedule_tolerance_seconds": HARD_BOUNDARY_TOLERANCE_SECONDS
        if hard
        else NEXT_VISIT_TOLERANCE_SECONDS
        if selected
        else None,
        "reasons": list(dict.fromkeys(reasons)),
        "applicability": "N/A"
        if canonical[0] is not None and canonical[0] == canonical[1]
        else "applicable",
    }
