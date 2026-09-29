"""Source-preserving schedule projection, independent of planner judgments."""

import re
from datetime import date, datetime

from .records import require, source, text

ACTIVITY_FIELDS = (
    "activity_id",
    "activity_kind",
    "title",
    "place_name",
    "source_place_id",
    "location",
    "start_time",
    "end_time",
    "estimated_cost",
    "notes",
)
TRANSFER_FIELDS = (
    "from_activity_id",
    "to_activity_id",
    "origin_place_id",
    "destination_place_id",
    "mode",
    "departure_time",
    "arrival_time",
    "provider_duration_seconds",
    "distance_meters",
    "reserve_seconds",
)
MODES = ("WALK", "TRANSIT", "DRIVE")
PLACEHOLDERS = {"free time", "break", "rest", "relax", "explore", "explore the area"}


def clock(value):
    try:
        return (
            datetime.fromisoformat(value)
            if isinstance(value, str) and ("T" in value or " " in value)
            else None
        )
    except ValueError:
        return None


def interval(start, end):
    a, b = clock(start), clock(end)
    try:
        return (a, b) if a is not None and b is not None and a < b else None
    except TypeError:
        return None


def mode_claim(raw, review):
    if review and "mode" in review:
        return review["mode"]
    found = set()
    prose = " ".join(str(raw.get(k) or "") for k in ("title", "notes")).casefold()
    patterns = {
        "WALK": r"\b(walk|walking|on foot)\b",
        "TRANSIT": r"\b(public transit|public transport|bus|train|metro|subway|tram)\b",
        "DRIVE": r"\b(drive|driving|by car)\b",
    }
    # Negated/conditional recommendations require review rather than keyword selection.
    if re.search(
        r"\b(not|no|avoid)\s+(walk(?:ing)?|driv(?:e|ing)|public transit|bus|train)\b"
        r"|\b(instead|could|either|if)\b",
        prose,
    ):
        return None
    for mode, pattern in patterns.items():
        if re.search(pattern, prose):
            found.add(mode)
    return next(iter(found)) if len(found) == 1 else None


def classify(raw, review):
    if review and "role" in review:
        return review["role"], "independently_reviewed", "reviewed_role"
    role = raw.get("activity_kind", "unknown")
    place = text(raw.get("place_name")) or text(raw.get("source_place_id"))
    title = raw["title"].strip().casefold()
    movement_title = bool(re.match(r"(?:walk|walking|drive|driving|take .*|transit)\b", title))
    visit_title = bool(re.match(r"(?:visit|tour|explore museum)\b", title))
    if (role == "transport" and visit_title) or (role == "main_poi" and movement_title):
        return "unresolved", "unresolved", "role_review_required"
    if role == "transport" and not place:
        return "transport", "declared_consistent", "declared_transport"
    if role == "main_poi" and title not in PLACEHOLDERS:
        return "primary_visit", "declared_consistent", "declared_visit"
    if place and role not in ("transport", "free_time"):
        return "primary_visit", "declared_consistent", "named_visit"
    if not place and title in PLACEHOLDERS and role != "transport":
        return "transition", "declared_consistent", "generic_placeholder"
    return "unresolved", "unresolved", "role_review_required"


def project(itinerary, context, prefix="/itinerary", reviews=(), *, version):
    """Return inventory and uncertainties; never compute metric verdicts."""
    require(isinstance(itinerary, dict), prefix, "Expected an itinerary object")
    require(version in ("v0", "v1", "v2", "v3"), prefix, "Unknown planner version")
    wire = itinerary.get("output_version", "itinerary_1")
    require(
        wire in ("itinerary_1", "itinerary_2"),
        prefix,
        "Unknown itinerary version",
        "unsupported_wire_version",
    )
    days = itinerary.get("days")
    require(isinstance(days, list), prefix, "days must be an array")
    review_map = {r["pointer"]: r for r in reviews}
    consumed = set()
    records, legs, claims, diagnostics = [], [], [], []
    ignored_transport = []
    ids, dates = set(), set()

    def report(reason, refs, explanation):
        diagnostics.append({"reason": reason, "sources": refs, "explanation": explanation})

    for di, day in enumerate(days):
        dp = f"{prefix}/days/{di}"
        require(isinstance(day, dict), dp, "Expected a day object")
        try:
            day_date = date.fromisoformat(day.get("date", ""))
        except (ValueError, TypeError):
            require(False, dp, "Missing or invalid declared day date")
        require(day_date not in dates, dp, "Duplicate declared day date", "duplicate_source_id")
        dates.add(day_date)
        activities = day.get("activities")
        require(isinstance(activities, list), dp, "activities must be an array")
        day_records = []
        for ai, raw in enumerate(activities):
            ap = f"{dp}/activities/{ai}"
            require(isinstance(raw, dict), ap, "Expected an activity object")
            require(
                text(raw.get("activity_id")) and text(raw.get("title")),
                ap,
                "Activity ID and title must be nonempty strings",
            )
            require(
                raw["activity_id"] not in ids, ap, "Duplicate activity ID", "duplicate_source_id"
            )
            ids.add(raw["activity_id"])
            review = review_map.get(ap)
            if review:
                consumed.add(ap)
                require(
                    not review.get("multi_poi"), ap, "Reviewed multi-POI block", "multi_poi_block"
                )
            role, status, reason = classify(raw, review)
            rec = {
                "source": source(context, ap),
                "declared_day": day["date"],
                "original": {k: raw[k] for k in ACTIVITY_FIELDS if k in raw},
                "evaluation_role": role,
                "role_status": status,
                "reason": reason,
                "review": review,
                "transport_applicable": role == "transport" and version == "v0",
            }
            records.append(rec)
            day_records.append(rec)
            times = [clock(raw.get(k)) for k in ("start_time", "end_time")]
            if any(t is not None and t.utcoffset() is None for t in times):
                report(
                    "timezone_unresolved",
                    [rec["source"]],
                    "Wall time retained; no machine timezone is inferred",
                )
            if role == "unresolved":
                report(reason, [rec["source"]], "Independent activity-role review required")
            if interval(raw.get("start_time"), raw.get("end_time")) is None:
                report("invalid_clock", [rec["source"]], "Invalid or incomparable interval")
        visits = [r for r in day_records if r["evaluation_role"] == "primary_visit"]
        spans = [
            interval(r["original"].get("start_time"), r["original"].get("end_time")) for r in visits
        ]
        ordered = []
        try:
            if any(span is None for span in spans):
                raise ValueError("Invalid visit time")
            ordered = sorted(
                visits,
                key=lambda r: (
                    clock(r["original"]["start_time"]),
                    clock(r["original"]["end_time"]),
                    r["source"]["pointer"],
                ),
            )
        except (TypeError, ValueError):
            report(
                "adjacency_unresolved",
                [r["source"] for r in visits],
                "Cannot establish chronological adjacency",
            )
        overlapping_ids = set()
        for index, left in enumerate(ordered):
            for right in ordered[index + 1 :]:
                if clock(right["original"]["start_time"]) >= clock(left["original"]["end_time"]):
                    break
                overlapping_ids.update(
                    (left["original"]["activity_id"], right["original"]["activity_id"])
                )
                report(
                    "overlapping_visit_intervals",
                    [left["source"], right["source"]],
                    "Visit intervals overlap; display ordering does not establish chronology",
                )
        uncertain_roles = any(r["evaluation_role"] == "unresolved" for r in day_records)
        for left, right in zip(ordered, ordered[1:], strict=False):
            leg = {
                "from_source": left["source"],
                "to_source": right["source"],
                "from_activity_id": left["original"]["activity_id"],
                "to_activity_id": right["original"]["activity_id"],
                "declared_day": day["date"],
                "claims": [],
                "gap_start": left["original"]["end_time"],
                "gap_end": right["original"]["start_time"],
                "adjacency_status": "unresolved"
                if uncertain_roles
                or (
                    left["original"]["activity_id"] in overlapping_ids
                    or right["original"]["activity_id"] in overlapping_ids
                )
                else "ordered_candidates",
            }
            legs.append(leg)
    transfers = itinerary.get("transfers", [])
    if not isinstance(transfers, list):
        report(
            "invalid_transfer_collection",
            [source(context, prefix + "/transfers")],
            "Preserved as unavailable transfer representation",
        )
        transfers = []
    for ti, raw in enumerate(transfers):
        ref = source(context, f"{prefix}/transfers/{ti}")
        if not isinstance(raw, dict):
            report("invalid_transfer", [ref], "Expected a transfer object")
            continue
        claim = {
            "source": ref,
            "kind": "transfer",
            "original": {k: raw[k] for k in TRANSFER_FIELDS if k in raw},
            "mode": raw.get("mode") if raw.get("mode") in MODES else None,
            "start": raw.get("departure_time"),
            "end": raw.get("arrival_time"),
        }
        if version == "v0":
            ignored_transport.append(claim)
            report("ignored_transport_source", [ref], "V0 transport uses model activities only")
            continue
        matches = [
            leg
            for leg in legs
            if (leg["from_activity_id"], leg["to_activity_id"])
            == (raw.get("from_activity_id"), raw.get("to_activity_id"))
        ]
        if not matches:
            dangling = (
                not text(raw.get("from_activity_id"))
                or not text(raw.get("to_activity_id"))
                or raw.get("from_activity_id") not in ids
                or raw.get("to_activity_id") not in ids
            )
            report(
                "dangling_transfer_endpoint" if dangling else "nonadjacent_transfer",
                [ref],
                "Transfer cannot be retargeted to another visit pair",
            )
        if raw.get("arrival_time") is None:
            report("missing_claimed_arrival", [ref], "Arrival is not synthesized from duration")
        attach(claim, matches, claims)
    for rec in records:
        if rec["evaluation_role"] != "transport":
            continue
        raw, review = rec["original"], rec["review"]
        claim = {
            "source": rec["source"],
            "kind": "activity",
            "original": raw,
            "mode": mode_claim(raw, review),
            "start": raw.get("start_time"),
            "end": raw.get("end_time"),
        }
        if version != "v0":
            ignored_transport.append(claim)
            report(
                "ignored_transport_source",
                [rec["source"]],
                "V1-V3 transport uses application transfers only; no activity fallback",
            )
            continue
        candidates = [leg for leg in legs if leg["declared_day"] == rec["declared_day"]]
        if review and "from_activity_id" in review:
            matches = [
                leg
                for leg in candidates
                if (leg["from_activity_id"], leg["to_activity_id"])
                == (review["from_activity_id"], review["to_activity_id"])
            ]
        else:
            # Endpoint prose is never interpreted as a trusted binding by a keyword guess.
            prose = str(raw.get("title", "")) + " " + str(raw.get("notes") or "")
            has_endpoint_prose = bool(
                re.search(r"\b(from|to|towards|between)\b|[\u2192>]|\u5230|\u81f3", prose, re.I)
            )
            plain_title = raw.get("title", "").strip().casefold() in {
                "walk",
                "walking",
                "public transit",
                "public transport",
                "drive",
                "driving",
                "transport",
                "transfer",
                "bus",
                "train",
                "metro",
                "subway",
                "tram",
            }
            plain_notes = not raw.get("notes") or str(raw["notes"]).strip().casefold() in {
                "model estimate",
                "estimated, not live verified",
                "estimated",
            }
            matches = (
                []
                if has_endpoint_prose or not plain_title or not plain_notes
                else [
                    leg
                    for leg in candidates
                    if leg["adjacency_status"] != "unresolved"
                    and contains(leg["gap_start"], leg["gap_end"], claim["start"], claim["end"])
                ]
            )
        attach(claim, matches, claims)
        if len(matches) != 1:
            report(
                "ambiguous_transport_association",
                [rec["source"]],
                "Endpoint/position association requires independent review",
            )
    for leg in legs:
        leg["journey"] = reconcile(leg["claims"])
        if leg["journey"]["agreement"] == "conflicting":
            report(
                "conflicting_transport_claims",
                [c["source"] for c in leg["claims"]],
                "No claim takes precedence",
            )
    require(consumed == set(review_map), prefix, "Review points to no activity in this projection")
    return {
        "context": context,
        "projection": prefix,
        "wire_version": wire,
        "planner_version": version,
        "transport_source": "activity" if version == "v0" else "transfer",
        "ignored_transport": ignored_transport,
        "absent_fields": [
            k
            for k in ("output_version", "transfers", "reference_recommendations")
            if k not in itinerary
        ],
        "header": {k: itinerary.get(k) for k in ("destination", "start_date", "end_date")},
        "declared_days": [d["date"] for d in days],
        "activities": records,
        "legs": legs,
        "unbound_transport": [c for c in claims if c["association_status"] != "unique"],
        "nearby": [
            {
                "source": source(context, f"{prefix}/reference_recommendations/{i}"),
                "original": {
                    k: r[k]
                    for k in (
                        "place_name",
                        "source_place_id",
                        "reason",
                        "associated_day",
                        "area",
                        "uncertainty",
                    )
                    if k in r
                },
            }
            for i, r in enumerate(itinerary.get("reference_recommendations", []) or [])
            if isinstance(r, dict)
        ]
        if isinstance(itinerary.get("reference_recommendations", []), list)
        else [],
        "diagnostics": diagnostics,
    }


def contains(start, end, inner_start, inner_end):
    outer, inner = interval(start, end), interval(inner_start, inner_end)
    try:
        return bool(outer and inner and outer[0] <= inner[0] and inner[1] <= outer[1])
    except TypeError:
        return False


def attach(claim, matches, claims):
    claim["association_status"] = "unique" if len(matches) == 1 else "unbound"
    if len(matches) > 1:
        claim["association_status"] = "ambiguous"
    claims.append(claim)
    if len(matches) == 1:
        matches[0]["claims"].append(claim)


def reconcile(claims):
    """Separate duplicates, segments and incompatible alternatives without choosing a winner."""
    if not claims:
        return {"agreement": "incomplete", "occupancy": [], "representation": "absent"}
    groups = {}
    for claim in claims:
        if interval(claim["start"], claim["end"]) is None:
            return {"agreement": "incomplete", "occupancy": [], "representation": "unresolved"}
        key = (claim["mode"], claim["start"], claim["end"])
        groups.setdefault(key, []).append(claim["source"])
    if any(mode is None or interval(a, b) is None for mode, a, b in groups):
        return {"agreement": "incomplete", "occupancy": [], "representation": "unresolved"}
    try:
        windows = sorted(groups, key=lambda key: clock(key[1]))
        segmented = all(
            clock(a[2]) <= clock(b[1]) for a, b in zip(windows, windows[1:], strict=False)
        )
    except TypeError:
        return {"agreement": "incomplete", "occupancy": [], "representation": "unresolved"}
    if len(windows) > 1 and (not segmented or any(c["kind"] == "transfer" for c in claims)):
        return {"agreement": "conflicting", "occupancy": [], "representation": "alternatives"}
    return {
        "agreement": "consistent",
        "representation": "segments" if len(windows) > 1 else "single",
        "occupancy": [
            {"mode": m, "start": a, "end": b, "sources": groups[(m, a, b)]} for m, a, b in windows
        ],
    }
