"""Deterministic V1-A acquisition, normalization, budgeting, and deduplication."""

import math
from collections import defaultdict
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import date
from typing import TypeVar

from backend.app.evidence.models import (
    DestinationContext,
    PlaceCandidate,
    PlaceEvidence,
    RouteEvidence,
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
from backend.app.policies.transport import TransportModeDecision
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
        factory: Callable[[], Awaitable[ValueT]],
    ) -> _ProviderResult[ValueT]:
        async def load() -> _ProviderResult[ValueT]:
            if budget_key is not None:
                self._budget.consume(budget_key, budget_amount)
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
    ) -> RouteEvidence:
        """Make one bounded Route Matrix call for the deterministic shortlist mode."""

        waypoints = [
            RouteWaypoint(
                place_id=place.place_id,
                location=LatLng(latitude=place.latitude, longitude=place.longitude),
            )
            for place in places
        ]
        request = RouteMatrixRequest(
            origins=waypoints,
            destinations=waypoints,
            travel_mode=mode.travel_mode.value,
            routing_preference=mode.routing_preference,
            field_mask=ROUTE_MATRIX_FIELD_MASK,
        )
        matrix_elements = len(waypoints) * len(waypoints)
        key = (
            "route_matrix",
            tuple(
                (item.place_id, item.location.latitude, item.location.longitude)
                for item in waypoints
            ),
            request.travel_mode,
            request.routing_preference,
            request.field_mask,
        )
        result: _ProviderResult[RouteMatrixDTO] = await self._cached_provider_call(
            key=key,
            budget_key=ToolBudgetKey.ROUTE_MATRIX_ELEMENTS,
            budget_amount=matrix_elements,
            factory=lambda: self._routes.compute_route_matrix(request),
        )
        if result.value is None:
            evidence = unavailable_routes(
                request,
                mode_reason=mode.reason,
                reason=f"Routes unavailable ({result.error_type})",
            )
        else:
            evidence = normalize_routes(result.value, request=request, mode_reason=mode.reason)
        self._tracer.payload(
            "evidence",
            "route_evidence",
            evidence,
            minimum_mode=TracePayloadMode.NORMALIZED,
        )
        return evidence
