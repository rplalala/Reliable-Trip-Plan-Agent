"""Deterministic V1-A acquisition, normalization, budgeting, and deduplication."""

from collections.abc import Awaitable, Callable, Iterable, Sequence
from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Literal, TypeVar
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from backend.app.evidence.models import (
    DestinationContext,
    EvidenceAvailability,
    NonWalkablePairEvidence,
    PlaceEvidence,
    RouteElementEvidence,
    RouteElementEvidenceType,
    RouteEvidence,
    RouteEvidenceBundle,
    RouteEvidencePurpose,
    WeatherEvidence,
)
from backend.app.evidence.normalization import (
    merge_baseline_route_chunks,
    normalize_routes,
    normalize_weather,
    unavailable_routes,
    unavailable_weather,
)
from backend.app.evidence.selection_models import (
    PlaceSearchIntent,
    PlaceSelectionInput,
)
from backend.app.evidence.selection_normalization import (
    normalize_place_search_hit,
)
from backend.app.integrations.dispatch import ProviderNotSentError
from backend.app.integrations.google.places import (
    PLACES_CANDIDATE_FIELD_MASK,
    PLACES_DESTINATION_FIELD_MASK,
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
from backend.app.policies.route_matrix_chunking import partition_baseline_origins
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
from backend.app.runtime.budget import ToolBudget, ToolBudgetExceededError, ToolBudgetKey
from backend.app.runtime.cache import RequestCache
from backend.app.schemas.request import TravelRequirements

ValueT = TypeVar("ValueT")


class NoViableCandidatesError(RuntimeError):
    """External acquisition could not produce a usable destination or POI pool."""


class PlaceSearchUnavailableError(RuntimeError):
    def __init__(self, error_type: str | None, *, cache_hit: bool) -> None:
        self.cache_hit = cache_hit
        super().__init__(f"Places provider unavailable ({error_type})")


@dataclass(frozen=True)
class _ProviderResult[ValueT]:
    value: ValueT | None = None
    error_type: str | None = None


@dataclass(frozen=True)
class SearchIntentExecution:
    intent_id: str
    status: Literal["provider_success", "provider_failed", "budget_not_attempted"]
    cache_hit: bool = False


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
        runtime_config=None,
    ) -> None:
        self.runtime_config = runtime_config
        self._places = places_provider
        self._weather = weather_provider
        self._routes = routes_provider
        self._budget = budget
        self._cache = cache
        self._tracer = tracer
        self._counted_candidate_ids: set[str] = set()

    async def _cached_provider_call_with_status(
        self,
        *,
        key: tuple[object, ...],
        budget_key: ToolBudgetKey | None,
        budget_amount: int,
        additional_budget_charges: tuple[tuple[ToolBudgetKey, int], ...] = (),
        factory: Callable[[], Awaitable[ValueT]],
    ) -> tuple[_ProviderResult[ValueT], bool]:
        async def load() -> _ProviderResult[ValueT]:
            charges = additional_budget_charges
            if budget_key is not None:
                charges = ((budget_key, budget_amount), *charges)
            if self._cache.terminal_attempt(key):
                return _ProviderResult(error_type="previous_sent_request")
            self._cache.attempts[key] = "reserved_not_sent"
            try:
                return _ProviderResult(
                    value=await self._cache.dispatch(
                        key,
                        factory,
                        on_send=lambda: self._budget.consume_many(charges),
                        observed=key[0] in {"place_details", "places_search"}
                        and getattr(self._places, "observes_send_boundary", False),
                    )
                )
            except ProviderNotSentError as exc:
                if isinstance(exc.__cause__, ToolBudgetExceededError):
                    raise exc.__cause__ from exc
                raise
            except Exception as exc:
                return _ProviderResult(error_type=type(exc).__name__)

        result, cache_hit = await self._cache.get_or_create(key, load)
        operation = str(key[0])
        self._tracer.event(
            "request_cache_lookup",
            {
                "operation": operation,
                "cache_hit": cache_hit,
                "outcome": "success" if result.value is not None else "unavailable",
                "error_type": result.error_type,
                "requested_elements": len(key[1]) * len(key[2])
                if operation == "route_matrix"
                else None,
            },
        )
        return result, cache_hit

    async def _cached_provider_call(
        self,
        *,
        key: tuple[object, ...],
        budget_key: ToolBudgetKey | None,
        budget_amount: int,
        additional_budget_charges: tuple[tuple[ToolBudgetKey, int], ...] = (),
        factory: Callable[[], Awaitable[ValueT]],
    ) -> _ProviderResult[ValueT]:
        result, _ = await self._cached_provider_call_with_status(
            key=key,
            budget_key=budget_key,
            budget_amount=budget_amount,
            additional_budget_charges=additional_budget_charges,
            factory=factory,
        )
        return result

    async def _search_places(
        self, request: PlaceSearchRequest, *, budget_key: ToolBudgetKey
    ) -> tuple[PlaceSearchResponse, bool]:
        key = (
            "places_search",
            request.text_query.casefold(),
            request.page_size,
            request.field_mask,
            request.include_future_opening_businesses,
            (
                request.location_bias.latitude,
                request.location_bias.longitude,
            )
            if request.location_bias is not None
            else None,
            request.language_code,
        )
        result, cache_hit = await self._cached_provider_call_with_status(
            key=key,
            budget_key=budget_key,
            budget_amount=1,
            factory=lambda: self._places.search_text(request),
        )
        if result.value is None:
            raise PlaceSearchUnavailableError(result.error_type, cache_hit=cache_hit)
        return result.value, cache_hit

    async def resolve_destination(self, destination: str) -> DestinationContext:
        """Resolve one destination coordinate using the same minimal candidate mask."""

        try:
            response, _ = await self._search_places(
                PlaceSearchRequest(
                    text_query=destination,
                    page_size=1,
                    field_mask=PLACES_DESTINATION_FIELD_MASK,
                ),
                budget_key=ToolBudgetKey.DESTINATION_SEARCH_CALLS,
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

    async def search_candidate_observations(
        self,
        requirements: TravelRequirements,
        destination: DestinationContext,
        *,
        intents: Sequence[PlaceSearchIntent],
        failed_intent_ids: set[str] | None = None,
        intent_executions: list[SearchIntentExecution] | None = None,
    ) -> list[PlaceSelectionInput]:
        """Preserve each valid search hit before later merging or selection."""

        queries = [(intent.intent_id, intent.query, intent.kind) for intent in intents]
        if not queries:
            raise NoViableCandidatesError("No candidate search budget remains")
        page_size = 20
        observations: list[PlaceSelectionInput] = []
        for category, query, kind in queries:
            request = PlaceSearchRequest(
                text_query=query,
                page_size=page_size,
                field_mask=PLACES_CANDIDATE_FIELD_MASK,
                include_future_opening_businesses=True,
                location_bias=LatLng(
                    latitude=destination.latitude,
                    longitude=destination.longitude,
                ),
            )
            try:
                response, cache_hit = await self._search_places(
                    request, budget_key=ToolBudgetKey.CANDIDATE_SEARCH_CALLS
                )
            except ToolBudgetExceededError:
                execution = SearchIntentExecution(category, "budget_not_attempted")
                if intent_executions is not None:
                    intent_executions.append(execution)
                self._tracer.event(
                    "candidate_search_intent_completed",
                    {"intent_id": category, "status": execution.status, "cache_hit": False},
                )
                continue
            except PlaceSearchUnavailableError as exc:
                if failed_intent_ids is not None:
                    failed_intent_ids.add(category)
                self._tracer.event(
                    "places_search_failed",
                    {"category": category, "error": type(exc).__name__},
                )
                execution = SearchIntentExecution(category, "provider_failed", exc.cache_hit)
                if intent_executions is not None:
                    intent_executions.append(execution)
                self._tracer.event(
                    "candidate_search_intent_completed",
                    {"intent_id": category, "status": execution.status, "cache_hit": exc.cache_hit},
                )
                continue
            execution = SearchIntentExecution(category, "provider_success", cache_hit)
            if intent_executions is not None:
                intent_executions.append(execution)
            self._tracer.event(
                "candidate_search_intent_completed",
                {
                    "intent_id": category,
                    "status": execution.status,
                    "cache_hit": cache_hit,
                    "observation_count": len(response.candidates),
                },
            )
            observations.extend(
                normalize_place_search_hit(
                    item,
                    intent_id=category,
                    source_query=query,
                    actual_result_count=response.actual_result_count,
                    intent_kind=kind,
                )
                for item in response.candidates
            )
        return observations

    def _consume_new_candidates(self, place_ids: Iterable[str]) -> None:
        identifiers = set(place_ids)
        new_ids = identifiers - self._counted_candidate_ids
        self._budget.consume(ToolBudgetKey.CANDIDATES, len(new_ids))
        self._counted_candidate_ids.update(new_ids)

    async def _get_place_details(
        self, request: PlaceDetailsRequest
    ) -> _ProviderResult[PlaceDetailsDTO]:
        if self._places is None:
            raise ProviderNotSentError("Places dependency is not ready")
        return await self._cached_provider_call(
            key=self._place_details_cache_key(request),
            budget_key=ToolBudgetKey.PLACE_DETAIL_CALLS,
            budget_amount=1,
            factory=lambda: self._places.get_place_details(request),
        )

    @staticmethod
    def _place_details_cache_key(request: PlaceDetailsRequest) -> tuple[object, ...]:
        return ("place_details", request.place_id, request.field_mask, request.language_code)

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
        """Acquire a complete directed baseline and bounded default-WALK alternatives."""

        waypoints = [
            RouteWaypoint(
                place_id=place.place_id,
                location=LatLng(latitude=place.latitude, longitude=place.longitude),
            )
            for place in places
        ]
        departure_time = (
            self._representative_departure_time(places, requirements)
            if mode.travel_mode is TravelMode.TRANSIT
            else None
        )
        baseline = await self._acquire_baseline_route_chunks(
            waypoints=waypoints,
            mode=mode,
            departure_time=departure_time,
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
                max_pairs=min(
                    self._budget.remaining(ToolBudgetKey.ALTERNATIVE_ROUTE_PAIRS),
                    self._budget.remaining(ToolBudgetKey.ALTERNATIVE_ROUTE_ELEMENTS),
                ),
                max_calls=self._budget.remaining(ToolBudgetKey.ALTERNATIVE_ROUTE_MATRIX_CALLS),
            )
            alternative_departure_time = (
                self._representative_departure_time(places, requirements) if selected else None
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

    async def _acquire_baseline_route_chunks(
        self,
        *,
        waypoints: list[RouteWaypoint],
        mode: TransportModeDecision,
        departure_time: datetime | None,
    ) -> RouteEvidence:
        """Reserve each cached-miss chunk atomically and merge a complete grid."""

        fallback_reason: str | None = None
        if not waypoints:
            fallback_reason = "No selected POIs were supplied for baseline routing"
            blocks: tuple[tuple[RouteWaypoint, ...], ...] = ()
        elif mode.travel_mode is TravelMode.TRANSIT and departure_time is None:
            fallback_reason = "Transit unavailable because no valid destination timezone was found"
            blocks = ()
        else:
            try:
                blocks = partition_baseline_origins(
                    waypoints,
                    per_request_element_limit=(
                        self._budget.limits.max_baseline_route_matrix_elements_per_request
                    ),
                )
            except ValueError as exc:
                if len(waypoints) > self._budget.limits.max_final_pois:
                    raise
                fallback_reason = str(exc)
                blocks = ()
        chunks: list[tuple[RouteMatrixRequest, RouteEvidence]] = []
        for index, origins in enumerate(blocks):
            request = RouteMatrixRequest(
                origins=list(origins),
                destinations=waypoints,
                travel_mode=mode.travel_mode.value,
                routing_preference=mode.routing_preference,
                departure_time=departure_time,
                field_mask=ROUTE_MATRIX_FIELD_MASK,
            )
            element_count = len(origins) * len(waypoints)
            self._tracer.event(
                "route_baseline_chunk_started",
                {
                    "chunk_index": index,
                    "origin_place_ids": [item.place_id for item in origins],
                    "destination_place_ids": [item.place_id for item in waypoints],
                    "requested_elements": element_count,
                    "travel_mode": request.travel_mode,
                },
            )
            try:
                evidence = await self._acquire_route_matrix(
                    request,
                    mode_reason=mode.reason,
                    purpose=RouteEvidencePurpose.BASELINE,
                    budget_key=ToolBudgetKey.BASELINE_ROUTE_MATRIX_ELEMENTS,
                    call_budget_key=ToolBudgetKey.BASELINE_ROUTE_MATRIX_CALLS,
                )
            except ToolBudgetExceededError as exc:
                evidence = unavailable_routes(
                    request,
                    mode_reason=mode.reason,
                    reason=f"Baseline route request not attempted ({exc.key.value} budget)",
                )
            chunks.append((request, evidence))
            self._tracer.event(
                "route_baseline_chunk_completed",
                {
                    "chunk_index": index,
                    "origin_place_ids": [item.place_id for item in origins],
                    "requested_elements": element_count,
                    "availability": evidence.availability.value,
                    "unavailable_reason": evidence.unavailable_reason,
                    "budget": self._route_budget_summary(),
                },
            )
        return merge_baseline_route_chunks(
            waypoints,
            chunks,
            travel_mode=mode.travel_mode.value,
            mode_reason=mode.reason,
            routing_preference=mode.routing_preference,
            departure_time=departure_time,
            fallback_reason=fallback_reason,
        )

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
        call_budget_key: ToolBudgetKey | None = None,
    ) -> RouteEvidence:
        matrix_elements = len(request.origins) * len(request.destinations)
        additional_charges = ((call_budget_key, 1),) if call_budget_key is not None else ()
        if budget_key is ToolBudgetKey.ALTERNATIVE_ROUTE_PAIRS:
            additional_charges += ((ToolBudgetKey.ALTERNATIVE_ROUTE_ELEMENTS, matrix_elements),)
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
                call_budget_key=ToolBudgetKey.ALTERNATIVE_ROUTE_MATRIX_CALLS,
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
                "collapsed_logical_pairs": [item.model_dump(mode="json") for item in logical_pairs],
                "selected_logical_pairs": [item.model_dump(mode="json") for item in selected],
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
                ToolBudgetKey.BASELINE_ROUTE_MATRIX_ELEMENTS,
                ToolBudgetKey.BASELINE_ROUTE_MATRIX_CALLS,
                ToolBudgetKey.ALTERNATIVE_ROUTE_PAIRS,
                ToolBudgetKey.ALTERNATIVE_ROUTE_MATRIX_CALLS,
            )
        }
