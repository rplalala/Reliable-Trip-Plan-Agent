"""Deterministic V1-A acquisition, normalization, budgeting, and deduplication."""

import math
from collections import defaultdict
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import date, datetime, time
from typing import TypeVar
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from backend.app.evidence.models import (
    DestinationContext,
    EvidenceAvailability,
    NonWalkablePairEvidence,
    PlaceCandidate,
    PlaceEvidence,
    RouteElementEvidence,
    RouteElementEvidenceType,
    RouteEvidence,
    RouteEvidenceBundle,
    RouteEvidencePurpose,
    WeatherEvidence,
)
from backend.app.evidence.normalization import (
    normalize_place_candidate,
    normalize_place_details,
    normalize_routes,
    normalize_weather,
    unavailable_place_details,
    unavailable_routes,
    unavailable_weather,
)
from backend.app.integrations.google.places import (
    PLACES_CANDIDATE_FIELD_MASK,
    PLACES_DETAILS_FIELD_MASK,
)
from backend.app.integrations.google.routes import ROUTE_MATRIX_FIELD_MASK
from backend.app.integrations.models import (
    LatLng,
    PlaceDetailsDTO,
    PlaceDetailsRequest,
    PlaceSearchRequest,
    PlaceSearchResponse,
    RouteMatrixDTO,
    RouteMatrixRequest,
    RouteWaypoint,
    WeatherForecastDTO,
    WeatherRequest,
)
from backend.app.integrations.protocols import PlacesProvider, RoutesProvider, WeatherProvider
from backend.app.observability.run_trace import RunTracer, TracePayloadMode
from backend.app.policies.transport import (
    MAX_WALK_DISTANCE_METERS,
    MAX_WALK_DURATION_SECONDS,
    DirectedWalkTrigger,
    TransportModeDecision,
    TravelMode,
    collapse_non_walkable_pairs,
    find_directed_non_walkable_pairs,
    select_alternative_route_pairs,
)
from backend.app.policies.trip_dates import TRIP_DATE_WINDOW_DAYS
from backend.app.runtime.budget import ToolBudget, ToolBudgetKey
from backend.app.runtime.cache import RequestCache
from backend.app.schemas.request import TravelRequirements

ValueT = TypeVar("ValueT")
_CLOSED_STATUSES = {"CLOSED_TEMPORARILY", "CLOSED_PERMANENTLY", "FUTURE_OPENING"}
_GENERIC_SEARCH_TERMS = (
    "top attractions",
    "local food",
    "museums and cultural attractions",
)
_EXPERIENCE_PREFERENCE_MARKERS = (
    "accessib",
    "crowd",
    "family",
    "quiet",
    "queue",
    "visit duration",
    "walking",
)


class NoViableCandidatesError(RuntimeError):
    """External acquisition could not produce a usable destination or POI shortlist."""


@dataclass(frozen=True)
class _ProviderResult[ValueT]:
    value: ValueT | None = None
    error_type: str | None = None


class V1EvidenceAcquisitionService:
    """Application-controlled external evidence pipeline for one V1 run."""

    def __init__(
        self,
        *,
        places_provider: PlacesProvider,
        weather_provider: WeatherProvider,
        routes_provider: RoutesProvider,
        budget: ToolBudget,
        cache: RequestCache,
        tracer: RunTracer,
    ) -> None:
        self._places = places_provider
        self._weather = weather_provider
        self._routes = routes_provider
        self._budget = budget
        self._cache = cache
        self._tracer = tracer

    async def _cached_provider_call(
        self,
        *,
        key: tuple[object, ...],
        budget_key: ToolBudgetKey | None,
        budget_amount: int,
        additional_budget_charges: tuple[tuple[ToolBudgetKey, int], ...] = (),
        factory: Callable[[], Awaitable[ValueT]],
    ) -> _ProviderResult[ValueT]:
        async def load() -> _ProviderResult[ValueT]:
            charges = additional_budget_charges
            if budget_key is not None:
                charges = ((budget_key, budget_amount), *charges)
            self._budget.consume_many(charges)
            try:
                return _ProviderResult(value=await factory())
            except Exception as exc:
                return _ProviderResult(error_type=type(exc).__name__)

        result, cache_hit = await self._cache.get_or_create(key, load)
        self._tracer.event(
            "request_cache_lookup",
            {"operation": str(key[0]), "cache_hit": cache_hit},
        )
        return result

    async def _search_places(self, request: PlaceSearchRequest) -> PlaceSearchResponse:
        key = (
            "places_search",
            request.text_query.casefold(),
            request.page_size,
            request.field_mask,
            (
                request.location_bias.latitude,
                request.location_bias.longitude,
            )
            if request.location_bias is not None
            else None,
            request.language_code,
        )
        result = await self._cached_provider_call(
            key=key,
            budget_key=ToolBudgetKey.PLACE_SEARCH_CALLS,
            budget_amount=1,
            factory=lambda: self._places.search_text(request),
        )
        if result.value is None:
            raise RuntimeError(f"Places provider unavailable ({result.error_type})")
        return result.value

    async def resolve_destination(self, destination: str) -> DestinationContext:
        """Resolve one destination coordinate using the same minimal candidate mask."""

        try:
            response = await self._search_places(
                PlaceSearchRequest(
                    text_query=destination,
                    page_size=1,
                    field_mask=PLACES_CANDIDATE_FIELD_MASK,
                )
            )
        except RuntimeError as exc:
            raise NoViableCandidatesError("Destination provider was unavailable") from exc
        if not response.candidates:
            raise NoViableCandidatesError("Destination could not be resolved")
        candidate = response.candidates[0]
        return DestinationContext(
            place_id=candidate.place_id,
            name=candidate.display_name,
            formatted_address=candidate.formatted_address,
            latitude=candidate.location.latitude,
            longitude=candidate.location.longitude,
        )

    def _candidate_queries(self, requirements: TravelRequirements) -> list[tuple[str, str]]:
        terms: list[str] = []
        known_terms: set[str] = set()
        planning_preferences = [
            value
            for value in requirements.preferences
            if not any(
                marker in value.casefold() for marker in _EXPERIENCE_PREFERENCE_MARKERS
            )
        ]
        for value in [*requirements.required_activities, *planning_preferences]:
            cleaned = " ".join(value.split())[:80]
            if cleaned and cleaned.casefold() not in known_terms:
                terms.append(cleaned)
                known_terms.add(cleaned.casefold())
        for fallback in _GENERIC_SEARCH_TERMS:
            if len(terms) >= 3:
                break
            if fallback.casefold() not in known_terms:
                terms.append(fallback)
                known_terms.add(fallback.casefold())

        max_queries = min(3, self._budget.remaining(ToolBudgetKey.PLACE_SEARCH_CALLS))
        return [
            (f"category_{index + 1}", f"{term} in {requirements.destination}")
            for index, term in enumerate(terms[:max_queries])
        ]

    async def search_candidates(
        self,
        requirements: TravelRequirements,
        destination: DestinationContext,
    ) -> list[PlaceCandidate]:
        """Run bounded category searches and deterministically deduplicate results."""

        queries = self._candidate_queries(requirements)
        if not queries:
            raise NoViableCandidatesError("No candidate search budget remains")
        page_size = min(20, math.ceil(self._budget.limits.max_candidates / len(queries)))
        candidates: list[PlaceCandidate] = []
        for category, query in queries:
            request = PlaceSearchRequest(
                text_query=query,
                page_size=page_size,
                field_mask=PLACES_CANDIDATE_FIELD_MASK,
                location_bias=LatLng(
                    latitude=destination.latitude,
                    longitude=destination.longitude,
                ),
            )
            try:
                response = await self._search_places(request)
            except RuntimeError as exc:
                self._tracer.event(
                    "places_search_failed",
                    {"category": category, "error": type(exc).__name__},
                )
                continue
            candidates.extend(
                normalize_place_candidate(item, source_query=query, category=category)
                for item in response.candidates
            )

        deduplicated: list[PlaceCandidate] = []
        seen: set[str] = set()
        for candidate in candidates:
            if candidate.place_id in seen or candidate.business_status in _CLOSED_STATUSES:
                continue
            seen.add(candidate.place_id)
            deduplicated.append(candidate)
            if len(deduplicated) == self._budget.limits.max_candidates:
                break
        if not deduplicated:
            raise NoViableCandidatesError("No viable Places candidates were found")
        self._budget.consume(ToolBudgetKey.CANDIDATES, len(deduplicated))
        return deduplicated

    def shortlist(self, candidates: list[PlaceCandidate]) -> list[PlaceCandidate]:
        """Round-robin provider-ranked categories with a stable Place ID tie-breaker."""

        route_limit = math.isqrt(self._budget.limits.max_route_matrix_elements)
        limit = min(8, self._budget.limits.max_place_detail_calls, route_limit)
        groups: dict[str, list[PlaceCandidate]] = defaultdict(list)
        category_order: list[str] = []
        for candidate in candidates:
            if candidate.category not in groups:
                category_order.append(candidate.category)
            groups[candidate.category].append(candidate)
        for values in groups.values():
            values.sort(key=lambda item: (item.provider_rank, item.place_id))

        shortlist: list[PlaceCandidate] = []
        offset = 0
        while len(shortlist) < limit:
            added = False
            for category in category_order:
                values = groups[category]
                if offset < len(values):
                    shortlist.append(values[offset])
                    added = True
                    if len(shortlist) == limit:
                        break
            if not added:
                break
            offset += 1
        if not shortlist:
            raise NoViableCandidatesError("No viable candidates remained after shortlisting")
        return shortlist

    async def enrich_places(self, shortlist: list[PlaceCandidate]) -> list[PlaceEvidence]:
        """Fetch rich details only for shortlisted Place IDs."""

        evidence: list[PlaceEvidence] = []
        for candidate in shortlist:
            request = PlaceDetailsRequest(
                place_id=candidate.place_id,
                field_mask=PLACES_DETAILS_FIELD_MASK,
            )
            key = (
                "place_details",
                request.place_id,
                request.field_mask,
                request.language_code,
            )
            result: _ProviderResult[PlaceDetailsDTO] = await self._cached_provider_call(
                key=key,
                budget_key=ToolBudgetKey.PLACE_DETAIL_CALLS,
                budget_amount=1,
                factory=lambda request=request: self._places.get_place_details(request),
            )
            if result.value is None:
                item = unavailable_place_details(
                    candidate,
                    f"Place Details unavailable ({result.error_type})",
                )
            else:
                item = normalize_place_details(result.value, candidate=candidate)
            evidence.append(item)
        self._tracer.payload(
            "evidence",
            "place_evidence",
            evidence,
            minimum_mode=TracePayloadMode.NORMALIZED,
        )
        return evidence

    async def acquire_weather(
        self,
        *,
        requirements: TravelRequirements,
        destination: DestinationContext,
        reference_date: date,
    ) -> WeatherEvidence:
        """Make at most one Daily Forecast call and retain only requested dates."""

        if requirements.start_date is None or requirements.end_date is None:
            raise ValueError("Complete trip dates are required for Weather")
        # Weather starts from the provider's current destination-local forecast day,
        # which can lag the application's fixed calendar date at day boundaries.
        # Request the full allowed horizon once, then expose only requested dates.
        horizon_days = TRIP_DATE_WINDOW_DAYS
        request = WeatherRequest(
            location=LatLng(
                latitude=destination.latitude,
                longitude=destination.longitude,
            ),
            horizon_days=horizon_days,
            requested_start=requirements.start_date,
            requested_end=requirements.end_date,
        )
        key = (
            "weather_daily",
            request.location.latitude,
            request.location.longitude,
            request.horizon_days,
            request.requested_start,
            request.requested_end,
            request.language_code,
        )
        result: _ProviderResult[WeatherForecastDTO] = await self._cached_provider_call(
            key=key,
            budget_key=ToolBudgetKey.WEATHER_CALLS,
            budget_amount=1,
            factory=lambda: self._weather.get_daily_forecast(request),
        )
        if result.value is None:
            evidence = unavailable_weather(
                request,
                requirements.destination or destination.name,
                f"Weather unavailable ({result.error_type})",
            )
        else:
            evidence = normalize_weather(
                result.value,
                request=request,
                destination=requirements.destination or destination.name,
            )
        self._tracer.payload(
            "evidence",
            "weather_evidence",
            evidence,
            minimum_mode=TracePayloadMode.NORMALIZED,
        )
        return evidence

    async def acquire_routes(
        self,
        *,
        places: list[PlaceEvidence],
        mode: TransportModeDecision,
        requirements: TravelRequirements,
    ) -> RouteEvidenceBundle:
        """Acquire one baseline matrix and bounded alternatives for default WALK."""

        waypoints = [
            RouteWaypoint(
                place_id=place.place_id,
                location=LatLng(latitude=place.latitude, longitude=place.longitude),
            )
            for place in places
        ]
        departure_time = None
        if mode.travel_mode is TravelMode.TRANSIT:
            departure_time = self._representative_departure_time(places, requirements)
        baseline_request = RouteMatrixRequest(
            origins=waypoints,
            destinations=waypoints,
            travel_mode=mode.travel_mode.value,
            routing_preference=mode.routing_preference,
            departure_time=departure_time,
            field_mask=ROUTE_MATRIX_FIELD_MASK,
        )
        if mode.travel_mode is TravelMode.TRANSIT and departure_time is None:
            baseline = unavailable_routes(
                baseline_request,
                mode_reason=mode.reason,
                reason="Transit unavailable because no valid destination timezone was found",
            )
        else:
            baseline = await self._acquire_route_matrix(
                baseline_request,
                mode_reason=mode.reason,
                purpose=RouteEvidencePurpose.BASELINE,
                budget_key=ToolBudgetKey.ROUTE_MATRIX_ELEMENTS,
            )
        self._tracer.event(
            "route_baseline_completed",
            {
                "travel_mode": baseline.travel_mode,
                "availability": baseline.availability.value,
                "element_count": len(baseline.elements),
                "representative_departure_time": baseline.representative_departure_time,
                "budget": self._route_budget_summary(),
            },
        )

        non_walkable_pairs: list[NonWalkablePairEvidence] = []
        alternatives: list[RouteEvidence] = []
        if (
            not mode.is_explicit
            and mode.travel_mode is TravelMode.WALK
            and baseline.availability is not EvidenceAvailability.UNAVAILABLE
        ):
            directed_triggers = find_directed_non_walkable_pairs(baseline)
            non_walkable_pairs = collapse_non_walkable_pairs(directed_triggers)
            selected, truncated = select_alternative_route_pairs(
                non_walkable_pairs,
                max_pairs=self._budget.remaining(ToolBudgetKey.ALTERNATIVE_ROUTE_PAIRS),
                max_calls=self._budget.remaining(
                    ToolBudgetKey.ALTERNATIVE_ROUTE_MATRIX_CALLS
                ),
            )
            alternative_departure_time = (
                self._representative_departure_time(places, requirements)
                if selected
                else None
            )
            self._trace_alternative_trigger(
                directed_triggers=directed_triggers,
                logical_pairs=non_walkable_pairs,
                selected=selected,
                truncated=truncated,
                departure_time=alternative_departure_time,
            )
            alternatives = await self._acquire_transit_alternatives(
                selected=selected,
                waypoints=waypoints,
                departure_time=alternative_departure_time,
            )
        else:
            skip_reason = (
                "explicit_transport_mode"
                if mode.is_explicit
                else "baseline_unavailable"
                if baseline.availability is EvidenceAvailability.UNAVAILABLE
                else "baseline_mode_is_not_walk"
            )
            self._tracer.event(
                "route_alternative_trigger_evaluated",
                {
                    "triggered": False,
                    "skip_reason": skip_reason,
                    "detected_directed_walk_triggers": [],
                    "collapsed_logical_pairs": [],
                    "selected_logical_pairs": [],
                    "budget_truncated_logical_pairs": [],
                    "canonical_directions": [],
                    "representative_departure_time": None,
                    "budget": self._route_budget_summary(),
                },
            )

        bundle = RouteEvidenceBundle(
            baseline=baseline,
            alternatives=alternatives,
            non_walkable_pairs=non_walkable_pairs,
        )
        self._tracer.payload(
            "evidence",
            "route_evidence_bundle",
            bundle,
            minimum_mode=TracePayloadMode.NORMALIZED,
        )
        return bundle

    @staticmethod
    def _representative_departure_time(
        places: list[PlaceEvidence], requirements: TravelRequirements
    ) -> datetime | None:
        if requirements.start_date is None:
            return None
        for place in places:
            if place.timezone_id is None:
                continue
            try:
                destination_timezone = ZoneInfo(place.timezone_id)
            except (ValueError, ZoneInfoNotFoundError):
                continue
            return datetime.combine(
                requirements.start_date,
                time(hour=12),
                tzinfo=destination_timezone,
            )
        return None

    @staticmethod
    def _route_cache_key(request: RouteMatrixRequest) -> tuple[object, ...]:
        return (
            "route_matrix",
            tuple(
                (item.place_id, item.location.latitude, item.location.longitude)
                for item in request.origins
            ),
            tuple(
                (item.place_id, item.location.latitude, item.location.longitude)
                for item in request.destinations
            ),
            request.travel_mode,
            request.routing_preference,
            request.departure_time,
            request.field_mask,
        )

    async def _acquire_route_matrix(
        self,
        request: RouteMatrixRequest,
        *,
        mode_reason: str,
        purpose: RouteEvidencePurpose,
        budget_key: ToolBudgetKey,
        count_call: bool = False,
    ) -> RouteEvidence:
        matrix_elements = len(request.origins) * len(request.destinations)
        additional_charges = (
            ((ToolBudgetKey.ALTERNATIVE_ROUTE_MATRIX_CALLS, 1),)
            if count_call
            else ()
        )
        result: _ProviderResult[RouteMatrixDTO] = await self._cached_provider_call(
            key=self._route_cache_key(request),
            budget_key=budget_key,
            budget_amount=matrix_elements,
            additional_budget_charges=additional_charges,
            factory=lambda: self._routes.compute_route_matrix(request),
        )
        if result.value is None:
            return unavailable_routes(
                request,
                mode_reason=mode_reason,
                reason=f"Routes unavailable ({result.error_type})",
                purpose=purpose,
            )
        return normalize_routes(
            result.value,
            request=request,
            mode_reason=mode_reason,
            purpose=purpose,
        )

    async def _acquire_transit_alternatives(
        self,
        *,
        selected: list[NonWalkablePairEvidence],
        waypoints: list[RouteWaypoint],
        departure_time: datetime | None,
    ) -> list[RouteEvidence]:
        waypoint_by_id = {item.place_id: item for item in waypoints}
        destinations_by_origin: dict[str, list[str]] = {}
        for pair in selected:
            destinations_by_origin.setdefault(pair.place_id_a, []).append(pair.place_id_b)

        alternatives: list[RouteEvidence] = []
        for origin_id, destination_ids in destinations_by_origin.items():
            request = RouteMatrixRequest(
                origins=[waypoint_by_id[origin_id]],
                destinations=[waypoint_by_id[item] for item in destination_ids],
                travel_mode=TravelMode.TRANSIT.value,
                departure_time=departure_time,
                field_mask=ROUTE_MATRIX_FIELD_MASK,
            )
            if departure_time is None:
                evidence = unavailable_routes(
                    request,
                    mode_reason="selective_transit_missing_destination_timezone",
                    reason=(
                        "Transit alternative unavailable because no valid "
                        "destination timezone was found"
                    ),
                    purpose=RouteEvidencePurpose.NON_WALKABLE_ALTERNATIVE,
                )
                alternatives.append(evidence)
                self._tracer.event(
                    "route_alternative_completed",
                    {
                        "origin_place_id": origin_id,
                        "destination_place_ids": destination_ids,
                        "availability": evidence.availability.value,
                        "element_count": len(evidence.elements),
                        "provider_observed_element_count": 0,
                        "mirrored_reverse_estimate_count": 0,
                        "billable_matrix_element_count": 0,
                        "representative_departure_time": None,
                        "unavailable_reason": evidence.unavailable_reason,
                        "budget": self._route_budget_summary(),
                    },
                )
                continue
            self._tracer.event(
                "route_alternative_started",
                {
                    "origin_place_id": origin_id,
                    "destination_place_ids": destination_ids,
                    "matrix_elements": len(destination_ids),
                    "representative_departure_time": departure_time,
                },
            )
            evidence = await self._acquire_route_matrix(
                request,
                mode_reason="selective_transit_for_non_walkable_pair",
                purpose=RouteEvidencePurpose.NON_WALKABLE_ALTERNATIVE,
                budget_key=ToolBudgetKey.ALTERNATIVE_ROUTE_PAIRS,
                count_call=True,
            )
            evidence = self._with_mirrored_reverse_estimates(evidence)
            alternatives.append(evidence)
            provider_observed_count = sum(
                item.evidence_type is RouteElementEvidenceType.PROVIDER_OBSERVED
                for item in evidence.elements
            )
            mirrored_count = sum(
                item.evidence_type is RouteElementEvidenceType.MIRRORED_REVERSE_ESTIMATE
                for item in evidence.elements
            )
            self._tracer.event(
                "route_alternative_completed",
                {
                    "origin_place_id": origin_id,
                    "destination_place_ids": destination_ids,
                    "availability": evidence.availability.value,
                    "element_count": len(evidence.elements),
                    "provider_observed_element_count": provider_observed_count,
                    "mirrored_reverse_estimate_count": mirrored_count,
                    "billable_matrix_element_count": len(destination_ids),
                    "representative_departure_time": departure_time,
                    "unavailable_reason": evidence.unavailable_reason,
                    "budget": self._route_budget_summary(),
                },
            )
        return alternatives

    @staticmethod
    def _with_mirrored_reverse_estimates(evidence: RouteEvidence) -> RouteEvidence:
        mirrored = [
            RouteElementEvidence(
                origin_place_id=item.destination_place_id,
                destination_place_id=item.origin_place_id,
                evidence_type=RouteElementEvidenceType.MIRRORED_REVERSE_ESTIMATE,
                derived_from_origin_place_id=item.origin_place_id,
                derived_from_destination_place_id=item.destination_place_id,
                duration_seconds=item.duration_seconds,
                availability=EvidenceAvailability.AVAILABLE,
            )
            for item in evidence.elements
            if item.evidence_type is RouteElementEvidenceType.PROVIDER_OBSERVED
            and item.availability is EvidenceAvailability.AVAILABLE
            and item.duration_seconds is not None
            and item.origin_place_id != item.destination_place_id
        ]
        if not mirrored:
            return evidence
        return evidence.model_copy(update={"elements": [*evidence.elements, *mirrored]})

    def _trace_alternative_trigger(
        self,
        *,
        directed_triggers: list[DirectedWalkTrigger],
        logical_pairs: list[NonWalkablePairEvidence],
        selected: list[NonWalkablePairEvidence],
        truncated: list[NonWalkablePairEvidence],
        departure_time: datetime | None,
    ) -> None:
        self._tracer.event(
            "route_alternative_trigger_evaluated",
            {
                "triggered": bool(logical_pairs),
                "thresholds": {
                    "walk_distance_meters": MAX_WALK_DISTANCE_METERS,
                    "walk_duration_seconds": MAX_WALK_DURATION_SECONDS,
                },
                "detected_directed_walk_triggers": [
                    {
                        "origin_place_id": item.origin_place_id,
                        "destination_place_id": item.destination_place_id,
                        "trigger": item.trigger.value,
                        "walk_distance_meters": item.walk_distance_meters,
                        "walk_duration_seconds": item.walk_duration_seconds,
                    }
                    for item in directed_triggers
                ],
                "collapsed_logical_pairs": [
                    item.model_dump(mode="json") for item in logical_pairs
                ],
                "selected_logical_pairs": [
                    item.model_dump(mode="json") for item in selected
                ],
                "budget_truncated_logical_pairs": [
                    item.model_dump(mode="json") for item in truncated
                ],
                "canonical_directions": [
                    {
                        "origin_place_id": item.place_id_a,
                        "destination_place_id": item.place_id_b,
                    }
                    for item in selected
                ],
                "representative_departure_time": departure_time,
                "budget": self._route_budget_summary(),
            },
        )

    def _route_budget_summary(self) -> dict[str, dict[str, int]]:
        summary = self._budget.summary()
        return {
            key.value: summary[key.value]
            for key in (
                ToolBudgetKey.ROUTE_MATRIX_ELEMENTS,
                ToolBudgetKey.ALTERNATIVE_ROUTE_PAIRS,
                ToolBudgetKey.ALTERNATIVE_ROUTE_MATRIX_CALLS,
            )
        }
