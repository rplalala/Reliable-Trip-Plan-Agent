"""Offline requirement and schedule metrics over immutable independent preparation."""

import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .identity import SUBJECT_SCOPE_VERSION, identity_references
from .occupancy import assess_occupancy, intersections, prepare_occupancy, read_span, stable_id
from .records import MaterialError, freeze, require, text, thaw
from .schedule_time import expand_protection, normalize_interval

REPORT_VERSION = "rtpeval_requirement_schedule_report_1"
RULES_VERSION = "rtpeval_requirement_schedule_rules_1"
RULES = {
    "version": RULES_VERSION,
    "identity_scope": SUBJECT_SCOPE_VERSION,
    "intervals": "half_open",
    "time_tolerance_seconds": 0,
    "transport": "v0_activity_v1_v3_transfer",
    "count_default": "explicit_reviewed_payload",
    "protection_units": False,
    "timestamp_fraction_digits": 6,
}
OBLIGATION_FIELDS = {
    "required_visit": {"subject_ref", "count", "distinct_dates", "date_obligations"},
    "excluded_visit": {"subject_ref", "scope", "dates"},
    "protected_time": {"date", "interval", "scope"},
    "fixed_visit_time": {"subject_ref", "date", "match", "conditions", "repeat_permission_refs"},
}


@dataclass(frozen=True)
class RequirementScheduleResult:
    status: str
    data: Mapping

    def to_dict(self):
        return {"status": self.status, **thaw(self.data)}


def _value(value):
    return value.to_dict() if hasattr(value, "to_dict") else thaw(value)


def _days(original):
    first = date.fromisoformat(original["start_date"])
    last = date.fromisoformat(original["end_date"])
    return [(first + timedelta(days=i)).isoformat() for i in range((last - first).days + 1)]


def _positive(value):
    return type(value) is int and value > 0


def _sources(refs, original, pointer):
    require(isinstance(refs, list) and bool(refs), pointer, "Nonempty original sources required")
    for ref in refs:
        require(isinstance(ref, dict) and text(ref.get("field_path")), pointer, "Invalid source")
        field = ref["field_path"]
        require(field in original, pointer, "Unknown original field")
        if "quote" in ref:
            quote, value, occurrence = ref["quote"], original[field], ref.get("occurrence", 0)
            require(
                text(quote)
                and isinstance(value, str)
                and type(occurrence) is int
                and occurrence >= 0,
                pointer,
                "Invalid quote",
            )
            positions, offset = [], 0
            while (offset := value.find(quote, offset)) >= 0:
                positions.append(offset)
                offset += len(quote)
            require(occurrence < len(positions), pointer, "Absent quote occurrence")
            if "offset_start" in ref or "offset_end" in ref:
                require(
                    type(ref.get("offset_start")) is int
                    and type(ref.get("offset_end")) is int
                    and ref["offset_start"] == positions[occurrence]
                    and ref["offset_end"] == positions[occurrence] + len(quote),
                    pointer,
                    "Invalid Unicode quote offsets",
                )
        else:
            require(
                "offset_start" not in ref and "offset_end" not in ref,
                pointer,
                "Offsets require a quote",
            )


def _clock(value, pointer, *, end=False):
    require(
        isinstance(value, str) and re.fullmatch(r"[0-9]{2}:[0-9]{2}(?::[0-9]{2})?", value),
        pointer,
        "Expected HH:MM[:SS]",
    )
    parts = [int(part) for part in value.split(":")]
    hour, minute, second = *parts[:2], parts[2] if len(parts) == 3 else 0
    require(
        0 <= minute < 60
        and 0 <= second < 60
        and (0 <= hour < 24 or end and hour == 24 and minute == second == 0),
        pointer,
        "Invalid local clock",
    )
    return hour * 3600 + minute * 60 + second


def _window(value, pointer):
    require(isinstance(value, dict) and set(value) == {"start", "end"}, pointer, "Invalid window")
    start = _clock(value["start"], pointer)
    end = _clock(value["end"], pointer, end=True)
    require(start < end, pointer, "Clock window must increase within one day")
    return start, end


def _validate_spec(group):
    spec, original = group["requirement_spec"], group["input"]
    days = set(_days(original))
    subjects = {item["subject_id"] for item in spec["subjects"]}
    totals, dated, exclusions, distinct, single_times = {}, {}, {}, {}, {}
    incomplete = False
    ids = {item["obligation_id"] for item in spec["obligations"]}
    for item in spec["obligations"]:
        oid, kind = item["obligation_id"], item["kind"]
        _sources(item["source_refs"], original, oid)
        if item["resolution"] != "resolved":
            require(text(item.get("reason")), oid, "Unresolved semantics require a reason")
            incomplete |= kind not in OBLIGATION_FIELDS
            continue
        require(
            kind in ("required_visit", "excluded_visit", "protected_time", "fixed_visit_time"),
            oid,
            "Unsupported executable obligation kind",
        )
        require(
            set(item)
            <= {"obligation_id", "kind", "resolution", "source_refs", "reason"}
            | OBLIGATION_FIELDS[kind],
            oid,
            "Unknown executable fields",
        )
        if kind != "protected_time":
            require(
                text(item.get("subject_ref")) and item["subject_ref"] in subjects,
                oid,
                "Unknown requirement subject",
            )
        if kind in ("protected_time", "fixed_visit_time"):
            require(
                text(item.get("date")) and item["date"] in days,
                oid,
                "Obligation date outside requested dates",
            )
        if kind == "required_visit":
            count = item.get("count")
            require(
                isinstance(count, dict)
                and set(count) == {"mode", "value"}
                and count["mode"] in ("minimum", "exact")
                and _positive(count["value"]),
                oid,
                "Invalid count",
            )
            require(type(item.get("distinct_dates", False)) is bool, oid, "Invalid distinct_dates")
            if item.get("distinct_dates"):
                require(count["value"] <= len(days), oid, "Impossible distinct-date count")
                distinct[item["subject_ref"]] = max(
                    distinct.get(item["subject_ref"], 0), count["value"]
                )
            total = (count["value"], count["value"] if count["mode"] == "exact" else None)
            totals.setdefault(item["subject_ref"], []).append(total)
            dates = item.get("date_obligations", [])
            require(isinstance(dates, list), oid, "Invalid date obligations")
            seen = set()
            for entry in dates:
                require(
                    isinstance(entry, dict)
                    and set(entry) == {"date", "count_mode", "count"}
                    and text(entry["date"])
                    and entry["date"] in days
                    and entry["date"] not in seen
                    and entry["count_mode"] in ("minimum", "exact")
                    and _positive(entry["count"]),
                    oid,
                    "Invalid/duplicate dated count",
                )
                seen.add(entry["date"])
                dated.setdefault((item["subject_ref"], entry["date"]), []).append(
                    (entry["count"], entry["count"] if entry["count_mode"] == "exact" else None)
                )
        elif kind == "excluded_visit":
            require(item.get("scope") in ("whole_trip", "specified_dates"), oid, "Invalid scope")
            if item["scope"] == "whole_trip":
                require("dates" not in item, oid, "Whole-trip exclusion cannot supply dates")
                excluded = days
            else:
                values = item.get("dates")
                require(
                    isinstance(values, list)
                    and bool(values)
                    and all(text(d) and d in days for d in values)
                    and len(set(values)) == len(values),
                    oid,
                    "Invalid excluded dates",
                )
                excluded = set(values)
            exclusions.setdefault(item["subject_ref"], set()).update(excluded)
        elif kind == "protected_time":
            require(
                item.get("scope") in ("primary_visits", "scheduled_commitments"),
                oid,
                "Invalid protected scope",
            )
            interval = item.get("interval")
            require(isinstance(interval, dict), oid, "Invalid protection interval")
            if interval.get("kind") == "full_day":
                require(set(interval) == {"kind"}, oid, "Unexpected full-day operators")
            else:
                require(
                    interval.get("kind") == "clock" and set(interval) == {"kind", "start", "end"},
                    oid,
                    "Invalid protection operator",
                )
                _window({key: interval[key] for key in ("start", "end")}, oid)
        else:
            require(
                item.get("match") in ("single_visit", "at_least_one"), oid, "Invalid time selector"
            )
            if item["match"] == "at_least_one":
                _sources(item.get("repeat_permission_refs"), original, oid)
                totals.setdefault(item["subject_ref"], []).append((1, None))
                dated.setdefault((item["subject_ref"], item["date"]), []).append((1, None))
            else:
                require(
                    "repeat_permission_refs" not in item,
                    oid,
                    "Single visit cannot permit repetition",
                )
                totals.setdefault(item["subject_ref"], []).append((1, 1))
                dated.setdefault((item["subject_ref"], item["date"]), []).append((1, None))
            conditions = item.get("conditions")
            require(
                isinstance(conditions, dict)
                and bool(conditions)
                and set(conditions) <= {"start_at", "within", "duration"},
                oid,
                "Invalid conditions",
            )
            start = _clock(conditions["start_at"], oid) if "start_at" in conditions else None
            window = _window(conditions["within"], oid) if "within" in conditions else None
            if "duration" in conditions:
                duration = conditions["duration"]
                require(
                    isinstance(duration, dict)
                    and set(duration) == {"mode", "seconds"}
                    and duration["mode"] in ("minimum", "exact")
                    and _positive(duration["seconds"]),
                    oid,
                    "Invalid duration",
                )
            require(
                start is None or window is None or window[0] <= start < window[1],
                oid,
                "Impossible time conjunction",
            )
            if item["match"] == "single_visit":
                single_times.setdefault((item["subject_ref"], item["date"]), []).append(conditions)
    for subject, ranges in totals.items():
        lower = max(low for low, _ in ranges)
        uppers = [high for _, high in ranges if high is not None]
        upper = min(uppers) if uppers else None
        minima, forced_dates, eligible_dates, date_maxima = 0, 0, 0, []
        for day in days:
            entries = dated.get((subject, day), [])
            lo = max((low for low, _ in entries), default=0)
            hi = [high for _, high in entries if high is not None]
            if day in exclusions.get(subject, set()):
                hi.append(0)
            require(not hi or lo <= min(hi), subject, "Contradictory dated requirements")
            minima += lo
            forced_dates += int(lo > 0)
            eligible_dates += int(not hi or min(hi) > 0)
            date_maxima.append(min(hi) if hi else None)
        require(upper is None or max(lower, minima) <= upper, subject, "Contradictory visit quotas")
        require(
            any(high is None for high in date_maxima) or lower <= sum(date_maxima),
            subject,
            "Dated exact counts cannot meet global minimum",
        )
        max_distinct = (
            eligible_dates if upper is None else min(eligible_dates, upper - minima + forced_dates)
        )
        require(
            distinct.get(subject, 0) <= max_distinct, subject, "Contradictory distinct-date quota"
        )
        require(
            exclusions.get(subject, set()) != days,
            subject,
            "Required visit excluded from whole trip",
        )
    for (subject, _), conditions in single_times.items():
        starts = {_clock(c["start_at"], subject) for c in conditions if "start_at" in c}
        windows = [_window(c["within"], subject) for c in conditions if "within" in c]
        exact = {
            c["duration"]["seconds"]
            for c in conditions
            if c.get("duration", {}).get("mode") == "exact"
        }
        minimum = max((c["duration"]["seconds"] for c in conditions if "duration" in c), default=0)
        require(
            len(starts) <= 1 and len(exact) <= 1 and (not exact or next(iter(exact)) >= minimum),
            subject,
            "Contradictory single-visit time conditions",
        )
        if windows:
            low, high = max(w[0] for w in windows), min(w[1] for w in windows)
            require(
                low < high and (not starts or low <= next(iter(starts)) < high),
                subject,
                "Disjoint single-visit time windows",
            )
    for item in spec["obligations"]:
        if (
            item["resolution"] == "resolved"
            and item["kind"] == "fixed_visit_time"
            and item["match"] == "at_least_one"
        ):
            require(
                not any(high == 1 for _, high in totals.get(item["subject_ref"], [])),
                item["obligation_id"],
                "Repeat selector conflicts with exact-one quota",
            )
    seen = set()
    for item in spec["unresolved_items"]:
        require(
            isinstance(item, dict)
            and text(item.get("item_id"))
            and item["item_id"] not in seen
            and text(item.get("reason")),
            "unresolved_items",
            "Invalid annotation",
        )
        seen.add(item["item_id"])
        _sources(item.get("source_refs"), original, item["item_id"])
        require(
            "classification" not in item or item["classification"] == "soft_preference",
            item["item_id"],
            "Unknown annotation classification",
        )
        require(
            "obligation_ref" not in item
            or text(item["obligation_ref"])
            and item["obligation_ref"] in ids,
            item["item_id"],
            "Unknown annotation parent",
        )
        require(
            not ("obligation_ref" in item and "classification" in item),
            item["item_id"],
            "Annotation has contradictory linkage",
        )
        incomplete |= "obligation_ref" not in item and "classification" not in item
    return incomplete


def _validate_time_capacity(group, timezone):
    if timezone is None:
        return
    combined = {}
    for item in group["requirement_spec"]["obligations"]:
        if item["resolution"] != "resolved" or item["kind"] != "fixed_visit_time":
            continue
        key = (
            (item["subject_ref"], item["date"])
            if item["match"] == "single_visit"
            else (item["obligation_id"], item["date"])
        )
        combined.setdefault(key, []).append(item["conditions"])
    for (subject, day), conditions in combined.items():
        windows = [condition["within"] for condition in conditions if "within" in condition]
        durations = [
            condition["duration"]["seconds"] for condition in conditions if "duration" in condition
        ]
        if not durations:
            continue
        if not windows:
            windows = [{"start": "00:00", "end": "24:00"}]
        low = max((_clock(w["start"], subject), w["start"]) for w in windows)[1]
        high = min((_clock(w["end"], subject, end=True), w["end"]) for w in windows)[1]
        starts = [condition["start_at"] for condition in conditions if "start_at" in condition]
        interval = expand_protection(
            {
                "date": day,
                "interval": {"kind": "clock", "start": starts[0] if starts else low, "end": high},
            },
            timezone,
        )
        if interval.span:
            require(
                max(durations) <= interval.span.seconds,
                subject,
                "Impossible elapsed duration within window",
            )


def _identity_ready(intake, identity):
    refs = identity_references(intake)
    if not isinstance(identity, dict) or (
        identity.get("status") not in ("complete", "needs_adjudication")
        or identity.get("schema_version") != "rtpeval_identity_1"
        or identity.get("subject_scope_version") != SUBJECT_SCOPE_VERSION
        or identity.get("reference_set_digest") != stable_id(refs)
        or identity.get("source_hashes") != intake["source_hashes"]
        or (identity.get("batch_id"), identity.get("batch_revision"))
        != (intake["batch_id"], intake["revision"])
    ):
        return False
    records = identity.get("records")
    if not isinstance(records, list) or len(records) != len(refs):
        return False
    for key in ("evidence_hash", "audit_plan_hash"):
        if not text(identity.get(key)) or not re.fullmatch(r"[0-9a-f]{64}", identity[key]):
            return False
    if (
        "review_hash" not in identity
        or identity["review_hash"] is not None
        and (
            not text(identity["review_hash"])
            or not re.fullmatch(r"[0-9a-f]{64}", identity["review_hash"])
        )
    ):
        return False
    for item in records:
        if not isinstance(item, dict) or not text(item.get("reference_id")):
            return False
        if item.get("resolution") not in ("resolved", "unresolved"):
            return False
        if item["resolution"] == "resolved" and not text(item.get("canonical_place_id")):
            return False
        if item["resolution"] == "unresolved" and item.get("canonical_place_id") is not None:
            return False
        if (
            type(item.get("high_impact")) is not bool
            or type(item.get("audit_selected")) is not bool
        ):
            return False
        if item["resolution"] == "resolved" and (item["high_impact"] or item["audit_selected"]):
            if item.get("decision_route") != "human_adjudication" or not item.get("review_history"):
                return False
    indexed = {item["reference_id"]: item for item in records}
    if len(indexed) != len(refs):
        return False
    return all(
        ref["reference_id"] in indexed
        and all(
            indexed[ref["reference_id"]].get(key) == ref[key]
            for key in ("source", "kind", "group_id", "version", "projection", "audit_key")
        )
        for ref in refs
    )


def _review_provenance(record, pointer):
    require(
        text(record.get("reviewer_ref")) and text(record.get("reviewed_at")),
        pointer,
        "Review provenance is required",
    )
    try:
        parsed = datetime.fromisoformat(record["reviewed_at"])
    except ValueError:
        parsed = None
    require(
        parsed is not None and parsed.utcoffset() is not None,
        pointer,
        "Review timestamp requires an offset",
    )


def _context(intake, envelope):
    if envelope is None:
        return {}
    require(
        isinstance(envelope, dict)
        and envelope.get("schema_version") == "rtpeval_schedule_context_1"
        and envelope.get("batch_id") == intake["batch_id"]
        and text(envelope.get("revision"))
        and isinstance(envelope.get("groups"), list),
        "context",
        "Invalid time context envelope",
    )
    groups = {group["group_id"]: group for group in intake["inventory"]}
    zones = {}
    for record in envelope["groups"]:
        require(
            isinstance(record, dict) and text(record.get("group_id")), "context", "Invalid group"
        )
        gid = record["group_id"]
        require(
            gid in groups
            and gid not in zones
            and record.get("input_sha256") == groups[gid]["input_sha256"],
            "context",
            "Stale/duplicate context group",
        )
        require(
            text(record.get("source_ref")) and text(record.get("timezone")),
            gid,
            "Independent zone evidence reference required",
        )
        _review_provenance(record, gid)
        try:
            ZoneInfo(record["timezone"])
        except (ZoneInfoNotFoundError, ValueError):
            require(False, gid, "Unknown IANA timezone")
        zones[gid] = record["timezone"]
    return zones


def _occupancy_reviews(intake, envelope):
    if envelope is None:
        return []
    require(
        isinstance(envelope, dict)
        and envelope.get("schema_version") == "rtpeval_occupancy_reviews_1"
        and envelope.get("batch_id") == intake["batch_id"]
        and text(envelope.get("revision"))
        and isinstance(envelope.get("records"), list),
        "occupancy_reviews",
        "Invalid review envelope",
    )
    sources = {}
    for group in intake["inventory"]:
        for run in group["runs"].values():
            projections = [run["final"], *(p for p in run.get("optional", {}).values() if p)]
            for projection in projections:
                for activity in projection["activities"]:
                    sources[activity["source"]["record_id"]] = (activity, group)
    seen = set()
    allowed = {
        "source",
        "revision",
        "reviewer_ref",
        "reviewed_at",
        "rationale",
        "occupancy",
        "protected_obligation_refs",
    }
    for item in envelope["records"]:
        require(
            isinstance(item, dict)
            and set(item) <= allowed
            and isinstance(item.get("source"), dict),
            "occupancy_reviews",
            "Review may only decide occupancy and correspondence",
        )
        source = item["source"]
        key = source.get("record_id")
        require(
            text(key)
            and key in sources
            and key not in seen
            and source == sources[key][0]["source"],
            "occupancy_reviews",
            "Stale/duplicate activity source",
        )
        seen.add(key)
        activity, group = sources[key]
        require(
            text(item.get("revision")) and text(item.get("rationale")),
            key,
            "Review identity/rationale missing",
        )
        _review_provenance(item, key)
        require(
            item.get("occupancy") in ("committed", "uncommitted", "unresolved"),
            key,
            "Invalid occupancy",
        )
        require(
            activity["evaluation_role"] != "transport",
            key,
            "Transport cannot receive occupancy reviews",
        )
        if activity["evaluation_role"] == "primary_visit":
            require(item["occupancy"] == "committed", key, "Primary visits remain commitments")
        refs = item.get("protected_obligation_refs", [])
        require(
            isinstance(refs, list)
            and all(text(ref) for ref in refs)
            and len(set(refs)) == len(refs),
            key,
            "Invalid protection links",
        )
        if refs:
            protections = {
                p["obligation_id"]: p
                for p in group["requirement_spec"]["obligations"]
                if p["kind"] == "protected_time"
            }
            require(
                activity["evaluation_role"] == "transition"
                and item["occupancy"] == "uncommitted"
                and all(ref in protections for ref in refs),
                key,
                "Contradictory protection correspondence",
            )
            linked = [protections[ref] for ref in refs]
            require(
                all(
                    p.get("date", activity["declared_day"]) == activity["declared_day"]
                    for p in linked
                )
                and len({p.get("scope") for p in linked}) == 1,
                key,
                "Protection links require same date/scope",
            )
    return envelope["records"]


def _conjunction(states):
    return "FAIL" if "FAIL" in states else "PASS" if all(s == "PASS" for s in states) else "UNKNOWN"


def _count_component(lower, upper, mode, target, kind="count"):
    if mode == "minimum":
        state = "PASS" if lower >= target else "FAIL" if upper < target else "UNKNOWN"
    else:
        state = (
            "PASS"
            if lower == upper == target
            else ("FAIL" if lower > target or upper < target else "UNKNOWN")
        )
    return {
        "kind": kind,
        "state": state,
        "bounds": {"lower": lower, "upper": upper},
        "mode": mode,
        "target": target,
    }


def _count_matches(confirmed, potential, mode, target, kind="count"):
    return {
        **_count_component(len(confirmed), len(confirmed) + len(potential), mode, target, kind),
        "confirmed_sources": [item["activity"]["source"] for item in confirmed],
        "potential_sources": [item["activity"]["source"] for item in potential],
    }


def _occurrences(projection, identity_index, timezone):
    result, seen = [], set()
    for activity in projection["activities"]:
        key = activity["source"]["record_id"]
        if key in seen or activity["evaluation_role"] not in ("primary_visit", "unresolved"):
            continue
        seen.add(key)
        raw = activity["original"]
        interval = normalize_interval(
            raw.get("start_time"), raw.get("end_time"), activity["declared_day"], timezone
        )
        record = identity_index.get(key, {})
        result.append(
            {
                "activity": activity,
                "interval": interval,
                "primary": activity["evaluation_role"] == "primary_visit",
                "canonical_id": record.get("canonical_place_id")
                if record.get("resolution") == "resolved"
                else None,
            }
        )
    return result


def _matches(occurrences, canonical, days):
    confirmed, potential = [], []
    for item in occurrences:
        activity = item["activity"]
        consistent = item["interval"].date_consistent
        if consistent and activity["declared_day"] not in days:
            continue
        adopted = item["canonical_id"]
        if item["primary"] and canonical and adopted and canonical != adopted:
            continue
        if item["primary"] and canonical and adopted == canonical and consistent:
            confirmed.append(item)
        else:
            potential.append(item)
    return confirmed, potential


def _time_conditions(item, conditions, timezone):
    interval = item["interval"]
    components = []
    for kind, value in conditions.items():
        state, reason = "UNKNOWN", None
        if interval.span is None:
            reason = "time_unresolved"
        elif kind == "duration":
            seconds = interval.span.seconds
            ok = (
                seconds == value["seconds"]
                if value["mode"] == "exact"
                else seconds >= value["seconds"]
            )
            state = "PASS" if ok else "FAIL"
        elif not timezone:
            reason = "timezone_missing"
        else:
            local_start = interval.span.start.astimezone(ZoneInfo(timezone))
            local_end = interval.span.end.astimezone(ZoneInfo(timezone))
            start_seconds = (
                local_start.hour * 3600
                + local_start.minute * 60
                + local_start.second
                + local_start.microsecond / 1e6
            )
            end_seconds = (
                local_end.hour * 3600
                + local_end.minute * 60
                + local_end.second
                + local_end.microsecond / 1e6
            )
            if kind == "start_at":
                ok = start_seconds == _clock(value, "start_at")
            else:
                first, last = _window(value, "within")
                ok = first <= start_seconds and end_seconds <= last
            state = "PASS" if ok else "FAIL"
        components.append(
            {"kind": kind, "state": state, "reason": reason, "interval": interval.to_dict()}
        )
    return _conjunction([c["state"] for c in components]), components


def _fixed_components(obligation, occurrences, canonical, days, timezone):
    confirmed, potential = _matches(occurrences, canonical, [obligation["date"]])
    evaluated = []
    for item in confirmed:
        state, components = _time_conditions(item, obligation["conditions"], timezone)
        evaluated.append(
            {"source": item["activity"]["source"], "state": state, "components": components}
        )
    possible_compliant = [
        item
        for item in potential
        if _time_conditions(item, obligation["conditions"], timezone)[0] != "FAIL"
    ]
    state = (
        "PASS"
        if any(item["state"] == "PASS" for item in evaluated)
        else (
            "UNKNOWN"
            if possible_compliant or any(item["state"] == "UNKNOWN" for item in evaluated)
            else "FAIL"
        )
    )
    components = [
        {
            "kind": "dated_time_conjunction",
            "state": state,
            "date": obligation["date"],
            "visits": evaluated,
            "potential_sources": [p["activity"]["source"] for p in potential],
        }
    ]
    if obligation["match"] == "single_visit":
        all_confirmed, all_potential = _matches(occurrences, canonical, days)
        components.insert(
            0,
            _count_matches(all_confirmed, all_potential, "exact", 1),
        )
    return components


def _requirement_checks(group, projection, identity_index, timezone):
    days = _days(group["input"])
    occurrences = _occurrences(projection, identity_index, timezone)
    subjects = {
        item["source"].get("subject_id"): item.get("canonical_place_id")
        for item in identity_index.values()
        if item["kind"] == "requirement_subject"
        and item["group_id"] == group["group_id"]
        and item["resolution"] == "resolved"
    }
    checks = []
    for obligation in group["requirement_spec"]["obligations"]:
        components = []
        kind = obligation["kind"]
        if kind not in OBLIGATION_FIELDS:
            continue
        if obligation["resolution"] != "resolved":
            components.append(
                {
                    "kind": kind,
                    "state": "UNKNOWN",
                    "reason": obligation.get("reason", "semantics_unresolved"),
                }
            )
        elif kind == "required_visit":
            confirmed, possible = _matches(
                occurrences, subjects.get(obligation["subject_ref"]), days
            )
            count = obligation["count"]
            components.append(_count_matches(confirmed, possible, count["mode"], count["value"]))
            if obligation.get("distinct_dates"):
                lower = {item["activity"]["declared_day"] for item in confirmed}
                upper = lower | {
                    item["activity"]["declared_day"]
                    for item in possible
                    if item["interval"].date_consistent
                }
                if any(not item["interval"].date_consistent for item in possible):
                    upper |= set(days)
                # One uncertain occurrence cannot establish multiple distinct dates.
                upper_count = min(len(upper), len(confirmed) + len(possible))
                components.append(
                    _count_component(
                        len(lower), upper_count, "minimum", count["value"], "distinct_dates"
                    )
                )
            for dated in obligation.get("date_obligations", []):
                matches, uncertain = _matches(
                    occurrences, subjects.get(obligation["subject_ref"]), [dated["date"]]
                )
                component = _count_matches(
                    matches, uncertain, dated["count_mode"], dated["count"], "dated_count"
                )
                component["date"] = dated["date"]
                components.append(component)
        elif kind == "excluded_visit":
            scope = days if obligation["scope"] == "whole_trip" else obligation["dates"]
            confirmed, possible = _matches(
                occurrences, subjects.get(obligation["subject_ref"]), scope
            )
            components.append(
                {
                    "kind": "exclusion",
                    "state": "FAIL" if confirmed else "UNKNOWN" if possible else "PASS",
                    "bounds": {"lower": len(confirmed), "upper": len(confirmed) + len(possible)},
                    "confirmed_sources": [item["activity"]["source"] for item in confirmed],
                    "potential_sources": [item["activity"]["source"] for item in possible],
                }
            )
        elif kind == "fixed_visit_time":
            components = _fixed_components(
                obligation, occurrences, subjects.get(obligation["subject_ref"]), days, timezone
            )
        else:
            components.append({"kind": kind, "state": "UNKNOWN", "reason": "pending_check"})
        checks.append(
            {
                "check_id": stable_id([projection["context"], obligation["obligation_id"]]),
                "obligation_id": obligation["obligation_id"],
                "kind": kind,
                "applicability": "applicable",
                "sources": obligation["source_refs"],
                "components": components,
                "state": _conjunction([c["state"] for c in components]),
            }
        )
    return checks, occurrences


def _dimension(checks, denominator_unresolved=False, reasons=()):
    counts = {
        state: sum(item["state"] == state for item in checks)
        for state in ("PASS", "FAIL", "UNKNOWN")
    }
    denominator = len(checks)
    return {
        "checks": checks,
        "counts": counts,
        "known_unit_count": denominator,
        "denominator_unresolved": denominator_unresolved,
        "denominator": None if denominator_unresolved else denominator,
        "state": "UNKNOWN"
        if denominator_unresolved
        else (_conjunction([item["state"] for item in checks]) if checks else "N/A"),
        "verified_fraction": counts["PASS"] / denominator
        if denominator and not denominator_unresolved
        else None,
        "reasons": list(reasons),
    }


def _descriptive(group, projection, occurrences):
    days = _days(group["input"])
    density, known_days, unknown_days = [], set(), set()
    for day in days:
        known = [
            item
            for item in occurrences
            if item["primary"]
            and item["interval"].date_consistent
            and item["activity"]["declared_day"] == day
        ]
        possible = [
            item
            for item in occurrences
            if not item["interval"].date_consistent
            or not item["primary"]
            and item["activity"]["declared_day"] == day
        ]
        lower, upper = len(known), len(known) + len(possible)

        def category(count):
            return "<2" if count < 2 else "2..5" if count <= 5 else ">5"

        density.append(
            {
                "date": day,
                "known_primary_count": lower,
                "possible_primary_count": len(possible),
                "category": category(lower) if category(lower) == category(upper) else None,
            }
        )
        if known:
            known_days.add(day)
        elif possible:
            unknown_days.add(day)
    groups, unidentified = {}, 0
    for item in occurrences:
        if not item["interval"].date_consistent:
            unidentified += 1
            continue
        day = item["activity"]["declared_day"]
        if day not in days:
            continue
        if not item["primary"] or not item["canonical_id"]:
            unidentified += 1
            continue
        canonical = item["canonical_id"]
        groups.setdefault(canonical, {}).setdefault(day, []).append(item["activity"]["source"])
    venues = []
    for canonical, dates in sorted(groups.items()):
        count = sum(len(sources) for sources in dates.values())
        venues.append(
            {
                "canonical_place_id": canonical,
                "occurrence_count": count,
                "date_count": len(dates),
                "extra_occurrences": count - 1,
                "within_day_extras": sum(len(sources) - 1 for sources in dates.values()),
                "across_day_extras": len(dates) - 1,
                "dates": dates,
            }
        )
    coverage = {
        "requested_day_count": len(days),
        "declared_day_present_count": len(set(projection["declared_days"]) & set(days)),
        "any_activity_day_count": len(
            {a["declared_day"] for a in projection["activities"]} & set(days)
        ),
        "known_primary_day_count": len(known_days),
        "unknown_primary_day_count": len(unknown_days),
        "empty_primary_day_count": len(days) - len(known_days) - len(unknown_days),
        "extra_declared_days": sorted(set(projection["declared_days"]) - set(days)),
    }
    return {
        "coverage": coverage,
        "density": density,
        "repetition": {
            "venues": venues,
            "repeated_venue_count": sum(v["occurrence_count"] > 1 for v in venues),
            "known_identity_occurrences": sum(v["occurrence_count"] for v in venues),
            "unknown_identity_occurrences": unidentified,
            "extra_occurrences": sum(v["extra_occurrences"] for v in venues),
            "within_day_extras": sum(v["within_day_extras"] for v in venues),
            "across_day_extras": sum(v["across_day_extras"] for v in venues),
            "status": "lower_bound" if unidentified else "complete",
            "reviewed_revisit_obligations": [
                item
                for item in group["requirement_spec"]["obligations"]
                if item["kind"] == "required_visit"
            ],
        },
    }


def _daily_measures(measures, requested_days, timezone):
    if not timezone:
        measures["daily"] = None
        measures["daily_availability_reason"] = "timezone_missing"
        return
    keys = (
        "scheduled_occupied",
        "protected_reserved",
        "commitment_conflict",
        "protection_conflict",
        "combined_conflict",
    )
    days = set(requested_days)
    zone = ZoneInfo(timezone)
    for key in keys:
        for raw in measures[key]["intervals"]:
            span = read_span(raw)
            start, end = span.start.astimezone(zone).date(), span.end.astimezone(zone).date()
            days.update(
                (start + timedelta(days=i)).isoformat() for i in range((end - start).days + 1)
            )
    daily = {}
    for day in sorted(days):
        boundary = expand_protection({"date": day, "interval": {"kind": "full_day"}}, timezone)
        if boundary.span is None:
            daily[day] = {"availability_reason": "local_midnight_unresolved"}
            continue
        daily[day] = {}
        for key in keys:
            measure = measures[key]
            spans = intersections([read_span(raw) for raw in measure["intervals"]], [boundary.span])
            daily[day][key] = {
                "seconds": sum(span.seconds for span in spans)
                if spans or measure["status"] == "complete"
                else None,
                "status": measure["status"],
                "unknown_record_count": measure["unknown_record_count"],
                "intervals": [span.to_dict() for span in spans],
            }
    measures["daily"] = daily
    measures["daily_availability_reason"] = None


def score_requirement_schedule(
    intake, identity_report, schedule_context=None, occupancy_reviews=None, *, paired=False
):
    """Evaluate a whole accepted batch; material correction never returns a partial cohort."""
    prepared, identity = _value(intake), _value(identity_report)
    schedule_context, occupancy_reviews = _value(schedule_context), _value(occupancy_reviews)
    base = {
        "schema_version": REPORT_VERSION,
        "batch_id": prepared.get("batch_id"),
        "batch_revision": prepared.get("revision"),
        "rules_version": RULES_VERSION,
        "rules_hash": stable_id(RULES),
        "results": [],
        "diagnostics": [],
    }
    try:
        require(prepared.get("status") == "accepted", "intake", "Accepted intake is required")
        completeness = {group["group_id"]: _validate_spec(group) for group in prepared["inventory"]}
        zones = _context(prepared, schedule_context)
        for group in prepared["inventory"]:
            _validate_time_capacity(group, zones.get(group["group_id"]))
        reviews = _occupancy_reviews(prepared, occupancy_reviews)
        if not _identity_ready(prepared, identity):
            base["diagnostics"] = [{"reason": "identity_replay_required"}]
            return RequirementScheduleResult("identity_replay_required", freeze(base))
        identity_index = {item["reference_id"]: item for item in identity["records"]}
        results = []
        for group in prepared["inventory"]:
            for version, run in group["runs"].items():
                projections = [("final", run["final"])]
                if paired and version == "v3":
                    projections.extend((label, p) for label, p in run["optional"].items() if p)
                for label, projection in projections:
                    zone = zones.get(group["group_id"])
                    checks, occurrences = _requirement_checks(
                        group, projection, identity_index, zone
                    )
                    occupancy = prepare_occupancy(
                        projection, group["requirement_spec"]["obligations"], zone, reviews
                    )
                    non_overlap, protections, measures = assess_occupancy(occupancy)
                    _daily_measures(measures, _days(group["input"]), zone)
                    for check in checks:
                        if check["kind"] == "protected_time":
                            state = protections[check["obligation_id"]]
                            check["state"] = state
                            check["components"] = [{"kind": "protected_conflict", "state": state}]
                    results.append(
                        {
                            "group_id": group["group_id"],
                            "version": version,
                            "projection": label,
                            "run_id": projection["context"]["run_id"],
                            "projection_id": stable_id(
                                [projection["context"], projection["projection"]]
                            ),
                            "source_hashes": {
                                "input": group["input_sha256"],
                                "requirement_spec": group["requirement_spec_sha256"],
                                "result": projection["context"]["artifact_sha256"],
                                "identity_report": stable_id(identity),
                                "identity_evidence": identity["evidence_hash"],
                                "identity_review": identity["review_hash"],
                                "identity_audit": identity["audit_plan_hash"],
                                "identity_references": identity["reference_set_digest"],
                                "schedule_context": stable_id(schedule_context)
                                if schedule_context
                                else None,
                                "occupancy_review": stable_id(occupancy_reviews)
                                if occupancy_reviews
                                else None,
                                "rules": base["rules_hash"],
                            },
                            "preparation_revisions": {
                                "context": schedule_context.get("revision")
                                if schedule_context
                                else None,
                                "occupancy_review": occupancy_reviews.get("revision")
                                if occupancy_reviews
                                else None,
                            },
                            "requirements": {
                                **_dimension(
                                    checks,
                                    completeness[group["group_id"]],
                                    ["requirement_completeness_unresolved"]
                                    if completeness[group["group_id"]]
                                    else [],
                                ),
                                "unclassified_obligations": [
                                    item
                                    for item in group["requirement_spec"]["obligations"]
                                    if item["kind"] not in OBLIGATION_FIELDS
                                ],
                            },
                            "non_overlap": {
                                **_dimension(
                                    non_overlap,
                                    bool(occupancy.candidates),
                                    ["commitment_denominator_unresolved"]
                                    if occupancy.candidates
                                    else [],
                                ),
                                "candidate_unit_count": len(occupancy.candidates),
                            },
                            "schedule_measures": measures,
                            "descriptive": _descriptive(group, projection, occurrences),
                            "occupancy": occupancy.to_dict(),
                        }
                    )
        base["results"] = results
        return RequirementScheduleResult("complete", freeze(base))
    except MaterialError as exc:
        base["diagnostics"] = [exc.diagnostic]
        return RequirementScheduleResult("needs_material_correction", freeze(base))
