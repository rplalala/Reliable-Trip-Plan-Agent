"""Versioned human facts supplement independent checks without changing execution."""

from copy import deepcopy
from datetime import UTC, datetime
from datetime import date as Date
from typing import Literal

from pydantic import Field, model_validator

from ._opening_hours import seconds, subtract
from ._route_evidence import components, conjunction, seconds_exact
from ._v3_continuity import build_continuity
from .controlled_models import FrozenModel
from .occupancy import intersections, union
from .preparation import _review_provenance
from .records import canonical_digest, require
from .schedule_time import Span, normalize_interval


class FactInterval(FrozenModel):
    start: datetime
    end: datetime

    @model_validator(mode="after")
    def positive(self):
        if self.start.utcoffset() is None or self.end.utcoffset() is None or self.end <= self.start:
            raise ValueError("Fact intervals require ordered offset-aware instants")
        return self

    def span(self):
        return Span(self.start.astimezone(UTC), self.end.astimezone(UTC))


class OpeningFact(FrozenModel):
    canonical_place_id: str = Field(min_length=1)
    date: Date
    timezone: str
    open_intervals: tuple[FactInterval, ...]
    closed_intervals: tuple[FactInterval, ...]


class RouteFact(FrozenModel):
    expected_context_hash: str = Field(min_length=64, max_length=64)
    availability: Literal["route_exists", "no_route"]
    duration_nanoseconds: int | None = Field(default=None, ge=0)
    distance_meters: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def route_values(self):
        if self.availability == "no_route" and (
            self.duration_nanoseconds is not None or self.distance_meters is not None
        ):
            raise ValueError("No-route facts cannot carry a duration or distance")
        return self


class FactualReviews(FrozenModel):
    schema_version: Literal["rtpeval_controlled_facts_1"]
    case_id: str
    case_hash: str
    replay_hash: str
    revision: str = Field(min_length=1)
    reviewer_ref: str = Field(min_length=1)
    reviewed_at: str
    rationale: str = Field(min_length=1)
    supporting_refs: tuple[str, ...] = Field(min_length=1)
    opening: tuple[OpeningFact, ...]
    routes: tuple[RouteFact, ...]


def _spans(rows):
    return [
        Span(datetime.fromisoformat(r["start"]), datetime.fromisoformat(r["end"])) for r in rows
    ]


def _opening(check, fact, provenance):
    require(
        check["timezone"]["id"] in (None, fact.timezone),
        "facts.opening",
        "Human fact contradicts established timezone evidence",
    )
    opened, closed = (
        union([i.span() for i in fact.open_intervals]),
        union([i.span() for i in fact.closed_intervals]),
    )
    require(not intersections(opened, closed), "facts.opening", "Contradictory reviewed intervals")
    for segment in check["basis_segments"]:
        require(
            not intersections(opened, _spans(segment["known_closed"]))
            and not intersections(closed, _spans(segment["known_open"])),
            "facts.opening",
            "Human fact contradicts established opening evidence",
        )
    interval = normalize_interval(
        check["interval"]["original_start"],
        check["interval"]["original_end"],
        check["declared_day"],
        fact.timezone,
        allow_cross_date=True,
    )
    require(
        check["identity_available"],
        "facts.opening",
        "Review identity through the identity channel first",
    )
    if interval.span is None:
        return check
    existing_open = _spans([r for s in check["basis_segments"] for r in s["known_open"]])
    existing_closed = _spans([r for s in check["basis_segments"] for r in s["known_closed"]])
    opened = intersections([interval.span], union(opened + existing_open))
    closed = intersections([interval.span], union(closed + existing_closed))
    unknown = seconds(subtract([interval.span], opened + closed))
    outside = seconds(closed)
    return {
        **check,
        "state": "FAIL" if outside else "UNKNOWN" if unknown else "PASS",
        "interval": interval.to_dict(),
        "basis": "controlled_human_review",
        "outside_seconds": outside if not unknown else None,
        "confirmed_outside_lower_bound_seconds": outside,
        "known_open_seconds": seconds(opened),
        "unknown_seconds": unknown,
        "factual_review": provenance,
        "reviewed_open": [s.to_dict() for s in opened],
        "reviewed_closed": [s.to_dict() for s in closed],
    }


def _route(check, fact, provenance):
    observed = {
        "state": "PASS" if fact.availability == "route_exists" else "FAIL",
        "reason": fact.availability,
        "duration_nanoseconds": fact.duration_nanoseconds,
        "distance_meters": fact.distance_meters,
    }
    original = check["observation"]
    if check["response_applicable"]:
        require(
            original["state"] == observed["state"]
            and all(
                original.get(k) is None or observed.get(k) is None or original[k] == observed[k]
                for k in ("duration_nanoseconds", "distance_meters")
            ),
            "facts.routes",
            "Human fact contradicts established route evidence",
        )
        for key in ("duration_nanoseconds", "distance_meters"):
            if observed[key] is None:
                observed[key] = original[key]
    evaluated, deficit = components(check, observed, True)
    return {
        **check,
        "state": conjunction(evaluated),
        "components": evaluated,
        "duration_nanoseconds": observed["duration_nanoseconds"],
        "duration_seconds_exact": seconds_exact(observed["duration_nanoseconds"]),
        "distance_meters": observed["distance_meters"],
        "raw_deficit_nanoseconds": deficit,
        "raw_deficit_seconds_exact": seconds_exact(deficit),
        "factual_review": provenance,
        "complete_evidence": all(c["state"] != "UNKNOWN" for c in evaluated.values()),
    }


def supplement_pair(pair, reviews, execution):
    pair = deepcopy(pair)
    if reviews is None:
        return pair, None
    facts = FactualReviews.model_validate(deepcopy(reviews))
    _review_provenance(reviews, "factual_reviews")
    require(
        (facts.case_id, facts.case_hash, facts.replay_hash)
        == (execution["case_id"], execution["case_hash"], execution["replay_hash"]),
        "factual_reviews",
        "Foreign/stale controlled facts",
    )
    provenance = {
        k: v for k, v in facts.model_dump(mode="json").items() if k not in {"opening", "routes"}
    }
    provenance["content_hash"] = canonical_digest(reviews)
    used_open, used_routes = set(), set()
    for stage in pair["stages"].values():
        for dimension in ("opening", "routes"):
            checks = stage["primary_metrics"][dimension]["checks"]
            for index, check in enumerate(checks):
                if dimension == "opening":
                    matches = [
                        (i, f)
                        for i, f in enumerate(facts.opening)
                        if (f.canonical_place_id, str(f.date))
                        == (check["canonical_place_id"], check["declared_day"])
                    ]
                    used = used_open
                    apply = _opening
                else:
                    matches = [
                        (i, f)
                        for i, f in enumerate(facts.routes)
                        if check["expected_context"]
                        and f.expected_context_hash == canonical_digest(check["expected_context"])
                    ]
                    used = used_routes
                    apply = _route
                require(
                    len(matches) <= 1,
                    "factual_reviews",
                    "Duplicate facts for an exact subject/context",
                )
                if matches:
                    i, fact = matches[0]
                    used.add(i)
                    checks[index] = apply(check, fact, provenance)
    require(
        len(used_open) == len(facts.opening) and len(used_routes) == len(facts.routes),
        "factual_reviews",
        "Fact has no applicable canonical subject/date/query",
    )
    pair["continuity"] = build_continuity(pair["stages"], pair["correspondence"])
    return pair, provenance
